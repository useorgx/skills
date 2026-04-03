---
name: Initiative Kickoff
description: |
  Create a complete OrgX initiative from a one-line goal, using the current
  workspace, hierarchy scaffolding tools, and guarded agent delegation.
  Use when the user wants to start a new project, create an initiative, kick
  off work on a goal, set up a project structure, or bootstrap a new effort.
---

# Initiative Kickoff

Transform a goal into a structured OrgX initiative with milestones, workstreams, starter tasks, and optional agent delegation.

## Quick Start

1. Bootstrap the session with `mcp__orgx__orgx_bootstrap`.
2. Confirm or set the target workspace with `mcp__orgx__workspace`.
3. Check for duplicate or overlapping initiatives.
4. Prefer `mcp__orgx__scaffold_initiative` for the full hierarchy.
5. Launch only if the user wants execution to start now.

## Workflow

1. Parse the goal:
   - target outcome
   - likely domains
   - timeline hints
   - success indicators
2. Check context:
   - `mcp__orgx__list_entities type=initiative`
   - `mcp__orgx__query_org_memory` for similar efforts or prior decisions
3. Create the full hierarchy with `mcp__orgx__scaffold_initiative`.
4. If the user requests specific agent delegation:
   - call `mcp__orgx__check_spawn_guard`
   - then `mcp__orgx__spawn_agent_task`
5. Launch with `mcp__orgx__entity_action type=initiative action=launch` when the initiative should go live immediately.
6. Finish with `mcp__orgx__recommend_next_action` so the user knows the first move after kickoff.

## Default Structure

- 3-5 milestones
- 2-6 workstreams depending on domain spread
- 2-4 starter tasks per workstream
- an orchestrator-owned coordination path when more than two domains are involved

## Timeline Inference

- 1 domain: 2 weeks
- 2-3 domains: 4-6 weeks
- 4+ domains: 8-12 weeks

## Output Format

```
Initiative created: [title] ([id])

Milestones:
- [milestone title] — [due date]

Workstreams:
- [domain] — [task count] starter tasks

Delegation:
- [agent assignment summary or "none"]

Next action:
- [single highest-leverage next step]
```

## Failure Handling

- If a similar initiative exists, stop and ask whether to extend it or create a new one.
- If the workspace is unset, resolve it before scaffolding anything.
- If spawn guard blocks delegation, create the initiative anyway and report the block explicitly.
