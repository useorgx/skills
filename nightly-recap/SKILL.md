---
name: nightly-recap
version: "2.2.0"
description: |
  Draft nightly recaps summarizing OrgX workspace activity including completed
  work, pending decisions, active agents, and notable risks still open at the
  end of the day.
---

# Nightly Recap

Generate an end-of-day OrgX summary for the active workspace.

## Required Sequence

1. Call `mcp__orgx__orgx_get_workspace_context` (read-only; it reads the workspace and does not select one or open a session; pass `workspace_id` only to override).
2. Gather:
   - `mcp__orgx__orgx_get_operator_brief` with `period=day`
   - `mcp__orgx__orgx_search` with `type=task`, `status=done`
   - `mcp__orgx__orgx_list_pending_decisions` (each carries a review link; only a person settles it)
   - `mcp__orgx__orgx_get_agent_status` with `include_idle=true`
   - `mcp__orgx__orgx_get_next_actions`

Prefer `reportingNarrative.briefMarkdown` from the operator brief as the
canonical recap body. Add only context that is missing from that body.

## Output

```markdown
# Nightly Recap - [Date]

## Summary

- Work completed: [highlights]
- Decisions still pending: [count]
- Decision chronology: [what changed today from reportingNarrative.whatChanged and rollups]
- Artifacts and PR receipts: [proof attached today]
- Risks still open: [count or none]

## Completed Work

- [task or milestone]

## Pending Decisions

- [decision — waiting on <person>, with its review link]

## Proof Gaps

- [missing artifact, PR receipt, execution receipt, or unclear ownership]
- [artifacts held below the AQ 0.85 gate or sitting in changes_requested awaiting rework]

## Agent Activity

- [agent summary]

## Tomorrow's First Move

> [single next action]
```
