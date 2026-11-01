import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V2_SKILLS = (
    "writing-spec",
    "executing-plan",
    "distill-feature",
    "maintain-memory",
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
        for name in ("writing-spec",):
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

        for name in ("writing-spec",):
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
        planning = (ROOT / "writing-spec" / "SKILL.md").read_text()
        self.assertIn("all currently unchecked TODOs", execution)
        self.assertIn("Feature Verification", delivery)
        self.assertIn("Automatic Delivery Finalization", execution)
        self.assertIn("status: delivered", execution)
        self.assertIn("checkbox token from `[ ]` to `[x]`", execution)
        self.assertIn("//TODO", execution)
        self.assertIn("[spec-template.md](spec-template.md)", planning)
        self.assertIn("//TODO", (ROOT / "writing-spec/spec-template.md").read_text())

    def test_downstream_approval_and_single_artifact_boundaries(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        policy = (
            ROOT / "using-lazyspec" / "references" / "approval-policy.md"
        ).read_text()
        spec = (ROOT / "writing-spec" / "SKILL.md").read_text()

        self.assertIn("The approved `spec.md` is the only planning artifact", routing)
        self.assertIn("`spec.md` → explicit Spec approval → execution", policy)
        self.assertIn("Await explicit approval before handoff to `executing-plan`", spec)
        self.assertIn("Only an explicit approval in the current conversation", policy)
        self.assertIn("A material change invalidates the prior approval", policy)
        self.assertIn("`spec.md` uses the complete saved document as its approval object", policy)
        self.assertIn("Require explicit approval of `spec.md` before routing to execution", spec)


if __name__ == "__main__":
    unittest.main()
