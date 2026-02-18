#!/usr/bin/env python3
"""
Validate OrgX orchestration artifacts (initiatives, delegations, syntheses).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_orchestration.py <file> --type <initiative|delegation|synthesis>

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


VALID_AGENTS = [
    "product-agent", "engineering-agent", "marketing-agent",
    "sales-agent", "design-agent", "operations-agent", "orchestrator-agent"
]


QUALITY_GATES = {
    "initiative": [
        ("has_title", "Initiative title is required",
         lambda d: bool(d.get("title", "").strip())),
        ("has_summary", "Summary is required (min 50 chars)",
         lambda d: len(d.get("summary", "")) >= 50),
        ("has_owner", "Initiative owner is required",
         lambda d: bool(d.get("owner"))),
        ("has_target_date", "Target completion date required",
         lambda d: bool(d.get("target_date"))),
        ("has_success_metrics", "At least 2 success metrics required",
         lambda d: len(d.get("success_metrics", [])) >= 2),
        ("metrics_have_targets", "All metrics must have targets",
         lambda d: all(m.get("target") for m in d.get("success_metrics", []))),
        ("has_workstreams", "3-5 workstreams required",
         lambda d: 3 <= len(d.get("workstreams", [])) <= 5),
        ("workstreams_have_agents", "All workstreams must be assigned to agents",
         lambda d: all(ws.get("agent") for ws in d.get("workstreams", []))),
        ("workstreams_valid_agents", "All agents must be valid",
         lambda d: all(ws.get("agent") in VALID_AGENTS for ws in d.get("workstreams", []))),
        ("workstreams_have_goals", "All workstreams must have goals",
         lambda d: all(ws.get("goal") for ws in d.get("workstreams", []))),
        ("workstreams_have_milestones", "All workstreams must have at least 2 milestones",
         lambda d: all(len(ws.get("milestones", [])) >= 2 for ws in d.get("workstreams", []))),
        ("has_risks", "At least 2 risks must be identified",
         lambda d: len(d.get("risks", [])) >= 2),
        ("risks_have_mitigation", "All risks must have mitigation",
         lambda d: all(r.get("mitigation") for r in d.get("risks", []))),
        ("no_circular_dependencies", "No circular dependencies allowed",
         lambda d: check_no_circular_deps(d.get("workstreams", []))),
    ],
    "delegation": [
        ("has_target_agent", "Target agent is required",
         lambda d: bool(d.get("target_agent"))),
        ("valid_agent", "Target agent must be valid",
         lambda d: d.get("target_agent") in VALID_AGENTS),
        ("has_context", "Context section is required",
         lambda d: bool(d.get("context"))),
        ("context_has_background", "Context must include background",
         lambda d: bool(d.get("context", {}).get("background"))),
        ("has_task", "Task section is required",
         lambda d: bool(d.get("task"))),
        ("task_has_objective", "Clear objective is required",
         lambda d: bool(d.get("task", {}).get("objective"))),
        ("has_requirements", "At least 2 requirements needed",
         lambda d: len(d.get("task", {}).get("requirements", [])) >= 2),
        ("has_quality", "Quality section is required",
         lambda d: bool(d.get("quality"))),
        ("has_acceptance_criteria", "At least 2 acceptance criteria needed",
         lambda d: len(d.get("quality", {}).get("acceptance_criteria", [])) >= 2),
        ("has_deadline", "Deadline is required",
         lambda d: bool(d.get("timeline", {}).get("deadline"))),
        ("has_output_format", "Expected output format is required",
         lambda d: bool(d.get("handoff", {}).get("output_format"))),
    ],
    "synthesis": [
        ("has_initiative_ref", "Initiative reference is required",
         lambda d: bool(d.get("initiative_id"))),
        ("has_inputs", "At least 2 input sources required",
         lambda d: len(d.get("inputs", [])) >= 2),
        ("inputs_have_sources", "All inputs must have source agents",
         lambda d: all(i.get("agent") for i in d.get("inputs", []))),
        ("has_conflicts_section", "Conflicts section is required",
         lambda d: "conflicts" in d),
        ("conflicts_resolved", "All conflicts must be resolved",
         lambda d: all(c.get("resolution") for c in d.get("conflicts", []))),
        ("has_synthesis", "Synthesized output is required",
         lambda d: bool(d.get("synthesis"))),
        ("synthesis_complete", "Synthesis must be at least 200 chars",
         lambda d: len(d.get("synthesis", "")) >= 200),
        ("has_recommendations", "At least 3 recommendations required",
         lambda d: len(d.get("recommendations", [])) >= 3),
        ("has_next_steps", "Next steps are required",
         lambda d: len(d.get("next_steps", [])) >= 2),
    ],
}


def check_no_circular_deps(workstreams: List[Dict]) -> bool:
    """Check for circular dependencies in workstreams."""
    if not workstreams:
        return True

    # Build dependency graph
    graph = {}
    for ws in workstreams:
        ws_id = ws.get("id", ws.get("name", ""))
        graph[ws_id] = ws.get("dependencies", [])

    # DFS to detect cycles
    visited = set()
    rec_stack = set()

    def has_cycle(node: str) -> bool:
        if node not in graph:
            return False
        visited.add(node)
        rec_stack.add(node)

        for dep in graph.get(node, []):
            if dep not in visited:
                if has_cycle(dep):
                    return True
            elif dep in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    for node in graph:
        if node not in visited:
            if has_cycle(node):
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

        data = parse_markdown_initiative(content)
        return data, "markdown"

    raise ValueError(f"Unsupported file type: {file_path.suffix}")


def parse_markdown_initiative(content: str) -> Dict[str, Any]:
    """Parse markdown initiative into structured data."""
    data = {
        "title": "",
        "summary": "",
        "owner": "",
        "success_metrics": [],
        "workstreams": [],
        "risks": []
    }

    # Extract title
    title_match = re.search(r'^#\s+(?:Initiative:?\s*)?(.+)$', content, re.MULTILINE)
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

        if 'overview' in section_title or 'summary' in section_title:
            data["summary"] = section_content.strip()
        elif 'metric' in section_title or 'success' in section_title:
            metrics = re.findall(r'[-*]\s+(.+)$', section_content, re.MULTILINE)
            data["success_metrics"] = [{"metric": m, "target": m} for m in metrics]
        elif 'workstream' in section_title:
            # Parse workstream subsections
            ws_sections = re.split(r'^###\s+', section_content, flags=re.MULTILINE)
            for ws_section in ws_sections:
                if ws_section.strip():
                    ws_lines = ws_section.strip().split('\n')
                    ws_name = ws_lines[0].strip()
                    ws_content = '\n'.join(ws_lines[1:])
                    agent_match = re.search(r'Agent:\s*(\S+)', ws_content)
                    goal_match = re.search(r'Goal:\s*(.+)', ws_content)
                    data["workstreams"].append({
                        "name": ws_name,
                        "agent": agent_match.group(1) if agent_match else None,
                        "goal": goal_match.group(1) if goal_match else None,
                        "milestones": []
                    })
        elif 'risk' in section_title:
            risks = re.findall(r'[-*]\s+\*\*(.+?)\*\*:?\s*(.*)$', section_content, re.MULTILINE)
            data["risks"] = [{"risk": r[0], "mitigation": r[1]} for r in risks]

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
    parser = argparse.ArgumentParser(description="Validate OrgX orchestration artifacts")
    parser.add_argument("file", type=Path, help="Path to artifact file")
    parser.add_argument("--type", "-t", required=True,
                       choices=["initiative", "delegation", "synthesis"],
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
