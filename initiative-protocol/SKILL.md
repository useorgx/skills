---
name: initiative-protocol
version: "2.1.0"
description: |
  Initiative lifecycle management for OrgX. Handles workspace selection,
  hierarchy scaffolding, launch, monitoring, evidence attachment, and completion.
  Use when planning or managing an OrgX initiative.
---

# Initiative Protocol

Use this protocol whenever the user is creating, updating, launching, pausing, or closing an initiative.

## Core Loop

1. Bootstrap the session with `mcp__orgx__orgx_bootstrap` (pass `workspace_id` only when overriding the auto-resolved workspace).
2. Load the target initiative with `mcp__orgx__orgx_search type=initiative`, then hydrate it with `mcp__orgx__orgx_inspect type=initiative`.
3. Create or update the hierarchy using the highest-level wrapper available (`mcp__orgx__scaffold_initiative` for a full hierarchy; `mcp__orgx__orgx_write` for single entities).
4. Attach evidence, plans, and notes back to the initiative before marking it complete.

## Creating an Initiative

1. Check for related work:
   - `mcp__orgx__orgx_search` for prior initiatives or decisions
   - `mcp__orgx__orgx_search type=initiative` for active duplicates
2. Prefer `mcp__orgx__scaffold_initiative` when the request includes milestones, workstreams, or starter tasks — one call creates the whole hierarchy and auto-resolves the workspace (include explicit `workstreams` to preserve the user's structure; omit them to enable auto-planning).
3. Use `mcp__orgx__orgx_write operation=create type=initiative` only for a single initiative shell with no nested hierarchy yet.
4. For follow-on edits, prefer:
   - `mcp__orgx__orgx_write operation=update` for single-entity field changes
   - `mcp__orgx__orgx_write operation=create` for one new child at a time
   - `mcp__orgx__orgx_apply_changeset` with `ref` keys and an `idempotency_key` when creating or mutating several related children at once
5. Launch or pause through `mcp__orgx__orgx_act`:
   - launch: `type=initiative action=launch`
   - pause: `type=initiative action=pause`

## Monitoring

- `mcp__orgx__get_initiative_pulse` for health, blockers, milestones, and AQ-scored deliverables (scored artifacts rank first)
- `mcp__orgx__orgx_inspect type=initiative hydrate_context=true` for stream progress and bottlenecks
- `mcp__orgx__orgx_recommend mode=next_action entity_type=initiative` when the user asks what to do next
- `mcp__orgx__orgx_act action=update note="..."` for status notes that should live on the initiative itself

## Completion

1. Confirm all dependent work is done or intentionally deferred.
2. Run `mcp__orgx__orgx_act type=initiative action=validate dry_run=true` to surface anything unfinished.
3. Attach proof with `mcp__orgx__orgx_attach` (always set `artifact_type` — see the `orgx-quality-bar` skill) for plans, docs, URLs, or deliverable artifacts.
4. If planning happened in OrgX, finish the plan loop with `mcp__orgx__orgx_plan action=complete attach_to=[...]` so the rationale is attached to the initiative context.
5. Mark complete with `mcp__orgx__orgx_act type=initiative action=complete` (or `action=complete_with_proof` to land evidence in the same call).

## Risk Handling

- Use `mcp__orgx__orgx_act type=initiative action=pause note="..."` for blockers or intentional holds.
- Use `mcp__orgx__orgx_act action=flag_risk` when the priority problem is risk or sequencing, not state.
- Record durable exceptions on the entity (`orgx_act action=update note="..."` or a decision via `mcp__orgx__orgx_decide action=create`) instead of burying them in the chat transcript.
