# Router Agent Design Spec

> DEMIURGE-013

## Agent identity

| Field | Value |
|-------|-------|
| id | hermes-router-revenue |
| name | Hermes |
| display_name | Hermes — Signal Router |
| archetype | Connector |
| routes_for | marketing, sales, product-discovery, operations |

## Responsibilities

1. **Dispatch** — match signals to `dispatch_rules` by type + routing_tags
2. **Deliver** — ensure right agents/channels receive payload within priority SLA
3. **Track quorum** — count reactions, enforce time_window, execute fallback
4. **Escalate** — fire timing_rules when SLA breached
5. **Audit** — log all routing decisions to episodic memory

## Inputs

- Inbound `Signal` objects (from revenue-stack and operations agents)
- `demiurge/router/revenue-signals.yaml` — signal type registry (revenue + operations cross-dept)
- `demiurge/router/dispatch-rules.yaml` — routing table
- `demiurge/router/timing-rules.yaml` — SLA definitions
- `demiurge/router/quorum-definitions.yaml` — quorum templates

## Outputs

- Delivered signals to recipient agents (via Hermes message / state queue)
- QuorumTracker updates (SQLite: `hermes-router-revenue.db`)
- Escalation signals to humans (`human:ivan`) or lead agents
- Daily routing summary → Argus health monitor

## Cadence

| type | schedule |
|------|----------|
| continuous | every 15 min on-hours, every 10 min off-hours |
| on_signal | immediate for critical priority |

Hermes cron id: `demiurge-hermes-router-tick`

## Hard stops

```yaml
hard_stops:
  - action: drop_signal
    require_approval: true
    approved_human: ivan
  - action: modify_dispatch_rules
    require_approval: true
    approved_human: ivan
```

## Failure modes

| Failure | Behavior |
|---------|----------|
| No matching dispatch_rule | Log + deliver to dept lead + alert Argus |
| Quorum not met in window | Execute quorum fallback |
| Recipient agent paused | Try fan_out next; escalate after 2 failures |
| Payload schema invalid | Reject to sender with validation error |

## Implementation phases

1. **Phase A** (this build): YAML config + documentation; manual/simulated routing
2. **Phase B**: Python router script + SQLite quorum tracker
3. **Phase C**: Full Hermes cron integration with signal queue

See [router-test-cases.md](router-test-cases.md).
