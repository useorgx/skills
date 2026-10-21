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
| [orgx-capability-mindset](./orgx-capability-mindset) | Shared Software 3.0 judgment layer: verifier gates, agent-native outputs, jagged-risk routing, adversarial review, and MCP progress ledger |
| [orgx-quality-bar](./orgx-quality-bar)     | How OrgX judges artifacts: four-lens verification, domain layer stacks, the AQ 0.85 gate, artifact type codes and the mistype guard, GTM sendability checks, and the rework loop |
| [orgx-design](./orgx-design)               | Canonical OrgX product design system: full-surface audits, app and widget patterns, responsive/accessibility verification, cut protocol, and cross-tool drift control |
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

## Founder/Team Artifact Contract

All role agents inherit the shared
[orgx-capability-mindset](./orgx-capability-mindset) contract. Agents should
first identify whether the workspace is acting like an early founder,
founder-led company, or operating team, then produce the practical artifact that
moves the company forward now.

When attaching artifacts or receipts through OrgX MCP, use the canonical
cross-domain artifact type where possible:

| Agent | MCP artifact_type examples |
| --- | --- |
| Orchestrator | `orchestration.next_initiative` |
| Engineering | `eng.pull_request`, `eng.deploy_proof`, `eng.structured_blocker` |
| Sales | `sales.strategy`, `sales.icp_offer_sequence`, `sales.follow_up_sequence`, `sales.send_plan` |
| Marketing | `marketing.launch_asset`, `marketing.channel_hypothesis`, `marketing.offer_package` |
| Product | `product.customer_discovery`, `product.prd`, `product.pricing_hypothesis`, `product.decision_record` |
| Design | `design.audit`, `design.component_spec`, `design.token_package` |
| Operations | `ops.operator_brief`, `ops.runbook`, `ops.budget_envelope`, `ops.incident_status` |

Attach `agent_type`, `company_stage`, `business_outcome`, `owner`,
`review_date`, and `verification` metadata so OrgX can connect artifacts to
proof, recommendations, morning briefs, and skill improvement. Use local
validator `--type` names inside each skill; use the MCP `artifact_type` values
when saving the artifact to OrgX.

## Idempotent Writes

Every OrgX MCP write (`orgx_create_*`, `orgx_update_work`, the plan, lifecycle,
dispatch, decision, artifact, and completion calls) requires `idempotency_key`;
the server refuses a write without one with 400 `idempotency_key_required`.

- Mint one key per intended change, e.g. `<skill>-<entity>-<purpose>-<uuid>`
  (letters, digits, `.`, `_`, `:`, `/`, `-`; under 160 characters).
- Reuse a key only to retry the identical input; changed input gets a new key.
- On `outcome_unknown`, check `orgx_get_operation_status` and retry with the
  SAME key. On `forbidden`, stop — never route around it through another tool.

Agents may also see `approval_required`, `stale_version`, `stale_lease`,
`budget_exhausted`, `rate_limited`, and `idempotency_key_conflict`. The full
rule and what to do for each code live in
[orgx-capability-mindset](./orgx-capability-mindset/SKILL.md#idempotent-writes).

## Quality Bar

OrgX verifies every attached artifact with a four-lens system (judged,
measured, observed, outcome) and gates shipping at AQ 0.85. The
`artifact_type` you declare selects which domain layer stack judges the work,
and below-gate artifacts come back as rework with layer-specific feedback.
[orgx-quality-bar](./orgx-quality-bar) documents the full system — every
domain agent's Quality Bar section is derived from it.

## Verification

Run the repo-level drift check before opening a PR or shipping skill changes:

```bash
python3 scripts/check_skill_tool_drift.py
```

The check fails on deprecated OrgX tool names, unknown `mcp__orgx__*` references, and high-value workflow gaps such as spawning without `orgx_start_agent_task` or opening plan sessions without `orgx_start_plan`.

It also fails any example call to a write tool (listed under `write_tools` in
`scripts/orgx-v2-catalog.json`) that omits `idempotency_key`. A call is a tool
reference followed by its arguments — `tool(...)` / `tool {...}` in a code
block, prose `tool` (`arg`, ...), `tool` with `arg`, an inline
`tool arg=... arg=...`, a tool-list entry `tool` — takes `arg`, or a JSON
object naming the tool. Plain prose mentions of a tool name are not calls.

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

## About OrgX

[OrgX](https://useorgx.com) is proof for AI-delivered work — the operating record your agents and tools share. Agents in ChatGPT, Claude, Cursor, and Codex work from one record of decisions, approvals, and work receipts.

- [OrgX FAQ](https://useorgx.com/faq): what it is, who it's for, and what it costs
- [Agent work receipts](https://useorgx.com/agent-work-receipts): how finished agent work is checked and signed off
- [Pricing](https://useorgx.com/pricing)
- Hosted MCP server: [useorgx/orgx-mcp](https://github.com/useorgx/orgx-mcp)
