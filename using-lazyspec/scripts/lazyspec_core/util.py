"""Shared primitives: exit codes, violations, result transport, file writes."""

from __future__ import annotations

import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

VERSION = "0.1.0"

EXIT_OK = 0
EXIT_VIOLATION = 1
EXIT_USAGE = 2
EXIT_BLOCKED = 3
EXIT_REFUSED = 4

NOTICE = "本结果仅为格式与证据形状判定，不构成批准。"

FEATURE_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


@dataclass
class Violation:
    code: str
    message: str
    path: Optional[str] = None
    line: Optional[int] = None

    def as_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"code": self.code, "message": self.message}
        if self.path:
            data["path"] = self.path
        if self.line:
            data["line"] = self.line
        return data


class LazyspecError(Exception):
    """A blocking condition that is not a document violation."""

    def __init__(self, code: str, message: str, exit_code: int = EXIT_BLOCKED) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.exit_code = exit_code


@dataclass
class Result:
    data: Dict[str, Any] = field(default_factory=dict)
    violations: List[Violation] = field(default_factory=list)
    warnings: List[Violation] = field(default_factory=list)
    human: List[str] = field(default_factory=list)
    exit_code: int = EXIT_OK


def resolve_root(value: str) -> Path:
    root = Path(value).expanduser().resolve()
    if not root.is_dir():
        raise LazyspecError("ENV-101", f"项目根目录不存在：{root}")
    return root


def validate_feature(value: str) -> str:
    if not FEATURE_RE.match(value or ""):
        raise LazyspecError(
            "ENV-102",
            f"feature 名称不合法：{value!r}；只允许字母、数字、点、下划线与连字符。",
            EXIT_USAGE,
        )
    return value


def spec_path(root: Path, feature: str) -> Path:
    return root / "specs" / validate_feature(feature) / "spec.md"


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise LazyspecError("ENV-103", f"文件不存在：{path}")
    except OSError as error:
        raise LazyspecError("ENV-104", f"无法读取 {path}：{error}")


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(dir=str(path.parent), prefix=".lazyspec-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
        os.replace(temporary, str(path))
    except BaseException:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def emit(result: Result, command: str, as_json: bool) -> None:
    if as_json:
        payload = {
            "ok": result.exit_code == EXIT_OK,
            "approval": False,
            "command": command,
            "notice": NOTICE,
        }
        payload.update(result.data)
        payload["violations"] = [item.as_dict() for item in result.violations]
        payload["warnings"] = [item.as_dict() for item in result.warnings]
        json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    for line in result.human:
        sys.stdout.write(line + "\n")
    for item in result.warnings:
        sys.stdout.write(f"[警告 {item.code}] {item.message}\n")
    for item in result.violations:
        location = ""
        if item.path:
            location = f" {item.path}"
            if item.line:
                location += f":{item.line}"
        sys.stdout.write(f"[{item.code}]{location} {item.message}\n")
    if result.exit_code != EXIT_OK:
        sys.stdout.write(NOTICE + "\n")


def fail(status: List[Violation], human: List[str]) -> Result:
    return Result(violations=status, human=human, exit_code=EXIT_VIOLATION)
