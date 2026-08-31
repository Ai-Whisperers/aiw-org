# Schema: Signal + Channel

> DEMIURGE-004

## Signal

A message between agents or departments.

```yaml
Signal:
  id: string                # uuid
  type: enum                # direct | group | dept_broadcast | cross_dept
                             # (kpi is SignalType-registry only — not a runtime Signal type)
  sender_id: string         # Agent id
  sender_dept_id: string    # optional context
  recipients:
    - type: enum            # agent | department | channel
      id: string
  channel_id: string        # optional, if routed via channel
  payload: object           # structured JSON per SignalType schema
  priority: enum            # normal | urgent | critical
  quorum_required: string   # Quorum id or null
  routing_tags: string[]    # Router dispatch hints
  created_at: iso8601
  expires_at: iso8601       # deadline for reaction
  status: enum              # pending | delivered | quorum_met | expired | escalated
  reactions: Reaction[]     # agent responses
```

## Reaction

An agent's response to a signal.

```yaml
Reaction:
  agent_id: string
  reacted_at: iso8601
  action: enum              # ack | approve | reject | delegate | complete
  payload: object           # optional structured response
  within_sla: boolean
```

## Channel

Communication pathway signals travel through.

```yaml
Channel:
  id: string
  name: string
  type: enum                # direct | group | dept | broadcast | cross_dept
  members:
    - type: enum            # agent | department
      id: string
  router_id: string         # Router agent managing this channel
  retention_days: int       # default 90
  allowed_signal_types: string[]
  description: string
```

## Signal type matrix

| type | Scope | Example |
|------|-------|---------|
| direct | Agent → Agent | Sales lead → proposal drafter |
| group | Agent → named group | Marketing content review circle |
| dept_broadcast | Agent → whole dept | Product insight to all Marketing |
| cross_dept | Dept → Dept | Marketing content-ready → Sales |
| kpi | Operations internal metric (registry only) | Daily incident count, OKR completion |

The `kpi` row applies to **SignalType** registry entries in `signals.yaml`, not to runtime `Signal` instances. KPI measurements are emitted as internal/direct signals with `type: kpi` in the registry; at runtime they map to agent-scoped delivery, not cross_dept routing.

## SignalType

Type registry entry in department `signals.yaml` files. Distinct from runtime `Signal` instances.

```yaml
SignalType:
  id: string
  direction: enum        # in | out | internal
  type: enum             # direct | group | dept_broadcast | cross_dept | kpi
  sender: string         # dept or agent id (shorthand; see below)
  sender_id: string      # agent id (schema-conformant alternative to sender)
  sender_dept_id: string # dept id when sender is an agent
  recipients: list       # bare dept/agent ids (shorthand) or typed objects
  routing_tags: string[] # required for cross_dept; optional for direct/internal when Hermes dispatch applies
  priority: enum         # normal | urgent | critical (default: normal)
  quorum_required: string
  sla_reaction: iso8601_duration
  payload: object        # payload field schema
  measurement_cadence: iso8601_duration  # kpi signals only
```

### Registry shorthands

Department signal registries may use shorthand forms that expand at runtime:

| Field | Shorthand | Expanded form |
|-------|-----------|---------------|
| `sender` | `marketing` (dept id) | `sender_dept_id: marketing` |
| `sender` | `clio-customer-signal-collector` (agent id) | `sender_id: clio-customer-signal-collector` |
| `recipients` | `[sales, product-discovery]` | `[{type: department, id: sales}, {type: department, id: product-discovery}]` |
| `recipients` | `[metis-proposal-drafter]` | `[{type: agent, id: metis-proposal-drafter}]` |

The `kpi` type is operations-internal: KPI measurement signals produced by agents within Operations. Not used for cross-dept routing.

### routing_tags semantics

`routing_tags` are **dispatch keys**, not descriptive metadata. Each tag may activate one or more `dispatch-rules.yaml` entries (subset match: all rule tags must appear on the signal). Tags must be **orthogonal** — do not add a tag to a signal type because its payload is semantically related to another route. Example: `sales-pipeline-feedback` uses `[pipeline, win-loss]` only; `customer-voice` belongs on `customer-signal-raw`, not on pipeline feedback, or `route-customer-signal` fires incorrectly.

## QuorumDefinition

Quorum rules referenced by `quorum_required` on SignalType or Signal instances.

```yaml
QuorumDefinition:
  id: string
  required_count: int
  required_agents: string[]
  time_window: iso8601_duration
  fallback: enum          # auto_resolve | escalate
  fallback_target: string # optional: human:<id>
  on_met: string          # optional: trigger_next_workflow
```

## Payload conventions

All payloads include:

```json
{
  "signal_version": "1.0",
  "subject": "string",
  "body": "string or markdown",
  "artifacts": [{"path": "...", "type": "markdown|json|url"}],
  "correlation_id": "uuid",
  "source_run_id": "cron or manual run id"
}
```

## Priority handling

| priority | Router behavior |
|----------|-----------------|
| normal | Next cadence slot or within 4h |
| urgent | Within 1h, notify if unacked |
| critical | Immediate dispatch, escalate at 30m |

## Validation checklist

- [ ] Every cross_dept signal has routing_tags
- [ ] Every cross_dept SignalType has routing_tags
- [ ] expires_at set for urgent/critical
- [ ] payload validates against SignalType schema
- [ ] sender is active agent
