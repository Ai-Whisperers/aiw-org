# AI Ops Department

> DEMIURGE-079

```yaml
id: ai-ops
name: AI Ops
tier: 2
status: skeleton
mission: Keep the agent layer itself healthy — eval gates, hard stops, drift detection, golden trajectories.
head_agent: ai-ops-coordinator
router_id: hermes-router-revenue
source_catalog_id: —
```

## Roles

| id | title | agent | status |
|----|-------|-------|--------|
| ai-ops-lead | AI Ops Lead | — | skeleton (Kiki) |
| ai-ops-coordinator | AI Ops Coordinator | ai-ops-coordinator | active |

## Outbound signals

| id | to | SLA |
|----|------|-----|
| ops-agent-health-anomaly | operations | PT1H |
| ops-incident-open-count | operations | P1D |

See [signals.yaml](signals.yaml) and [cadences.md](cadences.md).

Tier 2 taxonomy `status: skeleton` until Ivan approves dept activation. `ai-ops-coordinator` soul is `active` per DEMIURGE-079; dept promotion is a separate decision.
