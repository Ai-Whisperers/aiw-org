#!/usr/bin/env python3
"""HTTP server for the org dashboard.

Run: python3 ~/.hermes/scripts/dashboard-server.py [port]

Default port: 8765
Token auth: set DASHBOARD_TOKEN env var, or pass as 2nd arg.
If DASHBOARD_TOKEN is unset, server runs open (localhost-only safe).

Endpoints:
  /                       → org.html (live dashboard)
  /dept/<name>.html       → per-dept dashboard (operations, finance, ...)
  /healthz                → {"status": "ok"}
  /api/state              → all state files (JSON)
  /api/cron               → cron jobs
  /api/mcp                → MCP servers
  /api/kanban             → kanban tasks
  /api/all                → everything
  /export/csv             → combined CSV (cron + mcp + state summary)
  /export/board-report    → HTML board report (printable)
  /export/pdf             → simple text-based PDF (no external deps)

Auth:
  GET /api/* and /export/* require ?token=XXX or Authorization: Bearer XXX
  HTML pages (/, /dept/*, /healthz) are always public (dashboard is viewable)
  Set DASHBOARD_TOKEN env var to enable auth.
"""
import csv
import hashlib
import hmac
import http.server
import io
import json
import os
import secrets
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

DASHBOARD_DIR = Path('/opt/data/agents/dashboards')
ORG_HTML = DASHBOARD_DIR / 'org.html'
STATE_DIR = Path('/opt/data/agents/state')
CRON_FILE = Path('/opt/data/.hermes/cron/jobs.json')
KANBAN_DB = Path('/opt/data/kanban.db')
CONFIG_FILE = Path('/opt/data/.hermes/config.yaml')
HISTORY_DIR = STATE_DIR / 'history'
DEFAULT_PORT = 8765

# Auth: token from env or arg
AUTH_TOKEN = os.environ.get('DASHBOARD_TOKEN', '')
if not AUTH_TOKEN and len(sys.argv) > 2:
    AUTH_TOKEN = sys.argv[2]
    sys.argv.pop(2)  # so port arg stays in position 1


def log(msg):
    ts = datetime.now(timezone.utc).isoformat()[:19]
    print(f"[{ts}] {msg}", flush=True)


# ========================================================================
# Data readers (shared with the renderer)
# ========================================================================

def read_state_files():
    states = {}
    if not STATE_DIR.exists():
        return states
    for f in STATE_DIR.glob('*.json'):
        try:
            data = json.loads(f.read_text())
            states[f.stem] = {
                'data': data,
                'size': f.stat().st_size,
                'mtime': f.stat().st_mtime,
            }
        except Exception as e:
            states[f.stem] = {'error': str(e)}
    return states


def read_cron_jobs():
    if not CRON_FILE.exists():
        return []
    try:
        data = json.loads(CRON_FILE.read_text())
        jobs = data.get('jobs', [])
        return [{
            'id': j.get('id'),
            'name': j.get('name'),
            'schedule': j.get('schedule_display') or '?',
            'status': j.get('last_status') or 'pending',
            'enabled': j.get('enabled', True),
            'no_agent': j.get('no_agent', False),
            'toolsets_count': len(j.get('enabled_toolsets', []) or []),
        } for j in jobs]
    except Exception:
        return []


def read_kanban_tasks():
    if not KANBAN_DB.exists():
        return []
    import sqlite3
    try:
        conn = sqlite3.connect(str(KANBAN_DB), timeout=5)
        cur = conn.cursor()
        cur.execute("SELECT id, title, status, assignee, body, created_at FROM tasks WHERE status != 'archived' ORDER BY created_at DESC LIMIT 100")
        tasks = []
        for row in cur.fetchall():
            tasks.append({
                'id': row[0], 'title': row[1], 'status': row[2],
                'assignee': row[3], 'body': row[4], 'created_at': row[5],
            })
        conn.close()
        return tasks
    except Exception:
        return []


def read_mcp_servers():
    if not CONFIG_FILE.exists():
        return []
    content = CONFIG_FILE.read_text()
    lines = content.split('\n')
    start = end = None
    for i, line in enumerate(lines):
        if line == 'mcp_servers:':
            start = i
            for j in range(i + 1, len(lines)):
                if lines[j] and not lines[j].startswith(' ') and not lines[j].startswith('\t'):
                    end = j
                    break
            if end is None:
                end = len(lines)
            break
    if start is None:
        return []
    import re as _re
    servers = []
    i = start + 1
    while i < end:
        line = lines[i]
        m = _re.match(r'^  (\w+):\s*$', line)
        if m:
            name = m.group(1)
            i += 1
            body_lines = []
            while i < end and lines[i].startswith('    '):
                body_lines.append(lines[i])
                i += 1
            body = '\n'.join(body_lines)
            url = _re.search(r'url:\s*(\S+)', body)
            cmd = _re.search(r'command:\s*(\S+)', body)
            args = _re.findall(r'^\s*-\s+(.+)$', body, _re.MULTILINE)
            enabled = 'enabled: true' in body
            if url:
                transport = url.group(1)[:80]
            elif cmd:
                transport = (cmd.group(1) + ' ' + ' '.join(args[:2]))[:80]
            else:
                transport = '?'
            servers.append({'name': name, 'transport': transport, 'enabled': enabled})
        else:
            i += 1
    return servers


def read_history_csv():
    csv_file = HISTORY_DIR / 'summary.csv'
    if not csv_file.exists():
        return []
    rows = []
    for line in csv_file.read_text().split('\n')[1:]:
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) >= 6:
            rows.append({
                'date': parts[0],
                'cron_total': parts[1],
                'cron_ok': parts[2],
                'cron_error': parts[3],
                'cron_pending': parts[4],
                'mcp_count': parts[5],
                'kanban_total': parts[6] if len(parts) >= 7 else '0',
            })
    return rows


# ========================================================================
# Export generators
# ========================================================================

def export_csv_combined():
    """Build a combined CSV with cron + mcp + state summary."""
    buf = io.StringIO()
    w = csv.writer(buf)

    # Section 1: Cron jobs
    w.writerow(['# SECTION: CRON JOBS'])
    w.writerow(['name', 'schedule', 'status', 'enabled', 'mode', 'toolsets_count'])
    for j in read_cron_jobs():
        w.writerow([
            j.get('name', ''),
            j.get('schedule', ''),
            j.get('status', ''),
            j.get('enabled', False),
            'script' if j.get('no_agent') else 'agent',
            j.get('toolsets_count', 0),
        ])

    w.writerow([])
    # Section 2: MCP servers
    w.writerow(['# SECTION: MCP SERVERS'])
    w.writerow(['name', 'transport', 'enabled'])
    for s in read_mcp_servers():
        w.writerow([s.get('name', ''), s.get('transport', ''), s.get('enabled', False)])

    w.writerow([])
    # Section 3: State files
    w.writerow(['# SECTION: STATE FILES'])
    w.writerow(['file', 'size_bytes', 'mtime', 'keys_count'])
    for stem, info in read_state_files().items():
        if 'data' in info:
            w.writerow([
                f'{stem}.json',
                info.get('size', 0),
                datetime.fromtimestamp(info.get('mtime', 0), tz=timezone.utc).isoformat()[:19],
                len(info.get('data', {})),
            ])

    w.writerow([])
    # Section 4: History
    w.writerow(['# SECTION: HISTORY'])
    w.writerow(['date', 'cron_total', 'cron_ok', 'cron_error', 'cron_pending', 'mcp_count', 'kanban_total'])
    for row in read_history_csv():
        w.writerow([row['date'], row['cron_total'], row['cron_ok'], row['cron_error'],
                    row['cron_pending'], row['mcp_count'], row['kanban_total']])

    return buf.getvalue()


def export_board_report():
    """Build a printable HTML board report."""
    cron_jobs = read_cron_jobs()
    mcp_servers = read_mcp_servers()
    states = read_state_files()
    history = read_history_csv()

    cron_total = len(cron_jobs)
    cron_ok = sum(1 for j in cron_jobs if j['status'] == 'ok')
    cron_err = sum(1 for j in cron_jobs if j['status'] == 'error')

    now = datetime.now(timezone.utc).isoformat()[:19]

    # Cron health %
    health_pct = (cron_ok / cron_total * 100) if cron_total else 0

    # Recent wins / concerns
    recent_wins = []
    concerns = []
    for stem, info in states.items():
        if 'data' in info:
            for k in ('recent_wins', 'wins'):
                if k in info['data']:
                    recent_wins.extend(info['data'][k][:3])
            for k in ('top_risk', 'risks', 'blockers'):
                if k in info['data']:
                    concerns.extend(info['data'][k][:3])

    wins_html = ''.join(f'<li>{w}</li>' for w in recent_wins[:5]) or '<li class="empty">none recorded</li>'
    concerns_html = ''.join(f'<li>{c}</li>' for c in concerns[:5]) or '<li class="empty">none recorded</li>'

    # State file summary
    state_rows = []
    for stem, info in states.items():
        if 'data' in info:
            data = info['data']
            summary = ''
            for k in ('top_risk', 'recent_wins', 'next_action'):
                if k in data:
                    v = data[k]
                    if isinstance(v, list):
                        v = ', '.join(str(x)[:50] for x in v[:2])
                    summary += f'<b>{k}</b>: {str(v)[:80]} '
            if not summary:
                summary = f'{len(data)} fields'
            state_rows.append(f'<tr><td><code>{stem}</code></td><td>{summary or "—"}</td></tr>')

    return f'''<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<title>AI Whisperers Board Report · {now[:10]}</title>
<style>
@media print {{
  body {{ font-size: 11pt; }}
  .page-break {{ page-break-after: always; }}
  .no-print {{ display: none; }}
}}
body {{ font-family: Georgia, serif; max-width: 800px; margin: 32px auto; padding: 0 24px; color: #222; line-height: 1.5; }}
h1 {{ border-bottom: 2px solid #333; padding-bottom: 8px; }}
h2 {{ margin-top: 24px; color: #444; border-bottom: 1px solid #ddd; padding-bottom: 4px; }}
.kpi-row {{ display: flex; gap: 24px; margin: 16px 0; }}
.kpi {{ flex: 1; padding: 12px; border: 1px solid #ddd; border-radius: 4px; background: #f9f9f9; }}
.kpi-label {{ font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 0.05em; }}
.kpi-value {{ font-size: 24px; font-weight: bold; margin-top: 4px; }}
ul {{ padding-left: 24px; }}
li.empty {{ color: #999; font-style: italic; }}
table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 14px; }}
th, td {{ text-align: left; padding: 6px 8px; border-bottom: 1px solid #ddd; }}
th {{ background: #f0f0f0; }}
code {{ background: #f5f5f5; padding: 1px 4px; border-radius: 3px; font-family: "SF Mono", monospace; }}
.toc {{ background: #f9f9f9; padding: 12px 24px; border-radius: 4px; margin: 16px 0; }}
.toc ul {{ margin: 4px 0; }}
.btn {{ display: inline-block; padding: 8px 16px; background: #0066cc; color: white; text-decoration: none; border-radius: 4px; margin: 4px; }}
</style>
</head>
<body>

<div class="no-print" style="text-align:right;margin-bottom:16px">
  <a class="btn" href="javascript:window.print()">Print this report</a>
</div>

<h1>AI Whisperers Paraguay EAS</h1>
<p style="color:#666;margin-top:-8px">Board Report · Generated {now} UTC</p>

<div class="toc">
<b>Contents</b>
<ul>
<li><a href="#overview">Overview</a></li>
<li><a href="#wins">Recent wins</a></li>
<li><a href="#concerns">Concerns / risks</a></li>
<li><a href="#cron">Cron health</a></li>
<li><a href="#mcp">MCP servers</a></li>
<li><a href="#state">State file summary</a></li>
<li><a href="#history">7-day history</a></li>
</ul>
</div>

<h2 id="overview">Overview</h2>
<div class="kpi-row">
  <div class="kpi"><div class="kpi-label">Cron jobs</div><div class="kpi-value">{cron_total}</div></div>
  <div class="kpi"><div class="kpi-label">Cron OK rate</div><div class="kpi-value">{health_pct:.0f}%</div></div>
  <div class="kpi"><div class="kpi-label">Cron errors</div><div class="kpi-value">{cron_err}</div></div>
  <div class="kpi"><div class="kpi-label">MCP servers</div><div class="kpi-value">{len(mcp_servers)}</div></div>
  <div class="kpi"><div class="kpi-label">State files</div><div class="kpi-value">{len(states)}</div></div>
</div>

<h2 id="wins">Recent wins</h2>
<ul>{wins_html}</ul>

<h2 id="concerns">Concerns / risks</h2>
<ul>{concerns_html}</ul>

<h2 id="cron">Cron job health</h2>
<p>{cron_ok} of {cron_total} jobs running clean. {cron_err} need attention.</p>
<table>
<thead><tr><th>Job</th><th>Schedule</th><th>Status</th><th>Mode</th></tr></thead>
<tbody>
{''.join(f'<tr><td><code>{j["name"]}</code></td><td>{j["schedule"]}</td><td>{j["status"]}</td><td>{"script" if j.get("no_agent") else "agent"}</td></tr>' for j in cron_jobs)}
</tbody>
</table>

<div class="page-break"></div>

<h2 id="mcp">MCP servers ({len(mcp_servers)})</h2>
<table>
<thead><tr><th>Name</th><th>Transport</th><th>Enabled</th></tr></thead>
<tbody>
{''.join(f'<tr><td><code>{s["name"]}</code></td><td>{s["transport"]}</td><td>{"yes" if s["enabled"] else "no"}</td></tr>' for s in mcp_servers)}
</tbody>
</table>

<h2 id="state">State file summary</h2>
<table>
<thead><tr><th>File</th><th>Highlights</th></tr></thead>
<tbody>
{''.join(state_rows)}
</tbody>
</table>

<h2 id="history">7-day history</h2>
{('<table><thead><tr><th>Date</th><th>Cron OK</th><th>Errors</th><th>MCPs</th><th>Kanban</th></tr></thead><tbody>' + ''.join(f'<tr><td>{r["date"]}</td><td>{r["cron_ok"]}</td><td>{r["cron_error"]}</td><td>{r["mcp_count"]}</td><td>{r["kanban_total"]}</td></tr>' for r in history[-7:]) + '</tbody></table>') if history else '<p>no history snapshots yet</p>'}

<hr style="margin-top:32px;border:none;border-top:1px solid #ddd">
<p style="color:#666;font-size:11px;text-align:center">
Generated by AI Whisperers Paraguay EAS · auto-generated by Erebus · {now} UTC
</p>

</body></html>'''


def export_pdf():
    """Build a minimal PDF (text-based, no external libs).

    This generates a simple PDF with the board report content.
    Not pixel-perfect but printable + indexable by search engines.
    """
    # Generate the text content
    cron_jobs = read_cron_jobs()
    mcp_servers = read_mcp_servers()
    history = read_history_csv()

    cron_total = len(cron_jobs)
    cron_ok = sum(1 for j in cron_jobs if j['status'] == 'ok')
    cron_err = sum(1 for j in cron_jobs if j['status'] == 'error')
    now = datetime.now(timezone.utc).isoformat()[:19]

    lines = [
        "AI Whisperers Paraguay EAS — Board Report",
        f"Generated {now} UTC",
        "",
        "=" * 60,
        f"Cron jobs: {cron_total} total, {cron_ok} OK, {cron_err} errors",
        f"MCP servers: {len(mcp_servers)}",
        f"History snapshots: {len(history)}",
        "",
        "CRON HEALTH",
        "-" * 60,
    ]
    for j in cron_jobs:
        lines.append(f"  [{j['status']:>7}] {j['name']:35} {j['schedule']}")

    lines.extend([
        "",
        "MCP SERVERS",
        "-" * 60,
    ])
    for s in mcp_servers:
        lines.append(f"  [{('YES' if s['enabled'] else 'no '):>3}] {s['name']:25} {s['transport'][:50]}")

    if history:
        lines.extend([
            "",
            "7-DAY HISTORY",
            "-" * 60,
        ])
        for r in history[-7:]:
            lines.append(f"  {r['date']}  cron: {r['cron_ok']}ok/{r['cron_error']}err  mcps: {r['mcp_count']}  kanban: {r['kanban_total']}")

    text = '\n'.join(lines)

    # Build a minimal PDF (PDF 1.4)
    # Each line uses the built-in Helvetica font
    pdf_lines = []
    pdf_lines.append(b'%PDF-1.4\n')
    # Binary marker comment (PDF spec)

    # Object 1: Catalog
    objects = [None]  # 0-index unused
    objects.append(b'<< /Type /Catalog /Pages 2 0 R >>')
    objects.append(b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>')
    # Object 3: Page
    objects.append(b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>')

    # Build the content stream (text wrapped at ~80 chars per line)
    content_lines = ['BT', '/F1 10 Tf', '50 750 Td', '14 TL']
    for i, line in enumerate(text.split('\n')):
        # Escape PDF special chars
        escaped = line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')
        if i == 0:
            content_lines.append(f'({escaped}) Tj')
        else:
            content_lines.append(f'T*')
            content_lines.append(f'({escaped}) Tj')
    content_lines.append('ET')
    content_stream = '\n'.join(content_lines).encode('latin-1', errors='replace')

    # Object 4: Content stream
    objects.append(f'<< /Length {len(content_stream)} >>\nstream\n'.encode() + content_stream + b'\nendstream')
    # Object 5: Font
    objects.append(b'<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>')

    # Build the PDF body
    body = b''
    xref_offsets = [0]  # 0-index unused
    for i, obj in enumerate(objects[1:], 1):
        xref_offsets.append(len(b'%PDF-1.4\n') + len(body))
        body += f'{i} 0 obj\n'.encode('latin-1') + obj + b'\nendobj\n'

    xref_start = len(b'%PDF-1.4\n') + len(body)
    body += f'xref\n0 {len(objects)}\n'.encode('latin-1')
    body += b'0000000000 65535 f \n'
    for off in xref_offsets[1:]:
        body += f'{off:010d} 00000 n \n'.encode('latin-1')
    body += b'trailer\n'
    body += f'<< /Size {len(objects)} /Root 1 0 R >>\n'.encode('latin-1')
    body += b'startxref\n'
    body += f'{xref_start}\n'.encode('latin-1')
    body += b'%%EOF\n'

    return b'%PDF-1.4\n' + body


# ========================================================================
# HTTP handler
# ========================================================================

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Override to use our log format
        log(f"{self.address_string()} - {format % args}")

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def _check_auth(self):
        """Return True if request is authorized (no token required OR valid token)."""
        if not AUTH_TOKEN:
            return True
        parsed = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed.query)
        # Check ?token=
        if qs.get('token', [None])[0] == AUTH_TOKEN:
            return True
        # Check Authorization: Bearer
        auth_header = self.headers.get('Authorization', '')
        if auth_header.startswith('Bearer ') and auth_header[7:] == AUTH_TOKEN:
            return True
        return False

    def _send_unauthorized(self):
        body = json.dumps({
            'error': 'unauthorized',
            'message': 'set DASHBOARD_TOKEN env var and pass ?token=XXX or Authorization: Bearer XXX',
        }, indent=2).encode()
        self.send_response(401)
        self.send_header('Content-Type', 'application/json')
        self.send_header('WWW-Authenticate', 'Bearer realm="dashboard"')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # Public endpoints (no auth)
        if path == '/' or path == '/index.html':
            return self._serve_org_html()
        if path.startswith('/dept/') and path.endswith('.html'):
            return self._serve_dept(path)
        if path == '/healthz':
            return self._json({'status': 'ok', 'time': datetime.now(timezone.utc).isoformat()})

        # Authenticated endpoints (require token if DASHBOARD_TOKEN is set)
        if not self._check_auth():
            return self._send_unauthorized()

        if path == '/api/state':
            return self._json(read_state_files())
        if path == '/api/cron':
            return self._json(read_cron_jobs())
        if path == '/api/mcp':
            return self._json(read_mcp_servers())
        if path == '/api/kanban':
            return self._json(read_kanban_tasks())
        if path == '/api/all':
            return self._json({
                'state': read_state_files(),
                'cron': read_cron_jobs(),
                'mcp': read_mcp_servers(),
                'kanban': read_kanban_tasks(),
            })
        if path == '/export/csv':
            return self._csv(export_csv_combined())
        if path == '/export/board-report':
            return self._html(export_board_report())
        if path == '/export/pdf':
            return self._pdf(export_pdf())
        if path == '/':
            return self._serve_org_html()
        if path.endswith('.html'):
            fname = path.lstrip('/')
            fpath = DASHBOARD_DIR / fname
            if fpath.exists() and fpath.is_file():
                return self._html(fpath.read_text())
            return self._404()

        return self._404()

    def _serve_org_html(self):
        if ORG_HTML.exists():
            return self._html(ORG_HTML.read_text())
        return self._404()

    def _serve_dept(self, path):
        # Strip /dept/ prefix and optionally add 'dept-' prefix if missing
        fname = path[len('/dept/'):]
        if not fname.startswith('dept-'):
            fname = 'dept-' + fname
        fpath = DASHBOARD_DIR / fname
        if fpath.exists() and fpath.is_file():
            return self._html(fpath.read_text())
        return self._404()

    def _html(self, content):
        body = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data):
        body = json.dumps(data, indent=2, default=str).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _csv(self, content):
        body = content.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/csv; charset=utf-8')
        self.send_header('Content-Disposition', 'attachment; filename="org-dashboard.csv"')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _pdf(self, content):
        self.send_response(200)
        self.send_header('Content-Type', 'application/pdf')
        self.send_header('Content-Disposition', 'attachment; filename="org-board-report.pdf"')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _404(self):
        body = b'404 not found'
        self.send_response(404)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    server = http.server.HTTPServer(('127.0.0.1', port), DashboardHandler)
    print(f"Dashboard server listening on http://0.0.0.0:{port}/")
    print(f"  /            → live org dashboard")
    print(f"  /dept/<name>.html → per-dept dashboard")
    print(f"  /healthz     → ok")
    print(f"  /api/*       → JSON endpoints")
    print(f"  /export/csv  → combined CSV")
    print(f"  /export/board-report → printable HTML report")
    print(f"  /export/pdf  → minimal PDF")
    if AUTH_TOKEN:
        print()
        print(f"  AUTH ENABLED: ?token=*** or Authorization: Bearer ***")
        print(f"  token length: {len(AUTH_TOKEN)}")
    else:
        print()
        print(f"  AUTH DISABLED (no DASHBOARD_TOKEN env var)")
        print(f"  set DASHBOARD_TOKEN=XXX to require auth on /api/* and /export/*")
    print()
    print(f"Open in browser: http://localhost:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nshutting down")
        server.shutdown()


if __name__ == '__main__':
    main()