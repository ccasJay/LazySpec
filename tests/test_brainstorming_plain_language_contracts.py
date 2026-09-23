import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = ROOT / "using-lazyspec" / "SKILL.md"
BRAINSTORMING = ROOT / "brainstorming" / "SKILL.md"


class BrainstormingPlainLanguageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.router = ROUTER.read_text()
        cls.brainstorming = BRAINSTORMING.read_text()

    def test_router_defers_conversation_contract_to_brainstorming(self):
        text = self.router
        self.assertIn(
            "Human-First Interaction rules defined in `brainstorming/SKILL.md`", text
        )
        self.assertIn(
            "do not create a new artifact, change the internal `BrainstormingContext` schema",
            text,
        )
        self.assertIn(
            "Requirements, Design, Tasks, fast mode, or Memory behavior", text
        )

    def test_brainstorming_contract_is_result_first_and_brainstorming_only(self):
        text = self.brainstorming
        self.assertIn(
            "Apply these rules only to the user-facing Brainstorming conversation", text
        )
        self.assertIn("lead with the user-visible result", text)
        self.assertIn("Ask each question to make exactly one decision", text)
        self.assertIn("Name options by the result the user will notice", text)
        self.assertIn("plain-language Chinese by default", text)
        self.assertIn("technical term the first time it appears", text)
        self.assertIn("Do not omit the feature's scope, observable behavior, constraints, risks, or success criteria", text)
        self.assertIn("decision, option consequences, and recommendation reason", text)
        self.assertIn(
            "Requirements, Design, Tasks, fast mode, or Memory behavior", text
        )

    def test_questions_adapt_option_count_and_keep_one_decision(self):
        text = self.brainstorming
        self.assertIn("Ask only one question at a time", text)
        self.assertIn("Supply only meaningful mutually exclusive options when useful; do not pad the list", text)
        self.assertIn("not a required option count", text)
        self.assertIn("现在只需要决定什么，以及这个决定会影响什么", text)
        self.assertIn("（推荐）", text)
        self.assertIn("4. 其他", text)

    def test_approach_comparison_is_user_visible_and_decision_relevant(self):
        text = self.brainstorming
        self.assertIn("Compare viable requirements directions when their observable outcomes or scope differ", text)
        self.assertIn("do not manufacture alternatives", text)
        for heading in ("用户会得到什么", "主要限制或风险", "适用条件"):
            with self.subTest(heading=heading):
                self.assertIn(f"`{heading}`", text)
        self.assertIn("user-visible result rather than its implementation pattern", text)
        self.assertIn("leave implementation design decisions to Design", text)

    def test_plain_language_adapts_without_omitting_substance(self):
        text = self.brainstorming
        self.assertIn("plain-language Chinese by default", text)
        self.assertIn("match that level", text)
        self.assertIn("Briefly explain every necessary technical term", text)
        self.assertIn("Hide type names, internal field names, Requirement IDs, file paths", text)
        self.assertIn("scope, observable behavior, constraints, risks, or success criteria", text)
        self.assertIn("decision, option consequences, and recommendation reason", text)

    def test_final_context_headings_map_to_unchanged_schema(self):
        text = self.brainstorming
        headings = ("目标", "包含", "不包含", "必须遵守", "完成表现", "需求方向")
        positions = [text.index(f"     {heading}\n") for heading in headings]
        self.assertEqual(sorted(positions), positions)
        mappings = {
            "`目标` → `objective`",
            "`包含` and `不包含` → `scope`",
            "`必须遵守` → `constraints`",
            "`完成表现` → `successCriteria`",
            "`需求方向` → `selectedApproach`",
        }
        for mapping in mappings:
            with self.subTest(mapping=mapping):
                self.assertIn(mapping, text)
        self.assertIn("approved: true", text)

    def test_context_approval_stays_separate_from_approach_selection(self):
        text = self.brainstorming
        self.assertIn("Selecting an approach records only `selectedApproach`", text)
        self.assertIn("it is not approval", text)
        self.assertIn("ask a separate approval question", text)
        self.assertIn("是否批准以上需求方向并进入 Requirements？", text)
        self.assertIn("修改内容", text)
        self.assertIn("重新比较需求方向", text)
        self.assertIn("Only option 1 or an unambiguous affirmative answer", text)
        self.assertIn("Do not set `approved: true`", text)

    def test_readme_describes_plain_language_and_adaptive_depth(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("Brainstorming 默认用白话中文", text)
        self.assertIn("每次只请用户做一个决定", text)
        self.assertIn("表达会随之提高专业程度", text)
        self.assertIn("不会省略范围、约束、风险和成功标准", text)


if __name__ == "__main__":
    unittest.main()
