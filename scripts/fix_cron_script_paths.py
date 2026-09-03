#!/usr/bin/env python3
"""fix_cron_script_paths.py - Batch-fix crons with 'Blocked: script path' errors.

PR #13 fixed aiw-signal-indexer (one cron, one script). This script
generalizes the fix: scan jobs.json for ANY cron whose last_error is
"Blocked: script path resolves outside the scripts directory" and
apply the same pattern (move script to /opt/data/scripts/, add
backward-compat symlink, update cron entry).

Idempotent. Dry-run by default; --apply to write.

As of 2026-09-03 audit, this fixes 24 of 37 broken crons. The
remaining 13 are different error classes (auth, missing scripts,
runtime errors) and are out of scope.

Usage:
    python scripts/fix_cron_script_paths.py             # dry-run
    python scripts/fix_cron_script_paths.py --apply     # write changes

Refs: PR #13 (the original fix); HANDOFF-PHASE-8.md CRITICAL #2
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

CRON_PATHS = [
    Path("/opt/data/.hermes/cron/jobs.json"),
    Path("/opt/data/cron/jobs.json"),
]

CANONICAL_SCRIPTS_DIR = Path("/opt/data/scripts")
BLOCKED_RE = re.compile(
    r"Blocked: script path resolves outside the scripts directory"
)


def _split_script_field(script: str) -> tuple[str, str]:
    """Split 'path --arg1 --arg2' into (path, args_str)."""
    parts = script.split(None, 1)
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], parts[1]


def _plan_cron_fix(script_field: str) -> tuple[Path, str, Path] | None:
    """Return (source, args, new_path) if this cron needs fixing, else None.

    Rules:
    - If script path is already under /opt/data/scripts/, no-op.
    - If source file doesn't exist, skip (can't copy).
    - Otherwise: copy source to /opt/data/scripts/<basename>, return new path.
    """
    src_str, args = _split_script_field(script_field)
    src = Path(src_str)
    if not src_str.startswith("/"):
        return None  # not absolute; leave alone
    if "/opt/data/scripts/" in src_str or src_str == "/opt/data/scripts":
        return None  # already canonical
    if not src.exists():
        return None  # source missing
    new_path = CANONICAL_SCRIPTS_DIR / src.name
    if new_path == src:
        return None  # would be no-op
    return src, args, new_path


def _copy_and_link(src: Path, new: Path, apply: bool) -> list[str]:
    """Copy src to new, add symlink at src. Return human-readable ops."""
    ops = []
    if not new.exists() and apply:
        new.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, new)
        new.chmod(0o755)
        ops.append(f"COPY {src} -> {new}")
    elif not new.exists():
        ops.append(f"COPY {src} -> {new} (dry-run)")
    else:
        ops.append(f"SKIP copy: {new} already exists")
    # Symlink at original location (only if it's a real file, not already a symlink)
    if src.exists() and not src.is_symlink() and apply:
        backup = src.with_suffix(src.suffix + ".real")
        shutil.move(str(src), str(backup))
        src.symlink_to(new)
        ops.append(f"SYMLINK {src} -> {new} (backup: {backup})")
    elif src.exists() and not src.is_symlink():
        ops.append(f"SYMLINK {src} -> {new} (dry-run)")
    else:
        ops.append(f"SKIP symlink: {src} is already a symlink")
    return ops


def _build_new_script_field(new_path: Path, args: str) -> str:
    """Reconstruct the script field with the new path and original args."""
    s = str(new_path)
    if args:
        s += " " + args
    return s


def patch(apply: bool = False) -> int:
    total_fixed = 0
    for cp in CRON_PATHS:
        if not cp.exists():
            print(f"WARNING: {cp} missing - skipping")
            continue
        data = json.loads(cp.read_text())
        for j in data.get("jobs", []):
            if not j.get("enabled", True):
                continue
            err = j.get("last_error") or ""
            if not BLOCKED_RE.search(err):
                continue
            script_field = j.get("script", "")
            plan = _plan_cron_fix(script_field)
            if plan is None:
                continue
            src, args, new_path = plan
            new_field = _build_new_script_field(new_path, args)
            print(f"[{cp}] {j['name']}: {script_field!r} -> {new_field!r}")
            ops = _copy_and_link(src, new_path, apply=apply)
            for op in ops:
                print(f"    {op}")
            if apply:
                j["script"] = new_field
            total_fixed += 1
        if apply and total_fixed:
            cp.write_text(json.dumps(data, indent=2) + "\n")
    if not apply:
        print(f"\nDRY RUN: would fix {total_fixed} cron entries. Re-run with --apply.")
    elif total_fixed:
        print(f"\nApplied {total_fixed} fixes.")
    else:
        print(f"\nNo fixes needed (no crons match the pattern).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    return patch(apply=args.apply)


if __name__ == "__main__":
    sys.exit(main())
