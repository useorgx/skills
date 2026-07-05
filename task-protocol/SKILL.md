---
name: task-protocol
version: "2.1.0"
description: |
  Individual task execution protocol for OrgX. Handles task lifecycle from
  hydration through completion with consistent reporting, evidence attachment,
  and spawn-guarded delegation.
  Use when executing individual tasks within a workstream.
---

# Task Execution Protocol

## Starting a Task

- Bootstrap with `mcp__orgx__orgx_bootstrap`; pass `workspace_id` if the target workspace differs from the auto-resolved one.
- Read the task with `mcp__orgx__orgx_inspect type=task hydrate_context=true`.
- If you only have a title or partial reference, find the ID first with `mcp__orgx__orgx_search`.
- Start with `mcp__orgx__orgx_act type=task action=launch`.
- Emit kickoff telemetry with `mcp__orgx__orgx_emit_activity phase=intent`.
- Check `metadata.rework_feedback` on the task — if present, this is a rework run: address that feedback first (see the `orgx-quality-bar` skill).
- Verify prerequisites, context attachments, and acceptance criteria before doing work.

## Executing

- Follow the domain-specific workflow from the active skill.
- Emit progress with `mcp__orgx__orgx_emit_activity` at meaningful milestones.
- Use `mcp__orgx__orgx_attach` to link docs, URLs, plans, PRs, screenshots, or other proof back to the task. Always set `artifact_type` (see `orgx-quality-bar` for the type-code catalog) so the artifact is judged on the right layer stack.
- If the work starts as planning, run:
  - `mcp__orgx__orgx_plan action=start` to open a tracked session
  - `mcp__orgx__orgx_plan action=improve` for critique on the draft
  - `mcp__orgx__orgx_plan action=record_edit` for major revisions
  - `mcp__orgx__orgx_plan action=complete attach_to=[{ entity_type: "task", entity_id: ... }]`

## Handling Blockers

- Pause with `mcp__orgx__orgx_act type=task action=pause note="..."`.
- Document the blocker clearly with `mcp__orgx__orgx_act`.
- Emit blocker telemetry with `mcp__orgx__orgx_emit_activity phase=blocked`.
- When the blocker needs an explicit approval, tradeoff, or de-stall decision,
  create it through `mcp__orgx__orgx_write` with a `decision.create`
  operation and an idempotency key tied to the task/run.
- Before cross-domain delegation, call `mcp__orgx__orgx_spawn action=guard` (add `action=estimate` when cost matters).
- Dispatch with `mcp__orgx__orgx_spawn action=spawn` (or `action=handoff` to reassign) only after the guard passes.

## Completing

- Validate output against acceptance criteria and the domain's layer stack
  (`orgx-quality-bar`): OrgX verifies artifacts four-lens and gates at AQ 0.85.
- Run domain-specific quality gates.
- Verify readiness with `mcp__orgx__orgx_act type=task action=validate dry_run=true`.
- Attach final proof if anything is still only in the transcript — prefer
  `mcp__orgx__orgx_act action=complete_with_proof` so completion and evidence land together.
- Batch several related state mutations through `mcp__orgx__orgx_apply_changeset`
  with an `idempotency_key` when more than one task/milestone/decision changes at once.
- Close the loop with `mcp__orgx__orgx_submit_receipt receipt_type=proof` (evidence URLs required) and `receipt_type=learning` for reusable lessons.
- Emit final telemetry with `mcp__orgx__orgx_emit_activity phase=completed progress_pct=100`.
- Complete with `mcp__orgx__orgx_act type=task action=complete`.

## Task Types

- `research`: gather information, analyze options
- `create`: produce a new artifact
- `review`: evaluate existing work and comment on it
- `implement`: execute technical or operational changes
