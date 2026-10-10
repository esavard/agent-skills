"""Keep the plugin manifest in sync with skills/ (stdlib unittest)."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ManifestTest(unittest.TestCase):
    def test_plugin_lists_every_skill_exactly_once(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        listed = sorted(Path(s).name for s in manifest["skills"])
        on_disk = sorted(p.parent.name for p in ROOT.glob("skills/*/SKILL.md"))
        self.assertEqual(listed, on_disk)

    def test_every_skill_has_codex_metadata(self):
        for skill_md in ROOT.glob("skills/*/SKILL.md"):
            self.assertTrue((skill_md.parent / "agents/openai.yaml").is_file(), skill_md.parent.name)

    def test_marketplace_points_at_plugin(self):
        plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual([p["name"] for p in market["plugins"]], [plugin["name"]])


if __name__ == "__main__":
    unittest.main()
