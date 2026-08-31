#!/usr/bin/env python3
"""eval-trending.py — Track eval-gate scores over time.

Reads /opt/data/db/eval-gate.db, computes:
- Daily pass rate (last 30 days)
- Per-agent pass rate trend
- Alert if pass rate drops below threshold

Writes to /opt/data/state/eval-trending.json
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import defaultdict

STATE_DIR = Path("/opt/data/state")
DB_PATH = Path("/opt/data/db/eval-gate.db")
OUTPUT_FILE = STATE_DIR / "eval-trending.json"

PASS_THRESHOLD = 80.0  # Alert if pass rate drops below 80%


def main():
    if not DB_PATH.exists():
        print(f"ERROR: {DB_PATH} not found")
        return
    
    con = sqlite3.connect(str(DB_PATH))
    c = con.cursor()
    
    # Get all runs from last 30 days
    cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    c.execute("""
        SELECT id, ts, total, pass_count, fail_count 
        FROM runs 
        WHERE ts > ?
        ORDER BY ts ASC
    """, (cutoff,))
    rows = c.fetchall()
    
    if not rows:
        print("No runs in last 30 days")
        con.close()
        return
    
    # Daily aggregates
    daily = defaultdict(lambda: {"runs": 0, "total_briefs": 0, "pass": 0, "fail": 0})
    for run_id, ts, total, pass_count, fail_count in rows:
        date = ts[:10]  # YYYY-MM-DD
        daily[date]["runs"] += 1
        daily[date]["total_briefs"] += total
        daily[date]["pass"] += pass_count
        daily[date]["fail"] += fail_count
    
    # Compute pass rates
    trend = []
    for date in sorted(daily.keys()):
        d = daily[date]
        rate = (d["pass"] / d["total_briefs"] * 100) if d["total_briefs"] else 0
        trend.append({
            "date": date,
            "runs": d["runs"],
            "total_briefs": d["total_briefs"],
            "pass": d["pass"],
            "fail": d["fail"],
            "pass_rate_pct": round(rate, 1),
        })
    
    # Aggregate stats
    total_briefs = sum(d["total_briefs"] for d in daily.values())
    total_pass = sum(d["pass"] for d in daily.values())
    total_fail = sum(d["fail"] for d in daily.values())
    avg_rate = (total_pass / total_briefs * 100) if total_briefs else 0
    
    # Find days with low pass rate
    low_days = [d for d in trend if d["pass_rate_pct"] < PASS_THRESHOLD and d["total_briefs"] > 0]
    
    output = {
        "version": "1.0.0",
        "schema": "eval-trending-v1",
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "window_days": 30,
        "pass_threshold_pct": PASS_THRESHOLD,
        "summary": {
            "total_briefs": total_briefs,
            "total_pass": total_pass,
            "total_fail": total_fail,
            "avg_pass_rate_pct": round(avg_rate, 1),
            "days_tracked": len(trend),
            "low_perf_days": len(low_days),
        },
        "daily_trend": trend,
        "alerts": [
            {
                "date": d["date"],
                "pass_rate_pct": d["pass_rate_pct"],
                "fail_count": d["fail"],
            }
            for d in low_days
        ],
    }
    
    OUTPUT_FILE.write_text(json.dumps(output, indent=2))
    con.close()
    
    print(f"✓ Tracked {len(trend)} days")
    print(f"  Avg pass rate: {avg_rate:.1f}%")
    print(f"  Low-perf days: {len(low_days)}")
    if low_days:
        print(f"  Alerts: {low_days[:5]}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

