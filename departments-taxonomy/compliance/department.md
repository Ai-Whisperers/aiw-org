# Compliance Department

> DEMIURGE-079

```yaml
id: compliance
name: Compliance
tier: 2
status: skeleton
mission: Own the compliance program — GDPR, LGPD, EU AI Act, trademark banlist enforcement.
head_agent: compliance-monitor
router_id: hermes-router-revenue
source_catalog_id: —
```

## Roles

| id | title | agent | status |
|----|-------|-------|--------|
| compliance-officer | Compliance Officer | — | skeleton (Ivan) |
| compliance-monitor | Compliance Monitor | compliance-monitor | active |

## Outbound signals

| id | to | SLA |
|----|------|-----|
| ops-compliance-flag-count | operations | PT24H |

See [signals.yaml](signals.yaml) and [cadences.md](cadences.md).

## Hard-stop rule

No EU client contracts accepted until Compliance Officer role is filled by a named person (not Ivan alone).

Tier 2 taxonomy `status: skeleton` until Ivan approves dept activation. `compliance-monitor` soul is `active` per DEMIURGE-079; dept promotion is a separate decision.
