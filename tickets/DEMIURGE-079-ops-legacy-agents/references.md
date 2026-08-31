# References — DEMIURGE-079

## Gap analysis source

- Command: `/Grimoire/jp-analyze-gaps` (2026-08-29)
- Scope: `constitution/01-operations.md`, 5 legacy `agents-prompts/`
- Standards reference: `departments/marketing/`
- Dimensions: `impl`, `docs`
- Result: 18 findings (0 Critical, 11 High, 6 Medium, 1 Low)

## Legacy agent prompts

| File | Version |
|------|---------|
| `agents-prompts/management-coordinator.md` | 0.2.0 |
| `agents-prompts/business-analyst.md` | 0.2.0 |
| `agents-prompts/bizops-tracker.md` | 0.2.0 |
| `agents-prompts/ai-ops-coordinator.md` | 0.2.0 |
| `agents-prompts/compliance-monitor.md` | 0.2.0 |

## DEMIURGE artifacts (existing)

| File | Ticket |
|------|--------|
| `departments/operations/department.md` | DEMIURGE-075 |
| `departments/operations/signals.yaml` | DEMIURGE-075 |
| `departments/operations/cadences.md` | DEMIURGE-075 |
| `demiurge/agents/kronos-operations-lead/` | DEMIURGE-076 |
| `demiurge/router/dispatch-rules.yaml` (4 ops rules) | DEMIURGE-076 |
| `demiurge/router/timing-rules.yaml` (4 ops SLAs) | DEMIURGE-076 |
| `sources/operations/catalog.yaml` | DEMIURGE-074 |
| `sources/operations/gaps.md` | DEMIURGE-074 |

## Reference patterns

| Pattern | Path |
|---------|------|
| Sub-agent soul | `demiurge/agents/calliope-content-producer/` |
| Dept shell | `departments/marketing/` |
| Lead agent soul | `demiurge/agents/kronos-operations-lead/` |

## Related tickets

| ID | Status | Relationship |
|----|--------|--------------|
| DEMIURGE-074 | completed | Research + gaps.md — source of migration map |
| DEMIURGE-075 | completed | Dept skeleton — deferred sub-agent souls |
| DEMIURGE-076 | completed | Kronos lead + router — deferred sub-agent souls |
| DEMIURGE-072 | pending | Hermes persona constructor — may supersede legacy prompts |
