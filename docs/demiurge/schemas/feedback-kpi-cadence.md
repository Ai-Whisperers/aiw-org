# Schema: FeedbackLoop + KPI + Cadence

> DEMIURGE-007

## FeedbackLoop

Self-improvement cycle. The more loops, the better AI performs.

```yaml
FeedbackLoop:
  id: string
  name: string
  trigger:
    type: enum              # kpi_threshold | signal | schedule | manual
    condition: string       # e.g. "kpi.reply_rate < 0.15"
  input:
    type: enum              # kpi | signal | source_gap | monitor_alert
    ref: string
  action:
    type: enum              # update_source_catalog | revise_soul | add_role | adjust_cadence | escalate_human
    target: string
  output: string            # what changes
  frequency: duration
  owner_agent: string
  status: enum              # active | paused
```

### Standard loops (revenue stack)

| Loop | Trigger | Action |
|------|---------|--------|
| pipeline-to-content | Sales win/loss signal | Marketing updates content brief |
| content-to-pipeline | Low engagement KPI | Marketing revises source catalog |
| insight-to-product | PD customer signal | Product discovery updates role priorities |
| monitor-to-soul | Health score < 0.7 | Suggest soul/prompt revision |
| literature-to-dept | Quarterly scan | Add missing roles from gaps |

## KPI

Performance metric for role or department.

```yaml
KPI:
  id: string
  name: string
  formula: string           # human-readable
  target: number
  current: number
  unit: string              # %, count, USD, hours
  owner_type: enum          # agent | department
  owner_id: string
  measurement_cadence: duration
  feedback_trigger:
    below: number           # fires FeedbackLoop when current < this
    above: number           # optional upper bound alert
  feedback_loop_id: string
```

### KPI examples (top 3 depts)

See [kpi-schema-revenue.md](../kpi-schema-revenue.md).

## Cadence

When and how often an agent acts. Swarm works in time slots.

```yaml
Cadence:
  id: string
  agent_id: string
  schedule: string          # cron expression
  timezone: string          # America/Asuncion (PYT)
  type: enum                # scheduled | on_signal | on_demand | continuous
  time_slot: enum           # on_hours | off_hours | any
  hermes_cron_id: string    # registered job id
  idempotency_window: duration
  max_runs_per_day: int
```

### Cadence types

| type | When it runs |
|------|--------------|
| scheduled | Cron only |
| on_signal | Router delivers signal → agent wakes |
| on_demand | Human or agent invokes |
| continuous | Watchdog (e.g. every 30 min) |

### Time slot policy (from PLAN-v5)

- **on_hours**: 06:00–22:00 PYT, heartbeat every 30 min
- **off_hours**: 23:00–05:00 PYT, heartbeat every 15 min (denser)

## Validation checklist

- [ ] Every active agent has Cadence defined
- [ ] KPIs have feedback_trigger linked to FeedbackLoop
- [ ] Scheduled cadences registered in Hermes cron
- [ ] on_signal agents subscribed via Router dispatch_rules
