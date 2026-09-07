import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTER_PATH = ROOT / "using-lazyspec" / "SKILL.md"
ROUTER = ROUTER_PATH.read_text()
POLICIES = ROOT / "using-lazyspec" / "references"

ROUTE_TO_SKILL = {
    "brainstorming": "brainstorming",
    "requirements": "writing-requirement",
    "design": "writing-design",
    "tasks": "writing-task",
    "execute": "using-lazyspec",
    "fast": "fast",
    "orchestration": "orchestrating-specs",
    "memory-recall": "using-lazyspec",
    "memory-distill": "distill-spec-memory",
    "codex-plan-adapter": "using-lazyspec",
}


def parse_matrix():
    rows = re.findall(r"^\|\s*([a-z][a-z-]*)\s*\|\s*([^|]+)\|", ROUTER, re.MULTILINE)
    return {route: [r.strip() for r in res.split(",")] for route, res in rows}


class ResourceLoadingContractTests(unittest.TestCase):
    def test_router_defines_the_resource_loading_matrix(self):
        self.assertIn("## Resource Loading", ROUTER)
        self.assertIn("Load only resources required by the selected route.", ROUTER)
        self.assertIn("- Load the routed Skill after selecting the route.", ROUTER)
        self.assertIn("- Do not preload every reference at session start.", ROUTER)
        matrix = parse_matrix()
        self.assertEqual(set(ROUTE_TO_SKILL), set(matrix))

    def test_every_matrix_resource_exists(self):
        for route, resources in parse_matrix().items():
            with self.subTest(route=route):
                for resource in resources:
                    self.assertTrue(
                        (POLICIES / f"{resource}.md").exists(),
                        f"missing references/{resource}.md for route {route}",
                    )

    def test_routed_skills_declare_their_matrix_resources(self):
        matrix = parse_matrix()
        for route, skill in ROUTE_TO_SKILL.items():
            if skill == "using-lazyspec":
                continue
            text = (ROOT / skill / "SKILL.md").read_text()
            declared = set(re.findall(r"\]\(([^)]+)\)", text))
            for resource in matrix[route]:
                self.assertTrue(
                    any(f"{resource}.md" in link for link in declared),
                    f"{skill}/SKILL.md does not link {resource}.md",
                )

    def test_distill_memory_declares_only_its_matrix_policy(self):
        text = (ROOT / "distill-spec-memory" / "SKILL.md").read_text()
        self.assertEqual([], re.findall(r"\]\(([^)]+risk-policy\.md)\)", text))
        self.assertEqual(
            1, len(re.findall(r"\]\(([^)]+approval-policy\.md)\)", text))
        )

    def test_every_relative_link_in_skills_resolves(self):
        manifest = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
        for directory in manifest["skills"]:
            skill = ROOT / directory / "SKILL.md"
            for link in re.findall(r"\]\(([^)#]+\.md)\)", skill.read_text()):
                with self.subTest(skill=str(skill), link=link):
                    self.assertTrue(
                        (skill.parent / link).resolve().exists(),
                        f"broken reference {link}",
                    )

    def test_prompt_and_template_files_stay_skill_relative(self):
        for directory, resources in (
            ("writing-requirement", ("requirement-prompt.md", "requirement-templete.md")),
            ("writing-design", ("design-prompt.md", "design-templete.md")),
            ("writing-task", ("task-prompt.md", "task-templete.md")),
        ):
            skill = (ROOT / directory / "SKILL.md").read_text()
            self.assertIn(
                "relative to the directory containing this `SKILL.md`", skill
            )
            for resource in resources:
                self.assertIn(resource, skill)


if __name__ == "__main__":
    unittest.main()
