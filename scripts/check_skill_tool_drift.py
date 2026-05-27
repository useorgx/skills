#!/usr/bin/env python3
"""Validate OrgX skill docs against the current MCP tool surface."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRS = sorted(
    path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").exists()
)
FILE_NAMES = ("SKILL.md", "instructions.md", "skill.toml")
ORGX_TOOL_RE = re.compile(r"mcp__orgx__([a-zA-Z0-9_]+)")
STRING_RE = re.compile(r'"([^"]+)"')
CAPABILITY_MINDSET_SKILL = "orgx-capability-mindset"
ROLE_AGENT_DIRS = {
    "design-agent",
    "engineering-agent",
    "marketing-agent",
    "operations-agent",
    "orchestrator-agent",
    "product-agent",
    "sales-agent",
}

KNOWN_ORGX_TOOLS = {
    "orgx_act",
    "orgx_attach",
    "orgx_bootstrap",
    "orgx_decide",
    "orgx_emit_activity",
    "orgx_inspect",
    "orgx_plan",
    "orgx_recommend",
    "orgx_search",
    "orgx_spawn",
    "orgx_submit_receipt",
    "orgx_write",
}

DEPRECATED_ORGX_TOOLS = {
    "account_status",
    "account_upgrade",
    "account_usage_report",
    "approve_decision",
    "batch_action",
    "batch_delete_entities",
    "batch_create_entities",
    "classify_task_model",
    "check_spawn_guard",
    "complete_entity",
    "complete_plan",
    "configure_org",
    "create_decision",
    "create_entity",
    "create_milestone",
    "create_task",
    "entity_action",
    "get_active_sessions",
    "get_agent_status",
    "get_decision_history",
    "get_initiative_pulse",
    "get_initiative_stream_state",
    "get_morning_brief",
    "get_my_trust_context",
    "get_org_snapshot",
    "get_outcome_attribution",
    "get_pending_decisions",
    "get_relevant_learnings",
    "get_scoring_signals",
    "get_task_with_context",
    "handoff_task",
    "improve_plan",
    "launch_entity",
    "list_entity_comments",
    "list_entities",
    "pause_entity",
    "pin_workstream",
    "query_org_memory",
    "queue_action",
    "recommend_next_action",
    "record_outcome",
    "record_plan_edit",
    "record_quality_score",
    "reject_decision",
    "resume_plan_session",
    "save_artifact",
    "score_next_up_queue",
    "scoring_config",
    "spawn_agent_task",
    "start_autonomous_session",
    "start_plan_session",
    "stats",
    "submit_learning",
    "sync_client_state",
    "update_entity",
    "update_stream_progress",
    "validate_studio_content",
    "verify_entity_completion",
}

PLAN_TOOLS = {"orgx_plan"}
ARTIFACT_CONTRACT_FIELDS = {
    "metadata.artifact_contract",
    "agent_type",
    "company_stage",
    "business_outcome",
    "owner",
    "review_date",
    "verification",
}
LOOP_VALIDATION_FIELDS = {
    "action=\"estimate\"",
    "loop_validation",
    "validation_rung",
    "verification_status",
    "model_tier",
    "budget_mode",
}
ROLE_AGENT_ARTIFACT_TYPES = {
    "design-agent": {"design.audit", "design.component_spec", "design.token_package"},
    "engineering-agent": {"eng.pull_request", "eng.deploy_proof", "eng.structured_blocker"},
    "marketing-agent": {"marketing.launch_asset", "marketing.channel_hypothesis"},
    "operations-agent": {
        "ops.operator_brief",
        "ops.runbook",
        "ops.budget_envelope",
        "ops.incident_status",
    },
    "orchestrator-agent": {"orchestration.next_initiative"},
    "product-agent": {
        "product.customer_discovery",
        "product.prd",
        "product.pricing_hypothesis",
        "product.decision_record",
    },
    "sales-agent": {"sales.strategy", "sales.icp_offer_sequence", "sales.send_plan"},
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_skill_files(skill_dir: Path) -> list[Path]:
    return [path for name in FILE_NAMES if (path := skill_dir / name).exists()]


def collect_refs(text: str) -> set[str]:
    return set(ORGX_TOOL_RE.findall(text))


def parse_required_tools(skill_toml: Path) -> list[str]:
    text = read_text(skill_toml)
    match = re.search(r"required_tools\s*=\s*\[(.*?)\]", text, re.DOTALL)
    if not match:
        return []
    return STRING_RE.findall(match.group(1))


def main() -> int:
    errors: list[str] = []

    if not (ROOT / CAPABILITY_MINDSET_SKILL / "SKILL.md").exists():
        errors.append(
            f"missing shared `{CAPABILITY_MINDSET_SKILL}` skill required by role agents"
        )

    for skill_dir in SKILL_DIRS:
        combined_refs: set[str] = set()
        combined_text_parts: list[str] = []

        for file_path in iter_skill_files(skill_dir):
            text = read_text(file_path)
            combined_text_parts.append(text)
            refs = collect_refs(text)
            combined_refs |= refs

            for ref in sorted(refs):
                if ref in DEPRECATED_ORGX_TOOLS:
                    errors.append(
                        f"{file_path.relative_to(ROOT)} references deprecated OrgX tool "
                        f"`mcp__orgx__{ref}`"
                    )
                elif ref not in KNOWN_ORGX_TOOLS:
                    errors.append(
                        f"{file_path.relative_to(ROOT)} references unknown OrgX tool "
                        f"`mcp__orgx__{ref}`"
                    )

        combined_text = "\n".join(combined_text_parts)

        if "agentic-capability-protocol" in combined_text:
            errors.append(
                f"{skill_dir.name} references retired `agentic-capability-protocol`; "
                f"use `{CAPABILITY_MINDSET_SKILL}`"
            )

        if skill_dir.name in ROLE_AGENT_DIRS and CAPABILITY_MINDSET_SKILL not in combined_text:
            errors.append(
                f"{skill_dir.name} is missing shared `{CAPABILITY_MINDSET_SKILL}` pointer"
            )

        if skill_dir.name in ROLE_AGENT_DIRS:
            for field in sorted(ARTIFACT_CONTRACT_FIELDS):
                if field not in combined_text:
                    errors.append(
                        f"{skill_dir.name} is missing artifact contract field `{field}`"
                    )

            for artifact_type in sorted(ROLE_AGENT_ARTIFACT_TYPES[skill_dir.name]):
                if artifact_type not in combined_text:
                    errors.append(
                        f"{skill_dir.name} is missing canonical MCP artifact_type "
                        f"`{artifact_type}`"
                    )

        if skill_dir.name == CAPABILITY_MINDSET_SKILL:
            for field in sorted(ARTIFACT_CONTRACT_FIELDS):
                if field not in combined_text:
                    errors.append(
                        f"{CAPABILITY_MINDSET_SKILL} is missing shared artifact "
                        f"contract field `{field}`"
                    )
            for agent_dir, artifact_types in sorted(ROLE_AGENT_ARTIFACT_TYPES.items()):
                for artifact_type in sorted(artifact_types):
                    if artifact_type not in combined_text:
                        errors.append(
                            f"{CAPABILITY_MINDSET_SKILL} is missing canonical "
                            f"artifact_type `{artifact_type}` for {agent_dir}"
                        )
            for field in sorted(LOOP_VALIDATION_FIELDS):
                if field not in combined_text:
                    errors.append(
                        f"{CAPABILITY_MINDSET_SKILL} is missing loop validation "
                        f"receipt field `{field}`"
                    )

        if not combined_refs:
            continue

        missing_baseline = {"orgx_bootstrap"} - combined_refs
        for tool in sorted(missing_baseline):
            errors.append(
                f"{skill_dir.name} is missing baseline OrgX workflow tool "
                f"`mcp__orgx__{tool}` in its skill files"
            )

        skill_toml = skill_dir / "skill.toml"
        if skill_toml.exists():
            required_tools = set(parse_required_tools(skill_toml))
            orgx_required = {
                tool.removeprefix("mcp__orgx__")
                for tool in required_tools
                if tool.startswith("mcp__orgx__")
            }

            for tool in sorted({"orgx_bootstrap"} - orgx_required):
                errors.append(
                    f"{skill_toml.relative_to(ROOT)} is missing required tool "
                    f"`mcp__orgx__{tool}`"
                )

            for tool in sorted(orgx_required):
                if tool in DEPRECATED_ORGX_TOOLS:
                    errors.append(
                        f"{skill_toml.relative_to(ROOT)} declares deprecated OrgX tool "
                        f"`mcp__orgx__{tool}`"
                    )
                elif tool not in KNOWN_ORGX_TOOLS:
                    errors.append(
                        f"{skill_toml.relative_to(ROOT)} declares unknown OrgX tool "
                        f"`mcp__orgx__{tool}`"
                    )

    if errors:
        print("OrgX skill drift check failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"OrgX skill drift check passed for {len(SKILL_DIRS)} skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
