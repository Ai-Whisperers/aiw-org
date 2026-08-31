# 00-INDEX — Playbook Catalog Master Index

> Master index of all per-department playbooks. Master cross-dept table.
> **Last updated**: 2026-08-14

---

## Reading guide

- 01-06: per-department playbooks
- 07: cross-cutting concerns (AI Ops, BizOps, RevOps)
- 08: deferred Tier-3 departments (12-15 with promotion triggers)

---

## Master cross-department table

| # | Dept / Function | Head | Tier 1 agents | Tier 2 agents | Roles |
|---|-----------------|------|---------------|---------------|-------|
| 01 | **Operations** | Ivan | management-coordinator, business-analyst, kiki-coach | ai-ops-coordinator, bizops-tracker, compliance-monitor, source-curator, founder-bandwidth-watchdog | 8 |
| 02 | **Sales & Growth** | Ivan | sales-pipeline | proposal-drafter, lead-enrichment, marketing-content-producer, multimedia-producer, customer-health-scorer | 18 |
| 03 | **Engineering & Delivery** | Kiki | engineering-roster | devops-monitor, qa-automation-runner, security-watchdog, ai-safety-engineer | 24 |
| 04 | **Finance & Legal** | Ivan | finance-controller | accounting-automation, tax-receipt-tracker, procurement-tracker, compliance-monitor | 14 |
| 05 | **Research & Education** | Ivan | research-tracker | citation-checker, thesis-tracker, course-producer, source-curator | 12 |
| 06 | **People & Culture** | Ivan + Kiki | kiki-coach | founder-bandwidth-watchdog | 8 |
| 07 | **Cross-cutting (Tier 2)** | various | (cross-cutting) | ai-ops, bizops, revops, compliance (named role) | 6 (dedicated) + 4 (embedded) |
| 08 | **Deferred Tier-3 depts** | (TBD when triggered) | (none yet) | (none yet) | ~15 |
| | **TOTAL** | | **7** | **~14 + 8 cross-cutting** | **~135** |

---

## Role count by department

| Department | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Total |
|------------|--------|--------|--------|--------|-------|
| Operations | 6 | 1 | 1 | 0 | 8 |
| Finance & Legal | 6 | 4 | 4 | 0 | 14 |
| Sales & Growth | 5 | 6 | 7 | 0 | 18 |
| Engineering | 7 | 2 | 11 | 4 | 24 |
| Research | 5 | 4 | 3 | 0 | 12 |
| People | 3 | 0 | 2 | 3 | 8 |
| Cross-cutting | 1 | 3 | 2 | 0 | 6 (dedicated) |
| Deferred Tier-3 | 0 | 0 | 15 | 0 | 15 |
| Tier 4 enterprise | 0 | 0 | 0 | 5 | 5 |
| **TOTAL** | **~36** | **~31** | **~45** | **~12** | **~124** |

---

## Agent count by tier

| Tier | Count | Cadence |
|------|-------|---------|
| Tier 1 (active now) | 7 lead agents | cron-driven |
| Tier 2 (sub-agents) | ~14 | mixed |
| Tier 2 (cross-cutting) | ~8 | weekly |
| Tier 3 (deferred) | ~15 | not built |
| **TOTAL at buildout** | **~45** | |

---

## Decision matrix summary

- **Tier 1 staffed**: 36 roles (Ivan + Kiki + ~30 sub-agent roles)
- **Tier 2 hired**: 31 roles (when next FTE)
- **Tier 3 hire**: 45 roles (at 5+ clients, $50K MRR, etc.)
- **Tier 4 enterprise**: 12 roles (at 50+ people)

---

## State files (one per agent)

11 SQLite DBs at `/opt/data/db/`:
- analyst, coord, kiki, kiki-prep, finance, sales, engineering, research, people (9 active)
- 2 more for new sub-agents when they ship

---

## Cron jobs (24 currently, growing to ~30+)

Cadence map (per `ORCHESTRATION.md`):
- Daily 06:30 PYT: business-analyst
- Mon+Thu 17:00 PYT: management-coordinator
- Fri 17:00 PYT: kiki-coach
- Fri 18:00 PYT: finance-controller
- Tue+Fri 17:00 PYT: engineering-roster
- Sun 18:00 PYT: research-tracker
- Daily 12:00 PYT: sales-pipeline
- Watchdogs: health.sh (every 15m), site-health (15m), state-validate (15m), state-snapshot (6h), cron-heartbeat (15m off / 30m on), db-snapshot (daily 02:00)

---

## Cross-references

- `/opt/data/agents-v2/PLAN-v5.md` — master plan
- `/opt/data/agents-v2/DECISIONS-2026-Q3.md` — ratified decisions
- `/opt/data/agents-v2/ROLES-INVENTORY.md` — full ~135 role catalog
- `/opt/data/agents/departments/ORG-AGENTS.md` — constitution (v0.1.0, will be v0.2.0 in Phase 8)
- `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md` — 3-layer model
