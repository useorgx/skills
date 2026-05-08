---
name: task-protocol
version: "2.0.0"
description: |
  Individual task execution protocol for OrgX. Handles task lifecycle from
  hydration through completion with consistent reporting, evidence attachment,
  and spawn-guarded delegation.
  Use when executing individual tasks within a workstream.
---

# Task Execution Protocol

## Starting a Task

- Bootstrap with `mcp__orgx__orgx_bootstrap`.
- Confirm or set workspace through `mcp__orgx__orgx_bootstrap`.
- Read the task with `mcp__orgx__orgx_inspect`.
- If you only have an entity ID, use `mcp__orgx__orgx_search` with `id` and `hydrate_context=true`.
- Start with `mcp__orgx__orgx_act type=task action=launch`.
- Emit kickoff telemetry with `mcp__orgx__orgx_emit_activity phase=intent`.
- Verify prerequisites, context attachments, and acceptance criteria before doing work.

## Executing

- Follow the domain-specific workflow from the active skill.
- Emit progress with `mcp__orgx__orgx_emit_activity` at meaningful milestones.
- Use `mcp__orgx__orgx_act action=attach` to link docs, URLs, plans, PRs, screenshots, or other proof back to the task.
- If the work starts as planning, run:
  - `mcp__orgx__orgx_plan`
  - `mcp__orgx__orgx_plan`
  - `mcp__orgx__orgx_plan` for major revisions
  - `mcp__orgx__orgx_plan attach_to=[{ entity_type: "task", entity_id: ... }]`

## Handling Blockers

- Pause with `mcp__orgx__orgx_act type=task action=pause note="..."`.
- Document the blocker clearly with `mcp__orgx__orgx_act`.
- Emit blocker telemetry with `mcp__orgx__orgx_emit_activity phase=blocked`.
- When the blocker needs an explicit approval, tradeoff, or de-stall decision,
  create it through `mcp__orgx__orgx_write` with a `decision.create`
  operation and an idempotency key tied to the task/run.
- Before cross-domain delegation, call `mcp__orgx__orgx_spawn`.
- Use `mcp__orgx__orgx_spawn` or `mcp__orgx__orgx_spawn` only after the guard passes.

## Completing

- Validate output against acceptance criteria.
- Run domain-specific quality gates.
- Verify readiness with `mcp__orgx__orgx_act type=task`.
- Attach final proof if anything is still only in the transcript.
- Batch any final task, milestone, or decision state updates through
  `mcp__orgx__orgx_write` when more than one state mutation is
  required.
- Emit final telemetry with `mcp__orgx__orgx_emit_activity phase=completed progress_pct=100`.
- Complete with `mcp__orgx__orgx_act type=task action=complete`.

## Task Types

- `research`: gather information, analyze options
- `create`: produce a new artifact
- `review`: evaluate existing work and comment on it
- `implement`: execute technical or operational changes
