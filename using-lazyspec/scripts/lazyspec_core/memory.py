"""Feature Capsule parsing, deterministic index generation, and bounded recall."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from .specmd import HEADING_RE, parse_list, parse_scalar, split_row
from .util import Violation

CAPSULE_REQUIRED = (
    "feature",
    "status",
    "summary",
    "source_spec",
    "distilled_at",
    "reviewed_at",
    "tags",
    "authorities",
)
CAPSULE_STATUSES = {"active", "needs-review", "superseded", "obsolete"}
CAPSULE_SECTIONS = ("Purpose", "Durable Decisions", "Guardrails", "Revisit When", "Sources")
FACT_SECTIONS = ("Purpose", "Durable Decisions", "Guardrails")
INDEX_MARKER = "<!-- Generated from Capsule metadata; do not edit manually. -->"
INDEX_HEADER = ["Memory", "Summary", "Tags", "Status", "Source Spec", "Reviewed"]
INDEX_ROW_RE = re.compile(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*(.*?)\s*\|$")
SOURCE_ID_RE = re.compile(r"\[S\d+\]")
DECISION_ID_RE = re.compile(r"^- (D\d+) —")
SOURCE_LINE_RE = re.compile(r"^- S\d+:\s*`([^`]+)`")
D_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Capsule:
    path: Path
    text: str
    fields: Dict[str, str]
    lines: List[str]
    frontmatter_end: int
    defects: List[Tuple[str, str]] = field(default_factory=list)

    @property
    def feature(self) -> str:
        return self.fields.get("feature", "")

    @property
    def status(self) -> str:
        return self.fields.get("status", "")

    def sections(self) -> Dict[str, Tuple[int, int]]:
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

    def body_lines(self, name: str) -> List[str]:
        spans = self.sections()
        if name not in spans:
            return []
        start, end = spans[name]
        return [line.strip() for line in self.lines[start + 1 : end] if line.strip()]


def parse_capsule(path: Path) -> Capsule:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    fields: Dict[str, str] = {}
    frontmatter_end = 0
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() != "---":
                continue
            frontmatter_end = index + 1
            for line_index in range(1, index):
                line = lines[line_index]
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                key = key.strip()
                if key and not key.startswith("#"):
                    fields[key] = parse_scalar(value)
            break
    return Capsule(path=path, text=text, fields=fields, lines=lines, frontmatter_end=frontmatter_end)


def capsule_paths(root: Path) -> List[Path]:
    directory = root / "project-memory" / "features"
    if not directory.is_dir():
        return []
    return sorted(path for path in directory.glob("*.md") if path.is_file())


def read_capsules(root: Path) -> List[Capsule]:
    return [parse_capsule(path) for path in capsule_paths(root)]


def render_index(capsules: Iterable[Capsule]) -> str:
    ordered = sorted(capsules, key=lambda item: (item.feature, item.path.name))
    lines = [
        "# Project Memory Index",
        "",
        INDEX_MARKER,
        "",
        "| " + " | ".join(INDEX_HEADER) + " |",
        "|" + "|".join(["---"] * len(INDEX_HEADER)) + "|",
    ]
    for capsule in ordered:
        feature = capsule.feature
        display = f"project-memory/features/{capsule.path.name}"
        link = f"./features/{capsule.path.name}"
        source = capsule.fields.get("source_spec", f"specs/{feature}/")
        source_link = "../" + source.lstrip("./")
        tags = ", ".join(parse_list(capsule.fields.get("tags", "")))
        lines.append(
            f"| [{display}]({link}) | {capsule.fields.get('summary', '')} | "
            f"{tags} | {capsule.status} | "
            f"[{source}]({source_link}) | {capsule.fields.get('reviewed_at', '')} |"
        )
    return "\n".join(lines) + "\n"


def assemble_index_text(root: Path) -> str:
    return render_index(read_capsules(root))


def index_drift(root: Path) -> Optional[str]:
    index = root / "project-memory" / "index.md"
    expected = assemble_index_text(root)
    if not index.is_file():
        return expected
    actual = index.read_text(encoding="utf-8")
    return None if actual == expected else expected


def check_capsule(capsule: Capsule, strict_paths: bool = False) -> List[Violation]:
    violations: List[Violation] = []
    path = str(capsule.path)

    def add(code: str, message: str) -> None:
        violations.append(Violation(code, message, path))

    for key in CAPSULE_REQUIRED:
        if key not in capsule.fields:
            add("MEM-101", f"Capsule 缺少必需字段 {key}")

    if capsule.status not in CAPSULE_STATUSES:
        add("MEM-103", f"status 不合法：{capsule.status or '(空)'}")

    feature = capsule.fields.get("feature", "")
    if feature and feature != capsule.path.stem:
        add("MEM-102", f"feature 与文件名不一致：{feature} != {capsule.path.stem}")
    source_spec = capsule.fields.get("source_spec", "")
    if feature and source_spec and source_spec.strip("/") != f"specs/{feature}":
        add("MEM-102", f"source_spec 与 feature 不一致：{source_spec}")

    reviewed_at = capsule.fields.get("reviewed_at", "")
    if reviewed_at and not D_DATE_RE.match(reviewed_at):
        add("MEM-107", f"reviewed_at 不是 YYYY-MM-DD：{reviewed_at}")

    status = capsule.status
    if status != "active" and not capsule.fields.get("status_reason"):
        add("MEM-104", "非 active 状态必须提供 status_reason")
    if status == "superseded" and not parse_list(capsule.fields.get("superseded_by", "")):
        add("MEM-105", "superseded 状态必须提供 superseded_by")
    if status != "superseded" and parse_list(capsule.fields.get("superseded_by", "")):
        add("MEM-106", "只有 superseded 状态可以包含 superseded_by")

    spans = capsule.sections()
    missing = [name for name in CAPSULE_SECTIONS if name not in spans]
    for name in missing:
        add("MEM-201", f"缺少章节：## {name}")
    present = [name for name in spans if name in CAPSULE_SECTIONS]
    if present != [name for name in CAPSULE_SECTIONS if name in spans]:
        add("MEM-201", "Capsule 章节顺序不符合契约")

    decisions: List[str] = []
    for section in FACT_SECTIONS:
        for line in capsule.body_lines(section):
            if not line.startswith("- "):
                continue
            if not SOURCE_ID_RE.search(line):
                add("MEM-202", f"{section} 条目缺少来源 ID：{line}")
            if section == "Durable Decisions":
                match = DECISION_ID_RE.match(line)
                if match:
                    decisions.append(match.group(1))
    duplicates = sorted({value for value in decisions if decisions.count(value) > 1})
    for value in duplicates:
        add("MEM-203", f"决策编号重复：{value}")

    for line in capsule.body_lines("Sources"):
        match = SOURCE_LINE_RE.match(line)
        if not match:
            add("MEM-204", f"Sources 行格式不合法：{line}")
            continue
        if strict_paths:
            target = (capsule.path.parents[2] / match.group(1)).resolve()
            if not str(target).startswith(str(capsule.path.parents[2].resolve())):
                add("MEM-205", f"来源路径越出项目根：{match.group(1)}")
            elif not target.exists():
                add("MEM-205", f"来源路径不存在：{match.group(1)}")

    return violations


def check_memory(root: Path, strict_paths: bool = False) -> List[Violation]:
    capsules = read_capsules(root)
    violations: List[Violation] = []
    for capsule in capsules:
        violations.extend(check_capsule(capsule, strict_paths))
    violations.extend(check_supersession(capsules))
    violations.extend(check_index(root, capsules))
    return violations


def check_supersession(capsules: List[Capsule]) -> List[Violation]:
    by_path = {
        f"project-memory/features/{capsule.path.name}": capsule for capsule in capsules
    }
    violations: List[Violation] = []
    for key, capsule in by_path.items():
        for target in parse_list(capsule.fields.get("supersedes", "")):
            other = by_path.get(target)
            if other is None:
                violations.append(Violation("MEM-401", f"supersedes 指向不存在的 Capsule：{target}", str(capsule.path)))
                continue
            reciprocal = parse_list(other.fields.get("superseded_by", ""))
            if key not in reciprocal:
                violations.append(
                    Violation("MEM-401", f"{key} 的 supersedes 缺少对端 superseded_by：{target}", str(capsule.path))
                )

    state: Dict[str, int] = {}

    def visit(key: str, trail: List[str]) -> None:
        if state.get(key) == 1:
            violations.append(
                Violation("MEM-402", "supersession 形成环：" + " -> ".join(trail + [key]), str(by_path[key].path))
            )
            return
        if state.get(key) == 2:
            return
        state[key] = 1
        for target in parse_list(by_path[key].fields.get("supersedes", "")):
            if target in by_path:
                visit(target, trail + [key])
        state[key] = 2

    for key in by_path:
        visit(key, [])
    return violations


def check_index(root: Path, capsules: List[Capsule]) -> List[Violation]:
    index = root / "project-memory" / "index.md"
    if not index.is_file():
        return [Violation("MEM-301", "缺少 project-memory/index.md", str(index))]
    expected = render_index(capsules)
    actual = index.read_text(encoding="utf-8")
    if actual == expected:
        return []

    violations: List[Violation] = []
    if INDEX_MARKER not in actual:
        violations.append(Violation("MEM-301", "index.md 缺少生成标记", str(index)))
    rows = parse_index_rows(actual)
    declared = {row["path"] for row in rows}
    actual_capsules = {f"project-memory/features/{capsule.path.name}" for capsule in capsules}
    for missing in sorted(actual_capsules - declared):
        violations.append(Violation("MEM-301", f"index 缺少行：{missing}", str(index)))
    for extra in sorted(declared - actual_capsules):
        violations.append(Violation("MEM-301", f"index 存在多余行：{extra}", str(index)))
    if not violations:
        violations.append(Violation("MEM-301", "index 内容与 Capsule 元数据不一致（内容或顺序漂移）", str(index)))
    return violations


def parse_index_rows(text: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for line in text.splitlines():
        if not line.startswith("| ["):
            continue
        match = INDEX_ROW_RE.match(line.strip())
        if not match:
            continue
        rows.append(
            {
                "path": match.group(1),
                "link": match.group(2),
                "summary": match.group(3),
                "tags": match.group(4),
                "status": match.group(5),
                "source_spec": match.group(6),
                "source_link": match.group(7),
                "reviewed_at": match.group(8),
            }
        )
    return rows


def index_is_well_formed(text: str) -> List[str]:
    problems: List[str] = []
    lines = text.splitlines()
    if INDEX_MARKER not in text:
        problems.append("缺少生成标记")
    header = next((line for line in lines if line.startswith("| Memory |")), None)
    if header is None:
        problems.append("缺少六列表头")
    else:
        cells = split_row(header)
        if cells != INDEX_HEADER:
            problems.append(f"表头列不匹配：{cells}")
    return problems


def _tokens(query: str) -> List[str]:
    return [token for token in re.split(r"[\s,，、;；]+", query.lower()) if token]


def _score(row: Dict[str, str], tokens: List[str], query: str) -> int:
    feature = Path(row["path"]).stem.lower()
    tags = row["tags"].lower()
    summary = row["summary"].lower()
    source = row["source_spec"].lower()
    score = 0
    if query and query in feature:
        score += 16
    for token in tokens:
        if token in feature:
            score += 8
        if token in tags:
            score += 4
        if token in summary:
            score += 2
        if token in source:
            score += 1
    return score


def _safe_capsule_path(root: Path, display: str) -> Tuple[Optional[Path], Optional[str]]:
    if display.startswith("/") or display.startswith("~"):
        return None, "绝对路径被拒绝"
    parts = Path(display).parts
    if ".." in parts:
        return None, "包含 .. 上溯被拒绝"
    allowed = (root / "project-memory" / "features").resolve()
    raw = root / display
    if raw.is_symlink():
        return None, "符号链接被拒绝"
    candidate = raw.resolve()
    try:
        candidate.relative_to(allowed)
    except ValueError:
        return None, "路径越出 project-memory/features/"
    if not candidate.is_file():
        return None, "Capsule 文件不存在"
    return candidate, None


def recall(
    root: Path,
    query: str,
    limit: int = 3,
    include_non_active: bool = False,
) -> Tuple[Dict[str, object], List[str]]:
    index = root / "project-memory" / "index.md"
    warnings: List[str] = []
    payload: Dict[str, object] = {"query": query, "memories": []}
    if not index.is_file():
        return payload, warnings

    text = index.read_text(encoding="utf-8")
    problems = index_is_well_formed(text)
    if problems:
        warnings.extend(f"索引格式异常：{problem}" for problem in problems)
        return payload, warnings

    rows = parse_index_rows(text)
    tokens = _tokens(query)
    lowered = query.lower()
    ranked = []
    for row in rows:
        capsule, reason = _safe_capsule_path(root, row["path"])
        if capsule is None:
            warnings.append(f"跳过 {row['path']}：{reason}")
            continue
        capsule_meta = parse_capsule(capsule)
        if capsule_meta.fields.get("feature") != capsule.stem:
            warnings.append(f"跳过 {row['path']}：feature 与文件名不一致")
            continue
        if not capsule_meta.fields.get("reviewed_at") or not capsule_meta.fields.get("authorities"):
            warnings.append(f"跳过 {row['path']}：缺少 reviewed_at 或 authorities")
            continue
        if not include_non_active and row["status"] != "active":
            continue
        score = _score(row, tokens, lowered)
        if score <= 0:
            continue
        ranked.append((score, row["path"], row))
    ranked.sort(key=lambda item: (-item[0], item[1]))

    selected = ranked[:limit]
    for _score_value, _path, row in selected:
        capsule, _reason = _safe_capsule_path(root, row["path"])
        if capsule is None:
            continue
        capsule_meta = parse_capsule(capsule)
        relevant: List[str] = []
        for section in FACT_SECTIONS:
            body = " ".join(capsule_meta.body_lines(section)).lower()
            if any(token in body for token in tokens):
                relevant.append(section)
        entry = {
            "path": row["path"],
            "status": row["status"],
            "sourceSpec": row["source_spec"],
            "reviewedAt": row["reviewed_at"],
            "authorities": parse_list(capsule_meta.fields.get("authorities", "")),
            "relevantSections": relevant,
        }
        if row["status"] != "active":
            entry["warning"] = "非 active 记忆，不是当前事实"
        payload["memories"].append(entry)

    if len(ranked) > limit:
        warnings.append(f"另有 {len(ranked) - limit} 条匹配未展示。")
    payload["omitted"] = max(0, len(ranked) - limit)
    return payload, warnings
