#!/usr/bin/env python3
"""conversion-dashboard.py - Show conversion pipeline status."""
import json
from pathlib import Path
from datetime import datetime, timezone

# --- AIW_ROOT path bootstrap (DEMIURGE-098) ---
import sys as _sys_bootstrap_098
from pathlib import Path as _Path_bootstrap_098
_PY_PATHS_ROOT = _Path_bootstrap_098(__file__).resolve().parent.parent
if str(_PY_PATHS_ROOT) not in _sys_bootstrap_098.path:
    _sys_bootstrap_098.path.insert(0, str(_PY_PATHS_ROOT))
from _paths import AIW_ROOT, STATE
# --- end bootstrap ---


STATE_DIR = STATE
CUSTOMERS_FILE = STATE_DIR / "customers.json"
COACHING_FILE = STATE_DIR / "coaching-customers.json"
CONVERSION_LOG = STATE_DIR / "conversion-attempts.json"


def main():
    customers = json.loads(CUSTOMERS_FILE.read_text())
    coaching = json.loads(COACHING_FILE.read_text())
    conversion = json.loads(CONVERSION_LOG.read_text())
    
    out = []
    out.append("# Conversion Dashboard")
    out.append(f"_Generated: {datetime.now(timezone.utc).isoformat()}_")
    out.append("")
    
    # Funnel
    out.append("## Conversion Funnel")
    out.append("")
    out.append("| Stage | Count | % |")
    out.append("|--------|-------|---|")
    
    total = len(customers["customers"])
    onboarded = sum(1 for c in customers["customers"] if c.get("onboarded"))
    m_l = sum(1 for c in customers["customers"] if c.get("tier") in ("M", "L"))
    converted = sum(1 for a in conversion["attempts"] if a.get("status") == "APPROVED")
    
    out.append(f"| Webhook received | {total} | 100% |")
    out.append(f"| Onboarded (Day 1 consent sent) | {onboarded} | {onboarded/max(total,1)*100:.0f}% |")
    out.append(f"| Day 3/7/10/30 completed | 0 | 0% |")
    out.append(f"| Conversion approved | {converted} | {converted/max(total,1)*100:.0f}% |")
    out.append(f"| M-tier or L-tier | {m_l} | {m_l/max(total,1)*100:.0f}% |")
    out.append("")
    
    # MRR
    mrr = 0
    pricing = {"S": 150, "M": 500, "L": 1500}
    for c in customers["customers"]:
        tier = c.get("tier", "S")
        # Apply region adjustment
        region = "PY"
        if region == "PY":
            price = pricing.get(tier, 0) * 0.6
        else:
            price = pricing.get(tier, 0)
        mrr += price
    out.append(f"## MRR (Monthly Recurring Revenue)")
    out.append("")
    out.append(f"- **Current MRR**: ${mrr:.2f}")
    out.append(f"- **ARR (annualized)**: ${mrr * 12:.2f}")
    out.append("")
    
    # Conversion attempts
    out.append("## Conversion Attempts")
    out.append("")
    out.append(f"Total attempts: {len(conversion['attempts'])}")
    out.append("")
    if conversion["attempts"]:
        out.append("| Customer | Tier | Score | Verdict | Status |")
        out.append("|----------|------|-------|---------|--------|")
        for a in conversion["attempts"][-10:]:
            out.append(f"| {a.get('name', '?')} | {a.get('tier', '?')} | {a.get('score', 0)} | {a.get('verdict', '?')} | {a.get('status', '?')} |")
    
    print("\n".join(out))


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Conversion pipeline scripts.""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    main()
