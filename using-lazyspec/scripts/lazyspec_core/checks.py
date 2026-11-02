"""Deterministic invariants for the single `spec.md` artifact."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from . import gitx
from .specmd import ACCEPTANCE_HEADER, EXECUTION_FIELDS, SID_RE, Spec
from .util import Violation

REQUIRED_FIELDS = (
    "feature",
    "status",
    "risk",
    "created_at",
    "delivered_at",
    "supersedes",
    "superseded_by",
)
STATUSES = {"proposed", "delivered", "archived", "superseded", "obsolete"}
RISKS = {"low", "medium", "high"}
EVIDENCE_STATES = {"passed", "failed", "blocked", "pending-human"}
CONTRACT_SECTIONS = ("目标与范围", "用户故事", "验收标准", "决策", "风险与否定性保证")
CANONICAL_ORDER = CONTRACT_SECTIONS + ("任务", "执行记录")
BUDGETS = {
    "目标与范围": (2, "SPEC-501"),
    "验收标准": (12, "SPEC-502"),
    "决策": (5, "SPEC-503"),
    "风险与否定性保证": (3, "SPEC-504"),
    "任务": (12, "SPEC-505"),
    "执行记录": (5, "SPEC-506"),
}
COMMIT_RE = re.compile(r"\b[0-9a-f]{7,40}\b")
SENSITIVE_RE = re.compile(r"(?i)(password|passwd|secret|api[_-]?key|access[_-]?token|private[_-]?key)")

CODE_CATALOG: Sequence[tuple] = (
    ("SPEC-101", "缺少 frontmatter（按 legacy 处理，仅告警）"),
    ("SPEC-102", "frontmatter 缺少必需字段"),
    ("SPEC-103", "status 不在五态枚举内"),
    ("SPEC-104", "risk 不在 low/medium/high 内"),
    ("SPEC-105", "缺少必需章节"),
    ("SPEC-106", "章节顺序不符合契约"),
    ("SPEC-107", "frontmatter 的 feature 与目录名不一致"),
    ("SPEC-201", "验收表表头不等于规范形状"),
    ("SPEC-202", "S 或 R 编号重复"),
    ("SPEC-203", "任务引用了不存在的 R 编号"),
    ("SPEC-204", "存在没有任何任务覆盖的 R 编号"),
    ("SPEC-205", "存在未被任何 R 引用的用户故事"),
    ("SPEC-206", "验收行的验证列为空"),
    ("SPEC-207", "验收行引用了未定义的用户故事"),
    ("SPEC-301", "任务行不符合单行模板"),
    ("SPEC-302", "任务编号重复或不从 1 连续递增"),
    ("SPEC-303", "review 阶段仍有未勾选任务"),
    ("SPEC-304", "指定的任务编号不存在"),
    ("SPEC-305", "任务行 checkbox 无法安全翻转"),
    ("SPEC-401", "执行记录缺少四行字段之一"),
    ("SPEC-402", "执行记录状态值不合法"),
    ("SPEC-403", "review 阶段验证列未给出提交"),
    ("SPEC-404", "验证列引用的提交不存在或不是 HEAD 祖先"),
    ("SPEC-405", "执行记录超过 5 行"),
    ("SPEC-501", "目标与范围超过 2 行"),
    ("SPEC-502", "验收行超过 12 行"),
    ("SPEC-503", "决策超过 5 行"),
    ("SPEC-504", "风险超过 3 行"),
    ("SPEC-505", "任务超过 12 行"),
    ("SPEC-506", "执行记录超过 5 行"),
    ("SPEC-601", "已交付规范仍含任务章节"),
    ("SPEC-602", "已交付规范仍含 //TODO"),
    ("SPEC-603", "已交付规范仍含未勾选任务"),
    ("SPEC-604", "已交付规范缺少 delivered_at"),
    ("SPEC-605", "supersedes 指向的规范不存在"),
    ("SPEC-701", "工作区存在未提交改动"),
)


@dataclass
class CheckReport:
    violations: List[Violation] = field(default_factory=list)
    warnings: List[Violation] = field(default_factory=list)
    legacy: bool = False

    @property
    def ok(self) -> bool:
        return not self.violations


def _add(report: CheckReport, code: str, message: str, spec: Spec, line: Optional[int] = None) -> None:
    path = str(spec.path) if spec.path else None
    report.violations.append(Violation(code, message, path, line))


def _warn(report: CheckReport, code: str, message: str, spec: Spec) -> None:
    path = str(spec.path) if spec.path else None
    report.warnings.append(Violation(code, message, path))


def check_spec(
    spec: Spec,
    stage: str,
    root: Optional[Path] = None,
    require_clean: bool = False,
) -> CheckReport:
    report = CheckReport()

    if not spec.has_frontmatter or "feature" not in spec.fields:
        report.legacy = True
        _warn(
            report,
            "SPEC-101",
            "缺少 frontmatter；按 legacy 规范处理，不做形状判定。",
            spec,
        )
        return report

    for key in REQUIRED_FIELDS:
        if key not in spec.fields:
            _add(report, "SPEC-102", f"frontmatter 缺少字段 {key}", spec)
    status = spec.field("status")
    if status and status not in STATUSES:
        _add(report, "SPEC-103", f"status 不合法：{status}", spec)
    risk = spec.field("risk")
    if risk and risk not in RISKS:
        _add(report, "SPEC-104", f"risk 不合法：{risk}", spec)
    if spec.path is not None and spec.field("feature") != spec.path.parent.name:
        _add(
            report,
            "SPEC-107",
            f"feature 与目录名不一致：{spec.field('feature')} != {spec.path.parent.name}",
            spec,
        )

    _check_sections(spec, stage, report, require_tasks=stage != "delivered")
    _check_acceptance(spec, report)
    _check_tasks(spec, report)
    _check_budgets(spec, report)

    if stage == "review":
        _check_review(spec, report, root)
    elif stage == "delivered":
        _check_delivered(spec, report)

    if require_clean and root is not None and gitx.is_repository(root) and gitx.is_dirty(root):
        _add(report, "SPEC-701", "工作区存在未提交改动", spec)

    return report


def _check_sections(spec: Spec, stage: str, report: CheckReport, require_tasks: bool) -> None:
    spans = spec.section_spans()
    required = list(CONTRACT_SECTIONS) + ["执行记录"]
    if require_tasks:
        required.insert(len(CONTRACT_SECTIONS), "任务")
    for name in required:
        if name not in spans:
            _add(report, "SPEC-105", f"缺少章节：## {name}", spec)

    actual_order = [name for name in spans if name in CANONICAL_ORDER]
    expected_order = [name for name in CANONICAL_ORDER if name in spans]
    if actual_order != expected_order:
        _add(
            report,
            "SPEC-106",
            f"章节顺序不符合契约：期望 {' > '.join(expected_order)}，实际 {' > '.join(actual_order)}",
            spec,
        )

    if stage == "delivered":
        for name in ("任务",):
            if name in spans:
                _add(report, "SPEC-601", f"已交付规范仍含章节：## {name}", spec, spans[name][0] + 1)


def _check_acceptance(spec: Spec, report: CheckReport) -> None:
    if "验收标准" not in spec.section_spans():
        return
    header, rows, lines = spec.table_rows("验收标准", expected_header=ACCEPTANCE_HEADER)
    if header != ACCEPTANCE_HEADER:
        _add(report, "SPEC-201", f"验收表表头必须为 | {' | '.join(ACCEPTANCE_HEADER)} |", spec)

    story_ids = [
        match.group(1)
        for line in spec.section_body("用户故事")
        for match in SID_RE.finditer(line)
    ]
    stories = set(story_ids)
    for story_id in sorted({value for value in story_ids if story_ids.count(value) > 1}):
        _add(report, "SPEC-202", f"用户故事编号重复：{story_id}", spec)
    seen_criteria: set = set()
    referenced_stories: set = set()
    for offset, row in enumerate(rows):
        line_number = lines[offset] if offset < len(lines) else None
        if len(row) != 6:
            _add(report, "SPEC-201", f"验收行列数为 {len(row)}，应为 6 列", spec, line_number)
            continue
        criterion = row[0]
        story = row[1]
        if criterion in seen_criteria:
            _add(report, "SPEC-202", f"验收编号重复：{criterion}", spec, line_number)
        seen_criteria.add(criterion)
        for story_id in re.findall(r"S\d+", story):
            referenced_stories.add(story_id)
        if not row[5] or row[5] in {"-", "—"}:
            _add(report, "SPEC-206", f"{criterion} 的验证列为空", spec, line_number)

    for story_id in sorted(stories - referenced_stories):
        _add(report, "SPEC-205", f"用户故事 {story_id} 未被任何验收行引用", spec)

    for story_id in sorted(referenced_stories - stories):
        _add(report, "SPEC-207", f"验收行引用了未定义的用户故事 {story_id}", spec)


def _check_tasks(spec: Spec, report: CheckReport) -> None:
    if "任务" not in spec.section_spans():
        return
    for line_number, raw in spec.malformed_task_lines():
        _add(report, "SPEC-301", f"任务行不符合模板：{raw.strip()}", spec, line_number)

    tasks = spec.tasks()
    numbers = [task.number for task in tasks]
    if numbers and numbers != list(range(1, len(numbers) + 1)):
        _add(report, "SPEC-302", f"任务编号必须从 1 连续递增，实际：{numbers}", spec)

    criteria = {
        row[0]
        for row in spec.table_rows("验收标准", expected_header=ACCEPTANCE_HEADER)[1]
        if row
    }
    covered = {rid for task in tasks for rid in task.rids}
    for task in tasks:
        for rid in task.rids:
            if rid not in criteria:
                _add(report, "SPEC-203", f"任务 {task.number} 引用了不存在的验收编号 {rid}", spec, task.index + 1)
    for rid in sorted(criteria - covered):
        _add(report, "SPEC-204", f"验收编号 {rid} 没有被任何任务覆盖", spec)


def _check_budgets(spec: Spec, report: CheckReport) -> None:
    for section, (limit, code) in BUDGETS.items():
        if section not in spec.section_spans():
            continue
        body = spec.section_body(section)
        if section == "目标与范围":
            count = len([line for line in body if not line.startswith("|")])
        elif section == "执行记录":
            count = len([line for line in body if line.startswith("-")])
        else:
            header, rows, _ = spec.table_rows(section)
            count = len(rows) if section != "任务" else len(spec.tasks())
        if count > limit:
            _add(report, code, f"{section} 共 {count} 项，超过预算 {limit}", spec)


def _check_review(spec: Spec, report: CheckReport, root: Optional[Path]) -> None:
    tasks = spec.tasks()
    for task in tasks:
        if not task.checked:
            _add(report, "SPEC-303", f"任务 {task.number} 尚未勾选", spec, task.index + 1)

    values = spec.execution_fields()
    for field_name in EXECUTION_FIELDS:
        if field_name not in values or not values[field_name]:
            _add(report, "SPEC-401", f"执行记录缺少字段：{field_name}", spec)
    state = values.get("状态", "")
    if state and state not in EVIDENCE_STATES:
        _add(report, "SPEC-402", f"执行记录状态不合法：{state}", spec)

    tested = values.get("验证", "")
    if not tested:
        return
    if "无提交" in tested:
        return
    match = COMMIT_RE.search(tested)
    if not match:
        _add(report, "SPEC-403", "review 阶段的验证列必须给出被测提交", spec)
        return
    revision = match.group(0)
    if root is None or not gitx.is_repository(root):
        return
    if not gitx.has_commit(root, revision):
        _add(report, "SPEC-404", f"验证列引用的提交不存在：{revision}", spec)
    elif not gitx.is_ancestor(root, revision):
        _add(report, "SPEC-404", f"验证列引用的提交不是 HEAD 祖先：{revision}", spec)


def _check_delivered(spec: Spec, report: CheckReport) -> None:
    text = spec.text
    if "//TODO" in text:
        line = next(
            (index + 1 for index, value in enumerate(spec.lines) if "//TODO" in value),
            None,
        )
        _add(report, "SPEC-602", "已交付规范仍含 //TODO", spec, line)
    for index, line in enumerate(spec.lines):
        if line.strip().startswith("- [ ]"):
            _add(report, "SPEC-603", "已交付规范仍含未勾选任务", spec, index + 1)
    delivered_at = spec.field("delivered_at")
    if delivered_at in ("", "null", "~"):
        _add(report, "SPEC-604", "已交付规范缺少 delivered_at", spec)


def sensitive_hits(text: str) -> List[str]:
    return sorted({match.group(0) for match in SENSITIVE_RE.finditer(text)})
