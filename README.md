# agent-skills

[![skills.sh](https://skills.sh/b/esavard/agent-skills)](https://skills.sh/esavard/agent-skills)

Personal collection of Agent Skills for spec-driven development, managed with the
[skills.sh](https://skills.sh) CLI ([vercel-labs/skills](https://github.com/vercel-labs/skills)).

## Skills

| Skill | Description |
| --- | --- |
| [spec-interview](skills/spec-interview/SKILL.md) | Turns a rough feature idea into a spec file under `docs/specs/` by interviewing you one question at a time. |
| [spec-conventions-interview](skills/spec-conventions-interview/SKILL.md) | Establishes or repairs the repo's `CONVENTIONS.md` through an interview. Prerequisite of `spec-interview`. |

## Install

```bash
# all skills
npx skills add esavard/agent-skills

# list the skills without installing
npx skills add esavard/agent-skills --list

# a single skill
npx skills add esavard/agent-skills --skill spec-interview
```

## Usage

Once installed, the agent loads a skill when your request matches its description, for example
"let's spec this out" or "interview me about this feature". You can also name the skill explicitly.

## Structure

Each skill lives in its own directory under `skills/` and contains a `SKILL.md` with YAML
frontmatter (`name`, `description`):

```
skills/
  <skill-name>/
    SKILL.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Validate changes with:

```bash
node scripts/validate-skills.mjs
```

## License

MIT, see [LICENSE](LICENSE).
