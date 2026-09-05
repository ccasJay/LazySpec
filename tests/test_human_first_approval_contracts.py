import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
REQUIREMENT_SKILL = (ROOT / "writing-requirement" / "SKILL.md").read_text()
REQUIREMENT_PROMPT = (
    ROOT / "writing-requirement" / "requirement-prompt.md"
).read_text()
REQUIREMENT_TEMPLATE = (
    ROOT / "writing-requirement" / "requirement-templete.md"
).read_text()
DESIGN_SKILL = (ROOT / "writing-design" / "SKILL.md").read_text()
DESIGN_PROMPT = (ROOT / "writing-design" / "design-prompt.md").read_text()
DESIGN_TEMPLATE = (ROOT / "writing-design" / "design-templete.md").read_text()


def approval_payload(skill_text):
    payloads = re.findall(r"```json\n(.*?)\n\s*```", skill_text, re.DOTALL)
    if len(payloads) != 1:
        raise AssertionError(f"expected one approval payload, got {len(payloads)}")
    return json.loads(payloads[0])["questions"][0]


class HumanFirstApprovalContractTests(unittest.TestCase):
    def test_router_defines_summary_authority_and_materiality(self):
        for required in (
            "## Human-First Approval Contract",
            "user-facing approval contract",
            "Agent-facing elaboration",
            "bounded Human-First `审批摘要` projection",
            "public interfaces or data changes",
            "security or privacy",
            "When uncertain, classify a change as material",
            "missing material item",
            "summary/body conflict blocks approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, ROUTER)

    def test_router_defines_adaptive_review_and_revision_behavior(self):
        for required in (
            "cognitive complexity instead of enforcing a fixed item or character count",
            "complete one-screen review",
            "recommend splitting the Spec",
            "explicitly chooses to keep one Spec",
            "A material change invalidates the prior approval",
            "non-material body-only refinement",
            "additions, changes, removals, and risk changes",
            "material Requirements/Design changes and Tasks plan revisions invalidate affected approvals",
        ):
            with self.subTest(required=required):
                self.assertIn(required, ROUTER)

    def test_legacy_specs_migrate_only_when_revised(self):
        self.assertIn("Do not bulk-migrate existing Specs", ROUTER)
        self.assertIn("next created or revised", ROUTER)
        self.assertIn("approved legacy Requirements", ROUTER)
        self.assertIn("legacy Requirements document", REQUIREMENT_SKILL)
        self.assertIn("legacy Design document", DESIGN_SKILL)

    def test_requirements_template_starts_with_human_review_summary(self):
        for heading in (
            "## 审批摘要",
            "### 目标",
            "### 范围",
            "### 核心行为",
            "### 风险与待确认",
        ):
            self.assertIn(heading, REQUIREMENT_TEMPLATE)
        self.assertLess(
            REQUIREMENT_TEMPLATE.index("## 审批摘要"),
            REQUIREMENT_TEMPLATE.index("## 引言"),
        )
        self.assertLess(
            REQUIREMENT_TEMPLATE.index("## 引言"),
            REQUIREMENT_TEMPLATE.index('<a id="req-1-1"></a>'),
        )
        self.assertIn(
            "Keep HTML anchors and traceability syntax out of `审批摘要`",
            REQUIREMENT_TEMPLATE,
        )

    def test_requirements_prompt_enforces_complete_material_coverage(self):
        for required in (
            "Human-First `审批摘要`",
            "user-facing approval contract",
            "every materially distinct acceptance outcome",
            "one unambiguous summary group",
            "Keep HTML anchors and traceability syntax out of the summary",
            "Resolve material open questions before approval",
            "conversation delta",
        ):
            with self.subTest(required=required):
                self.assertIn(required, REQUIREMENT_PROMPT)

    def test_design_template_starts_with_decision_summary(self):
        for required in (
            "## 审批摘要",
            "### 方案",
            "### 关键决策",
            "| 决策 | 选择与理由 | 影响 |",
            "### 风险与待确认",
        ):
            with self.subTest(required=required):
                self.assertIn(required, DESIGN_TEMPLATE)
        self.assertLess(
            DESIGN_TEMPLATE.index("## 审批摘要"),
            DESIGN_TEMPLATE.index("- Overview"),
        )
        self.assertIn("reuse each summary decision title", DESIGN_TEMPLATE)

    def test_design_prompt_separates_material_and_internal_details(self):
        for required in (
            "public behavior or interfaces",
            "compatibility or migration",
            "external or irreversible effects",
            "Omit internal file layout, helpers, test organization",
            "exact short title",
            "summary/body conflict blocks approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, DESIGN_PROMPT)
        self.assertIn(
            "Excluding the Human-First `审批摘要`", DESIGN_SKILL
        )

    def test_approval_questions_target_the_summary(self):
        requirement = approval_payload(REQUIREMENT_SKILL)
        design = approval_payload(DESIGN_SKILL)
        self.assertIn("审批摘要", requirement["question"])
        self.assertIn("目标、范围、核心行为与风险", requirement["question"])
        self.assertIn("审批摘要", design["question"])
        self.assertIn("设计方案、关键决策及风险", design["question"])
        for question in (requirement, design):
            self.assertEqual(
                ["Approve", "Request changes"],
                [option["label"] for option in question["options"]],
            )

    def test_tasks_keep_the_existing_approval_object(self):
        task_skill = (ROOT / "writing-task" / "SKILL.md").read_text()
        task_template = (ROOT / "writing-task" / "task-templete.md").read_text()
        self.assertNotIn("审批摘要", task_skill)
        self.assertNotIn("审批摘要", task_template)
        self.assertIn(
            "Tasks keeps the complete task document as its approval object", ROUTER
        )


if __name__ == "__main__":
    unittest.main()
