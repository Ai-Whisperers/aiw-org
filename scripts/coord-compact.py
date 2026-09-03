#!/usr/bin/env python3
"""
coord-compact.py — Truncate coord.json:decisions_for_ivan[] queue.

The 18 every-30-min monitor agents have been writing 10-50 decisions/day each
into this queue. As of 2026-09-03 it had 551 items, 678KB.

This script:
  1. Reads /opt/data/state/coord.json
  2. Keeps the most recent N items (default: 50) by raised_at timestamp
  3. Archives the rest to /opt/data/state/coord-decisions-archive.jsonl
  4. Atomically writes the truncated coord.json

Why this matters:
  - Each monitor reads coord.json every 15-30 min
  - 678KB JSON parsed by every monitor = ~50k tokens wasted per day
  - Truncating to 50 items = ~30KB JSON = ~3k tokens/day = save ~47k tokens/day

Created: 2026-09-03 (AIW token audit Tier 2).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

COORD_FILE = Path("/opt/data/state/coord.json")
ARCHIVE_FILE = Path("/opt/data/state/coord-decisions-archive.jsonl")
KEEP_RECENT = 50  # keep most recent N items


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--keep", type=int, default=KEEP_RECENT, help="How many recent decisions to keep")
    p.add_argument("--dry-run", action="store_true", help="report what would happen, don't write")
    p.add_argument("--archive", type=Path, default=ARCHIVE_FILE, help="archive file path")
    args = p.parse_args()

    if not COORD_FILE.exists():
        print(f"ERROR: {COORD_FILE} not found", file=sys.stderr)
        return 1

    # Backup
    backup = COORD_FILE.with_suffix(f".pre-compact-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.bak")
    if not args.dry_run:
        shutil.copy2(COORD_FILE, backup)

    coord = json.loads(COORD_FILE.read_text())
    decisions = coord.get("decisions_for_ivan", [])

    if len(decisions) <= args.keep:
        print(f"Nothing to compact: {len(decisions)} decisions, keep={args.keep}")
        return 0

    # Sort by raised_at (most recent last)
    def key(d):
        return d.get("raised_at", "")
    decisions_sorted = sorted(decisions, key=key)
    to_archive = decisions_sorted[:-args.keep]
    to_keep = decisions_sorted[-args.keep:]

    print(f"Total decisions: {len(decisions)}")
    print(f"Keeping:         {len(to_keep)} (most recent)")
    print(f"Archiving:       {len(to_archive)}")

    if args.dry_run:
        print("Dry-run: would archive and truncate")
        return 0

    # Append to archive
    with args.archive.open("a") as f:
        for d in to_archive:
            f.write(json.dumps(d) + "\n")

    # Atomic write
    coord["decisions_for_ivan"] = to_keep
    coord["_last_modified_by"] = "coord-compact.py"
    coord["_last_modified"] = datetime.now(timezone.utc).isoformat()

    tmp = COORD_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(coord, indent=2))
    tmp.replace(COORD_FILE)

    # Show new size
    new_size = COORD_FILE.stat().st_size
    print(f"Wrote {COORD_FILE} ({new_size:,} bytes, was {len(decisions)} -> {len(to_keep)} decisions)")
    print(f"Archive: {args.archive}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
