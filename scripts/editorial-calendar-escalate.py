#!/usr/bin/env python3
"""Editorial calendar deadline escalation.

Built Phase 7 R6 (gap-closing execution, missing-process #5).

Reads state/editorial-calendar.json. Identifies entries whose deadlines
are approaching (within N days) or passed. Writes escalation alerts
to state/editorial-calendar-escalations.json.

Usage:
    python3 scripts/editorial-calendar-escalate.py             # scan + alert
    python3 scripts/editorial-calendar-escalate.py --print     # print only
"""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE_AGENT = Path("/opt/data/agents/state/editorial-calendar-escalations.json")
STATE_FILE_LIVE = Path("/opt/data/state/editorial-calendar-escalations.json")
CALENDAR_FILE = Path("/opt/data/agents/state/editorial-calendar.json")

WARN_DAYS = 3  # alert if deadline within 3 days


def atomic_write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            path.replace(path.with_suffix(path.suffix + ".bak"))
        except OSError:
            pass
    fd, tmp = tempfile.mkstemp(prefix=".ed-esc-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def parse_dl(s: str):
    if not s:
        return None
    try:
        if "T" in s:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        return datetime.fromisoformat(s + "T23:59:59+00:00")
    except ValueError:
        return None


def compute() -> dict:
    if not CALENDAR_FILE.exists():
        return {
            "version": "1.0.0",
            "computed_at": datetime.now(timezone.utc).isoformat(),
            "alerts": [],
            "note": "no calendar file",
        }
    cal = json.loads(CALENDAR_FILE.read_text())
    now = datetime.now(timezone.utc)
    alerts = []
    for entry in cal.get("entries", []):
        dl = parse_dl(entry.get("deadline", ""))
        if not dl:
            continue
        if entry.get("status") in ("idea", "drafting", "peer_review", "final"):
            days_left = (dl - now).days
            if days_left < 0:
                alerts.append({
                    "id": entry["id"],
                    "title": entry["title"],
                    "deadline": entry["deadline"],
                    "days_overdue": -days_left,
                    "severity": "CRITICAL",
                    "alert": f"OVERDUE by {-days_left}d",
                })
            elif days_left <= WARN_DAYS:
                alerts.append({
                    "id": entry["id"],
                    "title": entry["title"],
                    "deadline": entry["deadline"],
                    "days_left": days_left,
                    "severity": "WARNING",
                    "alert": f"DUE in {days_left}d",
                })
    return {
        "version": "1.0.0",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "warn_threshold_days": WARN_DAYS,
        "alerts_count": len(alerts),
        "alerts": alerts,
        "alert": "ESCALATION" if any(a["severity"] == "CRITICAL" for a in alerts) else None,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Editorial escalate")
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

    n = payload["alerts_count"]
    print(f"Editorial escalations: {n} alerts (threshold {WARN_DAYS}d)")
    for a in payload["alerts"]:
        print(f"  [{a['severity']}] {a['title']} — {a['alert']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())