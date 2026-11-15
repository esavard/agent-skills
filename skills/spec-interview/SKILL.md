---
name: spec-interview
description: Turn a rough feature idea into a spec file under docs/specs/ by interviewing the user one question at a time (grill-me / interview-me style), challenging vague terms, and only writing the spec once scope and acceptance criteria are unambiguous. Use when the user wants to plan a new feature, write a spec, or says things like "let's spec this out", "interview me about X", "grill me on this feature".
license: MIT
---

# Spec Interview

Use this skill when the user has a rough idea, a bare-bones prompt, or a one-line feature request and wants a rigorous spec before any code gets written. The skill acts as an interviewer, not a stenographer: it interrogates the premise, forces precise definitions, and only writes the spec once the answers actually resolve the ambiguity.

Output lands in `docs/specs/` **at the project root — never relative to the current working directory**. Every `docs/specs/` and `CONVENTIONS.md` path in this skill is anchored to the project root. Resolve the root once, before anything else: run `git rev-parse --show-toplevel`; if that fails (not a git repo), walk up from the current directory to the nearest ancestor containing `CONVENTIONS.md` or `docs/specs/`; if still unresolved, ask the user. If the session was started in a subdirectory, do not create a `docs/specs/` there, even if that subdirectory looks like a self-contained package or service.

If prior specs exist there, match their format. If `docs/specs/` is empty (first spec ever in this repo), use the section structure in Phase 2 directly — it's tech-agnostic and doesn't require prior art to follow.

Write the spec file in English, regardless of the language the interview was conducted in, unless the user explicitly asks for a different language.

When the spec is agreed upon, tell the user they MUST start a new session. Be insistent about it.

## Concept: Spec = Point-in-Time Record (ADR style)

The source code is ALWAYS the source of truth. A spec NEVER is. This rule overrides anything a past spec says.

- A file under `docs/specs/spec_NNN_<short_feature_description>.md` works like an ADR: a snapshot of one development effort at a given moment in the life of the repository, and a single-use execution contract for that effort.
- It is NOT living system documentation. Once the feature is built, the spec stays as a record of what was decided and why.
- Never edit a past spec to make it follow the code. The only edits allowed after a spec is agreed are the implementing agent ticking its checkboxes during that spec's own implementation. If the code later diverges, the code is right; a new decision gets a new spec.
- Current system state comes from the codebase only: active code, unit/architecture tests, and `CONVENTIONS.md`.
- When preparing a new spec, read past specs ONLY for historical intent. Any fact taken from a past spec (path, module, contract, pattern, behavior) MUST be verified against the current code before it is used in a question, a proposed default, or the new spec. If spec and code disagree, use the code and tell the user about the divergence.

## Phase 0 — Conventions precondition

Before interviewing about the feature itself, check `CONVENTIONS.md` at the repo root:

- **Missing, empty, or clearly self-contradictory** → stop and invoke `spec-conventions-interview` first (or tell the user to run it) — do not draft engineering rules ad hoc inside the spec. Resume this skill once `CONVENTIONS.md` exists.
- **Present and coherent** → read it, note its rules, continue directly to Phase 1. Do not re-litigate settled conventions during the feature interview.

## Phase 1 — Interview

Ask **one question at a time** and wait for the answer before asking the next. Do not batch questions into a list.

### Question Format Rules
To keep context lean and speed up answers:
- Provide 2–3 concrete options or defaults whenever possible (e.g., "A) Option X (Recommended), B) Option Y").
- Allow the user to answer with single letters/words.

Ground questions in the codebase, not blind guesses:
- Search the relevant service directories first, then `docs/specs/`, for prior art before asking something the code already answers.
- If a related spec or WBS phase doc already exists, read it for intent, check what it describes against the current code, and ask the user to confirm/narrow it rather than starting from zero. Never present a past spec's content as the current state of the system without that check.

Challenge vague terms on sight. Words like "fast", "robust", "secure", "simple", "handle errors", "support X" must be pinned to something concrete (a number, a specific failure mode, a specific mechanism) before the interview moves on. Do not let a vague answer stand — ask a follow-up that forces the definition.

If the user answers "I don't know" or "whatever you think" on a scope/requirement/architecture question, never fall back to a vague "industry best practice" claim — that's an unverifiable hallucination risk. Propose a default in this priority order, and say out loud which tier it came from:
1. **Existing code/config in this repo** — an already-implemented pattern doing the equivalent job elsewhere in the codebase (cite the file).
2. **Existing docs/specs or WBS docs in this repo** — a pattern decided in a past spec, only after confirming the code still follows it (cite the spec section and the code file).
3. **A verifiable industry-consensus default, not a vibe** — the pattern/library must be the de facto standard for that exact problem, and you must be able to name *why* it's consensus (dominant adoption for that job, official framework-recommended pattern) rather than just asserting "best practice." State the name + the one-line reason it counts as consensus.
4. **The Base Template below**, if nothing else applies (first spec ever in this repo).
Whichever tier is used, ask for a yes/no confirmation rather than leaving it open.

Cover these areas, skipping anything the codebase or an existing doc already answers unambiguously (state the inferred answer instead of asking):

1. **Title & Goal** — one sentence, outcome-focused. What does "done" look like from the user's/system's perspective?
2. **Scope** — concrete bullet list of what's included. Push back on anything phrased as a vague capability ("support offline mode") until it's a testable behavior.
3. **Out of scope** — what looks related but is explicitly excluded. If the user doesn't volunteer this, ask directly — silence here is how scope creep happens later.
4. **Context** — relevant modules/paths (confirm via a quick repo look, don't just take the user's word), tech stack, existing architecture notes, related specs/prior decisions, spec nature (`Domain logic` / `UI/presentation only` / `Mixed`).
5. **Architecture** — enough detail to draw a Mermaid diagram (components/adapters involved, data flow direction, what's a Command vs an Event if `CONVENTIONS.md` says this project uses DDD).
5b. **Architecture tests: skeleton first, then grow** — if `CONVENTIONS.md` requires architecture tests and the spec nature is `Domain logic` or `Mixed`, do NOT ask the user to choose between a skeleton and a complete architecture-test suite, and do not offer it as an A/B option. The approach is fixed. Tell the user, as a statement they can object to, that implementation will proceed this way:
   1. Start with a skeleton architecture-test suite covering only the boundaries the spec already fixes (the layers/modules named in the Architecture section), creating the minimal empty packages/modules the tool (e.g. ArchUnit, `import-linter`) needs to discover them.
   2. Extend the suite during implementation, adding a rule each time a new element or boundary is confirmed by the code being written.
   3. Finish with a suite that covers every boundary the feature introduced; this is a Definition of Done item.

   Record these three steps in the spec's `## 7. Engineering Rules` section and add the matching checkbox to `## 8. Definition of Done`. Ask a question here only if the spec introduces a boundary whose direction of dependency is genuinely undecided; that is an Architecture question (item 5), not a test-ordering one. Skip this item entirely for `UI/presentation only` specs or when `CONVENTIONS.md` does not require architecture tests. If `CONVENTIONS.md` states a different ordering (e.g. full test-first with an exception clause), still use the skeleton-then-grow approach, tell the user about the mismatch, and suggest running `spec-conventions-interview` to update that section.
6. **Requirements & acceptance criteria** — each requirement must map to an observable, checkable acceptance criterion. Reject requirements phrased only as intentions ("should be reliable") — ask for the specific condition that would make it false.
7. **Deliverables** — concrete artifacts (files, modules, test suites) expected at the end.
8. **Implementation phasing** — only ask if the feature is large enough to warrant it (multiple independent milestones); skip for small specs.
9. **Definition of Done** — beyond the standard checklist in `CONVENTIONS.md`, anything feature-specific that must hold (e.g. "legacy code untouched unless justified").

Stop asking once every section above has an unambiguous answer — do not pad the interview with questions that don't change the resulting spec.

## Phase 2 — Synthesize

Only after the ambiguity is resolved:

1. Determine the next spec number by listing `<project-root>/docs/specs/spec_*.md` and incrementing the highest `NNN`.
2. Write `<project-root>/docs/specs/spec_NNN_<short_feature_description>.md` (absolute path from the resolved project root, not the current directory; create `docs/specs/` at the root if it doesn't exist) using this section structure:
   - `## 1. Spec` (Title, Goal, Scope, Out of scope)
   - `## 2. Context` (Project, relevant modules/paths, tech stack, existing architecture notes, related specs, spec nature)
   - `## 3. Architecture Diagram (Mermaid)`
   - `## 4. Requirements` (with acceptance criteria as checkboxes)
   - `## 5. Deliverables`
   - `## 6. Implementation Plan` (only if phasing was discussed; omit section otherwise)
   - `## 7. Engineering Rules` — do **not** repeat the boilerplate; write: "Follow `CONVENTIONS.md`." plus only the deltas/exceptions specific to this spec, if any.
   - `## 8. Definition of Done` (standard checklist derived from `CONVENTIONS.md` + feature-specific items from the interview)
3. Directly under the spec's title, insert this line verbatim: `> Point-in-time record (ADR style): snapshot of one development effort, written <YYYY-MM-DD>. Source code is always the source of truth, never this spec. Implementing agent: if this spec disagrees with the current code, stop and ask. Do not update this file to follow later code changes.` Replace `<YYYY-MM-DD>` with the date the spec is written.
4. At top of `## 4. Requirements` and `## 8. Definition of Done`, insert this instruction line verbatim, addressed to implementing agent: `> Implementing agent: check `[ ]` → `[x]` in THIS file the moment each item completes. Do not batch checkbox updates to end of session — re-prompting agent to backfill them is wasted turn.`
5. Present the full file to the user for review before considering the spec final. Call out any answer you inferred rather than asked, so the user can correct it.

### Base Template (first spec in a repo, no prior art to match)

```markdown
# spec_001_<short_feature_description>

> Point-in-time record (ADR style): snapshot of one development effort, written <YYYY-MM-DD>. Source code is always the source of truth, never this spec. Implementing agent: if this spec disagrees with the current code, stop and ask. Do not update this file to follow later code changes.

## 1. Spec
**Title:** <one line>
**Goal:** <outcome-focused, one sentence>
**Scope:** <bullet list, each a testable behavior>
**Out of scope:** <bullet list>

## 2. Context
**Project:** <name>
**Relevant modules/paths:** <list, confirmed against repo>
**Tech stack:** <language, framework, key libs>
**Existing architecture notes:** <link to CONVENTIONS.md, or "none yet">
**Related specs:** <none — first spec>
**Spec nature:** <Domain logic | UI/presentation only | Mixed>

## 3. Architecture Diagram (Mermaid)
\`\`\`mermaid
flowchart LR
  A[Component] --> B[Component]
\`\`\`

## 4. Requirements
> Implementing agent: check `[ ]` → `[x]` in THIS file the moment each item completes. Do not batch checkbox updates to end of session — re-prompting agent to backfill them is wasted turn.
- [ ] Requirement 1 — Acceptance: <observable, checkable condition>
- [ ] Requirement 2 — Acceptance: <observable, checkable condition>

## 5. Deliverables
- <file/module/test suite>

## 6. Implementation Plan
<omit this section if the feature has no independent milestones>

## 7. Engineering Rules
Follow `CONVENTIONS.md`. <deltas/exceptions specific to this spec, if any>

## 8. Definition of Done
> Implementing agent: check `[ ]` → `[x]` in THIS file the moment each item completes. Do not batch checkbox updates to end of session — re-prompting agent to backfill them is wasted turn.
- [ ] <standard checklist item from CONVENTIONS.md>
- [ ] <feature-specific item from interview>
```

Use this skeleton verbatim for spec_001 in any repo; once it exists, later specs should match its established format instead of re-deriving from this template.

## Hand-off / Session Boundary

When the spec is complete and agreed upon:
1. Explicitly instruct the user to **STOP and open a FRESH session** before writing any code. Be insistent—explain that keeping execution separate from the interview context prevents hallucinations and saves tokens.
2. Provide a ready-to-copy kick-off message for the new session, formatted like this:

> "Implement `docs/specs/spec_NNN_<short_feature_description>.md`."

Keep the kick-off message to that one line. The rules the implementing agent needs (follow `CONVENTIONS.md`, source code is the source of truth, tick checkboxes as items complete) are already written in the spec file itself; do not repeat them in the message.

## Guardrails

- Never write the spec file before the interview has resolved scope, out-of-scope, and acceptance criteria — a spec drafted from a vague answer is worse than no spec.
- Never treat a past spec as the current state of the system, and never edit a past spec to match the code. Source code is always the source of truth; verify against it.
- Do not duplicate `CONVENTIONS.md` content into the spec; reference it.
- Do not invent file paths, modules, or tech stack choices without confirming them against the actual repo state.
- Do not silently expand scope beyond what the user described — if you notice an adjacent need, flag it as a question or as explicitly out-of-scope, don't fold it in.
- If `CONVENTIONS.md` is missing partway through and the user wants to skip establishing it, note explicitly in the spec's Engineering Rules section that conventions were not yet formalized — don't silently invent them.
- Enforce telegraphic style throughout the spec document. Eliminate fluff words while preserving 100% of technical identifiers, file paths, and contract bounds.

## Writing Style Directive (Ultra-Lean / Telegraphic)

Write specs using compressed, high-density technical prose (telegraphic style). Maximize information per token.

### Execution Rules
1. **Drop fluff & articles:** Omit "the", "a", "an", "in order to", "is responsible for", "should be configured to".
2. **Imperative fragments:** Start bullets with verbs (`Emit...`, `Enforce...`, `Reject...`).
3. **No conversational prose:** Do not write introductory or concluding summary paragraphs inside sections.
4. **Tables & Bullets over paragraphs:** Store data flows, model schemas, and status mappings in markdown tables or tight bullet lists.
5. **Zero loss of technical specs:** Never drop file paths, model names, status codes, or explicit constraints to hit brevity targets.

### Style Examples

**Bloated Prose (Do NOT use):**
> The system should be designed to handle disconnect events properly. When a TCP session drops due to a network peer closing the connection or a server shutdown occurs, the gateway will construct and publish a `DeviceDisconnected` event down to the asynchronous event sink so that downstream consumers are aware.

**Telegraphic Prose (REQUIRED):**
> Emits `DeviceDisconnected` to async event sink on session term (`peer_closed`, `connection_error`, `server_shutdown`).

## Recommended invocation

```text
Use spec-interview.
I want to add <rough feature idea>. Interview me and produce a spec under docs/specs/.
```
