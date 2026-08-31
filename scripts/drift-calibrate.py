#!/usr/bin/env python3
"""Drift detection threshold calibration.

Reads alerts from state/drift-alerts.json (or per-monitor notes), counts how
often each threshold fired over a window, and outputs a calibration report
suggesting tighter/looser thresholds.

Built as Phase 26 #4 (drift detection calibration scaffolding).

Usage:
    python3 scripts/drift-calibrate.py [--days 30] [--output state/drift-calibration.json]

Output schema (state/drift-calibration.json):
    {
      "computed_at": "<ISO>",
      "window_days": <int>,
      "alerts_analyzed": <int>,
      "calibrations": [
        {
          "monitor": "<name>",
          "category": "D1|D2|D3|D4|D5",
          "fires_in_window": <int>,
          "current_threshold": "<string>",
          "recommendation": "tighten|loosen|keep",
          "suggested_threshold": "<string>"
        }
      ],
      "summary": {
        "monitors_needing_calibration": <int>,
        "monitors_keeping_current": <int>,
        "monitors_with_zero_fires": <int>
      }
    }
"""
import argparse
import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

DEFAULT_ALERTS = Path("/opt/data/state/drift-alerts.json")
DEFAULT_OUTPUT = Path("/opt/data/state/drift-calibration.json")

# Default thresholds from engineering/drift-detection-methodology.md
DEFAULT_THRESHOLDS = {
    "D1": {"MEDIUM": 2.0, "HIGH": 3.0, "CRITICAL": 5.0},
    "D2": {"MEDIUM": 0.30, "HIGH": 0.50, "CRITICAL": 1.00},
    "D3": {"MEDIUM": None, "HIGH": None, "CRITICAL": "any_new_field"},
    "D4": {"MEDIUM": 0.50, "HIGH": 1.00, "CRITICAL": 2.00},
    "D5": {"MEDIUM": 0.30, "HIGH": 0.10, "CRITICAL": None},
}


def load_alerts(path: Path) -> list[dict]:
    """Load alerts from a JSON file. Returns empty list if file missing."""
    if not path.exists():
        return []
    try:
        with path.open() as f:
            data = json.load(f)
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "alerts" in data:
            return data["alerts"]
        return []
    except (json.JSONDecodeError, OSError):
        return []


def calibrate(alerts: list[dict], window_days: int) -> dict:
    """Apply threshold calibration rules to a window of alerts."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=window_days)
    recent = []
    for a in alerts:
        ts = a.get("timestamp") or a.get("ts") or a.get("fired_at")
        if not ts:
            continue
        try:
            when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            continue
        if when >= cutoff:
            recent.append(a)

    # Group by (monitor, category)
    grouped: dict[tuple[str, str], int] = {}
    for a in recent:
        monitor = a.get("monitor", "unknown")
        category = a.get("category", "D1")
        grouped[(monitor, category)] = grouped.get((monitor, category), 0) + 1

    calibrations = []
    for (monitor, category), fires in grouped.items():
        thresholds = DEFAULT_THRESHOLDS.get(category, {})
        # Rule: 0 fires -> loosen (threshold too tight, no signal)
        #       >20 fires in window -> tighten (threshold too loose, noisy)
        #       1-20 fires -> keep
        if fires == 0:
            recommendation = "loosen"
        elif fires > 20:
            recommendation = "tighten"
        else:
            recommendation = "keep"

        suggested = suggest_threshold(category, thresholds, recommendation)
        calibrations.append({
            "monitor": monitor,
            "category": category,
            "fires_in_window": fires,
            "current_threshold": format_thresholds(category, thresholds),
            "recommendation": recommendation,
            "suggested_threshold": suggested,
        })

    # Summary
    counts = {"tighten": 0, "loosen": 0, "keep": 0}
    for c in calibrations:
        counts[c["recommendation"]] += 1

    return {
        "computed_at": datetime.now(timezone.utc).isoformat(),
        "window_days": window_days,
        "alerts_analyzed": len(recent),
        "calibrations": calibrations,
        "summary": {
            "monitors_needing_calibration": counts["tighten"] + counts["loosen"],
            "monitors_keeping_current": counts["keep"],
            "monitors_with_zero_fires": counts["loosen"],
        },
    }


def suggest_threshold(category: str, current: dict, rec: str) -> str:
    """Suggest new threshold per category and recommendation."""
    if rec == "keep":
        return format_thresholds(category, current)
    if category == "D1":
        # z-score: tighten=raise, loosen=lower
        delta = 0.5 if rec == "tighten" else -0.5
        return f"MEDIUM: z>{current['MEDIUM']+delta}, HIGH: z>{current['HIGH']+delta}, CRITICAL: z>{current['CRITICAL']+delta}"
    if category == "D2":
        delta = 0.10 if rec == "tighten" else -0.10
        return f"MEDIUM: ±{current['MEDIUM']+delta:.0%}, HIGH: ±{current['HIGH']+delta:.0%}, CRITICAL: ±{current['CRITICAL']+delta:.0%}"
    if category == "D3":
        return "any_new_field (no change)"
    if category == "D4":
        delta = 0.20 if rec == "tighten" else -0.20
        return f"MEDIUM: +{current['MEDIUM']+delta:.0%} delay, HIGH: +{current['HIGH']+delta:.0%}, CRITICAL: +{current['CRITICAL']+delta:.0%}"
    if category == "D5":
        delta = 0.10 if rec == "tighten" else -0.10
        return f"MEDIUM: |r|<{current['MEDIUM']-delta:.2f}, HIGH: |r|<{current['HIGH']-delta:.2f}"
    return "no suggestion"


def format_thresholds(category: str, current: dict) -> str:
    parts = []
    for tier in ["MEDIUM", "HIGH", "CRITICAL"]:
        v = current.get(tier)
        if v is None:
            continue
        if isinstance(v, float):
            parts.append(f"{tier}: {v:.2f}")
        else:
            parts.append(f"{tier}: {v}")
    return ", ".join(parts) if parts else "no threshold"


def main():
    parser = argparse.ArgumentParser(description="Drift threshold calibration")
    parser.add_argument("--alerts", type=Path, default=DEFAULT_ALERTS,
                        help="Path to drift alerts JSON")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT,
                        help="Path to write calibration report")
    parser.add_argument("--days", type=int, default=30,
                        help="Window in days (default 30)")
    args = parser.parse_args()

    alerts = load_alerts(args.alerts)
    report = calibrate(alerts, args.days)

    with args.output.open("w") as f:
        json.dump(report, f, indent=2)

    # Stdout summary
    s = report["summary"]
    print(f"=== Drift Threshold Calibration ===")
    print(f"Computed at: {report['computed_at']}")
    print(f"Window: {args.days}d, alerts analyzed: {report['alerts_analyzed']}")
    print(f"Monitors needing calibration: {s['monitors_needing_calibration']}")
    print(f"Monitors keeping current: {s['monitors_keeping_current']}")
    print(f"Monitors with zero fires (loosen): {s['monitors_with_zero_fires']}")
    print(f"Written: {args.output}")

    if report["calibrations"]:
        print("\nTop recommendations:")
        for c in report["calibrations"][:5]:
            print(f"  [{c['recommendation']:7s}] {c['monitor']} ({c['category']}): {c['fires_in_window']} fires")
            print(f"           current: {c['current_threshold']}")
            print(f"           suggested: {c['suggested_threshold']}")


if __name__ == "__main__":
    main()
