---
name: nightly-recap
description: |
  Draft nightly recaps summarizing OrgX activity including completed tasks, decisions made, and agent work.
  Use when: user asks for a daily summary, end-of-day recap, activity report, or wants to see what happened today.
  Triggers on: "nightly recap", "daily summary", "what happened today", "end of day report", "activity summary".
---

# Nightly Recap

Generate a summary of the day's OrgX activity.

## Required Tools

- `context.run_summary` - Get run activity
- `telemetry.errors.list` - Check for errors

## Workflow

1. **Fetch today's activity** using run summary tools
2. **Aggregate by category**:

   - Tasks completed
   - Decisions made
   - Artifacts created
   - Agent activity
   - Errors/issues encountered

3. **Generate recap** in this format:

```markdown
# Nightly Recap - [Date]

## 📊 Summary

- Tasks completed: X
- Decisions made: Y
- Artifacts created: Z

## ✅ Completed Tasks

| Task | Initiative | Completed By |
| ---- | ---------- | ------------ |

## 🎯 Decisions Made

| Decision | Outcome | Initiative |
| -------- | ------- | ---------- |

## 🤖 Agent Activity

| Agent | Tasks Completed | Time Active |
| ----- | --------------- | ----------- |

## ⚠️ Issues (if any)

- [List any errors or blocked items]

## 📝 Notes

[Any notable patterns or recommendations]
```

## Checklist

See [checklist.md](checklist.md) for validation items.
