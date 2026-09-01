#!/usr/bin/env python3
"""Submission tracker for publication-coordinator agent.

Built Phase 7 R6 (gap-closing execution, missing-process #2).

Tracks paper/journal/conference submissions: venue, status, dates,
reviewer responses. Activates when first paper is submitted.

Usage:
    python3 scripts/submission-tracker.py add [--venue "IJGIS"] [--title "..."] [--date YYYY-MM-DD]
    python3 scripts/submission-tracker.py status <id> <status>
    python3 scripts/submission-tracker.py --print
"""

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("/opt/data/agents/state/submissions.json")
STATE_FILE_LIVE = Path("/opt/data/state/submissions.json")

VALID_STATUSES = {
    "drafting", "ready_to_submit", "submitted", "under_review",
    "revisions_requested", "accepted", "rejected", "withdrawn", "published",
}


def load():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"version": "1.0.0", "updated_at": None, "submissions": []}


def save(state):
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))
    try:
        STATE_FILE_LIVE.write_text(json.dumps(state, indent=2))
    except OSError:
        pass


def cmd_add(args):
    state = load()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "venue": args.venue,
        "title": args.title,
        "submitted_date": args.date or None,
        "status": "drafting",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "reviewers": [],
        "notes": args.notes or "",
    }
    state["submissions"].append(entry)
    save(state)
    print(f"Added submission: {entry['id']} — {entry['title']} ({entry['venue']})")
    return 0


def cmd_status(args):
    state = load()
    target = next((s for s in state["submissions"] if s["id"] == args.id), None)
    if not target:
        print(f"ERROR: no submission with id {args.id}", file=sys.stderr)
        return 2
    if args.status not in VALID_STATUSES:
        print(f"ERROR: invalid status (valid: {sorted(VALID_STATUSES)})", file=sys.stderr)
        return 2
    target["status"] = args.status
    target["status_updated_at"] = datetime.now(timezone.utc).isoformat()
    save(state)
    print(f"Updated {args.id} → {args.status}")
    return 0


def cmd_summary():
    state = load()
    by_status = {s: 0 for s in VALID_STATUSES}
    for s in state["submissions"]:
        by_status[s["status"]] = by_status.get(s["status"], 0) + 1
    print(f"Submissions: {len(state['submissions'])} total")
    for status, count in by_status.items():
        if count > 0:
            print(f"  {status}: {count}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Sub tracker")
    sub = p.add_subparsers(dest="cmd")

    pa = sub.add_parser("add")
    pa.add_argument("--venue", required=True, help="Journal/conference name")
    pa.add_argument("--title", required=True, help="Paper title")
    pa.add_argument("--date", help="Submission date YYYY-MM-DD")
    pa.add_argument("--notes", help="Notes")

    ps = sub.add_parser("status")
    ps.add_argument("id", help="Submission id")
    ps.add_argument("status", help=f"New status ({sorted(VALID_STATUSES)})")

    p.add_argument("--print", action="store_true", help="Print state JSON")

    args = p.parse_args(argv)

    if args.cmd == "add":
        return cmd_add(args)
    elif args.cmd == "status":
        return cmd_status(args)
    elif args.print:
        print(json.dumps(load(), indent=2))
        return 0
    else:
        return cmd_summary()


if __name__ == "__main__":
    sys.exit(main())