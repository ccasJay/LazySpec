import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
CODEX_ADAPTER = (
    ROOT / "using-lazyspec" / "references" / "codex-plan-mode.md"
).read_text()
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
            "the user has explicitly approved that native plan",
            "routes directly to `writing-requirement`",
            'RouteDecision.stage` remaining `"requirements"`',
            "do not invoke standard `brainstorming`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, CODEX_ADAPTER)
        self.assertIn("[codex-plan-mode.md](references/codex-plan-mode.md)", ROUTER)

    def test_approved_plan_is_passed_as_complete_raw_session_input(self):
        self.assertIn(
            "the `content` passed to Requirements must be the complete original text as approved",
            CODEX_ADAPTER,
        )
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

    def test_empty_unapproved_and_unknown_modes_fail_closed(self):
        for blocked_case in (
            "when the plan is missing or empty",
            "when a plan has been generated but not approved",
            "when the platform or mode is unknown",
        ):
            with self.subTest(blocked_case=blocked_case):
                self.assertIn(blocked_case, CODEX_ADAPTER)
        for required in (
            "fail closed",
            "do not invoke `writing-requirement`",
            "do not create or update `requirements.md`",
            "do not automatically choose either branch",
            "switching to standard Brainstorming",
        ):
            with self.subTest(required=required):
                self.assertIn(required, CODEX_ADAPTER)
        self.assertIn("必须停留并要求用户明确切换到标准 Brainstorming", ROUTER)

    def test_non_codex_normal_codex_and_existing_spec_routes_remain_compatible(self):
        for required in (
            "known to be non-Codex or not in Plan Mode, route to `brainstorming`",
            "已知处于非 Codex 环境或 Codex 非 Plan Mode 时，继续走标准 `brainstorming`",
            "Route to `brainstorming` first only when the user explicitly requests it",
        ):
            with self.subTest(required=required):
                self.assertIn(required, ROUTER)
        for required in (
            "when `requirements.md` already exists and the user has not explicitly requested replanning",
            "updates only the current session Context",
            "do not automatically modify existing Spec files because of the adapter",
        ):
            with self.subTest(required=required):
                self.assertIn(required, CODEX_ADAPTER)
        self.assertIn("ask a separate approval question", BRAINSTORMING_SKILL)

    def test_requirements_design_tasks_chain_keeps_approval_and_execution_boundaries(self):
        policy = (
            ROOT / "using-lazyspec" / "references" / "approval-policy.md"
        ).read_text()
        self.assertIn(
            "Draft toward combined review at every risk level under approval-policy.md",
            ROUTER,
        )
        self.assertIn(
            "Only an explicit approval in the current conversation",
            policy,
        )
        self.assertIn("A material change invalidates the prior approval", policy)
        self.assertIn(
            "never mark an unapproved draft approved",
            REQUIREMENT_SKILL,
        )
        self.assertIn("never mark an unapproved draft approved", DESIGN_SKILL)
        self.assertIn("Approval ends planning and MUST NOT start implementation", TASK_SKILL)
        delivery = (
            ROOT / "using-lazyspec" / "references" / "delivery-loop.md"
        ).read_text()
        self.assertIn("complete `requirements.md`, `design.md`, and `tasks.md`", delivery)
        self.assertIn("all currently unchecked TODOs", delivery)
        self.assertIn("After each TODO passes its verification", delivery)
        self.assertIn("`//TODO`", TASK_SKILL)

    def test_adapter_has_no_persistent_intermediate_artifact_or_new_stage(self):
        self.assertIn("it is not a new LazySpec stage", CODEX_ADAPTER)
        self.assertIn("must not create `plan.md`, a Brainstorming document, or any other persistent intermediate artifact", CODEX_ADAPTER)
        self.assertNotIn("codex-plan-bridge", PLUGIN_MANIFEST)
        self.assertFalse((ROOT / "specs" / "codex-plan-mode-adaptation" / "plan.md").exists())


if __name__ == "__main__":
    unittest.main()
