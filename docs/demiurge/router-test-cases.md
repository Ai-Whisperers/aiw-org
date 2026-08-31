# Router + Quorum Test Cases

> DEMIURGE-052, DEMIURGE-076

## TC-R01 — Inbound lead dispatch

**Given** signal `sales-inbound-lead` with tags `[lead, inbound]`  
**When** Router processes  
**Then** apollo-sales-lead and cadmus-lead-enrichment receive signal  
**And** quorum `quorum-sales-lead-ack` opens with PT2H window

## TC-R02 — Quorum met

**Given** open quorum requiring apollo-sales-lead  
**When** Apollo reacts with `ack` within PT2H  
**Then** signal status → `quorum_met`

## TC-R03 — Quorum failed escalation

**Given** open quorum PT2H expired  
**When** no reaction from apollo-sales-lead  
**Then** fallback `escalate` to human:ivan  
**And** Argus receives alert

## TC-R04 — Content ready routing

**Given** `marketing-content-ready` from Hera  
**When** Router matches `route-content-ready`  
**Then** apollo-sales-lead receives within PT4H SLA

## TC-R05 — PD insight fan-out

**Given** `product-discovery-insight` with quorum 2 (Athena + Hera)  
**When** both react within PT48H  
**Then** `on_met: trigger_next_workflow` for Calliope brief update

## TC-R06 — Invalid payload

**Given** signal missing required `subject`  
**When** Router validates  
**Then** reject to sender; no dispatch; log error

## TC-R07 — Paused recipient

**Given** calliope-content-producer status paused  
**When** direct signal to Calliope  
**Then** Router retries once; escalates to hera-marketing-lead

## TC-R08 — Dept activation routing

**Given** signal `dept-activation-ready` with tags `[dept-activation]`  
**When** Router matches `route-dept-activation`  
**Then** kronos-operations-lead receives within PT24H SLA

## TC-R09 — Dept health breach routing

**Given** signal `dept-health-breach` with tags `[dept-health, kpi-breach]`  
**When** Router matches `route-dept-health-breach`  
**Then** kronos-operations-lead receives within PT4H SLA  
**And** quorum `quorum-ops-health-breach` opens (bizops-tracker reaction)

## TC-R10 — Ops agent health anomaly

**Given** signal `ops-agent-health-anomaly` with tags `[eval-gate, drift, hard-stop]`  
**When** Router matches `route-ops-agent-anomaly`  
**Then** kronos-operations-lead receives within PT1H SLA  
**And** escalate to human:ivan after PT2H if unacked

## TC-R11 — Compliance flag routing

**Given** signal `ops-compliance-flag-count` with tags `[compliance, trademark]`  
**When** Router matches `route-compliance-flag`  
**Then** kronos-operations-lead receives within PT24H SLA

## Manual test procedure

1. Load `demiurge/router/dispatch-rules.yaml`
2. Submit fixture signals from `demiurge/router/test-fixtures/`
3. Verify expected recipients in routing audit log

Fixtures: create JSON samples in Phase B implementation.
