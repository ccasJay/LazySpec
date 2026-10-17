"""Static Skill contracts and Git discovery checks, not an Agent simulator."""

import json
import re
import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER = (ROOT / "using-lazyspec/SKILL.md").read_text()
SKILL = (ROOT / "writing-spec/SKILL.md").read_text()
PROMPT = (ROOT / "writing-spec/spec-prompt.md").read_text()
POLICY = (ROOT / "using-lazyspec/references/approval-policy.md").read_text()


class WritingSpecContractTests(unittest.TestCase):
    def test_manifest_registers_current_skills(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        expected = {
            "using-lazyspec", "writing-spec", "writing-plan", "executing-plan",
            "distill-feature", "maintain-memory",
            "fast", "orchestrating-specs",
        }
        self.assertEqual(expected, {Path(p).name for p in manifest["skills"]})
        self.assertEqual(len(expected), len(manifest["skills"]))

        self.assertFalse((ROOT / "writing-requirement/SKILL.md").exists())
        self.assertFalse((ROOT / "writing-design/SKILL.md").exists())
        self.assertFalse((ROOT / "writing-task/SKILL.md").exists())
        self.assertFalse((ROOT / "executing-task/SKILL.md").exists())
        self.assertFalse((ROOT / "distill-spec-memory/SKILL.md").exists())

    def test_creation_and_revision_route_directly_to_spec(self):
        self.assertIn("route directly to `writing-spec`", ROUTER)
        self.assertIn("Phase 1: Spec Creation / Revision", ROUTER)

    def test_decision_probing_grill_me_principles(self):
        self.assertIn("Structured Probing (/grill-me Style)", SKILL)
        self.assertIn("Identify Branches of Decision Tree", SKILL)
        self.assertIn("Ask One Focused Decision Question at a Time", SKILL)
        self.assertIn("Alternatives Considered", SKILL)
        self.assertIn("EARS", SKILL)
        self.assertIn("negative guarantees", SKILL)

    def test_ears_criteria_anchors(self):
        template = (ROOT / "writing-spec/spec-template.md").read_text()
        self.assertIn('spec-req-', template)
        self.assertIn('## 曾考虑的备选方案', template)
        self.assertIn('## 风险与否定性保证', template)

    def test_documented_discovery_command_observes_current_workspace_changes(self):
        command = shlex.split(re.search(r"```sh\n([^\n]+)\n```", SKILL).group(1))
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

            def discover():
                return subprocess.run(command, cwd=workspace, check=True, capture_output=True).stdout

            initial = discover()
            for record in (
                b"M  specs/staged/spec.md\0", b" M specs/unstaged/spec.md\0",
                b"MM specs/both/spec.md\0", b"A  specs/added/spec.md\0",
                "?? specs/新 草稿/spec.md\0".encode(),
                "R  specs/重命名 设计/spec.md\0specs/old/spec.md\0".encode(),
                b"D  specs/deleted/spec.md\0",
            ):
                with self.subTest(record=record):
                    self.assertIn(record, initial)
            self.assertNotIn(b"outside.txt", initial)
            self.assertNotIn(b"specs/clean/spec.md", initial)

            # A status-only snapshot misses content changes with unchanged XY codes.
            write("specs/unstaged/spec.md", "Revised again during probing.\n")
            self.assertEqual(initial, discover())
            self.assertEqual("Revised again during probing.\n", (workspace / "specs/unstaged/spec.md").read_text())
            write("specs/later/spec.md", "Peer created before approval.\n")
            self.assertIn(b"?? specs/later/spec.md\0", discover())
            self.assertNotIn(b"specs/later/spec.md", initial)


if __name__ == "__main__":
    unittest.main()
