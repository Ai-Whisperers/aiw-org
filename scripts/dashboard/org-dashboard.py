#!/usr/bin/env python3
"""org-dashboard.py - Single-pane-of-glass view of the AIW org.

FounderOS-inspired 8-route dashboard.
"""
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime, timezone

STATE_DIR = Path("/opt/data/state")


def load_json(path, default=None):
    if default is None:
        default = {}
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except:
        return default


def route_pulse():
    org = load_json(STATE_DIR / "org-state.json")
    metrics = org.get("metrics", {})
    cron = org.get("cron", {})
    eval_gate = org.get("eval_gate", {})
    cost = load_json(STATE_DIR / "cost-tracker.json")
    
    out = "# Org Pulse\n\n"
    out += "Last updated: " + datetime.now(timezone.utc).isoformat() + "\n\n"
    out += "## Metrics\n\n"
    out += "- Agents: " + str(metrics.get('agents_total', 0)) + " total, " + str(metrics.get('agents_with_briefs', 0)) + " with briefs\n"
    out += "- Briefs: " + str(metrics.get('total_briefs', 0)) + " total\n"
    out += "- Customers: " + str(metrics.get('customers_total', 0)) + " (" + str(metrics.get('customers_onboarded', 0)) + " onboarded)\n"
    out += "- Coaching pipeline: " + str(metrics.get('coaching_pipeline', 0)) + "\n"
    out += "- Cron: " + str(cron.get('total_jobs', 0)) + " jobs (" + str(cron.get('live_active', 0)) + " active)\n"
    out += "- MRR: $" + str(metrics.get('mrr_usd', 0)) + "\n"
    out += "- Burn: $" + str(metrics.get('burn_usd_month', 0)) + "/mo\n"
    
    pass_count = eval_gate.get('all_pass', 0)
    briefs_evaluated = eval_gate.get('all_briefs_evaluated', eval_gate.get('all_runs', 0))
    pass_rate = eval_gate.get('pass_rate_pct', 0)
    out += "- Eval-gate: " + str(pass_count) + "/" + str(briefs_evaluated) + " briefs (" + str(pass_rate) + "% PASS)\n"
    
    daily = cost.get('total_daily_usd', 0)
    monthly = cost.get('total_monthly_usd', 0)
    out += "- LLM cost: $" + str(daily) + "/day ($" + str(monthly) + "/mo)\n"
    
    return out


def route_agents():
    org = load_json(STATE_DIR / "org-state.json")
    agents = org.get("agents", {})
    
    out = "# Agent Roster\n\n"
    out += "Total agents: " + str(len(agents)) + "\n\n"
    
    sorted_agents = sorted(
        agents.items(),
        key=lambda x: x[1].get("latest_brief", {}).get("modified", "") if x[1].get("latest_brief") else "",
        reverse=True
    )
    
    out += "| Agent | Briefs | Last Brief |\n"
    out += "|-------|--------|------------|\n"
    
    for name, info in sorted_agents:
        last_brief = info.get("latest_brief")
        last_str = last_brief.get("date", "-") if last_brief else "-"
        brief_count = info.get("brief_count", 0)
        out += "| " + name + " | " + str(brief_count) + " | " + last_str + " |\n"
    
    return out


def route_cron():
    org = load_json(STATE_DIR / "org-state.json")
    cron = org.get("cron", {})
    
    out = "# Cron Health\n\n"
    out += "- File jobs: " + str(cron.get('total_jobs', 0)) + "\n"
    out += "- Enabled: " + str(cron.get('enabled', 0)) + "\n"
    out += "- No-agent scripts: " + str(cron.get('no_agent_scripts', 0)) + "\n"
    out += "- Live active: " + str(cron.get('live_active', 0)) + "\n"
    out += "- Drift: " + str(cron.get('total_jobs', 0) - cron.get('live_active', 0)) + " jobs in file but not live\n"
    return out


def route_customers():
    customers = load_json(STATE_DIR / "customers.json", {"customers": []})
    coaching = load_json(STATE_DIR / "coaching-customers.json", {"customers": {}})
    
    out = "# Customers\n\n"
    out += "## Webhook customers: " + str(len(customers.get('customers', []))) + "\n\n"
    for c in customers.get("customers", []):
        onboarded = "onboarded" if c.get("onboarded") else "pending"
        out += "- " + c['customer_id'] + ": " + str(c.get('name')) + " (" + c['tier'] + ")\n"
    
    out += "\n## Coaching pipeline: " + str(len(coaching.get('customers', {}))) + "\n\n"
    for cid, c in coaching.get("customers", {}).items():
        step = c.get("onboarding_step", "-")
        out += "- " + cid + ": " + c['name'] + " (" + c['tier'] + ") - " + step + "\n"
    
    return out


def route_finances():
    cost = load_json(STATE_DIR / "cost-tracker.json")
    
    out = "# Finances\n\n"
    out += "- Daily cost: $" + str(cost.get('total_daily_usd', 0)) + "\n"
    out += "- Monthly cost: $" + str(cost.get('total_monthly_usd', 0)) + "\n\n"
    out += "## Top 10 monthly costs\n\n"
    out += "| Agent | Monthly | Runs/day |\n"
    out += "|-------|---------|----------|\n"
    
    for a in cost.get("top_10_monthly", [])[:10]:
        out += "| " + a['agent'] + " | $" + str(round(a['monthly_cost_usd'], 2)) + " | " + str(round(a['runs_per_day'], 1)) + " |\n"
    
    return out


def route_briefs():
    org = load_json(STATE_DIR / "org-state.json")
    agents = org.get("agents", {})
    
    all_briefs = []
    for name, info in agents.items():
        for b in info.get("briefs", []):
            all_briefs.append(dict(b, agent=name))
    
    all_briefs.sort(key=lambda b: b.get("modified", ""), reverse=True)
    
    out = "# Recent Briefs\n\n"
    out += "Total: " + str(len(all_briefs)) + " briefs\n\n"
    for b in all_briefs[:30]:
        out += "- **" + b['agent'] + "** " + b['date'] + " (" + str(b['size_bytes']) + " bytes)\n"
    
    return out


def route_errors():
    errors = load_json(STATE_DIR / "errors.json")
    
    out = "# Recent Errors\n\n"
    out += "- Total: " + str(errors.get('total_errors', 0)) + "\n"
    out += "- By type: " + json.dumps(errors.get('errors_by_type', {})) + "\n"
    out += "- Unique jobs: " + str(errors.get('unique_jobs_affected', 0)) + "\n\n"
    
    out += "## Top errors\n\n"
    out += "| Job | Type | Code | Suggestion |\n"
    out += "|-----|------|------|------------|\n"
    for e in errors.get("errors", [])[:10]:
        out += "| " + e['job'] + " | " + e['type'] + " | " + str(e['code'] or "-") + " | " + e['suggestion'] + " |\n"
    
    return out


def route_skills():
    r = subprocess.run(
        ["/opt/hermes/.venv/bin/python3", "/opt/data/scripts/hermes-skills-audit.py", "score"],
        capture_output=True, text=True, timeout=30
    )
    
    out = "# Skill Audit\n\n"
    out += "```\n"
    out += r.stdout[:3000]
    out += "```\n"
    return out




def route_conversion():
    import subprocess
    r = subprocess.run(
        ["python3", "/opt/data/scripts/conversion-dashboard.py"],
        capture_output=True, text=True, timeout=30
    )
    return r.stdout


def main():
    routes = {
        "pulse": route_pulse,
        "agents": route_agents,
        "cron": route_cron,
        "customers": route_customers,
        "finances": route_finances,
        "briefs": route_briefs,
        "errors": route_errors,
        "skills": route_skills,
        "conversion": route_conversion,
    }
    
    if len(sys.argv) < 2:
        print("Usage: org-dashboard.py <route>")
        print("Routes: " + ", ".join(routes.keys()))
        sys.exit(1)
    
    route = sys.argv[1]
    if route == "all":
        for name in routes:
            print("\n" + "=" * 60 + "\n")
            print(routes[name]())
    elif route in routes:
        print(routes[route]())
    else:
        print("Unknown route: " + route)
        print("Available: " + ", ".join(routes.keys()))
        sys.exit(1)


if __name__ == "__main__":
    main()

