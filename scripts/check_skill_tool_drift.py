#!/usr/bin/env python3
"""Validate OrgX skill docs against the current MCP tool surface."""

from __future__ import annotations

import json
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

# The hosted server's default v2 catalog is the source of truth. A hand-kept
# list once let ~600 references to retired tools pass this check while every
# one of them returned "Tool not found" on v2.
CATALOG = json.loads((ROOT / "scripts" / "orgx-v2-catalog.json").read_text(encoding="utf-8"))
KNOWN_ORGX_TOOLS = {tool["name"] for tool in CATALOG["tools"]}
RETIRED_ORGX_TOOLS: dict[str, str] = CATALOG["retired"]
TOOL_PROPERTIES: dict[str, set[str]] = {
    tool["name"]: set(tool["properties"]) for tool in CATALOG["tools"]
}
BASELINE_ORGX_TOOL = "orgx_get_workspace_context"

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
    "get_decision_history",
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

# Tools only a host widget may call. A model never holds the single-use token
# they need, so a skill that tells an agent to call one teaches a dead end.
WIDGET_ONLY_ORGX_TOOLS = set(CATALOG["widget_only"])

# Writes the server rejects with 400 `idempotency_key_required` when the key is
# missing (useorgx/orgx-mcp#527). Every example call a skill shows for one of
# these must pass `idempotency_key`, or the skill teaches a call that fails.
IDEMPOTENCY_KEY = "idempotency_key"
WRITE_ORGX_TOOLS = set(CATALOG["write_tools"])
# Files scanned for example calls: every Markdown/JSON doc an agent may read.
EXAMPLE_FILE_SUFFIXES = {".md", ".json"}
WRITE_TOOL_RE = re.compile(
    r"\b(?:mcp__orgx__)?("
    + "|".join(sorted(map(re.escape, WRITE_ORGX_TOOLS), key=len, reverse=True))
    + r")\b"
)
FENCE_RE = re.compile(r"^[ \t]*(```|~~~)", re.MULTILINE)
BRACKETS = {"(": ")", "{": "}", "[": "]"}

# The truthful-state contract every agent inherits from the capability mindset:
# a model never settles a decision, a started run is not a finished one, and a
# retried write reuses its idempotency key.
TRUTHFUL_STATE_PHRASES = {
    "## Truthful State",
    "review_url",
    "orgx_get_operation_status",
    "next_poll_after_ms",
    "waiting_on",
    "idempotency_key",
}

# The idempotent-write contract (orgx-mcp#527) every agent inherits: one key
# per intended change, and the typed error codes agents must act on.
IDEMPOTENCY_CONTRACT_PHRASES = {
    "## Idempotent Writes",
    "idempotency_key_required",
    "idempotency_key_conflict",
    "approval_required",
    "stale_version",
    "stale_lease",
    "budget_exhausted",
    "rate_limited",
    "outcome_unknown",
    "forbidden",
}

ARTIFACT_CONTRACT_FIELDS = {
    "artifact_type",
    "agent_type",
    "company_stage",
    "business_outcome",
    "owner",
    "review_date",
    "verification",
}
LOOP_VALIDATION_FIELDS = {
    "orgx_estimate_agent_task",
    "loop_validation",
    "validation_rung",
    "verification_status",
    "model_tier",
    "budget_mode",
}
ROLE_AGENT_ARTIFACT_TYPES = {
    "design-agent": {"design.audit", "design.component_spec", "design.token_package"},
    "engineering-agent": {"eng.pull_request", "eng.deploy_proof", "eng.structured_blocker"},
    "marketing-agent": {
        "marketing.launch_asset",
        "marketing.channel_hypothesis",
        "marketing.offer_package",
    },
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
    "sales-agent": {
        "sales.strategy",
        "sales.icp_offer_sequence",
        "sales.follow_up_sequence",
        "sales.send_plan",
    },
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


def fenced_spans(text: str) -> list[tuple[int, int]]:
    """Return (start, end) offsets of fenced code blocks."""
    spans: list[tuple[int, int]] = []
    opened: tuple[int, str] | None = None
    for match in FENCE_RE.finditer(text):
        if opened is None:
            opened = (match.start(), match.group(1))
        elif match.group(1) == opened[1]:
            spans.append((opened[0], match.end()))
            opened = None
    if opened is not None:
        spans.append((opened[0], len(text)))
    return spans


def balanced_span(text: str, start: int) -> str | None:
    """Return text[start:close] for the bracket opened at `start`."""
    stack = [BRACKETS[text[start]]]
    index = start + 1
    while index < len(text) and stack:
        char = text[index]
        if char in BRACKETS:
            stack.append(BRACKETS[char])
        elif char == stack[-1]:
            stack.pop()
        index += 1
    return text[start:index] if not stack else None


def enclosing_object(text: str, position: int) -> str | None:
    """Return the innermost `{...}` that contains `position`, if any."""
    depth = 0
    index = position
    while index > 0:
        index -= 1
        char = text[index]
        if char == "}":
            depth += 1
        elif char == "{":
            if depth == 0:
                return balanced_span(text, index)
            depth -= 1
    return None


def names_tool_argument(payload: str, tool: str) -> bool:
    """True when the payload passes at least one of the tool's schema properties.

    Arguments count only in call-shaped spelling (`prop`, prop=, prop:, "prop")
    so ordinary prose words such as "type" or "note" never make a call.
    """
    for prop in TOOL_PROPERTIES.get(tool, set()):
        name = re.escape(prop)
        if re.search(
            rf"`{name}`|`{name}\s*[=:]|\b{name}\s*=|[\"']{name}[\"']\s*:|(?<![\w.]){name}\s*:",
            payload,
        ):
            return True
    return False


def write_call_payloads(text: str) -> list[tuple[int, str, str]]:
    """Find example calls to write tools as (offset, tool, argument payload).

    A call is a write-tool reference followed by a bracketed argument list
    (`tool(...)`, `tool {...}`, or prose `tool` (`arg`, ...)), a `with` clause
    naming arguments, an inline code call (`tool arg=... arg=...`), a tool
    reference list entry (`tool` — takes `arg`, ...), or a JSON object whose
    "tool"/"name" value is the tool.
    It counts only when it names at least one schema property of that tool, so
    a bare prose mention of a tool name is never a call.
    """
    fences = fenced_spans(text)
    found: list[tuple[int, str, str]] = []
    for match in WRITE_TOOL_RE.finditer(text):
        tool = match.group(1)
        in_fence = any(start <= match.start() < end for start, end in fences)
        rest = text[match.end():]
        lead = re.match(r"[`\"']?\s*(?:\*\*)?\s*" if in_fence else r"`?[ \t]*", rest)
        cursor = match.end() + (lead.end() if lead else 0)
        payload: str | None = None
        if cursor < len(text) and text[cursor] in "({":
            payload = balanced_span(text, cursor)
        elif not in_fence:
            clause = re.match(r"with\b[^.;\n]*", text[cursor:])
            if clause:
                payload = clause.group(0)
        if payload is None and not in_fence:
            # Inline code call: `mcp__orgx__orgx_pause_work level=task id=...`
            span_start = text.rfind("`", 0, match.start())
            line_start = text.rfind("\n", 0, match.start()) + 1
            if span_start >= line_start and text[span_start + 1:match.start()] in ("", "mcp__orgx__"):
                span_end = text.find("`", match.end())
                line_end = text.find("\n", match.end())
                if span_end != -1 and (line_end == -1 or span_end < line_end):
                    if re.match(r"\s+\S", text[match.end():span_end]):
                        payload = text[match.end():span_end]
        if payload is None and not in_fence:
            # Tool reference list: - `tool` — takes `arg`, `arg` (rest of the line).
            dash = re.match(r"(?:\s*,\s*`[^`\n]+`)*\s*(?:—|--|–)\s+[^\n]*", text[cursor:])
            if dash:
                payload = dash.group(0)
        if payload is None:
            before = text[max(0, match.start() - 40):match.start()]
            if re.search(r"[\"'](?:tool|name|tool_name)[\"']\s*:\s*[\"']$", before):
                payload = enclosing_object(text, match.start())
        if payload and names_tool_argument(payload, tool):
            found.append((match.start(), tool, payload))
    return found


def iter_example_files() -> list[Path]:
    files = [ROOT / "README.md"]
    for skill_dir in SKILL_DIRS:
        files.extend(
            path
            for path in sorted(skill_dir.rglob("*"))
            if path.is_file() and path.suffix in EXAMPLE_FILE_SUFFIXES
        )
    return [path for path in files if path.exists()]


def check_write_idempotency(errors: list[str]) -> None:
    for file_path in iter_example_files():
        text = read_text(file_path)
        for offset, tool, payload in write_call_payloads(text):
            if IDEMPOTENCY_KEY in payload:
                continue
            line = text.count("\n", 0, offset) + 1
            errors.append(
                f"{file_path.relative_to(ROOT)}:{line} shows a call to write tool "
                f"`{tool}` without `{IDEMPOTENCY_KEY}`; the server rejects it with "
                f"400 idempotency_key_required"
            )


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
                if ref in WIDGET_ONLY_ORGX_TOOLS:
                    errors.append(
                        f"{file_path.relative_to(ROOT)} references widget-only OrgX tool "
                        f"`mcp__orgx__{ref}`; agents must never call it"
                    )
                elif ref in RETIRED_ORGX_TOOLS:
                    errors.append(
                        f"{file_path.relative_to(ROOT)} references `mcp__orgx__{ref}`, "
                        f"which the v2 catalog does not register; use {RETIRED_ORGX_TOOLS[ref]}"
                    )
                elif ref in DEPRECATED_ORGX_TOOLS:
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
            for phrase in sorted(TRUTHFUL_STATE_PHRASES):
                if phrase not in combined_text:
                    errors.append(
                        f"{CAPABILITY_MINDSET_SKILL} is missing truthful-state "
                        f"contract text `{phrase}`"
                    )
            for phrase in sorted(IDEMPOTENCY_CONTRACT_PHRASES):
                if phrase not in combined_text:
                    errors.append(
                        f"{CAPABILITY_MINDSET_SKILL} is missing idempotent-write "
                        f"contract text `{phrase}`"
                    )
            for tool in sorted(WRITE_ORGX_TOOLS):
                if f"`{tool}`" not in combined_text:
                    errors.append(
                        f"{CAPABILITY_MINDSET_SKILL} Idempotent Writes does not list "
                        f"write tool `{tool}`"
                    )
            for field in sorted(LOOP_VALIDATION_FIELDS):
                if field not in combined_text:
                    errors.append(
                        f"{CAPABILITY_MINDSET_SKILL} is missing loop validation "
                        f"receipt field `{field}`"
                    )

        if not combined_refs:
            continue

        missing_baseline = {BASELINE_ORGX_TOOL} - combined_refs
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

            for tool in sorted({BASELINE_ORGX_TOOL} - orgx_required):
                errors.append(
                    f"{skill_toml.relative_to(ROOT)} is missing required tool "
                    f"`mcp__orgx__{tool}`"
                )

            for tool in sorted(orgx_required):
                if tool in RETIRED_ORGX_TOOLS:
                    errors.append(
                        f"{skill_toml.relative_to(ROOT)} declares `mcp__orgx__{tool}`, "
                        f"which the v2 catalog does not register; use {RETIRED_ORGX_TOOLS[tool]}"
                    )
                elif tool in DEPRECATED_ORGX_TOOLS:
                    errors.append(
                        f"{skill_toml.relative_to(ROOT)} declares deprecated OrgX tool "
                        f"`mcp__orgx__{tool}`"
                    )
                elif tool not in KNOWN_ORGX_TOOLS:
                    errors.append(
                        f"{skill_toml.relative_to(ROOT)} declares unknown OrgX tool "
                        f"`mcp__orgx__{tool}`"
                    )

    for tool in sorted(WRITE_ORGX_TOOLS):
        if tool not in KNOWN_ORGX_TOOLS:
            errors.append(f"catalog write_tools lists unknown OrgX tool `{tool}`")
        elif IDEMPOTENCY_KEY not in TOOL_PROPERTIES[tool]:
            errors.append(f"catalog write tool `{tool}` does not declare `{IDEMPOTENCY_KEY}`")

    check_write_idempotency(errors)

    if errors:
        print("OrgX skill drift check failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"OrgX skill drift check passed for {len(SKILL_DIRS)} skills against the v2 catalog "
        f"({CATALOG['source']['repo']}@{CATALOG['source']['commit']})."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
