# Health Dashboard — Per-Department Health Scoring

> **Phase 8 Area #5** | Operations dept | Owner: ai-ops-coordinator + business-analyst
> **Date**: 2026-09-01
> **Status**: First calculation; refresh weekly via cron

---

## Per-department health score

Computed from 5 dimensions, each 0-20:

| Dept | Activity | KPI freshness | Agent count | Monitor coverage | Cron health | **Total (0-100)** |
|------|----------|---------------|-------------|------------------|-------------|--------------------|
| 01-operations | 18 | 16 | 20 | 20 | 16 | **90** |
| 02-finance-legal | 8 | 4 | 12 | 20 | 4 | **48** |
| 03-sales-growth | 6 | 4 | 14 | 20 | 4 | **48** |
| 04-engineering | 20 | 18 | 20 | 20 | 18 | **96** |
| 05-research-education | 12 | 8 | 14 | 16 | 8 | **58** |
| 06-people-culture | 6 | 4 | 8 | 12 | 4 | **34** |
| board-of-directors | 8 | 6 | 6 | 8 | 6 | **34** |

---

## How scores were computed

### 01-operations: 90/100

- **Activity** (18): 8 PROMPTs + 6 sub-agents + monitor-notes dir, recent commits
- **KPI freshness** (16): state files updated within 24h, kpi-stack.yaml present
- **Agent count** (20): 6 sub-agents + bizops-tracker + founder-bandwidth-watchdog = 8
- **Monitor coverage** (20): PROMPT-monitor.md exists for all 6 sub-agents + dept-lead
- **Cron health** (16): 1 job in error (acceptable; not all)

### 04-engineering: 96/100

- **Activity** (20): 10 PROMPTs + 10 sub-agents; recent commits daily
- **KPI freshness** (18): kpi-stack.yaml + signals active
- **Agent count** (20): 10 sub-agents
- **Monitor coverage** (20): 10/10 PROMPT-monitor.md
- **Cron health** (18): 0 errors

### 02-finance-legal: 48/100

- **Activity** (8): 4 PROMPTs + 2 sub-agents; sparse commits
- **KPI freshness** (4): state/finance.json `last_run: null` (no recent data)
- **Agent count** (12): 2 sub-agents (hermes-finance-lead, demeter-finance-controller)
- **Monitor coverage** (20): PROMPT-monitor.md exists for both sub-agents
- **Cron health** (4): 5 of 6 cron errors are finance-related (token-plan exhaustion)

### 03-sales-growth: 48/100

- **Activity** (6): 4 PROMPTs + 4 sub-agents; pipeline DEAD
- **KPI freshness** (4): state/sales.json shows 0 leads, 0 deals
- **Agent count** (14): 4 sub-agents + 4 atomic-layer agents (apollo, cadmus, metis, hermes-router-revenue)
- **Monitor coverage** (20): PROMPT-monitor.md exists
- **Cron health** (4): 1 job in error (aiw-sales-pipeline-monitor)

### 05-research-education: 58/100

- **Activity** (12): 5 PROMPTs + 4 sub-agents; thesis active
- **KPI freshness** (8): research state present but stale
- **Agent count** (14): 4 sub-agents
- **Monitor coverage** (16): 4/5 PROMPT-monitor.md
- **Cron health** (8): some jobs in error

### 06-people-culture: 34/100 🔴

- **Activity** (6): 1 PROMPT + 2 sub-agents; minimal activity
- **KPI freshness** (4): state/people.json `last_run: null`
- **Agent count** (8): 2 sub-agents (people-hr, founder-bandwidth-watchdog)
- **Monitor coverage** (12): partial
- **Cron health** (4): aiw-people-hr-weekly has wrong provider

### board-of-directors: 34/100 🔴

- **Activity** (8): 1 PROMPT + no sub-agents
- **KPI freshness** (6): state not tracked
- **Agent count** (6): only the dept-lead itself
- **Monitor coverage** (8): partial
- **Cron health** (6): quarterly cron (no recent fire)

---

## The 4 departments below 60

| Dept | Score | Top issue |
|------|-------|-----------|
| 06-people-culture | 34 | Wrong provider in cron (config drift) |
| board-of-directors | 34 | No sub-agents (doctrinal: not needed for governance) |
| 02-finance-legal | 48 | Token-plan exhaustion on weekly stack |
| 03-sales-growth | 48 | Pipeline dead (sales.json empty) |

---

## Recommendations

1. **Fix `minimax-plan` provider** in `aiw-people-hr-weekly` cron → bumps People to 50
2. **Spread finance Sunday-evening crons** → bumps Finance to 64
3. **Sales revival** (already a Phase 8 priority) → will bump Sales as soon as pipeline flows
4. **Board**: low score is doctrinal (governance, not operations) — accept

---

**Cross-references**:
- `state/cron-error-watchdog.json`
- `demiurge/kpi/*-stack.yaml` (per-dept KPI stacks)
- `analysis/PHASE-7-dept-research/01-operations-research-areas.md` Area #5
- `analysis/L1-AUTONOMOUS-PRECHECKS-2026-09.md`

