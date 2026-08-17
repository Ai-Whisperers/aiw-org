# AI Whisperers — Org Agent Handoff Matrix

> The complete map of which agent writes which state file, which consumer
> agents read that state, what triggers escalation, and which cron jobs gate
> the workflow. The single document that says "if X breaks, who breaks with it
> and who needs to know first."

Last updated: 2026-08-13 — v1 of the matrix; will grow with each new agent.

---

## 1. Agent inventory

| Agent | Department | Cron job | Schedule | State file |
|-------|-----------|----------|----------|------------|
| **business-analyst** | finance | `aiw-business-analyst-daily` | daily 06:30 PYT | `state/analyst.json` |
| **management-coordinator** | operations | `aiw-management-coord-biwk` | Mon/Thu 18:00 PYT | `state/coord.json` |
| **kiki-coach** | people | `aiw-kiki-coach-weekly` | Fri 17:00 PYT | `state/kiki.json`, `state/kiki-prep.json` |
| **sales-pipeline** | sales | `aiw-sales-pipeline-daily` | daily 08:00 PYT | `state/sales.json` |
| **finance-controller** | finance | `aiw-finance-controller-weekly` | Mon 09:00 PYT | `state/finance.json` |
| **engineering-roster** | engineering | `aiw-engineering-roster-biwk` | Wed/Sat 11:00 PYT | `state/engineering.json` |
| **research-tracker** | research | `aiw-research-tracker-weekly` | Sun 14:00 PYT | `state/research.json` |

Support agents (no state file, no handoff):
- **morning-brief** — infrastructure digest for Ivan; reads cron logs, not state files.
- **thesis-tick / thesis-watchdog** — only touches `thesis-active/` repo.

---

## 2. Producer → consumer matrix

**Read this row-by-row: if the producer fails, the consumers below are degraded.**

| State file (producer) | Consumers | What they read | What breaks if missing |
|-----------------------|-----------|----------------|------------------------|
| `analyst.json` (business-analyst) | Ivan (human, daily), management-coordinator | kpi_snapshot, decisions, open_questions | Ivan misses business health signal; coord's escalation list is incomplete |
| `coord.json` (management-coordinator) | Ivan (biweekly), business-analyst | decisions_for_ivan, open_stuck | Escalation items invisible to morning brief; analyst's "what needs Ivan" list is empty |
| `kiki.json` (kiki-coach) | Kyrian (weekly), people dept | next_topic, lessons_delivered, streak | Kyrian's learning cadence dies; people dept has no HR signal |
| `kiki-prep.json` (kiki-coach prep, pre-step) | kiki-coach | recent_commits, recent_files_touched | kiki-coach prompt is forced to use stale context |
| `finance.json` (finance-controller) | Ivan (weekly), business-analyst | runway_months, mrr_usd, deals_open | Runway/MRR signal absent from daily brief |
| `sales.json` (sales-pipeline) | Ivan (daily), finance-controller | leads_in_flight, funnel_30d, stalled_deals | Finance-controller's "deals_open" is incomplete; Ivan has no sales pulse |
| `engineering.json` (engineering-roster) | management-coordinator, Ivan (biweekly) | stale_repos_7d, deploys_7d, incidents_72h | Coord's blocker list misses infra incidents |
| `research.json` (research-tracker) | Ivan (weekly) | thesis, publications_pipeline | Thesis status invisible to brief |

**Cross-cutting**: business-analyst (daily) is the *only* agent that reads everything. It's the failure-tolerant rollup.

---

## 3. Escalation graph

When an agent detects a fire, where it lands:

```
                            ┌──────────────────────┐
                            │ Ivan (founder/CEO)   │ ← final decision-maker
                            └──────────▲───────────┘
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        │                              │                              │
┌───────┴──────┐               ┌───────┴──────┐               ┌───────┴──────┐
│ morning-brief│               │ coord.json   │               │ Kanban board │
│ 06:00 PYT    │               │ decisions_   │               │ HIGH/CRIT    │
│              │               │ for_ivan     │               │ tasks        │
└──────────────┘               └──────────────┘               └──────────────┘
        ▲                              ▲                              ▲
        │                              │                              │
   ┌────┴────┐    ┌────────┐    ┌──────┴──────┐    ┌────────┐    ┌────┴─────┐
   │ cron    │    │ sales  │    │ engineering │    │ kiki   │    │ analyst  │
   │ errors  │    │ stalled│    │ incidents   │    │ HR     │    │ business │
   │ state   │    │ deals  │    │ stale repos │    │ issues │    │ fires    │
   └─────────┘    └────────┘    └─────────────┘    └────────┘    └──────────┘
```

**Escalation rules:**

1. **CRITICAL** (data loss, payment failure, site down) — agent writes to `coord.json:decisions_for_ivan` AND pings the morning-brief cron job's output channel directly via `delivery=origin`.
2. **HIGH** (revenue-blocking, deadline imminent) — agent writes to its own state's `open_questions` AND raises a HIGH-priority kanban task.
3. **MEDIUM** (process gap, stale repo) — agent writes to its state file only. Caught by next morning-brief rollup.
4. **LOW** (cosmetic, nice-to-have) — append to next weekly report.

---

## 4. Cron dependency graph

Which jobs gate which:

```
state-snapshot-daily (02:30 PYT)
       │
       ▼
cron-heartbeat-watchdog (every 15m)
       │
       ▼
morning-brief (06:00 PYT) ── reads all state/* + cron logs
       │
       ├──▶ business-analyst (06:30 PYT) ── reads everything
       │
       ├──▶ sales-pipeline (08:00 PYT)
       │
       ▼
kiki-coach-prep (Fri 16:30 PYT) ── writes kiki-prep.json
       │
       ▼
kiki-coach (Fri 17:00 PYT) ── reads kiki-prep.json
       │
       ▼
finance-controller (Mon 09:00 PYT)
engineering-roster (Wed/Sat 11:00 PYT)
management-coordinator (Mon/Thu 18:00 PYT)
research-tracker (Sun 14:00 PYT)

cron-sync (every 5m) ── keeps .hermes/cron/jobs.json ↔ /cron/jobs.json in sync
site-health (every 15m) ── no-agent; outputs to log
repo-ci-monitor (daily 07:00 PYT) ── no-agent; checks GH Actions
rbl-check (daily 08:00 PYT) ── no-agent; trademark scrub
evo-poll-watchdog (every 30m) ── no-agent; monitors evolution-api
aiw-dashboard-refresh (every 15m) ── no-agent; re-renders org.html
aiw-dashboard-snapshot (daily 02:00 PYT) ── no-agent; appends history.csv
```

**Critical-path**: if `state-snapshot-daily` fails, rollback is impossible. If `cron-sync` fails for >15min, cron-config drift returns (the 2026-08-13 outage).

---

## 5. Failure propagation scenarios

| Scenario | First sign | Cascades to | Detection agent |
|----------|-----------|-------------|-----------------|
| Cron-config drift | jobs randomly succeeding/failing | all jobs | cron-heartbeat-watchdog |
| State file corrupted | dashboard render errors | business-analyst | validate-state.py |
| Gateway down | no cron runs | all agents | cron-heartbeat-watchdog (heartbeat stale) |
| LLM proxy 4xx/5xx | single job error | depends on which job | cron-heartbeat-watchdog |
| Kanban DB lock | kanban writes fail | management-coordinator | engineering-roster |
| Thesis-active venv broken | thesis-tick error | research-tracker | cron-heartbeat-watchdog |
| GH CLI rate-limited | analyst brief incomplete | business-analyst | business-analyst |

---

## 6. Onboarding a new agent

Checklist (must pass before adding to production cron):

- [ ] PROMPT.md exists under `/opt/data/agents/<name>/`
- [ ] State file path decided; JSON Schema written under `/opt/data/agents/schemas/<name>.schema.json`
- [ ] `validate-state.py` returns OK on initial seed
- [ ] Cron job created with `provider=custom:litellm model=primary` (see #2 P1#3 lesson)
- [ ] Output contract followed (outbox file, 150-300 words, no emoji headlines)
- [ ] At least one row added to this matrix's §1 + §2
- [ ] Rollback path: snapshot of initial state lives in `/opt/data/agents/state/history/snapshots/`
- [ ] Health check: `health.sh` extended to include the new agent

---

## 7. Cross-references

- Source-of-truth config: `/opt/data/.hermes/config.yaml`
- Cron jobs: `/opt/data/.hermes/cron/jobs.json` (canonical) ↔ `/opt/data/cron/jobs.json` (gateway-read)
- State schemas: `/opt/data/agents/schemas/`
- Validators: `/opt/data/agents/scripts/validate-state.py`, `/opt/data/scripts/cron-heartbeat-check.sh`
- Snapshot history: `/opt/data/agents/state/history/snapshots/`
- Dashboard: http://127.0.0.1:8765 (token required)