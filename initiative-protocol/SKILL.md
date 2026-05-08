---
name: initiative-protocol
version: "2.0.0"
description: |
  Initiative lifecycle management for OrgX. Handles workspace selection,
  hierarchy scaffolding, launch, monitoring, evidence attachment, and completion.
  Use when planning or managing an OrgX initiative.
---

# Initiative Protocol

Use this protocol whenever the user is creating, updating, launching, pausing, or closing an initiative.

## Core Loop

1. Bootstrap the session with `mcp__orgx__orgx_bootstrap`.
2. Ensure the correct workspace is active with `mcp__orgx__orgx_bootstrap`.
3. Load the target initiative with `mcp__orgx__orgx_search` or `mcp__orgx__orgx_recommend`.
4. Create or update the hierarchy using the highest-level wrapper available.
5. Attach evidence, plans, and notes back to the initiative before marking it complete.

## Creating an Initiative

1. Check for related work:
   - `mcp__orgx__orgx_search` for prior initiatives or decisions
   - `mcp__orgx__orgx_search type=initiative` for active duplicates
2. Prefer `mcp__orgx__orgx_write` when the request includes milestones, workstreams, or starter tasks.
3. Use `mcp__orgx__orgx_write type=initiative` only for a single initiative shell with no nested hierarchy yet.
4. For follow-on edits, prefer:
   - `mcp__orgx__orgx_write`
   - `mcp__orgx__orgx_write`
   - `mcp__orgx__orgx_write` when creating several related children at once
5. Launch or pause through `mcp__orgx__orgx_act`:
   - launch: `type=initiative action=launch`
   - pause: `type=initiative action=pause`

## Monitoring

- `mcp__orgx__orgx_recommend` for health, blockers, and milestones
- `mcp__orgx__orgx_inspect` for stream progress and bottlenecks
- `mcp__orgx__orgx_recommend` when the user asks what to do next
- `mcp__orgx__orgx_act` for status notes that should live on the initiative itself

## Completion

1. Confirm all dependent work is done or intentionally deferred.
2. Run `mcp__orgx__orgx_act type=initiative`.
3. Attach proof with `mcp__orgx__orgx_act action=attach` for plans, docs, URLs, or deliverable artifacts.
4. If planning happened in OrgX, finish the plan loop with `mcp__orgx__orgx_plan attach_to=[...]` so the rationale is attached to the initiative context.
5. Mark complete with `mcp__orgx__orgx_act type=initiative action=complete`.

## Risk Handling

- Use `mcp__orgx__orgx_act type=initiative action=pause note="..."` for blockers or intentional holds.
- Use `mcp__orgx__orgx_act` or `mcp__orgx__orgx_act` when the priority problem is sequencing, not state.
- Use `mcp__orgx__orgx_act` instead of burying exceptions in the chat transcript.
