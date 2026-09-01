#!/usr/bin/env python3
"""DORA 4-metrics aggregator.

Built Phase 7 R5 (implementation plan §4 Phase 1.1).

DORA's 4 metrics (per Accelerate / Forsgren, Humble, Kim 2018):
  1. Deployment Frequency (DF)         — how often we ship to prod
  2. Lead Time for Changes (LT)       — commit-to-deploy time
  3. Change Failure Rate (CFR)        — % of deploys that cause incidents
  4. Mean Time to Restore (MTTR)      — incident-to-resolution time

Sources (best-effort with what we have):
  - git log (commits merged into main = deploys, for prod-deploying repos)
  - /opt/data/state/cron-error-watchdog.json  (incidents = cron jobs in error)
  - /opt/data/state/eval-per-agent.json  (agent-level eval failures)
  - /opt/data/state/engineering.json    (deploy_7d, incidents_72h)

Output:
  - /opt/data/agents/state/dora-metrics.json  (atomic write per P2 pattern)
  - /opt/data/state/dora-metrics.json         (mirror)

Classification (per DORA 2024 report):
  - Elite:    DF=on-demand, LT<1d, CFR<5%,  MTTR<1h
  - High:     DF=daily-weekly, LT<1w, CFR<20%, MTTR<1d
  - Medium:   DF=weekly-monthly, LT<1mo, CFR<30%, MTTR<1w
  - Low:      DF=<monthly, longer LT/CFR/MTTR

Usage:
    python3 scripts/dora-metrics-aggregator.py            # compute + write
    python3 scripts/dora-metrics-aggregator.py --print    # print only
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- Configuration ----------------------------------------------------------

DEFAULT_WINDOW_DAYS = 28
AGENTS_REPO = Path("/opt/data/agents")
CRON_ERROR_FILE = Path("/opt/data/state/cron-error-watchdog.json")
EVAL_FILE = Path("/opt/data/state/eval-per-agent.json")
ENGINEERING_STATE = Path("/opt/data/agents/state/engineering.json")

STATE_FILE_AGENT = Path("/opt/data/agents/state/dora-metrics.json")
STATE_FILE_LIVE = Path("/opt/data/state/dora-metrics.json")

# Detect branch (master vs main)
def _detect_branch(repo: Path) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=5
        )
        branch = r.stdout.strip()
        return branch if branch else "master"
    except Exception:
        return "master"

# DORA classification thresholds (per 2024 DORA report)
DORA_THRESHOLDS = {
    "elite": {
        "df_max_hours": 24,  # on-demand = <1 day
        "lt_max_hours": 24,  # <1 day
        "cfr_max_pct": 5.0,
        "mttr_max_minutes": 60,
    },
    "high": {
        "df_max_hours": 168,  # daily to weekly
        "lt_max_hours": 168,  # 1d to 1w
        "cfr_max_pct": 20.0,
        "mttr_max_minutes": 1440,  # 1 day
    },
    "medium": {
        "df_max_hours": 720,  # weekly to monthly
        "lt_max_hours": 720,  # 1w to 1mo
        "cfr_max_pct": 30.0,
        "mttr_max_minutes": 10080,  # 1 week
    },
}


# --- Helpers ----------------------------------------------------------------

def atomic_write_json(path: Path, payload: dict) -> None:
    """P2 pattern: atomic write with .tmp + rename + .bak."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        try:
            path.replace(path.with_suffix(path.suffix + ".bak"))
        except OSError:
            pass
    fd, tmp = tempfile.mkstemp(prefix=".dora-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def parse_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        if ts.endswith("Z"):
            ts = ts[:-1] + "+00:00"
        return datetime.fromisoformat(ts)
    except ValueError:
        return None


# --- Metric 1 & 2: Deploy frequency + lead time -----------------------------

def git_deploy_metrics(repo: Path, window_days: int) -> dict:
    """Read git log of commits to main/master within window.

    AIW workflow: direct commits to master (no merge commits). Each commit
    to the main branch = 1 deploy (proxy). PRs merged via squash would also
    appear here.

    Returns:
      {
        "deploy_count": int,
        "deploys_per_week": float,
        "lead_time_hours_avg": float (commit-to-commit median lag, proxy for LT),
        "first_deploy_at": iso | None,
        "last_deploy_at": iso | None
      }
    """
    if not (repo / ".git").exists():
        return {
            "deploy_count": 0,
            "deploys_per_week": 0.0,
            "lead_time_hours_avg": None,
            "first_deploy_at": None,
            "last_deploy_at": None,
            "source": "no-git-repo",
        }

    branch = _detect_branch(repo)
    since = (datetime.now(timezone.utc) - timedelta(days=window_days)).isoformat()

    # Get commits to main branch within window (proxy for deploys)
    try:
        result = subprocess.run(
            ["git", "-C", str(repo), "log", branch,
             "--since", since, "--pretty=format:%H|%cI|%s"],
            capture_output=True, text=True, timeout=10
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return {"deploy_count": 0, "deploys_per_week": 0.0,
                "lead_time_hours_avg": None, "first_deploy_at": None,
                "last_deploy_at": None, "source": "git-error"}

    commits = []
    for line in result.stdout.strip().splitlines():
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        sha, ts_iso, _subject = parts
        ts = parse_iso(ts_iso)
        if ts:
            commits.append({"sha": sha, "ts": ts})

    if not commits:
        return {"deploy_count": 0, "deploys_per_week": 0.0,
                "lead_time_hours_avg": None, "first_deploy_at": None,
                "last_deploy_at": None, "source": "no-commits-in-window"}

    # Lead time proxy: median time between consecutive commits
    sorted_commits = sorted(commits, key=lambda c: c["ts"])
    gaps_hours = []
    for i in range(1, len(sorted_commits)):
        gap = (sorted_commits[i]["ts"] - sorted_commits[i - 1]["ts"]).total_seconds() / 3600.0
        if gap >= 0:
            gaps_hours.append(gap)
    median_lt = sorted(gaps_hours)[len(gaps_hours) // 2] if gaps_hours else None

    weeks = window_days / 7.0
    deploys_per_week = len(commits) / weeks if weeks > 0 else 0.0

    return {
        "deploy_count": len(commits),
        "deploys_per_week": round(deploys_per_week, 2),
        "lead_time_hours_avg": round(median_lt, 2) if median_lt is not None else None,
        "first_deploy_at": sorted_commits[0]["ts"].isoformat(),
        "last_deploy_at": sorted_commits[-1]["ts"].isoformat(),
        "source": f"git-commit-count-{branch}",
    }


# --- Metric 3: Change failure rate -----------------------------------------

def cron_error_metrics(window_days: int) -> dict:
    """Cron errors = incidents. CFR proxy = cron_errors / deploys.

    If a cron job goes into error state after a recent deploy, that's
    a "change-induced failure".
    """
    if not CRON_ERROR_FILE.exists():
        return {"incidents_in_window": 0, "details": [], "source": "no-state-file"}

    try:
        data = json.loads(CRON_ERROR_FILE.read_text())
    except json.JSONDecodeError:
        return {"incidents_in_window": 0, "details": [], "source": "state-file-corrupt"}

    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    details = data.get("details", [])
    in_window = []
    for d in details:
        last_run = parse_iso(d.get("last_run_at", ""))
        if last_run and last_run >= cutoff:
            in_window.append({
                "name": d.get("name", "?"),
                "schedule": d.get("schedule", "?"),
                "last_run_at": d.get("last_run_at"),
                "error_snippet": (d.get("last_error", "") or "")[:120],
            })
    return {
        "incidents_in_window": len(in_window),
        "details": in_window,
        "source": "cron-error-watchdog",
    }


# --- Metric 4: MTTR ---------------------------------------------------------

def mttr_minutes(window_days: int) -> dict:
    """Mean time to restore. Proxy: time between last_run_at (failure)
    and the next successful run.

    For each cron job that errored, find when it next succeeded.
    """
    if not CRON_ERROR_FILE.exists():
        return {"mttr_minutes": None, "samples": 0, "source": "no-state-file"}

    try:
        data = json.loads(CRON_ERROR_FILE.read_text())
    except json.JSONDecodeError:
        return {"mttr_minutes": None, "samples": 0, "source": "state-file-corrupt"}

    # We don't have explicit recovery timestamps in cron-error-watchdog.
    # Use engineering.json incidents_72h as a proxy: each entry has a recovery time.
    if not ENGINEERING_STATE.exists():
        return {"mttr_minutes": None, "samples": 0, "source": "no-engineering-state"}

    try:
        eng = json.loads(ENGINEERING_STATE.read_text())
    except json.JSONDecodeError:
        return {"mttr_minutes": None, "samples": 0, "source": "engineering-state-corrupt"}

    incidents = eng.get("incidents_72h", [])
    if not incidents:
        return {"mttr_minutes": None, "samples": 0, "source": "no-incidents-recorded"}

    # Compute MTTR from incidents that have started_at + resolved_at
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    durations = []
    for inc in incidents:
        if not isinstance(inc, dict):
            continue
        started = parse_iso(inc.get("started_at", ""))
        resolved = parse_iso(inc.get("resolved_at", ""))
        if started and resolved and started >= cutoff and resolved >= started:
            durations.append((resolved - started).total_seconds() / 60.0)

    if not durations:
        return {"mttr_minutes": None, "samples": 0, "source": "incidents-need-resolved-at"}

    return {
        "mttr_minutes": round(sum(durations) / len(durations), 1),
        "samples": len(durations),
        "source": "engineering-incidents",
    }


# --- Classification ---------------------------------------------------------

def classify(perf: dict) -> str:
    """Classify team as elite/high/medium/low based on the 4 metrics."""
    df_per_week = perf.get("deploy_frequency", {}).get("deploys_per_week", 0)
    lt_hours = perf.get("lead_time", {}).get("lead_time_hours_avg")
    cfr_pct = perf.get("change_failure_rate", {}).get("cfr_pct")
    mttr_min = perf.get("mttr", {}).get("mttr_minutes")

    # Map DF (deploys/week) to hours-between-deploys
    df_hours_between = (7 * 24) / df_per_week if df_per_week > 0 else float("inf")

    for tier, t in DORA_THRESHOLDS.items():
        if df_hours_between > t["df_max_hours"]:
            continue
        if lt_hours is not None and lt_hours > t["lt_max_hours"]:
            continue
        if cfr_pct is not None and cfr_pct > t["cfr_max_pct"]:
            continue
        if mttr_min is not None and mttr_min > t["mttr_max_minutes"]:
            continue
        return tier
    return "low"


# --- Main -------------------------------------------------------------------

def compute(window_days: int = DEFAULT_WINDOW_DAYS) -> dict:
    deploy = git_deploy_metrics(AGENTS_REPO, window_days)
    cron = cron_error_metrics(window_days)
    mttr = mttr_minutes(window_days)

    # CFR: incidents / deploys (guard zero)
    deploy_count = deploy["deploy_count"]
    incidents = cron["incidents_in_window"]
    if deploy_count == 0:
        cfr_pct = None
        cfr_source = "no-deploys"
    elif incidents == 0:
        cfr_pct = 0.0
        cfr_source = "zero-incidents"
    else:
        cfr_pct = round((incidents / deploy_count) * 100.0, 2)
        cfr_source = "computed"

    perf = {
        "deploy_frequency": deploy,
        "lead_time": deploy,  # derived from same git data
        "change_failure_rate": {
            "cfr_pct": cfr_pct,
            "incidents_in_window": incidents,
            "deploy_count": deploy_count,
            "source": cfr_source,
            "details": cron.get("details", []),
        },
        "mttr": mttr,
    }

    classification = classify(perf)

    # Top-level summary
    df_pw = deploy["deploys_per_week"]
    if df_pw >= 7:
        df_label = "on-demand"
    elif df_pw >= 1:
        df_label = "daily-weekly"
    elif df_pw >= 0.25:
        df_label = "weekly-monthly"
    else:
        df_label = "<monthly"

    return {
        "version": "1.0.0",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "window_days": window_days,
        "performance": perf,
        "classification": classification,
        "summary": {
            "deploys_per_week": df_pw,
            "deploy_frequency_label": df_label,
            "lead_time_hours_avg": deploy.get("lead_time_hours_avg"),
            "change_failure_rate_pct": cfr_pct,
            "mttr_minutes": mttr.get("mttr_minutes"),
        },
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "DORA aggregator")
    p.add_argument("--print", action="store_true", help="Print JSON to stdout, don't write")
    p.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    args = p.parse_args(argv)

    payload = compute(window_days=args.window_days)

    if args.print:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    atomic_write_json(STATE_FILE_AGENT, payload)
    try:
        atomic_write_json(STATE_FILE_LIVE, payload)
    except OSError as exc:
        print(f"WARN: live mirror write failed: {exc}", file=sys.stderr)

    s = payload["summary"]
    print(
        f"DORA [{payload['classification'].upper()}]: "
        f"DF={s['deploys_per_week']}/wk ({s['deploy_frequency_label']}) | "
        f"LT={s['lead_time_hours_avg']}h | "
        f"CFR={s['change_failure_rate_pct']}% | "
        f"MTTR={s['mttr_minutes']}m"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())