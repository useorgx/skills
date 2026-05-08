---
name: Morning Briefing
version: "2.0.0"
description: |
  Generate a daily OrgX briefing with morning-brief value signals, pending
  decisions, blocked tasks, agent activity, initiative health, and the single
  best next action for the active workspace.
---

# Morning Briefing

Generate a concise daily status report for the active OrgX workspace.

## Workflow

1. Bootstrap with `mcp__orgx__orgx_bootstrap`.
2. Resolve the workspace with `mcp__orgx__orgx_bootstrap`.
3. Fetch:
   - `mcp__orgx__orgx_recommend`
   - `mcp__orgx__orgx_search type=decision status=pending`
   - `mcp__orgx__orgx_search type=task status=blocked`
   - `mcp__orgx__orgx_recommend include_idle=false`
   - `mcp__orgx__orgx_recommend`
   - `mcp__orgx__orgx_recommend entity_type=workspace`
4. Prioritize the briefing:
   - critical decisions
   - blocked work the user can unblock
   - value exceptions or risk signals
   - agents waiting on input

## Output Format

```markdown
## Morning Brief Signals

- [value delta, exceptions, notable receipts]

## Critical Decisions

- [decision summary]

## Blocked Tasks

- [task summary]

## Active Agents

- [agent + current work]

## Initiative Health

- [highest-risk initiatives]

## Suggested First Action

> [single actionable recommendation]
```
