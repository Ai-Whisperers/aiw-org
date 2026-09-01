#!/usr/bin/env python3
"""Cron auto-fix — apply cost-optimization findings to cron registry.

Built as Phase 35 R1 (Q1a).

Reads /opt/data/state/cost-optimization.json and applies:
  - Resume enabled crons (with confirmation)
  - Stagger overlapping schedules (auto, with stagger offset)

Always operates in dry-run by default. Use --apply to commit changes.

Usage:
    python3 scripts/cron-autofix.py              # dry-run all
    python3 scripts/cron-autofix.py --resume     # resume only
    python3 scripts/cron-autofix.py --stagger    # stagger only
    python3 scripts/cron-autofix.py --apply      # commit changes
"""
import argparse
import json
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

CRON_PATH = Path("/opt/data/.hermes/cron/jobs.json")
CANON_PATH = Path("/opt/data/cron/jobs.json")
FINDINGS_PATH = Path("/opt/data/state/cost-optimization.json")
AUDIT_LOG = Path("/opt/data/state/cron-autofix-audit.ndjson")


def load_findings() -> dict:
    """Load cost-optimization findings."""
    if not FINDINGS_PATH.exists():
        return {}
    try:
        return json.loads(FINDINGS_PATH.read_text())
    except json.JSONDecodeError:
        return {}


def find_disabled_to_resume(jobs: list) -> list:
    """Find safe-to-resume crons (excluding cancelled/completed)."""
    safe = []
    for j in jobs:
        state = j.get("state")
        enabled = j.get("enabled", True)
        if enabled is False and state in ("scheduled",):
            # State is scheduled but enabled=False — was paused
            safe.append({
                "name": j.get("name"),
                "reason": f"state={state} enabled={enabled}",
            })
    return safe


def find_stagger_candidates(jobs: list, max_stagger: int = 5) -> list:
    """Find top N overlapping schedules to stagger.

    Returns list of {schedule, crons, keep_name, stagger_plan} dicts.
    """
    by_schedule = defaultdict(list)
    for j in jobs:
        if not j.get("enabled", True):
            continue
        expr = j.get("schedule", {}).get("expr")
        if not expr:
            continue
        by_schedule[expr].append(j.get("name"))

    overlaps = [(expr, names) for expr, names in by_schedule.items() if len(names) > 1]
    overlaps.sort(key=lambda x: -len(x[1]))

    candidates = []
    for expr, names in overlaps[:max_stagger]:
        keep = names[0]
        stagger_plan = {}
        for i, name in enumerate(names[1:], start=1):
            stagger_plan[name] = i
        candidates.append({
            "schedule": expr,
            "count": len(names),
            "keep": keep,
            "stagger_plan": stagger_plan,
        })
    return candidates


def shift_n_schedule(expr: str, offset: int) -> "str | None":
    """Shift */N to specific minutes by offset. Returns None if invalid."""
    parts = expr.split()
    if not parts or not parts[0].startswith("*/"):
        return expr
    n = int(parts[0][2:])
    if offset >= n:
        return None
    minutes = []
    for k in range(0, 60, n):
        new_min = (k + offset) % 60
        if new_min not in minutes:
            minutes.append(new_min)
    minutes.sort()
    return ",".join(str(m) for m in minutes) + " " + " ".join(parts[1:])


def shift_fixed_minute(expr: str, offset: int) -> "str | None":
    """Shift fixed minute by offset. Returns None if invalid."""
    parts = expr.split()
    if len(parts) != 5 or not parts[0].isdigit():
        return expr
    if "*" in parts[0]:
        return expr
    new_min = (int(parts[0]) + offset) % 60
    new_hour = parts[1]
    if parts[1].isdigit():
        hour_offset = (int(parts[0]) + offset) // 60
        new_hour = str((int(parts[1]) + hour_offset) % 24)
    return " ".join([str(new_min), new_hour] + parts[2:])


def compute_new_schedules(jobs: list, candidates: list) -> dict:
    """Compute new schedule for each cron to be staggered."""
    new_schedules = {}
    for cand in candidates:
        expr = cand["schedule"]
        for cron_name, offset in cand["stagger_plan"].items():
            for j in jobs:
                if j.get("name") == cron_name and j.get("schedule", {}).get("expr") == expr:
                    if expr.startswith("*/"):
                        new = shift_n_schedule(expr, offset)
                    else:
                        new = shift_fixed_minute(expr, offset)
                    if new:
                        new_schedules[cron_name] = (expr, new)
                    break
    return new_schedules


def apply_resumes(jobs: list, to_resume: list) -> int:
    """Set enabled=True for safe-to-resume crons."""
    by_name = {j.get("name"): j for j in jobs}
    applied = 0
    for r in to_resume:
        name = r["name"]
        if name in by_name:
            by_name[name]["enabled"] = True
            by_name[name]["state"] = "scheduled"
            by_name[name]["paused_reason"] = None
            applied += 1
    return applied


def apply_staggers(jobs: list, new_schedules: dict) -> int:
    """Apply new schedules to crons."""
    by_name = {j.get("name"): j for j in jobs}
    applied = 0
    for name, (old_expr, new_expr) in new_schedules.items():
        if name in by_name and by_name[name].get("schedule", {}).get("expr") == old_expr:
            by_name[name]["schedule"]["expr"] = new_expr
            by_name[name]["schedule"]["display"] = new_expr
            applied += 1
    return applied


def write_cron_files(jobs: list, wrapped: bool = False) -> None:
    """Write jobs.json atomically + mirror to canonical.

    If jobs is a bare list (wrapped=True), we re-wrap it as {jobs: [...]}.
    Otherwise, we preserve the existing structure.
    """
    payload = {"jobs": jobs} if wrapped else jobs
    tmpname = str(CRON_PATH) + ".tmp"
    with open(tmpname, "w") as f:
        json.dump(payload, f, indent=2)
    shutil.move(tmpname, str(CRON_PATH))

    if CANON_PATH.exists():
        tmpname2 = str(CANON_PATH) + ".tmp"
        with open(tmpname2, "w") as f:
            json.dump(payload, f, indent=2)
        shutil.move(tmpname2, str(CANON_PATH))


def log_audit(action: str, target: str, details: dict) -> None:
    """Log autofix action to NDJSON audit log."""
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "target": target,
        "details": details,
    }
    with AUDIT_LOG.open("a") as f:
        f.write(json.dumps(entry, separators=(",", ":")) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Cron auto-fix from cost findings")
    parser.add_argument("--resume", action="store_true", help="Resume disabled crons only")
    parser.add_argument("--stagger", action="store_true", help="Stagger overlapping only")
    parser.add_argument("--apply", action="store_true", help="Apply (commit) changes")
    parser.add_argument("--max-stagger", type=int, default=5,
                        help="Max overlapping schedules to stagger (default 5)")
    args = parser.parse_args()

    if not CRON_PATH.exists():
        print("ERROR: cron jobs.json missing")
        return 1

    with open(CRON_PATH) as f:
        data = json.load(f)
    # Handle both wrapped {jobs: [...]} and bare list structures
    if isinstance(data, list):
        # Bare list (broken structure) - wrap it
        jobs = data
        wrapped = True
    else:
        jobs = data.get("jobs", [])
        wrapped = False

    findings = load_findings()
    to_resume = find_disabled_to_resume(jobs)
    stagger_candidates = find_stagger_candidates(jobs, max_stagger=args.max_stagger)
    new_schedules = compute_new_schedules(jobs, stagger_candidates)

    print(f"=== Cron Auto-Fix ===")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print(f"Resume candidates: {len(to_resume)}")
    print(f"Stagger candidates: {len(stagger_candidates)} ({sum(len(c['stagger_plan']) for c in stagger_candidates)} crons)")
    print()

    if to_resume:
        print("--- Resume plan ---")
        for r in to_resume:
            print(f"  {r['name']} ({r['reason']})")
        print()

    if stagger_candidates:
        print("--- Stagger plan ---")
        for cand in stagger_candidates:
            print(f"  {cand['schedule']} (keep {cand['keep']}, stagger {len(cand['stagger_plan'])})")
            for name, offset in cand["stagger_plan"].items():
                old, new = new_schedules.get(name, (cand["schedule"], cand["schedule"]))
                print(f"    {name}: {old} -> {new} (offset +{offset}min)")
        print()

    if not args.apply:
        print("(dry-run; use --apply to commit)")
        return 0

    # Apply
    n_resumed = apply_resumes(jobs, to_resume) if not args.stagger else 0
    n_staggered = apply_staggers(jobs, new_schedules) if not args.resume else 0
    if n_resumed or n_staggered:
        write_cron_files(jobs, wrapped=wrapped)
        log_audit("cron-autofix", "jobs.json", {
            "resumed": n_resumed,
            "staggered": n_staggered,
        })

    print(f"Applied: {n_resumed} resumed, {n_staggered} staggered")
    return 0


if __name__ == "__main__":
    sys.exit(main())
