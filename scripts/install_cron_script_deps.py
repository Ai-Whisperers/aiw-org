#!/usr/bin/env python3
"""install_cron_script_deps.py - Copy missing sibling deps to /opt/data/scripts/.

PR #18 moved scripts to /opt/data/scripts/ (canonical cron-runner
location). When a moved script does e.g.

    sys.path.insert(0, str(Path(__file__).parent))
    from signal_queue import ...

it looks for the sibling module in /opt/data/scripts/. If that
sibling wasn't moved alongside the script, the import fails.

This script:
  1. Lists every .py file in /opt/data/scripts/
  2. For each, parses imports to find siblings
  3. Resolves missing siblings from aiw-org/scripts/
  4. Copies them to /opt/data/scripts/

Idempotent. Dry-run by default; --apply to write.

Refs: PR #18, HANDOFF-PHASE-8.md.
"""
from __future__ import annotations

import argparse
import ast
import shutil
import sys
from pathlib import Path

CANONICAL = Path("/opt/data/scripts")
REPO_SCRIPTS = Path(__file__).resolve().parent


def _extract_imports(py_file: Path) -> set[str]:
    """Return the set of top-level module names imported by py_file."""
    try:
        tree = ast.parse(py_file.read_text(errors="ignore"))
    except SyntaxError:
        return set()
    modules = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                # Take the top-level package name only.
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module.split(".")[0])
    return modules


def find_missing_deps() -> dict[str, list[Path]]:
    """Return {missing_module: [script_files_that_need_it]}."""
    canonical_files = [
        p for p in CANONICAL.glob("*.py") if p.is_file()
    ]
    canonical_modules = {p.stem for p in canonical_files}
    missing: dict[str, list[Path]] = {}
    # Don't try to fill stdlib or third-party; only sibling-repo modules.
    stdlib = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else set()
    repo_modules = {p.stem for p in REPO_SCRIPTS.glob("*.py")}
    for py in canonical_files:
        imports = _extract_imports(py)
        for mod in imports:
            if mod in stdlib:
                continue
            if mod in canonical_modules:
                continue
            # Repo-local sibling candidates
            if mod in repo_modules and (REPO_SCRIPTS / f"{mod}.py").exists():
                missing.setdefault(mod, []).append(py)
    return missing


def patch(apply: bool = False) -> int:
    missing = find_missing_deps()
    if not missing:
        print("No missing sibling deps detected.")
        return 0
    print(f"Detected {len(missing)} missing sibling deps in /opt/data/scripts/:")
    for mod, callers in missing.items():
        print(f"  {mod}.py  callers={len(callers)}")
        for c in callers[:3]:
            print(f"    -> {c.name}")
        if len(callers) > 3:
            print(f"    ... +{len(callers)-3} more")
    if not apply:
        print("\nDRY RUN: re-run with --apply to copy missing deps.")
        return 0
    copied = 0
    for mod in missing:
        src = REPO_SCRIPTS / f"{mod}.py"
        dst = CANONICAL / f"{mod}.py"
        if dst.exists():
            continue
        shutil.copy2(src, dst)
        print(f"COPIED: {src} -> {dst}")
        copied += 1
    print(f"\nApplied {copied} copies.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    return patch(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
