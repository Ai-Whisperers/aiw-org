#!/usr/bin/env python3
"""
aiw-monitor-notes-compact.py — 7-day TTL cleanup for monitor breadcrumb files.

Walks every `monitor-notes/` directory under /opt/data/agents/ and deletes
files older than 7 days. Filenames parsed:
  YYYY-MM-DD.md
  YYYY-MM-DD-ptN.md

Keeps .gitkeep and any file without a parseable date.

Usage:
  python3 aiw-monitor-notes-compact.py            # delete in place
  python3 aiw-monitor-notes-compact.py --dry-run  # report only, delete nothing

Created: 2026-09-03 (AIW token audit remediation, Plan Task 4).
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

AGENTS_DIR = Path("/opt/data/agents")
DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")
TTL_DAYS = 7
NOW = datetime.now(timezone.utc)


def parse_date(name: str) -> datetime | None:
    m = DATE_RE.match(name)
    if not m:
        return None
    try:
        return datetime.strptime(m.group(1), "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--ttl-days", type=int, default=TTL_DAYS)
    args = p.parse_args()

    cutoff = NOW - timedelta(days=args.ttl_days)
    candidates: list[tuple[Path, datetime]] = []
    kept: list[Path] = []

    for notes_dir in AGENTS_DIR.glob("*/**/monitor-notes"):
        if not notes_dir.is_dir():
            continue
        for f in notes_dir.iterdir():
            if not f.is_file() or f.name.startswith("."):
                continue
            d = parse_date(f.name)
            if d is None:
                kept.append(f)
                continue
            if d < cutoff:
                candidates.append((f, d))
            else:
                kept.append(f)

    print(f"Scanned {AGENTS_DIR} — found {len(candidates)} files older than {args.ttl_days} days, {len(kept)} kept.")
    for f, d in candidates[:50]:
        print(f"  delete  {f}  (date={d.date()})")
    if len(candidates) > 50:
        print(f"  ... and {len(candidates) - 50} more")

    if args.dry_run:
        print("Dry-run — no deletions.")
        return 0

    deleted = 0
    for f, _ in candidates:
        try:
            f.unlink()
            deleted += 1
        except Exception as e:
            print(f"  ERROR deleting {f}: {e}", file=sys.stderr)
    print(f"Deleted {deleted} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
