---
name: spec-conventions-interview
description: Interview the user one question at a time to establish or repair the repo's CONVENTIONS.md (architecture style, SOLID/Clean Code stance, DDD usage, testing rules, dependency/reuse policy, process constraints). Use when CONVENTIONS.md is missing, empty, or its content is inconsistent/confusing, especially as a prerequisite step before spec-interview.
license: MIT
---

# Spec Conventions Interview

Use this skill to produce or repair `CONVENTIONS.md` at the repository root. `CONVENTIONS.md` holds the engineering rules that apply to every feature spec in `docs/specs/` (hexagonal/clean architecture stance, SOLID, DDD usage, testing rules, reuse/dependency policy, process constraints) so those rules are written once and referenced by every spec instead of copy-pasted into each one.

This skill is normally invoked by `spec-interview` when it detects `CONVENTIONS.md` is missing or confusing, but it can also be run directly.

Write `CONVENTIONS.md` in English, regardless of the language the interview was conducted in, unless the user explicitly asks for a different language.

## When to run

- `CONVENTIONS.md` does not exist at the repo root.
- `CONVENTIONS.md` exists but is empty, a stub, or contradicts itself (e.g. mixes two architecture styles, has TODOs instead of decisions, or is stale relative to the current codebase).
- The user explicitly asks to review or rewrite conventions.

If `CONVENTIONS.md` exists and reads as coherent and current, do not re-run the interview — report that it looks fine and stop, unless the user insists.

## Interview rules

- Ask **one question at a time**. Wait for the answer before asking the next.
- Never accept a vague term without pinning it down. If the user answers with a fuzzy word ("clean", "solid", "fast", "well-tested"), ask them to define it concretely for this repo (an example, a threshold, a rule you could lint for) before moving on.
- Ground questions in what the codebase already does. Before asking "which architecture style do you use", grep for obvious signals (folder names like `domain/`, `adapters/`, `application/`; existing test structure; presence of an architecture-test tool). Present what you found and ask the user to confirm, correct, or override it — don't ask blind.
- Keep the interview short. Skip a question entirely if the codebase already gives an unambiguous answer; state the inferred answer instead of asking.
- If the user answers "I don't know" or "whatever you think", never fall back to a vague "industry best practice" claim — that's an unverifiable hallucination risk. Propose a default in this priority order, and say out loud which tier it came from:
  1. **Existing docs/specs in this repo** — reuse rules already duplicated across `docs/specs/spec_*` (cite the file(s) and section).
  2. **Existing repo config that already encodes the rule** — a lint config, CI check, or tool section (e.g. `pyproject.toml [tool.pytest]`, `.eslintrc`, a Makefile target) that makes the default checkable right now. Cite the file.
  3. **A verifiable industry-consensus default, not a vibe** — the tool/pattern must be the de facto standard for that language/problem, and you must be able to name *why* it's consensus (widely-cited style guide, the dominant tool by adoption for that exact job, official framework-recommended pattern) rather than just asserting "best practice." Example: for Java/Kotlin architecture enforcement, ArchUnit qualifies — it's the dominant, most-referenced tool specifically for that job, verifiable by its adoption/citation footprint, not a guess. State the tool/pattern name + the one-line reason it counts as consensus, and still mark it "default, please confirm."
  4. **The Base Template below**, if nothing else applies (first spec ever, no config yet).
  Whichever tier is used, ask for a yes/no confirmation rather than leaving it open.

## Topics to cover

Ask about each of these, skipping any the codebase already answers unambiguously:

1. **Architecture style** — hexagonal/clean architecture, layered, or something else? Where do domain/application/infrastructure boundaries live (folder names)?
2. **Architecture enforcement** — should layer boundaries be enforced by automated architecture tests? Detect language first (see stack signals below), then propose matching tool. Required always, or only above some size/complexity threshold?

   | Language | Typical tool |
   |---|---|
   | Python | `import-linter`, `pytest-archon` |
   | Java / Kotlin | ArchUnit |
   | Go | `go-arch-lint`, `depguard` |
   | JS/TS | `dependency-cruiser`, `eslint-plugin-boundaries` |
   | C# | `NetArchTest`, ArchUnitNET |
   | Rust | workspace crate boundaries (compiler-enforced) + `cargo-deny` |

   Don't assume Python — grep for manifest files (`pyproject.toml`, `pom.xml`/`build.gradle`, `go.mod`, `package.json`, `*.csproj`, `Cargo.toml`) to detect stack before naming a tool.

   Ordering is fixed; do not ask the user whether architecture tests come as a skeleton or as a complete suite, and do not write a "tests before any production code" rule with an exception clause. When architecture tests are required, record this rule in `CONVENTIONS.md` §2 as-is:
   - Each spec starts with a skeleton architecture-test suite covering only the boundaries the spec already fixes, plus the minimal empty packages/modules the tool needs to discover them.
   - The agent adds a rule each time a new element or boundary is confirmed during implementation.
   - The spec is done only when the suite covers every boundary the feature introduced.

   If an existing `CONVENTIONS.md` states a different ordering (e.g. full test-first with an exception clause), point it out and propose replacing it with the rule above.
3. **DDD usage** — does this codebase use ubiquitous language / commands / aggregates / domain events, or is that overkill for its current scope? If yes, where is the ubiquitous language documented today?
4. **SOLID / Clean Code stance** — any repo-specific exceptions to the standard rules (e.g. a deliberate god-object, a naming convention that looks like an abbreviation but is idiomatic here)?
5. **Testing rules** — required test types (unit/integration/e2e), where integration tests live vs unit tests, whether Given/When/Then or another convention is expected, coverage expectations if any.
6. **Reuse & dependency policy** — process for adding a new external dependency (needs flagging? needs approval?), where shared/common code lives once duplicated twice.
7. **Process constraints** — anything the agent must never do unprompted in this repo (e.g. touching legacy MCU code, refactoring unrelated files, silently resolving ambiguity instead of asking).

## Output

Write `CONVENTIONS.md` at the repository root with one short section per topic above, each stated as concrete, checkable rules (not prose aspirations). If this repo already has specs under `docs/specs/` with an engineering-rules section, model the rigor after those — reuse whatever rules are already duplicated across them instead of inventing new ones. If no prior specs exist, use the Base Template below as the starting skeleton.

End the file with a short "Last reviewed" line (date + what prompted the review) so future confusion-detection has a signal to check freshness against.

After writing, show the user a summary of what changed (new file vs amended sections) and ask them to review before treating it as final.

## Base Template (greenfield repo, no prior specs/CONVENTIONS.md)

When there's nothing to ground questions in yet (empty repo, or first spec ever), don't ask all 7 topics blind. Use this skeleton to drive the interview instead — present it filled with your best inference from any scaffolding that exists (framework starter, folder stubs, README), then ask the user to confirm/override per section rather than open-ended:

```markdown
# CONVENTIONS.md

## 1. Architecture Style
Style: <hexagonal | layered | vertical-slice | other>
Boundaries: <folder-per-layer names, e.g. domain/ application/ infrastructure/>

## 2. Architecture Enforcement
Tool: <none yet | tool name from stack table>
Threshold: <always | above N modules/LOC>
Ordering: skeleton suite first (boundaries fixed by the spec), extended as boundaries are confirmed during implementation, complete for the feature at Definition of Done

## 3. DDD Usage
Used: <yes/no>
Ubiquitous language doc: <path, or "not yet — add when first aggregate is named">

## 4. SOLID / Clean Code Stance
Exceptions: <none | list>

## 5. Testing Rules
Required types: <unit | integration | e2e>
Location convention: <e.g. tests/ mirrors src/, or colocated *_test files>
Style: <Given/When/Then | Arrange/Act/Assert | none enforced>
Coverage gate: <none | threshold>

## 6. Reuse & Dependency Policy
New external dependency: <needs no approval | needs flagging in PR | needs approval from X>
Shared code threshold: <extract to shared/common on Nth duplication>

## 7. Process Constraints
<agent must never do X unprompted — list or "none yet">

Last reviewed: <date> — <what prompted this>
```

This is a starting point, not a fill-in-the-blanks form — still challenge vague answers and don't let the user rubber-stamp defaults they haven't actually thought about.
