# Operations — Literature Gap Analysis

> DEMIURGE-074

## In literature, missing or weak in our model

| Gap | Literature says | Action |
|-----|-----------------|--------|
| Formal OKR cadence | Doerr: weekly check-ins, quarterly reset with scoring | Wire `bizops-tracker` to `signals.yaml` OKR signals; define kill criteria per KR |
| Incident runbook library | ITIL + DORA: documented runbooks, blameless postmortems | Add `operations/runbooks/` stub; link ai-ops-coordinator anomalies to runbook IDs |
| Vendor renewal calendar | First Round / a16z: proactive SaaS renewal tracking | Add `ops_vendor_renewal_30d` signal; skeleton role `operations-vendor-steward` |
| Cost control / unit economics | Burn tracking, cost-per-transaction at <50 headcount | Add monthly `ops_burn_rate` + `ops_cost_per_transaction` to bizops-tracker inputs |
| Process documentation as code | Atlassian playbooks: retros, health monitors, decision logs | Migrate tribal ops knowledge from chat to `departments/operations/` |
| Cross-dept async coordination | Grove: no meeting-driven ops; briefs + decision queues | Formalize management-coordinator output as signal channel, not just chat |
| Decision latency tracking | bizops-tracker reads `state/people.json` but no KPI wired | `ops_decision_latency_days` defined in catalog; wire in DEMIURGE-075 `signals.yaml` |

## In our model, well covered (legacy prompts)

| Capability | Legacy agent | Benchmark alignment |
|------------|--------------|---------------------|
| Daily business snapshot | `business-analyst` | Grove signal-driven ops — daily leading indicators |
| Biweekly work visibility | `management-coordinator` | Stuck/stale/PR queue/decisions — async coordination |
| Weekly OKR progress | `bizops-tracker` | Doerr OKR methodology — partial (no kill criteria yet) |
| Agent layer health | `ai-ops-coordinator` | DORA-style monitoring — eval gates, drift, hard stops |
| Regulatory watch | `compliance-monitor` | ITIL change management — weekly compliance brief |

## Legacy → DEMIURGE migration gaps

| Legacy prompt | Missing DEMIURGE structure | DEMIURGE-075 action |
|---------------|---------------------------|---------------------|
| `management-coordinator` | No signals, no router wiring, no cadence schema | Promote to Kronos sub-agent with `signals.yaml` entries |
| `business-analyst` | No department.md parent, no KPI schema | Wire daily signals to operations dept |
| `bizops-tracker` | OKRs in `state/bizops.json` — not in repo | Move OKR definitions to `departments/operations/okrs.yaml` |
| `ai-ops-coordinator` | Belongs to Tier 2 `ai-ops`, not operations | Cross-dept signal feed into operations rollup |
| `compliance-monitor` | Belongs to Tier 2 `compliance` | Operations consumes `ops_compliance_flag_count` as input |

## AI-native <50 people benchmark

Sourced from practitioner playbooks, not a single study — representative refs:
- First Round Review ops articles (e.g. [How to Run a Quarterly Operating Review](https://review.firstround.com/))
- a16z operator essays on lean startup ops (no stable index URL; catalog uses `—`)
- Grove (*High Output Management*) on meeting load and managerial leverage

| Practice | Benchmark | AI Whisperers today |
|----------|-----------|---------------------|
| Headcount | <10 FTE, founder-led ops | Founder-led — aligned |
| Meeting load | <5 hrs/week standing meetings | Mostly async agents — aligned |
| OKR cadence | Quarterly objectives, weekly check-ins | Weekly bizops-tracker — partial |
| Incident response | <1hr MTTR for P1, runbooks | ai-ops-coordinator detects; no runbook library |
| Tool stack | <15 SaaS tools, quarterly audit | Unknown count — gap |
| Cost visibility | Monthly burn review | No formal signal — gap |
| Decision queue | ≤3 decisions/week for CEO | management-coordinator caps at 3 — aligned |

## Recommended additions (skeleton)

```yaml
- id: operations-vendor-steward
  tier: senior
  trigger: SaaS tools > 10
- id: operations-runbook-curator
  tier: mid
  trigger: first P1 incident without runbook
- id: operations-cost-analyst
  tier: mid
  trigger: first paying customer (unit economics matter)
```

## Next scan

Quarterly or when `ops_okr_completion_pct` drops below 0.5 at mid-quarter.
