# Operations Department

> DEMIURGE-075, DEMIURGE-076

```yaml
id: operations
name: Operations
tier: 1
status: active
mission: Run signal-driven daily operations — OKRs, incident response, vendor hygiene, cross-dept coordination, and cost control. Management spine for AI-native ops at <50 headcount.
head_agent: kronos-operations-lead
router_id: hermes-router-revenue
source_catalog_id: catalog-operations
```

## Roles

| id | title | agent | status |
|----|-------|-------|--------|
| ops-lead | Head of Operations | kronos-operations-lead | active |
| ops-management-coordinator | Management Coordinator | management-coordinator | active |
| ops-business-analyst | Business Analyst | business-analyst | active |
| ops-bizops-tracker | BizOps Tracker | bizops-tracker | active |
| ops-vendor-steward | Vendor Steward | — | deferred (SaaS tools > 10) |
| ops-runbook-curator | Runbook Curator | — | deferred (first P1 without runbook) |
| ops-cost-analyst | Cost Analyst | — | deferred (first paying customer) |

`ai-ops-coordinator` (Tier 2 `ai-ops`) and `compliance-monitor` (Tier 2 `compliance`) feed cross-dept signals into this department; they are not operations roles.

## Inbound signals

Summary only — canonical definitions in [signals.yaml](signals.yaml).

| id | from | SLA |
|----|------|-----|
| dept-activation-ready | ai-org-platform | PT24H |
| dept-health-breach | ai-org-platform | PT4H |
| ops-agent-health-anomaly | ai-ops | PT1H |
| ops-compliance-flag-count | compliance | PT24H |

## Outbound signals

| id | to | SLA |
|----|------|-----|
| dept-kpi-signals | ai-org-platform | PT48H |
| org-new-dept-request | ai-org-platform | PT24H |

See [signals.yaml](signals.yaml) and [cadences.md](cadences.md).
