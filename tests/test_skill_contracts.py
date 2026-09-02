import json
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

    def test_approval_payloads_use_only_supported_fields(self):
        for path in WRITING_SKILLS:
            with self.subTest(path=path):
                text = path.read_text()
                self.assertNotIn("metadata.source", text)
                payloads = re.findall(r"```json\n(.*?)\n\s*```", text, re.DOTALL)
                self.assertEqual(1, len(payloads))
                payload = json.loads(payloads[0])
                self.assertEqual({"questions"}, payload.keys())
                self.assertEqual(1, len(payload["questions"]))
                question = payload["questions"][0]
                self.assertEqual(
                    {"question", "header", "options", "multiSelect"},
                    question.keys(),
                )
                self.assertEqual("Review", question["header"])
                self.assertFalse(question["multiSelect"])
                self.assertEqual(
                    ["Approve", "Request changes"],
                    [option["label"] for option in question["options"]],
                )
                for option in question["options"]:
                    self.assertEqual({"label", "description"}, option.keys())
                self.assertIn("equivalent user-question tool", text)
                self.assertIn("directly in the conversation", text)

    def test_task_execution_contract_batches_todos_on_feature_branch(self):
        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        planning = (ROOT / "writing-task" / "SKILL.md").read_text()
        self.assertIn("complete `requirements.md`, `design.md`, and `tasks.md`", routing)
        self.assertIn("all currently unchecked TODOs", routing)
        self.assertIn("without waiting for per-task approval", routing)
        self.assertIn("new feature branch", routing)
        self.assertIn("codex/<feature-name>", routing)
        self.assertIn("After each TODO passes its verification", routing)
        self.assertNotIn("Only focus on ONE user-selected task", routing)
        self.assertNotIn("If multiple tasks are requested, ask the user to select one", routing)
        for text in (routing, planning):
            self.assertIn("checkbox token from `[ ]` to `[x]`", text)
            self.assertIn("`//TODO`", text)

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
