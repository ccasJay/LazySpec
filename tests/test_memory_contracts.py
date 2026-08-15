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
    for line in path.read_text().splitlines():
        if not line.startswith("| project-memory/features/"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows[cells[0]] = {
            "summary": cells[1],
            "tags": cells[2],
            "status": cells[3],
            "source_spec": cells[4],
        }
    return rows


class MemorySkillContractTests(unittest.TestCase):
    def test_skill_structure_and_frontmatter(self):
        skill_path = SKILL_ROOT / "SKILL.md"
        self.assertTrue(skill_path.is_file())
        self.assertTrue((SKILL_ROOT / "agents" / "openai.yaml").is_file())
        self.assertTrue(
            (SKILL_ROOT / "references" / "memory-format.md").is_file()
        )

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

    def test_openai_interface_matches_skill(self):
        text = (SKILL_ROOT / "agents" / "openai.yaml").read_text()
        self.assertIn('display_name: "Distill Spec Memory"', text)
        self.assertIn(
            'short_description: "Distill completed feature specs into project memory"',
            text,
        )
        self.assertIn("$distill-spec-memory", text)
        self.assertNotIn("icon_", text)
        self.assertNotIn("brand_color", text)

    def test_plugin_and_router_register_memory_skill(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertIn("./distill-spec-memory", manifest["skills"])
        self.assertEqual(len(manifest["skills"]), len(set(manifest["skills"])))

        routing = (ROOT / "using-lazyspec" / "SKILL.md").read_text()
        self.assertIn("`lazyspec:distill-spec-memory`", routing)
        self.assertIn("`../distill-spec-memory/SKILL.md`", routing)
        self.assertIn("only when the user explicitly asks", routing)
        self.assertIn("Do not infer a distillation request", routing)

    def test_memory_format_contract(self):
        text = (SKILL_ROOT / "references" / "memory-format.md").read_text()
        for required in (
            "project-memory/index.md",
            "project-memory/features/<feature-name>.md",
            "feature: <feature-name>",
            "status: active",
            "source_spec: specs/<feature-name>/",
            "distilled_at: YYYY-MM-DD",
            "tags: [<tag>]",
            "supersedes: []",
            "superseded_by: []",
            'status_reason: ""',
            "## Capability",
            "## Durable Decisions",
            "## Contracts and Invariants",
            "## Lessons",
            "## Reuse Triggers",
            "## Sources",
            "| Memory | Summary | Tags | Status | Source Spec |",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

        for status in ("active", "needs-review", "superseded", "obsolete"):
            self.assertIn(f"`{status}`", text)

        self.assertIn("project-root-relative", text)
        self.assertIn("no `topics/`, `sessions/`", text)
        self.assertIn("JSON index", text)
        self.assertIn("never copy complete sections", text)

    def test_completion_gate_requires_all_evidence_and_zero_write(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        for required in (
            "## Completion Gate",
            "requirements.md`, `design.md`, and `tasks.md`",
            "Read each file completely",
            "including nested checkboxes",
            "Every checkbox must be `[x]` or `[X]`",
            "current, attributable pass result",
            "separate, explicit confirmation",
            "Do not create `project-memory/`",
            "any `draft`/temporary Memory file",
            "Existing Memory must remain untouched",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_reconciliation_uses_session_evidence_matrix_and_blocks_gaps(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        for required in (
            "## Reconciliation and Evidence Matrix",
            "read the complete Requirements, Design, and Tasks again",
            "| Claim | Spec anchors | Implementation evidence | Test evidence | User ruling | Result |",
            "at least one approved intent anchor",
            "one observable implementation or test source",
            "Keep this matrix in the conversation only",
            "Mark the claim `conflict`",
            "mark the claim `insufficient`",
            "stop before preview generation",
            "Never downgrade an unsupported claim",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_deduplication_checks_only_relevant_capsules_and_stops_on_conflict(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        for required in (
            "## Deduplication and Conflict Check",
            "inspect `project-memory/index.md` if it exists",
            "select only Capsules whose feature, tags, source Spec, or summary can overlap",
            "Do not scan every Capsule",
            "An existing Capsule for the same Feature is an existing result",
            "potential duplicate or conflict",
            "do not silently merge, overwrite, or choose precedence",
            "index is malformed",
            "index and Capsule metadata disagree",
            "stop before preview and write nothing",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_gate_scenario_matrix_names_all_required_blocking_cases(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        scenarios = (
            "missing, unreadable, or truncated file",
            "remaining `[ ]`",
            "missing evidence",
            "ambiguous “done”",
            "they disagree",
            "evidence is absent, unreachable, stale",
            "potential duplicate or conflict",
            "index is malformed",
        )
        for scenario in scenarios:
            with self.subTest(scenario=scenario):
                self.assertIn(scenario, text)

    def test_preview_approval_loop_and_logical_write_set_contract(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        for required in (
            "## Preview, Approval, and Write Protocol",
            "The preview is the approval object",
            "the full candidate Capsule",
            "the exact `index.md` row",
            "every Capsule and index status transition",
            "the complete logical write set",
            "If the user requests any change",
            "ask again",
            "Never create a draft, staging Memory, or second index",
            "one logical write set",
            "partial write",
            "do not claim success",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

    def test_status_invariants_and_transitions_contract(self):
        text = (SKILL_ROOT / "SKILL.md").read_text()
        reference = (SKILL_ROOT / "references" / "memory-format.md").read_text()
        for required in (
            "active",
            "needs-review",
            "superseded",
            "obsolete",
            "status_reason",
            "superseded_by",
            "supersedes",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)
                self.assertIn(required, reference)
        for required in (
            "A status in a Capsule and its index row must always match",
            "Use only these intentional transitions",
            "Do not reactivate a `superseded` or `obsolete` conclusion",
            "freeze everything after the frontmatter closing marker",
        ):
            with self.subTest(document="skill", required=required):
                self.assertIn(required, text)
        for required in (
            "The Capsule frontmatter status and its index row status must be identical",
            "Allowed transitions are `active → needs-review`",
            "`superseded` and `obsolete` are terminal",
            "the body after the frontmatter closing marker is immutable",
        ):
            with self.subTest(document="reference", required=required):
                self.assertIn(required, reference)

    def test_fixture_capsule_and_index_statuses_stay_in_sync(self):
        rows = index_rows(FIXTURE_ROOT / "index.md")
        capsule_paths = sorted((FIXTURE_ROOT / "features").glob("*.md"))
        self.assertEqual(
            set(rows),
            {f"project-memory/features/{path.name}" for path in capsule_paths},
        )
        for path in capsule_paths:
            fields, _ = read_frontmatter(path)
            row = rows[f"project-memory/features/{path.name}"]
            with self.subTest(path=path):
                self.assertEqual(fields["status"], row["status"])
                self.assertEqual(fields["source_spec"], row["source_spec"])
                if fields["status"] == "active":
                    self.assertEqual(fields["status_reason"], '""')
                else:
                    self.assertNotEqual(fields["status_reason"], '""')

    def test_fixture_supersession_is_bidirectional_and_non_active_is_excluded(self):
        rows = index_rows(FIXTURE_ROOT / "index.md")
        old_fields, _ = read_frontmatter(FIXTURE_ROOT / "features" / "memory-v1.md")
        new_fields, _ = read_frontmatter(FIXTURE_ROOT / "features" / "memory-v2.md")
        self.assertEqual(old_fields["status"], "superseded")
        self.assertEqual(
            old_fields["superseded_by"],
            "[project-memory/features/memory-v2.md]",
        )
        self.assertEqual(new_fields["status"], "active")
        self.assertEqual(
            new_fields["supersedes"],
            "[project-memory/features/memory-v1.md]",
        )
        self.assertEqual(rows["project-memory/features/memory-v1.md"]["status"], "superseded")
        self.assertEqual(rows["project-memory/features/memory-v2.md"]["status"], "active")
        default_paths = [path for path, row in rows.items() if row["status"] == "active"]
        self.assertEqual(default_paths, ["project-memory/features/memory-v2.md"])

    def test_fixture_status_only_update_preserves_capsule_body(self):
        path = FIXTURE_ROOT / "features" / "memory-v1.md"
        fields, body = read_frontmatter(path)
        updated = path.read_text().replace("status: superseded", "status: obsolete", 1)
        updated_path = FIXTURE_ROOT / "features" / "memory-v1-status-only.md"
        updated_path.write_text(updated)
        try:
            updated_fields, updated_body = read_frontmatter(updated_path)
            self.assertEqual(fields["status"], "superseded")
            self.assertEqual(updated_fields["status"], "obsolete")
            self.assertEqual(body, updated_body)
        finally:
            updated_path.unlink()

    def test_using_lazyspec_recall_protocol_is_bounded_and_non_blocking(self):
        text = (ROUTER_ROOT / "SKILL.md").read_text()
        for required in (
            "### Memory Recall Routing",
            "after binding `ACTIVE_PROJECT_ROOT` and before selecting the phase Skill",
            "Check only `ACTIVE_PROJECT_ROOT/project-memory/index.md`",
            "If it does not exist, use an empty context",
            "Do not create an index or scan `project-memory/features/` as a fallback",
            "header, columns, path, or status is malformed",
            "absolute paths",
            "`..` traversal",
            "paths outside `project-memory/features/`",
            "only rows whose index status is `active`",
            "at most three",
            "remaining matches were omitted",
            "interface RelevantMemoryContext",
            "readonly memories",
            "readonly sourceSpec",
            "readonly relevantSections",
            'readonly status: "active"',
            "If there is no related valid `active` row, use an empty context",
            "needs-review`, `superseded`, or `obsolete`",
            "not current facts",
            "Never place a non-`active` item in `memories`",
            "must not approve a phase",
            "reorder Brainstorming → Requirements → Design → Tasks",
            "one-task execution boundary",
            "is never a phase error",
        ):
            with self.subTest(required=required):
                self.assertIn(required, text)

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
        self.assertNotIn("project-memory/features/review-memory.md", active[:3])


if __name__ == "__main__":
    unittest.main()
