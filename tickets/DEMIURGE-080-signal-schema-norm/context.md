# Context — DEMIURGE-080

**STATUS**: COMPLETE
**FOCUS**: Done
**RESUME_POINT**: None — ticket complete

## Current state

All gap analysis findings resolved across 6 files:
- `departments/marketing/signals.yaml`
- `departments/sales/signals.yaml`
- `departments/product-discovery/signals.yaml`
- `departments/operations/signals.yaml`
- `demiurge/router/dispatch-rules.yaml` (unchanged — signal-side tags fixed)
- `docs/demiurge/schemas/signal-channel.md`

## Components

| File | Role | Status |
|---|---|---|
| `pd/signals.yaml` | PD signal type registry | routing_tags added; quorum_required; priority defaults |
| `marketing/signals.yaml` | Marketing signal type registry | payload renamed; tags synced; quorum_required |
| `sales/signals.yaml` | Sales signal type registry | tags synced; quorum_required; priority defaults |
| `operations/signals.yaml` | Ops signal type registry | quorum_required; priority defaults; kpi documented in schema |
| `dispatch-rules.yaml` | Router routing config | route-customer-signal now matchable via customer-signal-raw tags |
| `signal-channel.md` | Authoritative schema | SignalType, QuorumDefinition, kpi enum, shorthands documented |

## Dependencies

- DEMIURGE-077 (Terminology Library) — in progress, pending Ivan review
  - `priority: normal` defaults added with `# pending DEMIURGE-077 P0-P3 review` comments
  - Refinement of priority values deferred to DEMIURGE-077 completion

## Decisions applied

| # | Decision | Choice |
|---|---|---|
| 1 | customer-signal-raw routing tag | A — add `[customer-voice]` to signal |
| 2 | sales-pipeline-feedback tags | C — union `[pipeline, win-loss, customer-voice]` |
| 3 | quorum vs quorum_required | A — rename to `quorum_required` |
| 4 | sender shorthand | B — document in schema |
| 5 | recipients shorthand | B — document in schema |
| 6 | type: kpi | A — add to schema enum |
