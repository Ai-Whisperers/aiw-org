# Tracker — DEMIURGE-079

## Phase 1 — Operations sub-agent souls (Tier 1)

| Task | Status |
|------|--------|
| Create `demiurge/agents/management-coordinator/` soul (agent.yaml, PROMPT.md, repo-manifest.yaml) | completed |
| Add emit_signal steps: ops-stale-repo-count, ops-decision-queue-depth, ops-cycle-time-days | completed |
| Update state schema to SQLite `/opt/data/db/coord.db` | completed |
| Create `demiurge/agents/business-analyst/` soul | completed |
| Add emit_signal step: ops-cron-error-count | completed |
| Create `demiurge/agents/bizops-tracker/` soul | completed |
| Fix parent_spec → `departments/operations/department.md` | completed |
| Add emit_signal steps: 8 weekly/monthly/quarterly KPIs | completed |
| Create `departments/operations/okrs.yaml` | completed |
| Update `department.md` — 3 roles skeleton → active | completed |

## Phase 2 — Tier 2 cross-cutting dept shells

| Task | Status |
|------|--------|
| Create `departments/ai-ops/department.md` | completed |
| Create `departments/ai-ops/signals.yaml` | completed |
| Create `departments/ai-ops/cadences.md` | completed |
| Create `demiurge/agents/ai-ops-coordinator/` soul | completed |
| Create `departments/compliance/department.md` | completed |
| Create `departments/compliance/signals.yaml` | completed |
| Create `departments/compliance/cadences.md` | completed |
| Create `demiurge/agents/compliance-monitor/` soul | completed |

## Phase 3 — Cadence authority + alignment

| Task | Status |
|------|--------|
| Resolve schedule authority (legacy wins over DEMIURGE-075 drafts) | completed |
| Update `departments/operations/cadences.md` — all 5 agents + Kronos | completed |
| Add PYT column to cadences.md | completed |
| Register ai-ops-coordinator (daily 09:00 PYT) | completed |
| Register compliance-monitor (Mon 08:00 PYT) | completed |

## Phase 4 — Doc-impl drift fixes

| Task | Status |
|------|--------|
| Normalize `sources/operations/catalog.yaml` signal IDs to hyphen convention | completed |
| Add 5 agents to `demiurge/agents/README.md` | completed |

## Phase 5 — Ticket closure

| Task | Status |
|------|--------|
| Update `tickets/INDEX.md` | completed |
| Mark ticket complete | completed |
