---
name: workstream-protocol
description: |
  Stream execution lifecycle for OrgX workstreams. Handles initialization,
  progress reporting, blocker management, and completion with DAG resolution.
  Use when executing work within an OrgX initiative stream.
---

# Workstream Execution Protocol

## When Assigned a Stream

### 1. Initialize

- Read stream: `mcp__orgx__list_entities type=stream`
- Check deps: `mcp__orgx__get_initiative_stream_state`
- Verify status is 'ready' or 'active' before proceeding
- Report 0% progress: `mcp__orgx__update_stream_progress`

### 2. Execute

- Follow your domain skill workflows
- Report progress at meaningful milestones (25%, 50%, 75%)
- Progress and confidence are SEPARATE:
  - `progress_pct` (0-100): How much work is done
  - `confidence` (0-1): How confident you are in the output quality
- Include `status_note` for human visibility
- Use `expected_version` for optimistic locking

### 3. Handle Blockers

- If blocked: `mcp__orgx__entity_action type=stream action=block`
- Always include `blocked_reason`
- Spawn tasks for unresolved deps: `mcp__orgx__spawn_agent_task`

### 4. Complete

- Run domain-specific validation (quality gates)
- Verify readiness: `mcp__orgx__verify_entity_completion type=workstream`
- Complete: `mcp__orgx__complete_entity type=stream`
- This triggers DAG resolution: downstream streams become 'ready'

### 5. Error Handling

- Recoverable: set confidence to 0.5, add status_note, continue
- Unrecoverable: block stream with reason, never silently fail
