You are creating a new OrgX initiative from a single goal statement.

## Required Sequence

1. Call `mcp__orgx__orgx_bootstrap`.
2. Call `mcp__orgx__orgx_bootstrap action=get`.
3. If no workspace is active, call `mcp__orgx__orgx_bootstrap action=list`, pick the default (or ask the user if the choice is ambiguous), then call `mcp__orgx__orgx_bootstrap action=set`.
4. Check for overlapping initiatives with:
   - `mcp__orgx__orgx_search type=initiative`
   - `mcp__orgx__orgx_search`
5. Prefer `mcp__orgx__orgx_write` to create the full initiative, workstream, milestone, and starter-task hierarchy in one call.
6. If the user asks for agent delegation, call `mcp__orgx__orgx_spawn` before `mcp__orgx__orgx_spawn`.
7. If the user wants execution to begin now, launch with `mcp__orgx__orgx_act type=initiative action=launch`.
8. End with `mcp__orgx__orgx_recommend` for the created initiative.

## Hierarchy Expectations

- Use 3-5 milestones unless the user specifies a tighter structure.
- Use only the domains implied by the goal.
- Add an orchestrator path when the effort spans more than two domains or has non-trivial dependencies.
- Keep starter tasks small enough to be owned by one agent.

## Output

Report:

- initiative title and ID
- milestones created
- workstreams created
- any delegated agents
- the single best next action
