# Marketing Department

> DEMIURGE-026

```yaml
id: marketing
name: Marketing
tier: 1
status: active
mission: Generate demand, nurture audience, and feed Sales with qualified attention and validated messaging.
head_agent: hera-marketing-lead
router_id: hermes-router-revenue
source_catalog_id: catalog-marketing
```

## Roles

| id | title | agent | status |
|----|-------|-------|--------|
| marketing-lead | Head of Marketing | hera-marketing-lead | active |
| marketing-content-producer | Content Producer | calliope-content-producer | active |
| marketing-community-monitor | Community Monitor | iris-community-monitor | active |
| marketing-brand-steward | Brand Steward | — | skeleton |
| marketing-ops-analyst | Marketing Ops Analyst | — | skeleton |
| marketing-localization | Localization Specialist | — | skeleton |

## Inbound signals

| id | from | SLA |
|----|------|-----|
| sales-pipeline-feedback | sales | PT24H |
| product-discovery-insight | product-discovery | PT48H |

## Outbound signals

| id | to | SLA |
|----|------|-----|
| marketing-content-ready | sales | PT4H |
| marketing-campaign-brief | sales, product-discovery | PT24H |

See [signals.yaml](signals.yaml).
