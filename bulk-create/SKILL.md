---
name: Bulk Create
version: "2.1.0"
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

1. Bootstrap with `mcp__orgx__orgx_bootstrap` (pass `workspace_id` only when overriding the auto-resolved workspace).
2. Parse the list into ordered items with priority, nesting, and completion state.
3. Check the parent initiative, milestone, or workstream with `mcp__orgx__orgx_search`.
4. Build a single `mcp__orgx__orgx_apply_changeset` payload with an `idempotency_key`:
   - use `ref` keys for each created item
   - use `depends_on` for nested or sequential dependencies
   - prefer `type=task` unless the user explicitly wants milestones
5. If only one or two standalone items are being added to an existing hierarchy, individual `mcp__orgx__orgx_write operation=create` calls are acceptable, but the batch changeset is preferred.

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
