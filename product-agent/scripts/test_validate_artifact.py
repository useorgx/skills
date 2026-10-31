"""Isolated synthetic regression cases; no source truth or customer outcome claim."""

import copy
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from validate_artifact import numeric_quantity, parse_file, validate


VALID_PRD = {
    "feature_name": "Preview CSV column mapping",
    "owner": "Product owner",
    "problem_statement": "First-time workspace admins cannot identify a mismatched CSV column before importing.",
    "evidence": [{
        "source_ref": "fixture://research/import-17",
        "summary": "Synthetic rehearsal interview; not customer research.",
    }],
    "assumptions": [{
        "assumption": "A preview will help admins correct the mapping before import.",
        "validation_method": "Compare completion of the bounded import task in a prototype.",
    }],
    "user_stories": [{
        "as_a": "first-time workspace admin",
        "i_want": "to preview how the selected CSV headers map to destination fields",
        "so_that": "I can correct the mapping before importing",
    }],
    "acceptance_criteria": [{
        "given": "a CSV file with a mismatched required column",
        "when": "the admin opens the import preview",
        "then": "the required field is marked unmapped and import stays disabled",
    }],
    "success_metrics": [{
        "metric": "Correct mapping in the prototype task",
        "current_baseline": "40%",
        "target": "80%",
        "measurement_method": "Fixture task completion counts divided by assigned prototype tasks",
        "timeline": "At the end of the rehearsal session",
    }],
    "out_of_scope": ["Saving reusable import templates"],
    "risks": [{
        "risk": "Admins may skip the preview without noticing a mismatched field",
        "probability": "medium",
        "impact": "medium",
        "mitigation": "Observe whether the required-field warning changes task behavior",
    }],
}


class ProductArtifactValidationTest(unittest.TestCase):
    def setUp(self):
        self.prd = copy.deepcopy(VALID_PRD)

    def gates(self, data=None):
        return {error["gate"] for error in validate(self.prd if data is None else data, "prd")}

    def test_one_bounded_hypothesis_needs_no_artificial_field_counts(self):
        self.assertEqual(validate(self.prd, "prd"), [])

    def test_unsupported_types_and_non_object_payloads_fail_closed(self):
        for artifact_type in ("research-brief", "", None, []):
            with self.subTest(artifact_type=artifact_type):
                self.assertEqual(validate({}, artifact_type)[0]["gate"], "unsupported_artifact_type")
        for value in ([], "not an object", False, 1, None):
            with self.subTest(value=value):
                self.assertEqual(validate(value, "prd")[0]["gate"], "payload_object")

    def test_original_false_positive_is_rejected(self):
        invalid = {
            "problem_statement": "We will build AI magic.",
            "user_stories": [dict(as_a="", i_want="", so_that="") for _ in range(2)],
            "acceptance_criteria": [dict(given="", when="", then="") for _ in range(3)],
            "success_metrics": [dict(target="unknown 1") for _ in range(2)],
        }
        self.assertTrue({"user_stories_format", "criteria_format", "metrics_measurable"}.issubset(self.gates(invalid)))

    def test_blank_or_malformed_story_and_criterion_components_are_rejected(self):
        for field, key, gate in (
            ("user_stories", "i_want", "user_stories_format"),
            ("acceptance_criteria", "then", "criteria_format"),
        ):
            for value in ("", " \n\t", None, [], 123, False):
                with self.subTest(field=field, value=value):
                    candidate = copy.deepcopy(self.prd)
                    candidate[field][0][key] = value
                    self.assertIn(gate, self.gates(candidate))
            for value in ([], "pretend array", {}, ["not an object"], [None]):
                with self.subTest(field=field, value=value):
                    candidate = copy.deepcopy(self.prd)
                    candidate[field] = value
                    self.assertIn(gate, self.gates(candidate))

    def test_numeric_targets_accept_canonical_quantities_but_not_placeholder_prose(self):
        for value in (0, 1.5, "45%", "80% of enterprise users", "<10%", "<5/week", "15/week", "$1,200", "100 ms", "100ms", "≥ 5 requests/day", "≥5requests/day", "1e2", "1e2ms", "2 requests per day"):
            with self.subTest(value=value):
                self.assertTrue(numeric_quantity(value))
        for value in ("unknown 1", "TBD 42", "1 unknown", "1 not measured", "1 missing", "1 pending", "1eNaN", "1e", "1 arbitrary-unit", "80% of unknown users", "1 or 2", "about 3", "1.2.3", "NaN", "Infinity", "1e999", math.nan, math.inf, -math.inf, True, None, {}, 10**400):
            with self.subTest(value=repr(value)):
                self.assertFalse(numeric_quantity(value))

    def test_placeholder_quantities_cannot_bypass_either_baseline_or_target(self):
        for value in ("1 not measured", "1 missing", "1 pending", "1eNaN", "1e"):
            for fields in (("current_baseline",), ("target",), ("current_baseline", "target")):
                candidate = copy.deepcopy(self.prd)
                metric = candidate["success_metrics"][0]
                for field in fields:
                    metric[field] = value
                with self.subTest(value=value, fields=fields):
                    gates = self.gates(candidate)
                    if "current_baseline" in fields:
                        self.assertIn("metric_baselines", gates)
                    if "target" in fields:
                        self.assertIn("metrics_measurable", gates)
                    self.assertTrue(gates)

    def test_valid_baseline_plan_cannot_excuse_an_invalid_target(self):
        metric = self.prd["success_metrics"][0]
        metric.update(current_baseline="1 missing", target="1 pending")
        metric["baseline_measurement_plan"] = {
            "method": "Read assigned tasks and completions",
            "owner": "Analytics owner", "within_days": 7,
        }
        self.assertNotIn("metric_baselines", self.gates())
        self.assertIn("metrics_measurable", self.gates())
        metric["target"] = "80%"
        self.assertEqual(self.gates(), set())

    def test_each_metric_needs_named_measurement_timeline_and_real_target(self):
        for key in ("metric", "measurement_method", "timeline", "target"):
            candidate = copy.deepcopy(self.prd)
            del candidate["success_metrics"][0][key]
            with self.subTest(key=key):
                self.assertTrue(self.gates(candidate) & {"metric_measurement", "metrics_measurable"})
        self.prd["success_metrics"].append({"target": "1 unknown"})
        self.assertIn("metrics_measurable", self.gates())

    def test_absent_baseline_requires_owned_measurement_within_fourteen_days(self):
        self.prd["success_metrics"][0]["current_baseline"] = "TBD"
        self.assertIn("metric_baselines", self.gates())
        plan = {"method": "Read the initial assigned-task denominator and completion events", "owner": "Analytics owner", "within_days": 14}
        self.prd["success_metrics"][0]["baseline_measurement_plan"] = plan
        self.assertEqual(self.gates(), set())
        for days in (0, 15, True, "7", math.inf, math.nan, None):
            plan["within_days"] = days
            with self.subTest(days=days):
                self.assertIn("metric_baselines", self.gates())
        plan["within_days"] = 7
        plan["owner"] = " "
        self.assertIn("metric_baselines", self.gates())

    def test_canonical_aliases_and_shared_baseline_plan_are_supported(self):
        self.prd["author"] = self.prd.pop("owner")
        metric = self.prd["success_metrics"][0]
        metric["baseline"] = metric.pop("current_baseline")
        metric["measurement"] = metric.pop("measurement_method")
        self.assertEqual(self.gates(), set())
        metric["baseline"] = "TBD"
        self.prd["baseline_measurement_plan"] = {"measurement_method": "Read assigned-task and completion events", "owner": "Analytics owner", "within_days": 7}
        self.assertEqual(self.gates(), set())

    def test_sources_or_an_explicit_owned_research_gap_are_required(self):
        self.prd["evidence"] = []
        self.assertIn("source_or_research_plan", self.gates())
        self.prd.update(confidence_level="low", research_plan={
            "question": "Do admins fail to detect mapping errors?",
            "method": "Observe the import task using the prototype",
            "owner": "Research owner",
            "timeline": "Before the delivery decision",
            "decision_criteria": "Revise or stop if the warning does not change mapping errors",
        })
        self.assertEqual(self.gates(), set())
        self.prd["confidence_level"] = "high"
        self.assertIn("source_or_research_plan", self.gates())
        self.prd["confidence_level"] = "low"
        self.prd["research_plan"]["owner"] = " "
        self.assertIn("source_or_research_plan", self.gates())

    def test_malformed_sources_assumptions_scope_and_risks_are_rejected(self):
        for field, value, gate in (
            ("evidence", [{}], "source_or_research_plan"),
            ("evidence", [{"source_ref": "fixture://id"}], "source_or_research_plan"),
            ("assumptions", None, "assumptions_declared"),
            ("assumptions", [{}], "assumptions_declared"),
            ("out_of_scope", [], "bounded_scope"),
            ("out_of_scope", [" "], "bounded_scope"),
            ("risks", [{"risk": "unknown"}], "risks_actionable"),
            ("owner", " ", "has_owner"),
        ):
            candidate = copy.deepcopy(self.prd)
            candidate[field] = value
            with self.subTest(field=field, value=value):
                self.assertIn(gate, self.gates(candidate))
        self.prd["assumptions"] = []
        self.assertEqual(self.gates(), set())

    def test_json_and_markdown_json_roundtrip_without_misreading_narrative(self):
        with tempfile.TemporaryDirectory() as directory:
            for name, content in (
                ("prd.json", json.dumps(self.prd)),
                ("prd.md", "# Synthetic PRD\n\n```json\n" + json.dumps(self.prd) + "\n```\n"),
            ):
                path = Path(directory) / name
                path.write_text(content)
                self.assertEqual(validate(parse_file(path)[0], "prd"), [])
            path = Path(directory) / "narrative.md"
            path.write_text("## User Stories\n\nThis prose is not a structured story array.")
            with self.assertRaisesRegex(ValueError, "fenced json"):
                parse_file(path)

    def test_cli_reports_validity_and_exit_status(self):
        script = Path(__file__).with_name("validate_artifact.py")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prd.json"
            path.write_text(json.dumps(self.prd))
            result = subprocess.run([sys.executable, str(script), str(path), "--type", "prd", "--json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["valid"])
            self.prd["success_metrics"][0]["target"] = "unknown 1"
            path.write_text(json.dumps(self.prd))
            result = subprocess.run([sys.executable, str(script), str(path), "--type", "prd", "--json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertFalse(json.loads(result.stdout)["valid"])
            path.write_text("[]")
            result = subprocess.run([sys.executable, str(script), str(path), "--type", "prd", "--json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(json.loads(result.stdout)["gates_passed"], 0)
            result = subprocess.run([sys.executable, str(script), str(path), "--type", "research-brief"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
