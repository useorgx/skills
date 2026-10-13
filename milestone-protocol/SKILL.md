---
name: milestone-protocol
version: "2.2.0"
description: |
  Milestone tracking and checkpoint management for OrgX initiatives.
  Handles milestone creation, launch, risk flagging, evidence attachment,
  and completion. Use when working with initiative milestones and delivery
  checkpoints.
---

# Milestone Protocol

Milestones are checkpoints with explicit deliverables. Treat them as proof gates, not status labels.

## Core Loop

1. Read context with `mcp__orgx__orgx_get_workspace_context` (pass `workspace_id` only when overriding the auto-resolved workspace).
2. Load the parent initiative or workstream with `mcp__orgx__orgx_search`.
3. Create or update the milestone.
4. Attach evidence as deliverables land.
5. Verify readiness before completing.

## Creating Milestones

- Use `mcp__orgx__orgx_create_milestone` (needs `workstream_id`; pass `initiative_id` too) for each checkpoint, with its own `idempotency_key`. There is no batch changeset; create several milestones with one call each, or use `mcp__orgx__orgx_create_initiative_hierarchy` when creating a whole plan.
- Always link the milestone to its initiative and workstream.
- Include deliverables and `due_date`.

## Tracking Progress

- Start the milestone by dispatching its ready tasks with `mcp__orgx__orgx_start_agent_task`; milestone status follows its tasks. `mcp__orgx__orgx_update_work` (it patches content only: title, summary, description, priority, due_date, goal_ids, metadata; it cannot change workflow status).
- Inspect status with `mcp__orgx__orgx_search type=milestone` or `mcp__orgx__orgx_get_initiative_progress` on the parent.
- Use `mcp__orgx__orgx_update_work type=milestone id=... fields={...}` for checkpoint notes that should remain visible to operators.

## Flagging Risk

- State the risk on the milestone with `mcp__orgx__orgx_update_work`, or record it with `mcp__orgx__orgx_capture_decision` when someone must choose; pause with `mcp__orgx__orgx_pause_work level=milestone id=...` for intentional holds.
- Include the blocker, mitigation path, and owner.
- Escalate cross-domain risks through the parent initiative or orchestrator comments, not only in chat. Only a person settles a decision: hand them its `review_url`.

## Completing

1. Verify all milestone deliverables are attached or linked.
2. Check the parent with `mcp__orgx__orgx_get_initiative_progress` for anything unfinished.
3. Attach proof with `mcp__orgx__orgx_attach_artifact` (set `artifact_type` — see `orgx-quality-bar`).
4. Complete with `mcp__orgx__orgx_complete_work_with_proof type=milestone id=...` so evidence lands in the same call.
