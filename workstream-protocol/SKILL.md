---
name: workstream-protocol
version: "2.1.0"
description: |
  Stream execution lifecycle for OrgX workstreams. Handles initialization,
  progress reporting, blocker management, evidence attachment, and completion
  with DAG-aware sequencing. Use when executing work within an OrgX initiative
  stream.
---

# Workstream Execution Protocol

## When Assigned a Stream

### 1. Initialize

- Bootstrap with `mcp__orgx__orgx_bootstrap` (pass `workspace_id` only when overriding the auto-resolved workspace).
- Read the stream with `mcp__orgx__orgx_search type=stream`.
- Check upstream and downstream pressure with `mcp__orgx__orgx_inspect type=workstream hydrate_context=true`.
- If the stream is ready to start, use `mcp__orgx__orgx_act type=stream action=launch`.
- Report 0% progress via `mcp__orgx__orgx_emit_activity`.

### 2. Execute

- Follow the relevant domain skill workflow.
- Report progress at meaningful milestones.
- Progress and confidence are separate:
  - `progress_pct`: how much work is done
  - `confidence`: how confident you are in the current output
- Attach important outputs to the stream or its tasks with `mcp__orgx__orgx_attach` — always set `artifact_type` so the artifact is judged on the right layer stack (see `orgx-quality-bar`).

### 3. Handle Blockers

- Pause or block with `mcp__orgx__orgx_act type=stream action=pause note="..."` (`action=block` when an explicit dependency blocks it).
- Attach a `*.structured_blocker` artifact for detailed blocker context — repo, branch, command, exact error. Blockers are judged on the ops stack: they must be actionable at 3am.
- Before delegating new work, call `mcp__orgx__orgx_spawn action=guard` (add `action=estimate` when cost matters).
- Dispatch with `mcp__orgx__orgx_spawn action=spawn` (or `action=handoff`) only after the guard passes.

### 4. Complete

- Run domain-specific validation against the domain's layer stack (`orgx-quality-bar`).
- Verify readiness with `mcp__orgx__orgx_act type=stream action=validate dry_run=true`.
- Complete with `mcp__orgx__orgx_act type=stream action=complete`, then submit `mcp__orgx__orgx_submit_receipt receipt_type=proof` with evidence URLs.
- Downstream streams should move because the DAG is now unblocked; verify with `mcp__orgx__orgx_inspect type=initiative`.

### 5. Error Handling

- Recoverable issue: lower confidence, document status, continue.
- Unrecoverable issue: pause the stream and make the blocker explicit on the entity.
