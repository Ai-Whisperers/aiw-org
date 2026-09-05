# Counteracting Controls Model

> **Status:** `proposed` — AIW-05 pending approval.
> **Scope:** Documentation design only — no runtime enforcement engine in this ticket.
> **Terms:** [counteracting_control](../terminology/TERMS.md), [maker_checker](../terminology/TERMS.md), [independence_requirement](../terminology/TERMS.md)
> **Assignments:** [entities/role-assignment.md](entities/role-assignment.md) · **Inventory:** [CONTROL-MAP.md](CONTROL-MAP.md)

---

## Purpose

Model deliberate **counteracting** responsibilities so agents detect errors early without confusing identity, authority, or accountability.

**Counteracting ≠ adversarial.** Each control pair shares an objective (quality, safety, compliance, reliability). Counteracting roles provide **independent evidence** and an **escalation path** when primary and checker disagree.

Agent and Role remain separate entities. Control relationships connect **roles** (and their RoleAssignments), not agent names alone.

---

## Counteracting control patterns

| Pattern | Primary (maker) | Counteracting (checker) | Shared objective | Independent evidence | Escalation |
|---------|-----------------|-------------------------|------------------|----------------------|------------|
| **maker–checker** | Creates artifact or state change | Validates before commit | Correct output | Separate read of source + rules | Block or escalate to approver |
| **proposer–approver** | Drafts decision or proposal | Approves or rejects | Sound decision | Approver reads primary evidence, not only proposer summary | Human approver or board |
| **builder–quality-gate** | Builds code, content, or config | Runs quality gate (tests, lint, eval) | Shippable artifact | Gate runs on artifact + independent checks | Fail gate → fix or waive with human |
| **operator–monitor** | Executes scheduled or on-demand work | Monitors health, drift, SLA | Reliable operation | Monitor reads telemetry/state, not operator self-report | Alert → lead agent or human |
| **decision-owner–independent-challenger** | Owns outcome | Challenges assumptions | Better decision | Challenger uses alternate sources or checklist | Escalation artifact if unresolved |
| **executor–auditor** | Performs transactional work | Audits trail and policy | Compliance | Auditor reads logs/evidence independently | Audit finding → remediation ticket |
| **primary–fallback** | Normal path executor | Standby when primary fails | Continuity | Fallback has separate trigger and state | Failover signal → human if both fail |
| **detector–remediator** | Detects anomaly or risk | Remediates or contains | Risk reduction | Detector output is input to remediator via artifact, not shared hallucination | Escalate if remediation blocked |

### Pattern notes

- **maker–checker** is the base pattern; other rows specialize it by domain.
- **proposer–approver** requires `independence_requirement: human` when impact is consequential (external send, merge, spend).
- **builder–quality-gate** maps to CI, eval-gate, and pre-commit chains — prompt-only instructions do **not** count as enforced gates (see [CONTROL-MAP.md](CONTROL-MAP.md)).
- **operator–monitor** covers cron + watchdog pairs; monitor must not mutate the same state it validates without a separate remediation role.
- **decision-owner–independent-challenger** prevents single-agent confirmation bias; challenger must cite evidence outside the primary's output.

---

## ControlAssignment schema

A **ControlAssignment** binds a control pattern to a controlled process and role pair(s).

```yaml
ControlAssignment:
  id: string
  control_id: string                    # catalog key, e.g. maker-checker-devin-qualis
  controlled_process_id: string           # process, workflow, or agent run id
  primary_role_id: string                 # Role id of maker/operator/executor
  counteracting_role_ids: string[]        # one or more checker roles
  control_type: preventive | detective | corrective
  independence_requirement: none | separate_role | separate_agent | human
  trigger: string                         # when checker runs (pre-commit, on PR, hourly, …)
  evidence_output_type: string            # eval result, test report, audit log, …
  failure_action: block | warn | escalate | rollback
  escalation_role_id: string              # Role id receiving unresolved failures
  effectiveness_kpi_id: string            # optional KPI for control health
```

### Field semantics

| Field | Notes |
|-------|-------|
| `control_type` | **preventive** — stops before harm; **detective** — finds after; **corrective** — remediates |
| `independence_requirement` | Minimum separation between primary and counteracting actors |
| `trigger` | Must be observable (cron, webhook, gate script) — not "agent remembers to check" |
| `failure_action` | `block` requires technical enforcement; `warn` alone is not sufficient for consequential impact |
| `escalation_role_id` | Receives artifact when primary and counteracting disagree |

### Independence requirement values

| Value | Meaning |
|-------|---------|
| `none` | Same actor may perform both sides (low-risk, informational only) |
| `separate_role` | Different RoleAssignments required; same agent allowed if roles differ |
| `separate_agent` | Different `actor_id` required for the same case |
| `human` | Human must perform approve/escalation side for consequential impact |

---

## Separation-of-duty rules

1. **Multiple roles per agent** — A single agent may hold multiple roles unless `independence_requirement` forbids it for a given control.
2. **`separate_agent`** — When required, the same `actor_id` cannot perform both primary and counteracting assignments in the **same case** (same `controlled_process_id` + time window).
3. **Consequential impact** — Requires `independence_requirement: human` for approval; agent-only approval is insufficient.
4. **Independent evidence** — Counteracting roles must not use the same unverified evidence as their sole input (e.g. checker must not accept only the maker's summary without reading source artifacts, tests, or schemas).
5. **Disagreement → escalation** — Disagreement produces an escalation artifact (ticket, signal, approval record) — not an infinite agent debate.
6. **No debate loops** — Agents must not re-prompt each other indefinitely to reach consensus; after one challenge cycle, route to `escalation_role_id` or `accountable_human_id`.

---

## Linking controls to RoleAssignment

ControlAssignment references **Role ids**, not agent ids. Resolve actors via active [RoleAssignment](entities/role-assignment.md) records at runtime.

```yaml
ControlAssignment:
  id: ca-devin-qualis-pr-gate
  control_id: builder-quality-gate-engineering
  controlled_process_id: engineering-pr-merge
  primary_role_id: engineering-roster
  counteracting_role_ids: [qa-automation-runner]
  control_type: preventive
  independence_requirement: separate_agent
  trigger: on_pull_request
  evidence_output_type: test_report
  failure_action: block
  escalation_role_id: engineering-roster
  effectiveness_kpi_id: kpi-pr-gate-pass-rate
```

When `engineering-roster` is held by Devin and `qa-automation-runner` by Qualis, the control is satisfied at `separate_agent` level. If both roles were held by the same agent, the assignment set violates rule 2 unless one assignment is suspended for that case.

---

## Anti-patterns

| Anti-pattern | Why forbidden | Correct approach |
|--------------|---------------|------------------|
| Same agent as maker and checker | Correlated errors; no independent evidence | `separate_agent` + distinct RoleAssignments |
| Prompt-only hard stop labeled "enforced" | No technical block; bypassable | Mark as `documented` only until gate script or CI enforces |
| Counteracting as adversarial rivalry | Destroys shared objective; hides escalation path | Document shared objective + escalation_role_id |
| Checker reads only maker output | No independent evidence | Require schema validation, test run, or external source |
| Unlimited agent debate | Latency + correlated hallucination | Rule 6 — one challenge cycle, then escalate |

---

## Related documents

| Document | Relationship |
|----------|--------------|
| [CONTROL-MAP.md](CONTROL-MAP.md) | AIW-specific control pair status |
| [entities/role-assignment.md](entities/role-assignment.md) | Actor–role bindings for control resolution |
| [METAMODEL.md](METAMODEL.md) | `checks`, `challenges`, `approves` relationship vocabulary |
| [GOVERNANCE.md](GOVERNANCE.md) | Human approval and lifecycle gates |
| [entities/governance.md](entities/governance.md) | Control entity type (policy-level) |
