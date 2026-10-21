"""Guard the v2 Plan task granularity contract and its behavioral slice rules."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / "writing-plan"
LINK = re.compile(r"\[(\d+\.\d+)\]\(\./spec\.md#spec-req-(\d+)-(\d+)\)")


class TaskGranularityContractTests(unittest.TestCase):
    def test_plan_groups_behavioral_slices_and_two_tier_verification(self):
        skill = (PLAN_DIR / "SKILL.md").read_text()
        prompt = (PLAN_DIR / "plan-prompt.md").read_text()

        self.assertIn("Behavioral Slices", skill)
        self.assertIn("[plan-prompt.md](plan-prompt.md)", skill)
        self.assertIn("independently deliverable behavior slice", prompt)
        self.assertIn("Behavioral Focus", prompt)
        self.assertIn("Two-tier verification", prompt)

        self.assertIn("basic per-TODO", skill)
        self.assertIn("spec.md", skill)
        self.assertIn("[plan-template.md](plan-template.md)", prompt)

    def test_plan_template_contains_behavioral_todos_and_feature_verification(self):
        template = (PLAN_DIR / "plan-template.md").read_text()
        self.assertIn("- [ ] //TODO 1. 完成", template)
        self.assertIn("实施目标：", template)
        self.assertIn("验证手段：", template)
        self.assertIn("## Feature Verification", template)
        self.assertIn("### Planned Checks", template)
        self.assertIn("### Latest Result", template)
        self.assertIn("状态：未执行", template)


if __name__ == "__main__":
    unittest.main()
