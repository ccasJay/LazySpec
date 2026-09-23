import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
POLICIES = ROOT / "using-lazyspec" / "references"
APPROVAL_POLICY = (POLICIES / "approval-policy.md").read_text()
DOC_POLICY = (POLICIES / "doc-policy.md").read_text()
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


class HumanFirstApprovalContractTests(unittest.TestCase):
    def test_policy_defines_summary_authority_and_materiality(self):
        for required in (
            "## Human-First approval summary",
            "user-facing approval contract",
            "Agent-facing elaboration",
            "public interfaces or data changes",
            "security or privacy",
            "When uncertain, classify a change as material",
            "missing material item",
            "summary/body conflict blocks approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)

    def test_policy_defines_summary_size_and_revision_behavior(self):
        for required in (
            "cognitive complexity instead of enforcing a fixed item or character count",
            "complete one-screen review",
            "recommend splitting the Spec",
            "explicitly chooses to keep one Spec",
            "A material change invalidates the prior approval",
            "non-material body-only refinement",
            "additions, changes, removals, and risk changes",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)

    def test_policy_is_the_single_approval_source(self):
        for required in (
            "Only an explicit approval in the current conversation",
            "File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval",
            "## Approval timing",
            "## How to ask",
            "Requirements → explicit Requirements approval → Design → explicit Design approval → Tasks → explicit Tasks approval",
            "Fast retains one plan and one plan approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)
        self.assertIn("bounded Human-First `审批摘要` projection", DOC_POLICY)
        self.assertIn("Risk level and decision impact do not change this order", APPROVAL_POLICY)
        self.assertNotIn("combined approval object", APPROVAL_POLICY)

    def test_legacy_specs_migrate_only_when_revised(self):
        self.assertIn("Do not bulk-migrate existing Specs", APPROVAL_POLICY)
        self.assertIn("next created or revised", APPROVAL_POLICY)
        self.assertIn("approved legacy Requirements", APPROVAL_POLICY)
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
            with self.subTest(heading=heading):
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

    def test_requirements_skill_enforces_complete_material_coverage(self):
        for required in (
            "Human-First `审批摘要`",
            "user-facing approval contract",
            "every materially distinct acceptance outcome",
            "one unambiguous group",
            "HTML anchors and traceability",
            "Resolve open requirements questions",
            "conversation delta",
        ):
            with self.subTest(required=required):
                self.assertTrue(
                    required in REQUIREMENT_SKILL or required in APPROVAL_POLICY
                )

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
        self.assertIn("Reuse each summary decision", DESIGN_SKILL)

    def test_design_skill_separates_material_and_internal_details(self):
        for required in (
            "public behavior or interfaces",
            "compatibility or migration",
            "external or irreversible effects",
            "Keep internal file layout, helpers, test organization",
            "exact short title",
            "summary/body conflict blocks approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, DESIGN_SKILL)
        self.assertIn(
            "Excluding the Human-First `审批摘要`", DESIGN_SKILL
        )

    def test_design_collects_its_own_decisions_after_brainstorming(self):
        brainstorming = (ROOT / "brainstorming" / "SKILL.md").read_text()
        self.assertIn("Collect decisions about observable outcomes here", brainstorming)
        self.assertIn("`selectedApproach` names the requirements direction", brainstorming)
        self.assertIn("## Design Decision Collection", DESIGN_SKILL)
        self.assertIn("hold a separate Design-stage user-question exchange", DESIGN_SKILL)
        self.assertIn("ask at least one design-focused question", DESIGN_SKILL)
        self.assertIn("Design decision collection is distinct from approval", DESIGN_SKILL)
        self.assertIn("return to Requirements", DESIGN_SKILL)

    def test_policy_asking_adapts_to_available_tool(self):
        self.assertIn("Whenever a LazySpec workflow needs an answer", APPROVAL_POLICY)
        self.assertIn("user-question tool exposed by the current agent environment", APPROVAL_POLICY)
        self.assertIn("Do not require a particular tool name", APPROVAL_POLICY)
        self.assertIn("only fields supported by the selected tool", APPROVAL_POLICY)
        self.assertIn("one decision", APPROVAL_POLICY)
        self.assertIn("single-choice question", APPROVAL_POLICY)
        self.assertIn("`Approve` and `Request changes` meanings", APPROVAL_POLICY)
        self.assertIn("directly in the conversation", APPROVAL_POLICY)
        self.assertNotIn("AskUserQuestion", APPROVAL_POLICY)
        self.assertNotIn("```json", APPROVAL_POLICY)
        for text in (ROUTER, REQUIREMENT_SKILL, DESIGN_SKILL):
            with self.subTest(document=text[:40]):
                self.assertEqual(
                    0, len(re.findall(r"```json\n", text))
                )

    def test_approval_questions_target_the_summary(self):
        self.assertIn(
            "审批摘要是否准确覆盖了需求的目标、范围、核心行为与风险？",
            REQUIREMENT_SKILL,
        )
        self.assertIn(
            "审批摘要是否准确覆盖了设计方案、关键决策及风险？", DESIGN_SKILL
        )
        for text in (REQUIREMENT_SKILL, DESIGN_SKILL):
            with self.subTest(document=text[:40]):
                self.assertIn("approval-policy.md", text)

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
