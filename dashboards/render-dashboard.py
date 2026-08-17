#!/usr/bin/env python3
"""Render the org dashboard from live state.

Reads:
  - /opt/data/agents/state/*.json
  - /opt/data/cron/jobs.json
  - /opt/data/config.yaml (mcp_servers)
  - /opt/data/kanban.db

Writes:
  - /opt/data/agents/dashboards/org.html
"""
import json
import re
import os
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path('/opt/data/agents/state')
TEMPLATE = Path('/opt/data/agents/dashboards/template.html')
OUT = Path('/opt/data/agents/dashboards/org.html')

# Hardcoded stats
MRR_USD = 240
ARR_USD = MRR_USD * 12
BURN_USD = 500
RUNWAY_MONTHS = None  # bootstrapped
SITES_LIVE = 17

DEFAULT_DEPT = {
    'stuck': 0, 'stale': 0,
    'deals': 0, 'compl': 0,
    'leads': 0, 'outreach': 0,
    'deploys': 0, 'inc': 0,
    'thesis': '3 (in flight)', 'pubs': 0,
    'kiki_streak': 0, 'contractors': 0,
}


def parse_cron_jobs() -> list:
    """Parse /opt/data/cron/jobs.json directly."""
    jobs_file = Path('/opt/data/cron/jobs.json')
    if not jobs_file.exists():
        return []
    try:
        data = json.loads(jobs_file.read_text())
    except Exception:
        return []
    jobs = []
    for j in data.get('jobs', []):
        sched = j.get('schedule', {})
        sched_display = sched.get('display', '?') if isinstance(sched, dict) else str(sched)
        has_script = bool(j.get('script_path') or j.get('script'))
        no_agent = j.get('no_agent', False) or has_script
        jobs.append({
            'name': j.get('name', '?'),
            'schedule': sched_display,
            'status': j.get('last_status') or 'pending',
            'mode': 'script' if no_agent else 'agent',
        })
    return jobs


def parse_mcp_servers() -> list:
    """Parse mcp_servers from config.yaml using bounded line-based parser."""
    config_files = ['/opt/data/.hermes/config.yaml', '/opt/data/config.yaml']
    for cf in config_files:
        try:
            content = Path(cf).read_text()
        except FileNotFoundError:
            continue
        # Find the line range for mcp_servers block
        lines = content.split('\n')
        start = end = None
        for i, line in enumerate(lines):
            if line == 'mcp_servers:':
                start = i
                # Find the end (next top-level key)
                for j in range(i + 1, len(lines)):
                    if re.match(r'^[a-z_]+:', lines[j]):
                        end = j
                        break
                if end is None:
                    end = len(lines)
                break
        if start is None:
            continue

        # Now parse line-by-line within the block
        mcp_servers = []
        i = start + 1
        while i < end:
            line = lines[i]
            # Server name: `  name:` at exactly 2-space indent
            m = re.match(r'^  (\w+):\s*$', line)
            if m:
                name = m.group(1)
                body_lines = []
                i += 1
                # Collect 4-space-indented lines
                while i < end and lines[i].startswith('    '):
                    body_lines.append(lines[i])
                    i += 1
                body = '\n'.join(body_lines)

                # Extract metadata
                url = re.search(r'url:\s*(\S+)', body)
                cmd = re.search(r'command:\s*(\S+)', body)
                args = re.findall(r'^\s*-\s+(.+)$', body, re.MULTILINE)
                enabled = 'enabled: true' in body
                if url:
                    transport = url.group(1)[:60]
                elif cmd:
                    transport = ' '.join(args[:3]) if args else cmd.group(1)
                else:
                    transport = '?'

                # Count specific tools if listed
                tools_match = re.search(r'tools:\s*\n((?:\s+-.*\n)+)', body)
                if tools_match:
                    n_tools = len(re.findall(r'^\s+-', tools_match.group(1), re.MULTILINE))
                    tools = f'{n_tools} tools'
                else:
                    tools = 'all'

                mcp_servers.append({
                    'name': name,
                    'transport': transport,
                    'tools': tools,
                    'status': 'enabled' if enabled else 'disabled',
                })
            else:
                i += 1
        return mcp_servers
    return []


def parse_kanban_tasks() -> list:
    """Parse /opt/data/kanban.db directly."""
    db_path = Path('/opt/data/kanban.db')
    if not db_path.exists():
        return []
    import sqlite3
    try:
        conn = sqlite3.connect(str(db_path), timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        tasks = []
        if 'tasks' in tables:
            cur.execute("SELECT id, title, status, assignee FROM tasks WHERE status != 'archived' ORDER BY id")
            for row in cur.fetchall():
                tasks.append({
                    'id': row[0],
                    'title': row[1] or '(untitled)',
                    'status': row[2] or 'unknown',
                    'assignee': row[3] or '—',
                    'project': '—',  # no project_slug column in schema
                })
        conn.close()
        return tasks
    except Exception as e:
        return [{'id': '?', 'title': f'parse error: {e}', 'status': '?', 'project': '?', 'assignee': '?'}]


def load_state_files() -> list:
    """Read all state files + return summaries."""
    states = []
    for f in sorted(STATE_DIR.glob('*.json')):
        try:
            data = json.loads(f.read_text())
            if 'decisions' in data:
                summary = f"{len(data.get('decisions',[]))} decisions, {len(data.get('open_questions',[]))} open"
            elif 'open_stuck' in data:
                summary = f"{len(data.get('open_stuck',[]))} stuck, {len(data.get('decisions_for_ivan',[]))} for Ivan"
            elif 'deals_open' in data:
                summary = f"{len(data.get('deals_open',[]))} deals, {len(data.get('compliance_flags',[]))} flags"
            elif 'leads_in_flight' in data:
                summary = f"{len(data.get('leads_in_flight',[]))} leads, {len(data.get('outreach_queue_today',[]))} queue"
            elif 'deploys_7d' in data:
                summary = f"{len(data.get('deploys_7d',[]))} deploys, {len(data.get('incidents_72h',[]))} incidents"
            elif 'thesis' in data:
                summary = f"thesis ch {data['thesis'].get('chapter','?')}"
            elif 'kiki_lesson_streak_weeks' in data:
                summary = f"streak {data.get('kiki_lesson_streak_weeks',0)}w, {len(data.get('contractors_active',[]))} contractors"
            else:
                summary = '—'
            stat = f.stat()
            states.append({
                'file': f.name,
                'size': stat.st_size,
                'mtime': datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat()[:19],
                'summary': summary,
            })
        except Exception as e:
            states.append({
                'file': f.name,
                'size': f.stat().st_size if f.exists() else 0,
                'mtime': '?',
                'summary': f'parse err: {e}',
            })
    return states


def load_history() -> list:
    """Read 7-day history from snapshot files."""
    history_dir = STATE_DIR / 'history'
    if not history_dir.exists():
        return []
    snapshots = []
    for f in sorted(history_dir.glob('*.json')):
        try:
            data = json.loads(f.read_text())
            snapshots.append(data)
        except Exception:
            pass
    return snapshots[-7:]


def load_history_csv() -> list:
    """Read summary.csv for cross-metric trends (cron health + MCP count + kanban)."""
    csv_file = STATE_DIR / 'history' / 'summary.csv'
    if not csv_file.exists():
        return []
    rows = []
    try:
        for line in csv_file.read_text().split('\n')[1:]:
            if not line.strip():
                continue
            parts = line.split(',')
            if len(parts) >= 6:
                rows.append({
                    'date': parts[0],
                    'cron_total': int(parts[1]) if parts[1].isdigit() else 0,
                    'cron_ok': int(parts[2]) if parts[2].isdigit() else 0,
                    'cron_error': int(parts[3]) if parts[3].isdigit() else 0,
                    'cron_pending': int(parts[4]) if parts[4].isdigit() else 0,
                    'mcp_count': int(parts[5]) if parts[5].isdigit() else 0,
                    'kanban_total': int(parts[6]) if len(parts) >= 7 and parts[6].isdigit() else 0,
                })
    except Exception:
        pass
    return rows[-30:]  # last 30 entries


def mcp_growth_chart(csv_rows: list) -> str:
    """SVG sparkline of MCP server count growth."""
    if len(csv_rows) < 2:
        return '<div class="empty">MCP growth trend starts tomorrow</div>'

    width = 400
    height = 60
    margin = 8
    n = len(csv_rows)
    x_step = (width - 2 * margin) / max(n - 1, 1)

    # Find min/max MCP for scaling
    counts = [r['mcp_count'] for r in csv_rows]
    max_count = max(counts) if counts else 1
    min_count = min(counts) if counts else 0
    span = max(max_count - min_count, 1)

    points = []
    for i, row in enumerate(csv_rows):
        x = margin + i * x_step
        y = height - margin - ((row['mcp_count'] - min_count) / span) * (height - 2 * margin)
        points.append((x, y))

    svg = f'<svg width="{width}" height="{height}" style="background:var(--bg-card);border:1px solid var(--border);border-radius:4px">'
    if len(points) > 1:
        path = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in points)
        svg += f'<path d="{path}" fill="none" stroke="var(--accent2)" stroke-width="2"/>'
        # Highlight first + last
        svg += f'<circle cx="{points[0][0]:.1f}" cy="{points[0][1]:.1f}" r="3" fill="var(--text-dim)"/>'
        svg += f'<circle cx="{points[-1][0]:.1f}" cy="{points[-1][1]:.1f}" r="4" fill="var(--accent2)"/>'
    # X-axis dates
    for i, row in enumerate(csv_rows):
        x = margin + i * x_step
        date = row['date'][-5:]
        svg += f'<text x="{x:.1f}" y="{height - 1}" fill="var(--text-dim)" font-size="9" text-anchor="middle">{date}</text>'
    svg += '</svg>'

    # Summary text
    first = csv_rows[0]['mcp_count']
    last = csv_rows[-1]['mcp_count']
    delta = last - first
    delta_pct = (delta / first * 100) if first else 0
    arrow = '↑' if delta > 0 else ('↓' if delta < 0 else '→')
    color = 'var(--ok)' if delta > 0 else ('var(--err)' if delta < 0 else 'var(--text-dim)')

    summary = f'<div style="display:flex;gap:24px;margin-top:8px;font-size:12px;color:var(--text-dim)">'
    summary += f'<span>first: <b style="color:var(--text)">{first}</b></span>'
    summary += f'<span>latest: <b style="color:var(--accent2)">{last}</b></span>'
    summary += f'<span>change: <b style="color:{color}">{arrow} {abs(delta)} ({delta_pct:+.0f}%)</b></span>'
    summary += '</div>'
    return svg + summary


def history_chart(history: list) -> str:
    """Build a simple SVG sparkline of cron health over 7 days."""
    if len(history) < 2:
        return '<div class="empty">history starts tomorrow (daily snapshot cron)</div>'

    width = 400
    height = 80
    margin = 10
    n = len(history)
    x_step = (width - 2 * margin) / max(n - 1, 1)

    points_ok = []
    points_err = []
    for i, snap in enumerate(history):
        cron = snap.get('cron', {})
        ok = cron.get('ok', 0)
        err = cron.get('error', 0)
        x = margin + i * x_step
        max_jobs = max(20, ok + err + 5)
        y_ok = height - margin - (ok / max_jobs) * (height - 2 * margin)
        y_err = height - margin - (err / max_jobs) * (height - 2 * margin)
        points_ok.append((x, y_ok))
        points_err.append((x, y_err))

    svg = f'<svg width="{width}" height="{height}" style="background:var(--bg-card);border:1px solid var(--border);border-radius:4px">'
    if len(points_ok) > 1:
        path_ok = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in points_ok)
        svg += f'<path d="{path_ok}" fill="none" stroke="var(--ok)" stroke-width="2"/>'
        for x, y in points_ok:
            svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="var(--ok)"/>'
    if len(points_err) > 1:
        path_err = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in points_err)
        svg += f'<path d="{path_err}" fill="none" stroke="var(--err)" stroke-width="2" stroke-dasharray="4,2"/>'
        for x, y in points_err:
            svg += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="var(--err)"/>'
    for i, snap in enumerate(history):
        x = margin + i * x_step
        date = snap.get('date', '')[-5:]
        svg += f'<text x="{x:.1f}" y="{height - 1}" fill="var(--text-dim)" font-size="9" text-anchor="middle">{date}</text>'
    svg += '<text x="5" y="12" fill="var(--ok)" font-size="9">● ok</text>'
    svg += f'<text x="35" y="12" fill="var(--err)" font-size="9">● error</text>'
    svg += '</svg>'

    last = history[-1].get('cron', {})
    summary = f'<div style="display:flex;gap:24px;margin-top:8px;font-size:12px;color:var(--text-dim)">'
    summary += f'<span>last: <b style="color:var(--text)">{history[-1].get("date","?")}</b></span>'
    summary += f'<span>ok: <b style="color:var(--ok)">{last.get("ok",0)}</b></span>'
    summary += f'<span>err: <b style="color:var(--err)">{last.get("error",0)}</b></span>'
    summary += f'<span>total: <b style="color:var(--text)">{last.get("total",0)}</b></span>'
    summary += '</div>'
    return svg + summary


def render():
    print("step 1: starting render", flush=True)
    template = TEMPLATE.read_text()
    now = datetime.now(timezone.utc).isoformat()[:19]
    print("step 2: parsed template", flush=True)

    cron_jobs = parse_cron_jobs()
    print(f"step 3: parsed {len(cron_jobs)} cron jobs", flush=True)

    cron_rows = []
    for j in cron_jobs:
        status_pill = {
            'ok': '<span class="pill pill-ok">ok</span>',
            'error': '<span class="pill pill-err">error</span>',
            'pending': '<span class="pill pill-dim">pending</span>',
        }[j['status']]
        mode_pill = f'<span class="pill pill-dim">{j["mode"]}</span>'
        # data-filter for JS interactive filtering
        filter_tags = f'{j["status"]} {j["mode"]}'
        cron_rows.append(
            f'<tr data-filter="{filter_tags}"><td><code>{j["name"]}</code></td>'
            f"<td>{j['schedule']}</td>"
            f"<td>{status_pill}</td>"
            f"<td>—</td>"
            f"<td>{mode_pill}</td></tr>"
        )
    cron_total = len(cron_jobs)
    cron_ok = sum(1 for j in cron_jobs if j['status'] == 'ok')
    cron_err = sum(1 for j in cron_jobs if j['status'] == 'error')
    print(f"step 4: built cron rows", flush=True)

    mcp_servers = parse_mcp_servers()
    print(f"step 5: parsed {len(mcp_servers)} MCP servers", flush=True)

    mcp_rows = []
    for s in mcp_servers:
        status_pill = (
            f'<span class="pill pill-ok">{s["status"]}</span>' if s['status'] == 'enabled'
            else f'<span class="pill pill-warn">{s["status"]}</span>'
        )
        # data-filter: transport (stdio/http) + status (ok/err) + auth needs
        auth_tag = 'auth' if 'oauth' in s.get('auth', '').lower() or 'token' in s.get('auth', '').lower() else ''
        transport_tag = s['transport'] if s['transport'] in ('stdio', 'http') else 'stdio'
        status_tag = 'ok' if s['status'] == 'enabled' else 'err'
        filter_tags = f'{transport_tag} {status_tag} {auth_tag}'.strip()
        mcp_rows.append(
            f'<tr data-filter="{filter_tags}"><td><code>{s["name"]}</code></td>'
            f"<td>{s['transport']}</td>"
            f"<td>{s['tools']}</td>"
            f"<td>{status_pill}</td></tr>"
        )
    mcp_total = len(mcp_servers)
    mcp_enabled = sum(1 for s in mcp_servers if s['status'] == 'enabled')
    print("step 6: built MCP rows", flush=True)

    tasks = parse_kanban_tasks()
    print(f"step 7: parsed {len(tasks)} kanban tasks", flush=True)

    kanban_rows = []
    for t in tasks[:20]:
        # Map status to filter tag
        status = t.get('status', 'unknown')
        if status in ('ready', 'todo'):
            status_tag = 'ready'
        elif status in ('claimed', 'in_progress', 'running'):
            status_tag = 'claimed'
        elif status in ('blocked', 'failed'):
            status_tag = 'blocked'
        elif status in ('done', 'completed'):
            status_tag = 'done'
        else:
            status_tag = 'ready'  # default
        kanban_rows.append(
            f'<tr data-filter="{status_tag}"><td>{t["title"][:60]}</td>'
            f"<td>{t['project']}</td>"
            f"<td>{t['assignee']}</td>"
            f"<td>{status}</td></tr>"
        )
    if not kanban_rows:
        kanban_rows.append('<tr data-filter="empty"><td colspan="4" class="empty">no active tasks</td></tr>')
    print("step 8: built kanban rows", flush=True)

    states = load_state_files()
    print(f"step 9: loaded {len(states)} state files", flush=True)

    state_rows = []
    now_dt = datetime.now(timezone.utc)
    for s in states:
        # Categorize: agent vs dept
        is_agent = s['file'] in ('analyst.json', 'coord.json', 'kiki.json', 'kiki-prep.json')
        category_tag = 'agent' if is_agent else 'dept'
        # Recency
        try:
            mt = datetime.fromisoformat(s['mtime'].replace('Z', '+00:00')) if 'T' in s['mtime'] else None
            age_days = (now_dt - mt).days if mt else 999
        except Exception:
            age_days = 999
        if age_days <= 1:
            recency_tag = 'recent'
        elif age_days > 7:
            recency_tag = 'stale'
        else:
            recency_tag = ''
        filter_tags = f'{category_tag} {recency_tag}'.strip()
        state_rows.append(
            f'<tr data-filter="{filter_tags}"><td><code>{s["file"]}</code></td>'
            f"<td>{s['size']}</td>"
            f"<td>{s['mtime']}</td>"
            f"<td>{s['summary']}</td></tr>"
        )

    history = load_history()
    print(f"step 9b: loaded {len(history)} history snapshots", flush=True)
    history_html = history_chart(history)

    csv_rows = load_history_csv()
    print(f"step 9c: loaded {len(csv_rows)} CSV rows for trend", flush=True)
    mcp_html = mcp_growth_chart(csv_rows)

    if RUNWAY_MONTHS is None:
        runway = '∞'
        runway_class = 'ok'
    else:
        runway = str(RUNWAY_MONTHS)
        runway_class = 'ok' if RUNWAY_MONTHS >= 6 else ('warn' if RUNWAY_MONTHS >= 3 else 'err')
    print("step 10: computed runway", flush=True)

    out = template
    replacements = {
        '__STAMP__': now + ' UTC',
        '__MRR__': str(MRR_USD),
        '__ARR__': f'{ARR_USD:,}',
        '__RUNWAY__': runway,
        '__RUNWAY_CLASS__': runway_class,
        '__BURN__': str(BURN_USD),
        '__SITES__': str(SITES_LIVE),
        '__PRS__': '0',
        '__PRS_OLD__': '—',
        '__STUCK__': str(DEFAULT_DEPT['stuck']),
        '__STUCK_CLASS__': 'ok' if DEFAULT_DEPT['stuck'] == 0 else 'warn',
        '__STALE__': str(DEFAULT_DEPT['stale']),
        '__DEALS__': str(DEFAULT_DEPT['deals']),
        '__COMPL__': str(DEFAULT_DEPT['compl']),
        '__COMPL_CLASS__': 'ok' if DEFAULT_DEPT['compl'] == 0 else 'warn',
        '__LEADS__': str(DEFAULT_DEPT['leads']),
        '__OUTREACH__': str(DEFAULT_DEPT['outreach']),
        '__DEPLOYS__': str(DEFAULT_DEPT['deploys']),
        '__INC__': str(DEFAULT_DEPT['inc']),
        '__INC_CLASS__': 'ok' if DEFAULT_DEPT['inc'] == 0 else 'warn',
        '__THESIS__': DEFAULT_DEPT['thesis'],
        '__PUBS__': str(DEFAULT_DEPT['pubs']),
        '__KIKI_STREAK__': f"{DEFAULT_DEPT['kiki_streak']}w",
        '__CONTRACTORS__': str(DEFAULT_DEPT['contractors']),
        '__CRON_TOTAL__': str(cron_total),
        '__CRON_OK__': str(cron_ok),
        '__CRON_ERR__': str(cron_err),
        '__CRON_ROWS__': '\n'.join(cron_rows) or '<tr><td colspan="5" class="empty">no cron jobs</td></tr>',
        '__MCP_TOTAL__': str(mcp_total),
        '__MCP_ENABLED__': str(mcp_enabled),
        '__MCP_ROWS__': '\n'.join(mcp_rows) or '<tr><td colspan="4" class="empty">no MCP servers</td></tr>',
        '__KANBAN_ROWS__': '\n'.join(kanban_rows),
        '__STATE_ROWS__': '\n'.join(state_rows),
        '__HISTORY_HTML__': history_html,
        '__MCP_GROWTH_HTML__': mcp_html,
    }

    for k, v in replacements.items():
        out = out.replace(k, v)
    out = re.sub(r'__[A-Z_]+__', '—', out)
    print("step 11: built output HTML", flush=True)

    OUT.write_text(out)
    print(f"step 12: wrote {OUT} ({len(out):,} bytes)", flush=True)
    print(f"\n  Cron: {cron_total} jobs ({cron_ok} ok, {cron_err} err)")
    print(f"  MCP: {mcp_total} servers ({mcp_enabled} enabled)")
    print(f"  Kanban: {len(tasks)} tasks")
    print(f"  State: {len(states)} files")


if __name__ == '__main__':
    render()