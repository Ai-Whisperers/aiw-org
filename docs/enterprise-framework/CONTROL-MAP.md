# AIW Control Pair Inventory

> **Status:** `proposed` — AIW-05 pending approval.
> **Model:** [CONTROLS.md](CONTROLS.md) · **Assignments:** [entities/role-assignment.md](entities/role-assignment.md)

Maps known AIW primary ↔ counteracting pairs to control patterns. Status columns reflect **current repo evidence**, not aspirational design.

**Legend**

| Column | Meaning |
|--------|---------|
| **documented** | Pattern described in PROMPT, dept doc, ADR, or framework |
| **implemented** | Scripts, gates, monitors, or schemas exist in repo |
| **enforced** | Technical block or mandatory gate — **not** prompt-only instruction |
| **measured** | KPI, eval log, or audit trail tracks control effectiveness |

**Rule:** Prompt-only hard stops (Soul `hard_stops`, PROMPT "do not send") are **not** marked `enforced`.

---

## Control map

| Pair | Pattern | Primary (role / agent) | Counteracting (role / agent) | control_type | documented | implemented | enforced | measured |
|------|---------|------------------------|------------------------------|--------------|------------|-------------|----------|----------|
| Devin ↔ Qualis | builder–quality-gate | `engineering-roster` / Devin | `qa-automation-runner` / Qualis | preventive | yes | partial | partial | partial |
| Devin ↔ Safina | operator–monitor + decision-owner–challenger | `engineering-roster` / Devin | `ai-safety-engineer` / Safina | detective | yes | partial | no | partial |
| Proposal drafter ↔ feasibility gate | proposer–approver | `metis-proposal-drafter` / Metis | `feasibility-gate` / Gatina | preventive | yes | partial | no | no |
| Agent executor ↔ eval gate | builder–quality-gate | any active agent (executor) | eval-gate scripts / eval-gate-runner role | preventive | yes | yes | partial | yes |
| State writer ↔ schema validator | maker–checker | agent state writers (monitors) | `schema-validate-write.py`, `aiw-state-validate.py` | detective | yes | yes | partial | partial |
| Cron job ↔ heartbeat/watchdog | operator–monitor | cadence-triggered agents | `*-monitor` PROMPTs, cron-error-watchdog | detective | yes | yes | partial | partial |
| Researcher ↔ citation checker | maker–checker | `research-tracker` / Renata | `citation-checker` | detective | yes | partial | no | no |

---

## Pair detail

### Devin ↔ Qualis

- **Shared objective:** Shippable engineering output with test and coverage confidence.
- **Independent evidence:** Qualis runs tests/coverage gate on artifact, not Devin's self-report.
- **Escalation:** Engineering lead (`engineering-roster`) or human accountable.
- **Evidence:** DD-07 (conflicting roles on purpose); `departments/04-engineering-delivery.md`; `qa-automation-runner` agent.
- **Gap:** Full PR-block enforcement depends on CI wiring; not all merge paths run Qualis gate.

### Devin ↔ Safina

- **Shared objective:** Prevent Kiro-class safety incidents without merging safety into delivery QA.
- **Independent evidence:** Safina scans for hard-stop bypasses, secret exposure, unsafe patterns.
- **Escalation:** Human accountable (`human:ivan` / `human:kiki` per Soul hard_stops).
- **Evidence:** DD-07; `ai-safety-engineer` agent; `security-watchdog` cadence variant.
- **Gap:** Soul hard_stops are **documented**, not **enforced** — THREAT-MODEL notes advisory-only hard stops.

### Proposal drafter ↔ feasibility gate

- **Shared objective:** No external proposal send without feasibility review.
- **Independent evidence:** Gatina (`feasibility-gate`) HARD STOP on Metis sends — documented in engineering dept naming table.
- **Escalation:** Human approver before external send.
- **Gap:** HARD STOP is PROMPT-level; no repo-wide technical block on send path marked enforced.

### Agent executor ↔ eval gate

- **Shared objective:** Agent output meets quality bar before destructive or high-impact runs.
- **Independent evidence:** `scripts/eval-gate-enforce.py`, `aiw-eval-gate-runner.sh`, `state/auto-eval-log.jsonl`.
- **Escalation:** Eval gate decisions log; human override per Phase 27 feedback.
- **Evidence:** `docs/phases/PHASE-16-LIVE-EXECUTION.md` (17/17 PASS); eval-gate cron.
- **Gap:** Not all agents hooked to pre-run eval block; enforcement is **partial**.

### State writer ↔ schema validator

- **Shared objective:** State files remain schema-valid and auditable.
- **Independent evidence:** JSON Schema files + `schema-validate-write.py` / `aiw-state-validate.py`; monitor PROMPTs validate on read.
- **Escalation:** HIGH escalation in monitor PROMPT when invalid.
- **Evidence:** Phase 28 schema rollout; `tests/test_schema_validate_write.py`.
- **Gap:** `--strict` validation not universal on every write path.

### Cron job ↔ heartbeat/watchdog

- **Shared objective:** Scheduled agents remain alive and within SLA.
- **Independent evidence:** Heartbeat fields in state; `*-monitor` agents; `cron-error-watchdog` schema.
- **Escalation:** Signal to lead agent or ops cron.
- **Evidence:** `feedback-kpi-cadence.md` (on_hours/off_hours heartbeat); `generate-monitors.py`.
- **Gap:** Measurement via cron traces partial; not all jobs have dedicated watchdog.

### Researcher ↔ citation checker

- **Shared objective:** Research outputs cite sources correctly.
- **Independent evidence:** Citation checker validates against source catalog, not researcher's draft alone.
- **Escalation:** Research lead or human review.
- **Evidence:** `docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md`; pre-commit `citation-coverage` mentioned in audit doc.
- **Gap:** Citation discipline **documented**; automated block on publish not marked enforced.

---

## Summary

| Status | Count (of 7 pairs) | Notes |
|--------|-------------------|-------|
| documented | 7/7 | All pairs have design or dept-level documentation |
| implemented | 5/7 | Scripts/monitors exist; proposal and citation paths thinner |
| enforced | 0/7 fully | Eval and schema paths **partial**; prompt hard stops excluded |
| measured | 3/7 | Eval gate, partial cron/schema telemetry |

---

## Related documents

| Document | Relationship |
|----------|--------------|
| [CONTROLS.md](CONTROLS.md) | Pattern definitions and SoD rules |
| [meetings/department-design/DECISIONS.md](../../meetings/department-design/DECISIONS.md) | DD-07 conflicting roles |
| [GOVERNANCE.md](GOVERNANCE.md) | Human approval requirements |
