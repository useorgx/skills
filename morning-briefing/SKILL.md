---
name: Morning Briefing
version: "2.1.0"
description: |
  Generate a daily OrgX briefing with morning-brief value signals, pending
  decisions, blocked tasks, agent activity, initiative health, and the single
  best next action for the active workspace.
---

# Morning Briefing

Generate a concise daily status report for the active OrgX workspace.

## Workflow

1. Bootstrap with `mcp__orgx__orgx_bootstrap` (the workspace auto-resolves; pass `workspace_id` only to override).
2. Fetch:
   - `mcp__orgx__get_operator_chronicle period=30d`
   - `mcp__orgx__orgx_recommend mode=morning_brief period=day`
   - `mcp__orgx__orgx_search type=decision status=pending`
   - `mcp__orgx__orgx_search type=task status=blocked`
   - `mcp__orgx__get_agent_status` for active and blocked agent runs
   - `mcp__orgx__orgx_recommend mode=next_action entity_type=workspace`
3. Prioritize the briefing:
   - `reportingNarrative.briefMarkdown` as the canonical report body
   - `reportingNarrative.nextAction`, `reportingNarrative.whatChanged`, and `rollups`
   - top priorities from the operator chronicle
   - decision chronology and what changed in the last 24 hours / week / 30 days
   - critical decisions
   - blocked work the user can unblock
   - artifacts, PR receipts, and reporting gaps
   - AQ scores on recent deliverables — call out anything held below the 0.85 gate or parked in `changes_requested`
   - value exceptions or risk signals
   - agents waiting on input
4. Decisions are settled only by the person, in the decisions widget (ordinary
   decisions, where the host renders it) or on the decision page in OrgX. Give
   each critical decision's `review_url`; never offer to approve or reject it
   on the user's behalf, and never report one as approved unless OrgX shows it
   settled.

## Output Format

```markdown
## Morning Brief Signals

- [operator chronicle headline, value delta, exceptions, notable receipts]
- [rollups: yesterday / past week / past 30 days]

## Decision Chronology

- [what changed yesterday, this week, and this month]

## Critical Decisions

- [decision summary — waiting on <person>, with its review link]

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
