#!/usr/bin/env python3
"""Isolated structure regressions; no real campaign, outreach or outcome proof."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


VALIDATOR_PATH = Path(__file__).with_name("validate_marketing.py")
SPEC = importlib.util.spec_from_file_location("marketing_validator", VALIDATOR_PATH)
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def campaign(channels):
    """Synthetic planned targets satisfy the legacy structural fields only."""
    return {
        "campaign_name": "Synthetic channel selection fixture",
        "objective": "Review 3 synthetic drafts by 2026-12-01",
        "target_audience": {
            "primary_icp": "Synthetic operations teams",
            "pain_points": ["Scattered draft evidence", "Unclear review ownership"],
        },
        "messaging_pillars": [
            {"pillar": name, "proof_points": ["Synthetic fixture reference"]}
            for name in ["Traceability", "Ownership", "Review"]
        ],
        "channels": channels,
        "success_metrics": [
            {"metric": name, "target": "Plan: 1 synthetic fixture"}
            for name in ["Drafts reviewed", "Sources retained", "Gaps named"]
        ],
        "timeline": [{"milestone": "Prepare fixture"}, {"milestone": "Review fixture"}],
        "hypotheses": ["An evidence-linked draft may simplify review; untested."],
    }


class MarketingChannelStructureTests(unittest.TestCase):
    def test_single_channel_does_not_force_an_unsupported_second_channel(self):
        self.assertEqual(VALIDATOR.validate(campaign(["community workshop"]), "campaign"), [])

    def test_multiple_channels_remain_supported(self):
        self.assertEqual(VALIDATOR.validate(campaign(["email", "community workshop"]), "campaign"), [])

    def test_missing_channel_blocks_campaign(self):
        errors = VALIDATOR.validate(campaign([]), "campaign")
        self.assertIn("has_channels", [error["gate"] for error in errors])

    def test_only_nonblank_channel_name_lists_satisfy_the_gate(self):
        for channels in [None, "email", {"email": True}, [""], ["  "], [42], ["email", ""]]:
            with self.subTest(channels=channels):
                errors = VALIDATOR.validate(campaign(channels), "campaign")
                self.assertIn("has_channels", [error["gate"] for error in errors])

    def test_single_channel_does_not_bypass_other_structural_gates(self):
        artifact = campaign(["community workshop"])
        artifact["hypotheses"] = []
        errors = VALIDATOR.validate(artifact, "campaign")
        self.assertEqual([error["gate"] for error in errors], ["has_hypotheses"])

    def test_markdown_parser_retains_one_evidenced_channel(self):
        parsed = VALIDATOR.parse_markdown_campaign("# Campaign: Fixture\n\n## Channels\n- Community workshop\n")
        self.assertEqual(parsed["channels"], ["Community workshop"])
        errors = VALIDATOR.validate(parsed, "campaign")
        self.assertNotIn("has_channels", [error["gate"] for error in errors])

    def test_cli_accepts_single_channel_structure_and_rejects_no_channel(self):
        with tempfile.TemporaryDirectory(prefix="mark-skill-fixture-") as directory:
            artifact_path = Path(directory) / "campaign.json"
            for channels, expected in [(["community workshop"], 0), ([], 1)]:
                artifact_path.write_text(json.dumps(campaign(channels)))
                result = subprocess.run(
                    [sys.executable, "-B", str(VALIDATOR_PATH), str(artifact_path), "--type", "campaign", "--json"],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, expected, result.stderr)
                report = json.loads(result.stdout)
                self.assertEqual(report["valid"], expected == 0)


if __name__ == "__main__":
    unittest.main()
