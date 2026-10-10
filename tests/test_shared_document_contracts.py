"""Static document/Skill contracts for v2 binary architecture."""

import json
import re
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
PLAN_SKILL = (ROOT / "writing-plan" / "SKILL.md").read_text()
PLAN_PROMPT = (ROOT / "writing-plan" / "plan-prompt.md").read_text()
PLAN_TEMPLATE = (ROOT / "writing-plan" / "plan-template.md").read_text()


class SharedDocumentContractTests(unittest.TestCase):
    def test_policy_defines_complete_file_authority_and_materiality(self):
        for required in (
            "`spec.md` and `plan.md` each use the complete saved phase document as their approval object",
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
            "Spec → explicit Spec approval → Plan → explicit Plan approval",
            "Fast retains one plan and one plan approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)
        self.assertIn("Record each decision, rationale, constraint, or procedure once", DOC_POLICY)
        self.assertIn("Risk level and decision impact do not change this order", APPROVAL_POLICY)
        self.assertNotIn("combined approval object", APPROVAL_POLICY)

    def test_doc_policy_enforces_binary_architecture(self):
        self.assertIn("put information in exactly two artifacts", DOC_POLICY)
        self.assertIn("spec.md", DOC_POLICY)
        self.assertIn("plan.md", DOC_POLICY)
        self.assertIn("Users and Agents share one document body", DOC_POLICY)
        self.assertNotIn("Requirements define observable behavior, Design records implementation decisions", DOC_POLICY)

    def test_spec_template_and_skill_enforce_unified_spec(self):
        self.assertIn("status: proposed", SPEC_TEMPLATE)
        self.assertIn("## 目标与范围", SPEC_TEMPLATE)
        self.assertIn("## 需求与验收标准", SPEC_TEMPLATE)
        self.assertIn("## 架构与核心决策", SPEC_TEMPLATE)
        self.assertIn("## 曾考虑的备选方案", SPEC_TEMPLATE)
        self.assertIn("## 风险与否定性保证", SPEC_TEMPLATE)

        self.assertIn("Structured Probing (/grill-me Style)", SPEC_SKILL)
        self.assertIn("alternatives considered", SPEC_SKILL.lower())
        self.assertIn("spec.md", SPEC_SKILL)
        self.assertNotIn("审批摘要", SPEC_TEMPLATE)

    def test_plan_template_and_skill_enforce_behavioral_tasks(self):
        self.assertIn("- [ ] //TODO 1. 完成", PLAN_TEMPLATE)
        self.assertIn("## Feature Verification", PLAN_TEMPLATE)
        self.assertIn("### Planned Checks", PLAN_TEMPLATE)
        self.assertIn("### Latest Result", PLAN_TEMPLATE)

        self.assertIn("Behavioral Slices", PLAN_SKILL)
        self.assertIn("Requirement Linkage", PLAN_SKILL)
        self.assertIn("Feature Verification Appendix", PLAN_SKILL)
        self.assertNotIn("审批摘要", PLAN_TEMPLATE)

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
            "请审阅规范文件 specs/<feature>/spec.md；是否批准其中的目标、范围、验收标准、架构决策与备选方案？",
            SPEC_SKILL,
        )
        self.assertIn(
            "请审阅执行计划 specs/<feature>/plan.md；是否批准其中的任务拆解与验收范围？",
            PLAN_SKILL,
        )


if __name__ == "__main__":
    unittest.main()
