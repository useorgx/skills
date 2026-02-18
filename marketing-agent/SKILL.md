---
name: orgx-marketing-agent
description: |
  Produce high-confidence marketing artifacts for OrgX: campaign briefs, multichannel content packs, and nurture email sequences.
  Use when go-to-market messaging, campaign strategy, content execution, or channel performance planning is needed.
---

# OrgX Marketing Agent

## Quick Start

1. Confirm the artifact or decision type and the target audience.
2. Pull OrgX context with `mcp__orgx__list_entities` and `mcp__orgx__query_org_memory`.
3. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps

Deliver conversion-oriented, evidence-backed marketing assets with deterministic quality gates.

## Trigger Map

Use this skill for:

- Campaign strategy and brief creation
- Content packs for social/blog/email channels
- Nurture sequence authoring and optimization

Do not use this skill for:

- Product spec writing and technical architecture
- Incident response and runbooks
- Pure sales deal qualification

## Required Inputs

Collect before drafting:

- `artifact_type`: `campaign` | `content` | `sequence`
- Audience and segment context (ICP, pain, buying stage)
- Offer and positioning (problem, value prop, proof)
- Performance target (pipeline, conversion, CAC/LTV, adoption)
- Brand constraints and legal/compliance notes

If required context is missing, list assumptions first.

## Operating Workflow

1. Choose `artifact_type` and define one primary goal metric.
2. Gather evidence:

- Prior campaign context from `mcp__orgx__query_org_memory`
- Existing artifacts from `mcp__orgx__list_entities`
- Channel constraints from CMS or content platform when available

3. Draft JSON-first artifact.
4. Validate:

```bash
python3 scripts/validate_marketing.py <artifact_file> --type <campaign|content|sequence>
```

5. Fix all failed gates, then publish with `mcp__orgx__create_entity`.

## Artifact Contracts

### Campaign Brief (`--type campaign`)

Required fields:

- `campaign_name`
- `objective` with measurable target/date cues
- `target_audience.primary_icp`
- `target_audience.pain_points` (>=2)
- `messaging_pillars` (>=3, each with `proof_points`)
- `channels` (>=2)
- `success_metrics` (>=3 with numeric targets)
- `timeline` (>=2 milestones)
- `hypotheses` (>=1)

### Content Pack (`--type content`)

Required fields:

- `campaign_id`
- `content_items` (>=3)
- each item includes: `channel`, `content` (>=50 chars), `cta`
- LinkedIn items <= 3000 chars
- Twitter items are thread-formatted (`1/`) or <=280 chars

### Nurture Sequence (`--type sequence`)

Required fields:

- `emails` (>=5)
- each email includes: `subject`, `body` (>=100 chars), `cta`, `day`
- at least one body includes personalization token like `{{first_name}}`

## Content Studio Integration

When deliverable needs visuals, route through Content Studio before finalizing campaign assets.

Preferred tool flow:

1. Select brand or ingest assets:

- `studio_brands_list`
- `studio_brand_ingest`

2. Generate visuals:

- `studio_content_create`

3. Retrieve outputs:

- `studio_library_search`

If these tools are unavailable, produce copy + visual brief placeholders and flag dependency.

## Precision Loop (Run Every Time)

1. Strategy pass: objective, ICP, and positioning are coherent.
2. Evidence pass: every claim has proof point or measurable hypothesis.
3. Channel pass: format and CTA match channel constraints.
4. Delivery pass: validator clean and sequencing is execution-ready.

## Tooling

Primary:

- `mcp__orgx__query_org_memory`
- `mcp__orgx__list_entities`
- `mcp__orgx__create_entity`
- `mcp__orgx__spawn_agent_task`

Optional (if configured):

- `mcp__headless_cms__publish`
- `mcp__notion__create_page`

## Failure Handling

- Missing ICP precision: provide two candidate ICPs and mark primary assumption.
- Missing brand rules: default to existing OrgX tone from org memory and tag as provisional.
- Validator errors: do not publish until fixed.

## Definition of Done

- Artifact satisfies the validator contract.
- Messaging is specific, not generic, and tied to measurable outcomes.
- Channel plan is executable without additional clarification.
- Artifact is stored in OrgX and linked to campaign context.
