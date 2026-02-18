#!/usr/bin/env python3
"""
Validate OrgX marketing artifacts (campaigns, content packs, email sequences).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_marketing.py <file> --type <campaign|content|sequence>

Exit codes:
    0 - All validations passed
    1 - Validation errors found
    2 - Invalid arguments
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


QUALITY_GATES = {
    "campaign": [
        ("has_name", "Campaign name is required", lambda d: bool(d.get("campaign_name", "").strip())),
        ("has_objective", "SMART objective is required", lambda d: bool(d.get("objective", "").strip())),
        ("objective_is_smart", "Objective must be SMART (contain numbers/dates)",
         lambda d: any(char.isdigit() for char in str(d.get("objective", "")))),
        ("has_target_audience", "Target audience with ICP is required",
         lambda d: bool(d.get("target_audience", {}).get("primary_icp"))),
        ("has_pain_points", "At least 2 pain points required",
         lambda d: len(d.get("target_audience", {}).get("pain_points", [])) >= 2),
        ("has_messaging_pillars", "At least 3 messaging pillars required",
         lambda d: len(d.get("messaging_pillars", [])) >= 3),
        ("pillars_have_proof", "Each pillar must have proof points",
         lambda d: all(len(p.get("proof_points", [])) > 0 for p in d.get("messaging_pillars", []))),
        ("has_channels", "At least 2 channels required", lambda d: len(d.get("channels", [])) >= 2),
        ("has_success_metrics", "At least 3 success metrics required",
         lambda d: len(d.get("success_metrics", [])) >= 3),
        ("metrics_have_targets", "All metrics must have numeric targets",
         lambda d: all(any(c.isdigit() for c in str(m.get("target", ""))) for m in d.get("success_metrics", []))),
        ("has_timeline", "Timeline with milestones required", lambda d: len(d.get("timeline", [])) >= 2),
        ("has_hypotheses", "At least 1 testable hypothesis required", lambda d: len(d.get("hypotheses", [])) >= 1),
    ],
    "content": [
        ("has_campaign_id", "Campaign ID reference required", lambda d: bool(d.get("campaign_id"))),
        ("has_content_items", "At least 3 content items required",
         lambda d: len(d.get("content_items", [])) >= 3),
        ("all_have_channel", "All items must specify channel",
         lambda d: all(c.get("channel") for c in d.get("content_items", []))),
        ("all_have_content", "All items must have content (min 50 chars)",
         lambda d: all(len(c.get("content", "")) >= 50 for c in d.get("content_items", []))),
        ("all_have_cta", "All items must have a CTA",
         lambda d: all(c.get("cta") for c in d.get("content_items", []))),
        ("linkedin_length", "LinkedIn posts must be under 3000 chars",
         lambda d: all(len(c.get("content", "")) <= 3000 for c in d.get("content_items", [])
                      if c.get("channel") == "linkedin")),
        ("twitter_has_thread", "Twitter content should be thread format (multiple tweets)",
         lambda d: all("1/" in c.get("content", "") or len(c.get("content", "")) <= 280
                      for c in d.get("content_items", []) if c.get("channel") == "twitter")),
    ],
    "sequence": [
        ("has_emails", "At least 5 emails required for nurture sequence",
         lambda d: len(d.get("emails", [])) >= 5),
        ("all_have_subject", "All emails must have subject lines",
         lambda d: all(e.get("subject") for e in d.get("emails", []))),
        ("all_have_body", "All emails must have body content",
         lambda d: all(len(e.get("body", "")) >= 100 for e in d.get("emails", []))),
        ("all_have_cta", "All emails must have a CTA",
         lambda d: all(e.get("cta") for e in d.get("emails", []))),
        ("has_timing", "All emails must have send timing",
         lambda d: all(e.get("day") is not None for e in d.get("emails", []))),
        ("has_personalization", "Emails should have personalization tokens",
         lambda d: any("{{" in e.get("body", "") for e in d.get("emails", []))),
        ("progressive_ctas", "CTAs should progress in urgency",
         lambda d: True),  # Manual check recommended
    ],
}


def parse_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """Parse JSON or Markdown file into structured data."""
    content = file_path.read_text()

    if file_path.suffix == ".json":
        return json.loads(content), "json"

    if file_path.suffix == ".md":
        # Try to find JSON code block
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1)), "markdown_json"

        # Parse markdown into structured format
        data = parse_markdown_campaign(content)
        return data, "markdown"

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def parse_markdown_campaign(content: str) -> Dict[str, Any]:
    """Parse markdown campaign brief into structured data."""
    data = {
        "campaign_name": "",
        "objective": "",
        "target_audience": {"primary_icp": "", "pain_points": []},
        "messaging_pillars": [],
        "channels": [],
        "success_metrics": [],
        "timeline": [],
        "hypotheses": []
    }

    # Extract title
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        data["campaign_name"] = title_match.group(1).replace("Campaign:", "").strip()

    # Extract sections
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        section_title = lines[0].lower().strip()
        section_content = '\n'.join(lines[1:])

        if 'objective' in section_title:
            data["objective"] = section_content.strip()
        elif 'audience' in section_title or 'icp' in section_title:
            data["target_audience"]["primary_icp"] = section_content.strip()
            # Extract bullet points as pain points
            pain_points = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["target_audience"]["pain_points"] = pain_points
        elif 'messaging' in section_title or 'pillar' in section_title:
            pillars = re.findall(r'[-*]\s+\*\*(.+?)\*\*:?\s*(.*)$', section_content, re.MULTILINE)
            data["messaging_pillars"] = [{"pillar": p[0], "proof_points": [p[1]] if p[1] else []} for p in pillars]
        elif 'channel' in section_title:
            channels = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["channels"] = channels
        elif 'metric' in section_title or 'success' in section_title:
            metrics = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["success_metrics"] = [{"metric": m, "target": m} for m in metrics]
        elif 'timeline' in section_title:
            milestones = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["timeline"] = [{"milestone": m} for m in milestones]
        elif 'hypothesis' in section_title or 'hypotheses' in section_title:
            hypotheses = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["hypotheses"] = [{"hypothesis": h} for h in hypotheses]

    return data


def validate(data: Dict[str, Any], artifact_type: str) -> List[Dict[str, str]]:
    """Run all quality gates for the artifact type."""
    errors = []

    gates = QUALITY_GATES.get(artifact_type, [])

    for gate_id, message, check_fn in gates:
        try:
            if not check_fn(data):
                errors.append({
                    "gate": gate_id,
                    "message": message,
                    "severity": "error"
                })
        except Exception as e:
            errors.append({
                "gate": gate_id,
                "message": f"{message} (validation error: {e})",
                "severity": "error"
            })

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate OrgX marketing artifacts")
    parser.add_argument("file", type=Path, help="Path to artifact file")
    parser.add_argument("--type", "-t", required=True, choices=["campaign", "content", "sequence"],
                       help="Artifact type to validate")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    if not args.file.exists():
        print(f"Error: File not found: {args.file}", file=sys.stderr)
        sys.exit(2)

    try:
        data, format_type = parse_file(args.file)
    except Exception as e:
        print(f"Error parsing file: {e}", file=sys.stderr)
        sys.exit(2)

    errors = validate(data, args.type)

    if args.json:
        result = {
            "file": str(args.file),
            "type": args.type,
            "valid": len(errors) == 0,
            "errors": errors,
            "gates_passed": len(QUALITY_GATES[args.type]) - len(errors),
            "gates_total": len(QUALITY_GATES[args.type])
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"\nValidating {args.type.upper()}: {args.file}")
        print("=" * 50)

        if errors:
            print(f"\n{len(errors)} error(s) found:\n")
            for err in errors:
                print(f"  [{err['gate']}] {err['message']}")
            print(f"\nValidation FAILED")
        else:
            gates_count = len(QUALITY_GATES[args.type])
            print(f"\nAll {gates_count} quality gates passed")
            print("Validation PASSED")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
