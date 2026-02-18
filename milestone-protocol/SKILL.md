---
name: milestone-protocol
description: |
  Milestone tracking and checkpoint management for OrgX initiatives.
  Handles milestone creation, progress tracking, risk flagging, and completion.
  Use when working with initiative milestones and delivery checkpoints.
---

# Milestone Protocol

## Creating Milestones

- Create: `mcp__orgx__create_entity type=milestone`
- Link to initiative and workstream
- Define deliverables and due_date

## Tracking Progress

- Start: `mcp__orgx__launch_entity type=milestone`
- Check status via `mcp__orgx__list_entities type=milestone`
- Review linked tasks for completion percentage

## Flagging Risk

- If at risk: `mcp__orgx__pause_entity type=milestone`
- Include reason and mitigation plan
- Escalate to orchestrator if cross-domain impact

## Completing

- Verify all deliverables are met
- Verify readiness: `mcp__orgx__verify_entity_completion type=milestone`
- Complete: `mcp__orgx__complete_entity type=milestone`
- Document what was delivered

## Best Practices

- Milestones are checkpoints, not tasks - they mark meaningful progress
- Each milestone should have clear, verifiable deliverables
- Flag risk early rather than missing silently
