import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
PLUGIN_MANIFEST = (ROOT / ".claude-plugin" / "plugin.json").read_text()
SKILL = (ROOT / "orchestrating-specs" / "SKILL.md").read_text()
TEMPLATE = (ROOT / "orchestrating-specs" / "orchestration-templete.md").read_text()
APPROVAL_POLICY = (
    ROOT / "using-lazyspec" / "references" / "approval-policy.md"
).read_text()
DELIVERY_LOOP = (
    ROOT / "using-lazyspec" / "references" / "delivery-loop.md"
).read_text()


class OrchestrationTriggerTests(unittest.TestCase):
    def test_activation_requires_explicit_multi_spec_request(self):
        for required in (
            "Activate only when the user explicitly asks to jointly execute, orchestrate, or implement multiple approved Specs",
            "Never activate merely because the project contains multiple Specs",
            "single-Spec requests keep their existing workflow unchanged",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)
        self.assertIn(
            "Route to `orchestrating-specs` only when the user explicitly asks to jointly execute, orchestrate, or implement multiple approved Specs",
            ROUTER,
        )
        self.assertIn(
            "Never infer an orchestration request from the mere existence of multiple Specs",
            ROUTER,
        )

    def test_participating_specs_need_approved_three_documents(self):
        for required in (
            "user-approved `specs/{feature_name}/requirements.md`, `design.md`, and `tasks.md`",
            "never infer it from file existence",
            "only a fast `plan.md`",
            "do not create `orchestration.md`",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)

    def test_orchestration_is_registered_and_routed(self):
        self.assertIn("./orchestrating-specs", PLUGIN_MANIFEST)
        self.assertIn("`orchestrating-specs`", ROUTER)
        self.assertIn("lazyspec:orchestrating-specs", ROUTER)
        self.assertIn("../orchestrating-specs/SKILL.md", ROUTER)
        self.assertIn(
            "pass `RelevantMemoryContext` to `orchestrating-specs` as advisory input",
            ROUTER,
        )


class OrchestrationBoundaryTests(unittest.TestCase):
    def test_orchestration_is_not_a_new_planning_layer(self):
        for required in (
            "not a new Requirements, Design, or Tasks layer",
            "MUST NOT define new user behavior, interface requirements, or business scope",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)

    def test_orchestration_does_not_govern_intra_spec_task_execution(self):
        for required in (
            "MUST NOT specify how tasks inside any individual Spec are executed",
            "remain governed by that Spec's approved `tasks.md` and delivery-loop.md",
            "The orchestration decides only when a Spec's turn arrives, on which branch, and alongside which other Specs",
            "each Spec's internal task execution remains fully governed by that Spec's `tasks.md` and delivery-loop.md",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)
        self.assertIn(
            "does not govern how tasks inside any individual Spec are executed",
            ROUTER,
        )
        self.assertIn(
            "it does not govern intra-Spec task execution", DELIVERY_LOOP
        )

    def test_gaps_route_back_to_spec_revisions(self):
        for required in (
            "route it back to the affected Spec's Requirements, Design, or Tasks revision under delivery-loop.md's failure routing",
            "MUST NOT fill the gap inside `orchestration.md` and execute it",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)
        self.assertIn(
            "gaps between Specs route back to the affected Spec's Requirements/Design/Tasks revision",
            ROUTER,
        )

    def test_specs_remain_their_own_source_of_truth(self):
        self.assertIn(
            "Execute each Spec through its own approved Requirements, Design, and Tasks as the source of truth via delivery-loop.md",
            SKILL,
        )
        self.assertIn(
            "MUST NOT override or modify any Spec's approved content", SKILL
        )


class OrchestrationApprovalAndBranchTests(unittest.TestCase):
    def test_orchestration_approval_gate(self):
        self.assertIn(
            "The complete `orchestration.md` is the approval object",
            SKILL,
        )
        self.assertIn(
            "do not start any Spec execution before explicit approval",
            SKILL,
        )
        self.assertIn(
            "Multi-Spec orchestration retains one approval gate", APPROVAL_POLICY
        )
        self.assertIn(
            "Orchestration approval never approves new Spec content", APPROVAL_POLICY
        )
        self.assertIn(
            "multi-Spec orchestration approves its complete `orchestration.md`", ROUTER
        )

    def test_stacked_branch_strategy(self):
        for required in (
            "堆叠分支策略",
            "B 基于 A 的分支创建",
            "最后按相同顺序依次 merge",
            "overriding the default single-Spec `codex/<feature-name>` branch rule",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)
        self.assertIn("堆叠分支", TEMPLATE)
        self.assertIn(
            "cross-Spec branch stacking, sequencing, and coordination constraints, which override the default single-Spec branch rule",
            DELIVERY_LOOP,
        )

    def test_document_covers_required_contents(self):
        for heading in (
            "## 编排目标",
            "## 涉及的 Spec",
            "## 依赖关系与执行顺序",
            "## 可并行执行的部分",
            "## 分支与合并策略",
            "## 跨 Spec 协调约束",
            "## 跨 Spec 集成验证",
            "## 生命周期状态",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, TEMPLATE)
        self.assertIn("Feature Verification passed", TEMPLATE)
        self.assertIn(
            "只描述跨 Spec 协调，不规定单个 Spec 内部任务如何执行", TEMPLATE
        )


class OrchestrationLifecycleTests(unittest.TestCase):
    def test_memory_distillation_gate_is_mandatory(self):
        for required in (
            "## Memory Distillation Gate",
            "MUST proactively initiate the distillation step",
            "distill-spec-memory",
            "MUST NOT bypass that boundary or write Memory directly",
            "neither may be silently skipped",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)
        self.assertIn("Memory 沉淀门完成", TEMPLATE)

    def test_deletion_only_after_full_group_completion(self):
        for required in (
            "Never delete `orchestration.md` because a single Spec's Tasks finished",
            "delete only after the whole group's execution, verification, distillation, and final user confirmation are all complete",
            "delete only `specs/orchestration.md` itself",
            "MUST NOT delete any Spec's Requirements, Design, Tasks, or Feature Verification evidence",
        ):
            with self.subTest(required=required):
                self.assertIn(required, SKILL)

    def test_lifecycle_checklist_order(self):
        self.assertIn("编排已获用户批准", TEMPLATE)
        self.assertIn("各 Spec Feature Verification 全部 passed", TEMPLATE)
        self.assertIn("跨 Spec Integration Verification passed", TEMPLATE)
        self.assertLess(
            TEMPLATE.index("跨 Spec Integration Verification passed"),
            TEMPLATE.index("Memory 沉淀门完成"),
        )
        self.assertLess(
            TEMPLATE.index("Memory 沉淀门完成"),
            TEMPLATE.index("用户确认最终交付"),
        )
        self.assertLess(
            TEMPLATE.index("用户确认最终交付"),
            TEMPLATE.index("已删除 orchestration.md"),
        )


if __name__ == "__main__":
    unittest.main()
