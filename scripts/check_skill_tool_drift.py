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

KNOWN_ORGX_TOOLS = {
    "account_status",
    "account_upgrade",
    "account_usage_report",
    "approve_decision",
    "batch_action",
    "batch_create_entities",
    "batch_delete_entities",
    "check_spawn_guard",
    "classify_task_model",
    "comment_on_entity",
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
    "list_entities",
    "list_entity_comments",
    "orgx_apply_changeset",
    "orgx_bootstrap",
    "orgx_describe_action",
    "orgx_describe_tool",
    "orgx_emit_activity",
    "pin_workstream",
    "query_org_memory",
    "queue_action",
    "recommend_next_action",
    "record_outcome",
    "record_plan_edit",
    "record_quality_score",
    "reject_decision",
    "resume_plan_session",
    "scaffold_initiative",
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
    "workspace",
}

DEPRECATED_ORGX_TOOLS = {
    "complete_entity",
    "get_decision_history",
    "get_pending_decisions",
    "launch_entity",
    "pause_entity",
    "score_next_up_queue",
}

PLAN_TOOLS = {"start_plan_session", "improve_plan", "record_plan_edit"}


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

    for skill_dir in SKILL_DIRS:
        combined_refs: set[str] = set()

        for file_path in iter_skill_files(skill_dir):
            refs = collect_refs(read_text(file_path))
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

        if not combined_refs:
            continue

        missing_baseline = {"orgx_bootstrap", "workspace"} - combined_refs
        for tool in sorted(missing_baseline):
            errors.append(
                f"{skill_dir.name} is missing baseline OrgX workflow tool "
                f"`mcp__orgx__{tool}` in its skill files"
            )

        if "spawn_agent_task" in combined_refs and "check_spawn_guard" not in combined_refs:
            errors.append(
                f"{skill_dir.name} references `mcp__orgx__spawn_agent_task` without "
                f"`mcp__orgx__check_spawn_guard`"
            )

        if combined_refs & PLAN_TOOLS and "complete_plan" not in combined_refs:
            errors.append(
                f"{skill_dir.name} references plan-session tools without "
                f"`mcp__orgx__complete_plan`"
            )

        skill_toml = skill_dir / "skill.toml"
        if skill_toml.exists():
            required_tools = set(parse_required_tools(skill_toml))
            orgx_required = {
                tool.removeprefix("mcp__orgx__")
                for tool in required_tools
                if tool.startswith("mcp__orgx__")
            }

            for tool in sorted({"orgx_bootstrap", "workspace"} - orgx_required):
                errors.append(
                    f"{skill_toml.relative_to(ROOT)} is missing required tool "
                    f"`mcp__orgx__{tool}`"
                )

            if "spawn_agent_task" in orgx_required and "check_spawn_guard" not in orgx_required:
                errors.append(
                    f"{skill_toml.relative_to(ROOT)} declares `mcp__orgx__spawn_agent_task` "
                    f"without `mcp__orgx__check_spawn_guard`"
                )

            if orgx_required & PLAN_TOOLS and "complete_plan" not in orgx_required:
                errors.append(
                    f"{skill_toml.relative_to(ROOT)} declares plan-session tools without "
                    f"`mcp__orgx__complete_plan`"
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
