"""Offline adversarial regression checks; no browsers or providers are called."""
import copy
import unittest

from validate_design import validate


def audit():
    return {
        "scope": "Synthetic checkout at fixture revision a",
        "wcag_level": "AA",
        "target_revision": "fixture-a",
        "summary": {"total_issues": 0, "critical_count": 0,
                    "major_count": 0, "minor_count": 0},
        "issues": [],
        "testing_notes": {
            "screen_readers_tested": [], "screen_reader_status": "not_tested",
            "screen_reader_evidence": [],
            "limitations": ["No screen reader was available; no conformance claim."],
        },
        "recommendations": [],
    }


def observed_audit():
    result = audit()
    result["testing_notes"] = {
        "screen_readers_tested": ["Fixture screen reader"],
        "screen_reader_status": "observed",
        "screen_reader_evidence": [{
            "technology": "Fixture screen reader", "outcome": "fail",
            "target_revision": "fixture-a",
            "evidence_ref": "fixture://checkout/announcement-transcript",
        }],
        "limitations": ["Synthetic evidence exercises validation, not live QA."],
    }
    return result


def gates(document, artifact_type="audit"):
    return {error["gate"] for error in validate(document, artifact_type)}


class DesignEvidenceValidation(unittest.TestCase):
    def test_honest_untested_report_is_valid_without_invented_findings(self):
        self.assertEqual(validate(audit(), "audit"), [])

    def test_claimed_screen_reader_without_record_is_rejected(self):
        document = audit()
        document["testing_notes"]["screen_readers_tested"] = ["NVDA"]
        self.assertIn("screen_reader_evidence", gates(document))

    def test_claimed_screen_reader_with_only_name_cannot_pass(self):
        document = observed_audit()
        document["testing_notes"]["screen_reader_evidence"] = [{"technology": "Fixture screen reader"}]
        self.assertIn("screen_reader_evidence", gates(document))

    def test_observed_failure_is_not_rewritten_as_unperformed(self):
        self.assertEqual(validate(observed_audit(), "audit"), [])

    def test_other_revision_evidence_is_rejected(self):
        document = observed_audit()
        document["testing_notes"]["screen_reader_evidence"][0]["target_revision"] = "fixture-b"
        self.assertIn("screen_reader_evidence", gates(document))

    def test_other_technology_evidence_is_rejected(self):
        document = observed_audit()
        document["testing_notes"]["screen_reader_evidence"][0]["technology"] = "Other fixture reader"
        self.assertIn("screen_reader_evidence", gates(document))

    def test_duplicate_reader_evidence_is_rejected(self):
        document = observed_audit()
        document["testing_notes"]["screen_readers_tested"] *= 2
        document["testing_notes"]["screen_reader_evidence"] *= 2
        self.assertIn("screen_reader_evidence", gates(document))

    def test_untested_requires_explicit_limitation(self):
        document = audit()
        document["testing_notes"]["limitations"] = []
        self.assertIn("screen_reader_evidence", gates(document))

    def test_untested_cannot_retain_observed_evidence(self):
        document = audit()
        document["testing_notes"]["screen_reader_evidence"] = observed_audit()["testing_notes"]["screen_reader_evidence"]
        self.assertIn("screen_reader_evidence", gates(document))

    def test_contradictory_findings_total_is_rejected(self):
        document = audit()
        document["summary"]["total_issues"] = 99
        self.assertIn("counts_match_findings", gates(document))

    def test_counts_must_be_integers_and_cannot_use_boolean(self):
        for value in (False, 0.0, "0", -1):
            with self.subTest(value=value):
                document = audit()
                document["summary"]["minor_count"] = value
                self.assertIn("counts_match_findings", gates(document))

    def test_severity_counts_match_actual_findings(self):
        document = audit()
        document["issues"] = [{"severity": "major", "wcag_criterion": "4.1.3",
                               "location": "fixture status", "remediation": "Announce the status."}]
        document["summary"] = {"total_issues": 1, "critical_count": 0,
                               "major_count": 1, "minor_count": 0}
        document["recommendations"] = ["Retest the fixture announcement after repair."]
        self.assertEqual(validate(document, "audit"), [])
        document["summary"]["major_count"] = 0
        self.assertIn("counts_match_findings", gates(document))

    def test_malformed_containers_fail_closed(self):
        for key in ("issues", "summary", "testing_notes"):
            with self.subTest(key=key):
                document = audit()
                document[key] = "not a container"
                self.assertTrue(validate(document, "audit"))

    def test_unknown_artifact_types_do_not_pass_zero_checks(self):
        for artifact_type in ("interaction", "research-plan", "critique", "motion", "dark-mode", "breakpoints", "typo"):
            with self.subTest(artifact_type=artifact_type):
                self.assertEqual(gates({}, artifact_type), {"unsupported_type"})

    def test_non_object_document_fails_closed(self):
        for document in (None, [], "text", 42):
            with self.subTest(document=document):
                self.assertEqual(gates(document), {"invalid_document"})

    def test_spacing_check_computes_instead_of_always_passing(self):
        document = {"tokens": {"spacing": {"a": {"value": "4px"}, "b": {"value": "0.5rem"}}}}
        self.assertNotIn("spacing_values_valid", gates(document, "tokens"))
        for value in ("-4px", "banana", True, "NaN", "4px extra", "٤px"):
            with self.subTest(value=value):
                invalid = copy.deepcopy(document)
                invalid["tokens"]["spacing"]["b"]["value"] = value
                self.assertIn("spacing_values_valid", gates(invalid, "tokens"))

    def test_supported_color_formats_accept_bounded_integer_channels(self):
        for value in ("#000000", "#AbCdEf", "rgb(0, 127, 255)", " RGB( 255 , 0, 12 ) "):
            with self.subTest(value=value):
                document = {"tokens": {"color": {"text": {"value": value}}}}
                self.assertNotIn("colors_valid_format", gates(document, "tokens"))

    def test_malformed_and_unsupported_colors_cannot_pass_by_prefix(self):
        for value in ("rgbgarbage", "rgb(256, 0, 0)", "rgb(-1, 0, 0)",
                      "rgb(1, 2)", "rgb(1, 2, 3) trailing", "#1234567",
                      "#123", "rgb(1.5, 0, 0)", "rgb(100%, 0%, 0%)",
                      "rgba(1, 2, 3, 1)", "rgb(1 2 3)", "rgb(١, ٢, ٣)", True, None):
            with self.subTest(value=value):
                document = {"tokens": {"color": {"text": {"value": value}}}}
                self.assertIn("colors_valid_format", gates(document, "tokens"))


if __name__ == "__main__":
    unittest.main()
