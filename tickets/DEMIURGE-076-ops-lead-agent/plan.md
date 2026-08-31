# DEMIURGE-076: Design Operations lead agent soul + wire to router

**Sprint**: Phase 2 — Reference Department (Operations)
**Size**: 45m
**Owner**: AI

## Objective

Design the Kronos (Operations lead) agent soul and wire Operations inbound signals to Hermes — promoting the Operations dept from `skeleton` to `active`.

## Inputs

- `departments/operations/department.md` — mission, roles, signal tables (DEMIURGE-075)
- `departments/operations/signals.yaml` — 15 KPI signals + 4 cross-dept signals
- `departments/operations/cadences.md` — legacy agent cron entries
- `demiurge/agents/hera-marketing-lead/` — lead agent soul pattern
- `demiurge/agents/apollo-sales-lead/` — lead agent soul pattern
- `demiurge/router/dispatch-rules.yaml` — existing revenue dispatch rules
- `demiurge/router/timing-rules.yaml` — existing revenue timing rules

## Output

```
demiurge/agents/kronos-operations-lead/
├── agent.yaml
├── PROMPT.md
└── repo-manifest.yaml
```

Plus router wiring, department activation, taxonomy promotion.

## Complexity Assessment

**Track**: Complex Implementation

**Rationale**: New agent soul design, 4 dispatch rules + 4 timing rules, dept status promotion across multiple artifacts.

## Acceptance criteria

- [x] `demiurge/agents/kronos-operations-lead/` — agent.yaml, PROMPT.md, repo-manifest.yaml
- [x] Ops signals wired in dispatch-rules.yaml + timing-rules.yaml
- [x] `departments/operations/department.md` — `head_agent` and `router_id` set, status `active`
- [x] `docs/demiurge/department-taxonomy-v1.md` — operations status `active`
- [x] Ticket files in `tickets/DEMIURGE-076-ops-lead-agent/`

## Dependencies

- DEMIURGE-075 (completed) — Operations dept skeleton
- DEMIURGE-074 (completed) — Operations research pass
