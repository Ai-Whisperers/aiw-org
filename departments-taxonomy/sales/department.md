# Sales Department

> DEMIURGE-034

```yaml
id: sales
name: Sales
tier: 1
status: active
mission: Qualify inbound demand, run discovery, close deals. Only dept that directly produces revenue.
head_agent: apollo-sales-lead
router_id: hermes-router-revenue
source_catalog_id: catalog-sales
```

## Roles

| id | title | agent | status |
|----|-------|-------|--------|
| sales-lead | Head of Sales | apollo-sales-lead | active |
| sales-lead-enrichment | Lead Enrichment | cadmus-lead-enrichment | active |
| sales-proposal-drafter | Proposal Drafter | metis-proposal-drafter | active |
| sales-sdr | SDR outbound | — | deferred (D2 inbound-first) |
| sales-ae | Account Executive | human:ivan | active |

## Signals

See [signals.yaml](signals.yaml).
