"""Artifact/contract lint and synthetic examples, not an Agent execution simulator.

scenarios.json is the manual decision-review suite. Its expected answers are not
executed by these tests; an actual model evaluation is a separate activity.
"""

import copy
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICIES = ROOT / "using-lazyspec/references"
FIXTURES = ROOT / "tests/fixtures"


def lint_report(report):
    """Check the evidence invariants in a synthetic representation of a report."""
    for field in ("verified_at", "tested_commit", "contract_fingerprint"):
        if not report.get(field):
            raise ValueError(f"missing attribution: {field}")
    if report["freshness"] not in {"current", "stale"}:
        raise ValueError("invalid freshness")
    if report["risk"] not in {"low", "medium", "high"}:
        raise ValueError("invalid risk")
    statuses = {"passed", "failed", "blocked", "pending-human"}
    if report["status"] not in statuses:
        raise ValueError("invalid status")
    for change in report["uncommitted_changes"]:
        if not change.get("path") or not change.get("fingerprint"):
            raise ValueError("unattributable worktree")
    covered = set()
    for check in report["checks"]:
        if check["status"] not in statuses:
            raise ValueError("skipped is not passed")
        if not all(check.get(key) for key in ("expected", "actual", "evidence")):
            raise ValueError("missing behavioral evidence")
        covered.update(check["outcomes"])
    if covered != set(report["required_outcomes"]):
        raise ValueError("acceptance coverage gap")
    states = {check["status"] for check in report["checks"]}
    expected = next((s for s in ("failed", "blocked", "pending-human") if s in states), "passed")
    if expected == "passed" and report["human_acceptance_required"] and not report["human_acceptance"]:
        expected = "pending-human"
    if report["status"] != expected:
        raise ValueError("unsupported aggregate success")
    return report["status"] == "passed" and report["freshness"] == "current"


class DeliveryContractTests(unittest.TestCase):
    def test_shared_references_resolve_from_every_installed_skill(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(8, len(manifest["skills"]))
        risk_readers = [
            d for d in manifest["skills"]
            if not any(d.endswith(suffix) for suffix in (
                "distill-feature", "maintain-memory"
            ))
        ]
        for directory in risk_readers:
            skill = ROOT / directory / "SKILL.md"
            links = re.findall(r"\]\(([^)]+risk-policy\.md)\)", skill.read_text())
            self.assertEqual(1, len(links), skill)
            self.assertEqual((POLICIES / "risk-policy.md").resolve(), (skill.parent / links[0]).resolve())
            approval = re.findall(r"\]\(([^)]+approval-policy\.md)\)", skill.read_text())
            self.assertEqual(1, len(approval), skill)
            self.assertEqual((POLICIES / "approval-policy.md").resolve(), (skill.parent / approval[0]).resolve())
        for distill_name in ("distill-feature", "maintain-memory"):
            distill = (ROOT / distill_name / "SKILL.md").read_text()
            self.assertEqual([], re.findall(r"\]\(([^)]+risk-policy\.md)\)", distill))
            approval_links = re.findall(r"\]\(([^)]+approval-policy\.md)\)", distill)
            if approval_links:
                self.assertEqual((POLICIES / "approval-policy.md").resolve(), (ROOT / distill_name / approval_links[0]).resolve())
        for directory in ("using-lazyspec", "fast", "writing-plan", "executing-plan", "orchestrating-specs"):
            skill = ROOT / directory / "SKILL.md"
            links = re.findall(r"\]\(([^)]+delivery-loop\.md)\)", skill.read_text())
            self.assertGreaterEqual(len(links), 1, skill)
            for link in links:
                self.assertEqual((POLICIES / "delivery-loop.md").resolve(), (skill.parent / link).resolve())


    def test_policy_tables_have_all_levels_and_failure_destinations(self):
        risk = (POLICIES / "risk-policy.md").read_text()
        rows = [line.split("|")[1:-1] for line in risk.splitlines() if re.match(r"\| (low|medium|high) \|", line)]
        self.assertEqual(["low", "medium", "high"], [r[0].strip() for r in rows])
        self.assertTrue(all(len(row) == 4 for row in rows))
        delivery = (POLICIES / "delivery-loop.md").read_text()
        rows = [line.split("|")[1:-1] for line in delivery.splitlines() if line.startswith("| ")][1:]
        self.assertEqual(
            ["Current execution task", "Plan (`plan.md`)", "Spec (`spec.md`)", "Current stage"],
            [row[1].strip() for row in rows],
        )

    def test_scenario_suite_references_real_rules(self):
        for suite in ("delivery-loop", "requirement-collection"):
            cases = json.loads((FIXTURES / suite / "scenarios.json").read_text())
            self.assertEqual(len(cases), len({c["id"] for c in cases}))
            for case in cases:
                with self.subTest(suite=suite, case=case["id"]):
                    self.assertTrue(case["facts"] and case["expected"])
                    path, anchor = case["rule"].split("#")
                    source = (POLICIES if suite == "delivery-loop" else ROOT) / path
                    headings = re.findall(r"^## (.+)$", source.read_text(), re.M)
                    self.assertIn(anchor, [re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-") for h in headings])

    def test_required_human_acceptance_is_independent_of_risk_level(self):
        report = json.loads((FIXTURES / "delivery-loop/verification.json").read_text())
        self.assertFalse(lint_report(report))
        automatic = copy.deepcopy(report)
        automatic["human_acceptance_required"] = False
        automatic["status"] = "passed"
        self.assertTrue(lint_report(automatic))
        report["risk"] = "low"
        self.assertFalse(lint_report(report))
        report["human_acceptance"] = True
        report["status"] = "passed"
        self.assertTrue(lint_report(report))
        report["freshness"] = "stale"
        self.assertFalse(lint_report(report))

    def test_bad_reports_cannot_claim_current_success(self):
        original = json.loads((FIXTURES / "delivery-loop/verification.json").read_text())
        mutations = [
            lambda r: r.update(status="passed"),
            lambda r: r["checks"].pop(),
            lambda r: r["checks"][0].update(evidence=""),
            lambda r: r["checks"][0].update(actual=""),
            lambda r: r["checks"][0].update(status="skipped"),
            lambda r: r.update(tested_commit=""),
            lambda r: r.update(uncommitted_changes=[{"path": "src/example"}]),
        ]
        for mutation in mutations:
            report = copy.deepcopy(original)
            mutation(report)
            with self.subTest(report=report), self.assertRaises(ValueError):
                lint_report(report)

    def test_failed_and_blocked_checks_are_not_human_pending(self):
        original = json.loads((FIXTURES / "delivery-loop/verification.json").read_text())
        for status in ("failed", "blocked"):
            report = copy.deepcopy(original)
            report["checks"][0]["status"] = status
            report["status"] = status
            self.assertFalse(lint_report(report))


if __name__ == "__main__":
    unittest.main()
