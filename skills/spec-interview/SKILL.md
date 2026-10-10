---
name: spec-interview
description: Turn a rough feature idea into a spec file under docs/specs/ (at the repository root) by interviewing the user one question at a time (grill-me / interview-me style), challenging vague terms, and only writing the spec once scope and acceptance criteria are unambiguous. Use when the user wants to plan a new feature, write a spec, or says things like "let's spec this out", "interview me about X", "grill me on this feature".
license: MIT
metadata:
  author: esavard
  version: "1.1"
---

# Spec Interview

Use this skill when the user has a rough idea, a bare-bones prompt, or a one-line feature request and wants a rigorous spec before any code gets written. The skill acts as an interviewer, not a stenographer: it interrogates the premise, forces precise definitions, and only writes the spec once the answers actually resolve the ambiguity.

Output lands in `<root>/docs/specs/` (see Step 0 for `<root>`). If prior specs exist there, match their format. If `docs/specs/` is empty (first spec ever in this repo), use [assets/spec-template.md](assets/spec-template.md) directly: it's tech-agnostic and doesn't require prior art to follow.

Write the spec file in English, regardless of the language the interview was conducted in, unless the user explicitly asks for a different language.

## Concept: Spec = Point-in-Time Record

- Files under `docs/specs/spec_NNN_<short_feature_description>.md` are point-in-time decision records and single-use execution contracts (ADR style).
- They are NOT living system documentation.
- The ONLY source of truth is the codebase itself: active code, unit/architecture tests, and `CONVENTIONS.md`.
- When preparing a new spec, reference past specs ONLY to understand historical intent or discover existing patterns, never as the absolute definition of current system state.

## Step 0: Resolve output location (never assume the current directory)

The agent is often launched from a subdirectory. Files must not land there silently.

1. Run `git rev-parse --show-toplevel` to get `<root>`. Compare it with the current working directory.
2. **cwd == `<root>`** and no existing `CONVENTIONS.md` / `docs/specs/` elsewhere: use `<root>`, no question needed.
3. **cwd != `<root>`**, or `<root>` cannot be resolved (not a git repo), or a `CONVENTIONS.md` / `docs/specs/` already exists in a subdirectory (monorepo): ask once, before the interview, e.g.
   > Repo root is `/abs/root`, you launched me from `/abs/root/backend`. Write `CONVENTIONS.md` and `docs/specs/` at: A) repo root `/abs/root` (Recommended), B) `/abs/root/backend`?
4. Use absolute paths from then on, and state the full target path when writing each file.

## Phase 0: Conventions precondition

Before interviewing about the feature itself, check `CONVENTIONS.md` at `<root>`:

- **Missing, empty, or clearly self-contradictory**: stop and invoke `spec-conventions-interview` first (or tell the user to run it). Do not draft engineering rules ad hoc inside the spec. Pass it the `<root>` already resolved in Step 0 so the user isn't asked twice. Resume this skill once `CONVENTIONS.md` exists.
- **Present and coherent**: read it, note its rules, continue directly to Phase 1. Do not re-litigate settled conventions during the feature interview.

## Phase 1: Interview

Ask **one question at a time** and wait for the answer before asking the next. Do not batch questions into a list.

### Question Format Rules
To keep context lean and speed up answers:
- Provide 2-3 concrete options or defaults whenever possible (e.g., "A) Option X (Recommended), B) Option Y").
- Allow the user to answer with single letters/words.

Ground questions in the codebase, not blind guesses:
- Search `docs/specs/`, and the relevant service directories for prior art before asking something the code already answers.
- If a related spec or WBS phase doc already exists, read it and ask the user to confirm/narrow it rather than starting from zero.

Challenge vague terms on sight. Words like "fast", "robust", "secure", "simple", "handle errors", "support X" must be pinned to something concrete (a number, a specific failure mode, a specific mechanism) before the interview moves on. Do not let a vague answer stand: ask a follow-up that forces the definition.

If the user answers "I don't know" or "whatever you think" on a scope/requirement/architecture question, never fall back to a vague "industry best practice" claim: that's an unverifiable hallucination risk. Propose a default in this priority order, and say out loud which tier it came from:
1. **Existing docs/specs or WBS docs in this repo**: reuse the pattern already used elsewhere (cite the file/section).
2. **Existing code/config in this repo**: an already-implemented pattern doing the equivalent job elsewhere in the codebase (cite the file).
3. **A verifiable industry-consensus default, not a vibe**: the pattern/library must be the de facto standard for that exact problem, and you must be able to name *why* it's consensus (dominant adoption for that job, official framework-recommended pattern) rather than just asserting "best practice." State the name + the one-line reason it counts as consensus.
4. **The base template** ([assets/spec-template.md](assets/spec-template.md)), if nothing else applies (first spec ever in this repo).
Whichever tier is used, ask for a yes/no confirmation rather than leaving it open.

Cover these areas, skipping anything the codebase or an existing doc already answers unambiguously (state the inferred answer instead of asking):

1. **Title & Goal**: one sentence, outcome-focused. What does "done" look like from the user's/system's perspective?
2. **Scope**: concrete bullet list of what's included. Push back on anything phrased as a vague capability ("support offline mode") until it's a testable behavior.
3. **Out of scope**: what looks related but is explicitly excluded. If the user doesn't volunteer this, ask directly: silence here is how scope creep happens later.
4. **Context**: relevant modules/paths (confirm via a quick repo look, don't just take the user's word), tech stack, existing architecture notes, related specs/prior decisions, spec nature (`Domain logic` / `UI/presentation only` / `Mixed`).
5. **Architecture**: enough detail to draw a Mermaid diagram (components/adapters involved, data flow direction, what's a Command vs an Event if `CONVENTIONS.md` says this project uses DDD).
5b. **Architecture-test ordering**: if `CONVENTIONS.md` section 2 applies (spec nature `Domain logic` or `Mixed`), ask whether architecture tests can genuinely be written before any production code exists for this spec, or whether a package/module must exist first for the tool (e.g. `import-linter`) to discover it. Offer: A) full test-first is feasible, B) minimal empty skeleton needed first, then tests, then implementation (per `CONVENTIONS.md` section 2's exception clause), C) not applicable, skip. Record the answer verbatim in the spec's `## 7. Engineering Rules` section so the ordering exception is decided upfront, not discovered and retrofitted mid-implementation.
6. **Requirements & acceptance criteria**: each requirement must map to an observable, checkable acceptance criterion. Reject requirements phrased only as intentions ("should be reliable"): ask for the specific condition that would make it false.
7. **Deliverables**: concrete artifacts (files, modules, test suites) expected at the end.
8. **Implementation phasing**: only ask if the feature is large enough to warrant it (multiple independent milestones); skip for small specs.
9. **Definition of Done**: beyond the standard checklist in `CONVENTIONS.md`, anything feature-specific that must hold (e.g. "legacy code untouched unless justified").
10. **Manual items**: identify acceptance/DoD items an agent cannot perform (manual testing against a real database, production deploy, stakeholder sign-off, device testing). Propose the list; the user confirms. These get the `(manual)` tag.

Stop asking once every section above has an unambiguous answer: do not pad the interview with questions that don't change the resulting spec.

## Phase 2: Synthesize

Only after the ambiguity is resolved:

1. Determine the next spec number by listing `<root>/docs/specs/spec_*.md` and incrementing the highest `NNN`.
2. Write `<root>/docs/specs/spec_NNN_<short_feature_description>.md` using this section structure (full skeleton in [assets/spec-template.md](assets/spec-template.md)):
   - Implementing agent protocol block, right under the title (copy verbatim from the template)
   - `## 1. Spec` (Title, Goal, Scope, Out of scope)
   - `## 2. Context` (Project, relevant modules/paths, tech stack, existing architecture notes, related specs, spec nature)
   - `## 3. Architecture Diagram (Mermaid)`
   - `## 4. Requirements` (with acceptance criteria as checkboxes)
   - `## 5. Deliverables`
   - `## 6. Implementation Plan` (only if phasing was discussed; omit section otherwise)
   - `## 7. Engineering Rules`: do **not** repeat the boilerplate; write: "Follow `CONVENTIONS.md`." plus only the deltas/exceptions specific to this spec, if any.
   - `## 8. Definition of Done` (standard checklist derived from `CONVENTIONS.md` + feature-specific items from the interview)
3. Checkbox rules for the spec body:
   - Every requirement, DoD item, and plan step that an agent must complete is a `- [ ]` checkbox.
   - Items from interview area 10 start with `(manual)`: `- [ ] (manual) Smoke test checkout against Stripe test mode`. The implementing agent may leave them unchecked without explanation; every other unchecked item will need a `NOT DONE: <reason>`.
   - Keep the protocol reminder line at the top of `## 4` and `## 8` (from the template).
   - If prior specs in this repo use an older protocol wording, use the template's wording anyway: the protocol block is the contract `spec-implement` enforces.
4. Present the full file to the user for review before considering the spec final. Call out any answer you inferred rather than asked, so the user can correct it.

For spec_001 in any repo, use the template verbatim; once it exists, later specs match its established format (protocol block excepted, see step 3).

## Hand-off / Session Boundary

When the spec is complete and agreed upon:
1. Explicitly instruct the user to **STOP and open a FRESH session** before writing any code. Be insistent: explain that keeping execution separate from the interview context prevents hallucinations and saves tokens.
2. Provide a ready-to-copy kick-off message for the new session, formatted like this:

> "Use the spec-implement skill. Implement `docs/specs/spec_NNN_<short_feature_description>.md` (repo root: `<root>`). Follow `CONVENTIONS.md` for architecture rules. Check each item in the spec the moment it is verified; any item left unchecked needs `NOT DONE: <reason>` unless tagged `(manual)`. Do not report completion until `check_spec.py` passes. Begin with Phase 1 tasks."

The kick-off message restates the checkbox protocol on purpose: it must work even if the implementing agent does not have `spec-implement` installed.

## Guardrails

- Never write the spec file before the interview has resolved scope, out-of-scope, and acceptance criteria: a spec drafted from a vague answer is worse than no spec.
- Never write a file relative to the current directory without the Step 0 resolution.
- Do not duplicate `CONVENTIONS.md` content into the spec; reference it.
- Do not invent file paths, modules, or tech stack choices without confirming them against the actual repo state.
- Do not silently expand scope beyond what the user described: if you notice an adjacent need, flag it as a question or as explicitly out-of-scope, don't fold it in.
- If `CONVENTIONS.md` is missing partway through and the user wants to skip establishing it, note explicitly in the spec's Engineering Rules section that conventions were not yet formalized: don't silently invent them.
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
