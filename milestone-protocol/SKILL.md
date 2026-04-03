---
name: milestone-protocol
description: |
  Milestone tracking and checkpoint management for OrgX initiatives.
  Handles milestone creation, launch, risk flagging, evidence attachment,
  and completion. Use when working with initiative milestones and delivery
  checkpoints.
---

# Milestone Protocol

Milestones are checkpoints with explicit deliverables. Treat them as proof gates, not status labels.

## Core Loop

1. Bootstrap and confirm workspace with `mcp__orgx__orgx_bootstrap` and `mcp__orgx__workspace`.
2. Load the parent initiative or workstream with `mcp__orgx__list_entities`.
3. Create or update the milestone.
4. Attach evidence as deliverables land.
5. Verify readiness before completing.

## Creating Milestones

- Prefer `mcp__orgx__create_milestone` when creating a single checkpoint.
- Use `mcp__orgx__batch_create_entities` when creating multiple milestones with shared refs.
- Always link the milestone to its initiative, and workstream when applicable.
- Include deliverables and `due_date`.

## Tracking Progress

- Start with `mcp__orgx__entity_action type=milestone action=launch`.
- Inspect status with `mcp__orgx__list_entities type=milestone` or the parent initiative pulse.
- Use `mcp__orgx__comment_on_entity` for checkpoint notes that should remain visible to operators.

## Flagging Risk

- Pause with `mcp__orgx__entity_action type=milestone action=pause note="..."`.
- Include the blocker, mitigation path, and owner.
- Escalate cross-domain risks through the parent initiative or orchestrator comments, not only in chat.

## Completing

1. Verify all milestone deliverables are attached or linked.
2. Run `mcp__orgx__verify_entity_completion type=milestone`.
3. Attach proof with `mcp__orgx__entity_action action=attach`.
4. Complete with `mcp__orgx__entity_action type=milestone action=complete`.
