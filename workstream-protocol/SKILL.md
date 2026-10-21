---
name: workstream-protocol
version: "2.2.0"
description: |
  Stream execution lifecycle for OrgX workstreams. Handles initialization,
  progress reporting, blocker management, evidence attachment, and completion
  with DAG-aware sequencing. Use when executing work within an OrgX initiative
  stream.
---

# Workstream Execution Protocol

## When Assigned a Stream

### 1. Initialize

- Read context with `mcp__orgx__orgx_get_workspace_context` (pass `workspace_id` only when overriding the auto-resolved workspace).
- Read the stream with `mcp__orgx__orgx_search type=workstream`.
- Check upstream and downstream pressure with `mcp__orgx__orgx_inspect type=workstream hydrate_context=true`.
- If the stream is ready to start, start its work with `mcp__orgx__orgx_start_agent_task task_id=<task_id> idempotency_key=<key>` for each ready task; status follows the dispatched work. `mcp__orgx__orgx_update_work` (it patches content only: title, summary, description, priority, due_date, goal_ids, metadata; it cannot change workflow status).
- Progress is captured by the client's hooks; there is no call to emit activity.

### 2. Execute

- Follow the relevant domain skill workflow.
- Report progress at meaningful milestones.
- Progress and confidence are separate:
  - `progress_pct`: how much work is done
  - `confidence`: how confident you are in the current output
- Attach important outputs to the stream or its tasks with `mcp__orgx__orgx_attach_artifact` — always set `artifact_type` (so the artifact is judged on the right layer stack; see `orgx-quality-bar`) and a fresh `idempotency_key`.

### 3. Handle Blockers

- Pause only the affected work when no independent work can proceed, using `mcp__orgx__orgx_pause_work level=workstream id=<stream_id> idempotency_key=<key>`, and state the blocking dependency on the stream with `mcp__orgx__orgx_update_work`.
- Attach a `*.structured_blocker` artifact for detailed blocker context — repo, branch, command, exact error. Blockers are judged on the ops stack: they must be actionable at 3am.
- Before delegating new work, call `mcp__orgx__orgx_estimate_agent_task` (v2 has no separate guard call; the estimate is the pre-dispatch check).
- Dispatch with `mcp__orgx__orgx_start_agent_task` (an existing `task_id`, `idempotency_key`) or `mcp__orgx__orgx_handoff_task` (`task_id`, `agent_type`, `idempotency_key`) only after the estimate is acceptable.
- A dispatched run is started, not done: report it as started and poll `mcp__orgx__orgx_get_operation_status` (honor `next_poll_after_ms`, read `waiting_on`) or `mcp__orgx__orgx_get_agent_status` before treating its output as landed.
- A blocker that needs a decision is filed with `mcp__orgx__orgx_capture_decision` (reuse its `idempotency_key` on retry) and waits on a person: give them the decision's `review_url` and hold only the work that depends on it until OrgX shows the decision settled. Continue independent work; routine choices within existing authorization do not need a decision. Never approve or reject it yourself.

### 4. Complete

- Run domain-specific validation against the domain's layer stack (`orgx-quality-bar`).
- Complete with `mcp__orgx__orgx_complete_work_with_proof type=workstream id=<stream_id> artifact=... verification=... quality_score=... note=... idempotency_key=<key>`, with evidence URLs in the artifact and lessons in the note. v2 has no separate receipt or learning-capture call.
- Downstream streams should move because the DAG is now unblocked; verify with `mcp__orgx__orgx_inspect type=initiative`.

### 5. Error Handling

- Recoverable issue: lower confidence, document status, continue.
- Unrecoverable issue: pause the stream and make the blocker explicit on the entity.
