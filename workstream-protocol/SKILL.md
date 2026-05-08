---
name: workstream-protocol
version: "2.0.0"
description: |
  Stream execution lifecycle for OrgX workstreams. Handles initialization,
  progress reporting, blocker management, evidence attachment, and completion
  with DAG-aware sequencing. Use when executing work within an OrgX initiative
  stream.
---

# Workstream Execution Protocol

## When Assigned a Stream

### 1. Initialize

- Bootstrap with `mcp__orgx__orgx_bootstrap`.
- Confirm or set workspace through `mcp__orgx__orgx_bootstrap`.
- Read the stream with `mcp__orgx__orgx_search type=stream`.
- Check upstream and downstream pressure with `mcp__orgx__orgx_inspect`.
- If the stream is ready to start, use `mcp__orgx__orgx_act type=stream action=launch`.
- Report 0% progress via `mcp__orgx__orgx_emit_activity`.

### 2. Execute

- Follow the relevant domain skill workflow.
- Report progress at meaningful milestones.
- Progress and confidence are separate:
  - `progress_pct`: how much work is done
  - `confidence`: how confident you are in the current output
- Attach important outputs to the stream or its tasks with `mcp__orgx__orgx_act action=attach`.

### 3. Handle Blockers

- Pause or block with `mcp__orgx__orgx_act type=stream action=pause note="..."`.
- Use `mcp__orgx__orgx_act` for detailed blocker context.
- Before delegating new work, call `mcp__orgx__orgx_spawn`.
- Use `mcp__orgx__orgx_spawn` or `mcp__orgx__orgx_spawn` only after the guard passes.

### 4. Complete

- Run domain-specific validation.
- Verify readiness with `mcp__orgx__orgx_act type=workstream`.
- Complete with `mcp__orgx__orgx_act type=stream action=complete`.
- Downstream streams should move because the DAG is now unblocked; verify with `mcp__orgx__orgx_inspect`.

### 5. Error Handling

- Recoverable issue: lower confidence, document status, continue.
- Unrecoverable issue: pause the stream and make the blocker explicit on the entity.
