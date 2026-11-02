"""Contracts tying Skill text to the shipped deterministic scripts."""

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ENTRIES = {
    "using-lazyspec": ("scripts/lazyspec.py", ("check", "recall", "scan-retired")),
    "writing-spec": ("scripts/spec_scan.py", ("scan-specs",)),
    "executing-plan": ("scripts/spec_state.py", ("task-done", "evidence", "deliver", "worktree", "checks")),
    "maintain-memory": ("scripts/memory_tool.py", ("index", "memory-check")),
}

ALLOWED_MODULES = {
    "__future__",
    "argparse",
    "ast",
    "dataclasses",
    "datetime",
    "difflib",
    "hashlib",
    "json",
    "lazyspec_core",
    "os",
    "pathlib",
    "re",
    "shutil",
    "subprocess",
    "sys",
    "tempfile",
    "typing",
}


class ScriptContractTests(unittest.TestCase):
    def test_each_skill_ships_runnable_commands(self):
        for skill, (relative, commands) in ENTRIES.items():
            entry = ROOT / skill / relative
            with self.subTest(skill=skill):
                self.assertTrue(entry.is_file(), f"missing {entry}")
                completed = subprocess.run(
                    [sys.executable, str(entry), "--help"],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, completed.returncode, completed.stderr)
                for command in commands:
                    self.assertIn(command, completed.stdout)

    def test_each_skill_documents_its_entry(self):
        for skill, (relative, commands) in ENTRIES.items():
            text = (ROOT / skill / "SKILL.md").read_text()
            with self.subTest(skill=skill):
                self.assertIn(Path(relative).name, text)
                for command in commands:
                    self.assertIn(command, text)
                self.assertIn("Python 3", text)

    def test_shared_core_has_exactly_one_copy(self):
        copies = [
            path
            for path in ROOT.rglob("lazyspec_core")
            if path.is_dir() and ".git" not in path.parts and "__pycache__" not in path.parts
        ]
        self.assertEqual([ROOT / "using-lazyspec" / "scripts" / "lazyspec_core"], copies)

    def test_scripts_use_only_the_standard_library(self):
        for path in (ROOT / "using-lazyspec" / "scripts").rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        with self.subTest(path=path, module=alias.name):
                            self.assertIn(alias.name.split(".")[0], ALLOWED_MODULES)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    with self.subTest(path=path, module=node.module):
                        self.assertIn(node.module.split(".")[0], ALLOWED_MODULES)

    def test_entries_resolve_the_core_from_the_skills_root(self):
        for skill, (relative, _commands) in ENTRIES.items():
            entry = (ROOT / skill / relative).read_text()
            with self.subTest(skill=skill):
                self.assertIn('parents[2]', entry)
                self.assertIn('"using-lazyspec"', entry)
                self.assertIn("dont_write_bytecode", entry)
                self.assertIn("ENV-130", entry)

    def test_router_script_owns_the_contract_gate_and_versions_match(self):
        router = ROOT / "using-lazyspec" / "scripts" / "lazyspec.py"
        completed = subprocess.run(
            [sys.executable, str(router), "--version"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual("lazyspec-scripts 0.1.0", completed.stdout.strip())

        core_version = (ROOT / "using-lazyspec" / "scripts" / "lazyspec_core" / "util.py").read_text()
        self.assertIn('VERSION = "0.1.0"', core_version)

    def test_plugin_manifest_still_registers_every_skill(self):
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(set(ENTRIES) | {"distill-feature", "orchestrating-specs"},
                         {Path(path).name for path in manifest["skills"]})


if __name__ == "__main__":
    unittest.main()
