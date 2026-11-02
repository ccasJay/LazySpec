"""Static Skill contracts and Git discovery checks, not an Agent simulator."""

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec/SKILL.md").read_text()
SKILL = (ROOT / "writing-spec/SKILL.md").read_text()
PROMPT = (ROOT / "writing-spec/spec-prompt.md").read_text()
POLICY = (ROOT / "using-lazyspec/references/approval-policy.md").read_text()
SCANNER = ROOT / "writing-spec" / "scripts" / "spec_scan.py"


class WritingSpecContractTests(unittest.TestCase):
    def test_manifest_registers_current_skills(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        expected = {
            "using-lazyspec", "writing-spec", "executing-plan",
            "distill-feature", "maintain-memory", "orchestrating-specs",
        }
        self.assertEqual(expected, {Path(p).name for p in manifest["skills"]})
        self.assertEqual(len(expected), len(manifest["skills"]))

        self.assertFalse((ROOT / "writing-requirement/SKILL.md").exists())
        self.assertFalse((ROOT / "writing-design/SKILL.md").exists())
        self.assertFalse((ROOT / "writing-task/SKILL.md").exists())
        self.assertFalse((ROOT / "writing-plan/SKILL.md").exists())
        self.assertFalse((ROOT / "executing-task/SKILL.md").exists())
        self.assertFalse((ROOT / "distill-spec-memory/SKILL.md").exists())

    def test_creation_and_revision_route_directly_to_spec(self):
        self.assertIn("route directly to `writing-spec`", ROUTER)
        self.assertIn("Phase 1: Spec Creation / Revision", ROUTER)
        self.assertIn("single planning artifact", ROUTER)

    def test_decision_probing_grill_me_principles(self):
        self.assertIn("Structured Probing (/grill-me Style)", SKILL)
        self.assertIn("Identify Branches of Decision Tree", SKILL)
        self.assertIn("Ask One Focused Decision Question at a Time", SKILL)
        self.assertIn("Alternatives Considered", SKILL)
        self.assertIn("EARS", SKILL)
        self.assertIn("negative guarantees", SKILL)

    def test_acceptance_table_and_stable_ids(self):
        template = (ROOT / "writing-spec/spec-template.md").read_text()
        self.assertIn("| ID | 故事 | 类型 | 当 | 系统应 | 验证 |", template)
        self.assertIn("R1.1", template)
        self.assertIn("S1", template)
        self.assertIn("## 风险与否定性保证", template)
        self.assertNotIn('spec-req-', template)

    def test_concise_spec_preserves_material_contracts(self):
        self.assertIn("references its ID instead of repeating the text", PROMPT)
        self.assertIn("only when a rejected alternative matters", PROMPT)
        self.assertIn("compatibility", PROMPT)
        self.assertIn("file inventories", PROMPT)
        self.assertIn("Never drop a distinct acceptance behavior", PROMPT)
        self.assertIn("Shape and budget", PROMPT)

    def test_skill_routes_discovery_and_plan_check_through_scripts(self):
        self.assertIn("scripts/spec_scan.py scan-specs --changed", SKILL)
        self.assertIn("lazyspec.py check --feature <f> --stage plan", SKILL)
        self.assertIn("If Python 3 or the scripts are unavailable", SKILL)

    def test_documented_discovery_script_observes_current_workspace_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            workspace = Path(directory)

            def git(*args):
                return subprocess.run(
                    ["git", "-c", "user.name=LazySpec Test",
                     "-c", "user.email=test@example.invalid",
                     "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", *args],
                    cwd=workspace, check=True, capture_output=True,
                ).stdout

            def write(path, content):
                file = workspace / path
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(content)

            git("init", "-q")
            for feature in ("staged", "unstaged", "both", "old", "deleted", "clean"):
                write(f"specs/{feature}/spec.md", f"# {feature}\nOriginal design.\n")
            git("add", ".")
            git("commit", "-qm", "Initial fixture")
            write("specs/staged/spec.md", "Staged design.\n")
            write("specs/both/spec.md", "Staged version.\n")
            write("specs/added/spec.md", "New staged Spec.\n")
            git("add", "specs/staged", "specs/both", "specs/added")
            write("specs/both/spec.md", "Current working-tree version.\n")
            write("specs/unstaged/spec.md", "Unstaged design.\n")
            write("specs/新 草稿/spec.md", "Untracked draft.\n")
            write("outside.txt", "Outside the Spec discovery scope.\n")
            git("mv", "specs/old", "specs/重命名 设计")
            git("rm", "specs/deleted/spec.md")

            def discover(*extra):
                completed = subprocess.run(
                    [sys.executable, str(SCANNER), "scan-specs", "--changed", "--json",
                     "--root", str(workspace), *extra],
                    cwd=workspace, check=False, capture_output=True, text=True,
                )
                self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)
                return json.loads(completed.stdout)

            initial = discover()["specs"]
            found = {entry["path"]: entry for entry in initial}
            self.assertEqual(
                {
                    "specs/staged/spec.md",
                    "specs/unstaged/spec.md",
                    "specs/both/spec.md",
                    "specs/added/spec.md",
                    "specs/新 草稿/spec.md",
                    "specs/重命名 设计/spec.md",
                },
                set(found),
            )
            self.assertEqual("specs/old/spec.md", found["specs/重命名 设计/spec.md"]["origin"])
            self.assertNotIn("specs/clean/spec.md", found)
            self.assertNotIn("specs/deleted/spec.md", found)
            self.assertNotIn("outside.txt", found)
            self.assertTrue(all(entry["sha256"] for entry in initial))

            # A status-only snapshot misses content changes with unchanged XY codes;
            # the content hash must change instead.
            previous = found["specs/unstaged/spec.md"]["sha256"]
            write("specs/unstaged/spec.md", "Revised again during probing.\n")
            current = {entry["path"]: entry for entry in discover()["specs"]}
            self.assertNotEqual(previous, current["specs/unstaged/spec.md"]["sha256"])

            revision = git("rev-parse", "HEAD").decode().strip()
            with_change = {entry["path"]: entry for entry in discover("--since", revision)["specs"]}
            self.assertEqual("changed", with_change["specs/unstaged/spec.md"]["content_change"])
            self.assertEqual("new", with_change["specs/新 草稿/spec.md"]["content_change"])

            write("specs/later/spec.md", "Peer created before approval.\n")
            self.assertIn("specs/later/spec.md", {entry["path"] for entry in discover()["specs"]})


if __name__ == "__main__":
    unittest.main()
