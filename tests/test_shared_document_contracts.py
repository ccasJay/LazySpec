"""Static document/Skill contracts for the single-artifact architecture."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
POLICIES = ROOT / "using-lazyspec" / "references"
APPROVAL_POLICY = (POLICIES / "approval-policy.md").read_text()
DOC_POLICY = (POLICIES / "doc-policy.md").read_text()
SPEC_SKILL = (ROOT / "writing-spec" / "SKILL.md").read_text()
SPEC_PROMPT = (ROOT / "writing-spec" / "spec-prompt.md").read_text()
SPEC_TEMPLATE = (ROOT / "writing-spec" / "spec-template.md").read_text()


class SharedDocumentContractTests(unittest.TestCase):
    def test_policy_defines_complete_file_authority_and_materiality(self):
        for required in (
            "`spec.md` uses the complete saved document as its approval object",
            "Users and Agents share one body",
            "public interfaces or data changes",
            "security or privacy",
            "When uncertain, classify a change as material",
            "contains no conflicting contract items",
            "no unresolved material user decision",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)

    def test_policy_preserves_revision_and_evidence_boundaries(self):
        for required in (
            "A material change invalidates the prior approval",
            "non-material refinement",
            "additions, changes, removals, and risk changes",
            "equally strong verification methods",
            "not unrelated completed work",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)

    def test_policy_is_the_single_approval_source(self):
        for required in (
            "Only an explicit approval in the current conversation",
            "File existence, timeout, silence, explanations, ambiguous replies, and requested changes do not imply approval",
            "## Approval timing",
            "## How to ask",
            "`spec.md` → explicit Spec approval → execution",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)
        self.assertIn("Record each decision, rationale, constraint, or procedure once", DOC_POLICY)
        self.assertIn("Risk level and decision impact do not change this order", APPROVAL_POLICY)
        self.assertNotIn("combined approval object", APPROVAL_POLICY)

    def test_doc_policy_enforces_single_artifact(self):
        for required in (
            "exactly one planning artifact per feature",
            "Do not create `plan.md`",
            "spec.md",
            "Users and Agents share one document body",
            "at most 12 acceptance rows",
            "Never omit distinct approved behavior",
        ):
            with self.subTest(required=required):
                self.assertIn(required, DOC_POLICY)
        self.assertNotIn("Requirements define observable behavior, Design records implementation decisions", DOC_POLICY)

    def test_spec_template_and_skill_enforce_single_artifact(self):
        for required in (
            "status: proposed",
            "## 目标与范围",
            "## 用户故事",
            "## 验收标准",
            "## 决策",
            "## 风险与否定性保证",
            "## 任务",
            "## 执行记录",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SPEC_TEMPLATE)

        self.assertIn("Structured Probing (/grill-me Style)", SPEC_SKILL)
        self.assertIn("alternatives considered", SPEC_SKILL.lower())
        self.assertIn("spec.md", SPEC_SKILL)
        self.assertIn("Create exactly one artifact", SPEC_SKILL)
        self.assertIn("Contract zone", SPEC_SKILL)
        self.assertNotIn("审批摘要", SPEC_TEMPLATE)

    def test_spec_prompt_enforces_compressed_shapes(self):
        for required in (
            "One artifact",
            "User stories",
            "Inline verification",
            "Shape and budget",
            "Single source",
            "Execution record",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SPEC_PROMPT)

    def test_approval_asking_adapts_to_available_tool(self):
        self.assertIn("Whenever a LazySpec workflow needs an answer", APPROVAL_POLICY)
        self.assertIn("tool definitions exposed by the current agent environment", APPROVAL_POLICY)
        self.assertIn("Do not require a particular tool name", APPROVAL_POLICY)
        self.assertIn("only fields supported by the selected tool", APPROVAL_POLICY)
        self.assertIn("one decision", APPROVAL_POLICY)
        self.assertIn("single-choice question", APPROVAL_POLICY)
        self.assertIn("`Approve` and `Request changes` meanings", APPROVAL_POLICY)
        self.assertIn("directly in the conversation", APPROVAL_POLICY)
        self.assertNotIn("AskUserQuestion", APPROVAL_POLICY)
        self.assertNotIn("```json", APPROVAL_POLICY)

    def test_approval_questions_target_the_current_file(self):
        self.assertIn(
            "请审阅规范文件 specs/<feature>/spec.md；是否批准其中的目标、用户故事、验收标准、架构决策、风险、任务拆解与验收方式？",
            SPEC_SKILL,
        )
        self.assertNotIn("请审阅执行计划 specs/<feature>/plan.md", ROUTER + SPEC_SKILL)


if __name__ == "__main__":
    unittest.main()
