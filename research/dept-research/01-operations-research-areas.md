# Department of Operations — Research Catalog

> **Built 2026-09-01** as part of Phase 7 (research deepening).
>
> **Department head**: Ivan | **Lead agent**: `management-coordinator` | **Atomic agents**: `kronos-operations-lead`, `bizops-tracker`, `argus-health-monitor`
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern + depth test).
>
> **Status**: 6 areas documented. Cadence tiers balanced across 🔴 HOT (3), 🟡 WARM (2), 🔵 COOL (1).

---

## Reading guide

This catalog lists the research areas specific to the **Operations department** — the function that runs the org day-to-day. Operations research differs from other depts because it's mostly **observability research** ("are the systems running correctly?") rather than external market research.

Areas are grouped by the 4 universal themes (internal / market / literature / actionable).

---

# Operations Research Areas



## 🔴 HOT areas

### 1. Self-running org criteria — the 7-system test 🔴

| | |
|---|---|
| **Question** | Does the org actually run itself for 7+ days without Ivan doing manual interventions? |
| **Why** | The whole "AI-native 2-person org" thesis depends on this. If we miss the test, we haven't built an org — we've built a more complex to-do list. |
| **Method** | (1) Read `docs/SELF-RUNNING-CRITERIA.md` (the 7 criteria). (2) For each criterion, find the monitoring signal in `state/*.json` + `PROMPT-monitor.md`. (3) Run a 7-day evaluation where Ivan records every manual intervention. (4) Score pass/fail per criterion. (5) Build a "self-running scorecard". |
| **Output** | `operations/self-running-scorecard-2026.md` (markdown table, 1 page) |
| **Owner** | management-coordinator agent + Ivan |
| **Cadence** | Monthly for first 3 months, then quarterly |
| **Cross-references** | `docs/SELF-RUNNING-CRITERIA.md`, `analysis/L1-AUTONOMOUS-PRECHECKS-2026-09.md`, every dept-lead's PROMPT-monitor.md |

### 2. Hard-stops wrapper enforcement audit 🔴

| | |
|---|---|
| **Question** | Why does `patterns/hard-stop-wrapper.py` exist but is invoked by 0 of the 49 production agents? |
| **Why** | The L1 audit found that hard-stops are 100% advisory. This means **if an LLM call would do something destructive (write state, send email, deploy code), nothing physically stops it**. That's a safety hole masquerading as a safety feature. |
| **Method** | (1) grep all 49 PROMPT.md files for `hard-stop-wrapper` references. (2) Read each cron job's prompt to see if the wrapper is mentioned. (3) Test: does `python3 patterns/hard-stop-wrapper.py` actually block the actions the docs say it should? (4) Recommend: either invoke the wrapper or remove it. |
| **Output** | `operations/hard-stops-enforcement-audit.md` (findings + recommended fix) |
| **Owner** | ai-ops-coordinator agent + engineering-roster + Ivan |
| **Cadence** | Once now, then quarterly verification |
| **Cross-references** | `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` (surprise #1), `docs/THREAT-MODEL.md`, `docs/FAILURE-MODES.md` |

### 3. Cron heartbeat anomaly patterns 🔴

| | |
|---|---|
| **Question** | What are the recurring failure patterns in our 131 cron jobs and which ones recur week-over-week? |
| **Why** | The L1 audit surfaced `cron_error_watchdog.json` records stale entries. Without analysis, we don't know if these are 1-time errors or systemic. |
| **Method** | (1) Parse `/opt/data/state/cron-error-watchdog.json` for the last 30 days. (2) Cluster errors by: agent name, error type, time-of-day, day-of-week. (3) Find recurring errors (≥3 occurrences). (4) For each pattern, trace the root cause. (5) Build "top 10 recurring cron errors" report. |
| **Output** | `operations/cron-error-patterns-30d.md` (markdown table + fix recommendations) |
| **Owner** | management-coordinator agent + ai-ops-coordinator |
| **Cadence** | Monthly |
| **Cross-references** | `state/cron-error-watchdog.json`, every agent's PROMPT-monitor.md, `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` (surprise #7) |

---

## 🟡 WARM areas

### 4. Department monitor matrix calibration 🟡

| | |
|---|---|
| **Question** | Are the 16 dept-monitors' threshold rules tuned to reality (no false positives, no missed events)? |
| **Why** | The Phase 5 monitors use educated-guess thresholds. After 30 days of real data, we'll know which are too tight (alert fatigue) or too loose (missed events). |
| **Method** | (1) Read all 16 PROMPT-monitor.md files. (2) Cross-reference the threshold rules against actual state files. (3) For each rule, calculate: how often does it fire on real data? Is that the right cadence? (4) Recommend threshold adjustments. (5) Update PROMPT-monitor.md with calibrated values. |
| **Output** | `operations/monitor-threshold-calibration-2026.md` (table per monitor with old/new threshold + rationale) |
| **Owner** | ai-ops-coordinator + each dept-lead |
| **Cadence** | Quarterly after first month of data |
| **Cross-references** | `dept-monitors/INDEX.md`, every dept-lead's PROMPT-monitor.md, `demiurge/kpi/{dept}-stack.yaml` |

### 5. Org-pulse anomaly detection patterns 🟡

| | |
|---|---|
| **Question** | What signals indicate the org is drifting from healthy to unhealthy before the damage is done? |
| **Why** | We have 131 crons + 49 agents + 16 monitors. We need leading indicators (not just lagging) so management-coordinator can escalate before the situation is critical. |
| **Method** | (1) Build a "health dashboard" from existing KPIs in `demiurge/kpi/*.yaml` (39 KPIs). (2) For each KPI, find the historical baseline. (3) Compute z-scores per dept per week. (4) Define "warning zone" (z>1.5) vs "critical" (z>3). (5) Document the dashboard in `operations/health-dashboard.md`. |
| **Output** | `operations/health-dashboard.md` (live KPI view) + drift-detector agent (built Phase 5) |
| **Owner** | management-coordinator + bizops-tracker |
| **Cadence** | Continuous (drift-detector runs daily) |
| **Cross-references** | `04-engineering/drift-detector/PROMPT.md`, `demiurge/kpi/*.yaml`, `analysis/COMPLETE-DEPT-ROLE-HISTORY-2026-09.md` |

---

## 🔵 COOL areas

### 6. Operational maturity model for AI-native orgs 🔵

| | |
|---|---|
| **Question** | Where on a 5-level operational maturity model does AI Whisperers sit, and what's the next level? |
| **Why** | Strategic — informs the next 12 months of operational investment. The org-design literature discusses "AI-native" orgs as a category, but no one's defined maturity levels for them. |
| **Method** | (1) Survey 5-10 AI-native small orgs (look at: Replit, Cursor, Anthropic ops, Hugging Face ops, smaller consultancies). (2) Define 5 levels (e.g., L1 = manual + cron, L2 = cron + monitor, L3 = cron + monitor + auto-remediate, L4 = cron + monitor + auto-remediate + cross-system correlation, L5 = cron + monitor + auto-remediate + proactive optimization). (3) Score AI Whisperers against the model. (4) Recommend the next level's prerequisites. |
| **Output** | `operations/maturity-model-2026.md` (5-level model + AIW score) |
| **Owner** | management-coordinator + Ivan |
| **Cadence** | Once + annual review |
| **Cross-references** | `research/org-design-literature.md`, `docs/SELF-RUNNING-CRITERIA.md`, `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` |


---

## Cross-reference index

- **Methodology**: `research/DEPT-RESEARCH-METHODOLOGY.md`
- **Org-wide research**: `research/30-research-areas.md` (30 areas)
- **Coaching research**: `research/30-coaching-research-areas.md` (30 areas)
- **Org design literature**: `research/org-design-literature.md`
- **Failure modes**: `docs/FAILURE-MODES.md`
- **Self-running criteria**: `docs/SELF-RUNNING-CRITERIA.md`
- **Threat model**: `docs/THREAT-MODEL.md`
- **12-factor audit**: `docs/phases/PHASE-21-*-audit*`
- **Phase 25 around-the-clock**: `docs/phases/PHASE-25-*`
- **L1 autonomous prechecks**: `analysis/L1-AUTONOMOUS-PRECHECKS-2026-09.md`
- **Sibling dept catalogs**: `research/dept-research/{02..06,board}-*-research-areas.md`

---

**Total operations research areas**: 6
**Cadence breakdown**: 🔴 HOT 3, 🟡 WARM 2, 🔵 COOL 1
**Built**: 2026-09-01 by Erebus (per Phase 7 plan)

