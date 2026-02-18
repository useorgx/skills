---
name: orgx-operations-agent
description: |
  Produce high-confidence operations artifacts for OrgX: incident analyses, operational playbooks, and budget controls.
  Use when reliability, incident management, escalation readiness, or operational cost governance is required.
---

# OrgX Operations Agent

## Quick Start

1. Confirm the artifact or decision type and the target audience.
2. Pull OrgX context with `mcp__orgx__list_entities` and `mcp__orgx__query_org_memory`.
3. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps

Deliver operational artifacts that reduce incident risk and improve response quality.

## Trigger Map

Use this skill for:

- Incident reports and corrective action plans
- Operational playbooks and escalation paths
- Budget variance analysis and operational forecasting

Do not use this skill for:

- Product roadmap decisions
- Marketing campaign copy
- Code-level architecture decisions

## Required Inputs

Collect before drafting:

- `artifact_type`: `incident` | `playbook` | `budget`
- Service or process scope
- Ownership model (DRI, on-call, escalation)
- Evidence source (logs, dashboards, ticket timelines, spend data)
- SLA/SLO or financial targets

If data is incomplete, state assumptions and confidence level.

## Operating Workflow

1. Pick `artifact_type` and define success condition.
2. Gather evidence:

- OrgX context: `mcp__orgx__query_org_memory`, `mcp__orgx__list_entities`
- Incident context: PagerDuty/observability tools when available

3. Draft JSON-first artifact.
4. Validate:

```bash
python3 scripts/validate_ops.py <artifact_file> --type <incident|playbook|budget>
```

5. Resolve all failed gates, then publish via `mcp__orgx__create_entity`.

## Artifact Contracts

### Incident Analysis (`--type incident`)

Required fields:

- `incident_id`, `title`, `severity` (`P1|P2|P3|P4`), `started_at`
- `impact.description` and `impact.users_affected`
- `timeline` with >=5 timestamped events in chronological order
- `root_cause.description` (>=100 chars)
- `action_items` (>=3, each with `owner` and `due_date`)
- `lessons_learned` (>=2)
- blameless language

### Playbook (`--type playbook`)

Required fields:

- `name`, `version`, `owner`
- `trigger.conditions` (>=1)
- `prerequisites`
- `steps` (>=5), each with `action` and `expected_outcome`
- at least half of steps include `if_fails`
- `escalation`
- `communication.templates` (>=1)
- `rollback.steps` (>=1)

### Budget Control (`--type budget`)

Required fields:

- `period`
- `categories` (>=3), each with `planned` and `actual`
- `variance_reason` for any category with >10% variance
- `recommendations` (>=3)
- `forecast`

## Precision Loop (Run Every Time)

1. Completeness pass: all mandatory fields present.
2. Operational realism pass: steps are executable by on-call responders.
3. Risk pass: escalation, rollback, and ownership are explicit.
4. Control pass: validator clean with no unresolved gaps.

## Tooling

Primary:

- `mcp__orgx__query_org_memory`
- `mcp__orgx__list_entities`
- `mcp__orgx__create_entity`

Optional (if configured):

- `mcp__pagerduty__list_incidents`, `mcp__pagerduty__get_incident`
- `mcp__grafana__get_dashboard`
- `mcp__datadog__query`

## Failure Handling

- Missing timeline precision: include estimated event times and mark uncertainty.
- Missing owner assignments: block completion and request DRI assignments.
- Validator errors: never publish until all errors are fixed.

## Definition of Done

- Artifact passes validator with zero errors.
- Incident and playbook outputs include clear ownership and rollback paths.
- Budget outputs include actionable recommendations tied to variance.
- Artifact is persisted in OrgX with traceable evidence links.
