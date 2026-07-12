# Distribution and Drift Control

The authoring source for this skill is the `orgx-design/` directory in
[useorgx/skills](https://github.com/useorgx/skills). Installed copies are
generated caches, not independent sources.

## Supported copies

The same pack can be consumed by:

- hosted installers such as `npx add-skill useorgx/skills/orgx-design`;
- global Claude skills;
- global Codex skills;
- global Cursor skills;
- repo-local `.claude/skills/orgx-design`;
- repo-local `.codex/skills/orgx-design`;
- repo-local `.cursor/orgx/skills/orgx-design`.

Companion plugins may pin a generated copy. Updating the hosted source does not
prove a plugin bundle has updated; verify the installed content independently.

## Change protocol

1. Edit the hosted authoring source.
2. Run `python3 scripts/check_skill_tool_drift.py`.
3. Run `node orgx-design/scripts/validate.mjs`.
4. Commit, review, and merge the hosted change.
5. Sync generated local copies from the merged source with
   `node orgx-design/scripts/sync-local.mjs --apply`.
6. Run the same command with `--check` and require zero drift.
7. Update companion plugin packages through their own release pipeline when
   they embed skill files.

Do not edit generated clients first and hope to reconstruct the canonical pack
later.
