#!/usr/bin/env python3
"""Entrypoint for the make.fun bounty "Make the Judge Smile".

Running this program writes a single line to ``entry.txt`` in the
harness output directory: ``$MAKEFUN_OUTPUT_DIR`` when that variable is
set, otherwise ``/output``.  Python 3.13 standard library only, no
network access, no command-line arguments, and the output is fully
deterministic -- the same bytes on every run.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

SMILE_LINE = (
    "At 7 a.m. the warung lady slipped an extra krupuk into my bag "
    "and whispered 'for luck' \u2014 and honestly it worked: my bus "
    "arrived on time."
)

# The line is one small morning kindness with a concrete time (7 a.m.),
# a concrete thing (the extra krupuk) and a small surprise at the end:
# the luck she wished for actually showed up, in the form of a bus
# that arrived on time.

MIN_CHARS = 1
MAX_CHARS = 200


def check_line(line: str) -> None:
    """Fail loudly if the line breaks any competition rule."""
    if not MIN_CHARS <= len(line) <= MAX_CHARS:
        raise ValueError(f"line is {len(line)} chars, must be 1-200")
    if line.strip() != line:
        raise ValueError("line has leading or trailing whitespace")
    if any(ord(c) < 32 for c in line):
        raise ValueError("line contains a control character")
    if "  " in line:
        raise ValueError("line contains a double space")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line is only whitespace")


def entry_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return Path(out_dir) / "entry.txt"


def run() -> int:
    check_line(SMILE_LINE)
    target = entry_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(SMILE_LINE, encoding="utf-8")
    if target.read_text(encoding="utf-8") != SMILE_LINE:
        raise RuntimeError("round-trip check failed: file differs")
    print(f"wrote {target} ({len(SMILE_LINE)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
