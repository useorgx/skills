You are bulk-creating OrgX tasks or milestones from a markdown list.

## Required Sequence

1. Call `mcp__orgx__orgx_get_workspace_context` to read the active workspace (pass `workspace_id` only to override it).
2. Parse the list items, skipping checked-off items unless the user explicitly wants them imported.
3. Resolve the parent initiative/workstream/milestone with `mcp__orgx__orgx_search`.
4. Create items in list order with `mcp__orgx__orgx_create_task` (or `mcp__orgx__orgx_create_milestone` when the user asks for milestones). Give every call its own `idempotency_key`; a retry reuses the same key.
5. For a whole new initiative, validate with `mcp__orgx__orgx_validate_initiative_plan`, then create it with `mcp__orgx__orgx_create_initiative_hierarchy` (`plan`, `idempotency_key`).
6. Record nested or sequential relationships in each item's description; v2 has no batch changeset or `depends_on` argument.

## Parsing Rules

- preserve item order
- infer priority from title and description
- carry nested text into the item description
- do not invent parent entities

## Output

Report the created IDs, skipped items, and any per-item failures.
