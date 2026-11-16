"""Tests for skills/spec-implement/scripts/check_spec.py (stdlib unittest)."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/spec-implement/scripts/check_spec.py"
spec = importlib.util.spec_from_file_location("check_spec", SCRIPT)
check_spec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_spec)


class FindUnresolvedTest(unittest.TestCase):
    def test_checked_items_pass(self):
        self.assertEqual(check_spec.find_unresolved("- [x] a\n* [X] b\n1. [x] c\n"), (3, 0, []))

    def test_manual_and_not_done_are_explained(self):
        text = "- [ ] (manual) smoke test on real DB\n- [ ] add index. NOT DONE: needs DBA approval\n"
        self.assertEqual(check_spec.find_unresolved(text), (0, 2, []))

    def test_unexplained_unchecked_item_is_reported_with_line(self):
        _, _, unresolved = check_spec.find_unresolved("# T\n- [x] a\n  - [ ] nested item\n")
        self.assertEqual(unresolved, [(3, "nested item")])

    def test_empty_or_trivial_reason_is_rejected(self):
        _, _, unresolved = check_spec.find_unresolved("- [ ] a NOT DONE:\n- [ ] b NOT DONE: x\n")
        self.assertEqual(len(unresolved), 2)

    def test_fenced_code_and_blockquotes_are_ignored(self):
        text = "```markdown\n- [ ] template item\n```\n> check `- [ ]` to `- [x]`\n"
        self.assertEqual(check_spec.find_unresolved(text), (0, 0, []))


class MainTest(unittest.TestCase):
    def run_on(self, content):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(content)
        try:
            return check_spec.main(["check_spec.py", f.name])
        finally:
            Path(f.name).unlink()

    def test_exit_codes(self):
        self.assertEqual(self.run_on("- [x] done\n"), 0)
        self.assertEqual(self.run_on("- [ ] forgotten\n"), 1)
        self.assertEqual(check_spec.main(["check_spec.py"]), 2)
        self.assertEqual(check_spec.main(["check_spec.py", "/nonexistent.md"]), 2)

    def test_base_template_in_spec_interview_is_checkable(self):
        skill = (SCRIPT.parents[2] / "spec-interview/SKILL.md").read_text()
        start = skill.index("```markdown\n# spec_001_") + len("```markdown\n")
        end = skill.index("\n```\n\nUse this skeleton")
        template = skill[start:end].replace("\\`", "`")
        self.assertIn("NOT DONE:", template)  # the protocol line is part of the template
        # The mermaid fence is escaped in the skill; once unescaped it is skipped like any code block.
        _, manual, unresolved = check_spec.find_unresolved(template)
        self.assertEqual(manual, 1)  # the (manual) example item
        self.assertEqual(len(unresolved), 4)  # 2 requirements + 2 DoD items, still to do

if __name__ == "__main__":
    unittest.main()
