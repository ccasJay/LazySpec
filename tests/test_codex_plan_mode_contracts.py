import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
REQUIREMENT_SKILL = (ROOT / "writing-requirement" / "SKILL.md").read_text()
REQUIREMENT_PROMPT = (ROOT / "writing-requirement" / "requirement-prompt.md").read_text()
DESIGN_SKILL = (ROOT / "writing-design" / "SKILL.md").read_text()
TASK_SKILL = (ROOT / "writing-task" / "SKILL.md").read_text()
BRAINSTORMING_SKILL = (ROOT / "brainstorming" / "SKILL.md").read_text()
PLUGIN_MANIFEST = (ROOT / ".claude-plugin" / "plugin.json").read_text()


class CodexPlanModeWorkflowContractTests(unittest.TestCase):
    def test_approved_plan_skips_brainstorming_and_enters_requirements(self):
        for required in (
            "requirements.md",
            'platform: "codex" | "non-codex" | "unknown"',
            'planMode: "active" | "inactive" | "unknown"',
            "content.trim()",
            "用户已明确批准该原生计划",
            "直接路由到 `writing-requirement`",
            'RouteDecision.stage` 仍为 `"requirements"',
            "不得调用标准 `brainstorming`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, ROUTER)

    def test_approved_plan_is_passed_as_complete_raw_session_input(self):
        self.assertIn("传递给 Requirements 的 `content` 必须是批准时的完整原文", ROUTER)
        for document in (REQUIREMENT_SKILL, REQUIREMENT_PROMPT):
            with self.subTest(document=document[:32]):
                self.assertIn("CodexPlanArtifact", document)
                self.assertIn("complete", document)
                self.assertIn("Markdown", document)
                self.assertIn("line breaks", document)
                self.assertIn("long text", document)
        for document in (REQUIREMENT_SKILL, REQUIREMENT_PROMPT):
            for forbidden_transform in ("summarize", "rewrite", "truncate"):
                with self.subTest(document=document[:32], transform=forbidden_transform):
                    self.assertIn(forbidden_transform, document)
        self.assertIn("Plan approval is not Requirements approval", REQUIREMENT_SKILL)
        self.assertIn("request the Requirements approval separately", REQUIREMENT_PROMPT)

    def test_empty_unapproved_and_unknown_modes_fail_closed(self):
        for blocked_case in ("计划不存在或为空", "计划已生成但未批准", "平台或模式未知"):
            with self.subTest(blocked_case=blocked_case):
                self.assertIn(blocked_case, ROUTER)
        for required in (
            "fail closed",
            "不得调用 `writing-requirement`",
            "不得创建或更新 `requirements.md`",
            "不得自动选择任一分支",
            "明确切换到标准 Brainstorming",
        ):
            with self.subTest(required=required):
                self.assertIn(required, ROUTER)

    def test_non_codex_normal_codex_and_existing_spec_routes_remain_compatible(self):
        for required in (
            "known to be non-Codex or not in Plan Mode, route to `brainstorming`",
            "已知处于非 Codex 环境或 Codex 非 Plan Mode 时，继续走标准 `brainstorming`",
            "Route to `brainstorming` first only when the user explicitly requests it",
            "已有 `requirements.md` 且用户未明确要求重新规划",
            "只更新当前会话 Context",
            "不得因适配自动修改既有 Spec 文件",
        ):
            with self.subTest(required=required):
                self.assertIn(required, ROUTER)
        self.assertIn("ask a separate approval question", BRAINSTORMING_SKILL)

    def test_requirements_design_tasks_chain_keeps_approval_and_execution_boundaries(self):
        self.assertIn(
            "For medium/high risk, route to `writing-design` only after Requirements has explicit user approval",
            ROUTER,
        )
        self.assertIn(
            "to `writing-task` only after Design has explicit user approval",
            ROUTER,
        )
        self.assertIn(
            "Only explicit approval in the current conversation records approval of the current `审批摘要`",
            REQUIREMENT_SKILL,
        )
        self.assertIn("Any material change invalidates prior approval", REQUIREMENT_SKILL)
        self.assertIn("MUST NOT proceed to the design document", REQUIREMENT_SKILL)
        self.assertIn(
            "Only explicit approval in the current conversation records approval of the current `审批摘要`",
            DESIGN_SKILL,
        )
        self.assertIn("Any material change invalidates prior approval", DESIGN_SKILL)
        self.assertIn("MUST NOT proceed to the implementation plan", DESIGN_SKILL)
        self.assertIn("Approval ends planning and MUST NOT start implementation", TASK_SKILL)
        self.assertIn("complete `requirements.md`, `design.md`, and `tasks.md`", ROUTER)
        self.assertIn("all currently unchecked TODOs", ROUTER)
        self.assertIn("After each TODO passes its verification", ROUTER)
        self.assertIn("`//TODO`", TASK_SKILL)

    def test_adapter_has_no_persistent_intermediate_artifact_or_new_stage(self):
        self.assertIn("不是新的 LazySpec 阶段", ROUTER)
        self.assertIn("不得创建 `plan.md`、Brainstorming 文档或其他持久化中间产物", ROUTER)
        self.assertNotIn("codex-plan-bridge", PLUGIN_MANIFEST)
        self.assertFalse((ROOT / "specs" / "codex-plan-mode-adaptation" / "plan.md").exists())


if __name__ == "__main__":
    unittest.main()
