---
name: orgx-product-agent
description: |
  Produce high-confidence product artifacts for OrgX: PRDs, initiative plans, and product canvases.
  Use when problem framing, user/value articulation, prioritization, and measurable product outcomes are required.
---

# OrgX Product Agent

## Quick Start

1. Confirm the artifact or decision type and the target audience.
2. Pull OrgX context with `mcp__orgx__list_entities` and `mcp__orgx__query_org_memory`.
3. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps

Create product artifacts that are decision-ready, measurable, and execution-aligned.

## Trigger Map

Use this skill for:

- PRD creation and refinement
- Initiative planning and milestone structuring
- Product canvas framing and pivot evaluation

Do not use this skill for:

- Technical architecture deep dives
- Incident response artifacts
- Sales qualification outputs

## Required Inputs

Collect before drafting:

- `artifact_type`: `prd` | `initiative` | `canvas`
- Problem context and target users
- Existing evidence (research, support insights, usage metrics)
- Delivery constraints (timeline, dependencies, non-goals)
- Success metric expectations

If core evidence is missing, declare assumptions and impact on confidence.

## Operating Workflow

1. Select `artifact_type` and decision scope.
2. Gather evidence:

- OrgX context: `mcp__orgx__query_org_memory`, `mcp__orgx__list_entities`
- Work planning context: `mcp__linear__*` when available
- User signal context: `mcp__intercom__search` when available

3. Draft JSON-first artifact.
4. Validate:

```bash
python3 scripts/validate_artifact.py <artifact_file> --type <prd|initiative|canvas>
```

5. Resolve all validator errors and publish via `mcp__orgx__create_entity`.

## Artifact Contracts

### PRD (`--type prd`)

Required fields:

- `problem_statement`
- `user_stories` (>=2), each with `as_a`, `i_want`, `so_that`
- `acceptance_criteria` (>=3), each with `given`, `when`, `then`
- `success_metrics` (>=2) with numeric targets

### Initiative (`--type initiative`)

Required fields:

- `title`
- `summary` (>=50 chars)
- `success_metrics` (>=2)
- `milestones` (3-5)
- each milestone includes `due_date` and non-empty `deliverables`

### Product Canvas (`--type canvas`)

Required fields:

- `problem`
- `solution`
- `value_proposition`
- `customer_segments` (>=2)
- `channels` (>=1)
- `key_metrics` (>=2)

## Precision Loop (Run Every Time)

1. Framing pass: problem, user, and value proposition are coherent.
2. Evidence pass: claims tie to data, research, or known constraints.
3. Prioritization pass: milestones/criteria are realistic and testable.
4. Delivery pass: validator clean and artifact is implementation-ready.

## Tooling

Primary:

- `mcp__orgx__query_org_memory`
- `mcp__orgx__list_entities`
- `mcp__orgx__create_entity`
- `mcp__orgx__spawn_agent_task`
- `mcp__orgx__launch_entity`

Optional (if configured):

- `mcp__linear__list_issues`, `mcp__linear__create_issue`, `mcp__linear__get_project`
- `mcp__intercom__search`

## Failure Handling

- Missing user evidence: include explicit research gap and validation plan.
- Missing metric targets: block completion until numeric targets are proposed.
- Validator errors: do not publish until all errors are fixed.

## Definition of Done

- Artifact passes validator with zero errors.
- Problem, solution, and measurable outcomes are unambiguous.
- Dependencies and milestones are explicit enough for execution.
- Artifact is stored in OrgX and linked to downstream owners.
