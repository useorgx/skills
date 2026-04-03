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
| [product-agent](./product-agent)           | 100x product domain expert: PRDs, initiatives, canvases, research briefs, competitive analyses, prioritization matrices, pivot evaluations, dashboard specs, launch readiness |
| [engineering-agent](./engineering-agent)   | 100x engineering domain expert: RFCs, ADRs, code reviews, postmortems, tech debt inventories, capacity plans, runbooks, migration playbooks, dependency audits, perf budgets |
| [marketing-agent](./marketing-agent)       | 100x marketing domain expert: campaign briefs, content packs, nurture sequences, positioning docs, messaging matrices, competitive narratives, launch plans, analyst briefs, community strategies |
| [sales-agent](./sales-agent)               | 100x sales domain expert: battlecards, MEDDIC scorecards, outreach sequences, territory plans, QBR decks, deal reviews, win/loss analyses, pricing proposals, partner pitches |
| [design-agent](./design-agent)             | 100x design domain expert: WCAG audits, design tokens, component docs, interaction specs, UX research plans, critiques, motion specs, dark mode audits, breakpoint maps |
| [operations-agent](./operations-agent)     | 100x operations domain expert: incident analyses, playbooks, budget controls, capacity plans, vendor evaluations, SLO proposals, chaos test plans, migration checklists, on-call audits |
| [orchestrator-agent](./orchestrator-agent) | 100x orchestration expert: initiative plans, delegations, synthesis reports, retrospectives, dependency audits, resource allocations, risk registers, stakeholder updates, program status |
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

## Verification

Run the repo-level drift check before opening a PR or shipping skill changes:

```bash
python3 scripts/check_skill_tool_drift.py
```

The check fails on deprecated OrgX tool names, unknown `mcp__orgx__*` references, and high-value workflow gaps such as spawning without `check_spawn_guard` or opening plan sessions without `complete_plan`.

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
