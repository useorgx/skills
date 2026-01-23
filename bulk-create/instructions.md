You are bulk-creating tasks or milestones from a markdown checklist or bullet list.

## Input Parsing

Parse the user's input to extract items from:

1. **Checkbox lists**: `- [ ] Item title` or `- [x] Item title` (completed)
2. **Bullet lists**: `- Item title` or `* Item title`
3. **Numbered lists**: `1. Item title`

For each item, extract:

- **Title**: The main text of the item
- **Description**: Any sub-bullets or indented text under the item
- **Priority**: Detect from keywords in the title or description

## Priority Detection

Scan for priority keywords (case-insensitive):

- **high**: "urgent", "critical", "asap", "important", "high priority", "p0", "p1"
- **medium**: "medium priority", "p2", "normal"
- **low**: "low priority", "p3", "nice to have", "backlog"

Default to "medium" if no keywords found.

## Nested Items and Dependencies

If items are nested (indented under a parent):

```
- [ ] Parent task
  - [ ] Child task 1
  - [ ] Child task 2
```

1. Create the parent entity first
2. Create child entities with `blockedBy` set to parent's ID
3. Use `mcp__orgx__update_entity` to set dependencies after creation

## Entity Creation Process

1. **Confirm scope**: Ask the user which entity type to create:

   - `task` (default)
   - `milestone`

2. **Check context**: Use `mcp__orgx__list_entities` to verify:

   - Active initiative (if creating tasks under an initiative)
   - Active workspace context

3. **Create entities**: For each parsed item, call `mcp__orgx__create_entity` with:

   ```
   type: "task" or "milestone"
   title: <extracted title>
   description: <extracted description or empty>
   priority: <detected priority>
   initiative_id: <if applicable>
   ```

4. **Set dependencies**: For nested items, use `mcp__orgx__update_entity` to set `blockedBy` relationships

## Output Format

After creation, report a summary:

```
Created X entities:

| ID | Title | Priority | Dependencies |
|----|-------|----------|--------------|
| abc123 | Task title | high | - |
| def456 | Child task | medium | blocked by abc123 |

All entities created successfully under initiative: [initiative name]
```

## Error Handling

- If an entity fails to create, continue with remaining items
- Report failures at the end with the specific error
- Suggest fixes for common issues (missing initiative, invalid priority)

## Example Workflow

User provides:

```
- [ ] URGENT: Set up CI pipeline
  - [ ] Configure GitHub Actions
  - [ ] Add test coverage reporting
- [ ] Update documentation
- [ ] Nice to have: Add dark mode support
```

You should:

1. Parse 4 items (1 parent with 2 children, 2 standalone)
2. Detect priorities: high, medium, medium, low
3. Create parent task first, then children with dependencies
4. Create remaining standalone tasks
5. Report all created entities with IDs
