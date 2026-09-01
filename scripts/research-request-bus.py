#!/usr/bin/env python3
"""research-request-bus.py — Cross-dept research request signal queue.

Phase 9 R3 / Tier C3 / Gap 5. Cross-dept research requests use a signal
queue at /opt/data/state/research-requests.ndjson. Each request is one
JSON line: {"from": "<dept>", "to": "05-research-education", "topic": "...",
"priority": "P0|P1|P2|P3", "timestamp": "..."}.

The research-associate agent reads this queue and produces research
deliverables, with results appended back as research-responses.

CLI:
  python3 research-request-bus.py post --from <dept> --topic <text> --priority P1
  python3 research-request-bus.py list
  python3 research-request-bus.py fulfill --id <request_id> --response <path>
"""
import argparse
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

QUEUE_PATH = Path("/opt/data/state/research-requests.ndjson")
RESPONSES_PATH = Path("/opt/data/state/research-responses.ndjson")


def _now():
    return datetime.now(timezone.utc).isoformat()


def post(from_dept: str, topic: str, priority: str) -> int:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    req = {
        "id": uuid.uuid4().hex[:12],
        "from": from_dept,
        "to": "05-research-education",
        "topic": topic,
        "priority": priority,
        "timestamp": _now(),
        "status": "pending",
    }
    with QUEUE_PATH.open("a") as f:
        f.write(json.dumps(req) + "\n")
    print(f"[bus] Request {req['id']} posted from {from_dept} (priority={priority})")
    return 0


def list_requests() -> int:
    if not QUEUE_PATH.exists():
        print("[bus] No requests")
        return 0
    pending = []
    with QUEUE_PATH.open() as f:
        for line in f:
            try:
                req = json.loads(line.strip())
                if req.get("status") == "pending":
                    pending.append(req)
            except json.JSONDecodeError:
                continue
    print(f"[bus] {len(pending)} pending requests:")
    for r in pending[:20]:
        print(f"  {r['id']} [{r['priority']}] from {r['from']}: {r['topic'][:60]}")
    return 0


def fulfill(request_id: str, response_path: str) -> int:
    if not QUEUE_PATH.exists():
        print(f"[bus] No queue")
        return 1
    requests = []
    with QUEUE_PATH.open() as f:
        for line in f:
            try:
                req = json.loads(line.strip())
                if req["id"] == request_id:
                    req["status"] = "fulfilled"
                    req["response"] = response_path
                    req["fulfilled_at"] = _now()
                requests.append(req)
            except json.JSONDecodeError:
                continue
    with QUEUE_PATH.open("w") as f:
        for r in requests:
            f.write(json.dumps(r) + "\n")
    # Append to responses log
    response = {
        "request_id": request_id,
        "response_path": response_path,
        "timestamp": _now(),
    }
    with RESPONSES_PATH.open("a") as f:
        f.write(json.dumps(response) + "\n")
    print(f"[bus] Request {request_id} fulfilled → {response_path}")
    return 0


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_post = sub.add_parser("post", help="Post a new request")
    p_post.add_argument("--from", dest="from_dept", required=True)
    p_post.add_argument("--topic", required=True)
    p_post.add_argument("--priority", default="P2", choices=["P0", "P1", "P2", "P3"])

    sub.add_parser("list", help="List pending requests")

    p_fulfill = sub.add_parser("fulfill", help="Mark request fulfilled")
    p_fulfill.add_argument("--id", required=True)
    p_fulfill.add_argument("--response", required=True)

    args = parser.parse_args()
    if args.cmd == "post":
        return post(args.from_dept, args.topic, args.priority)
    if args.cmd == "list":
        return list_requests()
    if args.cmd == "fulfill":
        return fulfill(args.id, args.response)
    return 0


if __name__ == "__main__":
    sys.exit(main())