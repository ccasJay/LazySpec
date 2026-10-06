"""Static document/Skill contracts; these do not simulate Agent behavior."""

import json
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


class SharedDocumentContractTests(unittest.TestCase):
    def test_policy_defines_complete_file_authority_and_materiality(self):
        for required in (
            "Requirements, Design, and Tasks each use the complete saved phase document as their approval object",
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
            "Requirements → explicit Requirements approval → Design → explicit Design approval → Tasks → explicit Tasks approval",
            "Fast retains one plan and one plan approval",
        ):
            with self.subTest(required=required):
                self.assertIn(required, APPROVAL_POLICY)
        self.assertIn("Record each decision, rationale, constraint, or procedure once", DOC_POLICY)
        self.assertIn("Risk level and decision impact do not change this order", APPROVAL_POLICY)
        self.assertNotIn("combined approval object", APPROVAL_POLICY)

    def test_legacy_specs_remain_readable_without_format_migration(self):
        self.assertIn("Do not migrate existing Specs solely to adopt this format", APPROVAL_POLICY)
        self.assertIn("without rewriting or adding a summary", APPROVAL_POLICY)
        self.assertIn("not a separate higher-authority contract", APPROVAL_POLICY)
        self.assertIn("If its sections conflict, resolve the affected contract", APPROVAL_POLICY)
        self.assertIn("retain unchanged behavior, anchors, TODO text, and valid evidence", APPROVAL_POLICY)
        self.assertIn("legacy Requirements document", REQUIREMENT_SKILL)
        self.assertIn("legacy Design document", DESIGN_SKILL)

    def test_requirements_template_has_one_body_with_stories_anchors_and_risk(self):
        body = REQUIREMENT_TEMPLATE.split("```markdown\n", 1)[1].split("```", 1)[0]
        self.assertEqual(
            ["引言", "需求", "风险与待确认"],
            re.findall(r"^## (.+)$", body, re.M),
        )
        requirements = re.findall(r"^### 需求 (\d+)：[^\n]*\n(.*?)(?=^### |^## |\Z)", body, re.M | re.S)
        self.assertEqual(2, len(requirements))
        all_anchors = []
        for number, section in requirements:
            with self.subTest(requirement=number):
                self.assertEqual(1, section.count("**用户故事：**"))
                self.assertIn("#### 验收标准", section)
                criteria = re.findall(r'^(\d+)\. <a id="([^"]+)"></a> .+$', section, re.M)
                self.assertTrue(criteria)
                for ordinal, anchor in criteria:
                    self.assertEqual(f"req-{number}-{ordinal}", anchor)
                    all_anchors.append(anchor)
        self.assertEqual(len(all_anchors), len(set(all_anchors)))
        self.assertNotIn("审批摘要", body)

    def test_risk_is_standalone_and_task_link_remains_valid(self):
        task_template = (ROOT / "writing-task/task-templete.md").read_text()
        for template in (REQUIREMENT_TEMPLATE, DESIGN_TEMPLATE):
            body = template.split("```markdown\n", 1)[1].split("```", 1)[0]
            with self.subTest(template=template[:40]):
                self.assertEqual(1, len(re.findall(r"^## 风险与待确认$", body, re.M)))
                for field in ("风险等级", "理由", "关键操作", "风险", "待确认"):
                    self.assertIn(f"{field}：", body)
        self.assertIn("(./design.md#风险与待确认)", task_template)

    def test_active_resources_do_not_require_the_retired_two_layer_contract(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        paths = [ROOT / "README.md"]
        for directory in manifest["skills"]:
            paths.extend((ROOT / directory).rglob("*.md"))
        for path in paths:
            text = path.read_text()
            for retired in ("Human-First", "summary/body", "one-screen", "upper-level material contract", "100–180", "summary-contract"):
                with self.subTest(path=path, retired=retired):
                    self.assertNotIn(retired, text)

    def test_requirements_skill_enforces_shared_material_contract(self):
        for required in (
            "one body for user review and Agent execution",
            "confirmed observable outcomes",
            "user stories and EARS criteria",
            "Resolve open requirements questions",
            "standalone `## 风险与待确认`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, REQUIREMENT_SKILL)
        self.assertIn("Do not add an approval summary", REQUIREMENT_PROMPT)

    def test_design_template_has_one_decision_section_and_conditional_details(self):
        body = DESIGN_TEMPLATE.split("```markdown\n", 1)[1].split("```", 1)[0]
        self.assertEqual(
            ["Overview", "Key Design Decisions", "风险与待确认", "Testing Strategy"],
            re.findall(r"^## (.+)$", body, re.M),
        )
        self.assertNotIn("审批摘要", body)
        for section in ("Architecture", "Components and Interfaces", "Data Models", "Error Handling", "Research Findings"):
            with self.subTest(section=section):
                self.assertNotIn(f"## {section}", body)
                self.assertIn(f"- {section}", DESIGN_TEMPLATE)
        self.assertIn("Omit an inapplicable section entirely", DESIGN_TEMPLATE)

    def test_design_skill_records_material_decisions_once_without_padding(self):
        for required in (
            "public behavior or interfaces",
            "compatibility or migration",
            "external or irreversible effects",
            "Record each key choice, rationale, and impact once",
            "Reference those decisions from technical sections",
            "complete design document within 180 lines",
            "no minimum length",
            "retain details needed to avoid implementation ambiguity",
        ):
            with self.subTest(required=required):
                self.assertIn(required, DESIGN_SKILL)
        self.assertIn("Tasks owns the concrete Planned Checks and running evidence", DESIGN_PROMPT)

    def test_design_collects_its_own_decisions_after_requirements(self):
        self.assertIn("Do not treat requirement collection or Requirements approval", DESIGN_SKILL)
        self.assertIn("## Design Decision Collection", DESIGN_SKILL)
        self.assertIn("hold a separate Design-stage user-question exchange", DESIGN_SKILL)
        self.assertIn("ask at least one design-focused question", DESIGN_SKILL)
        self.assertIn("Design decision collection is distinct from approval", DESIGN_SKILL)
        self.assertIn("return to Requirements", DESIGN_SKILL)

    def test_design_questions_resolve_user_choices_before_drafting(self):
        decision_section = DESIGN_SKILL.split("## Design Decision Collection", 1)[1].split(
            "## Document Contract", 1
        )[0]
        for expected in (
            "approved Requirements, relevant code, and explicit prior decisions",
            "architecture, public interfaces, data, dependencies, compatibility, external effects, security, and recovery",
            "Research discoverable project facts",
            "Distinguish material or user-reserved choices from routine internal techniques",
            "recommend a viable option with a concise reason",
            "main consequences or trade-offs",
            "Ask one focused question at a time",
            "Do not ask for a choice already made explicitly",
            "Clarify an ambiguous answer before moving on",
            "does not close an unresolved material choice",
            "Do not draft affected Design sections",
            "ask at least one design-focused question",
            "return to Requirements",
        ):
            with self.subTest(expected=expected):
                self.assertIn(expected, decision_section)
        self.assertLess(
            decision_section.index("Before asking, examine"),
            decision_section.index("For each choice requiring the user's decision"),
        )
        self.assertLess(
            decision_section.index("Clarify an ambiguous answer"),
            decision_section.index("For a new Design with no competing choice"),
        )
        self.assertIn("complete the Design-stage decision exchange", DESIGN_PROMPT)

    def test_policy_asking_adapts_to_available_tool(self):
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
        for text in (ROUTER, REQUIREMENT_SKILL, DESIGN_SKILL):
            with self.subTest(document=text[:40]):
                self.assertEqual(
                    0, len(re.findall(r"```json\n", text))
                )

    def test_approval_questions_target_the_current_file(self):
        self.assertIn(
            "请审阅需求文件；是否批准其中的目标、范围、验收标准与风险？",
            REQUIREMENT_SKILL,
        )
        self.assertIn(
            "请审阅设计文件；是否批准其中的方案、关键决策、风险与测试策略？", DESIGN_SKILL
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
            "Requirements, Design, and Tasks each use the complete saved phase document as their approval object", ROUTER
        )


if __name__ == "__main__":
    unittest.main()
