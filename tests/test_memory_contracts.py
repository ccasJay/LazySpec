import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / "distill-spec-memory"
ROUTER_ROOT = ROOT / "using-lazyspec"
FIXTURE_ROOT = ROOT / "tests" / "fixtures" / "project-memory"


def read_frontmatter(path):
    text = path.read_text()
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise AssertionError(f"fixture has no frontmatter: {path}")
    fields = {}
    for line in match.group(1).splitlines():
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()
    return fields, text[match.end() :]


def index_rows(path):
    rows = {}
    link = re.compile(r"^\[([^]]+)\]\([^)]+\)$")
    for line in path.read_text().splitlines():
        if not line.startswith(("| [project-memory/features/", "| [project-memory/learnings/")):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        memory_match = link.match(cells[0])
        source_match = link.match(cells[4])
        if memory_match is None or source_match is None:
            raise AssertionError(f"fixture row has invalid links: {line}")
        rows[memory_match.group(1)] = {
            "summary": cells[1],
            "tags": cells[2],
            "status": cells[3],
            "source_spec": source_match.group(1),
            "reviewed_at": cells[5],
        }
    return rows


class MemorySkillContractTests(unittest.TestCase):
    def test_skill_structure_frontmatter_and_interface(self):
        skill_path = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        self.assertTrue((SKILL_ROOT / "agents" / "openai.yaml").is_file())
        self.assertTrue((SKILL_ROOT / "references" / "memory-format.md").is_file())

        text = skill_path.read_text()
        match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
        self.assertIsNotNone(match)
        keys = {
            line.split(":", 1)[0]
            for line in match.group(1).splitlines()
            if ":" in line
        }
        self.assertEqual({"name", "description"}, keys)
        self.assertIn("name: distill-spec-memory", match.group(1))
        self.assertNotIn("TODO", text)

        interface = (SKILL_ROOT / "agents" / "openai.yaml").read_text()
        self.assertIn('display_name: "Distill Spec Memory"', interface)
        self.assertIn(
            'short_description: "Distill and maintain verified project memory"',
            interface,
        )
        self.assertIn("$distill-spec-memory", interface)
        self.assertNotIn("icon_", interface)
        self.assertNotIn("brand_color", interface)

    def test_plugin_and_router_register_memory_skill(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("./distill-spec-memory", manifest["skills"])
        self.assertEqual(len(manifest["skills"]), len(set(manifest["skills"])))

        routing = (ROUTER_ROOT / "SKILL.md").read_text()
        self.assertIn("`lazyspec:distill-spec-memory`", routing)
        self.assertIn("`../distill-spec-memory/SKILL.md`", routing)
        self.assertIn("only when the user explicitly asks", routing)
        self.assertIn("Do not infer a distillation request", routing)

    def test_memory_format_defines_current_maintainable_capsules(self):
        text = (SKILL_ROOT / "references" / "memory-format.md").read_text()
        for required in (
            "project-memory/index.md",
            "project-memory/features/<feature-name>.md",
            "feature: <feature-name>",
            "status: active",
            'summary: "<short routing summary>"',
            "source_spec: specs/<feature-name>/",
            "distilled_at: YYYY-MM-DD",
            "reviewed_at: YYYY-MM-DD",
            "tags: [<stable-tag>]",
            "authorities: [<current-architecture-or-source-path>]",
            "## Purpose",
            "## Durable Decisions",
            "- D1 —",
            "## Guardrails",
            "## Revisit When",
            "## Sources",
            "| Memory | Summary | Tags | Status | Source Spec | Reviewed |",
            "Active and needs-review bodies may change",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

        for status in ("active", "needs-review", "superseded", "obsolete"):
            self.assertIn(f"`{status}`", text)
        self.assertIn("project-root-relative", text)
        self.assertIn("JSON index", text)
        self.assertIn("completed-checkbox Specs", text)

    def test_skill_loads_local_contract_before_fallback(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        local = "ACTIVE_PROJECT_ROOT/project-memory/README.md"
        fallback = "references/memory-format.md"
        self.assertIn(local, text)
        self.assertIn(fallback, text)
        self.assertLess(text.index(local), text.index(fallback))
        self.assertIn("follow the local contract", text)

    def test_gate_requires_complete_current_evidence_and_zero_write(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        for required in (
            "## Gate before preview",
            "requirements.md`, `design.md`, and `tasks.md`",
            "including nested checkboxes",
            "every task checkbox",
            "current, attributable results",
            "explicit confirmation",
            "write nothing under `project-memory/`",
            "relevant implementation has uncommitted changes",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_evidence_matrix_and_single_owner_rules(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        for required in (
            "## Build an evidence matrix",
            "| Claim | Spec anchors | Implementation evidence | Test evidence | Existing owner | Result |",
            "at least one approved Spec anchor",
            "Stop on a material conflict",
            "## Select one owner for each decision",
            "Keep one active owner",
            "same Feature",
            "preserves `distilled_at`",
            "updates `reviewed_at`",
            "include the affected Capsule revision or status transition in the same preview",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_preview_write_and_status_contracts(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        for required in (
            "## Preview and approval",
            "The preview artifact is the approval object",
            "outside `ACTIVE_PROJECT_ROOT/project-memory/`",
            "concise 1–3 sentence summary",
            "approve that exact preview artifact",
            "content hash or stable identifier",
            "every complete proposed Capsule",
            "complete generated index",
            "complete project-root-relative logical write set",
            "Any requested edit invalidates the previous approval",
            "## Write and verify atomically",
            "project-local index generator",
            "project-local Memory validator",
            "partial writes",
            "Allow `active → active` maintenance",
            "Do not reactivate terminal Capsules",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_fixture_capsule_and_generated_index_stay_in_sync(self):
        rows = index_rows(FIXTURE_ROOT / "index.md")
        capsule_paths = sorted((FIXTURE_ROOT / "features").glob("*.md"))
        self.assertEqual(
            set(rows),
            {f"project-memory/features/{path.name}" for path in capsule_paths},
        )
        for path in capsule_paths:
            fields, body = read_frontmatter(path)
            row = rows[f"project-memory/features/{path.name}"]
            with self.subTest(path=path):
                self.assertEqual(fields["status"], row["status"])
                self.assertEqual(fields["source_spec"], row["source_spec"])
                self.assertEqual(fields["reviewed_at"], row["reviewed_at"])
                self.assertIn("summary", fields)
                self.assertIn("authorities", fields)
                self.assertIn("## Purpose", body)
                self.assertIn("## Revisit When", body)
                if fields["status"] == "active":
                    self.assertNotIn("status_reason", fields)
                    self.assertNotIn("superseded_by", fields)
                else:
                    self.assertNotEqual(fields["status_reason"], '""')

    def test_fixture_supersession_is_bidirectional_and_non_active_is_excluded(self):
        rows = index_rows(FIXTURE_ROOT / "index.md")
        old_fields, _ = read_frontmatter(FIXTURE_ROOT / "features" / "memory-v1.md")
        new_fields, _ = read_frontmatter(FIXTURE_ROOT / "features" / "memory-v2.md")
        self.assertEqual(
            old_fields["superseded_by"],
            "[project-memory/features/memory-v2.md]",
        )
        self.assertEqual(
            new_fields["supersedes"],
            "[project-memory/features/memory-v1.md]",
        )
        default_paths = [path for path, row in rows.items() if row["status"] == "active"]
        self.assertEqual(default_paths, ["project-memory/features/memory-v2.md"])

    def test_active_maintenance_updates_body_and_review_date(self):
        path = FIXTURE_ROOT / "features" / "memory-v2.md"
        fields, body = read_frontmatter(path)
        updated = path.read_text().replace("reviewed_at: 2026-08-18", "reviewed_at: 2026-08-19", 1)
        updated = updated.replace("current memory lifecycle", "maintained memory lifecycle", 1)
        match = re.match(r"\A---\n(.*?)\n---\n(.*)", updated, re.DOTALL)
        self.assertIsNotNone(match)
        self.assertEqual(fields["distilled_at"], "2026-08-15")
        self.assertIn("reviewed_at: 2026-08-19", match.group(1))
        self.assertNotEqual(body, match.group(2))

    def test_using_lazyspec_recall_is_bounded_advisory_and_authority_aware(self):
        text = (ROUTER_ROOT / "SKILL.md").read_text()
        for required in (
            "### Memory Recall Routing",
            "Check only `ACTIVE_PROJECT_ROOT/project-memory/index.md`",
            "generated six-column index header",
            "Markdown-linked rows",
            "only rows whose index status is `active`",
            "missing `reviewed_at` or `authorities`",
            "at most three",
            "readonly reviewedAt: string",
            "readonly authorities: readonly string[]",
            "read that current authority",
            "must not override current implementation evidence",
            "Never place a non-`active` item in `memories`",
            "user's explicit task scope",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_final_task_reports_memory_impact_without_writing(self):
        text = (ROUTER_ROOT / "SKILL.md").read_text()
        self.assertIn("When all requested TODOs are complete", text)
        self.assertIn("Report likely impact candidates", text)
        self.assertIn("do not create, edit, or re-status Memory", text)

    def test_recall_fixture_has_more_than_three_active_matches_and_history(self):
        rows = index_rows(FIXTURE_ROOT / "retrieval-index.md")
        active = [path for path, row in rows.items() if row["status"] == "active"]
        historical = [
            path
            for path, row in rows.items()
            if row["status"] in {"needs-review", "superseded", "obsolete"}
        ]
        self.assertGreater(len(active), 3)
        self.assertEqual(active[:3], sorted(active)[:3])
        self.assertEqual(historical, ["project-memory/features/review-memory.md"])


if __name__ == "__main__":
    unittest.main()
