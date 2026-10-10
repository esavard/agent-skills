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

    def test_template_asset_passes_once_items_are_checked(self):
        template = (SCRIPT.parents[2] / "spec-interview/assets/spec-template.md").read_text()
        _, ok, unresolved = check_spec.find_unresolved(template)
        self.assertEqual(ok, 1)  # the (manual) example
        self.assertEqual(len(unresolved), 4)


if __name__ == "__main__":
    unittest.main()
