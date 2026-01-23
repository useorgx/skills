# OrgX Skills

Agent skills for [OrgX](https://useorgx.com) - the AI-powered operations platform.

## Installation

```bash
# Install all OrgX skills
npx add-skill useorgx/skills

# Install a specific skill
npx add-skill useorgx/skills/morning-briefing

# List available skills
npx add-skill useorgx/skills --list
```

## Available Skills

| Skill                                      | Description                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| [morning-briefing](./morning-briefing)     | Daily OrgX briefing with pending decisions, blocked tasks, and agent status |
| [initiative-kickoff](./initiative-kickoff) | Create complete initiatives from a one-line goal                            |
| [bulk-create](./bulk-create)               | Create multiple tasks from markdown checklists                              |
| [nightly-recap](./nightly-recap)           | End-of-day activity summary                                                 |

## Requirements

These skills require the [OrgX MCP server](https://mcp.useorgx.com) to be configured:

```json
{
  "mcpServers": {
    "orgx": {
      "type": "http",
      "url": "https://mcp.useorgx.com/mcp"
    }
  }
}
```

## Skill Format

Each skill follows [Anthropic's skill format](https://github.com/anthropics/skills):

```
skill-name/
├── SKILL.md      # Required: Instructions with YAML frontmatter
├── skill.toml    # Optional: OrgX registry metadata
└── references/   # Optional: Additional documentation
```

## Contributing

1. Fork this repository
2. Create a new skill directory with a `SKILL.md` file
3. Follow the [Anthropic skill authoring best practices](https://github.com/anthropics/skills/tree/main/skills/skill-creator)
4. Submit a pull request

## License

MIT
