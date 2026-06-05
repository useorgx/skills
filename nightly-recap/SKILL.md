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
2. Resolve the workspace with `mcp__orgx__orgx_bootstrap`.
3. Gather:
   - `mcp__orgx__get_operator_chronicle period=day`
   - `mcp__orgx__orgx_recommend`
   - `mcp__orgx__orgx_search type=task status=done`
   - `mcp__orgx__orgx_search type=decision status=pending`
   - `mcp__orgx__orgx_recommend include_idle=true`
   - `mcp__orgx__orgx_recommend entity_type=workspace`

Prefer `reportingNarrative.briefMarkdown` from the operator chronicle as the
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

- [decision]

## Proof Gaps

- [missing artifact, PR receipt, execution receipt, or unclear ownership]

## Agent Activity

- [agent summary]

## Tomorrow's First Move

> [single next action]
```
