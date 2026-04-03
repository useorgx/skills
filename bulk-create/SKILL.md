---
name: Bulk Create
description: |
  Create multiple OrgX tasks or milestones from a markdown checklist or bullet
  list. Uses batch creation, ref-based dependency wiring, and current workspace
  context instead of one-off entity creation loops.
---

# Bulk Create

Parse markdown lists and create multiple OrgX entities in one pass.

## Supported Formats

- checkbox lists: `- [ ] item`
- bullet lists: `- item` or `* item`
- numbered lists: `1. item`

Completed checkbox items are skipped by default.

## Workflow

1. Bootstrap with `mcp__orgx__orgx_bootstrap`.
2. Confirm or set workspace via `mcp__orgx__workspace`.
3. Parse the list into ordered items with priority, nesting, and completion state.
4. Check the parent initiative, milestone, or workstream with `mcp__orgx__list_entities`.
5. Build a single `mcp__orgx__batch_create_entities` payload:
   - use `ref` keys for each created item
   - use `depends_on` for nested or sequential dependencies
   - prefer `type=task` unless the user explicitly wants milestones
6. If a few standalone items are being added to an existing hierarchy, `mcp__orgx__create_task` or `mcp__orgx__create_milestone` is acceptable, but batch create is preferred.

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
- Prefer `depends_on` in the batch payload over patching dependencies after creation.

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
