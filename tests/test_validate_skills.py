"""Tests for scripts/validate_skills.py (stdlib unittest)."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_skills", ROOT / "scripts/validate_skills.py")
validate_skills = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate_skills)


def make_repo(tmp, name="my-skill", front=None, readme=None):
    root = Path(tmp)
    (root / "skills" / name).mkdir(parents=True)
    front = front if front is not None else f"---\nname: {name}\ndescription: Does a thing.\n---\n# Body\n"
    (root / "skills" / name / "SKILL.md").write_text(front)
    (root / "README.md").write_text(readme if readme is not None else f"[x](skills/{name}/SKILL.md)")
    return root


class ValidateSkillsTest(unittest.TestCase):
    def errors(self, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            return validate_skills.validate(make_repo(tmp, **kwargs))

    def test_this_repository_is_valid(self):
        self.assertEqual(validate_skills.validate(ROOT), [])

    def test_valid_skill_has_no_errors(self):
        self.assertEqual(self.errors(), [])

    def test_name_must_match_directory(self):
        errs = self.errors(front="---\nname: other\ndescription: d\n---\n")
        self.assertTrue(any("must equal the directory name" in e for e in errs))

    def test_missing_frontmatter_and_description(self):
        self.assertTrue(any("frontmatter block" in e for e in self.errors(front="# no frontmatter\n")))
        errs = self.errors(front="---\nname: my-skill\n---\n")
        self.assertTrue(any("`description` is required" in e for e in errs))

    def test_description_too_long(self):
        errs = self.errors(front="---\nname: my-skill\ndescription: " + "x" * 1025 + "\n---\n")
        self.assertTrue(any("max 1024" in e for e in errs))

    def test_skill_must_be_listed_in_readme(self):
        errs = self.errors(readme="nothing here")
        self.assertTrue(any("README" in e for e in errs))

    def test_quoted_values_are_unquoted(self):
        fm = validate_skills.parse_frontmatter('---\nname: "a-b"\ndescription: \'d\'\n---\n')
        self.assertEqual(fm, {"name": "a-b", "description": "d"})


if __name__ == "__main__":
    unittest.main()
