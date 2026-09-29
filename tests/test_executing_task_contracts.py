"""Static routing and lifecycle contracts; scenario judgments still need human review."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXECUTOR = (ROOT / "executing-task" / "SKILL.md").read_text()
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
SHARED = (ROOT / "using-lazyspec" / "references" / "delivery-loop.md").read_text()


class ExecutingTaskContractTests(unittest.TestCase):
    def test_registered_and_routed_without_changing_fast_owner(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("./executing-task", manifest["skills"])
        self.assertIn("./fast", manifest["skills"])
        self.assertIn("../executing-task/SKILL.md", ROUTER)
        self.assertIn("verification-only requests, route to `executing-task`", ROUTER)
        self.assertIn("fast `plan.md` execution is owned by `fast/SKILL.md`", SHARED)

    def test_progressive_context_preserves_approval_and_full_coverage(self):
        for rule in (
            "Require explicit approval of the current Requirements, Design, and Tasks",
            "`审批摘要`",
            "complete `tasks.md` checklist and Planned Checks",
            "follow every linked acceptance criterion",
            "find the Design decisions and sections",
            "relevant source, callers, tests, and project instructions",
            "Expand to other Spec sections or code when the change crosses tasks",
            "Before claiming Feature Verification `passed`, inspect any still-uncovered contract sections",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)

    def test_full_and_selected_scope_keep_todo_text_and_verification_boundary(self):
        for rule in (
            "all currently unchecked TODOs, including nested TODOs",
            "one TODO number covers only that TODO and its children",
            "Only after the TODO passes, change its checkbox token from `[ ]` to `[x]`",
            "preserve `//TODO` and every character after it",
            "After all feature TODOs are checked, run Feature Verification",
            "A partial execution reports only its authorized subset",
            "verification-only request may run checks and update Feature Verification, but does not authorize implementation repairs",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)

    def test_progress_record_is_local_reconciled_and_conditionally_deleted(self):
        ignore_lines = (ROOT / ".gitignore").read_text().splitlines()
        self.assertEqual(1, ignore_lines.count("specs/**/.execution-progress.md"))
        for rule in (
            "Create it after branch selection and before TODO work or Feature Verification",
            "verification-only request with no existing file does not create one",
            "Never stage or commit it",
            "branch, HEAD, current Requirements/Design/Tasks content fingerprints",
            "compare the recorded scope, branch, HEAD, fingerprints, TODO states, and evidence",
            "If the branch differs, locate the authorized work",
            "If the contract changed, apply approval-policy.md's materiality rules and invalidate affected evidence",
            "Reconstruct or correct stale entries before continuing",
            "never mark a TODO complete, reuse verification, or claim approval solely from this file",
            "partial completion, failure, `blocked`, `pending-human`, interruption",
            "Delete only this file when every feature TODO is checked",
            "status `passed` and freshness `current`",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)

    def test_scenario_review_set_covers_requested_boundaries(self):
        cases = json.loads((ROOT / "tests/fixtures/executing-task/scenarios.json").read_text())
        self.assertEqual(8, len(cases))
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        headings = re.findall(r"^## (.+)$", EXECUTOR, re.M)
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertIn(case["section"], headings)
                self.assertTrue(case["facts"] and case["expected"])


if __name__ == "__main__":
    unittest.main()
