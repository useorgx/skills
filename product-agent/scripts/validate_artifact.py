#!/usr/bin/env python3
"""
Validate the structure and declared evidence of product artifacts.
Passing does not verify source truth, customer outcomes, or release readiness.

Usage:
    python validate_artifact.py <file> --type <prd|initiative|canvas>

Exit codes:
    0 - All validations passed
    1 - Validation errors found
    2 - Invalid arguments
"""

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Tuple


def text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def records(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, dict) for item in value
    )


def strings(value: Any, *, allow_empty: bool = False) -> bool:
    return isinstance(value, list) and (allow_empty or bool(value)) and all(
        text(item) for item in value
    )


# This is a quantity grammar, not a free-text suffix. Extend units deliberately;
# unknown units should use a numeric value and a separately documented unit.
TIME_UNIT = r"(?:ms|milliseconds?|s|secs?|seconds?|mins?|minutes?|h|hrs?|hours?|days?|weeks?|months?|years?)"
COUNT_UNIT = r"(?:users?|customers?|accounts?|workspaces?|events?|tickets?|requests?|sessions?|conversions?|deals?|responses?|participants?|points?)"
SCALAR_UNIT = rf"(?:{TIME_UNIT}|{COUNT_UNIT}|bytes?|kb|mb|gb|tb|usd|eur|gbp|pp|percentage\s+points?)"
RATE_UNIT = rf"(?:{TIME_UNIT}|{COUNT_UNIT})"
PERCENT_COHORT = rf"(?:[a-z]+(?:-[a-z]+)?\s+){{0,4}}{COUNT_UNIT}"
QUANTITY_UNIT = (
    rf"(?:%(?:\s+of\s+{PERCENT_COHORT})?"
    rf"|{SCALAR_UNIT}(?:\s*(?:/|per\s+)\s*{RATE_UNIT})?"
    rf"|/\s*{RATE_UNIT})?"
)


def numeric_quantity(value: Any) -> bool:
    """Accept finite quantities, not arbitrary prose containing a digit."""
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        try:
            return math.isfinite(value)
        except OverflowError:
            return False
    if not text(value):
        return False
    match = re.fullmatch(
        r"\s*(?:<=|>=|<|>|≤|≥)?\s*[$€£]?\s*"
        r"(?P<number>[+-]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?)"
        rf"\s*(?P<unit>{QUANTITY_UNIT})\s*",
        value,
        re.I,
    )
    if not match or re.search(
        r"\b(?:unknown|unmeasured|missing|pending|not|tbd|todo|placeholder|nan|inf|infinity)\b", match["unit"], re.I
    ):
        return False
    return math.isfinite(float(match["number"].replace(",", "")))


def components(value: Any, keys: Tuple[str, ...]) -> bool:
    return records(value) and all(
        all(text(item.get(key)) for key in keys) for item in value
    )


def document_owner(data: Dict[str, Any]) -> bool:
    return text(data.get("owner")) or text(data.get("author"))


def assumptions_declared(data: Dict[str, Any]) -> bool:
    assumptions = data.get("assumptions")
    return isinstance(assumptions, list) and all(
        text(item) or (
            isinstance(item, dict)
            and text(item.get("assumption"))
            and text(item.get("validation_method"))
        ) for item in assumptions
    )


def source_or_research_plan(data: Dict[str, Any]) -> bool:
    sources = data.get("evidence", data.get("data_sources"))
    if isinstance(sources, list) and sources:
        return all(text(item) or (
            isinstance(item, dict)
            and any(text(item.get(key)) for key in ("source_ref", "url", "location", "ref"))
            and text(item.get("summary"))
        ) for item in sources)
    # Missing research is an explicit hypothesis, never a verified customer claim.
    plan = data.get("research_plan")
    return (
        isinstance(sources, list)
        and data.get("confidence_level") == "low"
        and bool(data.get("assumptions"))
        and isinstance(plan, dict)
        and all(text(plan.get(key)) for key in (
            "question", "method", "owner", "timeline", "decision_criteria"
        ))
    )


def baseline_plan(plan: Any) -> bool:
    if not isinstance(plan, dict):
        return False
    days = plan.get("within_days")
    return (
        text(plan.get("method", plan.get("measurement_method")))
        and text(plan.get("owner"))
        and isinstance(days, (int, float))
        and not isinstance(days, bool)
        and 0 < days <= 14
    )


def metric_baselines(data: Dict[str, Any]) -> bool:
    metrics = data.get("success_metrics")
    return records(metrics) and all(
        numeric_quantity(metric.get("current_baseline", metric.get("baseline")))
        or baseline_plan(metric.get(
            "baseline_measurement_plan", data.get("baseline_measurement_plan")
        )) for metric in metrics
    )


def metric_measurement(data: Dict[str, Any]) -> bool:
    metrics = data.get("success_metrics")
    return records(metrics) and all(
        text(metric.get("metric", metric.get("name")))
        and text(metric.get("measurement_method", metric.get("measurement")))
        and text(metric.get("timeline"))
        for metric in metrics
    )


# Quality gate definitions
QUALITY_GATES = {
    "prd": [
        ("has_problem_statement", "Describe the target segment's problem", lambda d: text(d.get("problem_statement"))),
        ("has_owner", "Name the accountable owner (owner or author)", document_owner),
        ("assumptions_declared", "Declare assumptions as an array, even when empty", assumptions_declared),
        ("source_or_research_plan", "Provide source references or low confidence assumptions with an owned research plan", source_or_research_plan),
        ("user_stories_format", "Provide non-empty stories with as_a, i_want, so_that", lambda d: components(d.get("user_stories"), ("as_a", "i_want", "so_that"))),
        ("criteria_format", "Provide non-empty acceptance criteria with given, when, then", lambda d: components(d.get("acceptance_criteria"), ("given", "when", "then"))),
        ("metrics_measurable", "Provide success metrics with finite numeric targets or numeric quantities with units", lambda d: records(d.get("success_metrics")) and all(numeric_quantity(m.get("target")) for m in d["success_metrics"])),
        ("metric_measurement", "Each metric needs a name, measurement method and timeline", metric_measurement),
        ("metric_baselines", "Each metric needs a numeric baseline or an owned measurement plan within 14 days", metric_baselines),
        ("bounded_scope", "Provide non-empty out_of_scope boundaries", lambda d: strings(d.get("out_of_scope"))),
        ("risks_actionable", "Provide risks with probability, impact and mitigation", lambda d: components(d.get("risks"), ("risk", "probability", "impact", "mitigation"))),
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

        raise ValueError("Markdown validation requires a fenced json object; narrative examples are illustrative")

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def validate(data: Dict[str, Any], artifact_type: str) -> List[Dict[str, str]]:
    """Run all quality gates for the artifact type."""
    errors = []
    if not isinstance(artifact_type, str) or artifact_type not in QUALITY_GATES:
        return [{"gate": "unsupported_artifact_type", "message": "Supported types: prd, initiative, canvas", "severity": "error"}]
    if not isinstance(data, dict):
        return [{"gate": "payload_object", "message": "Artifact must be a JSON object", "severity": "error"}]
    gates = QUALITY_GATES[artifact_type]

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
    # A non-object payload fails the precondition; domain gates did not run.
    gates_total = len(QUALITY_GATES[args.type]) if isinstance(data, dict) else 1

    if args.json:
        result = {
            "file": str(args.file),
            "type": args.type,
            "valid": len(errors) == 0,
            "errors": errors,
            "gates_passed": gates_total - len(errors),
            "gates_total": gates_total
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
            print(f"\nAll {gates_total} quality gates passed")
            print("Validation PASSED")

    sys.exit(0 if not errors else 1)


if __name__ == "__main__":
    main()
