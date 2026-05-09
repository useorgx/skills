# AGENTS.md

Guidelines for Codex and other agents working in `useorgx/skills`.

## Project

This repo contains OrgX skill definitions and protocol guidance for MCP-capable agents.

## Setup

For Codex cloud, use:

```bash
bash .codex/setup-cloud.sh
```

Maintenance script for cached environments:

```bash
bash .codex/maintenance-cloud.sh
```

## Verification

```bash
python3 scripts/check_skill_tool_drift.py
```

Run the drift checker before claiming skill changes are ready. It is the minimum proof that skill files still reference valid OrgX MCP tool names and required workflow gates.
