---
name: spec-implement
description: Implement a spec file from docs/specs/ (produced by spec-interview) while keeping its checkboxes accurate. Enforces checking each item the moment it is verified, requires a written reason for every item left unchecked, and gates completion on scripts/check_spec.py. Use when the user says "implement spec_NNN", "start implementation of docs/specs/...", or pastes the kick-off message produced by spec-interview.
license: MIT
compatibility: Requires git (repository root detection) and Python 3 standard library (scripts/check_spec.py).
metadata:
  author: esavard
  version: "1.0"
---

# Spec Implement

Execute one spec under `docs/specs/` as a contract. The spec's checkboxes are the progress record: the user reads them, not your chat summary. A completed task with an unchecked box counts as not done.

## Step 0: Locate repository root and spec

1. Run `git rev-parse --show-toplevel`. All paths below (`docs/specs/`, `CONVENTIONS.md`) are relative to that root, never to the current working directory.
2. If the command fails (not a git repo), or the spec is not found under `<root>/docs/specs/`, stop and ask the user for the path. Do not guess.
3. Read the spec in full, then `<root>/CONVENTIONS.md` if it exists.

## Checkbox protocol (mandatory)

Applies to every `- [ ]` in the spec (Requirements, Definition of Done, Implementation Plan, anywhere).

| Situation | Action |
|---|---|
| Item done and verified (test passes, file exists, command succeeds) | Edit `- [ ]` to `- [x]` immediately, in the same turn as the work, before starting the next item |
| Item tagged `(manual)` (spec author marked it as needing a human: manual testing on a real database, production deploy, stakeholder approval) | Leave unchecked, no explanation needed. Check it only if you actually performed it |
| Item not done for any other reason (blocked, out of time, failed, deferred, judged unnecessary) | Leave unchecked and append on the same line: `NOT DONE: <concrete reason>` |
| Item partially done | Leave unchecked; `NOT DONE: <what remains>` |

Rules:
- Never batch checkbox updates at the end. One verified item, one edit.
- Never check an item you have not verified. "Should work" is not verified.
- A reason must be concrete: `NOT DONE: no Stripe test key in env, webhook test cannot run` is valid; `NOT DONE: later` is not.
- Do not delete, reword, or reorder items to make them pass. If an item is wrong, leave it unchecked with `NOT DONE: item conflicts with <X>, needs user decision`.

## Completion gate (mandatory)

Before saying the work is done, finished, complete, or ending the session:

1. Run `python3 <this-skill-dir>/scripts/check_spec.py <root>/docs/specs/spec_NNN_<name>.md`.
2. Exit code 1: fix each listed line (check it, or add `NOT DONE: <reason>`), then rerun. Repeat until exit code 0.
3. If Python is unavailable, run the same check by hand: list every `- [ ]` line outside code blocks; each must contain `(manual)` or `NOT DONE:`.
4. End your final message with a short report:
   - script output summary line (`N/M checked, ...`)
   - one bullet per `NOT DONE` item with its reason
   - one bullet per `(manual)` item, so the user knows what is left for them

Claiming completion without this gate passing is a protocol violation, even if all code is written.

## Scope discipline

- Implement only what the spec lists. Adjacent needs go in the final report as suggestions, not in the code.
- If the spec is ambiguous on something that changes the result, ask; do not resolve silently.
- Follow `CONVENTIONS.md`; the spec's `## 7. Engineering Rules` lists the only allowed deltas.
