# Context — DEMIURGE-079

**Status**: COMPLETED
**Focus**: Migrate 5 legacy Operations agents to full DEMIURGE standard

## Background

Gap analysis (2026-08-29, `/Grimoire/jp-analyze-gaps`) identified 18 findings (11 High, 6 Medium, 1 Low) across the Operations legacy agent scope. DEMIURGE-075/076 delivered the department skeleton and Kronos lead agent but explicitly deferred sub-agent soul migration:

> "Legacy agents in `agents-prompts/`: management-coordinator, business-analyst, bizops-tracker, ai-ops-coordinator, compliance-monitor. Promoted to skeleton roles with signals and cadences; router wiring deferred to DEMIURGE-076." — DEMIURGE-075 context.md

DEMIURGE-076 completed Kronos + router inbound wiring only. Sub-agent souls, Tier 2 dept shells, signal emission contracts, and cadence reconciliation remain open.

## Current state

| Artifact | Status |
|----------|--------|
| `departments/operations/department.md` | Active — 4 ops roles at `skeleton` |
| `departments/operations/signals.yaml` | Complete — 15 KPI + 4 cross-dept signals |
| `departments/operations/cadences.md` | Partial — 3 of 5 legacy agents; no PYT column; schedules diverge from legacy |
| `demiurge/agents/kronos-operations-lead/` | Complete |
| `demiurge/agents/management-coordinator/` | **Missing** |
| `demiurge/agents/business-analyst/` | **Missing** |
| `demiurge/agents/bizops-tracker/` | **Missing** |
| `demiurge/agents/ai-ops-coordinator/` | **Missing** |
| `demiurge/agents/compliance-monitor/` | **Missing** |
| `departments/ai-ops/` | **Missing** |
| `departments/compliance/` | **Missing** |
| `departments/operations/okrs.yaml` | **Missing** (deferred from DEMIURGE-075) |

## Legacy agent coverage map

| Legacy prompt | DEMIURGE role | Tier | Signals owned | Cadence (legacy) |
|---------------|---------------|------|---------------|------------------|
| `management-coordinator` | ops-management-coordinator | 1 | ops-stale-repo-count, ops-decision-queue-depth, ops-cycle-time-days | Mon+Thu 17:00 PYT |
| `business-analyst` | ops-business-analyst | 1 | ops-cron-error-count | Daily 06:30 PYT |
| `bizops-tracker` | ops-bizops-tracker | 1 | ops-okr-completion-pct, ops-vendor-renewal-30d, ops-cross-dept-blocker-count, ops-decision-latency-days, ops-burn-rate, ops-cost-per-transaction, ops-tool-sprawl-count, ops-okr-reset | Sun 17:00 PYT |
| `ai-ops-coordinator` | (ai-ops dept) | 2 | ops-incident-open-count, ops-agent-health-anomaly (outbound) | Daily 09:00 PYT |
| `compliance-monitor` | (compliance dept) | 2 | ops-compliance-flag-count (outbound) | Mon 08:00 PYT |

## Gap findings bundled in this ticket

| ID | Severity | Finding | Phase |
|----|----------|---------|-------|
| D2-1 | High | management-coordinator soul missing | 1 |
| D2-2 | High | business-analyst soul missing | 1 |
| D2-3 | High | bizops-tracker soul missing | 1 |
| D2-4 | High | ai-ops-coordinator soul + ai-ops dept shell missing | 2 |
| D2-5 | High | compliance-monitor soul + compliance dept shell missing | 2 |
| D2-6 | Medium | ai-ops + compliance absent from cadences.md | 3 |
| D2-7 | Medium | 5 agents absent from README.md index | 4 |
| D2-8 | Medium | okrs.yaml missing | 1 |
| D2-9 | Low | cadences.md missing PYT column | 3 |
| D4-1 | High | management-coordinator schedule diverges | 3 |
| D4-2 | High | business-analyst schedule diverges | 3 |
| D4-3 | High | bizops-tracker schedule diverges (Sun vs Fri) | 3 |
| D4-4 | High | bizops-tracker parent_spec points to cross-cutting playbook | 1 |
| D4-5 | High | management-coordinator has no emit_signal in procedure | 1 |
| D4-6 | High | business-analyst has no emit_signal in procedure | 1 |
| D4-7 | Medium | catalog.yaml uses underscores; signals.yaml uses hyphens | 4 |
| D4-8 | Medium | management-coordinator state schema still JSON path | 4 |
| D4-9 | Medium | okrs.yaml not created (DEMIURGE-075 miss) | 1 |

## Reference patterns

- Sub-agent soul: `demiurge/agents/calliope-content-producer/` (agent.yaml + PROMPT.md + repo-manifest.yaml)
- Dept shell: `departments/marketing/` (department.md + signals.yaml + cadences.md)
- Lead delegation: `demiurge/agents/kronos-operations-lead/PROMPT.md` — delegates to management-coordinator, business-analyst, bizops-tracker

## Integration points

- Router: no new dispatch/timing rules needed — inbound ops signals wired in DEMIURGE-076
- Kronos: sub-agents feed KPI signals that Kronos aggregates into `dept-kpi-signals` rollup
- Taxonomy: `ai-ops` and `compliance` remain `skeleton` in `department-taxonomy-v1.md` unless explicitly promoted

## Constraints

- Follow Marketing migration pattern (DEMIURGE-028/029/030) for soul file structure
- Do not modify router wiring — already complete from DEMIURGE-076
- Legacy `agents-prompts/` files: keep until persona constructor (DEMIURGE-072) supersedes them
- Schedule authority: legacy prompts + constitution take precedence over DEMIURGE-075 cadences.md drafts

## Next steps

1. Resolve schedule authority table (plan.md) — update cadences.md to legacy schedules
2. Create 3 Tier 1 sub-agent souls with emit_signal contracts
3. Create 2 Tier 2 dept shells + 2 cross-cutting agent souls
4. Create okrs.yaml; normalize catalog.yaml signal IDs
5. Update department.md role statuses, README.md index
6. Mark ticket complete in INDEX.md
