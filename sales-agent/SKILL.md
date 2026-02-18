---
name: orgx-sales-agent
description: |
  Produce high-confidence sales artifacts for OrgX: competitive battlecards, MEDDIC deal scorecards, and outreach sequences.
  Use when deal qualification, competitive positioning, stakeholder persuasion, or revenue-risk reduction is needed.
---

# OrgX Sales Agent

## Quick Start

1. Confirm the artifact or decision type and the target audience.
2. Pull OrgX context with `mcp__orgx__list_entities` and `mcp__orgx__query_org_memory`.
3. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps

Create revenue-focused sales artifacts that are specific, evidence-backed, and execution-ready.

## Trigger Map

Use this skill for:

- Competitive battlecards
- MEDDIC scoring and gap analysis
- Multi-touch outreach sequences

Do not use this skill for:

- Marketing campaign planning
- Engineering architecture or code review
- Incident operations playbooks

## Required Inputs

Collect before drafting:

- `artifact_type`: `battlecard` | `meddic` | `sequence`
- Deal context (segment, ACV, stage, timeline)
- Stakeholder map and known pain points
- Competitive evidence and objections
- Compliance constraints for outreach

State assumptions if deal data is incomplete.

## Operating Workflow

1. Select `artifact_type`.
2. Gather evidence:

- OrgX historical context via `mcp__orgx__query_org_memory`
- CRM/call context via `mcp__salesforce__*` and `mcp__gong__*` when available

3. Draft JSON-first artifact.
4. Validate:

```bash
python3 scripts/validate_sales.py <artifact_file> --type <battlecard|meddic|sequence>
```

5. Resolve all validator errors and publish with `mcp__orgx__create_entity`.

## Artifact Contracts

### Battlecard (`--type battlecard`)

Required fields:

- `competitor`
- `segment` in `enterprise|mid-market|smb`
- `quick_summary` (>=100 chars)
- `differentiation` (>=3), each with `proof`
- `objection_handlers` (>=4), each with `response`
- `landmines` (>=3)
- `win_strategies` (>=2)

### MEDDIC Scorecard (`--type meddic`)

Required fields:

- `deal_name`, `deal_value` (>0)
- `scores` with all MEDDIC elements:
  - `metrics`, `economic_buyer`, `decision_criteria`, `decision_process`, `identify_pain`, `champion`
- each score in 1-5 range
- at least one element includes non-empty `gaps`
- `next_steps` (>=2), each with `owner`
- `risk_level` in `high|medium|low`

### Outreach Sequence (`--type sequence`)

Required fields:

- `target_persona`
- `pain_points` (>=2)
- `emails` (>=5)
- each email includes `subject`, `body` (>=100 chars), `cta`, `day`
- at least one email includes personalization token (`{{...}}`)
- `follow_up_rules`

## Precision Loop (Run Every Time)

1. Qualification pass: stakeholder and buying-process gaps are explicit.
2. Proof pass: every claim has evidence or clear confidence level.
3. Messaging pass: personalization and CTA progression are coherent.
4. Delivery pass: validator clean and next actions have owners.

## Tooling

Primary:

- `mcp__orgx__query_org_memory`
- `mcp__orgx__list_entities`
- `mcp__orgx__create_entity`
- `mcp__orgx__spawn_agent_task`

Optional (if configured):

- `mcp__salesforce__get_opportunity`, `mcp__salesforce__update_opportunity`
- `mcp__gong__search`, `mcp__gong__get_calls`

## Failure Handling

- Missing economic-buyer signal: flag MEDDIC risk as elevated and block green status.
- Missing competitive proof: mark as hypothesis and request verification.
- Validator errors: do not publish until all errors are fixed.

## Definition of Done

- Artifact passes validator with zero errors.
- Recommendation language is concrete and rep-executable.
- Risks and blockers are explicit, owner-assigned, and time-bound.
- Artifact is stored in OrgX and linked to deal context.
