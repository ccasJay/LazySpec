"""Contract tests for LazySpec single-artifact architecture and lifecycle governance."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICIES = ROOT / "using-lazyspec" / "references"


class SingleArtifactArchitectureContractTests(unittest.TestCase):
    def test_v2_skills_exist_and_have_required_metadata(self):
        v2_skills = (
            "writing-spec",
            "executing-plan",
            "distill-feature",
            "maintain-memory",
        )
        try:
            import yaml

            parse_yaml = yaml.safe_load
        except ModuleNotFoundError:
            def parse_yaml(raw):
                return {
                    k.strip(): v.strip().strip('"')
                    for line in raw.splitlines()
                    if ":" in line
                    for k, v in [line.split(":", 1)]
                }

        for name in v2_skills:
            skill_file = ROOT / name / "SKILL.md"
            self.assertTrue(skill_file.exists(), f"missing skill {name}")
            text = skill_file.read_text()
            self.assertTrue(text.startswith("---\nname: " + name), f"invalid frontmatter in {name}")
            match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
            self.assertIsNotNone(match, f"frontmatter delimiters missing in {name}")
            data = parse_yaml(match.group(1))
            self.assertIsInstance(data, dict, f"frontmatter in {name} is not a dict")
            self.assertEqual(data.get("name"), name)
            self.assertTrue(data.get("description"), f"missing description in {name}")

    def test_spec_template_is_the_only_planning_artifact(self):
        template = (ROOT / "writing-spec" / "spec-template.md").read_text()
        for required in (
            "status: proposed",
            "delivered_at:",
            "supersedes: []",
            "superseded_by: null",
            "## 目标与范围",
            "## 用户故事",
            "## 验收标准",
            "| ID | 故事 | 类型 | 当 | 系统应 | 验证 |",
            "## 决策",
            "## 风险与否定性保证",
            "## 任务",
            "- [ ] //TODO 1.",
            "## 执行记录",
            "状态：未执行",
        ):
            with self.subTest(required=required):
                self.assertIn(required, template)
        self.assertNotIn("plan.md", template)

    def test_lifecycle_states_delegate_operations_to_their_owners(self):
        delivery_loop = (POLICIES / "delivery-loop.md").read_text()
        for state in ("proposed", "delivered", "archived", "superseded", "obsolete"):
            with self.subTest(state=state):
                self.assertIn(f"`{state}`", delivery_loop)
        self.assertIn("negative guardrail", delivery_loop.lower())
        governance = (ROOT / "maintain-memory/SKILL.md").read_text()
        self.assertIn("../../maintain-memory/SKILL.md", delivery_loop)
        self.assertIn("specs/retired/", governance)
        self.assertIn("specs/archived/", governance)
        self.assertIn("../../executing-plan/SKILL.md#merge-and-automatic-delivery-finalization", delivery_loop)

    def test_router_includes_negative_guardrail_inspection(self):
        router = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        self.assertIn("### Negative Guardrails Inspection", router)
        self.assertIn("specs/retired/", router)
        self.assertIn("preventing the agent from repeating past mistakes", router)


if __name__ == "__main__":
    unittest.main()
