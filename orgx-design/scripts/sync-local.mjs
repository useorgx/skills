#!/usr/bin/env node

import { createHash } from "node:crypto";
import { cp, mkdir, readdir, readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { dirname, join, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const source = dirname(dirname(fileURLToPath(import.meta.url)));
const args = process.argv.slice(2);
const apply = args.includes("--apply");
const check = args.includes("--check") || !apply;
const targets = [];

for (let index = 0; index < args.length; index += 1) {
  if (args[index] === "--target" && args[index + 1]) {
    targets.push(resolve(args[index + 1]));
    index += 1;
  }
}

if (targets.length === 0) {
  targets.push(
    join(homedir(), ".claude/skills/orgx-design"),
    join(homedir(), ".codex/skills/orgx-design"),
    join(homedir(), ".cursor/skills/orgx-design"),
  );
}

async function filesUnder(root, current = root) {
  const entries = await readdir(current, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.name === ".DS_Store") continue;
    const absolute = join(current, entry.name);
    if (entry.isDirectory()) files.push(...await filesUnder(root, absolute));
    else if (entry.isFile()) files.push(relative(root, absolute));
  }
  return files.sort();
}

function digest(value) {
  return createHash("sha256").update(value).digest("hex");
}

const sourceFiles = await filesUnder(source);
let drift = false;

for (const target of targets) {
  if (apply) {
    await mkdir(target, { recursive: true });
    for (const file of sourceFiles) {
      const destination = join(target, file);
      await mkdir(dirname(destination), { recursive: true });
      await cp(join(source, file), destination);
    }
  }

  const differences = [];
  for (const file of sourceFiles) {
    try {
      const [left, right] = await Promise.all([
        readFile(join(source, file)),
        readFile(join(target, file)),
      ]);
      if (digest(left) !== digest(right)) differences.push(file);
    } catch {
      differences.push(file);
    }
  }

  if (differences.length) {
    drift = true;
    console.error(`${target}: drift in ${differences.join(", ")}`);
  } else {
    console.log(`${target}: ${sourceFiles.length} canonical files match`);
  }
}

if (check && drift) process.exit(1);
