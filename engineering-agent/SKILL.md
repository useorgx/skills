---
name: orgx-engineering-agent
description: |
  Produce high-confidence engineering artifacts for OrgX: RFCs, ADRs, code reviews, and postmortems.
  Use when technical decisions, implementation risk, reliability analysis, or engineering quality gates are required.
---

# OrgX Engineering Agent

## Quick Start

1. Confirm the artifact or decision type and the target audience.
2. Pull OrgX context with `mcp__orgx__list_entities` and `mcp__orgx__query_org_memory`.
3. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps

Deliver technically rigorous artifacts that are evidence-based and execution-ready.

## Trigger Map

Use this skill for:

- RFC authoring and architecture decisions
- ADR documentation
- Code review summaries and decision recommendations
- Incident postmortems with corrective actions

Do not use this skill for:

- Product positioning or campaign planning
- Pure design-system token work
- Sales collateral

## Required Inputs

Collect before drafting:

- `artifact_type`: `rfc` | `adr` | `review` | `postmortem`
- Scope: repo/service, owner, timeline, constraints
- Evidence: PR links, logs, metrics, incident timeline, historical context
- Decision context: non-goals, alternatives, known risks

Declare assumptions explicitly if data is missing.

## Operating Workflow

1. Select `artifact_type` and target decision.
2. Gather evidence:

- `mcp__orgx__query_org_memory` for precedent
- `mcp__github__*` for code/PR evidence
- `mcp__grafana__*` and `mcp__loki__*` for runtime evidence

3. Draft artifact in JSON (or Markdown with fenced JSON).
4. Validate:

```bash
python3 scripts/validate_engineering.py <artifact_file> --type <rfc|adr|review|postmortem>
```

5. Fix all failed gates and publish with `mcp__orgx__create_entity`.

## Artifact Contracts

### RFC (`--type rfc`)

Required fields:

- `title`
- `summary` (>=100 chars)
- `background` (>=150 chars, includes quantitative data)
- `proposal.description`
- `alternatives_considered` with >=2 options, each including `pros`, `cons`, `why_not`
- `migration_plan` with rollback strategy
- `risks` with mitigation
- `success_metrics`

### ADR (`--type adr`)

Required fields:

- `title`
- `status` in `proposed|accepted|deprecated|superseded`
- `context` (>=100 chars)
- `decision` (>=50 chars)
- `consequences` with >=2 entries

### Code Review (`--type review`)

Required fields:

- `pr_url`
- `summary` (>=50 chars)
- `verdict` in `approve|request_changes|comment`
- `security_review`
- `test_coverage`
- `comments[]` with `file` and `line`

### Postmortem (`--type postmortem`)

Required fields:

- `title`
- `severity` in `P1|P2|P3|P4`
- `timeline` with >=5 events
- `root_cause` (>=100 chars)
- `impact` with quantified detail
- `action_items` with >=3 entries and owners
- `lessons_learned` with >=2 entries

## Precision Loop (Run Every Time)

1. Structural pass: contract fields present and well-typed.
2. Evidence pass: every major claim ties to code, logs, metrics, or incident facts.
3. Risk pass: tradeoffs, rollback path, and residual risks are explicit.
4. Delivery pass: validator clean and recommendation language is executable.

## Tooling

Primary:

- `mcp__orgx__query_org_memory`
- `mcp__orgx__list_entities`
- `mcp__orgx__create_entity`

Optional (if configured):

- `mcp__github__get_pr`, `mcp__github__search_code`, `mcp__github__create_pr_comment`
- `mcp__grafana__query`, `mcp__loki__search`
- `mcp__pagerduty__acknowledge`

## Failure Handling

- Missing telemetry: state uncertainty and reduce confidence score.
- Missing repo context: request exact PR/commit links before final verdict.
- Validator errors: block publication until fixed.

## Definition of Done

- Artifact type matches request.
- Validator passes with zero errors.
- All decisions include tradeoffs and clear next actions.
- Artifact is persisted in OrgX with references to evidence.
