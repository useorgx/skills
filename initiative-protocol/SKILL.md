---
name: initiative-protocol
description: |
  Initiative lifecycle management for OrgX. Handles creation, decomposition
  into workstreams/streams, launch, monitoring, and completion.
  Use when planning or managing an OrgX initiative.
---

# Initiative Protocol

## Creating an Initiative

1. Query existing: `mcp__orgx__query_org_memory("initiative [topic]")`
2. Create: `mcp__orgx__create_entity type=initiative` with title, summary, target_date
3. Break into 3-5 workstreams by domain
4. For each workstream, create a stream: `mcp__orgx__create_entity type=stream`
   - Set agent_domain, depends_on (DAG), auto_continue
5. Launch: `mcp__orgx__launch_entity type=initiative`

## Monitoring

- Check health: `mcp__orgx__get_initiative_pulse`
- Stream state: `mcp__orgx__get_initiative_stream_state`
- Key metrics: overall_progress, min_confidence, blocked_count, next_completions

## Completing

- All streams must be completed first
- Synthesize outputs from each domain
- Verify readiness: `mcp__orgx__verify_entity_completion type=initiative`
- Complete: `mcp__orgx__complete_entity type=initiative`

## Risk Management

- Pause: `mcp__orgx__pause_entity type=initiative` with reason
- Re-launch after resolving blockers
