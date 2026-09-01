#!/usr/bin/env python3
"""Peer-review queue trigger.

Built Phase 7 R6 (gap-closing execution, missing-process #4).

Detects research drafts that need peer review (in outbox/ with status
'drafting' older than N days) and emits an outbox alert.

Usage:
    python3 scripts/peer-review-trigger.py             # scan + emit alerts
    python3 scripts/peer-review-trigger.py --print     # print only
"""

import argparse
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

STATE_FILE_AGENT = Path("/opt/data/agents/state/peer-review-queue.json")
STATE_FILE_LIVE = Path("/opt/data/state/peer-review-queue.json")
RESEARCH_OUTBOX = Path("/opt/data/agents/05-research-education/research-tracker/outbox")
STALE_THRESHOLD_DAYS = 7


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            path.replace(path.with_suffix(path.suffix + ".bak"))
        except OSError:
            pass
    fd, tmp = tempfile.mkstemp(prefix=".peer-q-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def find_stale_drafts() -> list:
    """Find outbox files older than STALE_THRESHOLD_DAYS that mention 'drafting' or are partial."""
    stale = []
    if not RESEARCH_OUTBOX.exists():
        return stale
    cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_THRESHOLD_DAYS)
    for f in RESEARCH_OUTBOX.glob("*.md"):
        if f.name.startswith("_"):
            continue
        try:
            mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mtime < cutoff:
            text = f.read_text(encoding="utf-8", errors="replace")[:500].lower()
            if "draft" in text or "wip" in text or "todo" in text:
                stale.append({
                    "path": str(f.relative_to(Path("/opt/data/agents"))),
                    "age_days": (datetime.now(timezone.utc) - mtime).days,
                    "first_500_chars": f.read_text(encoding="utf-8", errors="replace")[:200],
                })
    return stale


def compute() -> dict:
    stale = find_stale_drafts()
    return {
        "version": "1.0.0",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "stale_threshold_days": STALE_THRESHOLD_DAYS,
        "stale_drafts_count": len(stale),
        "stale_drafts": stale,
        "alert": "REVIEW QUEUE FULL" if len(stale) > 3 else None,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Peer review trigger")
    p.add_argument("--print", action="store_true")
    args = p.parse_args(argv)

    payload = compute()
    if args.print:
        print(json.dumps(payload, indent=2))
        return 0

    atomic_write_json(STATE_FILE_AGENT, payload)
    try:
        atomic_write_json(STATE_FILE_LIVE, payload)
    except OSError as exc:
        print(f"WARN: live mirror write failed: {exc}", file=sys.stderr)

    s = payload["stale_drafts_count"]
    print(f"Peer-review queue: {s} stale drafts (threshold {STALE_THRESHOLD_DAYS}d)")
    if payload["alert"]:
        print(f"  ALERT: {payload['alert']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())