# 01 — Operations Playbook (Reference)

> Reference playbook for the Operations department. This is the "1 version good" — every other playbook derives from this template.
> **Last updated**: 2026-08-14

---

## Operations — Department Charter

**Mission**: Keep the agent platform itself alive, healthy, observable. Operations is the **objetivo-department** — it doesn't ship products, it makes sure every other department can ship.

**Head**: Ivan
**Cross-cutting concerns**: AI Ops (Tier 2), BizOps (Tier 2)

---

## Roles (8 roles)

| # | Role | Tier | Owner | Status |
|---|------|------|-------|--------|
| 1.1 | Operations Lead | 🟢 T1 | Ivan | active |
| 1.2 | Repo Steward | 🟢 T1 | sub-agent | planned |
| 1.3 | Asset Tracker | 🟢 T1 | sub-agent | planned |
| 1.4 | Vendor Coordinator | 🟢 T1 | Ivan | manual |
| 1.5 | Compliance Watchdog | 🟢 T1 | sub-agent | planned |
| 1.6 | Watchdog Engineer | 🟢 T1 | Kiki | technical |
| 1.7 | BizOps Specialist | 🟡 T2 | agent | planned |
| 1.8 | Chief Operating Officer (COO) | 🟠 T3 | future hire | deferred |

---

## Sub-agents (Tier 2)

| Agent | Cadence | Mission |
|-------|---------|---------|
| `management-coordinator` | Mon+Thu 17:00 PYT | Cross-repo stuck/stale/PR review |
| `business-analyst` | Daily 06:30 PYT | Pipeline/revenue/sites snapshot |
| `kiki-coach` | Fri 17:00 PYT | Weekly lesson for Kyrian |
| `ai-ops-coordinator` (NEW) | Daily 09:00 PYT | Agent layer health, eval gates, drift |
| `bizops-tracker` (NEW) | Weekly | Cross-functional analytics, OKRs |
| `compliance-monitor` (NEW) | Weekly | Compliance program monitoring |
| `source-curator` (NEW) | Weekly | source-materials/ curation |
| `founder-bandwidth-watchdog` (NEW) | Weekly | Burnout signal detection |

---

## Tooling (per role)

### Operations Lead (Ivan)
- **Communication**: Telegram (Erebus-test DM), WhatsApp (595981324569)
- **Project tracking**: Kanban DB at `/opt/data/kanban/`
- **Decision docs**: `/opt/data/agents/DECISIONS-2026-Q3.md`

### Repo Steward
- **Default**: GitHub CLI (`gh`)
- **OSS alt**: `gitea` (self-hosted)
- **Premium**: GitHub Enterprise

### Asset Tracker
- **Default**: Plain JSON inventory + spreadsheet
- **OSS alt**: Snipe-IT (asset management)
- **Premium**: Jamf (Dispositivo personal-focused)

### Vendor Coordinator
- **Default**: Spreadsheet + email
- **OSS alt**: FreeScout (help desk) + spreadsheet
- **Premium**: Vendr (procurement-specific)

### Compliance Watchdog
- **Default**: `trademark-compliance-scrub` skill (existing)
- **OSS alt**: OPA (Open Policy Agent) for policy-as-code
- **Premium**: Vanta (compliance automation)

### Watchdog Engineer (Kiki)
- **Default**: Cron + bash scripts (`/opt/data/agents/scripts/`)
- **OSS alt**: Healthchecks.io (heartbeat monitoring)
- **Premium**: Datadog (full observability)

---

## SOPs (Standard Operating Procedures)

### Daily
- 06:00: morning-brief cron (Ivan wake-up brief)
- 06:30: business-analyst cron (pipeline/revenue/sites snapshot)
- Every 15 min: health.sh watchdog
- Every 15 min: site-health cron (HTTP checks on live sites)
- Every 15 min (off-hours) / 30 min (on-hours): cron-heartbeat
- Every 15 min: validate-state.py (state schema check)
- Every 6 hours: state-snapshot.sh (atomic snapshot)
- Hourly: cost-cap (per-agent daily spend check)

### Weekly
- Mon+Thu 17:00: management-coordinator (cross-repo review)
- Fri 17:00: kiki-coach (lesson for Kyrian)
- Weekly: ai-ops-coordinator (NEW), bizops-tracker (NEW), compliance-monitor (NEW), source-curator (NEW), founder-bandwidth-watchdog (NEW)

### Monthly
- Quarterly: business review (every 90 days — see Phase 9 milestone)

---

## Hard stops (Operations dept)

| Action | Authority | Hard-stop ref |
|--------|-----------|---------------|
| Restart a stuck cron job | Operations agent | logged |
| Pause an agent emitting noise | Operations agent → flag Ivan | next brief |
| Delete old outbox file (>30d) | Operations agent | logged |
| Edit `ORG-AGENTS.md` | Ivan only | hard rule |
| Add/remove department | Ivan + Kiki together | hard rule |
| Force-push to any repo | Ivan | hard rule |

---

## Handoff matrix (Operations)

| From → To | Trigger | Mechanism |
|-----------|---------|-----------|
| Operations → Finance | Vendor cost change | Append to `finance.json` `infra_costs_monthly_usd` |
| Operations → Engineering | Repo stale > 30d | Surface in coord.json + flag in GH issue |
| Operations → Sales | New live site deployed | Add to sales.json funnel_30d |
| Operations → Research | Thesis tick fails | Alert via heartbeat |

---

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

---

## Escalation triggers

- Cron job in error state > 24h → page Ivan
- Repo stale > 30d with active issues → flag in coord + tag GH issue
- Org-pulse shows > 50% drop in any KPI → emergency brief

---

## Failure mode

If health.sh reports > 2 agents stale → Operations opens an issue and pages Ivan.

---

## Promotion triggers (Tier 3 depts that become own dept)

- **Customer Success**: 5+ recurring clients → split from Sales
- **Compliance Officer**: First EU client → split from Finance (named role already)
- **Chief of Staff**: Ivan coord hours > 50/week → split from Operations
- **COO**: When Operations dept > 5 people

---

## Cultural artifacts (PRESERVE)

Per `06-people-culture.md` lines 68-75 (cross-reference), Operations owns:
- First signed contract in new ICP → LinkedIn post (Sales drafts, Ivan approves)
- Major deploy win → Engineering notes

---

## See also

- `/opt/data/agents/departments/01-operations.md` (canonical charter)
- `/opt/data/agents/ORCHESTRATION.md` (cron schedule grid)
- `/opt/data/agents-v2/DECISIONS-2026-Q3.md` (ratified decisions)
- `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md` (3-layer model)
