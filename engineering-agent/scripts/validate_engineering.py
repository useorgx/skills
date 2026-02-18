#!/usr/bin/env python3
"""
Validate OrgX engineering artifacts (RFCs, ADRs, code reviews, post-mortems).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_engineering.py <file> --type <rfc|adr|review|postmortem>

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
    "rfc": [
        ("has_title", "Title is required", lambda d: bool(d.get("title", "").strip())),
        ("has_summary", "Summary is required (min 100 chars)",
         lambda d: len(d.get("summary", "")) >= 100),
        ("has_background", "Background with problem statement required",
         lambda d: len(d.get("background", "")) >= 150),
        ("background_has_data", "Background must include data/metrics",
         lambda d: any(char.isdigit() for char in d.get("background", ""))),
        ("has_proposal", "Detailed proposal is required",
         lambda d: bool(d.get("proposal", {}).get("description"))),
        ("has_alternatives", "At least 2 alternatives must be considered",
         lambda d: len(d.get("alternatives_considered", [])) >= 2),
        ("alternatives_have_reasoning", "Alternatives must have pros/cons/why_not",
         lambda d: all(
             a.get("pros") and a.get("cons") and a.get("why_not")
             for a in d.get("alternatives_considered", [])
         )),
        ("has_migration_plan", "Migration plan is required",
         lambda d: bool(d.get("migration_plan"))),
        ("migration_has_rollback", "Migration must have rollback strategy",
         lambda d: any(
             p.get("rollback") for p in d.get("migration_plan", {}).get("phases", [])
         ) or d.get("migration_plan", {}).get("rollback")),
        ("has_risks", "At least 2 risks must be identified",
         lambda d: len(d.get("risks", [])) >= 2),
        ("risks_have_mitigation", "All risks must have mitigation strategies",
         lambda d: all(r.get("mitigation") for r in d.get("risks", []))),
        ("has_success_metrics", "Success metrics required",
         lambda d: len(d.get("success_metrics", [])) >= 1),
    ],
    "adr": [
        ("has_title", "Title is required", lambda d: bool(d.get("title", "").strip())),
        ("has_status", "Status is required (proposed|accepted|deprecated|superseded)",
         lambda d: d.get("status") in ["proposed", "accepted", "deprecated", "superseded"]),
        ("has_context", "Context section required", lambda d: len(d.get("context", "")) >= 100),
        ("has_decision", "Decision section required", lambda d: len(d.get("decision", "")) >= 50),
        ("has_consequences", "Consequences section required",
         lambda d: len(d.get("consequences", [])) >= 2),
    ],
    "review": [
        ("has_pr_url", "PR URL is required", lambda d: bool(d.get("pr_url"))),
        ("has_summary", "Summary of changes required", lambda d: len(d.get("summary", "")) >= 50),
        ("has_verdict", "Verdict is required (approve|request_changes|comment)",
         lambda d: d.get("verdict") in ["approve", "request_changes", "comment"]),
        ("has_security_review", "Security review section required",
         lambda d: bool(d.get("security_review"))),
        ("security_issues_documented", "Security issues must be documented if found",
         lambda d: d.get("security_review", {}).get("passed", True) or
                   len(d.get("security_review", {}).get("issues", [])) > 0),
        ("has_test_coverage_assessment", "Test coverage assessment required",
         lambda d: bool(d.get("test_coverage"))),
        ("comments_have_location", "Review comments must specify file and line",
         lambda d: all(c.get("file") and c.get("line") is not None
                      for c in d.get("comments", []))),
    ],
    "postmortem": [
        ("has_title", "Incident title required", lambda d: bool(d.get("title", "").strip())),
        ("has_severity", "Severity level required", lambda d: d.get("severity") in ["P1", "P2", "P3", "P4"]),
        ("has_timeline", "Timeline with at least 5 events required",
         lambda d: len(d.get("timeline", [])) >= 5),
        ("has_root_cause", "Root cause analysis required",
         lambda d: len(d.get("root_cause", "")) >= 100),
        ("has_impact", "Impact assessment required",
         lambda d: bool(d.get("impact"))),
        ("impact_is_quantified", "Impact must be quantified",
         lambda d: any(char.isdigit() for char in str(d.get("impact", "")))),
        ("has_action_items", "At least 3 action items required",
         lambda d: len(d.get("action_items", [])) >= 3),
        ("action_items_have_owners", "All action items must have owners",
         lambda d: all(a.get("owner") for a in d.get("action_items", []))),
        ("has_lessons_learned", "Lessons learned section required",
         lambda d: len(d.get("lessons_learned", [])) >= 2),
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
        data = parse_markdown_rfc(content)
        return data, "markdown"

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def parse_markdown_rfc(content: str) -> Dict[str, Any]:
    """Parse markdown RFC into structured data."""
    data = {
        "title": "",
        "summary": "",
        "background": "",
        "proposal": {"description": ""},
        "alternatives_considered": [],
        "migration_plan": {"phases": []},
        "risks": [],
        "success_metrics": []
    }

    # Extract title
    title_match = re.search(r'^#\s+(?:RFC:?\s*)?(.+)$', content, re.MULTILINE)
    if title_match:
        data["title"] = title_match.group(1).strip()

    # Extract sections
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        section_title = lines[0].lower().strip()
        section_content = '\n'.join(lines[1:])

        if 'summary' in section_title:
            data["summary"] = section_content.strip()
        elif 'background' in section_title or 'context' in section_title:
            data["background"] = section_content.strip()
        elif 'proposal' in section_title:
            data["proposal"]["description"] = section_content.strip()
        elif 'alternative' in section_title:
            alts = re.findall(r'###\s+(.+?)\n(.*?)(?=###|\Z)', section_content, re.DOTALL)
            for alt_name, alt_content in alts:
                data["alternatives_considered"].append({
                    "option": alt_name.strip(),
                    "pros": re.findall(r'Pro[s]?:?\s*(.+)', alt_content),
                    "cons": re.findall(r'Con[s]?:?\s*(.+)', alt_content),
                    "why_not": re.search(r'Why not:?\s*(.+)', alt_content, re.IGNORECASE)
                })
        elif 'migration' in section_title or 'rollout' in section_title:
            phases = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["migration_plan"]["phases"] = [{"phase": p, "rollback": "rollback" in p.lower()} for p in phases]
        elif 'risk' in section_title:
            risks = re.findall(r'[-*]\s+\*\*(.+?)\*\*:?\s*(.*)$', section_content, re.MULTILINE)
            data["risks"] = [{"risk": r[0], "mitigation": r[1]} for r in risks]
        elif 'metric' in section_title or 'success' in section_title:
            metrics = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["success_metrics"] = [{"metric": m} for m in metrics]

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
    parser = argparse.ArgumentParser(description="Validate OrgX engineering artifacts")
    parser.add_argument("file", type=Path, help="Path to artifact file")
    parser.add_argument("--type", "-t", required=True,
                       choices=["rfc", "adr", "review", "postmortem"],
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
