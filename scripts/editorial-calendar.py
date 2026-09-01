#!/usr/bin/env python3
"""Editorial calendar keeper — track what's in review, what's published.

Built Phase 7 R5 (implementation plan §4 Phase 2.6).

CRON_WORKFLOW (no LLM). Tracks Research dept output pipeline:
  - draft → peer-review → final → published

Output: /opt/data/agents/state/editorial-calendar.json (atomic per P2).

Usage:
    python3 scripts/editorial-calendar.py              # compute + write
    python3 scripts/editorial-calendar.py --add       # add new entry from stdin
    python3 scripts/editorial-calendar.py --status-id <id> <status>  # update entry
    python3 scripts/editorial-calendar.py --print     # print only
"""

import argparse
import json
import os
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE_AGENT = Path("/opt/data/agents/state/editorial-calendar.json")
STATE_FILE_LIVE = Path("/opt/data/state/editorial-calendar.json")

VALID_STATUSES = {"idea", "drafting", "peer_review", "final", "published", "retracted"}


def atomic_write_json(path: Path, payload: dict) -> None:
    """P2 pattern."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            path.replace(path.with_suffix(path.suffix + ".bak"))
        except OSError:
            pass
    fd, tmp = tempfile.mkstemp(prefix=".editorial-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def load_state() -> dict:
    if STATE_FILE_AGENT.exists():
        try:
            return json.loads(STATE_FILE_AGENT.read_text())
        except json.JSONDecodeError:
            pass
    return {"version": "1.0.0", "updated_at": None, "entries": []}


def save_state(state: dict) -> None:
    state["updated_at"] = datetime.now(timezone.utc).isoformat()
    atomic_write_json(STATE_FILE_AGENT, state)
    try:
        atomic_write_json(STATE_FILE_LIVE, state)
    except OSError:
        pass


def cmd_add(args):
    state = load_state()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "title": args.title,
        "type": args.type or "blog_post",
        "status": "idea",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "deadline": args.deadline,
        "owner": args.owner or "ivan",
        "notes": args.notes or "",
    }
    state["entries"].append(entry)
    save_state(state)
    print(f"Added entry: {entry['id']} — {entry['title']}")
    return 0


def cmd_status(args):
    state = load_state()
    target = next((e for e in state["entries"] if e["id"] == args.id), None)
    if not target:
        print(f"ERROR: no entry with id {args.id}", file=sys.stderr)
        return 2
    if args.status not in VALID_STATUSES:
        print(f"ERROR: invalid status {args.status} (valid: {sorted(VALID_STATUSES)})", file=sys.stderr)
        return 2
    target["status"] = args.status
    target["status_updated_at"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print(f"Updated {args.id} → {args.status}")
    return 0


def cmd_print(args):
    state = load_state()
    print(json.dumps(state, indent=2, sort_keys=True))
    return 0


def cmd_summary(state=None):
    state = state or load_state()
    entries = state["entries"]
    by_status = {s: 0 for s in VALID_STATUSES}
    for e in entries:
        by_status[e["status"]] = by_status.get(e["status"], 0) + 1
    stale = []
    now = datetime.now(timezone.utc)
    for e in entries:
        if e["status"] in ("idea", "drafting", "peer_review", "final") and e.get("deadline"):
            try:
                # Accept both ISO datetime and date-only
                dl_str = e["deadline"]
                if "T" in dl_str:
                    dl = datetime.fromisoformat(dl_str.replace("Z", "+00:00"))
                else:
                    # date-only → end-of-day UTC
                    dl = datetime.fromisoformat(dl_str + "T23:59:59+00:00")
                if dl < now:
                    stale.append(f"{e['id']} ({e['title']}, deadline {e['deadline']})")
            except ValueError:
                pass

    atomic_write_json(STATE_FILE_AGENT, state)
    try:
        atomic_write_json(STATE_FILE_LIVE, state)
    except OSError:
        pass

    print(f"Editorial calendar: {len(entries)} entries | "
          f"idea={by_status['idea']} drafting={by_status['drafting']} "
          f"peer_review={by_status['peer_review']} final={by_status['final']} "
          f"published={by_status['published']}")
    if stale:
        print(f"  STALE: {len(stale)} entries past deadline:")
        for s in stale:
            print(f"    - {s}")
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "Editorial calendar")
    sub = p.add_subparsers(dest="cmd")

    # add
    pa = sub.add_parser("add", help="Add new entry")
    pa.add_argument("title", help="Entry title")
    pa.add_argument("--type", choices=["blog_post", "thesis_chapter", "course_module",
                                       "paper", "whitepaper", "social_post"],
                    default="blog_post")
    pa.add_argument("--deadline", help="ISO deadline (or null)")
    pa.add_argument("--owner", default="ivan", help="Owner (default: ivan)")
    pa.add_argument("--notes", help="Notes")

    # status
    ps = sub.add_parser("status", help="Update entry status")
    ps.add_argument("id", help="Entry id")
    ps.add_argument("status", help=f"New status ({sorted(VALID_STATUSES)})")

    # print
    pp = sub.add_parser("print", help="Print state")

    # summary (default)
    args = p.parse_args(argv)

    if args.cmd == "add":
        return cmd_add(args)
    elif args.cmd == "status":
        return cmd_status(args)
    elif args.cmd == "print":
        return cmd_print(args)
    else:
        return cmd_summary()


if __name__ == "__main__":
    sys.exit(main())