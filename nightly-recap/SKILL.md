---
name: nightly-recap
version: "1.0.0"
description: |
  Draft nightly recaps summarizing OrgX workspace activity including completed
  work, pending decisions, active agents, and notable risks still open at the
  end of the day.
---

# Nightly Recap

Generate an end-of-day OrgX summary for the active workspace.

## Required Sequence

1. Call `mcp__orgx__orgx_bootstrap`.
2. Resolve the workspace with `mcp__orgx__workspace`.
3. Gather:
   - `mcp__orgx__get_org_snapshot`
   - `mcp__orgx__list_entities type=task status=done`
   - `mcp__orgx__list_entities type=decision status=pending`
   - `mcp__orgx__get_agent_status include_idle=true`
   - `mcp__orgx__recommend_next_action entity_type=workspace`

## Output

```markdown
# Nightly Recap - [Date]

## Summary

- Work completed: [highlights]
- Decisions still pending: [count]
- Risks still open: [count or none]

## Completed Work

- [task or milestone]

## Pending Decisions

- [decision]

## Agent Activity

- [agent summary]

## Tomorrow's First Move

> [single next action]
```
