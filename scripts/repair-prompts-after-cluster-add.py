#!/usr/bin/env python3
"""Repair PROMPT.md files broken by add-cluster-field.py (lost newline before ---).

The bug: splitlines() strips the final \n before the closing ---.
Fix: detect patterns like `xxx---` (no newline) and insert \n.
"""

import re
import sys
from pathlib import Path

AGENTS_REPO = Path("/opt/data/agents")
SCAN_PATHS = [
    AGENTS_REPO / "04-engineering",
    AGENTS_REPO / "05-research-education",
    AGENTS_REPO / "demiurge" / "agents",
]


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="replace")
    original = text

    if not text.startswith("---"):
        return False

    # Find patterns where a non-newline character is immediately followed by ---
    # without a newline separator. This is the bug from add-cluster-field.
    # Examples:
    #   "  - thoth-literature-scanner---" → "  - thoth-literature-scanner\n---"
    #   "cluster: build---" → "cluster: build\n---"
    # Use ([^\n]) to capture the last char before ---; ensure --- is the closing delimiter
    # by checking it's followed by \n or end-of-file.

    fixed = re.sub(r"([^\n])(---)(?=\n|$)", r"\1\n\2", text)

    if fixed != original:
        path.write_text(fixed, encoding="utf-8")
        return True
    return False


def main():
    fixed_count = 0
    for parent in SCAN_PATHS:
        if not parent.exists():
            continue
        for prompt in parent.rglob("PROMPT.md"):
            if "monitor-notes" in str(prompt):
                continue
            if fix_file(prompt):
                print(f"  FIXED: {prompt.relative_to(AGENTS_REPO)}")
                fixed_count += 1
    print(f"\n{fixed_count} files repaired")


if __name__ == "__main__":
    main()