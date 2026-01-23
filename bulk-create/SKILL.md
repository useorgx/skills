---
name: Bulk Create
description: |
  Create multiple OrgX tasks or milestones from a markdown checklist or bullet list.
  Automatically detects priorities from keywords and sets up dependencies for nested items.
  Use when: importing a task list, creating multiple items at once, converting notes to tasks,
  or batch-creating entities from any list format.
  Triggers on: "bulk create", "create tasks from list", "import checklist", "batch create".
  Supports: checkbox lists (- [ ]), bullet lists (- or *), numbered lists (1.).
---

# Bulk Create

Parse markdown lists and create multiple OrgX entities in batch.

## Supported Formats

```markdown
# Checkbox lists

- [ ] Task one
- [ ] Task two (urgent)
- [x] Already done (skipped)

# Bullet lists

- Task one
- Task two
  - Subtask (creates dependency)

# Numbered lists

1. First task
2. Second task (high priority)

# Mixed priorities

- [CRITICAL] Fix security issue
- [P0] Launch blocker
- Task with (urgent) keyword
- (low priority) Nice to have
```

## Workflow

1. **Parse input** to extract items:

   - Title: main text content
   - Priority: detected from keywords
   - Parent: if nested under another item
   - Checked: skip if already checked [x]

2. **Confirm scope** with user:

   - Entity type: task (default) or milestone
   - Parent initiative/workstream/milestone
   - Default priority if not detected

3. **Check context** using `mcp__orgx__list_entities`

   - Verify parent entities exist
   - Avoid duplicates

4. **Create entities** using `mcp__orgx__create_entity`

   - Process in order (parents before children)
   - Capture IDs for dependency setup

5. **Set dependencies** using `mcp__orgx__update_entity`
   - Nested items blocked by their parent
   - Sequential items can be linked if requested

## Priority Detection

| Keywords                                            | Priority |
| --------------------------------------------------- | -------- |
| urgent, critical, ASAP, P0, blocker, [CRITICAL]     | high     |
| important, P1, high priority                        | high     |
| normal, P2, medium priority                         | medium   |
| low priority, P3, nice to have, backlog, eventually | low      |

Default: medium (if no keywords detected)

## Output Format

```
✅ Bulk Create Complete

| # | Title | Priority | ID | Blocked By |
|---|-------|----------|----|-----------|
| 1 | Task one | high | task_xxx | - |
| 2 | Task two | medium | task_yyy | - |
| 3 | Subtask | medium | task_zzz | task_yyy |

📊 Summary:
  - Created: X entities
  - Dependencies: Y set
  - Skipped: Z (already checked or errors)

❌ Errors (if any):
  - "Item text": [error message]
```

## Dependency Logic

```
- Parent task
  - Child task 1    → blockedBy: [parent]
  - Child task 2    → blockedBy: [parent]
    - Grandchild    → blockedBy: [child 2]
```

For sequential mode (optional):

```
1. First   → blockedBy: []
2. Second  → blockedBy: [first]
3. Third   → blockedBy: [second]
```

## Error Handling

- Continue on individual failures
- Report all errors at end
- Never fail entire batch for one item
- Rollback not supported (items remain if created)
