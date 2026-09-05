"""Artifact/contract lint and synthetic examples, not an Agent execution simulator.

scenarios.json is the manual decision-review suite. Its expected answers are not
executed by these tests; an actual model evaluation is a separate activity.
"""

import copy
import json
import re
import unittest
from pathlib import Path

from test_memory_contracts import index_rows, read_frontmatter


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
    if expected == "passed" and report["risk"] == "high" and not report["human_acceptance"]:
        expected = "pending-human"
    if report["status"] != expected:
        raise ValueError("unsupported aggregate success")
    return report["status"] == "passed" and report["freshness"] == "current"


class DeliveryContractTests(unittest.TestCase):
    def test_shared_references_resolve_from_every_installed_skill(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        self.assertEqual(7, len(manifest["skills"]))
        for directory in manifest["skills"]:
            skill = ROOT / directory / "SKILL.md"
            links = re.findall(r"\]\(([^)]+risk-policy\.md)\)", skill.read_text())
            self.assertEqual(1, len(links), skill)
            self.assertEqual((POLICIES / "risk-policy.md").resolve(), (skill.parent / links[0]).resolve())
        for directory in ("using-lazyspec", "fast", "writing-task"):
            skill = ROOT / directory / "SKILL.md"
            link, = re.findall(r"\]\(([^)]+delivery-loop\.md)\)", skill.read_text())
            self.assertEqual((POLICIES / "delivery-loop.md").resolve(), (skill.parent / link).resolve())

    def test_policy_tables_have_all_levels_and_failure_destinations(self):
        risk = (POLICIES / "risk-policy.md").read_text()
        rows = [line.split("|")[1:-1] for line in risk.splitlines() if re.match(r"\| (low|medium|high) \|", line)]
        self.assertEqual(["low", "medium", "high"], [r[0].strip() for r in rows])
        self.assertTrue(all(len(row) == 4 for row in rows))
        delivery = (POLICIES / "delivery-loop.md").read_text()
        rows = [line.split("|")[1:-1] for line in delivery.splitlines() if line.startswith("| ")][1:]
        self.assertEqual(
            ["Current execution task", "Tasks", "Design", "Requirements", "Current stage"],
            [row[1].strip() for row in rows],
        )

    def test_scenario_suite_references_real_rules(self):
        cases = json.loads((FIXTURES / "delivery-loop/scenarios.json").read_text())
        self.assertEqual(len(cases), len({c["id"] for c in cases}))
        for case in cases:
            with self.subTest(case=case["id"]):
                self.assertTrue(case["facts"] and case["expected"])
                path, anchor = case["rule"].split("#")
                headings = re.findall(r"^## (.+)$", (POLICIES / path).read_text(), re.M)
                self.assertIn(anchor, [re.sub(r"[^a-z0-9 -]", "", h.lower()).replace(" ", "-") for h in headings])

    def test_high_risk_report_requires_current_human_acceptance(self):
        report = json.loads((FIXTURES / "delivery-loop/verification.json").read_text())
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

    def test_mixed_index_keeps_legacy_capsule_and_learning_metadata(self):
        corpus = FIXTURES / "project-memory"
        rows = index_rows(corpus / "mixed-index.md")
        self.assertEqual(2, len(rows))
        kinds = []
        for path, row in rows.items():
            capsule = corpus / path.removeprefix("project-memory/")
            fields, body = read_frontmatter(capsule)
            kind = fields.get("kind", "feature")
            kinds.append(kind)
            self.assertEqual(kind + "s", capsule.parent.name)
            self.assertEqual(fields.get("feature", fields.get("learning")), capsule.stem)
            for key in ("status", "source_spec", "reviewed_at"):
                self.assertEqual(fields[key], row[key])
            self.assertEqual(fields["summary"].strip('"'), row["summary"])
            self.assertEqual(fields["tags"].strip("[]"), row["tags"])
            if kind == "learning":
                sections = re.findall(r"^## (.+)$", body, re.M)
                self.assertEqual(["Applicability", "Observation", "Validated Practice", "Limits", "Revisit When", "Sources"], sections)
                defined = set(re.findall(r"^- (S\d+):", body, re.M))
                cited = set(re.findall(r"S\d+", " ".join(re.findall(r"\[([^]]+)\]", body))))
                self.assertEqual(defined, cited)
                source_plan = corpus / fields["source_spec"] / "plan.md"
                self.assertIn("- [ ] //TODO", source_plan.read_text())
                self.assertFalse((source_plan.parent / "requirements.md").exists())
        self.assertEqual(["feature", "learning"], kinds)


if __name__ == "__main__":
    unittest.main()
