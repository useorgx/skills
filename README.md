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
| [product-agent](./product-agent)           | Product artifacts: PRDs, initiatives, product canvases                      |
| [engineering-agent](./engineering-agent)   | Engineering artifacts: RFCs, ADRs, reviews, postmortems                     |
| [marketing-agent](./marketing-agent)       | Marketing artifacts: briefs, content packs, campaign plans                  |
| [sales-agent](./sales-agent)               | Sales artifacts: battlecards, MEDDIC, outreach sequences                    |
| [design-agent](./design-agent)             | Design artifacts: audits, tokens, component docs                            |
| [operations-agent](./operations-agent)     | Operations artifacts: playbooks, budgets, incident analysis                 |
| [orchestrator-agent](./orchestrator-agent) | Cross-domain coordination and initiative orchestration                      |
| [initiative-protocol](./initiative-protocol) | Initiative lifecycle creation, launch, monitoring, completion              |
| [milestone-protocol](./milestone-protocol) | Milestone tracking, risk flags, completion                                  |
| [workstream-protocol](./workstream-protocol) | Workstream execution lifecycle and blockers                                |
| [task-protocol](./task-protocol)           | Task lifecycle execution and status reporting                               |

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
