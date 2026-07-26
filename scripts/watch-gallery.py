#!/usr/bin/env python3
"""
Watch ch*/ folders and auto-run build-gallery.py on changes.
Useful while developing locally (before / without GitHub Actions).

  python scripts/watch-gallery.py
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "scripts" / "build-gallery.py"
POLL_SEC = 1.0


def snapshot() -> dict[str, float]:
    state: dict[str, float] = {}
    chapter_root = ROOT / "chapter"
    if not chapter_root.is_dir():
        return state
    for folder in chapter_root.glob("ch*"):
        if not folder.is_dir():
            continue
        for path in folder.rglob("*"):
            if path.is_file():
                try:
                    state[str(path.relative_to(ROOT))] = path.stat().st_mtime
                except OSError:
                    pass
    return state


def build() -> None:
    print("\n[watch] building gallery...")
    subprocess.run([sys.executable, str(BUILD)], cwd=ROOT, check=False)


def main() -> None:
    print(f"[watch] watching {ROOT}/chapter/ch*  (Ctrl+C to stop)")
    build()
    prev = snapshot()
    try:
        while True:
            time.sleep(POLL_SEC)
            curr = snapshot()
            if curr != prev:
                build()
                prev = snapshot()
    except KeyboardInterrupt:
        print("\n[watch] stopped")


if __name__ == "__main__":
    main()
