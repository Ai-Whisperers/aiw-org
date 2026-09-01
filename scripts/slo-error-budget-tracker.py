#!/usr/bin/env python3
"""SLO / error-budget tracker.

Built Phase 7 R5 (implementation plan §4 Phase 1.3).

Per-service SLO tracking:
  - availability SLO (e.g. 99.9% over 28d window)
  - latency p95 SLO (ms)
  - error-budget consumption (% of budget used)
  - status: healthy / warning / exhausted / unknown

Reads:
  - /opt/data/logs/site-health.log  (HTTP availability checks per service)
  - /opt/data/logs/deploy-*.log     (deploy events)

Writes:
  - /opt/data/agents/state/slo-budget.json  (atomic write per P2 pattern)
  - /opt/data/state/slo-budget.json         (mirror)

SLO config (built-in defaults — extend via config file later):
  - 28-day rolling window
  - 99.9% availability target
  - 500ms p95 latency target
  - warning threshold: 50% budget consumed
  - exhausted threshold: 100% budget consumed

Usage:
    python3 scripts/slo-error-budget-tracker.py            # compute + write
    python3 scripts/slo-error-budget-tracker.py --print     # compute + print only
    python3 scripts/slo-error-budget-tracker.py --service nexa-paraguay  # one service
"""

import argparse
import json
import os
import re
import sys
import tempfile
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

# --- Configuration ----------------------------------------------------------

DEFAULT_WINDOW_DAYS = 28
DEFAULT_SLO_AVAILABILITY = 0.999  # 99.9%
DEFAULT_SLO_LATENCY_P95_MS = 500
WARNING_BUDGET_THRESHOLD_PCT = 50.0
EXHAUSTED_BUDGET_THRESHOLD_PCT = 100.0

# Services to monitor (extend via config file later)
# Per implementation plan Phase 1.5: top live client sites.
# Sources: /opt/data/work/research-repos/*/content/es/site.json (live domains)
DEFAULT_SERVICES = [
    {
        "name": "nexaparaguay.com.py",
        "host": "nexaparaguay.com.py",
        "category": "client_prod",
        "slo_availability": 0.999,
        "slo_latency_p95_ms": 500,
    },
    {
        "name": "ometzdental.com",
        "host": "ometzdental.com",
        "category": "client_prod",
        "slo_availability": 0.999,
        "slo_latency_p95_ms": 500,
    },
]

# Config file path (overrides DEFAULT_SERVICES if present)
SERVICES_CONFIG = Path("/opt/data/agents/state/slo-services.json")

# --- Paths ------------------------------------------------------------------

SITE_HEALTH_LOG = Path("/opt/data/logs/site-health.log")
DEPLOY_LOG_DIR = Path("/opt/data/logs")
STATE_FILE_AGENT = Path("/opt/data/agents/state/slo-budget.json")
STATE_FILE_LIVE = Path("/opt/data/state/slo-budget.json")


# --- Helpers ----------------------------------------------------------------

def parse_iso(ts: str) -> datetime:
    """Parse ISO timestamp, accept trailing Z."""
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts)


def atomic_write_json(path: Path, payload: dict) -> None:
    """P2 pattern: atomic write with .tmp + rename + .bak (best-effort)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    # backup existing
    if path.exists():
        try:
            bak = path.with_suffix(path.suffix + ".bak")
            path.replace(bak)
        except OSError:
            pass
    # write tmp + rename
    fd, tmp_path = tempfile.mkstemp(prefix=".slo-", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp_path, path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


# --- Log parsing ------------------------------------------------------------

# site-health.log lines look like:
#   2026-09-01T17:30:00Z  GET https://nexaparaguay.com.py/  200  142ms  ok
SITE_HEALTH_LINE_RE = re.compile(
    r"^(?P<ts>\S+)\s+(?P<method>\S+)\s+(?P<url>\S+)\s+(?P<status>\d{3})\s+(?P<latency_ms>\d+)ms\s+(?P<verdict>\S+)"
)


def load_site_health_samples(
    services: list, window_days: int
) -> dict:
    """Return {service_name: {"samples": int, "ok": int, "latencies": [ms, ...]}}.

    Parses /opt/data/logs/site-health.log within window. Missing log file
    means no data (returns empty samples).
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    out = {
        s["name"]: {"samples": 0, "ok": 0, "latencies": [], "host": s["host"]}
        for s in services
    }

    if not SITE_HEALTH_LOG.exists():
        return out

    with SITE_HEALTH_LOG.open("r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = SITE_HEALTH_LINE_RE.match(line.strip())
            if not m:
                continue
            try:
                ts = parse_iso(m.group("ts"))
            except ValueError:
                continue
            if ts < cutoff:
                continue
            url = m.group("url")
            for svc_name, bucket in out.items():
                if bucket["host"] in url:
                    bucket["samples"] += 1
                    if m.group("status").startswith("2"):
                        bucket["ok"] += 1
                    try:
                        bucket["latencies"].append(int(m.group("latency_ms")))
                    except ValueError:
                        pass
                    break

    return out


def compute_p95(latencies: list) -> int:
    """Naive p95 (95th percentile) — sort and pick index."""
    if not latencies:
        return 0
    s = sorted(latencies)
    idx = max(0, int(len(s) * 0.95) - 1)
    return s[idx]


def compute_service_slo(
    service: dict,
    samples: dict,
    window_days: int,
) -> dict:
    """Compute SLO + error-budget for one service."""
    name = service["name"]
    slo_avail = float(service.get("slo_availability", DEFAULT_SLO_AVAILABILITY))
    slo_p95 = int(service.get("slo_latency_p95_ms", DEFAULT_SLO_LATENCY_P95_MS))

    bucket = samples.get(name, {"samples": 0, "ok": 0, "latencies": []})
    n = bucket["samples"]
    ok = bucket["ok"]
    p95 = compute_p95(bucket["latencies"])

    if n == 0:
        return {
            "slo_availability": slo_avail,
            "slo_latency_p95_ms": slo_p95,
            "window_days": window_days,
            "samples": 0,
            "availability_pct": 0.0,
            "latency_p95_ms": None,
            "error_budget_used_pct": 0.0,
            "error_budget_remaining_pct": 100.0,
            "budget_status": "unknown",
            "last_check_at": datetime.now(timezone.utc).isoformat(),
        }

    avail_pct = ok / n
    # Error budget: fraction of (1 - SLO) used
    allowed_error = max(1e-9, 1.0 - slo_avail)
    consumed_error = max(0.0, slo_avail - avail_pct)
    budget_used_pct = min(100.0, (consumed_error / allowed_error) * 100.0)
    budget_remaining_pct = max(0.0, 100.0 - budget_used_pct)

    # Latency budget: if p95 > target, count as fully consumed (binary for now)
    latency_over = p95 > slo_p95 and n > 0
    if latency_over:
        # Weight latency into budget (50/50 with availability)
        budget_used_pct = min(100.0, budget_used_pct + 50.0)
        budget_remaining_pct = max(0.0, 100.0 - budget_used_pct)

    if budget_used_pct >= EXHAUSTED_BUDGET_THRESHOLD_PCT:
        status = "exhausted"
    elif budget_used_pct >= WARNING_BUDGET_THRESHOLD_PCT:
        status = "warning"
    else:
        status = "healthy"

    return {
        "slo_availability": slo_avail,
        "slo_latency_p95_ms": slo_p95,
        "window_days": window_days,
        "samples": n,
        "availability_pct": round(avail_pct, 4),
        "latency_p95_ms": p95,
        "error_budget_used_pct": round(budget_used_pct, 2),
        "error_budget_remaining_pct": round(budget_remaining_pct, 2),
        "budget_status": status,
        "last_check_at": datetime.now(timezone.utc).isoformat(),
    }


def aggregate(per_service: dict) -> dict:
    """Aggregate counts + alert level."""
    total = len(per_service)
    healthy = sum(1 for v in per_service.values() if v.get("budget_status") == "healthy")
    warning = sum(1 for v in per_service.values() if v.get("budget_status") == "warning")
    exhausted = sum(1 for v in per_service.values() if v.get("budget_status") == "exhausted")
    if exhausted > 0:
        alert = "CRITICAL"
    elif warning > 0:
        alert = "WARNING"
    else:
        alert = None
    return {
        "services_total": total,
        "services_healthy": healthy,
        "services_warning": warning,
        "services_exhausted": exhausted,
        "alert": alert,
    }


# --- Main -------------------------------------------------------------------

def compute(services=None, window_days=DEFAULT_WINDOW_DAYS) -> dict:
    if services is None:
        # Try config file first
        if SERVICES_CONFIG.exists():
            try:
                cfg = json.loads(SERVICES_CONFIG.read_text())
                if isinstance(cfg, list) and cfg:
                    services = cfg
                else:
                    services = DEFAULT_SERVICES
            except (json.JSONDecodeError, OSError):
                services = DEFAULT_SERVICES
        else:
            services = DEFAULT_SERVICES
    samples = load_site_health_samples(services, window_days)
    per_service = {s["name"]: compute_service_slo(s, samples, window_days) for s in services}
    return {
        "version": "1.0.0",
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "services": per_service,
        "aggregate": aggregate(per_service),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0] if __doc__ else "SLO tracker")
    p.add_argument("--print", action="store_true", help="Print JSON to stdout, don't write")
    p.add_argument("--service", help="Compute only one service (debug)")
    p.add_argument("--window-days", type=int, default=DEFAULT_WINDOW_DAYS)
    args = p.parse_args(argv)

    services = None  # let compute() load from config or fall back to DEFAULT_SERVICES
    if args.service:
        services = [s for s in DEFAULT_SERVICES if s["name"] == args.service]
        if not services:
            print(f"ERROR: unknown service {args.service!r}", file=sys.stderr)
            return 2

    payload = compute(services=services, window_days=args.window_days)

    if args.print:
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    # Atomic write to both locations
    atomic_write_json(STATE_FILE_AGENT, payload)
    try:
        atomic_write_json(STATE_FILE_LIVE, payload)
    except OSError as exc:
        print(f"WARN: live mirror write failed: {exc}", file=sys.stderr)

    # Stdout summary
    agg = payload["aggregate"]
    print(
        f"SLO tracker: {agg['services_total']} services | "
        f"healthy={agg['services_healthy']} warning={agg['services_warning']} "
        f"exhausted={agg['services_exhausted']} | alert={agg['alert']}"
    )
    for name, v in payload["services"].items():
        print(
            f"  {name}: avail={v['availability_pct']:.3%} "
            f"p95={v.get('latency_p95_ms', 'n/a')}ms "
            f"budget_used={v['error_budget_used_pct']:.1f}% "
            f"status={v['budget_status']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())