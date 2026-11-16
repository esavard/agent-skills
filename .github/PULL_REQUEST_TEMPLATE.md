## What and why

<!-- Which skill, what changes in the agent's behavior, and the problem it solves. Link the issue. -->

## How it was tested

<!-- Agent + model, the prompt you used, and what the agent did before / after. -->

## Checklist

- [ ] `python3 scripts/validate_skills.py` passes
- [ ] `python3 -m unittest discover -s tests` passes
- [ ] New skill: listed in the README "Skills" table and in `skills` of `.claude-plugin/plugin.json`, with an `agents/openai.yaml`
- [ ] Plugin manifest or install docs changed: `claude plugin validate . --strict` passes
- [ ] Changed a skill's behavior: the README workflow section still matches
- [ ] Ran at least one real session with the skill installed
- [ ] No private paths, organisation names, secrets or personal data
- [ ] One skill or one concern in this pull request
