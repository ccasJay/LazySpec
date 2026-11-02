"""Behavioral tests for the deterministic LazySpec scripts."""

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "specs"
CORE = ROOT / "using-lazyspec" / "scripts"
sys.path.insert(0, str(CORE))

from lazyspec_core import memory, scan  # noqa: E402
from lazyspec_core.checks import check_spec  # noqa: E402
from lazyspec_core.specmd import Spec  # noqa: E402

ENTRY_ROUTER = ROOT / "using-lazyspec" / "scripts" / "lazyspec.py"
ENTRY_SCAN = ROOT / "writing-spec" / "scripts" / "spec_scan.py"
ENTRY_STATE = ROOT / "executing-plan" / "scripts" / "spec_state.py"
ENTRY_MEMORY = ROOT / "maintain-memory" / "scripts" / "memory_tool.py"


def run(entry, *args, cwd=None):
    completed = subprocess.run(
        [sys.executable, str(entry), *args],
        cwd=str(cwd or ROOT),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return completed


def run_json(entry, *args, cwd=None):
    completed = run(entry, *args, "--json", cwd=cwd)
    payload = json.loads(completed.stdout) if completed.stdout.strip() else {}
    return completed.returncode, payload


def git(repo, *args):
    return subprocess.run(
        [
            "git",
            "-c",
            "user.name=LazySpec Test",
            "-c",
            "user.email=test@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.hooksPath=/dev/null",
            *args,
        ],
        cwd=str(repo),
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def init_repo(directory):
    git(directory, "init", "-q")
    git(directory, "add", ".")
    git(directory, "commit", "-qm", "init")
    return directory


class Workspace:
    """Temporary project holding a copy of the spec fixtures."""

    def __init__(self, features=("valid-plan",)):
        self._temporary = tempfile.TemporaryDirectory()
        self.root = Path(self._temporary.name)
        for feature in features:
            shutil.copytree(FIXTURES / feature, self.root / "specs" / feature)

    def spec(self, feature):
        return self.root / "specs" / feature / "spec.md"

    def read(self, feature):
        return self.spec(feature).read_text(encoding="utf-8")

    def write(self, feature, text):
        self.spec(feature).write_text(text, encoding="utf-8")

    def close(self):
        self._temporary.cleanup()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


class EntryPointTests(unittest.TestCase):
    def test_all_entries_expose_the_same_version(self):
        for entry in (ENTRY_ROUTER, ENTRY_SCAN, ENTRY_STATE, ENTRY_MEMORY):
            completed = run(entry, "--version")
            self.assertEqual(0, completed.returncode, completed.stderr)
            self.assertEqual("lazyspec-scripts 0.1.0", completed.stdout.strip())

    def test_each_entry_exposes_only_its_commands(self):
        router = run(ENTRY_ROUTER, "--help")
        self.assertIn("check", router.stdout)
        self.assertNotIn("task-done", router.stdout)
        state = run(ENTRY_STATE, "--help")
        self.assertIn("task-done", state.stdout)
        self.assertNotIn("recall", state.stdout)
        scanner = run(ENTRY_SCAN, "--help")
        self.assertIn("scan-specs", scanner.stdout)
        memory_entry = run(ENTRY_MEMORY, "--help")
        self.assertIn("memory-check", memory_entry.stdout)


class CheckStageTests(unittest.TestCase):
    def test_plan_fixture_passes(self):
        with Workspace() as workspace:
            code, payload = run_json(ENTRY_ROUTER, "check", "--feature", "valid-plan", "--stage", "plan", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            self.assertFalse(payload["approval"])
            self.assertEqual(0, payload["violation_count"])

    def test_delivered_fixture_passes(self):
        with Workspace(("delivered",)) as workspace:
            code, payload = run_json(ENTRY_ROUTER, "check", "--feature", "delivered", "--stage", "delivered", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)

    def test_legacy_spec_passes_with_warning(self):
        with Workspace(("legacy-format",)) as workspace:
            code, payload = run_json(ENTRY_ROUTER, "check", "--feature", "legacy-format", "--stage", "plan", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            self.assertTrue(payload["legacy"])
            self.assertEqual(0, payload["violation_count"])

    def codes_for(self, text, stage="plan"):
        match = re.search(r"^feature:\s*(.+)$", text, re.MULTILINE)
        feature = match.group(1).strip() if match else "demo"
        spec = Spec(text, Path("/tmp") / feature / "spec.md")
        return {violation.code for violation in check_spec(spec, stage).violations}

    def test_each_structural_rule_has_a_code(self):
        base = (FIXTURES / "valid-plan" / "spec.md").read_text(encoding="utf-8")
        cases = {
            "SPEC-102": base.replace("risk: medium\n", "", 1),
            "SPEC-103": base.replace("status: proposed", "status: doing", 1),
            "SPEC-104": base.replace("risk: medium", "risk: extreme", 1),
            "SPEC-105": base.replace("## 决策", "## 取舍", 1),
            "SPEC-106": base.replace("## 决策", "## 临时", 1).replace("## 风险与否定性保证", "## 决策", 1).replace("## 临时", "## 风险与否定性保证", 1),
            "SPEC-201": base.replace("| ID | 故事 | 类型 | 当 | 系统应 | 验证 |", "| ID | 故事 | 类型 | 当 | 系统应 | 检查 |", 1),
            "SPEC-202": base.replace("| R1.2 |", "| R1.1 |", 1),
            "SPEC-203": base.replace("→ R1.2；", "→ R9.9；", 1),
            "SPEC-204": base.replace("→ R1.2；", "→ R1.1；", 1),
            "SPEC-205": base.replace(
                "- **S2** 作为用户，我希望看到失败提示，以便定位问题。\n",
                "- **S2** 作为用户，我希望看到失败提示，以便定位问题。\n"
                "- **S3** 作为用户，我希望查看历史，以便复盘。\n",
                1,
            ),
            "SPEC-206": base.replace("| `pytest tests/test_demo.py::test_invalid` |", "|  |", 1),
            "SPEC-207": base.replace("| R1.2 | S2 |", "| R1.2 | S9 |", 1),
            "SPEC-301": base.replace("- [ ] //TODO 2.", "- [ ] TODO 2.", 1),
            "SPEC-502": base.replace(
                "| R1.2 | S2 |",
                "".join(f"| R1.{index} | S2 | 事件 | 条件{index} | 结果 | `pytest -q` |\n" for index in range(2, 14))
                + "| R1.2 | S2 |",
                1,
            ),
        }
        for expected, text in cases.items():
            with self.subTest(code=expected):
                self.assertIn(expected, self.codes_for(text))

    def test_task_numbering_and_coverage_are_enforced(self):
        base = (FIXTURES / "valid-plan" / "spec.md").read_text(encoding="utf-8")
        duplicated = base.replace("//TODO 2.", "//TODO 1.", 1)
        self.assertIn("SPEC-302", self.codes_for(duplicated))

    def test_review_stage_requires_checked_tasks_and_evidence(self):
        base = (FIXTURES / "review-ready" / "spec.md").read_text(encoding="utf-8")
        self.assertEqual(set(), self.codes_for(base, stage="review"))

        unchecked = base.replace("- [x] //TODO 2.", "- [ ] //TODO 2.", 1)
        self.assertIn("SPEC-303", self.codes_for(unchecked, stage="review"))

        missing = base.replace("- 未决：无\n", "", 1)
        self.assertIn("SPEC-401", self.codes_for(missing, stage="review"))

        bad_state = base.replace("- 状态：passed", "- 状态：good", 1)
        self.assertIn("SPEC-402", self.codes_for(bad_state, stage="review"))

        no_commit = base.replace("abc1234 · 2026-01-02T10:00:00+08:00", "刚刚", 1)
        self.assertIn("SPEC-403", self.codes_for(no_commit, stage="review"))

    def test_delivered_stage_rejects_leftover_tasks(self):
        base = (FIXTURES / "review-ready" / "spec.md").read_text(encoding="utf-8")
        delivered = base.replace("status: proposed", "status: delivered", 1).replace(
            "delivered_at: null", "delivered_at: 2026-01-03", 1
        )
        codes = self.codes_for(delivered, stage="delivered")
        self.assertIn("SPEC-601", codes)
        self.assertIn("SPEC-602", codes)


class SpecMutationTests(unittest.TestCase):
    def test_checkbox_flip_preserves_every_other_byte(self):
        with Workspace() as workspace:
            before = workspace.read("valid-plan")
            code, payload = run_json(ENTRY_STATE, "task-done", "--feature", "valid-plan", "--n", "2", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            after = workspace.read("valid-plan")
            self.assertEqual(before.replace("- [ ] //TODO 2.", "- [x] //TODO 2.", 1), after)
            self.assertEqual(["2"], [str(item) for item in payload["completed"]])

    def test_second_call_is_idempotent(self):
        with Workspace() as workspace:
            run_json(ENTRY_STATE, "task-done", "--feature", "valid-plan", "--n", "1", "--root", str(workspace.root))
            code, payload = run_json(ENTRY_STATE, "task-done", "--feature", "valid-plan", "--n", "1", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            self.assertEqual(["1"], [str(item) for item in payload["already_done"]])

    def test_commit_stages_only_named_paths(self):
        with Workspace() as workspace:
            init_repo(workspace.root)
            (workspace.root / "code.txt").write_text("change\n", encoding="utf-8")
            code, payload = run_json(
                ENTRY_STATE, "task-done", "--feature", "valid-plan", "--n", "1",
                "--commit", "--paths", "code.txt", "--root", str(workspace.root),
            )
            self.assertEqual(0, code, payload)
            message = git(workspace.root, "log", "-1", "--pretty=%s").strip()
            self.assertEqual("feat(valid-plan): TODO 1 实现成功路径", message)
            files = git(workspace.root, "show", "--name-only", "--pretty=", "HEAD").split()
            self.assertEqual(["code.txt", "specs/valid-plan/spec.md"], sorted(files))

    def test_commit_refuses_unrelated_staged_changes(self):
        with Workspace() as workspace:
            init_repo(workspace.root)
            (workspace.root / "other.txt").write_text("other\n", encoding="utf-8")
            git(workspace.root, "add", "other.txt")
            code, payload = run_json(
                ENTRY_STATE, "task-done", "--feature", "valid-plan", "--n", "1",
                "--commit", "--root", str(workspace.root),
            )
            self.assertEqual(4, code, payload)

    def test_evidence_records_four_lines_with_head(self):
        with Workspace() as workspace:
            init_repo(workspace.root)
            head = git(workspace.root, "rev-parse", "--short", "HEAD").strip()
            code, payload = run_json(
                ENTRY_STATE, "evidence", "--feature", "valid-plan",
                "--status", "passed", "--result", "R1.1 通过", "--root", str(workspace.root),
            )
            self.assertEqual(0, code, payload)
            self.assertEqual(head, payload["tested_commit"])
            body = workspace.read("valid-plan")
            record = body.split("## 执行记录", 1)[1]
            lines = [line for line in record.splitlines() if line.startswith("- ")]
            self.assertEqual(4, len(lines))
            self.assertIn(f"- 验证：{head} · 20", body)

    def test_evidence_can_record_an_explicit_no_commit_state(self):
        with Workspace() as workspace:
            code, payload = run_json(
                ENTRY_STATE, "evidence", "--feature", "valid-plan",
                "--status", "blocked", "--result", "环境缺失", "--no-commit", "--root", str(workspace.root),
            )
            self.assertEqual(0, code, payload)
            self.assertIn("无提交", payload["tested_commit"])

    def test_evidence_can_commit_the_record(self):
        with Workspace() as workspace:
            init_repo(workspace.root)
            code, payload = run_json(
                ENTRY_STATE, "evidence", "--feature", "valid-plan",
                "--status", "passed", "--result", "R1.1 通过", "--commit-record",
                "--root", str(workspace.root),
            )
            self.assertEqual(0, code, payload)
            self.assertTrue(payload["commit"])
            self.assertEqual("docs(valid-plan): record verification evidence",
                             git(workspace.root, "log", "-1", "--pretty=%s").strip())
            self.assertEqual("", git(workspace.root, "status", "--porcelain").strip())

    def test_deliver_without_review_evidence_is_refused(self):
        with Workspace() as workspace:
            code, payload = run_json(ENTRY_STATE, "deliver", "--feature", "valid-plan", "--root", str(workspace.root))
            self.assertEqual(1, code, payload)
            self.assertIn("## 任务", workspace.read("valid-plan"))

    def test_deliver_dry_run_writes_nothing_then_finalizes(self):
        with Workspace() as workspace:
            init_repo(workspace.root)
            run_json(ENTRY_STATE, "task-done", "--feature", "valid-plan", "--n", "1", "--n", "2", "--commit", "--root", str(workspace.root))
            run_json(ENTRY_STATE, "evidence", "--feature", "valid-plan", "--status", "passed", "--result", "R1.1、R1.2 通过", "--root", str(workspace.root))
            before = workspace.read("valid-plan")
            code, payload = run_json(ENTRY_STATE, "deliver", "--feature", "valid-plan", "--dry-run", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            self.assertIn("## 任务", workspace.read("valid-plan"))
            self.assertIn("- [x] //TODO 1.", payload["diff"])

            code, payload = run_json(ENTRY_STATE, "deliver", "--feature", "valid-plan", "--commit", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            after = workspace.read("valid-plan")
            self.assertNotIn("## 任务", after)
            self.assertNotIn("//TODO", after)
            self.assertIn("status: delivered", after)
            self.assertNotIn(before, after)
            self.assertEqual("docs(valid-plan): finalize delivered specification",
                             git(workspace.root, "log", "-1", "--pretty=%s").strip())

            code, _payload = run_json(ENTRY_ROUTER, "check", "--feature", "valid-plan", "--stage", "delivered", "--root", str(workspace.root))
            self.assertEqual(0, code)

    def test_deliver_syncs_supersession(self):
        with Workspace(("delivered", "review-ready")) as workspace:
            old = workspace.spec("delivered")
            text = old.read_text(encoding="utf-8").replace(
                "superseded_by: null", "superseded_by: null", 1
            )
            old.write_text(text, encoding="utf-8")
            new = workspace.spec("review-ready")
            new.write_text(
                new.read_text(encoding="utf-8").replace("supersedes: []", "supersedes: [specs/delivered/]", 1),
                encoding="utf-8",
            )
            init_repo(workspace.root)
            run_json(ENTRY_STATE, "task-done", "--feature", "review-ready", "--n", "1", "--n", "2", "--commit", "--root", str(workspace.root))
            run_json(ENTRY_STATE, "evidence", "--feature", "review-ready", "--status", "passed", "--result", "R1.1、R1.2 通过", "--root", str(workspace.root))
            code, payload = run_json(ENTRY_STATE, "deliver", "--feature", "review-ready", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            superseded = old.read_text(encoding="utf-8")
            self.assertIn("status: superseded", superseded)
            self.assertIn("superseded_by: specs/review-ready/", superseded)
            self.assertIn("[!WARNING]", superseded)


class WorktreeTests(unittest.TestCase):
    def test_add_carries_an_uncommitted_spec(self):
        with Workspace() as workspace:
            spec_text = workspace.read("valid-plan")
            workspace.spec("valid-plan").unlink()
            (workspace.root / "README.md").write_text("demo\n", encoding="utf-8")
            init_repo(workspace.root)
            git(workspace.root, "branch", "-m", "dev")
            workspace.write("valid-plan", spec_text)

            code, payload = run_json(ENTRY_STATE, "worktree", "add", "--feature", "valid-plan", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            self.assertTrue(payload["spec_carried"])
            carried = workspace.root / ".worktrees" / "valid-plan" / "specs" / "valid-plan" / "spec.md"
            self.assertEqual(spec_text, carried.read_text(encoding="utf-8"))
            self.assertFalse(workspace.spec("valid-plan").exists())

    def test_add_is_idempotent_and_remove_requires_clean(self):
        with Workspace() as workspace:
            init_repo(workspace.root)
            git(workspace.root, "branch", "-m", "dev")
            code, payload = run_json(ENTRY_STATE, "worktree", "add", "--feature", "valid-plan", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            path = workspace.root / ".worktrees" / "valid-plan"
            self.assertTrue(path.is_dir())
            code, payload = run_json(ENTRY_STATE, "worktree", "add", "--feature", "valid-plan", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            self.assertTrue(payload["exists"])

            (path / "dirty.txt").write_text("dirty\n", encoding="utf-8")
            code, payload = run_json(ENTRY_STATE, "worktree", "remove", "--feature", "valid-plan", "--root", str(workspace.root))
            self.assertEqual(4, code, payload)

            code, payload = run_json(ENTRY_STATE, "worktree", "remove", "--feature", "valid-plan", "--force", "--root", str(workspace.root))
            self.assertEqual(0, code, payload)
            self.assertFalse(path.exists())

    def test_remove_refuses_tracked_changes_even_with_force(self):
        with Workspace() as workspace:
            init_repo(workspace.root)
            git(workspace.root, "branch", "-m", "dev")
            run_json(ENTRY_STATE, "worktree", "add", "--feature", "valid-plan", "--root", str(workspace.root))
            path = workspace.root / ".worktrees" / "valid-plan"
            (path / "specs" / "valid-plan" / "spec.md").write_text("changed\n", encoding="utf-8")

            code, payload = run_json(ENTRY_STATE, "worktree", "remove", "--feature", "valid-plan", "--force", "--root", str(workspace.root))
            self.assertEqual(4, code, payload)
            self.assertTrue(path.is_dir())


class MemoryScriptTests(unittest.TestCase):
    def test_index_generation_matches_the_fixture(self):
        completed = run(ENTRY_MEMORY, "index", "--check", "--root", str(ROOT / "tests" / "fixtures"), "--json")
        payload = json.loads(completed.stdout)
        self.assertEqual(0, completed.returncode, payload)
        self.assertFalse(payload["drift"])

    def test_index_detects_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "tests" / "fixtures" / "project-memory", root / "project-memory")
            index = root / "project-memory" / "index.md"
            index.write_text(index.read_text(encoding="utf-8").replace("active", "needs-review", 1), encoding="utf-8")
            completed = run(ENTRY_MEMORY, "index", "--check", "--root", str(root))
            self.assertEqual(1, completed.returncode)
            self.assertIn("MEM-301", completed.stdout)

    def test_memory_check_rejects_missing_reason(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "tests" / "fixtures" / "project-memory", root / "project-memory")
            capsule = root / "project-memory" / "features" / "drifting.md"
            capsule.write_text(
                capsule.read_text(encoding="utf-8").replace(
                    'status_reason: "Implementation drift requires review."\n', "", 1
                ),
                encoding="utf-8",
            )
            completed = run(ENTRY_MEMORY, "memory-check", "--root", str(root))
            self.assertEqual(1, completed.returncode)
            self.assertIn("MEM-104", completed.stdout)

    def test_recall_rejects_traversal_and_absolute_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = ROOT / "tests" / "fixtures" / "project-memory"
            shutil.copytree(base, root / "project-memory")
            index = root / "project-memory" / "index.md"
            text = index.read_text(encoding="utf-8")
            text += (
                "| [project-memory/features/escape.md](../secret.md) | escape | escape | active | "
                "[specs/escape/](../specs/escape/) | 2026-08-18 |\n"
                "| [/etc/passwd](/etc/passwd) | absolute | absolute | active | "
                "[specs/absolute/](../specs/absolute/) | 2026-08-18 |\n"
            )
            index.write_text(text, encoding="utf-8")
            code, payload = run_json(ENTRY_ROUTER, "recall", "--query", "memory", "--root", str(root))
            self.assertEqual(0, code, payload)
            paths = [entry["path"] for entry in payload["memories"]]
            self.assertNotIn("project-memory/features/escape.md", paths)
            self.assertTrue(any("跳过" in warning["message"] for warning in payload["warnings"]))

    def test_recall_is_limited_and_active_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "tests" / "fixtures" / "project-memory", root / "project-memory")
            code, payload = run_json(ENTRY_ROUTER, "recall", "--query", "memory", "--root", str(root))
            self.assertEqual(0, code, payload)
            self.assertLessEqual(len(payload["memories"]), 3)
            self.assertTrue(all(entry["status"] == "active" for entry in payload["memories"]))


class ScanTests(unittest.TestCase):
    def test_porcelain_parser_handles_renames_and_unicode(self):
        raw = (
            "M  specs/staged/spec.md\0"
            " M specs/unstaged/spec.md\0"
            "?? specs/新 草稿/spec.md\0"
            "R  specs/重命名/spec.md\0specs/old/spec.md\0"
        ).encode()
        records = scan.parse_porcelain_z(raw)
        self.assertEqual("specs/old/spec.md", records[3]["origin"])
        self.assertEqual("specs/\u91cd\u547d\u540d/spec.md", records[3]["path"])
        self.assertTrue(scan.is_spec_path("specs/\u65b0 \u8349\u7a3f/spec.md"))
        self.assertFalse(scan.is_spec_path("specs/a/spec.md/b.md"))
        self.assertFalse(scan.is_spec_path("specs/archived/a/spec.md"))

    def test_scan_specs_excludes_archived_and_current_feature(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for feature in ("alpha", "beta"):
                (root / "specs" / feature).mkdir(parents=True)
                (root / "specs" / feature / "spec.md").write_text("# x\n", encoding="utf-8")
            (root / "specs" / "archived" / "gamma").mkdir(parents=True)
            (root / "specs" / "archived" / "gamma" / "spec.md").write_text("# y\n", encoding="utf-8")
            git(root, "init", "-q")
            git(root, "add", ".")
            git(root, "commit", "-qm", "init")
            (root / "specs" / "alpha" / "spec.md").write_text("# changed\n", encoding="utf-8")
            git(root, "mv", "specs/beta", "specs/beta-renamed")

            code, payload = run_json(ENTRY_SCAN, "scan-specs", "--changed", "--root", str(root))
            self.assertEqual(0, code, payload)
            paths = [entry["path"] for entry in payload["specs"]]
            self.assertEqual(["specs/alpha/spec.md", "specs/beta-renamed/spec.md"], paths)
            self.assertTrue(all("sha256" in entry for entry in payload["specs"]))

            code, payload = run_json(
                ENTRY_SCAN, "scan-specs", "--changed", "--feature", "alpha", "--root", str(root)
            )
            self.assertEqual(["specs/beta-renamed/spec.md"], [entry["path"] for entry in payload["specs"]])

    def test_scan_retired_reports_obsolete_specs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "specs" / "retired" / "old-thing"
            target.mkdir(parents=True)
            (target / "spec.md").write_text(
                "---\nstatus: obsolete\n---\n\n# Old Thing\n\n> 该方案已被证伪。\n", encoding="utf-8"
            )
            code, payload = run_json(ENTRY_ROUTER, "scan-retired", "--root", str(root))
            self.assertEqual(0, code, payload)
            self.assertEqual("old-thing", payload["retired"][0]["feature"])
            self.assertIn("证伪", payload["retired"][0]["reason"])


if __name__ == "__main__":
    unittest.main()
