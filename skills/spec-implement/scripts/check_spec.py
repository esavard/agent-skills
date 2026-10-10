#!/usr/bin/env python3
"""Fail if a spec still has unchecked items without an explanation.

Usage: python3 check_spec.py <path/to/spec.md>

Every Markdown checkbox outside fenced code blocks must be either:
  - checked:             - [x] Item
  - tagged manual:       - [ ] (manual) Item an agent cannot perform
  - explained not done:  - [ ] Item. NOT DONE: <reason>

Exit codes: 0 = all items resolved, 1 = unexplained unchecked items, 2 = usage error.
Standard library only, so it runs in any repo regardless of its stack.
"""

import re
import sys
from pathlib import Path

CHECKBOX = re.compile(r"^\s*(?:[-*+]|\d+[.)])\s+\[([ xX])\]\s*(.*)$")
FENCE = re.compile(r"^\s*(```|~~~)")
MANUAL_TAG = re.compile(r"\(manual\)", re.IGNORECASE)
NOT_DONE = re.compile(r"NOT DONE:\s*(\S.{2,})")


def find_unresolved(text):
    """Return (checked, unchecked_ok, unresolved) where unresolved is a list of (line_no, text)."""
    checked = 0
    unchecked_ok = 0
    unresolved = []
    in_fence = False
    for line_no, line in enumerate(text.splitlines(), start=1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = CHECKBOX.match(line)
        if not match:
            continue
        state, body = match.groups()
        if state in "xX":
            checked += 1
        elif MANUAL_TAG.search(body) or NOT_DONE.search(body):
            unchecked_ok += 1
        else:
            unresolved.append((line_no, body.strip()))
    return checked, unchecked_ok, unresolved


def main(argv):
    if len(argv) != 2:
        print("usage: check_spec.py <path/to/spec.md>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    if not path.is_file():
        print(f"error: spec not found: {path}", file=sys.stderr)
        return 2

    checked, unchecked_ok, unresolved = find_unresolved(path.read_text(encoding="utf-8"))
    total = checked + unchecked_ok + len(unresolved)
    print(f"{path}: {checked}/{total} checked, {unchecked_ok} manual/explained, {len(unresolved)} unresolved")

    if not unresolved:
        return 0
    print("\nUnchecked items with no explanation:")
    for line_no, body in unresolved:
        print(f"  line {line_no}: {body}")
    print(
        "\nFor each item: check it ([x]) if done and verified, otherwise append"
        " 'NOT DONE: <reason>' on the same line."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
