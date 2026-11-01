"""Guard the single-artifact task granularity and compressed shape contracts."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = ROOT / "writing-spec"


class TaskGranularityContractTests(unittest.TestCase):
    def test_spec_groups_behavioral_slices_and_two_tier_verification(self):
        skill = (SPEC_DIR / "SKILL.md").read_text()
        prompt = (SPEC_DIR / "spec-prompt.md").read_text()

        self.assertIn("## Task Design", skill)
        self.assertIn("independently deliverable behavior slices", skill)
        self.assertIn("[spec-prompt.md](spec-prompt.md)", skill)
        self.assertIn("independently deliverable behavior slice", prompt)
        self.assertIn("Tasks", prompt)
        self.assertIn("Reserve full test suites and end-to-end execution for the final verification pass", prompt)

    def test_spec_template_contains_tasks_and_execution_record(self):
        template = (SPEC_DIR / "spec-template.md").read_text()
        self.assertIn("- [ ] //TODO 1.", template)
        self.assertIn("→ R1.1；检查：", template)
        self.assertIn("## 任务", template)
        self.assertIn("## 执行记录", template)
        self.assertIn("状态：未执行", template)
        self.assertNotIn("## Feature Verification", template)
        self.assertNotIn("### Planned Checks", template)

    def test_compact_verification_keeps_individual_coverage(self):
        prompt = (SPEC_DIR / "spec-prompt.md").read_text()
        delivery = (ROOT / "using-lazyspec/references/delivery-loop.md").read_text()
        self.assertIn("A shared command may cover several criteria", prompt)
        self.assertIn("their individual coverage remains explicit", delivery)
        self.assertIn("distinct scenarios needed for exceptions or failure paths", delivery)
        self.assertIn("Never rewrite completed task descriptions", delivery)

    def test_writing_plan_skill_is_gone(self):
        self.assertFalse((ROOT / "writing-plan" / "SKILL.md").exists())
        self.assertFalse((ROOT / "writing-plan" / "plan-template.md").exists())
        self.assertFalse((ROOT / "writing-plan" / "plan-prompt.md").exists())


if __name__ == "__main__":
    unittest.main()
