"""Static routing and lifecycle contracts for executing-plan."""

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXECUTOR = (ROOT / "executing-plan" / "SKILL.md").read_text()
ROUTER = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
SHARED = (ROOT / "using-lazyspec" / "references" / "delivery-loop.md").read_text()


class ExecutingPlanContractTests(unittest.TestCase):
    def test_registered_and_routed_as_sole_executor(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("./executing-plan", manifest["skills"])
        self.assertNotIn("./fast", manifest["skills"])
        self.assertNotIn("./writing-plan", manifest["skills"])
        self.assertIn("../executing-plan/SKILL.md", ROUTER)
        self.assertIn("route to `executing-plan`", ROUTER)
        self.assertIn("execution and delivery finalization by `executing-plan/SKILL.md`", SHARED)

    def test_execution_strategy_and_verification_boundary(self):
        for rule in (
            "all currently unchecked TODOs",
            "without per-TODO confirmation",
            "feature branch",
            "lightweight basic check",
            "Do not run the full test suite or force a Red-Green TDD cycle on each individual TODO",
            "Only after the TODO passes its basic check",
            "checkbox token from `[ ]` to `[x]`",
            "preserve `//TODO` and every character after it",
            "Feature Verification (Full Test Suite)",
            "After all TODOs are completed, run the full test suite",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)

    def test_automatic_delivery_finalization(self):
        for rule in (
            "Automatic Delivery Finalization",
            "status: delivered",
            "delivered_at:",
            "Collapse the Execution Scaffolding",
            "Delete the entire `## 任务` section",
            "Bidirectional Supersession Sync",
            "status: superseded",
            "superseded_by:",
            "[!WARNING]",
            "no `//TODO`",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)


    def test_worktree_and_commit_discipline_contract(self):
        for rule in (
            "Worktree & Branch Setup",
            "spec_state.py worktree add",
            "--base dev",
            "First Commit (Spec Baseline)",
            "docs(spec): add approved specification for",
            "Task Implementation, Basic Check & Commit",
            "User Review Gate",
            "Merge to dev",
            "git merge --no-ff",
            "Worktree Cleanup",
            "spec_state.py worktree remove",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)


if __name__ == "__main__":
    unittest.main()
