"""Contract tests for LazySpec v2.0 binary architecture and lifecycle governance."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICIES = ROOT / "using-lazyspec" / "references"


class V2BinaryArchitectureContractTests(unittest.TestCase):
    def test_v2_skills_exist_and_have_required_metadata(self):
        v2_skills = (
            "writing-spec",
            "writing-plan",
            "executing-plan",
            "distill-feature",
            "distill-learning",
            "maintain-memory",
        )
        import yaml

        for name in v2_skills:
            skill_file = ROOT / name / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"missing skill {name}")
            text = skill_file.read_text()
            self.assertTrue(text.startswith("---\nname: " + name), f"invalid frontmatter in {name}")
            match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
            self.assertIsNotNone(match, f"frontmatter delimiters missing in {name}")
            data = yaml.safe_load(match.group(1))
            self.assertIsInstance(data, dict, f"frontmatter in {name} is not a dict")
            self.assertEqual(data.get("name"), name)
            self.assertTrue(data.get("description"), f"missing description in {name}")

    def test_spec_template_contains_frontmatter_and_alternatives(self):
        template = (ROOT / "writing-spec" / "spec-template.md").read_text()
        self.assertIn("status: proposed", template)
        self.assertIn("supersedes: []", template)
        self.assertIn("superseded_by: null", template)
        self.assertIn("## 目标与范围", template)
        self.assertIn("## 需求与验收标准", template)
        self.assertIn("## 架构与核心决策", template)
        self.assertIn("## 曾考虑的备选方案", template)
        self.assertIn("## 风险与否定性保证", template)

    def test_plan_template_contains_behavioral_todos_and_feature_verification(self):
        template = (ROOT / "writing-plan" / "plan-template.md").read_text()
        self.assertIn("- [ ] //TODO", template)
        self.assertIn("## Feature Verification", template)
        self.assertIn("### Planned Checks", template)
        self.assertIn("### Latest Result", template)

    def test_delivery_loop_defines_four_lifecycle_states_and_guardrails(self):
        delivery_loop = (POLICIES / "delivery-loop.md").read_text()
        for state in ("proposed", "delivered", "archived", "superseded", "obsolete"):
            with self.subTest(state=state):
                self.assertIn(f"`{state}`", delivery_loop)
        self.assertIn("negative guardrail", delivery_loop.lower())
        self.assertIn("specs/retired/", delivery_loop)
        self.assertIn("specs/archived/", delivery_loop)
        self.assertIn("Automatic Delivery Finalization", delivery_loop)

    def test_router_includes_negative_guardrail_inspection(self):
        router = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        self.assertIn("### Negative Guardrails Inspection", router)
        self.assertIn("specs/retired/", router)
        self.assertIn("preventing the agent from repeating past mistakes", router)


if __name__ == "__main__":
    unittest.main()

