"""Command implementations and the argparse registry shared by all entry points."""

from __future__ import annotations

import argparse
import difflib
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import gitx, memory, scan
from .checks import CODE_CATALOG, EVIDENCE_STATES, check_spec, sensitive_hits
from .specmd import Spec, parse_list
from .util import (
    EXIT_REFUSED,
    EXIT_USAGE,
    EXIT_VIOLATION,
    LazyspecError,
    Result,
    Violation,
    VERSION,
    atomic_write,
    emit,
    read_text,
    resolve_root,
    spec_path,
    validate_feature,
)

DEFAULT_BRANCH = "feat/{feature}"
BASE_BRANCH = "dev"


# -- shared helpers -----------------------------------------------------


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".", help="项目根目录，默认当前目录")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")


def _load_spec(root: Path, feature: str) -> Tuple[Path, Spec]:
    path = spec_path(root, feature)
    return path, Spec(read_text(path), path)


def _commit_message(feature: str, numbers: List[int], behavior: str) -> str:
    label = ",".join(str(number) for number in numbers)
    summary = behavior.strip()[:72]
    return f"feat({feature}): TODO {label} {summary}".strip()


# -- check -------------------------------------------------------------


def add_check(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--feature", help="功能目录名")
    parser.add_argument("--stage", choices=("plan", "review", "delivered"), default="plan")
    parser.add_argument("--require-clean", action="store_true", help="要求工作区无未提交改动")
    parser.add_argument("--list-codes", action="store_true", help="列出全部错误码")


def run_check(args: argparse.Namespace) -> Result:
    if args.list_codes:
        lines = [f"{code}\t{message}" for code, message in CODE_CATALOG]
        return Result(data={"codes": [{"code": c, "message": m} for c, m in CODE_CATALOG]}, human=lines)
    if not args.feature:
        raise LazyspecError("ENV-102", "--feature 必填", EXIT_USAGE)
    root = resolve_root(args.root)
    path, spec = _load_spec(root, args.feature)
    report = check_spec(spec, args.stage, root, args.require_clean)
    if report.ok:
        human = [f"规范检查（{args.stage}）通过：{path}"]
        if report.legacy:
            human.append("该文件为 legacy 格式，仅校验可读结构。")
        return Result(
            data={
                "stage": args.stage,
                "feature": args.feature,
                "legacy": report.legacy,
                "violation_count": 0,
                "warning_count": len(report.warnings),
            },
            warnings=report.warnings,
            human=human,
        )
    return Result(
        data={
            "stage": args.stage,
            "feature": args.feature,
            "legacy": report.legacy,
            "violation_count": len(report.violations),
            "warning_count": len(report.warnings),
        },
        violations=report.violations,
        warnings=report.warnings,
        human=[f"规范检查（{args.stage}）未通过：{len(report.violations)} 项"],
        exit_code=EXIT_VIOLATION,
    )


# -- recall ------------------------------------------------------------


def add_recall(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--include-non-active", action="store_true")


def run_recall(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    payload, warnings = memory.recall(root, args.query, args.limit, args.include_non_active)
    human = [f"记忆候选：{len(payload['memories'])} 条"]
    for entry in payload["memories"]:
        human.append(f"- {entry['path']} [{entry['status']}]")
    human.extend(warnings)
    return Result(
        data=payload,
        warnings=[Violation("MEM-206", warning) for warning in warnings],
        human=human,
    )


# -- scan-retired ------------------------------------------------------


def add_scan_retired(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)


def run_scan_retired(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    entries = scan.scan_retired(root)
    human = [f"已退役规范：{len(entries)} 份"] + [
        f"- {entry['feature']}：{entry['title']}" for entry in entries
    ]
    return Result(data={"retired": entries}, human=human)


# -- scan-specs --------------------------------------------------------


def add_scan_specs(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--changed", action="store_true", help="只扫描未提交改动")
    parser.add_argument("--since", help="与指定 revision 比对内容哈希")
    parser.add_argument("--feature", help="排除当前 Spec 的 feature 名")


def run_scan_specs(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    if not args.changed:
        raise LazyspecError("ENV-120", "当前只支持 --changed", EXIT_USAGE)
    entries = scan.scan_changed(root, args.feature, args.since)
    human = [f"发现的候选 Spec：{len(entries)} 份"]
    for entry in entries:
        suffix = f" content={entry.content_change}" if entry.content_change else ""
        human.append(f"- {entry.path} [{entry.status}]{suffix} sha256={entry.sha256 or '-'}")
    return Result(data={"specs": [entry.as_dict() for entry in entries]}, human=human)


# -- task-done ---------------------------------------------------------


def add_task_done(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--n", type=int, action="append", required=True, dest="numbers")
    parser.add_argument("--commit", action="store_true", help="勾选后立即提交")
    parser.add_argument("--paths", nargs="+", action="extend", default=[], help="随本次提交的改动文件")
    parser.add_argument("--message", help="覆盖默认提交信息")


def run_task_done(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    feature = validate_feature(args.feature)
    path, spec = _load_spec(root, feature)
    tasks = {task.number: task for task in spec.tasks()}
    missing = [number for number in args.numbers if number not in tasks]
    if missing:
        raise LazyspecError("SPEC-304", f"任务不存在：{missing}", EXIT_VIOLATION)

    already = [number for number in args.numbers if tasks[number].checked]
    flipped: List[int] = []
    behavior = ""
    for number in args.numbers:
        if number in already:
            continue
        try:
            changed = spec.check_task(number)
        except ValueError as error:
            raise LazyspecError("SPEC-305", str(error), EXIT_VIOLATION)
        if changed:
            flipped.append(number)
            if not behavior:
                behavior = tasks[number].behavior

    if flipped:
        atomic_write(path, spec.text)

    relative_spec = path.relative_to(root).as_posix()
    commit_sha = None
    if args.commit and flipped:
        allowed = {relative_spec, *args.paths}
        unrelated = [item for item in gitx.staged_paths(root) if item not in allowed]
        if unrelated:
            raise LazyspecError(
                "ENV-121",
                f"暂存区存在与本次任务无关的改动：{unrelated}",
                EXIT_REFUSED,
            )
        gitx.add(root, [relative_spec, *args.paths])
        message = args.message or _commit_message(feature, flipped, behavior)
        commit_sha = gitx.commit(root, message)

    human = [f"任务 {args.numbers}：已勾选 {flipped or '无，已是最新'}"
             + (f"；提交 {commit_sha}" if commit_sha else "")]
    if already:
        human.append(f"已勾选跳过：{already}")
    return Result(
        data={
            "feature": feature,
            "completed": flipped,
            "already_done": already,
            "commit": commit_sha,
            "path": relative_spec,
        },
        human=human,
    )


# -- evidence ----------------------------------------------------------


def add_evidence(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--status", required=True, choices=sorted(EVIDENCE_STATES))
    parser.add_argument("--result", required=True, help="覆盖的 R 编号与观察结果")
    parser.add_argument("--unresolved", default="无")
    parser.add_argument("--commit", dest="revision", help="被测提交，默认 HEAD")
    parser.add_argument("--no-commit", action="store_true", help="显式记录为无提交")
    parser.add_argument("--commit-record", action="store_true", help="写入后立即提交执行记录")


def run_evidence(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    feature = validate_feature(args.feature)
    path, spec = _load_spec(root, feature)
    if not spec.has_section("执行记录"):
        raise LazyspecError("SPEC-105", "缺少 ## 执行记录 章节", EXIT_VIOLATION)

    if args.no_commit:
        tested = "无提交"
    elif args.revision:
        tested = args.revision
    else:
        tested = gitx.head_short(root) or "无提交"
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    spec.set_execution_record(args.status, f"{tested} · {timestamp}", args.result, args.unresolved)
    atomic_write(path, spec.text)

    commit_sha = None
    if args.commit_record:
        relative = path.relative_to(root).as_posix()
        unrelated = [item for item in gitx.staged_paths(root) if item != relative]
        if unrelated:
            raise LazyspecError("ENV-121", f"暂存区存在无关改动：{unrelated}", EXIT_REFUSED)
        gitx.add(root, [relative])
        commit_sha = gitx.commit(root, f"docs({feature}): record verification evidence")

    warnings = [
        Violation("SPEC-404", f"结果疑似包含敏感词：{hit}", str(path)) for hit in sensitive_hits(args.result)
    ]
    return Result(
        data={
            "feature": feature,
            "status": args.status,
            "tested_commit": tested,
            "verified_at": timestamp,
            "commit": commit_sha,
        },
        warnings=warnings,
        human=[f"执行记录已更新：{args.status} @ {tested}"
               + (f"（提交 {commit_sha}）" if commit_sha else "")],
    )


# -- deliver -----------------------------------------------------------


def add_deliver(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--feature", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--commit", action="store_true")


def run_deliver(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    feature = validate_feature(args.feature)
    path, spec = _load_spec(root, feature)
    report = check_spec(spec, "review", root)
    if report.violations:
        return Result(
            data={"feature": feature, "dry_run": args.dry_run, "violation_count": len(report.violations)},
            violations=report.violations,
            human=["交付前置检查未通过，未做任何修改。"],
            exit_code=EXIT_VIOLATION,
        )

    original = spec.text
    if spec.has_section("任务"):
        spec.delete_section("任务")
    values = spec.execution_fields()
    spec.set_execution_record(
        values.get("状态", "passed"),
        values.get("验证", ""),
        values.get("结果", ""),
        values.get("未决", "无"),
    )
    spec.set_field("status", "delivered")
    spec.set_field("delivered_at", datetime.now().date().isoformat())

    pending: List[Tuple[Path, str, str]] = [(path, original, spec.text)]
    superseded: List[str] = []
    for target in spec.list_field("supersedes"):
        target_dir = root / target.strip("/")
        target_path = target_dir / "spec.md"
        if not target_path.is_file():
            raise LazyspecError("SPEC-605", f"supersedes 指向的规范不存在：{target}", EXIT_VIOLATION)
        other = Spec(read_text(target_path), target_path)
        if feature in [item.strip("/") for item in other.list_field("supersedes")]:
            raise LazyspecError("MEM-402", f"supersession 形成环：{feature} ↔ {target}", EXIT_VIOLATION)
        other_original = other.text
        other.set_field("status", "superseded")
        other.set_field("superseded_by", f"specs/{feature}/")
        if "[!WARNING]" not in other.text:
            other.insert_after_frontmatter(
                ["\n", "> [!WARNING]\n", "> 本规范已被新规范废黜，请勿作为当前系统事实参考。\n", "\n"]
            )
        pending.append((target_path, other_original, other.text))
        superseded.append(target_dir.name)

    if args.dry_run:
        chunks: List[str] = []
        for target_path, before, after in pending:
            chunks.extend(
                difflib.unified_diff(
                    before.splitlines(keepends=True),
                    after.splitlines(keepends=True),
                    fromfile=str(target_path),
                    tofile=str(target_path) + " (delivered)",
                )
            )
        diff = "".join(chunks)
        return Result(
            data={"feature": feature, "dry_run": True, "diff": diff, "superseded": superseded},
            human=[diff] if diff else ["无差异。"],
        )

    for target_path, _before, after in pending:
        atomic_write(target_path, after)
    commits = None
    if args.commit:
        relatives = [item.relative_to(root).as_posix() for item, _before, _after in pending]
        allowed = set(relatives)
        unrelated = [item for item in gitx.staged_paths(root) if item not in allowed]
        if unrelated:
            raise LazyspecError("ENV-121", f"暂存区存在无关改动：{unrelated}", EXIT_REFUSED)
        gitx.add(root, relatives)
        commits = gitx.commit(root, f"docs({feature}): finalize delivered specification")

    return Result(
        data={
            "feature": feature,
            "dry_run": False,
            "superseded": superseded,
            "commit": commits,
        },
        human=[f"交付收口完成：{feature}" + (f"（提交 {commits}）" if commits else "")],
    )


# -- worktree ----------------------------------------------------------


def add_worktree(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("action", choices=("add", "remove"))
    parser.add_argument("--feature", required=True)
    parser.add_argument("--base", default=BASE_BRANCH)
    parser.add_argument("--branch", help="默认 feat/<feature>")
    parser.add_argument(
        "--keep-source",
        action="store_true",
        help="携带 spec 时保留主工作区副本",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="确认未跟踪文件为生成物后强制删除",
    )


def run_worktree(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    gitx.require_repository(root)
    feature = validate_feature(args.feature)
    path = root / ".worktrees" / feature

    if args.action == "add":
        if path.is_dir():
            return Result(
                data={"feature": feature, "path": str(path), "exists": True},
                human=[f"worktree 已存在：{path}"],
            )
        if not gitx.has_commit(root, args.base):
            raise LazyspecError("ENV-112", f"基线分支不存在：{args.base}")
        branch = args.branch or DEFAULT_BRANCH.format(feature=feature)
        if gitx.has_commit(root, branch):
            gitx.run(root, "worktree", "add", str(path), branch)
        else:
            gitx.run(root, "worktree", "add", "-b", branch, str(path), args.base)
        carried = _carry_spec(root, path, feature, args.keep_source)
        return Result(
            data={
                "feature": feature,
                "path": str(path),
                "branch": branch,
                "exists": False,
                "spec_carried": carried,
            },
            human=[f"worktree 已创建：{path}（分支 {branch}）"]
            + (["已携带未提交的 spec，可作为基线提交。"] if carried else []),
        )

    if not path.is_dir():
        return Result(
            data={"feature": feature, "path": str(path), "exists": False},
            human=[f"worktree 不存在，无需清理：{path}"],
        )
    progress = path / ".execution-progress.md"
    if progress.is_file():
        progress.unlink()
    if gitx.has_tracked_changes(path):
        raise LazyspecError("ENV-122", f"worktree 存在已跟踪文件的未提交改动，拒绝删除：{path}", EXIT_REFUSED)
    if gitx.is_dirty(path) and not args.force:
        raise LazyspecError(
            "ENV-123",
            f"worktree 存在未跟踪文件（可能是测试生成物）；确认后可加 --force：{path}",
            EXIT_REFUSED,
        )
    gitx.run(root, "worktree", "remove", *(["--force"] if args.force else []), str(path))
    return Result(
        data={"feature": feature, "path": str(path), "removed": True},
        human=[f"worktree 已清理：{path}"],
    )


def _carry_spec(root: Path, worktree: Path, feature: str, keep_source: bool) -> bool:
    """Copy an approved but uncommitted spec into the fresh worktree.

    A worktree created from the base branch cannot contain the spec that was just
    written and approved. Untracked specs are moved so the main checkout stays
    clean for the later merge; tracked specs are copied so no base-branch state is
    destroyed.
    """
    source = root / "specs" / feature / "spec.md"
    target = worktree / "specs" / feature / "spec.md"
    if not source.is_file() or target.is_file():
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    relative = f"specs/{feature}/spec.md"
    if not keep_source and not gitx.is_tracked(root, relative):
        source.unlink()
    return True


# -- checks ------------------------------------------------------------


def add_checks(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--feature", required=True)


def run_checks(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    _path, spec = _load_spec(root, args.feature)
    header, rows, _lines = spec.table_rows("验收标准")
    tasks = spec.tasks()
    entries = []
    for row in rows:
        if len(row) != 6:
            continue
        entries.append(
            {
                "id": row[0],
                "story": row[1],
                "kind": row[2],
                "when": row[3],
                "shall": row[4],
                "verification": row[5],
                "tasks": [task.number for task in tasks if row[0] in task.rids],
            }
        )
    missing = [entry["id"] for entry in entries if not entry["tasks"]]
    human = [f"验收项：{len(entries)} 条（未覆盖：{missing or '无'}）"]
    for entry in entries:
        human.append(f"- {entry['id']} -> {entry['verification']}")
    return Result(data={"checks": entries, "uncovered": missing}, human=human)


# -- index -------------------------------------------------------------


def add_index(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="校验索引是否漂移（默认）")
    group.add_argument("--write", action="store_true", help="重写索引")


def run_index(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    expected = memory.assemble_index_text(root)
    index = root / "project-memory" / "index.md"
    actual = index.read_text(encoding="utf-8") if index.is_file() else ""
    if args.write:
        atomic_write(index, expected)
        return Result(data={"written": True, "path": str(index)}, human=[f"索引已重写：{index}"])
    if actual == expected:
        return Result(data={"drift": False}, human=["索引与 Capsule 元数据一致。"])
    diff = "".join(
        difflib.unified_diff(
            actual.splitlines(keepends=True),
            expected.splitlines(keepends=True),
            fromfile="project-memory/index.md",
            tofile="project-memory/index.md (expected)",
        )
    )
    return Result(
        data={"drift": True, "diff": diff},
        violations=[Violation("MEM-301", "index.md 与 Capsule 元数据不一致", str(index))],
        human=["索引已漂移，可用 --write 重建。", diff],
        exit_code=EXIT_VIOLATION,
    )


# -- memory-check ------------------------------------------------------


def add_memory_check(parser: argparse.ArgumentParser) -> None:
    _add_common(parser)
    parser.add_argument("--strict-paths", action="store_true", help="额外校验来源路径真实存在")


def run_memory_check(args: argparse.Namespace) -> Result:
    root = resolve_root(args.root)
    violations = memory.check_memory(root, args.strict_paths)
    if not violations:
        return Result(data={"violation_count": 0}, human=["记忆检查通过。"])
    return Result(
        data={"violation_count": len(violations)},
        violations=violations,
        human=[f"记忆检查未通过：{len(violations)} 项"],
        exit_code=EXIT_VIOLATION,
    )


HANDLERS = {
    "check": (add_check, run_check),
    "recall": (add_recall, run_recall),
    "scan-retired": (add_scan_retired, run_scan_retired),
    "scan-specs": (add_scan_specs, run_scan_specs),
    "task-done": (add_task_done, run_task_done),
    "evidence": (add_evidence, run_evidence),
    "deliver": (add_deliver, run_deliver),
    "worktree": (add_worktree, run_worktree),
    "checks": (add_checks, run_checks),
    "index": (add_index, run_index),
    "memory-check": (add_memory_check, run_memory_check),
}


def main(prog: str, allowed: Optional[List[str]] = None, argv: Optional[List[str]] = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    parser = argparse.ArgumentParser(prog=prog, description="LazySpec deterministic helpers")
    parser.add_argument("--version", action="version", version=f"lazyspec-scripts {VERSION}")
    subparsers = parser.add_subparsers(dest="command")
    for name, (register, _handler) in HANDLERS.items():
        if allowed is not None and name not in allowed:
            continue
        subparser = subparsers.add_parser(name)
        register(subparser)

    if not argv:
        parser.print_help()
        return EXIT_USAGE
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return EXIT_USAGE

    try:
        result = HANDLERS[args.command][1](args)
    except LazyspecError as error:
        result = Result(
            violations=[Violation(error.code, error.message)],
            human=[f"未执行：{error.message}"],
            exit_code=error.exit_code,
        )
    emit(result, args.command, getattr(args, "json", False))
    return result.exit_code
