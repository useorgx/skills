---
name: task-protocol
description: |
  Individual task execution protocol for OrgX. Handles task lifecycle from
  start through completion with consistent status reporting.
  Use when executing individual tasks within a workstream.
---

# Task Execution Protocol

## Starting a Task

- Read task details: `mcp__orgx__list_entities type=task`
- Start: `mcp__orgx__launch_entity type=task`
- Emit kickoff telemetry: `mcp__orgx__orgx_emit_activity` (`phase=intent`)
- Verify prerequisites are met

## Executing

- Follow domain-specific workflows from your skill
- For each meaningful step, emit telemetry: `mcp__orgx__orgx_emit_activity` (`phase=execution`)
- Create artifacts as needed: `mcp__orgx__create_entity type=artifact`
- Batch state mutations through `mcp__orgx__orgx_apply_changeset` (do not do per-entity reporting writes)

## Handling Blockers

- Block: `mcp__orgx__pause_entity type=task`
- Document the blocker clearly
- Emit blocker telemetry: `mcp__orgx__orgx_emit_activity` (`phase=blocked`)
- Escalate if cross-domain: `mcp__orgx__spawn_agent_task` to relevant agent

## Completing

- Validate output against acceptance criteria
- Run domain-specific quality gates
- Verify readiness: `mcp__orgx__verify_entity_completion type=task`
- Complete via changeset when possible: `mcp__orgx__orgx_apply_changeset` (`task.update`, `milestone.update`, `decision.create` as needed)
- Emit final telemetry: `mcp__orgx__orgx_emit_activity` (`phase=completed`, `progress_pct=100`)
- Complete: `mcp__orgx__complete_entity type=task`
- Link artifacts to task for traceability

## Task Types

- `research`: Gather information, analyze options
- `create`: Produce new artifact (RFC, PRD, campaign, etc.)
- `review`: Evaluate existing work, provide feedback
- `implement`: Execute technical changes
