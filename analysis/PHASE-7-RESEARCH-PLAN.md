# Phase 7 — Per-Dept Research Deepening Plan

> **Date**: 2026-09-01
> **Trigger**: Ivan's request "do all of this and research for all the areas more in depth also research methodologies and all the department relevant researches we should do for each department"
> **Selected scope** (per Ivan's multi-select): (1) Deepen existing research, (2) Build per-dept research catalogs
> **Deferred**: Tier-3 dept expansion (correctly deferred per doctrine)

---

## What exists today (the "before" state)

### Org-wide research (~30 areas already enumerated)
- `research/30-research-areas.md` — 30 areas with Why/Method/Output/Owner/Cadence
- `research/30-coaching-research-areas.md` — 30 coaching-specific areas
- `research/org-design-literature.md` — 20+ sources synthesis
- `research/1000-company-questions.md` — 1652-line discovery framework
- `research/STRATEGY.md` — 6-part org strategy

### Per-topic research
- `research/funding-landscape-2026-Q3.md` (38KB) — finance topic
- `research/alternative-income-2026-Q3.md` (58KB) — finance topic
- `research/200-ai-companies.md` — sales/competitive topic
- `research/200-ai-coaching-companies.md` — sales/coaching topic
- `research/coaching-funnel-playbook.md` — sales/coaching topic
- `research/PROMPT-ANALYSIS.md` — engineering/agent topic

### Per-dept research (mostly missing)
- `01-operations/` — no dedicated research doc (uses SELF-RUNNING-CRITERIA.md in docs/)
- `02-finance-legal/` — funding-landscape covers most of it
- `03-sales-growth/` — 200-ai-companies covers some
- `04-engineering/` — engineering has docs/phases/PHASE-21, 25 etc.
- `05-research-education/` — some scattered
- `06-people-culture/` — kiki/coaching research scattered
- `board-of-directors/` — nothing

---

## Plan — 3 sequential rounds

### Round 1 — Per-dept research methodology template

Create `research/DEPT-RESEARCH-METHODOLOGY.md` (shared template):
- Define the 7-question pattern every dept research should answer
- Owner-by-dept mapping
- Cross-references to existing research
- The "depth test" (4 levels: enumerate → analyze → synthesize → recommend)

### Round 2 — Per-dept research catalog (7 files, one per dept)

For each of the 7 Tier-1 dirs + board, write `research/dept-research/{dept}-research-areas.md` with:
- 10-20 specific research areas/questions for that dept
- Methodology per area (How/Output/Owner/Cadence)
- Cross-reference to existing research in `research/`
- Gap analysis: what exists vs. what's needed

### Round 3 — Deepen 4 highest-value existing research files

Pick the 4 most-strategic existing files and deepen them with:
- Current data (2026-08-31 state)
- Cross-references to the new dept-specific catalogs
- Action items extracted from the research

Files to deepen:
1. `research/STRATEGY.md` — add dept-research cross-references
2. `research/coaching-funnel-playbook.md` — add sales-dept catalog link
3. `research/funding-landscape-2026-Q3.md` — add finance-dept catalog link
4. `research/PROMPT-ANALYSIS.md` — add engineering-dept catalog link

---

## Per-dept research topics (the "what" for Round 2)

### 01-operations (6 research areas)
1. Self-running org criteria (the 7 from SELF-RUNNING-CRITERIA.md, deep dive)
2. Cron heartbeat patterns (failure detection, error recovery)
3. State file write discipline (the "additionalProperties: false" pattern)
4. Department monitor matrix (16 monitors, threshold tuning)
5. Hard-stops wrapper enforcement (currently never invoked - root cause)
6. Org-pulse anomaly detection (broadcast, escalation routing)

### 02-finance-legal (8 research areas)
1. Margin analysis (5 projects × cost × price × margin)
2. Funding landscape refresh (2026 Q3 already done; refresh after each new application)
3. Tax optimization (PY/NL/EU 3-jurisdiction)
4. Pricing benchmark refresh (LATAM AI agencies)
5. Compliance frameworks (LGPD + GDPR + EU AI Act + Trademark)
6. Cashflow projection models (runway scenarios)
7. Spending trends (vendor optimization)
8. Procurement vendor audit

### 03-sales-growth (10 research areas)
1. LATAM AI market sizing (currently in 30-research-areas #8, deepen)
2. ICP validation (customer archaeology from real data)
3. Pricing benchmarks (currently in 30-research-areas #9, deepen)
4. WhatsApp outreach at scale (Evolution API patterns)
5. Sales funnel mechanics (currently DEAD - need revival playbook)
6. Discovery methodology (SPIN/MED vs BANT vs GPCTBA)
7. Proposal templates (per vertical)
8. Customer success playbooks (Tier-3 deferred, but research now)
9. Competitive positioning (per ICP)
10. Lead enrichment patterns (Cadmus + Clio atomic agents)

### 04-engineering (10 research areas)
1. 12-factor compliance audit (Phase 21, refresh post-DEMIURGE)
2. AI safety engineering (hard-stops + eval gates)
3. Drift detection methodology
4. Chaos testing methodology
5. Eval gate architecture (per-agent pass rates)
6. Around-the-clock upgrade methodology (Phase 25)
7. State-write discipline (the additionalProperties: false pattern)
8. Cron heartbeat on/off-hours patterns
9. MCP / interop protocol maturity tracking
10. Open-source AI dependency audit (license + security)

### 05-research-education (8 research areas)
1. Citation discipline (current research/citation-checker)
2. Course production methodology (P1 GeoData v2 thesis)
3. Thesis to product conversion path
4. Academic liaison processes
5. Source-materials curation
6. Hero's journey for curriculum design
7. Peer review and quality gates
8. Publication pipeline management

### 06-people-culture (6 research areas)
1. Ivan bandwidth audit (2-week time tracking)
2. Kiki engineering growth path
3. AI engineer hiring rubric
4. Coaching for engineering leaders (Kiki's methodology)
5. Performance review cadence (biweekly 1:1s)
6. Founder bandwidth optimization (the "founder-bandwidth-watchdog" agent's data)

### board-of-directors (4 research areas)
1. Co-chair decision-making (Ivan + Kiki tiebreaker pattern)
2. Quarterly review structure (board-of-directors cadence)
3. Risk oversight at <$1K MRR
4. Decision rights matrix maintenance

---

## Out of scope

- Tier-3/4 dept expansion (deferred per doctrine)
- Coaching products (live in coach-agents repo)
- Customer Success (Tier-3 deferred)
- Marketing (Tier-3 deferred)

---

## Success criteria

By end of Phase 7:
- 1 shared methodology template (research/DEPT-RESEARCH-METHODOLOGY.md)
- 7 per-dept research catalogs (~50KB each = ~350KB total)
- 4 existing research files deepened with cross-references
- 3 feedback docs (plan + round-1 + round-2-3 combined)
- Lint + smoke gate still 100%
- 1 commit pushed

Estimated time: 90-120 minutes total.
