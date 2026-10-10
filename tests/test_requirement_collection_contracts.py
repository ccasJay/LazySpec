"""Static Skill contracts and manual-scenario integrity, not Agent behavior tests.

The scenario fixtures describe checks for a real interaction trace. These tests
do not execute their expected answers or claim that a model called a tool.
"""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec/SKILL.md").read_text()
SKILL = (ROOT / "writing-requirement/SKILL.md").read_text()
PROMPT = (ROOT / "writing-requirement/requirement-prompt.md").read_text()
POLICY = (ROOT / "using-lazyspec/references/approval-policy.md").read_text()
COLLECTION = SKILL.split("## Requirement Collection", 1)[1].split(
    "## Document Contract", 1
)[0]


class RequirementCollectionContractTests(unittest.TestCase):
    def test_manifest_registers_only_the_eight_remaining_skills(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        expected = {
            "using-lazyspec", "writing-spec", "writing-plan", "executing-plan",
            "distill-feature", "distill-learning", "maintain-memory",
            "writing-requirement", "writing-design",
            "writing-task", "executing-task", "distill-spec-memory",
            "fast", "orchestrating-specs",
        }
        self.assertEqual(expected, {Path(p).name for p in manifest["skills"]})
        self.assertEqual(len(expected), len(manifest["skills"]))

        self.assertFalse((ROOT / "brainstorming/SKILL.md").exists())
        self.assertFalse((ROOT / "using-lazyspec/references/codex-plan-mode.md").exists())

    def test_active_resources_do_not_depend_on_retired_inputs(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        paths = [ROOT / "README.md", ROOT / ".claude-plugin/plugin.json"]
        for directory in manifest["skills"]:
            paths.extend((ROOT / directory).rglob("*.md"))
        for path in paths:
            text = path.read_text().lower()
            for retired in (
                "brainstorming", "codex-plan", "codexplanartifact",
                "runtimemode", "brainstorminginput", "selectedapproach",
            ):
                with self.subTest(path=path, retired=retired):
                    self.assertNotIn(retired, text)

    def test_creation_and_revision_route_directly_to_requirements(self):
        chain = ROUTER.split("### Phase Chain", 1)[1].split("## Workflow Diagram", 1)[0]
        creation, revision = chain.split("\n2. ", 1)
        self.assertIn("route directly to `writing-requirement`", creation)
        self.assertIn("route directly to `writing-requirement`", revision)
        self.assertIn("No separate context approval", creation)
        self.assertIn("current tool and file-writing restrictions", creation)

    def test_every_new_requirement_must_be_asked_before_inclusion(self):
        self.assertIn("every requirement MUST be individually asked and explicitly confirmed before inclusion", COLLECTION)
        self.assertIn("even when the initial request or a supplied plan already describes it in detail", COLLECTION)
        self.assertIn("Do not batch multiple requirements into one tool call or conversation question", COLLECTION)
        self.assertNotIn("WITHOUT asking sequential questions first", SKILL)

    def test_collection_questions_keep_the_user_visible_target_concise(self):
        self.assertIn("what the requirement is and its concise target behavior", COLLECTION)
        self.assertIn("Do not show detailed acceptance criteria, formal user stories", COLLECTION)
        self.assertIn("plain-language Chinese by default", COLLECTION)
        self.assertIn("lead with the user-visible result", COLLECTION)
        self.assertIn("Leave architecture, data models, APIs", COLLECTION)
        self.assertIn("meaningful mutually exclusive options", COLLECTION)
        self.assertIn("focused free-text question when choices would be artificial", COLLECTION)
        self.assertIn("without omitting scope, constraints, risks, or success criteria", COLLECTION)

    def test_changed_rejected_and_ambiguous_answers_have_distinct_rules(self):
        self.assertIn("a clear replacement supplied by the user settles that behavior", COLLECTION)
        self.assertIn("Clarify an ambiguous answer or a new dependent choice before continuing", COLLECTION)
        self.assertIn("Exclude rejected requirements", COLLECTION)
        self.assertIn("Update remaining candidates from the answers", COLLECTION)
        self.assertIn("do not invent speculative requirements to meet a count", COLLECTION)

    def test_completion_answer_precedes_the_complete_draft(self):
        ordered = (
            "Propose one candidate requirement at a time",
            "Ask the user to confirm, modify, or reject",
            "ask whether the user has additional requirements",
            "Wait for explicit confirmation that collection is complete",
            "Only after collection is complete, draft and write",
        )
        positions = [COLLECTION.index(rule) for rule in ordered]
        self.assertEqual(sorted(positions), positions)
        self.assertIn("resume the same one-at-a-time exchange", COLLECTION)
        self.assertIn("Do not create or incrementally update it while collection is pending", COLLECTION)
        self.assertIn("do not create a collection file", SKILL)
        self.assertIn("Do not use this prompt to bypass collection or write an incremental draft", PROMPT)

    def test_revisions_confirm_behavior_changes_and_preserve_unchanged_requirements(self):
        self.assertIn("collect only additions, material behavior changes, and removals", COLLECTION)
        self.assertIn("Confirm a removal's effect before deleting", COLLECTION)
        self.assertIn("Preserve unchanged requirements and their anchors without asking again", COLLECTION)
        self.assertIn("For purely editorial revisions, skip this collection workflow", COLLECTION)
        self.assertIn("do not ask a collection-completion question", COLLECTION)
        self.assertIn("For purely editorial revisions, skip collection", PROMPT)
        self.assertIn("Purely editorial revisions preserve any still-valid prior document approval", SKILL)

    def test_elaboration_cannot_introduce_an_unconfirmed_material_choice(self):
        self.assertIn("Derive user stories and EARS criteria only from confirmed behavior", COLLECTION)
        self.assertIn("return to collection before writing the affected revision and reconfirm completion", COLLECTION)
        self.assertIn("return to SKILL.md's collection exchange before writing", PROMPT)
        self.assertIn("A supplied plan is ordinary background", PROMPT)
        self.assertIn("No separately approved input object", SKILL)

    def test_collection_answers_do_not_approve_the_document(self):
        self.assertIn("Confirming individual requirements or finishing collection does not approve the complete document", SKILL)
        self.assertIn("completing collection does not approve the complete Requirements document", POLICY)
        self.assertIn("explicit Requirements approval before creating any Design document", SKILL)

    def test_asking_policy_uses_capabilities_permissions_and_actual_schema(self):
        for rule in (
            "tool definitions exposed by the current agent environment",
            "capability-discovery mechanism",
            "documented ability to collect the user's answer",
            "current mode restrictions",
            "only fields supported by the selected tool",
            "it MUST be called",
            "a conversation question cannot substitute for that call",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, POLICY)
        self.assertIn("Follow approval-policy.md's `How to ask` protocol for every collection", SKILL)
        for name in ("AskUserQuestion", "request_user_input", "ask_user"):
            self.assertNotIn(name, POLICY)
            self.assertNotIn(name, SKILL)

    def test_unavailable_and_async_tools_do_not_skip_waiting_for_the_user(self):
        self.assertIn("If no applicable tool is available or permitted", POLICY)
        self.assertIn("explain the limitation briefly", POLICY)
        self.assertIn("stop while awaiting the answer", POLICY)
        self.assertIn("successful dispatch or a tool acknowledgment is not an answer", POLICY)
        self.assertIn("keep the question pending until the reply arrives", POLICY)
        self.assertIn("Silence, timeout, or a preselected option does not resolve the question", POLICY)

    def test_initial_risk_is_assessed_in_requirements_and_rechecked_in_design(self):
        risk = (ROOT / "using-lazyspec/references/risk-policy.md").read_text()
        self.assertIn("Requirements assesses the initial level during requirement collection", risk)
        self.assertIn("Design re-evaluates it", risk)
        self.assertIn("Assess the initial risk under risk-policy.md", COLLECTION)

    def test_manual_scenarios_reference_current_rules(self):
        cases = json.loads((ROOT / "tests/fixtures/requirement-collection/scenarios.json").read_text())
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["facts"] and case["expected"])
                path, anchor = case["rule"].split("#")
                headings = re.findall(r"^## (.+)$", (ROOT / path).read_text(), re.M)
                anchors = [h.lower().replace(" ", "-") for h in headings]
                self.assertIn(anchor, anchors)


if __name__ == "__main__":
    unittest.main()
