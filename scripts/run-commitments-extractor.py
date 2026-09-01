#!/usr/bin/env python3
"""run-commitments-extractor.py — Cron entry point for commitment extraction.

Phase 9 R3 / A1.6 fix: the previous inline `python3 -c` script wrote
coord.json unconditionally on every tick. This wrapper:

  1. Reads the current coord.json + signal-queue.ndjson
  2. Extracts new commitments from signals (dedup by id)
  3. Writes coord.json ONLY if the commitments list changed

Output: rc=0 if processed (whether or not anything was added)
        rc=0 also if no signal-queue exists (no-op)
        rc=2 on unexpected exception

Idempotent: can be run multiple times safely without corrupting coord.json.
"""
import sys
import json
import shutil
from pathlib import Path

REPO = Path("/opt/data/agents")
sys.path.insert(0, str(REPO / "scripts/memory"))

from commitments import extract_commitments_from_signal, merge_commitments  # noqa: E402

STATE = Path("/opt/data/state")
SIGNAL_QUEUE = STATE / "signal-queue.ndjson"
COORD = REPO / "state" / "coord.json"


def main() -> int:
    if not COORD.exists():
        print("[commitments] no coord.json — skipping")
        return 0

    coord_data = json.loads(COORD.read_text())

    if not SIGNAL_QUEUE.exists():
        # No new signals — exit cleanly without writing
        return 0

    lines = []
    for line in SIGNAL_QUEUE.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            lines.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    if not lines:
        return 0

    extracted = []
    for sig in lines:
        extracted.extend(extract_commitments_from_signal(sig))

    # Snapshot current commitments to detect diff
    before = json.dumps(coord_data.get("commitments", []), sort_keys=True)
    merge_commitments(coord_data, extracted)
    after = json.dumps(coord_data.get("commitments", []), sort_keys=True)

    if before == after:
        # No diff — do NOT rewrite the file (avoid 365 rewrites/year noise)
        return 0

    # Atomic write: tmp + rename
    tmp = COORD.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(coord_data, indent=2, ensure_ascii=False))
    tmp.replace(COORD)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[commitments] FAIL: {e}", file=sys.stderr)
        sys.exit(2)