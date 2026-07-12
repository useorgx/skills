#!/usr/bin/env node

import { readFile, stat } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
const skillPath = join(skillDir, "SKILL.md");
const text = await readFile(skillPath, "utf8");
const errors = [];

for (const phrase of [
  'version: "3.0.0"',
  "existing / new / missing",
  "goal → plan → work → decision → artifact → proof → next action",
  "desktop 1440px",
  "tablet 768px",
  "phone 375px",
  "44px",
  "AQ ≥ 0.85",
]) {
  if (!text.includes(phrase)) errors.push(`SKILL.md is missing: ${phrase}`);
}

const references = [...text.matchAll(/\]\((references\/[^)]+\.md)\)/g)]
  .map((match) => match[1]);

for (const relative of new Set(references)) {
  try {
    const file = await stat(join(skillDir, relative));
    if (!file.isFile()) errors.push(`${relative} is not a file`);
  } catch {
    errors.push(`missing referenced file: ${relative}`);
  }
}

for (const required of [
  "references/philosophy.md",
  "references/surface-audit.md",
  "references/app-shell.md",
  "references/implementation-map.md",
  "references/verification.md",
  "references/scorecard.md",
  "references/widget-sdk.md",
  "references/distribution.md",
]) {
  if (!references.includes(required)) errors.push(`SKILL.md does not route to ${required}`);
}

if (errors.length) {
  console.error(errors.map((error) => `- ${error}`).join("\n"));
  process.exit(1);
}

console.log(`orgx-design v3 valid: ${new Set(references).size} references resolved`);
