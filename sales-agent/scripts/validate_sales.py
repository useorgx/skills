#!/usr/bin/env python3
"""
Validate OrgX sales artifacts (battlecards, MEDDIC scorecards, outreach sequences).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_sales.py <file> --type <battlecard|meddic|sequence>

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
    "battlecard": [
        ("has_competitor", "Competitor name is required",
         lambda d: bool(d.get("competitor", "").strip())),
        ("has_segment", "Target segment is required",
         lambda d: d.get("segment") in ["enterprise", "mid-market", "smb"]),
        ("has_summary", "Quick summary is required (min 100 chars)",
         lambda d: len(d.get("quick_summary", "")) >= 100),
        ("has_differentiation", "At least 3 differentiation points required",
         lambda d: len(d.get("differentiation", [])) >= 3),
        ("differentiation_has_proof", "All differentiation points must have proof",
         lambda d: all(dp.get("proof") for dp in d.get("differentiation", []))),
        ("has_objection_handlers", "At least 4 objection handlers required",
         lambda d: len(d.get("objection_handlers", [])) >= 4),
        ("objections_have_responses", "All objections must have responses",
         lambda d: all(oh.get("response") for oh in d.get("objection_handlers", []))),
        ("has_landmines", "At least 3 landmine questions required",
         lambda d: len(d.get("landmines", [])) >= 3),
        ("has_win_strategies", "At least 2 win strategies required",
         lambda d: len(d.get("win_strategies", [])) >= 2),
    ],
    "meddic": [
        ("has_deal_name", "Deal name is required", lambda d: bool(d.get("deal_name"))),
        ("has_deal_value", "Deal value is required", lambda d: d.get("deal_value", 0) > 0),
        ("has_all_scores", "All MEDDIC elements must be scored",
         lambda d: all(
             d.get("scores", {}).get(elem, {}).get("score") is not None
             for elem in ["metrics", "economic_buyer", "decision_criteria",
                         "decision_process", "identify_pain", "champion"]
         )),
        ("scores_valid_range", "Scores must be 1-5",
         lambda d: all(
             1 <= int(d.get("scores", {}).get(elem, {}).get("score", 0)) <= 5
             for elem in ["metrics", "economic_buyer", "decision_criteria",
                         "decision_process", "identify_pain", "champion"]
             if d.get("scores", {}).get(elem, {}).get("score")
         )),
        ("has_gaps", "At least one element must identify gaps",
         lambda d: any(
             len(d.get("scores", {}).get(elem, {}).get("gaps", [])) > 0
             for elem in d.get("scores", {}).keys()
         )),
        ("has_next_steps", "At least 2 next steps required",
         lambda d: len(d.get("next_steps", [])) >= 2),
        ("next_steps_have_owners", "All next steps must have owners",
         lambda d: all(ns.get("owner") for ns in d.get("next_steps", []))),
        ("has_risk_level", "Risk level must be assessed",
         lambda d: d.get("risk_level") in ["high", "medium", "low"]),
    ],
    "sequence": [
        ("has_target_persona", "Target persona is required",
         lambda d: bool(d.get("target_persona"))),
        ("has_pain_points", "At least 2 pain points required",
         lambda d: len(d.get("pain_points", [])) >= 2),
        ("has_emails", "At least 5 emails required",
         lambda d: len(d.get("emails", [])) >= 5),
        ("emails_have_subject", "All emails must have subject lines",
         lambda d: all(e.get("subject") for e in d.get("emails", []))),
        ("emails_have_body", "All emails must have body content (min 100 chars)",
         lambda d: all(len(e.get("body", "")) >= 100 for e in d.get("emails", []))),
        ("emails_have_cta", "All emails must have CTA",
         lambda d: all(e.get("cta") for e in d.get("emails", []))),
        ("has_personalization", "Emails must contain personalization tokens",
         lambda d: any("{{" in e.get("body", "") for e in d.get("emails", []))),
        ("emails_have_timing", "All emails must have send timing",
         lambda d: all(e.get("day") is not None for e in d.get("emails", []))),
        ("has_follow_up_rules", "Follow-up rules must be defined",
         lambda d: bool(d.get("follow_up_rules"))),
    ],
}


def parse_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """Parse JSON or Markdown file into structured data."""
    content = file_path.read_text()

    if file_path.suffix == ".json":
        return json.loads(content), "json"

    if file_path.suffix == ".md":
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1)), "markdown_json"

        data = parse_markdown_battlecard(content)
        return data, "markdown"

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def parse_markdown_battlecard(content: str) -> Dict[str, Any]:
    """Parse markdown battlecard into structured data."""
    data = {
        "competitor": "",
        "segment": "",
        "quick_summary": "",
        "differentiation": [],
        "objection_handlers": [],
        "landmines": [],
        "win_strategies": []
    }

    # Extract competitor from title
    title_match = re.search(r'^#\s+(?:Battlecard:?\s*)?(.+)$', content, re.MULTILINE)
    if title_match:
        data["competitor"] = title_match.group(1).strip()

    # Extract sections
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        section_title = lines[0].lower().strip()
        section_content = '\n'.join(lines[1:])

        if 'summary' in section_title:
            data["quick_summary"] = section_content.strip()
        elif 'differentiation' in section_title or 'our advantage' in section_title:
            points = re.findall(r'[-*]\s+\*\*(.+?)\*\*:?\s*(.*)$', section_content, re.MULTILINE)
            data["differentiation"] = [{"point": p[0], "proof": p[1]} for p in points]
        elif 'objection' in section_title:
            objs = re.findall(r'\|([^|]+)\|([^|]+)\|', section_content)
            data["objection_handlers"] = [{"objection": o[0].strip(), "response": o[1].strip()}
                                          for o in objs if "Objection" not in o[0]]
        elif 'landmine' in section_title:
            questions = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["landmines"] = [{"question": q} for q in questions]
        elif 'win' in section_title and 'strateg' in section_title:
            strategies = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["win_strategies"] = [{"strategy": s} for s in strategies]

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
    parser = argparse.ArgumentParser(description="Validate OrgX sales artifacts")
    parser.add_argument("file", type=Path, help="Path to artifact file")
    parser.add_argument("--type", "-t", required=True,
                       choices=["battlecard", "meddic", "sequence"],
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
