"""Weekly summary cron — Phase 4.2 of AIW upgrade plan.

Generates a weekly digest of:
  - Agent traces (state/agent-traces.jsonl) — which agents ran, how often
  - Decision log (state/coord.json) — decisions_for_ivan items
  - Routing activity (state/routing-decisions.jsonl) — what got routed
  - Memory L1 commitments extracted
  - Stale repos + chronic state issues

Writes to outbox/summaries/weekly-YYYY-WW.md
Archives source data to state/snapshots/weekly/YYYY-WW/ for replay.

Usage:
  python3 -m scripts.cron.weekly_summary [--dry-run] [--week 2026-W36]
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# Defaults
DEFAULT_TRACES = Path("/opt/data/state/agent-traces.jsonl")
DEFAULT_COORD = Path("/opt/data/agents/state/coord.json")
DEFAULT_ROUTING = Path("/opt/data/state/routing-decisions.jsonl")
DEFAULT_OUTBOX = Path("/opt/data/agents/demiurge/agents/management-coordinator/outbox/summaries")
DEFAULT_SNAPSHOTS = Path("/opt/data/agents/state/snapshots/weekly")


def _iso_week(now: datetime) -> str:
    y, w, _ = now.isocalendar()
    return f"{y}-W{w:02d}"


def _read_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    out = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def _read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def generate_summary(week: str, traces_path: Path = DEFAULT_TRACES,
                    coord_path: Path = DEFAULT_COORD,
                    routing_path: Path = DEFAULT_ROUTING,
                    outbox_path: Path = DEFAULT_OUTBOX,
                    snapshots_path: Path = DEFAULT_SNAPSHOTS,
                    dry_run: bool = False) -> dict:
    """Build a weekly summary dict. Returns a report."""
    traces = _read_jsonl(traces_path)
    coord = _read_json(coord_path)
    routing = _read_jsonl(routing_path)
    decisions = coord.get("decisions_for_ivan", [])
    commitments = coord.get("commitments", [])

    # Compute week boundaries (Monday-Sunday)
    year_str, week_str = week.split("-W")
    year, wk = int(year_str), int(week_str)
    # Find the Monday of this ISO week
    jan4 = datetime(year, 1, 4, tzinfo=timezone.utc)
    week_1_monday = jan4 - timedelta(days=jan4.weekday())
    week_start = week_1_monday + timedelta(weeks=wk - 1)
    week_end = week_start + timedelta(days=7)

    # Filter items in this week
    def in_week(ts_str: str) -> bool:
        if not ts_str:
            return False
        try:
            t = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return False
        return week_start <= t < week_end

    week_traces = [t for t in traces if in_week(t.get("ts", ""))]
    week_routing = [r for r in routing if in_week(r.get("ts", ""))]
    week_decisions = [d for d in decisions if in_week(d.get("raised_at", ""))]

    # Aggregate
    agent_counts = Counter(t.get("agent", "unknown") for t in week_traces)
    rule_counts = Counter(r.get("rule_id", "unknown") for r in week_routing)
    no_rule_count = sum(1 for r in week_routing if r.get("result") == "no_rule")
    degraded_count = sum(1 for r in week_routing if r.get("degraded"))
    avg_latency = (sum(r.get("latency_ms", 0) for r in week_routing) / len(week_routing)
                  if week_routing else 0)

    # Build summary text
    md = []
    md.append(f"# Weekly Summary — {week}")
    md.append("")
    md.append(f"**Generated:** {datetime.now(timezone.utc).isoformat()}")
    md.append(f"**Period:** {week_start.date()} to {week_end.date()}")
    md.append("")
    md.append("## Activity")
    md.append("")
    md.append(f"- **Agent traces:** {len(week_traces)} (total: {len(traces)})")
    md.append(f"- **Routing decisions:** {len(week_routing)} (total: {len(routing)})")
    md.append(f"- **Decisions for ivan:** {len(week_decisions)} (current queue: {len(decisions)})")
    md.append(f"- **Commitments tracked:** {len(commitments)}")
    md.append("")
    md.append("## Top agents by activity")
    md.append("")
    for agent, count in agent_counts.most_common(10):
        md.append(f"- `{agent}`: {count} traces")
    md.append("")
    md.append("## Top routing rules")
    md.append("")
    for rule, count in rule_counts.most_common(10):
        md.append(f"- `{rule}`: {count} hits")
    md.append("")
    md.append("## Routing health")
    md.append("")
    md.append(f"- No-rule rate: {no_rule_count} / {len(week_routing)} "
              f"({100*no_rule_count/max(1,len(week_routing)):.1f}%)")
    md.append(f"- Degraded-rule rate: {degraded_count} / {len(week_routing)} "
              f"({100*degraded_count/max(1,len(week_routing)):.1f}%)")
    md.append(f"- Average latency: {avg_latency:.1f} ms")
    md.append("")
    if week_decisions:
        md.append("## Decisions raised this week (top 5)")
        md.append("")
        for d in week_decisions[:5]:
            q = d.get("question", "")[:120]
            md.append(f"- {q}...")
        md.append("")

    md_text = "\n".join(md)

    if not dry_run:
        outbox_path.mkdir(parents=True, exist_ok=True)
        out_path = outbox_path / f"weekly-{week}.md"
        out_path.write_text(md_text)

        # Archive source data
        snapshots_path.mkdir(parents=True, exist_ok=True)
        week_snap = snapshots_path / week
        week_snap.mkdir(exist_ok=True)
        (week_snap / "traces.jsonl").write_text(
            "\n".join(json.dumps(t) for t in week_traces) + "\n"
            if week_traces else "")
        (week_snap / "routing.jsonl").write_text(
            "\n".join(json.dumps(r) for r in week_routing) + "\n"
            if week_routing else "")

    return {
        "week": week,
        "week_start": week_start.isoformat(),
        "week_end": week_end.isoformat(),
        "stats": {
            "traces": len(week_traces),
            "routing": len(week_routing),
            "decisions": len(week_decisions),
            "commitments": len(commitments),
        },
        "no_rule_count": no_rule_count,
        "degraded_count": degraded_count,
        "avg_latency_ms": round(avg_latency, 1),
        "top_agents": agent_counts.most_common(10),
        "top_rules": rule_counts.most_common(10),
        "out_path": str(outbox_path / f"weekly-{week}.md") if not dry_run else None,
        "snapshot_path": str(snapshots_path / week) if not dry_run else None,
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Weekly summary cron")
    parser.add_argument("--traces", type=Path, default=DEFAULT_TRACES)
    parser.add_argument("--coord", type=Path, default=DEFAULT_COORD)
    parser.add_argument("--routing", type=Path, default=DEFAULT_ROUTING)
    parser.add_argument("--outbox", type=Path, default=DEFAULT_OUTBOX)
    parser.add_argument("--snapshots", type=Path, default=DEFAULT_SNAPSHOTS)
    parser.add_argument("--week", type=str, default=None,
                        help="ISO week (e.g. 2026-W36). Default: current week.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    week = args.week or _iso_week(datetime.now(timezone.utc))
    report = generate_summary(
        week=week,
        traces_path=args.traces,
        coord_path=args.coord,
        routing_path=args.routing,
        outbox_path=args.outbox,
        snapshots_path=args.snapshots,
        dry_run=args.dry_run,
    )
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
