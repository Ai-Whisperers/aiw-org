# Marketing — Literature Gap Analysis

> DEMIURGE-024

## In literature, missing or weak in our model

| Gap | Literature says | Action |
|-----|-----------------|--------|
| Brand guidelines agent | Brand Manager role at scale | Skeleton role `marketing-brand-steward`, Tier 3 |
| Paid performance | Performance marketing at scale | Deferred (trademark restrictions in playbook) |
| Marketing ops / MarTech stack | HubSpot ops certification | Add `marketing-ops-analyst` skeleton |
| Localization | Trilingual EN/ES/NL is our edge | Add explicit `marketing-localization` sub-role |
| Community-led growth | CMX, Orbit model | Covered by Iris community-monitor |

## In our model, well covered

- Content marketing (Calliope)
- Inbound methodology
- JTBD / product-marketing bridge to PD
- Founder-led GTM

## Recommended additions (skeleton)

```yaml
- id: marketing-brand-steward
  tier: deferred
  trigger: first major brand campaign
- id: marketing-ops-analyst
  tier: senior
  trigger: MarTech tools > 5
- id: marketing-localization
  tier: mid
  trigger: now (EN/ES/NL)
```

## Next scan

Quarterly or when KPI `content_engagement_rate` drops below 0.15.
