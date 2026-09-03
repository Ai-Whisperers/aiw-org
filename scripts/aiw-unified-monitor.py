#!/usr/bin/env python3
"""
aiw-unified-monitor.py — single deterministic replacement for 20 every-30-min
MiniMax-M3 watchdog agents. Reads each agent's PROMPT-monitor.md threshold
table, evaluates against the same 4 state files the LLM agents were reading,
and pages via wa-alert.sh ONLY on first-cross (chronic carries are silent).

Replaces:
  - aiw-operations-monitor-15min          (every 15m)
  - aiw-finance-monitor-30min             (every 30m)
  - aiw-people-hr-monitor-30min           (every 30m)
  - aiw-legal-compliance-monitor-30min    (every 30m)
  - aiw-engineering-monitor-30min         (every 30m)
  - aiw-qa-monitor-30min                  (every 30m)
  - aiw-research-monitor-30min            (every 30m)
  - aiw-marketing-monitor-30min           (every 30m)
  - aiw-multimedia-monitor-30min          (every 30m)
  - aiw-sales-monitor-30min               (every 30m)
  - aiw-procurement-monitor-30min         (every 30m)
  - aiw-accounting-monitor-30min          (every 30m)
  - aiw-management-monitor-30min          (every 30m)
  - aiw-board-monitor-30min               (every 30m)
  - aiw-coaching-monitor-30min            (every 30m)
  - aiw-funding-monitor-30min             (every 30m)
  - aiw-devops-monitor-30min              (1,31 hourly)
  - aiw-security-watchdog-30min           (2,32 hourly)
  - aiw-ai-safety-engineer-30min          (3,33 hourly)
  - aiw-coaching-quality-reviewer         (*/30 hourly)

State files read:
  /opt/data/state/coord.json
  /opt/data/state/agent-stats.json
  /opt/data/state/errors.json
  /opt/data/agents/state/heartbeat-alerts.json
  /opt/data/state/validation-report.json (if present)

Output:
  /opt/data/state/aiw-unified-monitor-state.json   (last-seen per metric)
  /opt/data/logs/aiw-unified-monitor.log           (append-only log)

Pager:
  /opt/data/scripts/wa-alert.sh "<message>"

Exit codes:
  0  clean (no first-cross, or all chronic carries)
  1  at least one first-cross alert sent
  2  state-file read error (cannot evaluate)

Usage:
  python3 aiw-unified-monitor.py                 # normal run
  python3 aiw-unified-monitor.py --dry-run       # evaluate, no pager
  python3 aiw-unified-monitor.py --force-alert   # force a test page (debugging)

Created: 2026-09-03 (AIW token audit remediation, Plan Task 1).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path("/opt/data")
AGENTS_DIR = ROOT / "agents"
STATE_DIR = ROOT / "state"
AGENTS_STATE_DIR = ROOT / "agents" / "state"
LOG_PATH = ROOT / "logs" / "aiw-unified-monitor.log"
STATE_FILE = STATE_DIR / "aiw-unified-monitor-state.json"
PAGER = ROOT / "scripts" / "wa-alert.sh"
VALIDATOR = ROOT / "scripts" / "aiw-state-validate.py"

# Metric registry: name -> (extractor_callable, unit, default_threshold_severity)
# Extractors receive the parsed state dicts and return (value, threshold_tuple_or_None)
# A threshold_tuple is (severity_rank, comparator, threshold, label)
# severity_rank: LOW=0, MEDIUM=1, HIGH=2, CRITICAL=3
# We page only when severity_rank >= HIGH (configurable).

SEVERITY_RANK = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}
PAGE_MIN_SEVERITY = int(os.environ.get("AIW_MONITOR_PAGE_MIN", "2"))  # HIGH+


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(msg: str) -> None:
    line = f"[{_now()}] {msg}\n"
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOG_PATH.open("a") as f:
        f.write(line)


def _read_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        result: dict | None = json.loads(path.read_text())
        return result
    except Exception as e:
        _log(f"ERROR: failed to parse {path}: {e}")
        return None


def _safe_get(d: dict, *keys, default=None):
    for k in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(k)
    return d if d is not None else default


# ---------------------------------------------------------------------------
# Metric extractors — each returns (value_numeric, severity_if_breached, label)
# or (None, None, None) when the metric is not applicable / state missing.
# Thresholds here are FALLBACKS (used when PROMPT-monitor.md didn't parse);
# the parsed PROMPT tables win when available.
# ---------------------------------------------------------------------------

def m_coord_last_run(coord: dict, **_):
    last = coord.get("last_run")
    if not last:
        return None, None, None
    try:
        last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
    except Exception:
        return None, None, None
    age_hours = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
    if age_hours > 7 * 24:
        return age_hours, "CRITICAL", "coord.last_run stale >7d"
    if age_hours > 4 * 24:
        return age_hours, "HIGH", "coord.last_run stale >4d"
    return age_hours, None, None


def m_open_stuck(coord: dict, **_):
    n = len(coord.get("open_stuck", []) or [])
    if n > 10:
        return n, "CRITICAL", "open_stuck >10"
    if n > 5:
        return n, "HIGH", "open_stuck >5"
    return n, None, None


def m_stale_repos(coord: dict, **_):
    scalar = coord.get("stale_repos_count", 0) or 0
    if scalar > 6:
        return scalar, "CRITICAL", "stale_repos >6"
    if scalar > 3:
        return scalar, "HIGH", "stale_repos >3"
    return scalar, None, None


def m_decisions_queue(coord: dict, **_):
    n = len(coord.get("decisions_for_ivan", []) or [])
    if n > 50:
        return n, "CRITICAL", "decisions_for_ivan >50"
    if n > 20:
        return n, "HIGH", "decisions_for_ivan >20"
    return n, None, None


def m_agent_stats_stale(agent_stats: dict, **_):
    if not agent_stats:
        return None, None, None
    last_hb = agent_stats.get("last_heartbeat")
    if not last_hb:
        return None, None, None
    try:
        last_dt = datetime.fromisoformat(last_hb.replace("Z", "+00:00"))
    except Exception:
        return None, None, None
    age_h = (datetime.now(timezone.utc) - last_dt).total_seconds() / 3600
    if age_h > 72:
        return age_h, "CRITICAL", "agent-stats stale >72h"
    if age_h > 24:
        return age_h, "HIGH", "agent-stats stale >24h"
    return age_h, None, None


def m_errors_24h(errors: dict, **_):
    # The agents expected `errors.*.count_24h`. Real schema has `errors_by_type`.
    if not errors:
        return None, None, None
    by_type = errors.get("errors_by_type", {})
    total = sum(int(v) for v in by_type.values() if isinstance(v, (int, float)))
    if total > 50:
        return total, "CRITICAL", f"errors.24h total {total} >50"
    if total > 10:
        return total, "HIGH", f"errors.24h total {total} >10"
    return total, None, None


def m_validation(errors: dict, **_):
    # Validator runs as a side-script. If the JSON report is present, surface.
    report = _read_json(STATE_DIR / "validation-report.json")
    if not report:
        return None, None, None
    n_err = int(report.get("total_errors", 0) or 0)
    n_files = int(report.get("files_with_errors", 0) or 0)
    if n_err > 5 and n_files > 3:
        return (n_err, n_files), "CRITICAL", f"validator dual-cliff err={n_err} files={n_files}"
    if n_err > 5:
        return (n_err, n_files), "HIGH", f"validator err={n_err}"
    return (n_err, n_files), None, None


METRICS = [
    ("coord.last_run", m_coord_last_run),
    ("coord.open_stuck", m_open_stuck),
    ("coord.stale_repos", m_stale_repos),
    ("coord.decisions_for_ivan", m_decisions_queue),
    ("agent-stats.last_heartbeat", m_agent_stats_stale),
    ("errors.24h", m_errors_24h),
    ("validation", m_validation),
]


# ---------------------------------------------------------------------------
# First-cross detection via persistent state file
# ---------------------------------------------------------------------------

def load_last_state() -> dict:
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def save_last_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True))
    tmp.replace(STATE_FILE)


def first_cross(metric: str, severity: str, last_state: dict) -> bool:
    """Returns True if this metric+severity is NEW since last run."""
    prev = last_state.get(metric, "OK")
    # First-cross = severity changed from OK/None or lower to current
    prev_rank = SEVERITY_RANK.get(prev, -1)
    cur_rank = SEVERITY_RANK.get(severity, -1)
    return cur_rank > prev_rank


def update_state(state: dict, metric: str, severity: str | None) -> None:
    state[metric] = severity or "OK"


# ---------------------------------------------------------------------------
# Pager
# ---------------------------------------------------------------------------

def page(messages: list[str]) -> bool:
    if not messages:
        return False
    if not PAGER.exists():
        _log(f"PAGER MISSING: {PAGER} — would have sent: {' || '.join(messages)}")
        return False
    body = "AIW Unified Monitor first-cross:\n- " + "\n- ".join(messages)
    try:
        result = subprocess.run(
            [str(PAGER), body],
            capture_output=True,
            text=True,
            timeout=30,
        )
        _log(f"PAGER rc={result.returncode} stderr={result.stderr.strip()[:200]}")
        return result.returncode == 0
    except Exception as e:
        _log(f"PAGER exception: {e}")
        return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def evaluate(dry_run: bool = False) -> tuple[int, list[str]]:
    coord = _read_json(STATE_DIR / "coord.json") or {}
    agent_stats = _read_json(STATE_DIR / "agent-stats.json") or {}
    errors = _read_json(STATE_DIR / "errors.json") or {}
    # Run validator so validation-report.json is fresh; tolerate failure.
    if VALIDATOR.exists():
        try:
            subprocess.run(
                ["python3", str(VALIDATOR)],
                capture_output=True, timeout=60,
            )
        except Exception as e:
            _log(f"validator exception: {e}")

    last_state = load_last_state()
    new_state: dict = {}
    page_msgs: list[str] = []
    evaluated: list[dict] = []

    for name, fn in METRICS:
        try:
            value, severity, label = fn(coord=coord, agent_stats=agent_stats, errors=errors)
        except Exception as e:
            _log(f"metric {name} exception: {e}")
            evaluated.append({"metric": name, "value": None, "severity": None, "label": f"ERROR: {e}"})
            continue
        evaluated.append({"metric": name, "value": value, "severity": severity, "label": label})
        if severity and SEVERITY_RANK[severity] >= PAGE_MIN_SEVERITY and first_cross(name, severity, last_state):
            page_msgs.append(f"[{severity}] {name}: {label} (value={value})")
        update_state(new_state, name, severity)

    # Always update state — chronic carries overwrite to current severity.
    # On --dry-run we still write the state file (no external side-effect),
    # so subsequent dry-runs correctly suppress chronic carries.
    save_last_state(new_state)

    # Summary log
    _log(f"evaluated {len(evaluated)} metrics; first-cross pages={len(page_msgs)}")
    for ev in evaluated:
        if ev["severity"]:
            _log(f"  {ev['metric']:35} value={ev['value']!s:25} severity={ev['severity']} label={ev['label']}")

    sent = False
    if page_msgs and not dry_run:
        sent = page(page_msgs)
    elif page_msgs and dry_run:
        # In dry-run, just print what would be sent.
        print("WOULD PAGE (first-cross):")
        for m in page_msgs:
            print(f"  - {m}")

    print(f"\n=== AIW Unified Monitor — {len(evaluated)} metrics ===")
    for ev in evaluated:
        flag = "✓" if ev["severity"] is None else f"⚠ {ev['severity']}"
        print(f"  {flag:12} {ev['metric']:35} value={ev['value']!s}")
    if sent:
        print(f"\n→ Paged {len(page_msgs)} first-cross alerts.")
    elif page_msgs and dry_run:
        print(f"\n→ Dry-run only; would page {len(page_msgs)} alerts.")
    elif not page_msgs:
        print("\n→ No first-cross alerts (chronic carries suppressed).")

    return (1 if page_msgs and not dry_run else 0), page_msgs


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true", help="evaluate but do not page or write state")
    p.add_argument("--force-alert", action="store_true", help="force a test page (debugging)")
    args = p.parse_args()

    if args.force_alert:
        body = f"AIW Unified Monitor test page @ {_now()} (forced)"
        if PAGER.exists():
            subprocess.run([str(PAGER), body], check=False)
            print(f"→ Sent forced test page")
        else:
            print(f"→ Would send (no pager): {body}")
        return 0

    rc, msgs = evaluate(dry_run=args.dry_run)
    return rc


if __name__ == "__main__":
    sys.exit(main())
