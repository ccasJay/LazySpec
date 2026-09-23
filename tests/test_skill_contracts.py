import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WRITING_SKILLS = (
    ROOT / "writing-requirement" / "SKILL.md",
    ROOT / "writing-design" / "SKILL.md",
    ROOT / "writing-task" / "SKILL.md",
)


class SkillContractTests(unittest.TestCase):
    def test_registered_routing_has_sibling_fallbacks(self):
        text = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        for name in (
            "brainstorming",
            "writing-requirement",
            "writing-design",
            "writing-task",
            "distill-spec-memory",
            "fast",
            "orchestrating-specs",
        ):
            self.assertIn(f"`lazyspec:{name}`", text)
            self.assertIn(f"`../{name}/SKILL.md`", text)
        self.assertIn("relative to this `using-lazyspec/SKILL.md`", text)

    def test_writing_resources_are_skill_relative(self):
        for path in WRITING_SKILLS:
            with self.subTest(path=path):
                text = path.read_text()
                self.assertIn("relative to the directory containing this `SKILL.md`", text)
                self.assertIn("against `ACTIVE_PROJECT_ROOT`", text)
                self.assertIn("user's project working directory at session start", text)
                self.assertIn("Never use this Skill's directory", text)

        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        self.assertIn("bind `ACTIVE_PROJECT_ROOT`", routing)
        self.assertIn("Never derive `ACTIVE_PROJECT_ROOT`", routing)
        self.assertIn("never default to the Plugin installation directory", routing)

    def test_approval_question_tool_rule_lives_only_in_policy(self):
        policy = (
            ROOT / "using-lazyspec" / "references" / "approval-policy.md"
        ).read_text()
        self.assertIn("user-question tool exposed by the current agent environment", policy)
        self.assertIn("Do not require a particular tool name", policy)
        self.assertIn("only fields supported by the selected tool", policy)
        self.assertIn("single-choice question", policy)
        self.assertIn("`Approve` and `Request changes` meanings", policy)
        self.assertIn("directly in the conversation", policy)
        self.assertNotIn("AskUserQuestion", policy)
        self.assertNotIn("```json", policy)

        for path in WRITING_SKILLS:
            with self.subTest(path=path):
                text = path.read_text()
                self.assertNotIn("metadata.source", text)
                self.assertEqual(0, len(re.findall(r"```json\n", text)))
                self.assertIn("approval-policy.md", text)

    def test_task_execution_contract_batches_todos_on_feature_branch(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        delivery = (
            ROOT / "using-lazyspec" / "references" / "delivery-loop.md"
        ).read_text()
        planning = (ROOT / "writing-task" / "SKILL.md").read_text()
        self.assertIn("complete `requirements.md`, `design.md`, and `tasks.md`", delivery)
        self.assertIn("all currently unchecked TODOs", delivery)
        self.assertIn("without waiting for per-task approval", delivery)
        self.assertIn("new feature branch", delivery)
        self.assertIn("codex/<feature-name>", delivery)
        self.assertIn("After each TODO passes its verification", delivery)
        self.assertNotIn("Only focus on ONE user-selected task", routing)
        self.assertNotIn("If multiple tasks are requested, ask the user to select one", routing)
        self.assertNotIn("execute only one requested task at a time", routing)
        for text in (delivery, planning):
            self.assertIn("checkbox token from `[ ]` to `[x]`", text)
            self.assertIn("`//TODO`", text)

    def test_codex_plan_mode_routing_contract(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        adapter = (
            ROOT / "using-lazyspec" / "references" / "codex-plan-mode.md"
        ).read_text()
        self.assertIn("[codex-plan-mode.md](references/codex-plan-mode.md)", routing)
        for token in (
            "RuntimeMode",
            'platform: "codex" | "non-codex" | "unknown"',
            'planMode: "active" | "inactive" | "unknown"',
            "CodexPlanArtifact",
            'source: "codex-plan-mode"',
            "BrainstormingInput",
            "content.trim()",
            "requirements.md",
            'RouteDecision.stage` remaining `"requirements"`',
        ):
            with self.subTest(token=token):
                self.assertIn(token, adapter)
        self.assertIn("不得调用标准 `brainstorming`", routing)
        self.assertIn("不得自动选择任一分支", routing)
        self.assertIn("do not serialize them or write them into project files", adapter)

    def test_codex_plan_mode_failure_and_session_boundaries(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        adapter = (
            ROOT / "using-lazyspec" / "references" / "codex-plan-mode.md"
        ).read_text()
        for token in (
            "fail closed",
            "when the plan is missing or empty",
            "when a plan has been generated but not approved",
            "when the platform or mode is unknown",
            "do not create or update `requirements.md`",
            "must not create `plan.md`, a Brainstorming document",
            "the old `CodexPlanArtifact` and its approval status become invalid immediately",
            "replanning",
            "when `requirements.md` already exists and the user has not explicitly requested replanning",
        ):
            with self.subTest(token=token):
                self.assertIn(token, adapter)
        self.assertIn("不得自动选择任一分支", routing)

    def test_downstream_approval_and_compatibility_boundaries(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        policy = (
            ROOT / "using-lazyspec" / "references" / "approval-policy.md"
        ).read_text()
        requirements = (ROOT / "writing-requirement" / "SKILL.md").read_text()
        design = (ROOT / "writing-design" / "SKILL.md").read_text()
        tasks = (ROOT / "writing-task" / "SKILL.md").read_text()
        brainstorming = (ROOT / "brainstorming" / "SKILL.md").read_text()

        self.assertIn(
            "create and approve Requirements, Design, and Tasks one at a time at every risk level",
            routing,
        )
        self.assertIn("Do not create or draft Design until the current Requirements has explicit approval", requirements)
        self.assertIn("Do not create or draft Tasks until the current Design has explicit approval", design)
        self.assertIn(
            "Only an explicit approval in the current conversation",
            policy,
        )
        self.assertIn(
            "A material change invalidates the prior approval", policy
        )
        self.assertIn(
            "Only explicit approval in the current conversation records approval of the current `审批摘要`",
            policy,
        )
        self.assertIn(
            "never mark an unapproved draft approved",
            requirements,
        )
        self.assertIn("never mark an unapproved draft approved", design)
        self.assertIn("Approval ends planning and MUST NOT start implementation", tasks)
        delivery = (
            ROOT / "using-lazyspec" / "references" / "delivery-loop.md"
        ).read_text()
        self.assertIn("complete `requirements.md`, `design.md`, and `tasks.md`", delivery)
        self.assertIn("all currently unchecked TODOs", delivery)
        self.assertIn("After each TODO passes its verification", delivery)
        self.assertIn("Answer task questions without starting work", routing)
        self.assertIn("`//TODO`", tasks)
        self.assertIn("ask a separate approval question", brainstorming)

    def test_requirement_writer_accepts_codex_plan_artifact(self):
        skill = (ROOT / "writing-requirement" / "SKILL.md").read_text()
        prompt = (ROOT / "writing-requirement" / "requirement-prompt.md").read_text()
        for text in (skill, prompt):
            with self.subTest(document=text[:40]):
                self.assertIn("CodexPlanArtifact", text)
                self.assertIn("complete `content`", text)
                self.assertIn("Markdown", text)
                self.assertIn("line breaks", text)
                self.assertIn("long text", text)
                self.assertIn("summarize", text)
                self.assertIn("rewrite", text)
                self.assertIn("truncate", text)
        self.assertIn("does not need those five fields", skill)
        self.assertIn("lacking the `BrainstormingContext` shape", prompt)
        self.assertIn("Plan approval is not Requirements approval", skill)

    def test_brainstorming_requires_separate_context_approval(self):
        text = (ROOT / "brainstorming" / "SKILL.md").read_text()
        self.assertIn("Selecting an approach records only `selectedApproach`", text)
        self.assertIn("it is not approval", text)
        self.assertIn("ask a separate approval question", text)
        self.assertIn("Only option 1 or an unambiguous affirmative answer", text)
        self.assertIn("Do not set `approved: true`", text)

    def test_fast_discussion_explicitly_recommends_an_approach(self):
        text = (ROOT / "fast" / "SKILL.md").read_text()
        self.assertIn("mark it as recommended", text)
        self.assertIn("explain the recommendation concisely", text)
        self.assertIn(
            "explicitly present the recommended implementation approach", text
        )
        self.assertIn("explain why it best fits", text)
        self.assertIn("Do not make the user infer the recommendation", text)
        self.assertIn("present the viable alternatives", text)
        self.assertIn("without forcing a three-approach comparison", text)

    def test_all_spec_task_checkboxes_keep_todo_marker_and_text(self):
        checkbox = re.compile(r"^\s*- \[[ xX]\] ")
        valid_task = re.compile(r"^\s*- \[[ xX]\] //TODO \S.+$")
        for path in (ROOT / "specs").glob("*/tasks.md"):
            for line_number, line in enumerate(path.read_text().splitlines(), start=1):
                if checkbox.match(line):
                    with self.subTest(path=path, line=line_number):
                        self.assertRegex(line, valid_task)


if __name__ == "__main__":
    unittest.main()
