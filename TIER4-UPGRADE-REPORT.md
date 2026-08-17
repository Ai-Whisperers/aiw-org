# Tier 4 — Followup Sub-tasks Report (2026-08-13)

> Pure-internal upgrades. 5 sub-tasks all done.

---

## Summary

| # | Sub-task | Status | Files changed |
|---|----------|--------|---------------|
| 1 | Wire dept agents to per-dept toolset | ✓ DONE | 7 cron job prompts |
| 2 | Add HTTP server for dashboard | ✓ DONE | 1 new script + symlink |
| 3 | Wire state files to real agents | ✓ DONE | 4 cron job prompts |
| 4 | 7-day history tracking | ✓ DONE | 1 new script + cron + chart |
| 5 | Interactive filters + sort | ✓ DONE | template.html + JS |

---

## Sub-task 1: Dept lead agents to per-dept toolset

### What I did

For each of the 7 dept lead agents, I set `enabled_toolsets` (allowlist) in the cron job's JSON record. This is the cron-level equivalent of per-profile `disabled_toolsets`.

### Mapping

| Job | Dept | Toolsets allowed | Count |
|-----|------|----------------|-------|
| aiw-business-analyst-daily | operations | terminal, file, web, skills, memory, code_execution, ... | 15 |
| aiw-management-coord-biwk | operations | (same) | 15 |
| aiw-kiki-coach-weekly | people | file, memory, skills, code_execution, ... | 11 |
| aiw-sales-pipeline-daily | sales | + browser, delegation, image_gen | 15 |
| aiw-finance-controller-weekly | finance | + delegation | 12 |
| aiw-engineering-roster-biwk | engineering | (most permissive) | 17 |
| aiw-research-tracker-weekly | research | + browser | 13 |

### Discovery

The runtime was split: cron jobs are persisted to `/opt/data/cron/jobs.json` (via the cronjob tool), but the gateway reads from `/opt/data/.hermes/cron/jobs.json`. Fixed by copying + gateway restart.

### Files changed

- `/opt/data/cron/jobs.json` — written
- `/opt/data/.hermes/cron/jobs.json` — copied + gateway restarted
- 7 jobs in `jobs.json` got `enabled_toolsets` field

### Verification

```
$ hermes cron list
19 jobs visible, 7 aiw- agents have dept-specific toolsets enabled
```

---

## Sub-task 2: HTTP server for dashboard

### What I built

`/opt/data/agents/dashboards/dashboard-server.py` — a minimal Python HTTP server.

### Endpoints

| Path | Returns | Size |
|------|---------|------|
| `/` | Live org dashboard (org.html) | ~21KB |
| `/healthz` | `{"status": "ok", "time": ...}` | 60B |
| `/api/state` | All 9 state files as JSON | ~3KB |
| `/api/cron` | All cron jobs as JSON | ~5KB |
| `/api/mcp` | All MCP servers as JSON | ~1KB |
| `/api/kanban` | All kanban tasks as JSON | ~1KB |
| `/api/all` | Everything combined | ~10KB |

### How to start

```bash
python3 ~/.hermes/scripts/dashboard-server.py 8765
# or
nohup python3 ~/.hermes/scripts/dashboard-server.py 8765 &
```

Default port 8765. Curl-tested: all endpoints return 200 in <10ms.

### Features

- No external dependencies (stdlib only)
- No caching (always live state)
- CORS headers for cross-origin access
- Serves any other `.html` file in the dashboards dir
- Clean 404 for unknown paths

### Files

- `/opt/data/agents/dashboards/dashboard-server.py` (7.5KB)
- `/opt/data/home/.hermes/scripts/dashboard-server.py` (symlink)

### Not done

- No TLS (run behind reverse proxy if exposed externally)
- No auth (anyone on the network can read state)
- No HTTPS

---

## Sub-task 3: State files to real agents

### What I did

For the 4 dept lead agents that didn't have explicit state-write directives, I added them. (The other 3 — business-analyst, management-coordinator, kiki-coach — already had them.)

### Agents updated

| Agent | Cron | State file | Schema added |
|-------|------|-----------|--------------|
| sales-pipeline | aiw-sales-pipeline-daily | sales.json | `last_run`, `leads_in_flight`, `funnel_30d`, `outreach_queue_today`, `stalled_deals`, `open_questions` |
| finance-controller | aiw-finance-controller-weekly | finance.json | `last_run`, `runway_months`, `mrr_usd`, `burn_usd_monthly`, `deals_open`, `deals_signed_this_week`, `compliance_flags`, `renewals_due_30d` |
| engineering-roster | aiw-engineering-roster-biwk | engineering.json | `last_run`, `deploys_7d`, `open_prs`, `stale_repos_7d`, `incidents_72h`, `kiki_commits_7d`, `infra_costs_monthly_usd`, `tools_pending_decision` |
| research-tracker | aiw-research-tracker-weekly | research.json | `last_run`, `thesis`, `publications_pipeline`, `courses_ready`, `courses_in_draft`, `monetization_backlog` |

### Each prompt now has the directive

> "After delivering, update `/opt/data/agents/state/X.json` with this schema. Every run MUST write state, even if nothing changed (just update `last_run`)."

### Files changed

- `/opt/data/.hermes/cron/jobs.json` — 4 prompts updated

### What this unlocks

The dashboard was showing hardcoded zeros for dept metrics because no agent was writing state. Now each dept agent has explicit instructions to write state on every run. Once they fire (next scheduled tick), the dashboard will show real numbers.

---

## Sub-task 4: 7-day history tracking

### What I built

1. **`snapshot-state.py`** — daily snapshot script that copies all state + cron + kanban + MCP count into a dated JSON file.
2. **`/opt/data/agents/state/history/`** — directory for daily snapshots + CSV summary.
3. **Daily cron** — `aiw-state-snapshot-daily` at `0 11 * * *` (11am UTC = 7am PYT).
4. **SVG sparkline chart** in the dashboard — shows last 7 days of cron health (ok vs error counts).

### Snapshot format

```json
{
  "date": "2026-08-13",
  "timestamp": "2026-08-13T18:30:00+00:00",
  "state": { /* all 9 state files at snapshot time */ },
  "cron": {"total": 19, "ok": 6, "error": 3, "pending": 10},
  "kanban": {"ready": 1},
  "mcp_count": 10
}
```

### CSV summary

```
date,cron_total,cron_ok,cron_error,cron_pending,mcp_count,kanban_total
2026-08-13,19,6,3,10,10,1
```

### Chart

- SVG sparkline, 400x80px, dark theme
- Green line: cron_ok per day
- Red dashed line: cron_error per day
- X-axis: dates
- Below chart: latest snapshot stats

### Files

- `/opt/data/agents/dashboards/snapshot-state.py` (3.5KB)
- `/opt/data/agents/state/history/2026-08-13.json` (2.8KB) — initial snapshot
- `/opt/data/agents/state/history/summary.csv` (97B) — initial
- `/opt/data/agents/dashboards/render-dashboard.py` — updated with `load_history()` + `history_chart()`

### Cron job added

- `aiw-state-snapshot-daily` (id: `e19b20b4007a`)
- Schedule: `0 11 * * *`
- Mode: no-agent (script only)

### What this unlocks

After 7 days of snapshots, the dashboard will show:
- Trend lines (cron health improving/declining)
- Capacity changes (MCP count growth)
- Activity (kanban task throughput)

---

## Sub-task 5: Interactive filters + sort

### What I added to the dashboard

1. **Search box** (top right) — type to filter rows across all tables
2. **Filter checkboxes** (above cron table) — toggle ok/err/pending/script/agent
3. **Sortable column headers** — click any `data-sort` header to sort ascending/descending
4. **Visual feedback** — hidden rows are display:none, sorted header has ▲/▼ indicator

### JavaScript

- All inline in `template.html` (no external deps)
- 60 lines of vanilla JS
- Pure DOM manipulation

### Tag-based filtering

Each cron row has `data-filter="ok script"` etc. — JS checks the dataset against the checked checkboxes.

### How it works

```javascript
// Filter rows by checkboxes
document.querySelectorAll('table tr[data-filter]').forEach(row => {
  const tags = (row.dataset.filter || '').split(' ');
  const matchesStatus = allowed.size === 0 || [...allowed].some(a => tags.includes(a));
  row.classList.toggle('hidden', !matchesStatus);
});

// Sort by column
function sortTable(th) {
  const idx = Array.from(th.parentNode.children).indexOf(th);
  rows.sort((a, b) => {
    const av = a.children[idx]?.textContent || '';
    const an = parseFloat(av), bn = parseFloat(b.children[idx]?.textContent || '');
    if (!isNaN(an) && !isNaN(bn)) return asc ? an - bn : bn - an;  // numeric
    return asc ? av.localeCompare(bv) : bv.localeCompare(av);  // text
  });
}
```

### Files

- `/opt/data/agents/dashboards/template.html` — added JS + filter UI
- `/opt/data/agents/dashboards/render-dashboard.py` — added `data-filter` to cron rows
- `/opt/data/agents/dashboards/render-dashboard.py` — fixed kanban parser (was querying non-existent `project_slug` column; now queries actual schema, shows all 12 tasks instead of 1 with parse error)

### Not done

- Filter checkboxes only on cron table (could be added to MCP, kanban, state tables)
- No date range filters (history chart could be filtered by week/month)
- No export-to-CSV button

---

## Final state

### Cron jobs (19 total)

| Job | Type | Schedule | Profile/Toolsets |
|-----|------|----------|------------------|
| site-health | script | every 15m | n/a |
| repo-ci-monitor | script | `0 11 * * *` | n/a |
| rbl-check | script | `0 12 * * *` | n/a |
| morning-brief | agent | `0 10 * * *` | default |
| ometzdental-weekly-refresh | script | `0 6 * * 1` | n/a |
| thesis-daily-tick | script+skill | `0 6 * * *` | n/a |
| thesis-weekly-review | agent+skill | `0 18 * * 0` | default |
| thesis-git-maintenance | agent+skill | `0 23 * * 0` | default |
| thesis-watchdog | agent+skill | every 15m | default |
| evo-poll-watchdog | script | every 5m | n/a |
| **aiw-business-analyst-daily** | agent+skill | `30 10 * * *` | **15 toolsets (operations)** |
| **aiw-management-coord-biwk** | agent+skill | `0 21 * * 1,4` | **15 toolsets (operations)** |
| **aiw-kiki-coach-weekly** | agent+skill | `0 21 * * 5` | **11 toolsets (people)** |
| **aiw-sales-pipeline-daily** | agent+skill | `0 13,16 * * *` | **15 toolsets (sales)** |
| **aiw-finance-controller-weekly** | agent+skill | `0 21 * * 5` | **12 toolsets (finance)** |
| **aiw-engineering-roster-biwk** | agent+skill | `0 20 * * 2,5` | **17 toolsets (engineering)** |
| **aiw-research-tracker-weekly** | agent+skill | `0 21 * * 0` | **13 toolsets (research)** |
| aiw-dashboard-refresh | script | every 15m | n/a |
| **aiw-state-snapshot-daily** | script | `0 11 * * *` | n/a |

**Bold** = new in this session or with major updates.

### Files modified

| File | Lines | Purpose |
|------|-------|---------|
| `/opt/data/agents/dashboards/template.html` | 280 | CSS + JS for interactive dashboard |
| `/opt/data/agents/dashboards/render-dashboard.py` | 350 | Generates org.html from live state |
| `/opt/data/agents/dashboards/dashboard-server.py` | 230 | HTTP server for live dashboard |
| `/opt/data/agents/dashboards/snapshot-state.py` | 95 | Daily state snapshot for history |
| `/opt/data/home/.hermes/scripts/dashboard-server.py` | symlink | |
| `/opt/data/home/.hermes/scripts/snapshot-state.py` | symlink | |
| `/opt/data/home/.hermes/scripts/render-dashboard.py` | symlink | |
| `/opt/data/.hermes/cron/jobs.json` | +1200 | 4 prompts updated + new snapshot cron |
| `/opt/data/agents/state/history/2026-08-13.json` | 1 | Initial snapshot |
| `/opt/data/agents/state/history/summary.csv` | 1 | Initial summary |

### What unlocks (what happens now)

| Trigger | What happens |
|---------|-------------|
| Tomorrow 11:00 UTC | snapshot-state.py runs → 2nd daily snapshot |
| Tomorrow 06:30 PYT | business-analyst runs → writes state/analyst.json with REAL data |
| Tomorrow 09:00 PYT | sales-pipeline runs → writes state/sales.json |
| etc. | Each dept agent populates its state file |
| After 7 days | History chart shows 7-day trend |
| When you open browser | `dashboard-server.py` shows live state with filter/sort UI |

---

## What's still pending (Tier 5 — optional)

| Action | Time | Why |
|--------|------|-----|
| Wire kanban + MCP tables to filter UI | 1 hour | Only cron table has filters now |
| Add chart to MCP count over time | 30 min | Show MCP growth as a sparkline |
| Add per-dept dashboard sub-pages | 2 hours | One per dept with dept-specific KPIs |
| Auth on HTTP server | 1 hour | Anyone on network can read state |
| HTTPS via reverse proxy | 1 hour | For external access |
| Export to CSV/PDF | 2 hours | For board reports |

---

Last updated: 2026-08-13 by Erebus. All 5 sub-tasks complete. No client work touched.

**Total files in `/opt/data/agents/dashboards/`: 5** (template.html, render-dashboard.py, dashboard-server.py, snapshot-state.py, org.html)
**Total dashboard: 22KB** (live, interactive, filterable, with 7-day history)
**Total cron jobs: 19** (7 dept lead agents, 2 dashboard refreshers, 4 thesis, 5 operations)
**Total MCP servers: 10** (all enabled, all in `/opt/data/.hermes/config.yaml`)

---

## Bonus fix discovered while verifying

While verifying the dashboard, I noticed the kanban section was showing "parse error: no such column: project_slug" — the renderer had a stale schema assumption. Fixed by querying the actual kanban table columns (id, title, status, assignee) instead. Now all 12 kanban tasks display correctly instead of just 1.

This is the same pattern as the earlier regex backtracking bug — dashboards should always be tested by browsing the rendered output, not just checking the script's exit code.