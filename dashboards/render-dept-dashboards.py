#!/usr/bin/env python3
"""Render per-department dashboard pages.

Reads the same state files as the main dashboard but builds dept-specific
views with focused KPIs for each department.

Usage:
  python3 render-dept-dashboards.py [dept_id]
  # dept_id = operations | finance | sales | engineering | research | people
  # No dept_id = render all 6

Outputs:
  /opt/data/agents/dashboards/dept-operations.html
  /opt/data/agents/dashboards/dept-finance.html
  ... etc
"""
import json
import os
import re
import csv
from datetime import datetime, timezone, timedelta
from pathlib import Path

STATE_DIR = Path('/opt/data/agents/state')
DASHBOARD_DIR = Path('/opt/data/agents/dashboards')
OUT_DIR = DASHBOARD_DIR

# Dept metadata
DEPTS = {
    'operations': {
        'label': 'Operations & Coordination',
        'head': 'Ivan',
        'lead_agent': 'management-coordinator',
        'cadence': 'Mon+Thu 17:00 PYT',
        'state_file': 'coord.json',
        'color': '#6b7280',
        'kpis': [
            ('cron_total', 'Cron jobs', 'Total scheduled'),
            ('cron_ok', 'OK', 'Cron jobs running clean'),
            ('cron_error', 'Errors', 'Cron jobs failing'),
            ('agents_active', 'Agents', 'Lead agents wired'),
            ('state_files', 'State files', 'Active memory files'),
            ('mcp_servers', 'MCP servers', 'External capabilities'),
        ],
    },
    'finance': {
        'label': 'Finance & Legal',
        'head': 'Ivan',
        'lead_agent': 'finance-controller',
        'cadence': 'Fri 18:00 PYT',
        'state_file': 'finance.json',
        'color': '#10b981',
        'kpis': [
            ('mrr_usd', 'MRR', 'Monthly recurring revenue USD'),
            ('burn_usd', 'Burn', 'Monthly spend USD'),
            ('runway_months', 'Runway', 'Months remaining'),
            ('deals_open', 'Open deals', 'In pipeline'),
            ('compliance_flags', 'Compliance flags', 'Trademark/billing'),
            ('renewals_due', 'Renewals (30d)', 'Coming due'),
        ],
    },
    'sales': {
        'label': 'Sales & Growth',
        'head': 'Ivan',
        'lead_agent': 'sales-pipeline',
        'cadence': 'Daily 12:00 PYT',
        'state_file': 'sales.json',
        'color': '#f59e0b',
        'kpis': [
            ('leads_total', 'Leads total', 'All-time'),
            ('leads_open', 'In flight', 'Currently active'),
            ('queue_today', 'Outreach queue', 'Today'),
            ('stalled', 'Stalled', 'No reply 7d+'),
            ('conversion_rate', 'Conv. rate', 'Lead → closed'),
            ('deals_won_30d', 'Won (30d)', 'Closed deals'),
        ],
    },
    'engineering': {
        'label': 'Engineering & Delivery',
        'head': 'Kiki',
        'lead_agent': 'engineering-roster',
        'cadence': 'Tue+Fri 17:00 PYT',
        'state_file': 'engineering.json',
        'color': '#3b82f6',
        'kpis': [
            ('deploys_7d', 'Deploys (7d)', 'Production releases'),
            ('open_prs', 'Open PRs', 'Awaiting merge'),
            ('stale_repos', 'Stale repos', 'No activity 7d+'),
            ('incidents_72h', 'Incidents (72h)', 'Customer-impacting'),
            ('infra_cost', 'Infra cost', 'Monthly USD'),
            ('tools_pending', 'Pending tools', 'Awaiting decision'),
        ],
    },
    'research': {
        'label': 'Research & Education',
        'head': 'Ivan',
        'lead_agent': 'research-tracker',
        'cadence': 'Sun 18:00 PYT',
        'state_file': 'research.json',
        'color': '#8b5cf6',
        'kpis': [
            ('thesis_progress', 'Thesis', 'Chapters done'),
            ('publications', 'Publications', 'In pipeline'),
            ('courses_ready', 'Courses ready', 'Published'),
            ('courses_draft', 'Courses draft', 'In development'),
            ('monetization_backlog', 'Monetization backlog', 'Revenue ideas'),
            ('integrity_audits', 'Integrity audits', 'Citation checks'),
        ],
    },
    'people': {
        'label': 'People & Culture',
        'head': 'Kiki',
        'lead_agent': 'kiki-coach',
        'cadence': 'Fri 17:00 PYT',
        'state_file': 'kiki.json',
        'color': '#ec4899',
        'kpis': [
            ('kiki_streak', 'Lesson streak', 'Weeks continuous'),
            ('kiki_lesson_count', 'Lessons total', 'All-time'),
            ('contractors_active', 'Contractors', 'Active'),
            ('founder_hours', 'Founder hours', 'Billable/week'),
            ('recognition_log', 'Recognitions', 'Milestones'),
            ('onboarding_queue', 'Onboarding queue', 'Next hires'),
        ],
    },
}


def read_state(state_file: str) -> dict:
    """Read a state file, return empty dict if missing."""
    p = STATE_DIR / state_file
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        return {}


def read_cron_for_dept(dept_id: str) -> list:
    """Find cron jobs that belong to a dept."""
    cron_file = Path('/opt/data/.hermes/cron/jobs.json')
    if not cron_file.exists():
        return []
    try:
        data = json.loads(cron_file.read_text())
    except Exception:
        return []
    jobs = []
    for j in data.get('jobs', []):
        name = j.get('name', '')
        # Match by dept prefix or lead agent name
        if name.startswith(f'aiw-{dept_id}-') or name.startswith(f'aiw-{DEPTS[dept_id]["lead_agent"].replace("-", "")}-') or DEPTS[dept_id]["lead_agent"] in name:
            jobs.append({
                'name': name,
                'schedule': j.get('schedule_display', '?'),
                'status': j.get('last_status') or 'pending',
                'enabled': j.get('enabled', True),
            })
    return jobs


def read_kanban_for_dept(dept_id: str) -> list:
    """Find kanban tasks tagged with dept."""
    db = Path('/opt/data/kanban.db')
    if not db.exists():
        return []
    import sqlite3
    try:
        conn = sqlite3.connect(str(db), timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT title, status, assignee, created_at FROM tasks WHERE status != 'archived' ORDER BY created_at DESC LIMIT 50")
        tasks = []
        for row in cur.fetchall():
            tasks.append({
                'title': row[0],
                'status': row[1] or 'unknown',
                'assignee': row[2] or '—',
                'created_at': row[3] or 0,
            })
        conn.close()
        return tasks
    except Exception:
        return []


def get_kpi_value(dept_id: str, kpi_key: str, state: dict, cron_jobs: list, kanban_tasks: list) -> str:
    """Get the KPI value for a dept + key."""
    # Per-dept-specific logic
    if dept_id == 'operations':
        if kpi_key == 'cron_total': return str(len(cron_jobs))
        if kpi_key == 'cron_ok': return str(sum(1 for j in cron_jobs if j['status'] == 'ok'))
        if kpi_key == 'cron_error': return str(sum(1 for j in cron_jobs if j['status'] == 'error'))
        if kpi_key == 'agents_active': return str(sum(1 for d in DEPTS if any(read_cron_for_dept(d))))
        if kpi_key == 'state_files': return str(len(list(STATE_DIR.glob('*.json'))))
        if kpi_key == 'mcp_servers': return '—'  # could parse config

    if dept_id == 'finance':
        return str(state.get(kpi_key, '—'))

    if dept_id == 'sales':
        if kpi_key == 'leads_total':
            return str(state.get('leads_total', len(state.get('leads_in_flight', []))))
        return str(state.get(kpi_key, '—'))

    if dept_id == 'engineering':
        return str(state.get(kpi_key, '—'))

    if dept_id == 'research':
        if kpi_key == 'thesis_progress':
            t = state.get('thesis', {})
            return f"ch {t.get('chapter', '?')}/{t.get('total', 5)}"
        return str(state.get(kpi_key, '—'))

    if dept_id == 'people':
        return str(state.get(kpi_key, '—'))

    return '—'


def render_dept(dept_id: str) -> str:
    """Build the HTML for one department."""
    cfg = DEPTS[dept_id]
    state = read_state(cfg['state_file'])
    cron_jobs = read_cron_for_dept(dept_id)
    kanban_tasks = read_kanban_for_dept(dept_id)

    # KPI cards
    kpi_cards = []
    for kpi_key, kpi_label, kpi_help in cfg['kpis']:
        val = get_kpi_value(dept_id, kpi_key, state, cron_jobs, kanban_tasks)
        kpi_cards.append(f'''
<div class="kpi-card" style="border-left:3px solid {cfg['color']}">
  <div class="kpi-label">{kpi_label}</div>
  <div class="kpi-value">{val}</div>
  <div class="kpi-help">{kpi_help}</div>
</div>''')

    # Cron jobs table
    if cron_jobs:
        cron_rows = '\n'.join(
            f'<tr><td><code>{j["name"]}</code></td>'
            f'<td>{j["schedule"]}</td>'
            f'<td><span class="pill pill-{("ok" if j["status"]=="ok" else ("err" if j["status"]=="error" else "dim"))}">{j["status"]}</span></td></tr>'
            for j in cron_jobs
        )
    else:
        cron_rows = '<tr><td colspan="3" class="empty">no cron jobs scheduled for this dept</td></tr>'

    # Kanban tasks
    if kanban_tasks:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        task_rows = []
        for t in kanban_tasks[:15]:
            created = t['created_at']
            age = ''
            if created:
                try:
                    age_dt = datetime.fromtimestamp(created, tz=timezone.utc)
                    age = f'{(now - age_dt).days}d'
                except Exception:
                    pass
            task_rows.append(
                f'<tr><td>{t["title"][:50]}</td>'
                f'<td>{t["status"]}</td>'
                f'<td>{t["assignee"]}</td>'
                f'<td>{age}</td></tr>'
            )
        kanban_rows = '\n'.join(task_rows)
    else:
        kanban_rows = '<tr><td colspan="4" class="empty">no tasks</td></tr>'

    # State summary
    state_summary = '<div class="empty">no state yet</div>'
    if state:
        # Pull out interesting keys
        interesting_keys = ['last_run', 'next_action', 'blockers', 'pending_decisions',
                           'top_risk', 'recent_wins', 'open_questions']
        items = []
        for k in interesting_keys:
            if k in state:
                v = state[k]
                if isinstance(v, list):
                    v = ', '.join(str(x)[:60] for x in v[:3])
                elif isinstance(v, dict):
                    v = ', '.join(f'{kk}={vv}' for kk, vv in list(v.items())[:3])
                else:
                    v = str(v)[:200]
                items.append(f'<li><code>{k}</code>: {v}</li>')
        if items:
            state_summary = '<ul style="font-size:13px;color:var(--text);line-height:1.6">' + '\n'.join(items) + '</ul>'

    # Last updated
    state_file = STATE_DIR / cfg['state_file']
    if state_file.exists():
        last_modified = datetime.fromtimestamp(state_file.stat().st_mtime, tz=timezone.utc).isoformat()[:19]
    else:
        last_modified = 'never'

    now_str = datetime.now(timezone.utc).isoformat()[:19]

    return f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>{cfg["label"]} · AI Whisperers</title>
<style>
:root {{
  --bg: #0f1115; --bg-card: #181c23; --text: #e6e6e6; --text-dim: #9ca3af;
  --border: #2a2f3a; --ok: #10b981; --err: #ef4444; --warn: #f59e0b;
  --accent: {cfg["color"]}; --accent2: #a78bfa;
}}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 24px; }}
header {{ display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 24px; }}
h1 {{ margin: 0; font-size: 22px; }}
h1 small {{ color: var(--text-dim); font-weight: 400; font-size: 13px; }}
.dept-meta {{ color: var(--text-dim); font-size: 13px; margin-bottom: 24px; }}
.kpi-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin-bottom: 24px; }}
.kpi-card {{ background: var(--bg-card); padding: 16px; border-radius: 6px; }}
.kpi-label {{ color: var(--text-dim); font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; }}
.kpi-value {{ font-size: 28px; font-weight: 600; color: var(--accent); margin: 6px 0; font-variant-numeric: tabular-nums; }}
.kpi-help {{ color: var(--text-dim); font-size: 11px; }}
.card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 6px; padding: 16px; margin-bottom: 16px; }}
h2 {{ font-size: 13px; color: var(--text-dim); margin: 16px 0 12px; text-transform: uppercase; letter-spacing: 0.05em; }}
table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
th, td {{ text-align: left; padding: 6px 8px; border-bottom: 1px solid var(--border); }}
th {{ color: var(--text-dim); font-weight: 500; font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; }}
.pill {{ display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 11px; }}
.pill-ok {{ background: rgba(16, 185, 129, 0.2); color: var(--ok); }}
.pill-err {{ background: rgba(239, 68, 68, 0.2); color: var(--err); }}
.pill-dim {{ background: var(--border); color: var(--text-dim); }}
code {{ background: rgba(255,255,255,0.05); padding: 1px 4px; border-radius: 3px; font-family: "SF Mono", monospace; }}
.empty {{ color: var(--text-dim); font-style: italic; }}
footer {{ color: var(--text-dim); font-size: 11px; text-align: center; margin-top: 32px; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
@media (max-width: 800px) {{ .grid-2 {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<header>
  <div>
    <h1>{cfg["label"]} <small>Dept dashboard</small></h1>
    <div class="dept-meta">
      Head: <b>{cfg["head"]}</b> · Lead agent: <code>{cfg["lead_agent"]}</code> · Cadence: <b>{cfg["cadence"]}</b>
      · <a href="/">← main dashboard</a>
    </div>
  </div>
  <div class="dept-meta">Generated {now_str} UTC</div>
</header>

<div class="kpi-grid">
{''.join(kpi_cards)}
</div>

<div class="grid-2">
<div class="card">
<h2>Cron Jobs ({len(cron_jobs)})</h2>
<table>
<thead><tr><th>Job</th><th>Schedule</th><th>Status</th></tr></thead>
<tbody>{cron_rows}</tbody>
</table>
</div>

<div class="card">
<h2>State File Summary</h2>
<p style="color:var(--text-dim);font-size:11px;margin:0 0 8px"><code>{cfg["state_file"]}</code> · last modified {last_modified}</p>
{state_summary}
</div>
</div>

<div class="card">
<h2>Recent Kanban Tasks</h2>
<table>
<thead><tr><th>Task</th><th>Status</th><th>Assignee</th><th>Age</th></tr></thead>
<tbody>{kanban_rows}</tbody>
</table>
</div>

<footer>
AI Whisperers Paraguay EAS · Dept dashboard · auto-generated by Erebus
</footer>
</body></html>'''


def main():
    import sys
    depts_to_render = sys.argv[1:] if len(sys.argv) > 1 else list(DEPTS.keys())

    for dept_id in depts_to_render:
        if dept_id not in DEPTS:
            print(f"unknown dept: {dept_id}", file=sys.stderr)
            continue
        html = render_dept(dept_id)
        out = OUT_DIR / f'dept-{dept_id}.html'
        out.write_text(html)
        print(f"✓ {out} ({out.stat().st_size:,} bytes)")


if __name__ == '__main__':
    main()