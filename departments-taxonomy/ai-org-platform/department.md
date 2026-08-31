# AI Org Platform Department

> DEMIURGE-073

```yaml
id: ai-org-platform
name: AI Org Platform
tier: 1
status: skeleton
mission: Design, activate, and continuously improve all company departments using signal-driven, science-backed agent workflows.
head_agent: —
router_id: —
source_catalog_id: —
```

## Roles

| id | title | agent | status |
|----|-------|-------|--------|
| aop-dept-finder | Dept Finder | — | skeleton |
| aop-dept-researcher | Dept Researcher | — | skeleton |
| aop-dept-decorator | Dept Decorator | — | skeleton |
| aop-dept-coach | Dept Coach | — | skeleton |
| aop-role-finder | Role Finder | — | skeleton |
| aop-role-researcher | Role Researcher | — | skeleton |
| aop-role-decorator | Role Decorator | — | skeleton |
| aop-dept-monitor | Dept Monitor | — | skeleton |

Role Coach applies at dept layer only (`aop-dept-coach`); role layer has Finder/Researcher/Decorator per ticket spec.

## Inbound signals

| id | from | SLA |
|----|------|-----|
| org-new-dept-request | founder, operations | PT24H |
| dept-kpi-signals | all departments | PT48H |

## Outbound signals

| id | to | SLA |
|----|------|-----|
| dept-activation-ready | operations | PT24H |
| dept-health-breach | operations, target-dept | PT4H |
| dept-improvement-suggested | target-dept | PT48H |

Signals inline while `status: skeleton`; extract to `signals.yaml` on activation.
