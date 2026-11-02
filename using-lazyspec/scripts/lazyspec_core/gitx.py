"""Thin Git wrappers. Every call passes argument lists, never shell strings."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Optional, Sequence

from .util import EXIT_BLOCKED, EXIT_REFUSED, LazyspecError


def run(root: Path, *args: str, check: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(root),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip() or "git 命令失败"
        raise LazyspecError("ENV-110", f"git {' '.join(args)} 失败：{detail}", EXIT_BLOCKED)
    return completed.stdout


def run_bytes(root: Path, *args: str) -> bytes:
    completed = subprocess.run(
        ["git", *args],
        cwd=str(root),
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        detail = completed.stderr.decode("utf-8", "replace").strip() or "git 命令失败"
        raise LazyspecError("ENV-110", f"git {' '.join(args)} 失败：{detail}", EXIT_BLOCKED)
    return completed.stdout


def is_repository(root: Path) -> bool:
    completed = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        cwd=str(root),
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0 and completed.stdout.strip() == "true"


def require_repository(root: Path) -> None:
    if not is_repository(root):
        raise LazyspecError("ENV-111", f"不是 Git 仓库：{root}", EXIT_BLOCKED)


def head_short(root: Path) -> Optional[str]:
    completed = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"],
        cwd=str(root),
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout.strip() or None


def has_commit(root: Path, revision: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
        cwd=str(root),
        check=False,
        capture_output=True,
    )
    return completed.returncode == 0


def is_ancestor(root: Path, ancestor: str, descendant: str = "HEAD") -> bool:
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=str(root),
        check=False,
        capture_output=True,
    )
    return completed.returncode == 0


def status_porcelain_z(root: Path, pathspec: Sequence[str] = ("specs/",)) -> bytes:
    return run_bytes(
        root,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "-M",
        "--",
        *pathspec,
    )


def staged_paths(root: Path) -> List[str]:
    output = run(root, "diff", "--cached", "--name-only", "-z")
    return [item for item in output.split("\0") if item]


def worktree_list(root: Path) -> List[str]:
    output = run(root, "worktree", "list", "--porcelain")
    return [line[len("worktree "):] for line in output.splitlines() if line.startswith("worktree ")]


def is_tracked(root: Path, path: str) -> bool:
    completed = subprocess.run(
        ["git", "ls-files", "--error-unmatch", "--", path],
        cwd=str(root),
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def is_dirty(root: Path) -> bool:
    output = run(root, "status", "--porcelain=v1", "--untracked-files=all")
    return bool(output.strip())


def has_tracked_changes(root: Path) -> bool:
    output = run(root, "status", "--porcelain=v1", "--untracked-files=no")
    return bool(output.strip())


def add(root: Path, paths: Sequence[str]) -> None:
    if not paths:
        raise LazyspecError("ENV-112", "没有需要暂存的路径", EXIT_REFUSED)
    run(root, "add", "--", *paths)


def commit(root: Path, message: str) -> str:
    run(root, "commit", "-m", message)
    return run(root, "rev-parse", "--short", "HEAD").strip()


def show_file(root: Path, revision: str, path: str) -> Optional[bytes]:
    completed = subprocess.run(
        ["git", "show", f"{revision}:{path}"],
        cwd=str(root),
        check=False,
        capture_output=True,
    )
    if completed.returncode != 0:
        return None
    return completed.stdout
