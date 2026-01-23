---
name: Initiative Kickoff
description: |
  Create a complete OrgX initiative from a one-line goal, with milestones, workstreams, tasks, and agent assignments.
  Use when the user wants to: start a new project, create an initiative, kick off work on a goal,
  set up a project structure, or bootstrap a new effort.
  Triggers on: "kickoff", "new initiative", "start project", "create initiative for", "set up [goal]".
  NOT for: updating existing initiatives, simple task creation, or research questions.
---

# Initiative Kickoff

Transform a goal into a structured OrgX initiative with milestones, workstreams, and initial tasks.

## Workflow

1. **Parse the goal** to extract:

   - Core objective (what success looks like)
   - Domain signals (engineering, product, marketing, etc.)
   - Timeline hints (if mentioned)
   - Success indicators

2. **Check context** using `mcp__orgx__list_entities`

   - Verify no duplicate initiative exists
   - Check for related initiatives to link

3. **Create initiative** using `mcp__orgx__create_entity`

   ```json
   {
     "type": "initiative",
     "title": "[Derived from goal]",
     "description": "[Expanded goal with context]",
     "priority": "high"
   }
   ```

4. **Create 3-5 milestones** following this pattern:

   - M1: Discovery/Planning (10-15% of timeline)
   - M2: Foundation/Setup (15-20%)
   - M3: Core Development (40-50%)
   - M4: Integration/Testing (15-20%)
   - M5: Launch/Delivery (10-15%)

5. **Create workstreams** by detected domains:

   - Engineering: technical implementation
   - Product: requirements, specs, prioritization
   - Marketing: positioning, launch prep
   - Sales: enablement, outreach prep
   - Operations: processes, tooling
   - Design: UX/UI, visual assets

6. **Create 2-4 initial tasks per workstream**:

   | Domain      | Starter Tasks                                 |
   | ----------- | --------------------------------------------- |
   | Engineering | Tech spike, architecture doc, dev environment |
   | Product     | PRD draft, user stories, acceptance criteria  |
   | Marketing   | Messaging brief, positioning doc              |
   | Sales       | ICP definition, battlecard draft              |
   | Operations  | Process mapping, tool evaluation              |
   | Design      | Design brief, wireframes, style exploration   |

7. **Assign agents** (if requested) using `mcp__orgx__spawn_agent_task`

8. **Launch initiative** (if requested) using `mcp__orgx__launch_entity`

## Output Format

```
✅ Initiative Created: [title] (ID: init_xxx)

📍 Milestones (X created):
  M1: [title] - Due: [date] (ID: ms_xxx)
  M2: [title] - Due: [date] (ID: ms_xxx)
  ...

🔀 Workstreams (X created):
  - [domain]: [X tasks] (ID: ws_xxx)
  ...

📋 Tasks Created: X total

🤖 Agents Assigned: [list or "none - use /delegate to assign"]

🔗 Next Steps:
  1. Review milestones and adjust dates
  2. Add specific tasks to workstreams
  3. Assign agents with: delegate-task [task_id] to [agent]
```

## Timeline Inference

If no timeline specified:

- Small initiative (1 domain): 2 weeks
- Medium initiative (2-3 domains): 4-6 weeks
- Large initiative (4+ domains): 8-12 weeks

Set milestone due dates proportionally.

## Domain Detection

Detect domains from goal keywords:

- "build", "implement", "code", "API" → engineering
- "launch", "campaign", "content" → marketing
- "sell", "pipeline", "deal" → sales
- "design", "UI", "UX" → design
- "process", "workflow", "automate" → operations
- "spec", "requirements", "feature" → product
