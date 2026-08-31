# DEMIURGE-075: Define Operations dept — mission, roles, signals, KPIs, cadences

**Sprint**: Phase 2 — Reference Department (Operations)
**Size**: 60m
**Owner**: AI

## Objective

Define the Operations department skeleton — mission, role inventory, signals, KPIs, and cadences — consuming DEMIURGE-074 research outputs. This is the reference department buildout that DEMIURGE-076 (lead agent soul) will activate.

## Inputs

- `sources/operations/catalog.yaml` — signal types, frameworks
- `sources/operations/gaps.md` — legacy agent migration, recommended roles
- `sources/operations/community-signals.md` — scan cadence mapping
- `docs/demiurge/department-taxonomy-v1.md` — operations as Tier 1 skeleton

## Output

```
departments/operations/
├── department.md
├── signals.yaml
└── cadences.md
```

## Complexity Assessment

**Track**: Complex Implementation

**Rationale**: Multiple artifacts, cross-dept signal wiring, legacy agent migration mapping, 15+ signal definitions. Not a single-file fix.

## Acceptance criteria

- [x] `departments/operations/department.md` — mission, roles table, signals reference
- [x] `departments/operations/signals.yaml` — all DEMIURGE-074 signals + cross-dept signals
- [x] `departments/operations/cadences.md` — cron per legacy agent
- [x] Taxonomy status stays `skeleton` (no change until DEMIURGE-076)
- [x] Ticket files in `tickets/DEMIURGE-075-ops-dept/`

## Dependencies

- DEMIURGE-074 (completed) — research pass
- DEMIURGE-076 (pending) — lead agent soul + router wiring
