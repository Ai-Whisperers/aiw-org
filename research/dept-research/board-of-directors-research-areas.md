# Board of Directors — Research Catalog

> **Built 2026-09-01** as part of Phase 7 (research deepening).
>
> **Co-chairs**: Ivan + Kiki (per Ivan's 2026-09-01 clarification; tiebreaker rotates monthly)
> **Agent**: `board-of-directors` (governance layer, not a charter dept)
>
> **Methodology**: Follows `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern + depth test).
>
> **Status**: 4 areas documented. Cadence tiers: 🟡 WARM (3), 🔵 COOL (1).

---

## Reading guide

Board of Directors is **governance** — not a charter dept. It exists to oversee the 6 charter depts + escalate to Ivan/Kiki on HIGH/CRITICAL decisions.

The 4 areas here are different from other dept research: they're about **how decisions get made**, not how work gets done.

---

# Board of Directors Research Areas



## 🟡 WARM areas

### 1. Co-chair decision-making — Ivan + Kiki tiebreaker pattern 🟡

| | |
|---|---|
| **Question** | When Ivan and Kiki disagree on a HIGH/CRITICAL decision, what's the resolution path? (Monthly rotating tiebreaker, escalation to external advisor, consensus-with-deadline, etc.) |
| **Why** | Co-chair model is new (Ivan's 2026-09-01 decision). Without explicit decision-making rules, disagreements stall. |
| **Method** | (1) Survey 5 dual-founder orgs (Stripe, Github early, Basecamp, Buffer, WordPress). (2) For each: their disagreement resolution mechanism. (3) Pick a fit-for-2-person-org pattern. (4) Codify as a 1-page decision-rights matrix. (5) Pilot for 1 quarter. |
| **Output** | `board/co-chair-decision-rights.md` (decision-rights matrix + resolution mechanism) |
| **Owner** | board-of-directors agent + Ivan + Kiki |
| **Cadence** | Once + on first disagreement |
| **Cross-references** | `constitution/ORG-AGENTS.md`, `board-of-directors/PROMPT.md`, `state/coord.json:decisions_for_ivan` |

### 2. Quarterly review structure — what goes on the agenda 🟡

| | |
|---|---|
| **Question** | When the board meets quarterly (Jan/Apr/Jul/Oct, 1st, 14:00 UTC per `board-of-directors/PROMPT.md`), what's the standard agenda + how are decisions documented? |
| **Why** | Quarterly reviews are scheduled but not structured. Without agenda, meetings ramble. Without decision documentation, accountability is lost. |
| **Method** | (1) Read `board-of-directors/PROMPT.md` (schedule). (2) Design 90-min agenda: 5min context, 20min KPIs per dept, 20min risk review, 15min decisions, 15min open, 15min action items. (3) Design template for "decision log" output. (4) Pilot for Q4 2026. |
| **Output** | `board/quarterly-review-template.md` (agenda + decision log template) |
| **Owner** | board-of-directors agent + Ivan |
| **Cadence** | Quarterly (template stable; instance per quarter) |
| **Cross-references** | `board-of-directors/PROMPT.md`, `demiurge/kpi/board-stack.yaml` |

### 3. Risk oversight at <$1K MRR 🟡

| | |
|---|---|
| **Question** | What risks (operational, financial, compliance, security, reputational) does AI Whisperers face TODAY (at $240 MRR), and what's our mitigation per risk? |
| **Why** | Phase 4 L4 gate is unblocked at $1000 MRR. Until then, we need risk oversight at our actual scale. |
| **Method** | (1) Read `docs/THREAT-MODEL.md` (existing 5 actors, 7 threats). (2) For each threat: rate likelihood × impact at $240 MRR scale. (3) Build risk register. (4) For each HIGH-risk: mitigation + owner. (5) Update THREAT-MODEL.md. |
| **Output** | `board/risk-register-2026.md` (per-risk table with mitigation + owner) |
| **Owner** | board-of-directors + ai-safety-engineer + Ivan |
| **Cadence** | Quarterly + on new risk |
| **Cross-references** | `docs/THREAT-MODEL.md`, `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` |

---

## 🔵 COOL areas

### 4. Decision rights matrix maintenance 🔵

| | |
|---|---|
| **Question** | Over time, decision thresholds (USD 50/500/5000/50000) drift from reality. How do we detect drift and recalibrate? |
| **Why** | The decision rights matrix in `constitution/ORG-AGENTS.md` (USD 50 logged / 50-500 surface / 500-5K Ivan / >5K Ivan+Kiki) was set in 2026-08. As org grows, thresholds need periodic recalibration. |
| **Method** | (1) Review the matrix every 6 months. (2) For each threshold: has it been hit? Was the response appropriate? (3) Recalibrate. (4) Document. |
| **Output** | `board/decision-rights-recalibration-2026.md` (threshold review + new values) |
| **Owner** | board-of-directors + Ivan |
| **Cadence** | Bi-annually |
| **Cross-references** | `constitution/ORG-AGENTS.md`, `state/coord.json:decisions_for_ivan` |


---

## Cross-reference index

- **Methodology**: `research/DEPT-RESEARCH-METHODOLOGY.md`
- **Constitution**: `constitution/ORG-AGENTS.md`
- **DECISIONS log**: `DECISIONS-2026-Q3.md` (if exists)
- **Board kpis-stack**: `demiurge/kpi/board-stack.yaml`
- **Board signals**: `demiurge/signals/board-of-directors.yaml`
- **Board PROMPT**: `board-of-directors/PROMPT.md`
- **Sibling dept catalogs**: `research/dept-research/{01..06}-*-research-areas.md`

---

**Total board research areas**: 4
**Cadence breakdown**: 🟡 WARM 3, 🔵 COOL 1
**Built**: 2026-09-01 by Erebus (per Phase 7 plan)

