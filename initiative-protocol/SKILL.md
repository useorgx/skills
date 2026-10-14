---
name: initiative-protocol
version: "2.2.0"
description: |
  Initiative lifecycle management for OrgX. Handles workspace context,
  hierarchy scaffolding, launch, monitoring, evidence attachment, and completion.
  Use when planning or managing an OrgX initiative.
---

# Initiative Protocol

Use this protocol whenever the user is creating, updating, launching, pausing, or closing an initiative.

## Core Loop

1. Read context with `mcp__orgx__orgx_get_workspace_context` (pass `workspace_id` only when overriding the auto-resolved workspace). It reads; it does not select a workspace or create a session.
2. Load the target initiative with `mcp__orgx__orgx_search type=initiative`, then hydrate it with `mcp__orgx__orgx_inspect type=initiative id=...`.
3. Create or update the hierarchy using the highest-level call available (`mcp__orgx__orgx_validate_initiative_plan` then `mcp__orgx__orgx_create_initiative_hierarchy` for a full hierarchy; the typed create calls and `mcp__orgx__orgx_update_work` for single entities).
4. Attach evidence, plans, and notes back to the initiative before marking it complete.

## Creating an Initiative

1. Check for related work:
   - `mcp__orgx__orgx_search` for prior initiatives or decisions
   - `mcp__orgx__orgx_search type=initiative` for active duplicates
2. Prefer `mcp__orgx__orgx_validate_initiative_plan` followed by `mcp__orgx__orgx_create_initiative_hierarchy` (`plan`, `idempotency_key`) when the request includes milestones, workstreams, or starter tasks — validate first, then one call creates the whole hierarchy (include explicit workstreams in the `plan` to preserve the user's structure). Retry a failed create with the same `idempotency_key`.
3. Use `mcp__orgx__orgx_create_initiative` only for a single initiative shell with no nested hierarchy yet.
4. For follow-on edits, prefer:
   - `mcp__orgx__orgx_update_work type=... id=... fields={...} idempotency_key=<key>` for single-entity field changes
   - `mcp__orgx__orgx_create_workstream` (needs `initiative_id`, `idempotency_key`), `mcp__orgx__orgx_create_milestone` (needs `workstream_id`, `idempotency_key`), or `mcp__orgx__orgx_create_task` (needs `workstream_id`, `idempotency_key`; `milestone_id` optional) for one new child at a time, each with its own `idempotency_key`
5. Launch or pause:
   - launch: `mcp__orgx__orgx_launch_initiative initiative_id=... idempotency_key=<key>`
   - pause: `mcp__orgx__orgx_pause_work level=initiative id=... idempotency_key=<key>`

## Monitoring

- `mcp__orgx__orgx_get_initiative_progress initiative_id=...` for health, blockers, milestones, and AQ-scored deliverables (scored artifacts rank first)
- `mcp__orgx__orgx_inspect type=initiative hydrate_context=true` for stream progress and bottlenecks
- `mcp__orgx__orgx_get_next_actions entity_type=initiative` when the user asks what to do next
- `mcp__orgx__orgx_update_work type=initiative id=... fields={...} idempotency_key=<key>` for notes (summary, description, metadata) that should live on the initiative itself; it cannot change status

## Completion

1. Confirm all dependent work is done or intentionally deferred.
2. Run `mcp__orgx__orgx_get_initiative_progress` to surface anything unfinished.
3. Attach proof with `mcp__orgx__orgx_attach_artifact` (always set `artifact_type` and a fresh `idempotency_key` — see the `orgx-quality-bar` skill) for plans, docs, URLs, or deliverable artifacts.
4. If planning happened in OrgX, finish the plan loop with `mcp__orgx__orgx_complete_plan attach_to=[...] idempotency_key=<key>` so the rationale is attached to the initiative context.
5. Mark complete with `mcp__orgx__orgx_complete_work_with_proof type=initiative id=... idempotency_key=<key>` so evidence lands in the same call.

## Risk Handling

- Use `mcp__orgx__orgx_pause_work level=initiative id=... idempotency_key=<key>` for blockers or intentional holds.
- When the priority problem is risk or sequencing, not state, say so on the entity with `mcp__orgx__orgx_update_work` or record it with `mcp__orgx__orgx_capture_decision`, whichever states the risk honestly.
- Record durable exceptions on the entity (`mcp__orgx__orgx_update_work`) or as a decision via `mcp__orgx__orgx_capture_decision` instead of burying them in the chat transcript. Only a person settles a decision: hand them its `review_url`.
- A launched initiative is started, not done: poll `mcp__orgx__orgx_get_operation_status` (honor `next_poll_after_ms`, read `waiting_on`) before reporting progress.
