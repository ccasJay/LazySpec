import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "distill-spec-memory"


class MemorySkillContractTests(unittest.TestCase):
    def test_skill_structure_and_frontmatter(self):
        skill_path = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        self.assertTrue((SKILL_ROOT / "agents" / "openai.yaml").is_file())
        self.assertTrue(
            (SKILL_ROOT / "references" / "memory-format.md").is_file()
        )

        text = skill_path.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        keys = {
            line.split(":", 1)[0]
            for line in match.group(1).splitlines()
            if ":" in line
        }
        self.assertEqual({"name", "description"}, keys)
        self.assertIn("name: distill-spec-memory", match.group(1))
        self.assertNotIn("TODO", text)

    def test_openai_interface_matches_skill(self):
        text = (SKILL_ROOT / "agents" / "openai.yaml").read_text()
        self.assertIn('display_name: "Distill Spec Memory"', text)
        self.assertIn(
            'short_description: "Distill completed feature specs into project memory"',
            text,
        )
        self.assertIn("$distill-spec-memory", text)
        self.assertNotIn("icon_", text)
        self.assertNotIn("brand_color", text)

    def test_plugin_and_router_register_memory_skill(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("./distill-spec-memory", manifest["skills"])
        self.assertEqual(len(manifest["skills"]), len(set(manifest["skills"])))

        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        self.assertIn("`lazyspec:distill-spec-memory`", routing)
        self.assertIn("`../distill-spec-memory/SKILL.md`", routing)
        self.assertIn("only when the user explicitly asks", routing)
        self.assertIn("Do not infer a distillation request", routing)

    def test_memory_format_contract(self):
        text = (SKILL_ROOT / "references" / "memory-format.md").read_text()
        for required in (
            "project-memory/index.md",
            "project-memory/features/<feature-name>.md",
            "feature: <feature-name>",
            "status: active",
            "source_spec: specs/<feature-name>/",
            "distilled_at: YYYY-MM-DD",
            "tags: [<tag>]",
            "supersedes: []",
            "superseded_by: []",
            'status_reason: ""',
            "## Capability",
            "## Durable Decisions",
            "## Contracts and Invariants",
            "## Lessons",
            "## Reuse Triggers",
            "## Sources",
            "| Memory | Summary | Tags | Status | Source Spec |",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

        for status in ("active", "needs-review", "superseded", "obsolete"):
            self.assertIn(f"`{status}`", text)

        self.assertIn("project-root-relative", text)
        self.assertIn("no `topics/`, `sessions/`", text)
        self.assertIn("JSON index", text)
        self.assertIn("never copy complete sections", text)


if __name__ == "__main__":
    unittest.main()
