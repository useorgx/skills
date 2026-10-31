#!/usr/bin/env python3
"""Isolated structural validator regressions; no model or service is called."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


sys.dont_write_bytecode = True
VALIDATOR_PATH = Path(__file__).with_name("validate_ops.py")
SPEC = importlib.util.spec_from_file_location("validate_ops", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def incident_fixture():
    """A synthetic complete record; passing checks does not authenticate evidence."""
    return {
        "incident_id": "INC-EXAMPLE",
        "title": "Synthetic batch connection leak",
        "severity": "P2",
        "started_at": "2026-10-31T10:00:00Z",
        "impact": {"description": "Synthetic fixture requests timed out", "users_affected": 10},
        "timeline": [
            {"timestamp": f"2026-10-31T10:0{index}:00Z", "event": event,
             "evidence_ref": f"fixture://log/{index}"}
            for index, event in enumerate([
                "Batch started", "Pool saturation observed", "Alert received",
                "Batch stopped in fixture", "Recovery observed in fixture",
            ])
        ],
        "root_cause": {
            "description": "The batch process failed to release connections. "
            "Synthetic log samples and a bounded reproduction show that connection "
            "ownership persisted after each completed fixture task.",
        },
        "action_items": [
            {"action": action, "owner": "Fixture reliability owner", "due_date": "2026-11-02"}
            for action in ["Repair connection cleanup", "Test retry cleanup", "Review pool alerts"]
        ],
        "lessons_learned": ["Observe ownership at task completion", "Rehearse pool recovery"],
    }


class TimestampTests(unittest.TestCase):
    def test_orders_by_instant_across_timezone_offsets(self):
        self.assertTrue(validator.is_chronological([
            {"timestamp": "2026-10-31T11:00:00+02:00"},
            {"timestamp": "2026-10-31T09:00:00.500Z"},
            {"timestamp": "2026-10-31T04:01:00-05:00"},
        ]))

    def test_reversed_instants_fail(self):
        self.assertFalse(validator.is_chronological([
            {"timestamp": "2026-10-31T10:00:00Z"},
            {"timestamp": "2026-10-31T09:59:00Z"},
        ]))

    def test_invalid_or_ambiguous_timestamps_fail(self):
        for value in [None, 0, "", "not-a-time", "2026-10-31", "10:00 UTC",
                      "2026-10-31T10:00:00", "2026-10-31 10:00:00Z",
                      "2026-02-30T10:00:00Z", "2026-10-31T25:00:00Z",
                      "2026-10-31T10:00:00.1234569Z",
                      "2026-10-31T10:00:00+24:00", "2026-10-31T10:00:00+00:60"]:
            with self.subTest(value=value):
                self.assertFalse(validator.is_timestamp(value))
                self.assertFalse(validator.is_chronological([{"timestamp": value}]))

    def test_missing_or_empty_evidence_does_not_establish_chronology(self):
        for timeline in [None, [], {}, "timeline unavailable", [{}], [None]]:
            with self.subTest(timeline=timeline):
                self.assertFalse(validator.is_chronological(timeline))

    def test_mixed_naive_and_aware_timestamps_fail(self):
        self.assertFalse(validator.is_chronological([
            {"timestamp": "2026-10-31T10:00:00Z"},
            {"timestamp": "2026-10-31T09:00:00"},
        ]))


class BlameHeuristicTests(unittest.TestCase):
    def test_technical_observations_are_not_personal_blame(self):
        for text in ["Run fault injection only in the authorized isolated fixture.",
                     "The default timeout expired; the worker failed to connect.",
                     "This is a blameless postmortem.",
                     "The system should have a bounded retry policy."]:
            with self.subTest(text=text):
                self.assertTrue(validator.is_blameless({"observation": text}))

    def test_likely_personal_blame_remains_a_review_finding(self):
        for text in ["The engineer failed to check the pool.", "The operator should have known.",
                     "Bob was careless.", "Alice is to blame.", "It was their fault."]:
            with self.subTest(text=text):
                self.assertFalse(validator.is_blameless({"observation": text}))

    def test_field_names_are_not_treated_as_prose(self):
        self.assertTrue(validator.is_blameless({"fault_injection": {"blame": ["Isolated fixture"]}}))


class ValidationTests(unittest.TestCase):
    def test_complete_synthetic_record_passes_structural_checks(self):
        self.assertEqual([], validator.validate(incident_fixture(), "incident"))

    def test_unsupported_types_never_pass_vacuously(self):
        for artifact_type in ["slo", "capacity", "unknown", ""]:
            with self.subTest(artifact_type=artifact_type):
                errors = validator.validate({}, artifact_type)
                self.assertEqual(["supported_artifact_type"], [error["gate"] for error in errors])

    def test_non_object_artifacts_fail_with_a_shape_error(self):
        for artifact in [None, [], "unavailable", 0]:
            with self.subTest(artifact=artifact):
                errors = validator.validate(artifact, "incident")
                self.assertEqual(["artifact_object"], [error["gate"] for error in errors])

    def test_active_incident_with_unknown_impact_does_not_become_success(self):
        artifact = incident_fixture()
        artifact["impact"]["users_affected"] = None
        artifact["timeline"] = artifact["timeline"][:1]
        artifact["root_cause"] = {"category": "unknown", "description": "Evidence unavailable"}
        artifact["action_items"] = [{"action": "Request scoped logs", "owner": "On-call",
                                     "due_date": "2026-10-31"}]
        original = copy.deepcopy(artifact)
        errors = {error["gate"] for error in validator.validate(artifact, "incident")}
        self.assertTrue({"impact_quantified", "has_timeline", "has_root_cause"}.issubset(errors))
        self.assertEqual(original, artifact, "Validation must not fill missing evidence")

    def test_invalid_timeline_fails_even_when_field_counts_are_satisfied(self):
        artifact = incident_fixture()
        artifact["timeline"][2]["timestamp"] = "timestamp unavailable"
        errors = {error["gate"] for error in validator.validate(artifact, "incident")}
        self.assertIn("timeline_chronological", errors)
        self.assertNotIn("has_timeline", errors)

    def test_invalid_start_time_fails(self):
        artifact = incident_fixture()
        artifact["started_at"] = "2026-10-31"
        self.assertIn("has_started_at", {error["gate"] for error in validator.validate(artifact, "incident")})

    def test_cli_returns_failure_for_invalid_evidence_timestamps(self):
        artifact = incident_fixture()
        artifact["timeline"][0]["timestamp"] = "unknown"
        with tempfile.TemporaryDirectory(prefix="orion-validator-") as directory:
            artifact_path = Path(directory) / "incident.json"
            artifact_path.write_text(json.dumps(artifact))
            result = subprocess.run(
                [sys.executable, "-B", str(VALIDATOR_PATH), str(artifact_path), "--type", "incident", "--json"],
                capture_output=True, text=True, check=False,
            )
        self.assertEqual(1, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report["valid"])
        self.assertIn("timeline_chronological", {error["gate"] for error in report["errors"]})


if __name__ == "__main__":
    unittest.main()
