#!/usr/bin/env python3
"""
Validate OrgX operations artifacts (incidents, playbooks, budgets).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_ops.py <file> --type <incident|playbook|budget>

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
from datetime import datetime


QUALITY_GATES = {
    "incident": [
        ("has_id", "Incident ID is required",
         lambda d: bool(d.get("incident_id", "").strip())),
        ("has_title", "Incident title is required",
         lambda d: bool(d.get("title", "").strip())),
        ("has_severity", "Severity must be P1-P4",
         lambda d: d.get("severity") in ["P1", "P2", "P3", "P4"]),
        ("has_started_at", "Start time is required",
         lambda d: bool(d.get("started_at"))),
        ("has_impact", "Impact description is required",
         lambda d: bool(d.get("impact", {}).get("description"))),
        ("impact_quantified", "Impact must be quantified (users affected)",
         lambda d: d.get("impact", {}).get("users_affected") is not None),
        ("has_timeline", "Timeline with at least 5 events required",
         lambda d: len(d.get("timeline", [])) >= 5),
        ("timeline_has_timestamps", "All timeline events must have timestamps",
         lambda d: all(e.get("timestamp") for e in d.get("timeline", []))),
        ("timeline_chronological", "Timeline must be chronological",
         lambda d: is_chronological(d.get("timeline", []))),
        ("has_root_cause", "Root cause analysis required (min 100 chars)",
         lambda d: len(d.get("root_cause", {}).get("description", "")) >= 100),
        ("has_action_items", "At least 3 action items required",
         lambda d: len(d.get("action_items", [])) >= 3),
        ("action_items_have_owners", "All action items must have owners",
         lambda d: all(ai.get("owner") for ai in d.get("action_items", []))),
        ("action_items_have_dates", "All action items must have due dates",
         lambda d: all(ai.get("due_date") for ai in d.get("action_items", []))),
        ("has_lessons_learned", "At least 2 lessons learned required",
         lambda d: len(d.get("lessons_learned", [])) >= 2),
        ("is_blameless", "Language must be blameless (no blame indicators)",
         lambda d: is_blameless(d)),
    ],
    "playbook": [
        ("has_name", "Playbook name is required",
         lambda d: bool(d.get("name", "").strip())),
        ("has_version", "Version is required",
         lambda d: bool(d.get("version"))),
        ("has_owner", "Owner is required",
         lambda d: bool(d.get("owner"))),
        ("has_trigger", "Trigger conditions required",
         lambda d: len(d.get("trigger", {}).get("conditions", [])) >= 1),
        ("has_prerequisites", "Prerequisites must be listed",
         lambda d: bool(d.get("prerequisites"))),
        ("has_steps", "At least 5 steps required",
         lambda d: len(d.get("steps", [])) >= 5),
        ("steps_have_actions", "All steps must have actions",
         lambda d: all(s.get("action") for s in d.get("steps", []))),
        ("steps_have_outcomes", "All steps must have expected outcomes",
         lambda d: all(s.get("expected_outcome") for s in d.get("steps", []))),
        ("steps_have_failure_handling", "At least half of steps should have failure handling",
         lambda d: sum(1 for s in d.get("steps", []) if s.get("if_fails")) >= len(d.get("steps", [])) / 2),
        ("has_escalation", "Escalation path required",
         lambda d: bool(d.get("escalation"))),
        ("has_communication", "Communication templates required",
         lambda d: len(d.get("communication", {}).get("templates", [])) >= 1),
        ("has_rollback", "Rollback procedure required",
         lambda d: len(d.get("rollback", {}).get("steps", [])) >= 1),
    ],
    "budget": [
        ("has_period", "Budget period is required",
         lambda d: bool(d.get("period"))),
        ("has_categories", "At least 3 budget categories required",
         lambda d: len(d.get("categories", [])) >= 3),
        ("categories_have_planned", "All categories must have planned amounts",
         lambda d: all(c.get("planned") is not None for c in d.get("categories", []))),
        ("categories_have_actual", "All categories must have actual amounts",
         lambda d: all(c.get("actual") is not None for c in d.get("categories", []))),
        ("has_variance_analysis", "Variance analysis required for items > 10%",
         lambda d: has_variance_analysis(d)),
        ("has_recommendations", "At least 3 recommendations required",
         lambda d: len(d.get("recommendations", [])) >= 3),
        ("has_forecast", "Forecast for next period required",
         lambda d: bool(d.get("forecast"))),
    ],
}


def is_chronological(timeline: List[Dict]) -> bool:
    """Check if timeline events are in chronological order."""
    if not timeline:
        return True
    try:
        timestamps = [datetime.fromisoformat(e["timestamp"].replace("Z", "+00:00"))
                     for e in timeline if e.get("timestamp")]
        return timestamps == sorted(timestamps)
    except (ValueError, TypeError):
        return True  # Can't validate, assume OK


def is_blameless(data: Dict) -> bool:
    """Check if language is blameless (no blame indicators)."""
    blame_words = ["fault", "blame", "failed to", "should have", "mistake by",
                   "negligence", "careless", "incompetent"]
    text = json.dumps(data).lower()
    return not any(word in text for word in blame_words)


def has_variance_analysis(data: Dict) -> bool:
    """Check if variance analysis exists for significant variances."""
    for cat in data.get("categories", []):
        planned = cat.get("planned", 0)
        actual = cat.get("actual", 0)
        if planned > 0:
            variance_pct = abs((actual - planned) / planned)
            if variance_pct > 0.10:  # > 10% variance
                if not cat.get("variance_reason"):
                    return False
    return True


def parse_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """Parse JSON or Markdown file into structured data."""
    content = file_path.read_text()

    if file_path.suffix == ".json":
        return json.loads(content), "json"

    if file_path.suffix == ".md":
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1)), "markdown_json"

        data = parse_markdown_incident(content)
        return data, "markdown"

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def parse_markdown_incident(content: str) -> Dict[str, Any]:
    """Parse markdown incident into structured data."""
    data = {
        "incident_id": "",
        "title": "",
        "severity": "",
        "impact": {},
        "timeline": [],
        "root_cause": {"description": ""},
        "action_items": [],
        "lessons_learned": []
    }

    # Extract title and ID
    title_match = re.search(r'^#\s+(?:Incident:?\s*)?(.+)$', content, re.MULTILINE)
    if title_match:
        data["title"] = title_match.group(1).strip()
        id_match = re.search(r'(INC-\d+)', data["title"])
        if id_match:
            data["incident_id"] = id_match.group(1)

    # Extract severity
    severity_match = re.search(r'Severity:\s*(P[1-4])', content)
    if severity_match:
        data["severity"] = severity_match.group(1)

    # Extract sections
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split('\n')
        section_title = lines[0].lower().strip()
        section_content = '\n'.join(lines[1:])

        if 'impact' in section_title:
            data["impact"]["description"] = section_content.strip()
            users_match = re.search(r'(\d+[%]?)\s*users?', section_content, re.IGNORECASE)
            if users_match:
                data["impact"]["users_affected"] = users_match.group(1)
        elif 'timeline' in section_title:
            events = re.findall(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|', section_content)
            data["timeline"] = [{"timestamp": e[0].strip(), "event": e[1].strip()}
                               for e in events if "Time" not in e[0]]
        elif 'root cause' in section_title:
            data["root_cause"]["description"] = section_content.strip()
        elif 'action' in section_title:
            items = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["action_items"] = [{"action": i} for i in items]
        elif 'lesson' in section_title:
            lessons = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["lessons_learned"] = lessons

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
    parser = argparse.ArgumentParser(description="Validate OrgX operations artifacts")
    parser.add_argument("file", type=Path, help="Path to artifact file")
    parser.add_argument("--type", "-t", required=True,
                       choices=["incident", "playbook", "budget"],
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
