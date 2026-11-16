#!/usr/bin/env python3
"""Validate every skill under skills/ and check the README table lists them.

Usage: python3 scripts/validate_skills.py [repo-root]

Standard library only. Exit codes: 0 = valid, 1 = errors found.
"""

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_LINES = 500
FRONTMATTER = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
KEY_VALUE = re.compile(r"^([A-Za-z][\w-]*):\s*(.*)$")


def parse_frontmatter(text):
    """Return the top-level `key: value` scalars of a YAML frontmatter block, or None."""
    match = FRONTMATTER.match(text)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        kv = KEY_VALUE.match(line)
        if not kv:
            continue
        value = kv.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            value = value[1:-1]
        fields[kv.group(1)] = value
    return fields


def validate(root):
    """Return a list of error strings for the repository at `root`."""
    root = Path(root)
    skills_dir = root / "skills"
    errors = []
    dirs = sorted(d.name for d in skills_dir.iterdir() if d.is_dir()) if skills_dir.is_dir() else []
    if not dirs:
        errors.append("skills/: no skill directory found")
    readme_path = root / "README.md"
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""

    for name in dirs:
        def fail(msg, name=name):
            errors.append(f"skills/{name}: {msg}")

        skill_md = skills_dir / name / "SKILL.md"
        if not skill_md.is_file():
            fail("missing SKILL.md")
            continue
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm is None:
            fail("SKILL.md must start with a YAML frontmatter block (--- ... ---)")
            continue
        if not fm.get("name"):
            fail("frontmatter `name` is required")
        else:
            if fm["name"] != name:
                fail(f'frontmatter name "{fm["name"]}" must equal the directory name')
            if not NAME_RE.match(fm["name"]):
                fail("name must be lowercase letters, digits and single hyphens")
            if len(fm["name"]) > MAX_NAME:
                fail(f"name longer than {MAX_NAME} characters")
        if not fm.get("description"):
            fail("frontmatter `description` is required (single line)")
        elif len(fm["description"]) > MAX_DESCRIPTION:
            fail(f"description is {len(fm['description'])} characters (max {MAX_DESCRIPTION})")
        lines = len(text.split("\n"))
        if lines > MAX_LINES:
            fail(f"SKILL.md is {lines} lines (max {MAX_LINES}); move detail to references/")
        if f"skills/{name}/" not in readme:
            fail('not listed in the README "Skills" table')
    return errors


def main(argv):
    root = Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        print("\n".join(f"ERROR {e}" for e in errors), file=sys.stderr)
        return 1
    names = sorted(d.name for d in (root / "skills").iterdir() if d.is_dir())
    print(f"OK: {len(names)} skill(s) valid: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
