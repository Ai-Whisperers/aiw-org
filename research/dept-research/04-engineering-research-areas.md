# Department of Engineering & Development — Research Catalog

> **Built 2026-09-01** as part of Phase 7 (research deepening).
>
> **Department head**: Kiki (CTO) | **Lead agent**: `engineering-roster` | **Atomic agents**: `devops-monitor`, `ai-safety-engineer`, `security-watchdog`, `chaos-test-runner`
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern + depth test).
>
> **Status**: 10 areas documented. Cadence tiers: 🔴 HOT (3), 🟡 WARM (5), 🔵 COOL (2).

---

## Reading guide

Engineering & Development research is the most **methodology-heavy** of all departments — we have the 12-factor methodology, around-the-clock upgrade methodology, and 5+ phases of org-design literature. The 10 areas here mostly **refresh existing methodologies** with post-DEMIURGE reality.

Areas are grouped by the 4 universal themes (internal / market / literature / actionable).

---

# Engineering & Development Research Areas



## 🔴 HOT areas

### 1. 12-factor compliance re-audit post-DEMIURGE 🔴

| | |
|---|---|
| **Question** | After DEMIURGE promotion (24 atomic agents), which of the 12 factors still pass, and which need a refresh? |
| **Why** | The Phase 21 audit (`docs/phases/PHASE-21-*`) was done pre-DEMIURGE. The org has ~28 new sub-agents + 18 new monitors. The 12-factor score is stale. |
| **Method** | (1) Read `docs/phases/PHASE-21-12-FACTOR-AUDIT.md` (the original). (2) Re-score each factor against current state. (3) Note regressions (e.g., Factor 5: Unified State — is it still unified?). (4) Note improvements (e.g., Factor 11: Webhook triggers — implemented in Phase 19). (5) Build refreshed scorecard. |
| **Output** | `engineering/12-factor-audit-2026-q3.md` (refreshed scorecard) |
| **Owner** | engineering-roster + ai-safety-engineer |
| **Cadence** | Quarterly |
| **Cross-references** | `docs/phases/PHASE-21-12-FACTOR-AUDIT.md`, `docs/phases/PHASE-25-*`, every dept's PROMPT.md (Factor 5) |

### 2. AI safety engineering — hard-stops + eval gates enforcement 🔴

| | |
|---|---|
| **Question** | What's the actual safety posture of the system right now, and what's the path to compliant AI-safety-engineer coverage? |
| **Why** | The Phase 6 audit found hard-stops wrapper is invoked by 0 of 49 agents. The `eval-per-agent.json` aggregate pass_rate isn't computed. These are **safety holes**, not just operational gaps. |
| **Method** | (1) Audit: which agents can do destructive actions (write state, send email, deploy code)? (2) For each, verify hard-stop enforcement. (3) Compute aggregate pass_rate from `eval-per-agent.json`. (4) Identify gap: agents without safety gates. (5) Recommend: invoke hard-stops wrapper globally + add eval-gate at agent execution. |
| **Output** | `engineering/ai-safety-posture-2026.md` (current posture + gap list + remediation plan) |
| **Owner** | ai-safety-engineer + engineering-roster + Kiki |
| **Cadence** | Quarterly |
| **Cross-references** | `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` surprise #1+2, `04-engineering/ai-safety-engineer/PROMPT.md`, `patterns/hard-stop-wrapper.py` |

### 3. Around-the-clock upgrade — Phase 25 revisit 🔴

| | |
|---|---|
| **Question** | Which of the 14 Phase 25 around-the-clock upgrade items are now complete, which are in progress, which are pending, and which need a Phase 26? |
| **Why** | Phase 25 was the last big methodology shift. Post-DEMIURGE, some items are done, some aren't. We need a refresh to know what to work on next. |
| **Method** | (1) Read `docs/phases/PHASE-25-*`. (2) For each of 14 items: status (done / in-progress / pending / failed). (3) Note what was completed since (Phase 5+6 monitor wiring closes several). (4) Identify remaining items. (5) Build Phase 26 candidate list. |
| **Output** | `engineering/phase-25-revisit-2026.md` (14-item status table + Phase 26 candidates) |
| **Owner** | engineering-roster + Kiki |
| **Cadence** | Once |
| **Cross-references** | `docs/phases/PHASE-25-*`, `analysis/PHASE-5-COMPLETION-REPORT.md`, `analysis/PHASE-6-REFINEMENT-FEEDBACK.md` |

---

## 🟡 WARM areas

### 4. Drift detection methodology 🟡

| | |
|---|---|
| **Question** | What kinds of drift (distribution, agent output, schema, cron timing) should we detect and at what sensitivity? |
| **Why** | `drift-detector` agent was built in Phase 5 R6 but with educated-guess thresholds. After 30 days of real data, we know what fires too often vs not enough. |
| **Method** | (1) Read `04-engineering/drift-detector/PROMPT.md`. (2) Run for 30 days. (3) Daily review: which drift types fire, how often, are they useful? (4) Calibrate thresholds per drift type. (5) Document the calibration in `drift-detection-methodology.md`. |
| **Output** | `engineering/drift-detection-methodology.md` (calibration table + per-type thresholds) |
| **Owner** | drift-detector agent + ai-safety-engineer |
| **Cadence** | Once + quarterly tune |
| **Cross-references** | `04-engineering/drift-detector/PROMPT.md`, `drift-detector/monitor-notes/` |

### 5. Chaos testing methodology — first chaos test run 🟡

| | |
|---|---|
| **Question** | What failure scenarios should we test, and what's the runbook for each (with hard-stops wrapper active)? |
| **Why** | `chaos-test-runner` agent exists but never fired in production. We have 16 monitors + 49 agents; we need to know what happens when key components fail. |
| **Method** | (1) Read `04-engineering/chaos-test-runner/PROMPT.md`. (2) Identify 5 high-value chaos scenarios (e.g., coord.json deleted, finance.json corrupted, eval-per-agent.json missing, hermes-router-revenue down). (3) For each: runbook (pre-conditions, action, expected outcome, rollback). (4) Run one scenario in staging. (5) Document learnings. |
| **Output** | `engineering/chaos-test-runbook.md` (5 scenarios with runbooks + first-run learnings) |
| **Owner** | chaos-test-runner + engineering-roster |
| **Cadence** | Once + per new scenario |
| **Cross-references** | `04-engineering/chaos-test-runner/PROMPT.md`, `state/chaos-test-B-result.json`, `state/chaos-test-C-result.json` |

### 6. Eval gate architecture — aggregate pass_rate + per-agent trend 🟡

| | |
|---|---|
| **Question** | Can we compute aggregate eval-gate pass_rate and per-agent trend signals from `state/eval-per-agent.json`? |
| **Why** | `eval-gate-runner` monitor (built Phase 5) describes the formula but doesn't actually compute it. Without this, the eval gate is a poster, not a tool. |
| **Method** | (1) Read `state/eval-per-agent.json` structure. (2) Write a small Python script that computes: aggregate pass_rate, per-agent trend (last 7d vs prior 7d), longest consecutive-failure streak. (3) Output to `state/eval-trending.json`. (4) Verify eval-gate-runner monitor picks it up. |
| **Output** | `scripts/eval-aggregate-pass-rate.py` + `state/eval-trending.json` (initial values) |
| **Owner** | eval-gate-runner + ai-safety-engineer |
| **Cadence** | Once + cron |
| **Cross-references** | `04-engineering/eval-gate-runner/PROMPT.md`, `state/eval-per-agent.json`, `04-engineering/ai-safety-engineer/PROMPT-monitor.md` |

### 7. State-write discipline — pattern formalization 🟡

| | |
|---|---|
| **Question** | What are the 5+ state-file write-discipline patterns (e.g., additionalProperties: false, monitor-notes parallel files, atomic-write with .bak) and when does each apply? |
| **Why** | We've discovered these patterns organically. Without formalization, future agents will reinvent or violate them. |
| **Method** | (1) Read `~/skills/aiw-state-file-write-discipline/` (skill exists). (2) Catalog every state-file write convention we've established. (3) Document each pattern: name, problem it solves, when to use, example, anti-pattern. (4) Cross-link from each PROMPT.md to the relevant pattern. |
| **Output** | `engineering/state-write-discipline-catalog.md` (pattern catalog) |
| **Owner** | management-coordinator + ai-ops-coordinator |
| **Cadence** | Once + on new pattern |
| **Cross-references** | `~/skills/aiw-state-file-write-discipline/`, `dept-monitors/INDEX.md`, every schema in `schemas/` |

### 8. Cron heartbeat on/off-hours patterns 🟡

| | |
|---|---|
| **Question** | What's the right cron heartbeat frequency: 15min during business hours vs 30min off-hours, and how do we balance thoroughness vs cost? |
| **Why** | We have `aiw-cron-heartbeat-onhours` (30min, 06:00-22:00) and `aiw-cron-heartbeat-offhours` (15min, 23:00-05:00). The off-hours is actually more frequent — counter-intuitive. |
| **Method** | (1) Read the heartbeat skill at `~/skills/aiw-cron-monitor-tick/`. (2) Compare: actual error detection latency vs the cost of running heartbeat (LLM tokens). (3) Find the right balance. (4) Document the heartbeat-strategy. |
| **Output** | `engineering/cron-heartbeat-strategy.md` (frequency choices + cost/benefit analysis) |
| **Owner** | management-coordinator + Ivan |
| **Cadence** | Once + quarterly review |
| **Cross-references** | `~/skills/aiw-cron-monitor-tick/`, `docs/phases/PHASE-25-*` |

---

## 🔵 COOL areas

### 9. MCP / interop protocol maturity tracking 🔵

| | |
|---|---|
| **Question** | Which MCPs (Model Context Protocols) and interop standards should AI Whisperers depend on, given that some are still pre-stable? |
| **Why** | Long-term: avoid lock-in to unstable protocols. Short-term: don't block on stable ones. |
| **Method** | (1) Catalog MCPs we use (look at `hermes-agent/pyproject.toml`). (2) For each: maturity (alpha/beta/stable), alternatives, lock-in risk. (3) Recommend: keep / replace / wait. |
| **Output** | `engineering/mcp-maturity-tracking.md` (per-MCP assessment) |
| **Owner** | engineering-roster |
| **Cadence** | Quarterly |
| **Cross-references** | `hermes-agent/pyproject.toml`, `research/30-research-areas.md` #19 |

### 10. Open-source AI dependency audit 🔵

| | |
|---|---|
| **Question** | What OSS AI dependencies (models, libraries, MCPs) do we use, what's their license + CVE status, and what's our license-compliance posture? |
| **Why** | `pip-audit` + `npm audit` exist (per `04-engineering/security-auditor/PROMPT.md`) but never ran on our actual dependencies. We don't know if we have CVEs. |
| **Method** | (1) Run `pip-audit --format json` on every Python project. (2) Run `npm audit --json` on every Node project. (3) Aggregate CVE list. (4) For each: severity (CVSS), fix availability, owner decision (patch now / wait / accept). (5) Build OSS-dependency dashboard. |
| **Output** | `engineering/oss-dependency-audit.md` (per-project CVE table + decisions) |
| **Owner** | security-watchdog + ai-safety-engineer |
| **Cadence** | Quarterly + on new dependency |
| **Cross-references** | `04-engineering/security-auditor/PROMPT.md`, `research/30-research-areas.md` #21 |


---

## Cross-reference index

- **Methodology**: `research/DEPT-RESEARCH-METHODOLOGY.md`
- **12-factor audit** (Phase 21): `docs/phases/PHASE-21-*`
- **Around-the-clock upgrade** (Phase 25): `docs/phases/PHASE-25-*`
- **Prompt analysis**: `research/PROMPT-ANALYSIS.md`
- **Org-wide 30-research**: `research/30-research-areas.md` (Areas 5, 10, 19, 21, 24 owner: eng)
- **State-write discipline skill**: `~/skills/aiw-state-file-write-discipline/`
- **Cron monitor skill**: `~/skills/aiw-cron-monitor-tick/`
- **Pattern 22 monitor-notes-rollover**: `~/skills/pattern-22-monitor-notes-rollover/`
- **Sibling dept catalogs**: `research/dept-research/{01..03,05,06,board}-*-research-areas.md`

---

**Total engineering research areas**: 10
**Cadence breakdown**: 🔴 HOT 3, 🟡 WARM 5, 🔵 COOL 2
**Built**: 2026-09-01 by Erebus (per Phase 7 plan)

