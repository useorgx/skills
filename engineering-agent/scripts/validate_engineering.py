#!/usr/bin/env python3
"""
Validate OrgX engineering artifacts (RFCs, ADRs, code reviews, post-mortems,
tech debt inventories, capacity plans, runbooks, migration playbooks,
dependency audits, and performance budgets).
Ensures all quality gates pass before artifacts are saved.

Usage:
    python validate_engineering.py <file> --type <type>

Supported types:
    rfc, adr, review, postmortem, tech-debt, capacity, runbook,
    migration, dependency-audit, perf-budget

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


VALID_SEVERITIES = ["critical", "high", "medium", "low"]
VALID_CATEGORIES = ["architecture", "code-quality", "testing", "infrastructure", "documentation", "dependency"]
VALID_INTEREST_RATES = ["accelerating", "linear", "stable", "diminishing"]
VALID_EFFORT_SIZES = ["XS", "S", "M", "L", "XL"]
VALID_PRIORITIES = ["P0", "P1", "P2", "P3"]
VALID_MIGRATION_STRATEGIES = ["strangler-fig", "big-bang", "parallel-run", "blue-green", "canary"]
VALID_DATA_MIGRATION_STRATEGIES = ["online", "offline", "hybrid"]
VALID_MAINTENANCE_STATUSES = ["active", "maintained", "deprecated", "abandoned"]
VALID_LICENSE_RISKS = ["none", "low", "medium", "high"]
VALID_AUDIT_ACTIONS = ["upgrade", "replace", "remove", "monitor"]


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
    "tech-debt": [
        ("has_inventory_date", "Inventory date is required (ISO 8601)",
         lambda d: bool(d.get("inventory_date", "").strip())),
        ("has_scope", "Scope (repository/service/system) is required",
         lambda d: bool(d.get("scope", "").strip())),
        ("has_items", "At least 1 tech debt item is required",
         lambda d: len(d.get("items", [])) >= 1),
        ("items_have_id", "All items must have a unique id",
         lambda d: all(i.get("id") for i in d.get("items", []))),
        ("items_have_title", "All items must have a title",
         lambda d: all(i.get("title") for i in d.get("items", []))),
        ("items_have_description", "All items must have a description (min 50 chars)",
         lambda d: all(len(i.get("description", "")) >= 50 for i in d.get("items", []))),
        ("items_have_valid_category", "All items must have a valid category",
         lambda d: all(i.get("category") in VALID_CATEGORIES for i in d.get("items", []))),
        ("items_have_valid_severity", "All items must have a valid severity",
         lambda d: all(i.get("severity") in VALID_SEVERITIES for i in d.get("items", []))),
        ("items_have_effort_estimate", "All items must have an effort estimate (XS|S|M|L|XL)",
         lambda d: all(i.get("effort_estimate", "").split(" ")[0] in VALID_EFFORT_SIZES
                      for i in d.get("items", []))),
        ("items_have_blast_radius", "All items must describe blast radius",
         lambda d: all(bool(i.get("blast_radius")) for i in d.get("items", []))),
        ("items_have_interest_rate", "All items must have an interest rate",
         lambda d: all(i.get("interest_rate") in VALID_INTEREST_RATES for i in d.get("items", []))),
        ("items_have_evidence", "All items must include evidence",
         lambda d: all(bool(i.get("evidence")) for i in d.get("items", []))),
        ("items_have_proposed_fix", "All items must have a proposed fix",
         lambda d: all(bool(i.get("proposed_fix")) for i in d.get("items", []))),
        ("has_prioritized_backlog", "Prioritized backlog with top 5 items required",
         lambda d: len(d.get("prioritized_backlog", [])) == 5),
        ("has_total_estimated_cost", "Total estimated cost in person-weeks required",
         lambda d: bool(d.get("total_estimated_cost"))),
        ("has_recommended_budget", "Recommended budget percentage required",
         lambda d: bool(d.get("recommended_budget"))),
        ("categories_diverse", "Items should span at least 3 categories",
         lambda d: len(set(i.get("category") for i in d.get("items", []))) >= 3),
    ],
    "capacity": [
        ("has_planning_period", "Planning period is required",
         lambda d: bool(d.get("planning_period", "").strip())),
        ("has_team_size", "Team size with role breakdown is required",
         lambda d: bool(d.get("team_size"))),
        ("has_velocity_trend", "Velocity trend data is required",
         lambda d: bool(d.get("velocity_trend"))),
        ("has_planned_commitments", "Planned commitments are required",
         lambda d: len(d.get("planned_commitments", [])) >= 1),
        ("commitments_have_initiative", "All commitments must name the initiative",
         lambda d: all(c.get("initiative") for c in d.get("planned_commitments", []))),
        ("commitments_have_effort", "All commitments must have effort estimate",
         lambda d: all(c.get("estimated_effort") for c in d.get("planned_commitments", []))),
        ("commitments_have_priority", "All commitments must have priority (P0-P3)",
         lambda d: all(c.get("priority") in VALID_PRIORITIES for c in d.get("planned_commitments", []))),
        ("has_utilization_rate", "Utilization rate is required",
         lambda d: d.get("utilization_rate") is not None),
        ("has_buffer_percentage", "Buffer percentage is required (minimum 20%)",
         lambda d: (d.get("buffer_percentage") or 0) >= 20),
        ("has_risk_areas", "Risk areas where capacity < demand are required",
         lambda d: len(d.get("risk_areas", [])) >= 1),
        ("has_recommendations", "Recommendations are required",
         lambda d: len(d.get("recommendations", [])) >= 1),
        ("has_scenario_analysis", "Scenario analysis with at least 2 scenarios required",
         lambda d: len(d.get("scenario_analysis", [])) >= 2),
    ],
    "runbook": [
        ("has_service", "Service name is required",
         lambda d: bool(d.get("service", "").strip())),
        ("has_owner", "Owner (team or individual) is required",
         lambda d: bool(d.get("owner", "").strip())),
        ("has_last_verified", "Last verified date is required",
         lambda d: bool(d.get("last_verified", "").strip())),
        ("has_alert_triggers", "Alert triggers are required",
         lambda d: len(d.get("alert_triggers", [])) >= 1),
        ("has_procedures", "At least 1 procedure step is required",
         lambda d: len(d.get("procedures", [])) >= 1),
        ("procedures_have_action", "All procedures must have an action",
         lambda d: all(p.get("action") for p in d.get("procedures", []))),
        ("procedures_have_expected_output", "All procedures must have expected output",
         lambda d: all(p.get("expected_output") for p in d.get("procedures", []))),
        ("procedures_have_if_fails", "All procedures must have an if_fails fallback",
         lambda d: all(p.get("if_fails") for p in d.get("procedures", []))),
        ("has_escalation_path", "Escalation path is required",
         lambda d: bool(d.get("escalation_path"))),
        ("has_verification_checklist", "Verification checklist is required",
         lambda d: len(d.get("verification_checklist", [])) >= 1),
    ],
    "migration": [
        ("has_title", "Title is required",
         lambda d: bool(d.get("title", "").strip())),
        ("has_source_system", "Source system description is required",
         lambda d: bool(d.get("source_system", "").strip())),
        ("has_target_system", "Target system description is required",
         lambda d: bool(d.get("target_system", "").strip())),
        ("has_valid_strategy", "Strategy must be valid",
         lambda d: d.get("strategy") in VALID_MIGRATION_STRATEGIES),
        ("has_justification", "Justification is required (min 100 chars with data)",
         lambda d: len(d.get("justification", "")) >= 100 and
                   any(c.isdigit() for c in d.get("justification", ""))),
        ("has_phases", "At least 2 migration phases are required",
         lambda d: len(d.get("phases", [])) >= 2),
        ("phases_have_rollback_trigger", "All phases must have rollback triggers",
         lambda d: all(p.get("rollback_trigger") for p in d.get("phases", []))),
        ("phases_have_rollback_procedure", "All phases must have rollback procedures",
         lambda d: all(p.get("rollback_procedure") for p in d.get("phases", []))),
        ("phases_have_success_criteria", "All phases must have success criteria",
         lambda d: all(p.get("success_criteria") for p in d.get("phases", []))),
        ("has_data_migration_plan", "Data migration plan is required",
         lambda d: bool(d.get("data_migration_plan"))),
        ("data_migration_has_strategy", "Data migration plan must have a strategy",
         lambda d: d.get("data_migration_plan", {}).get("strategy") in VALID_DATA_MIGRATION_STRATEGIES),
        ("data_migration_has_verification", "Data migration must have consistency verification",
         lambda d: bool(d.get("data_migration_plan", {}).get("consistency_verification"))),
        ("has_verification_criteria", "Overall verification criteria are required",
         lambda d: bool(d.get("verification_criteria"))),
        ("has_feature_flags", "Feature flags for controlling migration are required",
         lambda d: bool(d.get("feature_flags"))),
        ("has_risk_matrix", "Risk matrix with at least 3 risks is required",
         lambda d: len(d.get("risk_matrix", [])) >= 3),
        ("risks_have_mitigation", "All risks must have mitigation",
         lambda d: all(r.get("mitigation") for r in d.get("risk_matrix", []))),
    ],
    "dependency-audit": [
        ("has_audit_date", "Audit date is required (ISO 8601)",
         lambda d: bool(d.get("audit_date", "").strip())),
        ("has_scope", "Scope (repository/package) is required",
         lambda d: bool(d.get("scope", "").strip())),
        ("has_dependencies", "At least 1 dependency must be listed",
         lambda d: len(d.get("dependencies", [])) >= 1),
        ("deps_have_name", "All dependencies must have a name",
         lambda d: all(dep.get("name") for dep in d.get("dependencies", []))),
        ("deps_have_current_version", "All dependencies must have current version",
         lambda d: all(dep.get("current_version") for dep in d.get("dependencies", []))),
        ("deps_have_latest_version", "All dependencies must have latest version",
         lambda d: all(dep.get("latest_version") for dep in d.get("dependencies", []))),
        ("deps_have_license", "All dependencies must have license info",
         lambda d: all(dep.get("license") for dep in d.get("dependencies", []))),
        ("deps_have_license_risk", "All dependencies must have license risk assessment",
         lambda d: all(dep.get("license_risk") in VALID_LICENSE_RISKS for dep in d.get("dependencies", []))),
        ("deps_have_maintenance_status", "All dependencies must have maintenance status",
         lambda d: all(dep.get("maintenance_status") in VALID_MAINTENANCE_STATUSES
                      for dep in d.get("dependencies", []))),
        ("deps_have_risk_score", "All dependencies must have a risk score (1-10)",
         lambda d: all(1 <= (dep.get("risk_score") or 0) <= 10 for dep in d.get("dependencies", []))),
        ("has_summary_statistics", "Summary statistics are required",
         lambda d: bool(d.get("summary_statistics"))),
        ("has_recommendations", "Recommendations are required",
         lambda d: len(d.get("recommendations", [])) >= 1),
        ("recommendations_have_action", "All recommendations must have a valid action",
         lambda d: all(r.get("action") in VALID_AUDIT_ACTIONS for r in d.get("recommendations", []))),
    ],
    "perf-budget": [
        ("has_application", "Application name or URL is required",
         lambda d: bool(d.get("application", "").strip())),
        ("has_budget_date", "Budget date is required (ISO 8601)",
         lambda d: bool(d.get("budget_date", "").strip())),
        ("has_targets", "Performance targets are required",
         lambda d: bool(d.get("targets"))),
        ("targets_have_lcp", "LCP target is required",
         lambda d: d.get("targets", {}).get("lcp_ms") is not None),
        ("targets_have_fid", "FID target is required",
         lambda d: d.get("targets", {}).get("fid_ms") is not None),
        ("targets_have_cls", "CLS target is required",
         lambda d: d.get("targets", {}).get("cls") is not None),
        ("targets_have_ttfb", "TTFB target is required",
         lambda d: d.get("targets", {}).get("ttfb_ms") is not None),
        ("targets_have_bundle_size", "Bundle size target is required",
         lambda d: d.get("targets", {}).get("bundle_size_kb") is not None),
        ("has_current_measurements", "Current measurements are required",
         lambda d: bool(d.get("current_measurements"))),
        ("has_device_profile", "Device profile for testing is required",
         lambda d: bool(d.get("device_profile", "").strip())),
        ("has_monitoring_setup", "Monitoring setup is required",
         lambda d: bool(d.get("monitoring_setup"))),
        ("monitoring_has_tool", "Monitoring must specify the tool",
         lambda d: bool(d.get("monitoring_setup", {}).get("tool"))),
        ("monitoring_has_frequency", "Monitoring must specify measurement frequency",
         lambda d: bool(d.get("monitoring_setup", {}).get("frequency"))),
        ("monitoring_has_ci_gate", "Monitoring must specify if CI gate is enforced",
         lambda d: d.get("monitoring_setup", {}).get("ci_gate") is not None),
    ],
}


ALL_TYPES = list(QUALITY_GATES.keys())


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
                       choices=ALL_TYPES,
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
