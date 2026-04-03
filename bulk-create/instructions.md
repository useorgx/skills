You are bulk-creating OrgX tasks or milestones from a markdown list.

## Required Sequence

1. Call `mcp__orgx__orgx_bootstrap`.
2. Resolve the active workspace with `mcp__orgx__workspace`.
3. Parse the list items, skipping checked-off items unless the user explicitly wants them imported.
4. Resolve the parent initiative/workstream/milestone with `mcp__orgx__list_entities`.
5. Build one `mcp__orgx__batch_create_entities` payload using:
   - `ref` for each created item
   - `depends_on` for nested or sequential relationships
6. Only fall back to repeated `create_task` / `create_milestone` calls if batching is impossible.

## Parsing Rules

- preserve item order
- infer priority from title and description
- carry nested text into the item description
- do not invent parent entities

## Output

Report the created IDs, skipped items, and any per-item failures.
