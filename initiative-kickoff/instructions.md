You are creating a new OrgX initiative from a single goal statement.

## Required Sequence

1. Call `mcp__orgx__orgx_get_workspace_context` (pass `workspace_id` only to override the auto-resolved workspace). It reads context; it does not select a workspace or create a session. If the workspace is ambiguous, ask the user which one to use.
2. Check for overlapping initiatives with:
   - `mcp__orgx__orgx_search type=initiative`
   - `mcp__orgx__orgx_search`
3. Validate the proposed hierarchy with `mcp__orgx__orgx_validate_initiative_plan`, then create the full initiative, workstream, milestone, and starter-task hierarchy in one call with `mcp__orgx__orgx_create_initiative_hierarchy` (`plan`, `idempotency_key`). Retry with the same `idempotency_key` if the outcome is unclear.
4. If the user asks for agent delegation, call `mcp__orgx__orgx_estimate_agent_task` before `mcp__orgx__orgx_start_agent_task`.
5. If the user wants execution to begin now, launch with `mcp__orgx__orgx_launch_initiative`.
6. End with `mcp__orgx__orgx_get_next_actions` for the created initiative.

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
- any delegated agents, each as started (with its operation ID, polled via `mcp__orgx__orgx_get_operation_status`) rather than done
- the single best next action
