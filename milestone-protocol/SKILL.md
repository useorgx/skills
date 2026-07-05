---
name: milestone-protocol
version: "2.1.0"
description: |
  Milestone tracking and checkpoint management for OrgX initiatives.
  Handles milestone creation, launch, risk flagging, evidence attachment,
  and completion. Use when working with initiative milestones and delivery
  checkpoints.
---

# Milestone Protocol

Milestones are checkpoints with explicit deliverables. Treat them as proof gates, not status labels.

## Core Loop

1. Bootstrap with `mcp__orgx__orgx_bootstrap` (pass `workspace_id` only when overriding the auto-resolved workspace).
2. Load the parent initiative or workstream with `mcp__orgx__orgx_search`.
3. Create or update the milestone.
4. Attach evidence as deliverables land.
5. Verify readiness before completing.

## Creating Milestones

- Prefer `mcp__orgx__orgx_write operation=create type=milestone` when creating a single checkpoint.
- Use `mcp__orgx__orgx_apply_changeset` with `ref` keys when creating multiple milestones with shared dependencies.
- Always link the milestone to its initiative, and workstream when applicable.
- Include deliverables and `due_date`.

## Tracking Progress

- Start with `mcp__orgx__orgx_act type=milestone action=launch`.
- Inspect status with `mcp__orgx__orgx_search type=milestone` or `mcp__orgx__get_initiative_pulse` on the parent.
- Use `mcp__orgx__orgx_act action=update note="..."` for checkpoint notes that should remain visible to operators.

## Flagging Risk

- Flag with `mcp__orgx__orgx_act type=milestone action=flag_risk note="..."`; pause with `action=pause` for intentional holds.
- Include the blocker, mitigation path, and owner.
- Escalate cross-domain risks through the parent initiative or orchestrator comments, not only in chat.

## Completing

1. Verify all milestone deliverables are attached or linked.
2. Run `mcp__orgx__orgx_act type=milestone action=validate dry_run=true`.
3. Attach proof with `mcp__orgx__orgx_attach` (set `artifact_type` — see `orgx-quality-bar`).
4. Complete with `mcp__orgx__orgx_act type=milestone action=complete` (or `action=complete_with_proof` to land evidence in the same call).
