#!/usr/bin/env python3
"""self-running-check-v2.py - Self-running check using org-state.json.

Replaces the old filesystem-based version.
Reads from /opt/data/state/org-state.json instead of scanning files.
"""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

STATE_DIR = Path("/opt/data/state")


def main():
    org_state_file = STATE_DIR / "org-state.json"
    if not org_state_file.exists():
        print("ERROR: org-state.json not found. Run build-org-state.py first.")
        return
    
    org = json.loads(org_state_file.read_text())
    
    print("=" * 60)
    print(f"Self-running check @ {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)
    print()
    
    # Condition 1: All 7 lead agents delivered in last 7 days
    cutoff = datetime.now(timezone.utc).date() - timedelta(days=7)
    print(f"Condition 1 - All 7 lead agents delivered in last 7 days:")
    
    critical_agents = [
        "business-analyst", "management-coordinator", "kiki-coach",
        "finance-controller", "sales-pipeline", "engineering-roster",
        "research-tracker",
    ]
    
    all_delivered = True
    for agent in critical_agents:
        agent_data = org.get("agents", {}).get(agent, {})
        latest = agent_data.get("latest_brief")
        if latest:
            try:
                date = datetime.strptime(latest["date"], "%Y-%m-%d").date()
                if date >= cutoff:
                    print(f"  [OK] {agent}: latest={latest['date']}")
                    continue
            except (ValueError, TypeError):
                pass
        print(f"  [FAIL] {agent}: no recent brief")
        all_delivered = False
    
    # Condition 2: 0 cron jobs in error state
    print()
    cron = org.get("cron", {})
    file_jobs = cron.get("total_jobs", 0)
    live_jobs = cron.get("live_active", 0)
    drift = file_jobs - live_jobs
    
    no_errors = drift == 0
    print(f"Condition 2 - 0 cron jobs in error state:")
    print(f"  File: {file_jobs}, Live: {live_jobs}, Drift: {drift}")
    if no_errors:
        print("  [OK] No errors")
    else:
        print(f"  [FAIL] {drift} jobs in file but not live")
    
    # Condition 3: Manual check (we can't read WhatsApp history)
    print()
    print(f"Condition 3 - 0 'is X live?' messages from Ivan: (manual check)")
    
    # Overall
    self_running = all_delivered and no_errors
    
    # Check eval-gate pass rate
    print()
    eval_gate = org.get("eval_gate", {})
    pass_rate = eval_gate.get("pass_rate_pct", 0)
    print(f"Condition 4 - Eval-gate pass rate: {pass_rate}%")
    if pass_rate >= 80:
        print("  [OK] Pass rate >= 80%")
    else:
        print(f"  [WARN] Pass rate below 80%")
    
    # Check cost
    cost = json.loads((STATE_DIR / "cost-tracker.json").read_text())
    monthly = cost.get("total_monthly_usd", 0)
    print()
    print(f"Condition 5 - LLM cost under $1000/month:")
    print(f"  Monthly: ${monthly:.2f}")
    if monthly < 1000:
        print("  [OK]")
    else:
        print("  [WARN]")
    
    # Customers
    print()
    metrics = org.get("metrics", {})
    print(f"Condition 6 - Customer pipeline:")
    print(f"  Total customers: {metrics.get('customers_total', 0)}")
    print(f"  Onboarded: {metrics.get('customers_onboarded', 0)}")
    print(f"  Coaching pipeline: {metrics.get('coaching_pipeline', 0)}")
    
    print()
    print(f"OVERALL: {'[OK] SELF-RUNNING' if self_running and pass_rate >= 80 else '[FAIL] NOT YET'}")
    return 0 if self_running and pass_rate >= 80 else 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""Script description not available""")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

