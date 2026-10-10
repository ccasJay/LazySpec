"""Static Skill contracts for writing-spec and decision probing."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec/SKILL.md").read_text()
SKILL = (ROOT / "writing-spec/SKILL.md").read_text()
PROMPT = (ROOT / "writing-spec/spec-prompt.md").read_text()
POLICY = (ROOT / "using-lazyspec/references/approval-policy.md").read_text()


class WritingSpecContractTests(unittest.TestCase):
    def test_manifest_registers_pure_v2_nine_skills(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        expected = {
            "using-lazyspec", "writing-spec", "writing-plan", "executing-plan",
            "distill-feature", "distill-learning", "maintain-memory",
            "fast", "orchestrating-specs",
        }
        self.assertEqual(expected, {Path(p).name for p in manifest["skills"]})
        self.assertEqual(len(expected), len(manifest["skills"]))

        self.assertFalse((ROOT / "writing-requirement/SKILL.md").exists())
        self.assertFalse((ROOT / "writing-design/SKILL.md").exists())
        self.assertFalse((ROOT / "writing-task/SKILL.md").exists())
        self.assertFalse((ROOT / "executing-task/SKILL.md").exists())
        self.assertFalse((ROOT / "distill-spec-memory/SKILL.md").exists())

    def test_creation_and_revision_route_directly_to_spec(self):
        self.assertIn("route directly to `writing-spec`", ROUTER)
        self.assertIn("Phase 1: Spec Creation / Revision", ROUTER)

    def test_decision_probing_grill_me_principles(self):
        self.assertIn("Structured Probing (/grill-me Style)", SKILL)
        self.assertIn("Identify Branches of Decision Tree", SKILL)
        self.assertIn("Ask One Focused Decision Question at a Time", SKILL)
        self.assertIn("Alternatives Considered", SKILL)
        self.assertIn("EARS", SKILL)
        self.assertIn("negative guarantees", SKILL)

    def test_ears_criteria_anchors(self):
        template = (ROOT / "writing-spec/spec-template.md").read_text()
        self.assertIn('spec-req-', template)
        self.assertIn('## 曾考虑的备选方案', template)
        self.assertIn('## 风险与否定性保证', template)


if __name__ == "__main__":
    unittest.main()
