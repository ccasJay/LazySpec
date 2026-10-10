import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V2_SKILLS = (
    "writing-spec",
    "writing-plan",
    "executing-plan",
    "distill-feature",
    "distill-learning",
    "maintain-memory",
    "fast",
    "orchestrating-specs",
)


class SkillContractTests(unittest.TestCase):
    def test_registered_routing_has_sibling_fallbacks(self):
        text = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        for name in V2_SKILLS:
            self.assertIn(f"`lazyspec:{name}`", text)
            self.assertIn(f"`../{name}/SKILL.md`", text)
        self.assertIn("relative to this `using-lazyspec/SKILL.md`", text)

    def test_writing_resources_are_skill_relative(self):
        for name in ("writing-spec", "writing-plan"):
            path = ROOT / name / "SKILL.md"
            with self.subTest(path=path):
                text = path.read_text()
                self.assertIn("relative to the directory containing this `SKILL.md`", text)
                self.assertIn("ACTIVE_PROJECT_ROOT", text)
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
        self.assertIn("tool definitions exposed by the current agent environment", policy)
        self.assertIn("Do not require a particular tool name", policy)
        self.assertIn("only fields supported by the selected tool", policy)
        self.assertIn("single-choice question", policy)
        self.assertIn("`Approve` and `Request changes` meanings", policy)
        self.assertIn("directly in the conversation", policy)
        self.assertNotIn("AskUserQuestion", policy)
        self.assertNotIn("```json", policy)

        for name in ("writing-spec", "writing-plan"):
            path = ROOT / name / "SKILL.md"
            with self.subTest(path=path):
                text = path.read_text()
                self.assertNotIn("metadata.source", text)
                self.assertEqual(0, len(re.findall(r"```json\n", text)))
                self.assertIn("approval-policy.md", text)

    def test_task_execution_contract_in_executing_plan(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        delivery = (
            ROOT / "using-lazyspec" / "references" / "delivery-loop.md"
        ).read_text()
        execution = (ROOT / "executing-plan" / "SKILL.md").read_text()
        planning = (ROOT / "writing-plan" / "SKILL.md").read_text()
        self.assertIn("all currently unchecked TODOs", execution)
        self.assertIn("Feature Verification", delivery)
        self.assertIn("Automatic Delivery Finalization", execution)
        self.assertIn("status: delivered", execution)
        self.assertIn("checkbox token from `[ ]` to `[x]`", execution)
        self.assertIn("//TODO", execution)
        self.assertIn("//TODO", planning)

    def test_downstream_approval_and_binary_boundaries(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        policy = (
            ROOT / "using-lazyspec" / "references" / "approval-policy.md"
        ).read_text()
        spec = (ROOT / "writing-spec" / "SKILL.md").read_text()
        plan = (ROOT / "writing-plan" / "SKILL.md").read_text()

        self.assertIn("`spec.md` and `plan.md` separately in that order", routing)
        self.assertIn("Await explicit approval before transitioning to `writing-plan`", spec)
        self.assertIn("Only an explicit approval in the current conversation", policy)
        self.assertIn("A material change invalidates the prior approval", policy)
        self.assertIn("`spec.md` and `plan.md` each use the complete saved phase document as their approval object", policy)
        self.assertIn("Require explicit approval of `spec.md` before creating `plan.md`", plan)

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


if __name__ == "__main__":
    unittest.main()
