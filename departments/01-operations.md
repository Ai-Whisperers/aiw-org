# Department 1 — Operations

**Head**: Ivan
**Lead agent**: `management-coordinator` (Mon/Thu 17:00 PYT)
**Version**: 0.2.0
**Last updated**: 2026-08-14

---

## Mission

Keep the agent platform itself alive, healthy, observable. Operations is the **meta-department** — it doesn't ship products, it makes sure every other department can ship.

## What this department owns

- Cron job health (liveness, error states, schedule collisions)
- Agent outbox freshness (`/opt/data/agents/scripts/health.sh`)
- Cross-repo work tracking (issues, PRs, stale repos)
- The org constitution itself (`ORG-AGENTS.md`) — surfaced in briefs when it changes
- State file hygiene (rolling caps respected, no orphan entries)
- **NEW v0.2.0**: Storage architecture (git repos + SQLite per agent)
- **NEW v0.2.0**: AI Ops (agent layer health)

## What this department does NOT own

- Production infra uptime — that's Engineering
- Thesis state — that's Research
- Lead pipeline — that's Sales

## Decision rights (v0.2.0)

| Action | Authority |
|--------|-----------|
| Restart a stuck cron job | Operations agent (logged) |
| Pause an agent emitting noise | Operations agent → flag Ivan in next brief |
| Delete an old outbox file (>30d) | Operations agent (logged) |
| Edit `ORG-AGENTS.md` | Ivan only |
| Add/remove department | Ivan + Kiki together |
| **NEW**: Backup state DB | Operations agent (daily) |
| **NEW**: Update storage architecture | Ivan only |

## Sub-roles (v0.2.0 — added from ROLES-INVENTORY.md)

| # | Role | Tier | Owner |
|---|------|------|-------|
| 1.1 | Operations Lead | 🟢 T1 | Ivan |
| 1.2 | Repo Steward | 🟢 T1 | sub-agent |
| 1.3 | Asset Tracker | 🟢 T1 | sub-agent |
| 1.4 | Vendor Coordinator | 🟢 T1 | Ivan |
| 1.5 | Compliance Watchdog | 🟢 T1 | sub-agent |
| 1.6 | Watchdog Engineer | 🟢 T1 | Kiki |
| 1.7 | BizOps Specialist | 🟡 T2 | agent (planned) |
| 1.8 | COO | 🟠 T3 | future hire |

## Sub-agents (v0.2.0)

| Agent | Cadence | Status |
|-------|---------|--------|
| `management-coordinator` | Mon+Thu 17:00 PYT | active |
| `business-analyst` | Daily 06:30 PYT | active |
| `kiki-coach` | Fri 17:00 PYT | active |
| **NEW** `ai-ops-coordinator` | Daily 09:00 PYT | planned |
| **NEW** `bizops-tracker` | Weekly | planned |
| **NEW** `compliance-monitor` | Weekly | planned (cross-cutting) |
| **NEW** `source-curator` | Weekly | planned (Research dept) |
| **NEW** `founder-bandwidth-watchdog` | Weekly | planned (People dept) |

## Inputs the lead agent reads (v0.2.0)

1. `hermes cron list` — every cron job's status
2. `/opt/data/agents/scripts/health.sh` output — agent outbox freshness
3. `gh api search/issues?q=org:Ai-Whisperers+is:open+is:issue` — issue backlog
4. `gh api orgs/Ai-Whisperers/repos --paginate` — repo push activity
5. `/opt/data/thesis-active/THESIS_STATE.md` — for the thesis one-liner
6. Prior `/opt/data/agents/state/coord.json`
7. **NEW**: `/opt/data/backups/db/` — backup freshness
8. **NEW**: `/opt/data/agents-v2/cron-heartbeat-alerts.log` — recent alerts

## Cadence (v0.2.0)

| Time (PYT) | What |
|------------|------|
| 06:00 | morning-brief (existing) |
| 06:30 | business-analyst brief |
| Every 15 min | health.sh watchdog |
| Every 15 min (off-hours) / 30 min (on-hours) | cron-heartbeat |
| Every 15 min | state-validate |
| Every 6 hours | state-snapshot |
| Hourly | cost-cap |
| Daily 02:00 | db-snapshot |
| 09:00 | **NEW** ai-ops-coordinator |
| Mon+Thu 17:00 | management-coordinator |
| Tue+Fri 17:00 | engineering-roster (handoff) |
| Fri 17:00 | kiki-coach |
| Sat/Sun weekly | bizops-tracker, compliance-monitor, source-curator, founder-bandwidth-watchdog |

## Escalation triggers (v0.2.0)

- Cron job in error state > 24h → page Ivan immediately
- Repo stale > 30d with active issues → flag in brief + tag GH issue
- Org-pulse shows > 50% drop in any KPI → emergency brief
- **NEW**: Backup missing for > 24h → alert
- **NEW**: Per-agent cost > $1/day → halt agent + alert
- **NEW**: Hard-stop wrapper blocked an action → log to escalations table

## Failure mode

If `health.sh` reports > 2 agents stale → Operations opens an issue in agents repo (or scratchpad) and pings Ivan directly. Don't wait for next scheduled brief.

## State schema (`state/coord.json`)

```json
{
  "last_run": null,
  "open_stuck": [],
  "stale_repos": [],
  "decisions_for_ivan": []
}
```

Caps: open_stuck ≤ 10, decisions_for_ivan ≤ 3.

## Storage architecture (v0.2.0)

Per `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md`:
- State lives in SQLite at `/opt/data/db/coord.db`
- Per-agent git repos at `/opt/data/git-repos/aiw-agents-management-coordinator/`
- Daily backups at `/opt/data/backups/db/{date}/`

## Cross-references

- Constitution: `/opt/data/agents/departments/ORG-AGENTS.md` (v0.2.0)
- Playbook: `/opt/data/agents-v2/playbooks/01-operations.md`
- Storage: `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md`
- Decisions: `/opt/data/agents/DECISIONS-2026-Q3.md`
- Threat model: `/opt/data/agents-v2/THREAT-MODEL.md`
- Failure modes: `/opt/data/agents-v2/FAILURE-MODES.md`

---

## CHANGELOG

- v0.2.0 (2026-08-14): added Sub-roles table, Sub-agents table (incl. 4 new Tier 2), Inputs (storage layer), Cadence (expanded), Escalation (storage/cost/hard-stop), Failure mode (expanded), Storage architecture, Cross-references.
- v0.1.0 (2026-08-13): initial ratification.
