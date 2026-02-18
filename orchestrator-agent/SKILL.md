---
name: orgx-orchestrator-agent
description: |
  Coordinate high-confidence cross-domain execution in OrgX by creating initiatives, delegating to domain agents, and synthesizing outputs.
  Use when work spans multiple teams or requires explicit dependency, sequencing, and quality coordination.
---

# OrgX Orchestrator Agent

## Quick Start

1. Confirm the artifact or decision type and the target audience.
2. Pull OrgX context with `mcp__orgx__list_entities` and `mcp__orgx__query_org_memory`.
3. Produce the artifact using the contract below and return:
   - A concise summary (3-6 bullets)
   - The artifact body (JSON or structured Markdown)
   - 3 actionable next steps

Drive multi-agent execution with clear dependencies, quality gates, and accountable handoffs.

## Trigger Map

Use this skill for:

- Initiative planning across multiple domains
- Agent task delegation with explicit acceptance criteria
- Cross-domain synthesis and conflict resolution

Do not use this skill for:

- Single-domain deep work better handled by one specialist agent
- Artifact authoring that does not require orchestration

## Required Inputs

Collect before drafting:

- `artifact_type`: `initiative` | `delegation` | `synthesis`
- Business objective and target date
- Stakeholders and accountable owner
- Required participating agents
- Constraints: budget, deadlines, compliance, dependencies

If unknown, state assumptions and request missing owners/dates.

## Operating Workflow

1. Choose `artifact_type`.
2. Gather baseline context:

- `mcp__orgx__query_org_memory`
- `mcp__orgx__list_entities`
- `mcp__orgx__get_initiative_pulse` for in-flight work

3. Draft JSON-first artifact.
4. Validate:

```bash
python3 scripts/validate_orchestration.py <artifact_file> --type <initiative|delegation|synthesis>
```

5. Resolve all failed gates.
6. Execute orchestration:

- Create/launch initiative with `mcp__orgx__create_entity` and `mcp__orgx__launch_entity`
- Delegate with `mcp__orgx__spawn_agent_task`
- Close loop with `mcp__orgx__complete_entity`
- Emit progress checkpoints with `mcp__orgx__orgx_emit_activity`
- Batch state updates with `mcp__orgx__orgx_apply_changeset` (idempotent, transactional)

## Artifact Contracts

### Initiative Plan (`--type initiative`)

Required fields:

- `title`, `summary` (>=50 chars), `owner`, `target_date`
- `success_metrics` (>=2 with targets)
- `workstreams` (3-5), each with:
  - valid `agent` (`product-agent`, `engineering-agent`, `marketing-agent`, `sales-agent`, `design-agent`, `operations-agent`, `orchestrator-agent`)
  - `goal`
  - `milestones` (>=2)
- `risks` (>=2) with mitigations
- dependency graph with no circular dependencies

### Delegation Message (`--type delegation`)

Required fields:

- `target_agent` (valid)
- `context.background`
- `task.objective`
- `task.requirements` (>=2)
- `quality.acceptance_criteria` (>=2)
- `timeline.deadline`
- `handoff.output_format`

### Synthesis Report (`--type synthesis`)

Required fields:

- `initiative_id`
- `inputs` (>=2), each with source `agent`
- `conflicts` key present; each conflict includes `resolution`
- `synthesis` (>=200 chars)
- `recommendations` (>=3)
- `next_steps` (>=2)

## Precision Loop (Run Every Time)

1. Dependency pass: sequencing is coherent and non-circular.
2. Delegation pass: each task has owner, objective, and acceptance criteria.
3. Synthesis pass: conflicts are resolved with explicit decision rationale.
4. Delivery pass: validator clean and all spawned tasks are traceable.

## Tooling

Primary:

- `mcp__orgx__query_org_memory`
- `mcp__orgx__list_entities`
- `mcp__orgx__orgx_emit_activity`
- `mcp__orgx__orgx_apply_changeset`
- `mcp__orgx__create_entity`
- `mcp__orgx__launch_entity`
- `mcp__orgx__spawn_agent_task`
- `mcp__orgx__get_initiative_pulse`
- `mcp__orgx__complete_entity`

## Failure Handling

- Missing owner: do not launch initiative without accountable owner.
- Dependency ambiguity: block launch until DAG is explicit.
- Validator errors: fix before delegation.

## Definition of Done

- Artifact passes validator with zero errors.
- Delegations are actionable and assigned to valid agents.
- Initiative state is updated in OrgX and progress is observable.
