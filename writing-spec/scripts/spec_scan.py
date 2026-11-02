#!/usr/bin/env python3
"""Plan-stage helper: discover Specs changed in the working tree.

Invoke explicitly with the Python interpreter:
    python3 <writing-spec-skill>/scripts/spec_scan.py scan-specs --changed [--json]
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.dont_write_bytecode = True

WORKSPACE = Path(__file__).resolve().parents[2]
CORE = WORKSPACE / "using-lazyspec" / "scripts"
sys.path.insert(0, str(CORE))

try:
    from lazyspec_core.cli import main
except ImportError:  # pragma: no cover - installation guard
    sys.stderr.write(
        "ENV-130 找不到 lazyspec_core。请重新安装 LazySpec 全部技能："
        "npx skills add ccasJay/LazySpec --skill '*' -g\n"
    )
    raise SystemExit(3)

ALLOWED = ["scan-specs"]

if __name__ == "__main__":
    raise SystemExit(main("spec_scan.py", ALLOWED))
