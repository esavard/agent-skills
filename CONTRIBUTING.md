# Contributing

Thanks for helping. This repository holds Agent Skills: instructions an AI coding agent loads on
demand. A skill is prose that changes agent behavior, so review focuses on what the agent actually
does with it.

## Ways to contribute

- **Report a problem**: the skill did not trigger, triggered when it should not, or the agent ignored
  or misread an instruction. Open an issue with the agent and model you used and what happened.
- **Improve an existing skill**: clearer wording, a missing guardrail, a fixed contradiction.
- **Propose a new skill**: open an issue first so scope can be agreed before you write it.

## What belongs here

A skill fits this repository when it:

- supports spec-driven development (interviewing, specifying, planning, executing or reviewing specs);
- works in any repository: no dependency on a private tool, a company-specific layout or one tech
  stack, unless it detects the stack itself;
- works across agents: it does not rely on tools only one agent provides.

## Adding or changing a skill

1. Fork and create a branch.
2. Create `skills/<skill-name>/SKILL.md`. The directory name is the skill name: lowercase letters,
   digits and hyphens.

   ```markdown
   ---
   name: my-skill
   description: What it does, and when to use it, including phrases a user would say. Single line.
   license: MIT
   ---

   # My Skill

   Instructions for the agent.
   ```

3. Add a row for it in the "Skills" table of `README.md`, add it to `skills` in
   `.claude-plugin/plugin.json`, and give it an `agents/openai.yaml` (a test checks both).
4. Validate:

   ```bash
   node scripts/validate-skills.mjs
   npx skills add . --list        # the CLI must discover your skill
   python3 -m unittest discover -s tests   # manifest sync and helper scripts
   ```

5. Try it for real: install it into a scratch project (`npx skills add /path/to/your/clone`) and run
   at least one full session with it. Say in the pull request which agent and model you used and
   what you observed.
6. Open a pull request. Keep it to one skill or one concern.

## Writing guidelines

- **The description decides triggering.** State what the skill does and when to use it, with the
  words users really type. Keep it on one line, under 1024 characters.
- **Write instructions, not documentation.** Address the agent, use imperatives, give the reason
  behind a rule when it is not obvious.
- **Be concrete.** Prefer a checkable rule, an example or a template over an aspiration.
- **Stay lean.** Keep `SKILL.md` under 500 lines. Move long reference material to
  `references/<topic>.md` and link it from `SKILL.md` so it is read only when needed.
- **Stay generic.** No hard-coded paths, organisation names, secrets or personal data.
- **Scripts** go in `skills/<skill-name>/scripts/`, must not need network access or credentials
  unless the skill says so up front, and must be explained in `SKILL.md`.

## Pull request review

CI runs `scripts/validate-skills.mjs`, the unit tests and the plugin manifest validation on every pull request. A maintainer then checks that the skill
is in scope, reads clearly, and does not instruct an agent to do anything destructive or surprising
(deleting files, pushing, sending data to external services) without the user asking for it.

## License

By contributing, you agree that your contribution is licensed under the [MIT License](LICENSE).
