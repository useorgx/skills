---
name: Bulk Create
version: "2.2.0"
description: |
  Create multiple OrgX tasks or milestones from a markdown checklist or bullet
  list. Uses typed create operations with one idempotency key per item, ordered
  dependency notes, and current workspace context.
---

# Bulk Create

Parse markdown lists and create multiple OrgX entities in one pass.

## Supported Formats

- checkbox lists: `- [ ] item`
- bullet lists: `- item` or `* item`
- numbered lists: `1. item`

Completed checkbox items are skipped by default.

## Workflow

1. Read workspace context with `mcp__orgx__orgx_get_workspace_context` (pass `workspace_id` only when overriding the auto-resolved workspace). It reads; it does not select a workspace.
2. Parse the list into ordered items with priority, nesting, and completion state.
3. Check the parent initiative, milestone, or workstream with `mcp__orgx__orgx_search`.
4. Create each item with a typed call, in list order, each with its own stable `idempotency_key`:
   - `mcp__orgx__orgx_create_task` (needs `workstream_id`, `idempotency_key`; `milestone_id` optional) is the default
   - `mcp__orgx__orgx_create_milestone` (needs `workstream_id`, `idempotency_key`) only when the user explicitly wants milestones
   - a retried create reuses the same `idempotency_key`, so a repeat never makes a duplicate
5. If the list describes a whole new initiative (initiative, workstreams, milestones, tasks), validate the plan with `mcp__orgx__orgx_validate_initiative_plan`, then create it in one call with `mcp__orgx__orgx_create_initiative_hierarchy` (`plan`, `idempotency_key`).

v2 has no generic batch changeset. Do not look for one; use the typed create calls above.

## Priority Detection

| Keywords | Priority |
| --- | --- |
| urgent, critical, ASAP, P0, blocker | high |
| important, P1, high priority | high |
| normal, P2, medium priority | medium |
| low priority, P3, backlog, nice to have | low |

Default priority is `medium`.

## Dependency Logic

- Nested items depend on their nearest parent item.
- Sequential mode is optional; only apply it when the user asks for ordered execution.
- The typed create calls take no dependency argument. Record the dependency in the item description ("Depends on: <title or id>"). For a new initiative, express dependencies inside the `plan` given to `mcp__orgx__orgx_create_initiative_hierarchy`.

## Output Format

```
Bulk create complete

Created:
- [id] [title] ([priority])

Skipped:
- [title] — already complete

Errors:
- [title] — [reason]
```
