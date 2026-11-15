#!/usr/bin/env node
// Validates every skill under skills/ and checks the README table lists them.
// No dependencies: run with `node scripts/validate-skills.mjs`.
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const skillsDir = join(root, 'skills');
const NAME_RE = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const MAX_NAME = 64;
const MAX_DESCRIPTION = 1024;
const MAX_LINES = 500;

const errors = [];
const fail = (skill, msg) => errors.push(`skills/${skill}: ${msg}`);

/** Parses the top-level `key: value` scalars of a YAML frontmatter block. */
function parseFrontmatter(text) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(text);
  if (!match) return null;
  const fields = {};
  for (const line of match[1].split(/\r?\n/)) {
    const kv = /^([A-Za-z][\w-]*):\s*(.*)$/.exec(line);
    if (!kv) continue;
    let value = kv[2].trim();
    if (/^(['"]).*\1$/.test(value)) value = value.slice(1, -1);
    fields[kv[1]] = value;
  }
  return fields;
}

const dirs = existsSync(skillsDir)
  ? readdirSync(skillsDir, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name).sort()
  : [];
if (dirs.length === 0) errors.push('skills/: no skill directory found');

const readme = existsSync(join(root, 'README.md')) ? readFileSync(join(root, 'README.md'), 'utf8') : '';

for (const dir of dirs) {
  const file = join(skillsDir, dir, 'SKILL.md');
  if (!existsSync(file)) {
    fail(dir, 'missing SKILL.md');
    continue;
  }
  const text = readFileSync(file, 'utf8');
  const fm = parseFrontmatter(text);
  if (!fm) {
    fail(dir, 'SKILL.md must start with a YAML frontmatter block (--- ... ---)');
    continue;
  }
  if (!fm.name) fail(dir, 'frontmatter `name` is required');
  else {
    if (fm.name !== dir) fail(dir, `frontmatter name "${fm.name}" must equal the directory name`);
    if (!NAME_RE.test(fm.name)) fail(dir, 'name must be lowercase letters, digits and single hyphens');
    if (fm.name.length > MAX_NAME) fail(dir, `name longer than ${MAX_NAME} characters`);
  }
  if (!fm.description) fail(dir, 'frontmatter `description` is required (single line)');
  else if (fm.description.length > MAX_DESCRIPTION) {
    fail(dir, `description is ${fm.description.length} characters (max ${MAX_DESCRIPTION})`);
  }
  const lines = text.split('\n').length;
  if (lines > MAX_LINES) fail(dir, `SKILL.md is ${lines} lines (max ${MAX_LINES}); move detail to references/`);
  if (!readme.includes(`skills/${dir}/`)) fail(dir, 'not listed in the README "Skills" table');
}

if (errors.length) {
  console.error(errors.map((e) => `ERROR ${e}`).join('\n'));
  process.exit(1);
}
console.log(`OK: ${dirs.length} skill(s) valid: ${dirs.join(', ')}`);
