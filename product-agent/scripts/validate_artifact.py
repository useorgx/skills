#!/usr/bin/env python3
"""
Validate OrgX product artifacts (PRDs, initiatives, canvases).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_artifact.py <file> --type <prd|initiative|canvas>

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

# Quality gate definitions
QUALITY_GATES = {
    "prd": [
        ("has_problem_statement", "Problem statement is required", lambda d: bool(d.get("problem_statement", "").strip())),
        ("has_user_stories", "At least 2 user stories required", lambda d: len(d.get("user_stories", [])) >= 2),
        ("user_stories_format", "User stories must have as_a, i_want, so_that", lambda d: all(
            all(k in s for k in ["as_a", "i_want", "so_that"]) for s in d.get("user_stories", [])
        )),
        ("has_acceptance_criteria", "At least 3 acceptance criteria required", lambda d: len(d.get("acceptance_criteria", [])) >= 3),
        ("criteria_format", "Acceptance criteria must have given, when, then", lambda d: all(
            all(k in c for k in ["given", "when", "then"]) for c in d.get("acceptance_criteria", [])
        )),
        ("has_success_metrics", "At least 2 measurable success metrics required", lambda d: len(d.get("success_metrics", [])) >= 2),
        ("metrics_measurable", "Success metrics must have numeric targets", lambda d: all(
            any(char.isdigit() for char in str(m.get("target", ""))) for m in d.get("success_metrics", [])
        )),
    ],
    "initiative": [
        ("has_title", "Title is required", lambda d: bool(d.get("title", "").strip())),
        ("has_summary", "Summary is required (min 50 chars)", lambda d: len(d.get("summary", "")) >= 50),
        ("has_success_metrics", "At least 2 success metrics required", lambda d: len(d.get("success_metrics", [])) >= 2),
        ("has_milestones", "3-5 milestones required", lambda d: 3 <= len(d.get("milestones", [])) <= 5),
        ("milestones_have_dates", "All milestones must have due dates", lambda d: all(
            bool(m.get("due_date")) for m in d.get("milestones", [])
        )),
        ("milestones_have_deliverables", "All milestones must have deliverables", lambda d: all(
            len(m.get("deliverables", [])) > 0 for m in d.get("milestones", [])
        )),
    ],
    "canvas": [
        ("has_problem", "Problem section required", lambda d: bool(d.get("problem", "").strip())),
        ("has_solution", "Solution section required", lambda d: bool(d.get("solution", "").strip())),
        ("has_value_proposition", "Value proposition required", lambda d: bool(d.get("value_proposition", "").strip())),
        ("has_customer_segments", "At least 2 customer segments required", lambda d: len(d.get("customer_segments", [])) >= 2),
        ("has_channels", "At least 1 channel required", lambda d: len(d.get("channels", [])) >= 1),
        ("has_metrics", "Key metrics required", lambda d: len(d.get("key_metrics", [])) >= 2),
    ],
}


def parse_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """Parse JSON or Markdown file into structured data."""
    content = file_path.read_text()

    if file_path.suffix == ".json":
        return json.loads(content), "json"

    # Parse Markdown with YAML frontmatter or JSON code blocks
    if file_path.suffix == ".md":
        # Try to find JSON code block
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1)), "markdown_json"

        # Parse markdown sections into dict
        data = {}
        current_section = None
        current_content = []

        for line in content.split("\n"):
            if line.startswith("## "):
                if current_section:
                    data[current_section] = "\n".join(current_content).strip()
                current_section = line[3:].lower().replace(" ", "_")
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            data[current_section] = "\n".join(current_content).strip()

        return data, "markdown"

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def validate(data: Dict[str, Any], artifact_type: str) -> List[Dict[str, str]]:
    """Run all quality gates for the artifact type."""
    errors = []
    warnings = []

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
    parser = argparse.ArgumentParser(description="Validate OrgX product artifacts")
    parser.add_argument("file", type=Path, help="Path to artifact file")
    parser.add_argument("--type", "-t", required=True, choices=["prd", "initiative", "canvas"],
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
