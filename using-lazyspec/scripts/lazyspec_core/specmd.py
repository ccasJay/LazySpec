"""Parse and edit the single `spec.md` artifact.

Edits are position-preserving: unchanged lines are written back byte for byte,
so the approved contract never drifts because of a parser round trip.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

FRONTMATTER_DELIMITER = "---"
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
TASK_RE = re.compile(r"^- \[(?P<box>[ xX])\] //TODO (?P<number>\d+)\.\s*(?P<rest>.*)$")
RID_RE = re.compile(r"R\d+(?:\.\d+)*")
SID_RE = re.compile(r"\*\*(S\d+)\*\*")
ACCEPTANCE_HEADER = ["ID", "故事", "类型", "当", "系统应", "验证"]
EXECUTION_FIELDS = ("状态", "验证", "结果", "未决")


def parse_scalar(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_list(raw: str) -> List[str]:
    value = (raw or "").strip()
    if value in ("", "[]", "null", "~"):
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item) for item in inner.split(",") if item.strip()]
    return [parse_scalar(value)]


def render_list(values: List[str]) -> str:
    return "[" + ", ".join(values) + "]"


def split_row(line: str) -> List[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator_row(line: str) -> bool:
    stripped = line.strip()
    return bool(stripped) and set(stripped) <= set("|-: ")


@dataclass
class Task:
    index: int
    number: int
    checked: bool
    text: str
    raw: str
    rids: List[str]

    @property
    def behavior(self) -> str:
        head = self.text.split("→", 1)[0].strip()
        return head or self.text.strip()


class Spec:
    """Mutable, position-preserving view of one `spec.md`."""

    def __init__(self, text: str, path: Optional[Path] = None) -> None:
        self.path = path
        self.lines: List[str] = text.splitlines(keepends=True)
        self.has_frontmatter = False
        self.fields: Dict[str, str] = {}
        self.field_lines: Dict[str, int] = {}
        self.frontmatter_end = 0
        self._parse_frontmatter()

    # -- frontmatter ----------------------------------------------------

    def _parse_frontmatter(self) -> None:
        self.has_frontmatter = False
        self.fields = {}
        self.field_lines = {}
        self.frontmatter_end = 0
        if not self.lines or self.lines[0].strip() != FRONTMATTER_DELIMITER:
            return
        for index in range(1, len(self.lines)):
            if self.lines[index].strip() != FRONTMATTER_DELIMITER:
                continue
            self.has_frontmatter = True
            self.frontmatter_end = index + 1
            for line_index in range(1, index):
                line = self.lines[line_index]
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                if not key or key.startswith("#"):
                    continue
                self.fields[key] = parse_scalar(value)
                self.field_lines[key] = line_index
            return

    def field(self, key: str, default: str = "") -> str:
        return self.fields.get(key, default)

    def list_field(self, key: str) -> List[str]:
        return parse_list(self.fields.get(key, "[]"))

    def set_field(self, key: str, value: str) -> None:
        if key in self.field_lines:
            self.lines[self.field_lines[key]] = f"{key}: {value}\n"
            self._parse_frontmatter()
            return
        insert_at = max(self.frontmatter_end - 1, 1)
        if not self.lines[insert_at - 1].endswith("\n"):
            self.lines[insert_at - 1] += "\n"
        self.lines.insert(insert_at, f"{key}: {value}\n")
        self._parse_frontmatter()

    # -- sections -------------------------------------------------------

    def section_spans(self) -> Dict[str, Tuple[int, int]]:
        headings: List[Tuple[str, int]] = []
        for index in range(self.frontmatter_end, len(self.lines)):
            match = HEADING_RE.match(self.lines[index])
            if match:
                headings.append((match.group(1), index))
        spans: Dict[str, Tuple[int, int]] = {}
        for position, (name, start) in enumerate(headings):
            end = headings[position + 1][1] if position + 1 < len(headings) else len(self.lines)
            spans[name] = (start, end)
        return spans

    def has_section(self, name: str) -> bool:
        return name in self.section_spans()

    def section_lines(self, name: str) -> List[str]:
        start, end = self.section_spans()[name]
        return self.lines[start + 1 : end]

    def section_body(self, name: str) -> List[str]:
        return [line.strip() for line in self.section_lines(name) if line.strip()]

    def set_section_body(self, name: str, body: List[str]) -> None:
        start, end = self.section_spans()[name]
        self.lines[start + 1 : end] = body

    def delete_section(self, name: str) -> None:
        start, end = self.section_spans()[name]
        if start > 0 and not self.lines[start - 1].strip():
            start -= 1
        del self.lines[start:end]

    def insert_after_frontmatter(self, block: List[str]) -> None:
        insert_at = self.frontmatter_end
        while insert_at < len(self.lines) and not self.lines[insert_at].strip():
            insert_at += 1
        self.lines[insert_at:insert_at] = block

    # -- tables ---------------------------------------------------------

    def table_rows(self, section: str, expected_header: Optional[List[str]] = None) -> Tuple[List[str], List[List[str]], List[int]]:
        if section not in self.section_spans():
            return [], [], []
        start, end = self.section_spans()[section]
        rows: List[List[str]] = []
        line_numbers: List[int] = []
        header: List[str] = []
        seen_header = False
        for index in range(start + 1, end):
            line = self.lines[index]
            if not line.strip().startswith("|"):
                if rows:
                    break
                continue
            if not seen_header:
                header = split_row(line)
                seen_header = True
                continue
            if is_separator_row(line):
                continue
            rows.append(split_row(line))
            line_numbers.append(index + 1)
        if expected_header is not None and header and header != expected_header:
            return header, rows, line_numbers
        return header, rows, line_numbers

    # -- tasks ----------------------------------------------------------

    def tasks(self) -> List[Task]:
        if "任务" not in self.section_spans():
            return []
        start, end = self.section_spans()["任务"]
        found: List[Task] = []
        for index in range(start + 1, end):
            match = TASK_RE.match(self.lines[index])
            if not match:
                continue
            rest = match.group("rest").strip()
            found.append(
                Task(
                    index=index,
                    number=int(match.group("number")),
                    checked=match.group("box").lower() == "x",
                    text=rest,
                    raw=self.lines[index],
                    rids=RID_RE.findall(rest),
                )
            )
        return found

    def malformed_task_lines(self) -> List[Tuple[int, str]]:
        if "任务" not in self.section_spans():
            return []
        start, end = self.section_spans()["任务"]
        found: List[Tuple[int, str]] = []
        for index in range(start + 1, end):
            line = self.lines[index]
            if not line.strip().startswith("- ["):
                continue
            if not TASK_RE.match(line):
                found.append((index + 1, line.rstrip("\n")))
        return found

    def check_task(self, number: int) -> bool:
        for task in self.tasks():
            if task.number != number:
                continue
            if task.checked:
                return False
            original = self.lines[task.index]
            if original.count("[ ]") != 1:
                raise ValueError(f"任务行包含多个未勾选标记：{original!r}")
            updated = original.replace("[ ]", "[x]", 1)
            if len(updated) != len(original) or updated.count("[x]") != original.count("[x]") + 1:
                raise ValueError(f"checkbox 替换未保持其余字符：{original!r}")
            self.lines[task.index] = updated
            return True
        return False

    # -- execution record ----------------------------------------------

    def execution_fields(self) -> Dict[str, str]:
        values: Dict[str, str] = {}
        if "执行记录" not in self.section_spans():
            return values
        for line in self.section_body("执行记录"):
            if not line.startswith("-"):
                continue
            body = line[1:].strip()
            if "：" not in body:
                continue
            key, value = body.split("：", 1)
            values[key.strip()] = value.strip()
        return values

    def set_execution_record(self, state: str, tested: str, result: str, unresolved: str) -> None:
        self.set_section_body(
            "执行记录",
            [
                "\n",
                f"- 状态：{state}\n",
                f"- 验证：{tested}\n",
                f"- 结果：{result}\n",
                f"- 未决：{unresolved}\n",
            ],
        )

    # -- output ---------------------------------------------------------

    @property
    def text(self) -> str:
        return "".join(self.lines)
