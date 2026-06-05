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
   - `mcp__orgx__get_operator_chronicle period=30d`
   - `mcp__orgx__orgx_recommend`
   - `mcp__orgx__orgx_search type=decision status=pending`
   - `mcp__orgx__orgx_search type=task status=blocked`
   - `mcp__orgx__orgx_recommend include_idle=false`
   - `mcp__orgx__orgx_recommend`
   - `mcp__orgx__orgx_recommend entity_type=workspace`
4. Prioritize the briefing:
   - `reportingNarrative.briefMarkdown` as the canonical report body
   - `reportingNarrative.nextAction`, `reportingNarrative.whatChanged`, and `rollups`
   - top priorities from the operator chronicle
   - decision chronology and what changed in the last 24 hours / week / 30 days
   - critical decisions
   - blocked work the user can unblock
   - artifacts, PR receipts, and reporting gaps
   - value exceptions or risk signals
   - agents waiting on input

## Output Format

```markdown
## Morning Brief Signals

- [operator chronicle headline, value delta, exceptions, notable receipts]
- [rollups: yesterday / past week / past 30 days]

## Decision Chronology

- [what changed yesterday, this week, and this month]

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

## Reporting Gaps

- [missing PR receipts, artifacts, execution receipts, unlinked goals, or duplicate decisions]
```
