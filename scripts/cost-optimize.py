#!/usr/bin/env python3
"""G7 cost optimization — find unused cron capacity + optimization opportunities.

Built as Phase 33 R5.

Reads:
  - /opt/data/.hermes/cron/jobs.json (cron registry)
  - /opt/data/state/cron-error-watchdog.json (recent errors)
  - /opt/data/state/cost-tracker.json (per-agent costs)

Outputs:
  - /opt/data/state/cost-optimization-report.md
  - /opt/data/state/cost-optimization.json

Finds:
  1. Disabled/paused crons (wasted slots)
  2. Frequent-error crons (high cost, low value)
  3. Overlapping schedule crons (same agent, similar time)
  4. Off-hours crons with no recent activity
  5. Recommended optimizations

Usage:
    python3 scripts/cost-optimize.py             # full analysis
    python3 scripts/cost-optimize.py --suggest   # just recommendations
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CRON_PATH = Path("/opt/data/.hermes/cron/jobs.json")
WATCHDOG = Path("/opt/data/state/cron-error-watchdog.json")
COST_TRACKER = Path("/opt/data/state/cost-tracker.json")
OUTPUT_MD = Path("/opt/data/state/cost-optimization-report.md")
OUTPUT_JSON = Path("/opt/data/state/cost-optimization.json")


def load_jobs() -> list:
    if not CRON_PATH.exists():
        return []
    with open(CRON_PATH) as f:
        return json.load(f).get("jobs", [])


def load_watchdog() -> dict:
    if not WATCHDOG.exists():
        return {}
    try:
        return json.loads(WATCHDOG.read_text())
    except Exception:
        return {}


def load_costs() -> dict:
    if not COST_TRACKER.exists():
        return {}
    try:
        return json.loads(COST_TRACKER.read_text())
    except Exception:
        return {}


def find_disabled(jobs: list) -> list:
    """Crons that are paused or disabled."""
    return [{
        "name": j.get("name"),
        "schedule": j.get("schedule", {}).get("expr"),
        "state": j.get("state"),
        "paused_reason": j.get("paused_reason"),
    } for j in jobs if not j.get("enabled", True) or j.get("state") in ("paused", "disabled")]


def find_failing(jobs: list, watchdog: dict) -> list:
    """Crons with recent errors (per watchdog)."""
    details = watchdog.get("details", [])
    failing = {}
    for entry in details:
        name = entry.get("name")
        if name:
            failing[name] = failing.get(name, 0) + 1
    return [
        {"name": name, "error_count": count}
        for name, count in sorted(failing.items(), key=lambda x: -x[1])[:10]
    ]


def find_overlapping(jobs: list, proximity_window_min: int = 60,
                    min_cluster_size: int = 3) -> list:
    """Find crons that pile up in the same time window on the same day.

    Phase 9 R3 / Tier B2 fix. The previous implementation bucketed by exact
    cron-expr string, which missed real pile-ups like the 2026-08-30 Sunday
    stack ('0 18 * * 0', '30 19 * * 0', '0 20 * * 0', '0 21 * * 0' — 4
    distinct strings but all within ~3.5h on Sunday causing 429s).

    Algorithm:
      1. For each cron, generate fire times for the next 7 days
      2. Cluster fires by (day_of_week, hour) — so all Sunday-19:00 fires
         are in one cluster regardless of which cron produced them
      3. Report clusters with >= min_cluster_size distinct crons that fire
         within proximity_window_min of each other

    Args:
      jobs: list of cron job dicts (with schedule.expr and enabled)
      proximity_window_min: minutes within which to consider fires "same time"
      min_cluster_size: minimum distinct crons to flag a cluster as pile-up

    Returns:
      List of {day, hour, crons, fire_count} dicts (real pile-ups only)
    """
    from collections import defaultdict
    from datetime import datetime, timedelta, timezone
    from croniter import croniter

    horizon = datetime.now(timezone.utc) + timedelta(days=7)
    fires_by_job = {}
    for j in jobs:
        if not j.get("enabled", True):
            continue
        expr = j.get("schedule", {}).get("expr")
        if not expr:
            continue
        try:
            it = croniter(expr, datetime.now(timezone.utc))
            fires = []
            while len(fires) < 50:
                nxt = it.get_next(datetime)
                if nxt > horizon:
                    break
                fires.append(nxt)
            fires_by_job[j["name"]] = fires
        except Exception:
            continue

    # Cluster: bucket = (dow) → list of (job_name, fire_time)
    # (not by hour — fires within proximity_window_min can span hours)
    clusters = defaultdict(list)
    for name, fires in fires_by_job.items():
        for f in fires:
            if f.tzinfo is None:
                f = f.replace(tzinfo=timezone.utc)
            else:
                f = f.astimezone(timezone.utc)
            key = f.weekday()
            clusters[key].append((name, f))

    # For each (day) cluster, find sub-clusters where fires are within proximity_window_min
    pileups = []
    for dow, entries in clusters.items():
        entries.sort(key=lambda x: x[1])
        sub_clusters = []
        current = [entries[0]]
        for e in entries[1:]:
            if (e[1] - current[-1][1]).total_seconds() / 60 <= proximity_window_min:
                current.append(e)
            else:
                if len({name for name, _ in current}) >= min_cluster_size:
                    sub_clusters.append(current)
                current = [e]
        if len({name for name, _ in current}) >= min_cluster_size:
            sub_clusters.append(current)

        for sc in sub_clusters:
            distinct_crons = sorted({name for name, _ in sc})
            pileups.append({
                "day_of_week": dow,
                "crons": distinct_crons,
                "fire_count": len(sc),
                "earliest_fire": sc[0][1].isoformat(),
                "latest_fire": sc[-1][1].isoformat(),
                "spread_minutes": round(
                    (sc[-1][1] - sc[0][1]).total_seconds() / 60, 1
                ),
            })

    # Sort by fire_count desc
    pileups.sort(key=lambda x: -x["fire_count"])
    return pileups


def find_low_activity(jobs: list, watchdog: dict) -> list:
    """Crons with no recent activity (last 7d)."""
    details = watchdog.get("details", [])
    active_names = {d.get("name") for d in details if d.get("name")}
    # Crons that should have run but haven't appeared in watchdog
    low_activity = []
    for j in jobs:
        name = j.get("name")
        if not j.get("enabled", True):
            continue
        if not name:
            continue
        last_run = j.get("last_run_at")
        if not last_run:
            low_activity.append({"name": name, "reason": "never ran"})
        elif name not in active_names:
            # Has run but not in recent watchdog activity
            last_run_dt = None
            try:
                last_run_dt = datetime.fromisoformat(last_run.replace("Z", "+00:00"))
            except Exception:
                pass
            if last_run_dt:
                age_days = (datetime.now(timezone.utc) - last_run_dt).days
                if age_days > 7:
                    low_activity.append({
                        "name": name,
                        "reason": f"last ran {age_days}d ago",
                        "last_run": last_run,
                    })
    return low_activity[:10]


def render_report(jobs: list, findings: dict, costs: dict) -> str:
    lines = [
        "# Cost Optimization Report (G7)",
        "",
        f"**Date**: {datetime.now(timezone.utc).isoformat()}",
        f"**Total jobs**: {len(jobs)}",
        f"**Enabled**: {sum(1 for j in jobs if j.get('enabled', True))}",
        f"**Disabled/paused**: {len(findings['disabled'])}",
        "",
        "## Disabled/Paused Crons",
        "",
    ]
    if not findings["disabled"]:
        lines.append("(none)")
    else:
        for d in findings["disabled"][:10]:
            lines.append(f"- **{d['name']}** — state: {d['state']}, reason: {d.get('paused_reason', 'none')}")
    lines.append("")

    lines.append("## High-Failure Crons")
    lines.append("")
    if not findings["failing"]:
        lines.append("(none — all crons healthy)")
    else:
        for f in findings["failing"]:
            lines.append(f"- **{f['name']}**: {f['error_count']} recent errors")
    lines.append("")

    lines.append("## Schedule Overlaps")
    lines.append("")
    if not findings["overlapping"]:
        lines.append("(none — all schedules unique)")
    else:
        for o in findings["overlapping"][:10]:
            lines.append(f"- **{o['schedule']}**: {len(o['crons'])} crons")
            for c in o["crons"]:
                lines.append(f"  - {c}")
    lines.append("")

    lines.append("## Low-Activity Crons")
    lines.append("")
    if not findings["low_activity"]:
        lines.append("(none — all crons active)")
    else:
        for la in findings["low_activity"]:
            lines.append(f"- **{la['name']}**: {la['reason']}")
    lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    recs = []
    if findings["disabled"]:
        n_disabled = len(findings["disabled"])
        recs.append(f"Resume or remove {n_disabled} disabled crons (currently consuming slots)")
    if findings["failing"]:
        top_fail = findings["failing"][0]
        recs.append(f"Investigate {top_fail['name']} ({top_fail['error_count']} errors) — consider disable until fixed")
    if findings["overlapping"]:
        for o in findings["overlapping"][:3]:
            recs.append(f"Schedule overlap at {o['schedule']}: {', '.join(o['crons'])} — consider staggering")
    if not recs:
        recs.append("(none — cron registry healthy)")
    for r in recs:
        lines.append(f"- {r}")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="G7 cost optimization")
    parser.add_argument("--suggest", action="store_true", help="Just print recommendations")
    args = parser.parse_args()

    jobs = load_jobs()
    watchdog = load_watchdog()
    costs = load_costs()

    findings = {
        "disabled": find_disabled(jobs),
        "failing": find_failing(jobs, watchdog),
        "overlapping": find_overlapping(jobs),
        "low_activity": find_low_activity(jobs, watchdog),
    }

    summary = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "total_jobs": len(jobs),
        "enabled": sum(1 for j in jobs if j.get("enabled", True)),
        "disabled_count": len(findings["disabled"]),
        "failing_count": len(findings["failing"]),
        "overlapping_count": len(findings["overlapping"]),
        "low_activity_count": len(findings["low_activity"]),
        "findings": findings,
    }

    # Outputs
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(json.dumps(summary, indent=2))
    OUTPUT_MD.write_text(render_report(jobs, findings, costs))

    if args.suggest:
        # Just print suggestions
        if findings["disabled"]:
            print(f"Resume/remove {len(findings['disabled'])} disabled crons")
        if findings["failing"]:
            top = findings["failing"][0]
            print(f"Investigate {top['name']} ({top['error_count']} errors)")
        if findings["overlapping"]:
            print(f"Stagger {len(findings['overlapping'])} overlapping schedules")
        return

    # JSON to stdout (parseable) + paths to stderr (informational)
    sys.stdout.write(json.dumps({
        "total_jobs": summary["total_jobs"],
        "enabled": summary["enabled"],
        "disabled": summary["disabled_count"],
        "failing": summary["failing_count"],
        "overlapping": summary["overlapping_count"],
        "low_activity": summary["low_activity_count"],
    }, indent=2) + "\n")
    sys.stderr.write(f"Report: {OUTPUT_MD}\n")
    sys.stderr.write(f"JSON: {OUTPUT_JSON}\n")


if __name__ == "__main__":
    main()
