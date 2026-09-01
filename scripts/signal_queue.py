#!/usr/bin/env python3
"""Signal queue — append-only NDJSON queue for incoming signals.

Built as Phase 28 R2 (A1 - Router).

A signal is a unit of work that needs routing. Signals are produced by:
- Webhooks (incoming leads, compliance flags, customer signals)
- Monitors (drift detected, eval-gate failed, cron error)
- Cron jobs (weekly content ready, deal stalled)
- Agents (need escalation, need review)

Each signal has:
  id:           unique signal ID (auto-generated)
  ts:           timestamp
  source:       who/what produced it (agent name, cron name, webhook name)
  signal_type:  cross_dept | inbound | outbound | internal
  routing_tags: list of tags (e.g., ["lead", "inbound"])
  department:   optional dept hint
  payload:      arbitrary dict with signal details
  status:       pending | routed | claimed | done | failed
  routed_at:    when router processed
  routed_to:    list of agents signal was delivered to

Usage:
    Append:    echo '{"source":"webhook","signal_type":"cross_dept","routing_tags":["lead"]}' \\
                   >> /opt/data/state/signal-queue.ndjson
    Process:   python3 scripts/router.py --process
    Inspect:   python3 scripts/router.py --list --status pending
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

SIGNAL_QUEUE = Path("/opt/data/state/signal-queue.ndjson")


def append_signal(signal: dict, queue_path: Path | None = None) -> dict:
    """Append a signal to the queue. Auto-assigns id + ts if missing.

    queue_path: explicit path; defaults to module SIGNAL_QUEUE at call time.
    """
    if queue_path is None:
        queue_path = SIGNAL_QUEUE
    if "id" not in signal:
        signal["id"] = f"sig-{uuid.uuid4().hex[:12]}"
    if "ts" not in signal:
        signal["ts"] = datetime.now(timezone.utc).isoformat()
    if "status" not in signal:
        signal["status"] = "pending"
    line = json.dumps(signal, separators=(",", ":")) + "\n"
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    with queue_path.open("a") as f:
        f.write(line)
    return signal


def list_signals(
    queue_path: Path | None = None,
    status: str | None = None,
    limit: int = 100,
) -> list[dict]:
    """Read signals from queue, optionally filter by status."""
    if queue_path is None:
        queue_path = SIGNAL_QUEUE
    if not queue_path.exists():
        return []
    out = []
    for line in queue_path.read_text().splitlines():
        if not line.strip():
            continue
        try:
            sig = json.loads(line)
        except json.JSONDecodeError:
            continue
        if status is None or sig.get("status") == status:
            out.append(sig)
        if len(out) >= limit:
            break
    return out


def update_signal_status(
    signal_id: str,
    new_status: str,
    queue_path: Path | None = None,
    extra: dict | None = None,
) -> bool:
    """Update a signal's status. Reads-modifies-writes the whole file.

    Phase 28 note: signals are infrequent (10s-100s per day), so the
    read-modify-write here is acceptable. If we ever go to 1000+/min,
    switch to a database-backed queue.
    """
    if queue_path is None:
        queue_path = SIGNAL_QUEUE
    if not queue_path.exists():
        return False
    lines = queue_path.read_text().splitlines()
    found = False
    new_lines = []
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        try:
            sig = json.loads(line)
        except json.JSONDecodeError:
            new_lines.append(line)
            continue
        if sig.get("id") == signal_id:
            sig["status"] = new_status
            if extra:
                sig.update(extra)
            found = True
        new_lines.append(json.dumps(sig, separators=(",", ":")))
    if found:
        queue_path.write_text("\n".join(new_lines) + "\n")
    return found


def main():
    parser = argparse.ArgumentParser(description="Signal queue operations")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # append
    p_append = sub.add_parser("append", help="Append a signal")
    p_append.add_argument("--source", required=True)
    p_append.add_argument("--signal-type", required=True)
    p_append.add_argument("--routing-tag", action="append", default=[],
                          help="Routing tag (can be repeated)")
    p_append.add_argument("--department", default=None)
    p_append.add_argument("--payload", default=None,
                          help="JSON string with signal details")

    # list
    p_list = sub.add_parser("list", help="List signals")
    p_list.add_argument("--status", default=None)
    p_list.add_argument("--limit", type=int, default=100)

    # update
    p_update = sub.add_parser("update", help="Update signal status")
    p_update.add_argument("--id", required=True)
    p_update.add_argument("--status", required=True,
                          choices=["pending", "routed", "claimed", "done", "failed"])

    args = parser.parse_args()
    if args.cmd == "append":
        payload = {}
        if args.payload:
            payload = json.loads(args.payload)
        sig = {
            "source": args.source,
            "signal_type": args.signal_type,
            "routing_tags": args.routing_tag,
            "department": args.department,
            "payload": payload,
        }
        out = append_signal(sig)
        print(f"Appended: {out['id']}")
        print(json.dumps(out, indent=2))
    elif args.cmd == "list":
        sigs = list_signals(status=args.status, limit=args.limit)
        print(f"Found {len(sigs)} signals")
        for s in sigs:
            tags = ",".join(s.get("routing_tags", []))
            print(f"  {s['id']} [{s['status']}] {s.get('source','?')} tags=[{tags}]")
    elif args.cmd == "update":
        ok = update_signal_status(args.id, args.status)
        print(f"Updated {args.id}: {ok}")


if __name__ == "__main__":
    main()
