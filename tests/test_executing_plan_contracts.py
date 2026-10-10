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
    def test_registered_and_routed_without_changing_fast_owner(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("./executing-plan", manifest["skills"])
        self.assertIn("./fast", manifest["skills"])
        self.assertIn("../executing-plan/SKILL.md", ROUTER)
        self.assertIn("route to `executing-plan`", ROUTER)
        self.assertIn("fast `plan.md` execution is owned by `fast/SKILL.md`", SHARED)

    def test_execution_strategy_and_verification_boundary(self):
        for rule in (
            "all currently unchecked TODOs",
            "without per-TODO confirmation",
            "feature branch",
            "Only after the TODO passes",
            "change its checkbox token from `[ ]` to `[x]`",
            "Preserve `//TODO` and every character after it",
            "Feature Verification",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)

    def test_automatic_delivery_finalization(self):
        for rule in (
            "Automatic Delivery Finalization",
            "status: delivered",
            "delivered_at:",
            "Cleanses proposal/hypothetical phrasing",
            "Decision",
            "Bidirectional Supersession Sync",
            "status: superseded",
            "superseded_by:",
            "[!WARNING]",
        ):
            with self.subTest(rule=rule):
                self.assertIn(rule, EXECUTOR)


if __name__ == "__main__":
    unittest.main()
