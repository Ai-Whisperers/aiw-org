# DEMIURGE-079: Migrate Operations legacy agents to DEMIURGE standard

**Sprint**: Phase 2 — Reference Department (Operations)
**Size**: 120m
**Owner**: AI

## Objective

Complete Operations department buildout to full DEMIURGE standard by migrating all 5 legacy `agents-prompts/` agents into `demiurge/agents/` souls, activating Tier 2 shells for `ai-ops` and `compliance`, and resolving doc-impl drift surfaced in the gap analysis (DEMIURGE-074/075/076 follow-up).

DEMIURGE-075 delivered dept skeleton + signals; DEMIURGE-076 delivered Kronos lead + router inbound wiring. This ticket closes the remaining gap: sub-agent souls, signal emission contracts, cadence authority, and Tier 2 cross-cutting dept shells.

## Inputs

- Gap analysis (2026-08-29) — 18 findings across `impl` + `docs` dimensions
- `agents-prompts/management-coordinator.md`, `business-analyst.md`, `bizops-tracker.md`, `ai-ops-coordinator.md`, `compliance-monitor.md`
- `constitution/01-operations.md` — legacy constitution (v0.2.0)
- `departments/operations/department.md`, `signals.yaml`, `cadences.md`
- `sources/operations/catalog.yaml`, `gaps.md`
- Reference pattern: `demiurge/agents/calliope-content-producer/` + `departments/marketing/`

## Output

```
demiurge/agents/
├── management-coordinator/     # agent.yaml, PROMPT.md, repo-manifest.yaml
├── business-analyst/
├── bizops-tracker/
├── ai-ops-coordinator/
└── compliance-monitor/

departments/
├── operations/
│   ├── okrs.yaml               # OKR definitions (moved from state/bizops.json)
│   └── cadences.md             # updated: all 5 agents + PYT column
├── ai-ops/
│   ├── department.md
│   ├── signals.yaml
│   └── cadences.md
└── compliance/
    ├── department.md
    ├── signals.yaml
    └── cadences.md

sources/operations/catalog.yaml  # signal IDs normalized to hyphen convention
demiurge/agents/README.md          # 5 agents added to index
departments/operations/department.md # role statuses updated skeleton → active
```

## Complexity Assessment

**Track**: Complex Implementation

**Rationale**: 5 agent soul migrations, 2 new Tier 2 dept shells, cadence reconciliation across 5 agents, signal emission contract updates in PROMPTs, okrs.yaml creation, catalog ID normalization. 20+ files touched across 4 directories.

## Acceptance criteria

### Phase 1 — Operations sub-agent souls (Tier 1)

- [ ] `demiurge/agents/management-coordinator/` — agent.yaml, PROMPT.md, repo-manifest.yaml
- [ ] `demiurge/agents/business-analyst/` — agent.yaml, PROMPT.md, repo-manifest.yaml
- [ ] `demiurge/agents/bizops-tracker/` — agent.yaml, PROMPT.md, repo-manifest.yaml
- [ ] Each soul references `departments/operations/department.md` as `parent_spec`
- [ ] Each PROMPT includes `emit_signal` step for assigned KPIs in `signals.yaml`:
  - management-coordinator → `ops-stale-repo-count`, `ops-decision-queue-depth`, `ops-cycle-time-days`
  - business-analyst → `ops-cron-error-count`
  - bizops-tracker → `ops-okr-completion-pct`, `ops-vendor-renewal-30d`, `ops-cross-dept-blocker-count`, `ops-decision-latency-days`, `ops-burn-rate`, `ops-cost-per-transaction`, `ops-tool-sprawl-count`, `ops-okr-reset`
- [ ] `departments/operations/department.md` — ops-management-coordinator, ops-business-analyst, ops-bizops-tracker status `active`
- [ ] `departments/operations/okrs.yaml` — OKR structure definitions (quarterly objectives + key results)

### Phase 2 — Tier 2 cross-cutting dept shells

- [ ] `departments/ai-ops/department.md` — mission, roles, signal tables (feeds `ops-agent-health-anomaly`, `ops-incident-open-count`)
- [ ] `departments/ai-ops/signals.yaml` — outbound cross_dept signals to operations
- [ ] `departments/ai-ops/cadences.md` — ai-ops-coordinator daily 09:00 PYT
- [ ] `demiurge/agents/ai-ops-coordinator/` — agent.yaml, PROMPT.md, repo-manifest.yaml
- [ ] `departments/compliance/department.md` — mission, roles, signal tables (feeds `ops-compliance-flag-count`)
- [ ] `departments/compliance/signals.yaml` — outbound cross_dept signals to operations
- [ ] `departments/compliance/cadences.md` — compliance-monitor weekly Mon 08:00 PYT
- [ ] `demiurge/agents/compliance-monitor/` — agent.yaml, PROMPT.md, repo-manifest.yaml

### Phase 3 — Cadence authority + alignment

- [ ] Resolve schedule authority: `departments/operations/cadences.md` is canonical; legacy `agents-prompts/` schedules updated or annotated as superseded
- [ ] Cadences reconciled per decision table in `context.md` (see Schedule authority)
- [ ] `departments/operations/cadences.md` — all 5 legacy agents + Kronos registered with `hermes_cron_id`, schedule, PYT column
- [ ] ai-ops-coordinator and compliance-monitor cadences registered

### Phase 4 — Doc-impl drift fixes

- [ ] `sources/operations/catalog.yaml` — signal IDs normalized to hyphen convention matching `signals.yaml`
- [ ] management-coordinator PROMPT state schema updated: `/opt/data/db/coord.db` (SQLite, v0.2.0 storage architecture)
- [ ] bizops-tracker `parent_spec` corrected from `07-cross-cutting-concerns.md` to `departments/operations/department.md`
- [ ] `demiurge/agents/README.md` — all 5 agents added to index

### Phase 5 — Ticket closure

- [ ] Ticket files in `tickets/DEMIURGE-079-ops-legacy-agents/`
- [ ] `tickets/INDEX.md` updated

## Schedule authority (decision required at start)

| Agent | Legacy (`agents-prompts/`) | DEMIURGE (`cadences.md`) | Recommended canonical |
|-------|---------------------------|--------------------------|----------------------|
| management-coordinator | Mon+Thu 17:00 PYT | Mon 09:00 | **Legacy** — biweekly cadence is operational requirement per constitution |
| business-analyst | Daily 06:30 PYT | Daily 08:00 | **Legacy** — 06:30 aligns with constitution cadence table |
| bizops-tracker | Sun 17:00 PYT | Fri 10:00 | **Legacy** — Sunday after research-tracker per prompt comment |
| ai-ops-coordinator | Daily 09:00 PYT | (missing) | **Legacy** — add to cadences.md |
| compliance-monitor | Mon 08:00 PYT | (missing) | **Legacy** — add to cadences.md |

## Testing strategy

- Verify each soul folder has all 3 required files (agent.yaml, PROMPT.md, repo-manifest.yaml)
- Cross-check every `sender:` in `departments/operations/signals.yaml` has a corresponding `emit_signal` step in the agent PROMPT
- Verify cadences.md entries match resolved schedule authority table
- Confirm catalog.yaml signal IDs match signals.yaml (hyphen convention)
- No router changes expected — inbound ops signals already wired in DEMIURGE-076

## Risks

- Schedule authority decision may conflict with Kronos delegation model (daily vs biweekly management-coordinator)
- Tier 2 dept shells (`ai-ops`, `compliance`) are skeleton — taxonomy status stays `skeleton` until Ivan approves activation
- Legacy `agents-prompts/` files may remain as runtime source until Hermes persona constructor (DEMIURGE-072) migrates them

## Questions

- Should legacy `agents-prompts/*.md` be deleted or kept as deprecated stubs after soul migration?
- Tier 2 `ai-ops` and `compliance` taxonomy status: keep `skeleton` or promote to `active` on soul creation?

## Dependencies

- DEMIURGE-074 (completed) — research + gaps.md
- DEMIURGE-075 (completed) — dept skeleton
- DEMIURGE-076 (completed) — Kronos lead + router inbound wiring
