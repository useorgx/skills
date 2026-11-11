# AGENTS.md

Guidelines for Codex and other agents working in `useorgx/skills`.

## Project

This repo contains OrgX skill definitions and protocol guidance for MCP-capable agents.

## Keep routine work moving

Carry the user's authorized task through implementation and relevant verification.
Existing user authorization persists: do not ask again for routine edits, fixes,
PR updates, or an authorized merge. Ask only for a material scope change or an
actual missing permission, and continue independent work while it is resolved.

OrgX lifecycle calls, receipt schemas, scoring rubrics, and domain checklists
apply to work tracked in OrgX or to the requested deliverable. They do not add
approval, planning-session, score, or tool-availability prerequisites to ordinary
repository work. Use the checks relevant to the change; preserve repository CI,
access controls, data integrity, and truthful reporting of results.

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

Run the drift checker before claiming skill changes are ready. It is the minimum proof that skill files still reference valid OrgX MCP tool names and supported API contracts.
