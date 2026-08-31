#!/usr/bin/env python3
"""cost-alerts.py — WhatsApp alerts when cost exceeds thresholds.

Thresholds:
- daily > $50/day: ALERT (Ivan)
- monthly > $1000/mo: ALERT
- monthly > $5000/mo: URGENT
- monthly > $10000/mo: CRITICAL

Run via cron: aiw-cost-alerts (every 6 hours)
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path("/opt/data/state")
COST_FILE = STATE_DIR / "cost-tracker.json"
WHATSAPP_HELPER = "/opt/data/scripts/whatsapp-send.py"


def main():
    if not COST_FILE.exists():
        return
    
    cost = json.loads(COST_FILE.read_text())
    daily = cost.get("total_daily_usd", 0)
    monthly = cost.get("total_monthly_usd", 0)
    
    alerts = []
    
    if monthly > 10000:
        alerts.append(("CRITICAL", f"Monthly cost ${monthly:.2f} exceeds $10K! Top up LLM or disable agents now."))
    elif monthly > 5000:
        alerts.append(("URGENT", f"Monthly cost ${monthly:.2f} exceeds $5K threshold."))
    elif monthly > 1000:
        alerts.append(("WARN", f"Monthly cost ${monthly:.2f} exceeds $1K threshold."))
    
    if daily > 50:
        alerts.append(("DAILY", f"Daily cost ${daily:.2f} exceeds $50/day."))
    
    if not alerts:
        print(f"OK - monthly ${monthly:.2f}, daily ${daily:.2f}")
        return
    
    # Send WhatsApp
    for level, msg in alerts:
        full_msg = f"[COST-ALERT {level}] {msg} Top agents: "
        top3 = ", ".join(f"{a['agent']} (${a['monthly_cost_usd']:.2f})" for a in cost.get("top_10_monthly", [])[:3])
        full_msg += top3
        
        r = subprocess.run(
            ["python3", WHATSAPP_HELPER, "ivan", full_msg, "--sender", "cost-monitor"],
            capture_output=True, text=True, timeout=30
        )
        try:
            result = json.loads(r.stdout)
            status = result.get("status")
        except:
            status = "error"
        
        print(f"[{level}] WhatsApp sent: {status}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

