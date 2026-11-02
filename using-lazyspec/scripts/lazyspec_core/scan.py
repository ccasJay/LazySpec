"""Changed-Spec discovery with NUL-safe porcelain parsing and content hashing."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from . import gitx

EXCLUDED_PREFIXES = ("specs/archived/", "specs/retired/")


@dataclass
class ChangedSpec:
    path: str
    status: str
    feature: str
    sha256: Optional[str]
    origin: Optional[str] = None
    content_change: Optional[str] = None

    def as_dict(self) -> Dict[str, object]:
        return {key: value for key, value in asdict(self).items() if value is not None}


def parse_porcelain_z(raw: bytes) -> List[Dict[str, Optional[str]]]:
    fields = raw.split(b"\0")
    records: List[Dict[str, Optional[str]]] = []
    index = 0
    while index < len(fields):
        entry = fields[index]
        index += 1
        if not entry:
            continue
        text = entry.decode("utf-8", "surrogateescape")
        if len(text) < 4:
            continue
        code = text[:2]
        path = text[3:]
        origin: Optional[str] = None
        if "R" in code or "C" in code:
            if index < len(fields) and fields[index]:
                origin = fields[index].decode("utf-8", "surrogateescape")
                index += 1
        records.append({"code": code, "path": path, "origin": origin})
    return records


def is_spec_path(path: str) -> bool:
    if not path.startswith("specs/") or not path.endswith("/spec.md"):
        return False
    if path.count("/") != 2:
        return False
    if any(path.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    return True


def feature_of(path: str) -> str:
    return path.split("/")[1]


def sha256_file(path: Path) -> Optional[str]:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def scan_changed(root: Path, current_feature: Optional[str] = None, since: Optional[str] = None) -> List[ChangedSpec]:
    gitx.require_repository(root)
    records = parse_porcelain_z(gitx.status_porcelain_z(root))
    results: List[ChangedSpec] = []
    for record in records:
        path = record["path"] or ""
        if not is_spec_path(path):
            continue
        code = record["code"] or ""
        if "D" in code:
            continue
        feature = feature_of(path)
        if current_feature and feature == current_feature:
            continue
        digest = sha256_file(root / path)
        entry = ChangedSpec(
            path=path,
            status=(code or "").strip() or "??",
            feature=feature,
            sha256=digest,
            origin=record["origin"],
        )
        if since:
            entry.content_change = compare_with_revision(root, since, path, digest)
        results.append(entry)
    results.sort(key=lambda item: item.path)
    return results


def compare_with_revision(root: Path, revision: str, path: str, current_digest: Optional[str]) -> str:
    previous = gitx.show_file(root, revision, path)
    if previous is None:
        return "new" if current_digest else "absent"
    if current_digest is None:
        return "deleted"
    previous_digest = hashlib.sha256(previous).hexdigest()
    return "unchanged" if previous_digest == current_digest else "changed"


def scan_retired(root: Path) -> List[Dict[str, object]]:
    entries: List[Dict[str, object]] = []
    for base, state in ((root / "specs" / "retired", "obsolete"), (root / "specs", None)):
        if not base.is_dir():
            continue
        candidates = sorted(base.rglob("spec.md"))
        for path in candidates:
            relative = path.relative_to(root).as_posix()
            if state is None:
                if relative.count("/") != 1 or relative.startswith(("specs/archived/", "specs/retired/")):
                    continue
            text = path.read_text(encoding="utf-8")
            status = _frontmatter_value(text, "status")
            if status not in {"obsolete"}:
                continue
            entries.append(
                {
                    "path": relative,
                    "feature": path.parent.name,
                    "status": status,
                    "title": _title(text),
                    "reason": _reason(text),
                }
            )
    unique: Dict[str, Dict[str, object]] = {str(item["path"]): item for item in entries}
    return [unique[key] for key in sorted(unique)]


def _frontmatter_value(text: str, key: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        name, value = line.split(":", 1)
        if name.strip() == key:
            return value.strip().strip('"\'')
    return ""


def _title(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def _reason(text: str) -> str:
    for line in text.splitlines():
        lowered = line.lower()
        if "[!caution]" in lowered or "[!warning]" in lowered:
            continue
        if line.startswith(">") and len(line.strip()) > 2:
            return line.strip("> ").strip()
        if "status_reason:" in lowered:
            return line.split(":", 1)[1].strip().strip('"\'')
    return ""
