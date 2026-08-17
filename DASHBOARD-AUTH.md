# Dashboard Auth Notes — 2026-08-13

> Brief reference for the dashboard HTTP server's token-based auth.
> The dashboard lives at `http://127.0.0.1:8765` (localhost-only binding).
> It serves `/opt/data/agents/dashboards/org.html` and `/api/*` endpoints.

## Current state (as of 2026-08-13)

- **Server**: `/opt/data/agents/dashboards/dashboard-server.py` (PID 196657)
- **Bind**: `127.0.0.1:8765` (NOT exposed externally)
- **Auth mode**: Token via env var `DASHBOARD_TOKEN`
- **Current token**: `rubiconeas-2026-aiw-pa-erebus` (already set in server env)

## Auth contract

| Endpoint | Auth required? | Token delivery |
|----------|----------------|----------------|
| `GET /` | No | n/a (HTML page is open; localhost-only safe) |
| `GET /healthz` | No | n/a (liveness probe) |
| `GET /api/*` | Yes (if `DASHBOARD_TOKEN` set) | `?token=XXX` OR `Authorization: Bearer XXX` |
| `GET /api/export/csv` | Yes | same |
| `GET /api/export/pdf` | Yes | same |
| `GET /dept/*.html` | No | n/a (static dept dashboards) |

## Token rotation

```bash
# 1. Stop server
pkill -f dashboard-server.py

# 2. Generate new token
NEW=$(python3 -c 'import secrets; print(secrets.token_urlsafe(24))')

# 3. Start server with new token
DASHBOARD_TOKEN="$NEW" nohup python3 /opt/data/agents/dashboards/dashboard-server.py \
  > /tmp/dashboard-server.log 2>&1 &

# 4. Update bookmarks (anywhere you browse from)
echo "$NEW" # copy to password manager
```

## When DASHBOARD_TOKEN is unset

Server runs **open** (no auth check). For localhost-only binding this is acceptable; for any non-localhost exposure, you MUST set the env var. The server prints a startup warning if auth is disabled:

```
AUTH DISABLED (no DASHBOARD_TOKEN env var)
set DASHBOARD_TOKEN=XXX to require auth on /api/* and /export/*
```

## Security notes

- The token is the **only** protection. Anyone with read access to `/proc/<pid>/environ` on this host can grab it. Treat the host as the security boundary, not the token.
- For external exposure (e.g., behind a reverse proxy), add real auth (OIDC / mTLS / Cloudflare Access) instead of relying on this env-var token.
- Logs are at `/tmp/dashboard-server.log` — auth failures are logged with the client IP and timestamp.

## Quick reference

```bash
# Curl with token
curl -H "Authorization: Bearer rubiconeas-2026-aiw-pa-erebus" http://127.0.0.1:8765/api/state

# Or as query param
curl "http://127.0.0.1:8765/api/state?token=rubiconeas-2026-aiw-pa-erebus"

# Health check (no auth)
curl http://127.0.0.1:8765/healthz
```

## Related

- Server source: `/opt/data/agents/dashboards/dashboard-server.py` (~669 lines)
- Dashboard HTML: `/opt/data/agents/dashboards/org.html` (~31KB)
- Per-dept pages: `/opt/data/agents/dashboards/dept-*.html` (6 files)