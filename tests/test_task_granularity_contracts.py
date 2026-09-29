"""Guard the normal Tasks planning contract and its behavior-slice example."""

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASK_DIR = ROOT / "writing-task"
LINK = re.compile(r"\[(\d+\.\d+)\]\(\./requirements\.md#req-(\d+)-(\d+)\)")


class TaskGranularityContractTests(unittest.TestCase):
    def test_normal_planning_groups_complete_behavior_without_a_link_cap(self):
        skill = (TASK_DIR / "SKILL.md").read_text()
        prompt = (TASK_DIR / "task-prompt.md").read_text()
        readme = (ROOT / "README.md").read_text()

        for document in (skill, prompt):
            with self.subTest(document=document[:40]):
                self.assertIn("fewest TODOs", document)
                self.assertIn("independently verifiable behavior", document)
                self.assertIn("entry-point integration", document)
                self.assertIn("automated tests", document)
                self.assertIn("dependencies, risks, or observable", document)
                self.assertIn("file, architectural layer, or test type", document)
                self.assertNotRegex(document, r"(?:no more than|at most) 5(?: acceptance)?")

        self.assertIn("no fixed per-TODO link limit", skill)
        self.assertIn("success, validation, and failure paths of one behavior", skill)
        self.assertIn("newly created `tasks.md` files and user-requested revisions", skill)
        self.assertIn("every acceptance criterion directly implemented", skill)
        self.assertIn("every acceptance criterion is linked by at least one task", skill)
        self.assertIn("普通模式的 Tasks", readme)
        self.assertIn("//TODO 1. 完成创建记录行为", readme)
        self.assertIn("//TODO 2. 完成按 ID 查询行为", readme)

    def test_example_groups_create_flow_and_splits_independent_query_flow(self):
        template = (TASK_DIR / "task-templete.md").read_text()
        example = template.split("```markdown\n", 1)[1].split("\n```", 1)[0]
        tasks_section, verification = example.split("## Feature Verification", 1)
        blocks = re.findall(
            r"^- \[ \] //TODO (\d+)\. ([^\n]+)\n(.*?)(?=^- \[ \] //TODO|\Z)",
            tasks_section,
            re.MULTILINE | re.DOTALL,
        )
        self.assertEqual(2, len(blocks))
        self.assertEqual(["1", "2"], [number for number, _, _ in blocks])

        task_links = []
        for _, _, body in blocks:
            with self.subTest(body=body[:40]):
                self.assertEqual(1, body.count("实现目标："))
                self.assertEqual(1, body.count("成功判据："))
                self.assertEqual(1, body.count("验证方式："))
                self.assertIn("待实现", body)
                links = LINK.findall(body)
                self.assertTrue(links)
                self.assertTrue(all(label == f"{major}.{minor}" for label, major, minor in links))
                task_links.append({label for label, _, _ in links})

        self.assertIn("参数校验", blocks[0][2])
        self.assertIn("数据写入", blocks[0][2])
        self.assertIn("响应接入", blocks[0][2])
        self.assertIn("自动化测试", blocks[0][2])
        self.assertIn("查询入口", blocks[1][2])
        self.assertTrue(task_links[0].isdisjoint(task_links[1]))

        planned = verification.split("### Planned Checks", 1)[1].split("### Latest Result", 1)[0]
        planned_links = {label for label, _, _ in LINK.findall(planned)}
        self.assertEqual(task_links[0] | task_links[1], planned_links)
        self.assertIn("未执行", verification)


if __name__ == "__main__":
    unittest.main()
