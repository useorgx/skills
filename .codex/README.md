# Codex Cloud Environment

Use these repo-local scripts when configuring the Codex cloud environment for `useorgx/skills`.

## Setup script

```bash
bash .codex/setup-cloud.sh
```

## Maintenance script

```bash
bash .codex/maintenance-cloud.sh
```

## Environment notes

- Python 3 is enough for the repo-level drift checker.
- No OrgX API secrets are required for static skill drift checks.
- Keep internet access limited to the setup phase unless a task explicitly needs external services.

## Verification commands

```bash
python3 scripts/check_skill_tool_drift.py
```
