---
name: task-protocol
version: "2.2.0"
description: |
  Individual task execution protocol for OrgX. Handles task lifecycle from
  hydration through completion with consistent reporting, evidence attachment,
  and estimate-guarded delegation.
  Use when executing individual tasks within a workstream.
---

# Task Execution Protocol

## Starting a Task

- Read workspace context with `mcp__orgx__orgx_get_workspace_context`; pass `workspace_id` if the target workspace differs from the auto-resolved one. It reads context; it does not select a workspace or create a session.
- Read the task with `mcp__orgx__orgx_inspect type=task hydrate_context=true`.
- If you only have a title or partial reference, find the ID first with `mcp__orgx__orgx_search`.
- Start the task with `mcp__orgx__orgx_start_agent_task task_id=<task_id>`; status follows the dispatched run. There is no v2 call that sets a status directly: `mcp__orgx__orgx_update_work` (it patches content only: title, summary, description, priority, due_date, goal_ids, metadata; it cannot change workflow status).
- Progress is captured by the client's hooks; there is no call to emit activity. Record outcomes with `mcp__orgx__orgx_complete_work_with_proof`.
- Check `metadata.rework_feedback` on the task — if present, this is a rework run: address that feedback first (see the `orgx-quality-bar` skill).
- Verify prerequisites, context attachments, and acceptance criteria before doing work.

## Executing

- Follow the domain-specific workflow from the active skill.
- Use `mcp__orgx__orgx_attach_artifact type=task id=<task_id> name=... location=...` to link docs, URLs, plans, PRs, screenshots, or other proof back to the task. Always set `artifact_type` (see `orgx-quality-bar` for the type-code catalog) so the artifact is judged on the right layer stack.
- If the work starts as planning, run:
  - `mcp__orgx__orgx_start_plan title=...` to open a tracked session
  - `mcp__orgx__orgx_save_plan session_id=... plan_content=... expected_version=...` to save each revision
  - `mcp__orgx__orgx_record_plan_edit session_id=... edit_summary=...` for major revisions
  - `mcp__orgx__orgx_complete_plan session_id=... plan_content=... expected_version=... attach_to=[{ entity_type: "task", entity_id: ... }]`

## Handling Blockers

- Pause with `mcp__orgx__orgx_pause_work level=task id=<task_id>` and state the blocker on the task with `mcp__orgx__orgx_update_work`.
- When the blocker needs an explicit approval, tradeoff, or de-stall decision,
  create it with `mcp__orgx__orgx_capture_decision` (`decision`, `context`) and
  an idempotency key tied to the task/run. Only a person settles
  it: report the task as waiting on them, hand them the decision's `review_url`,
  and never approve or reject it yourself (`mcp__orgx__orgx_open_decision_review`
  only returns where the person decides).
- If a write's outcome is unclear (timeout, dropped connection), retry it with
  the same idempotency key; OrgX replays the stored result instead of
  duplicating it. A 409 means the first attempt is still running.
- Before cross-domain delegation, call `mcp__orgx__orgx_estimate_agent_task` with the `task`; v2 has no separate guard or classify call, so the estimate is the pre-dispatch check.
- Dispatch with `mcp__orgx__orgx_start_agent_task` (an existing `task_id`), or `mcp__orgx__orgx_handoff_task task_id=... agent_type=...` to reassign, only after the estimate is acceptable.
- A started task run is not a finished one. Report it as started, keep the
  returned operation id, and poll `mcp__orgx__orgx_get_operation_status`
  (honor `next_poll_after_ms`, read `waiting_on`) or `mcp__orgx__orgx_get_agent_status`
  before relying on its output. See `orgx-capability-mindset` → Truthful State.

## Completing

- Validate output against acceptance criteria and the domain's layer stack
  (`orgx-quality-bar`): OrgX verifies artifacts four-lens and gates at AQ 0.85.
- Run domain-specific quality gates.
- Attach final proof if anything is still only in the transcript — complete with
  `mcp__orgx__orgx_complete_work_with_proof type=task id=<task_id> artifact=... verification=... quality_score=... note=...`
  so completion and evidence land together.
- Put reusable lessons in the completion `note`; v2 has no separate learning-capture call. For an independent quality judgment, call `mcp__orgx__orgx_request_independent_artifact_review artifact_id=...`.
- When several related mutations change at once, make each typed call with its own `idempotency_key`; there is no batch changeset.

## Task Types

- `research`: gather information, analyze options
- `create`: produce a new artifact
- `review`: evaluate existing work and comment on it
- `implement`: execute technical or operational changes
