---
name: Morning Briefing
description: |
  Generate a daily OrgX briefing with pending decisions, blocked tasks, agent status, and initiative health.
  Use when the user asks for: a daily briefing, morning update, status overview, what needs attention today,
  pending decisions summary, blocked work report, or any variation of "what should I work on first?"
  Triggers on: "morning briefing", "daily status", "what's pending", "show me blockers", "agent activity".
---

# Morning Briefing

Generate a concise daily status report for OrgX users.

## Workflow

1. **Fetch pending decisions** using `mcp__orgx__get_pending_decisions`

   - Filter by urgency: critical and high first
   - Sort by age (oldest first)

2. **Fetch blocked tasks** using `mcp__orgx__list_entities`

   - Type: `task`, status: `blocked`
   - Group by initiative

3. **Fetch agent status** using `mcp__orgx__get_agent_status`

   - Include active agents only by default
   - Show current task for each

4. **Fetch initiative health** using `mcp__orgx__get_initiative_pulse`

   - For active initiatives
   - Include blockers and upcoming milestones

5. **Synthesize and prioritize** the suggested first action:
   - Critical decision > Blocked high-priority task > Stale decision > Agent needing input

## Output Format

```markdown
## 🔴 Critical Decisions (X need attention)

| ID  | Title | Urgency | Age |
| --- | ----- | ------- | --- |

## 🟡 Blocked Tasks (X blocked)

| ID  | Title | Blocker | Unblock Owner |
| --- | ----- | ------- | ------------- |

## 🤖 Active Agents (X running)

| Agent | Domain | Current Task |
| ----- | ------ | ------------ |

## 📊 Initiative Health

| Name | Status | Health | Next Milestone |
| ---- | ------ | ------ | -------------- |

## ✅ Suggested First Action

> [Specific, actionable recommendation with entity ID]
```

## Priority Logic

Recommend first action based on:

1. Critical decision pending > 24 hours
2. High-priority task blocked by something user can resolve
3. Decision aging toward SLA breach
4. Agent waiting for input
5. Initiative at risk (health < 50%)
6. Stale task needing attention
7. Low-priority cleanup items
8. Proactive review if nothing urgent

## Error Handling

If any API call fails:

- Continue with available data
- Note missing sections
- Never block on partial failures
