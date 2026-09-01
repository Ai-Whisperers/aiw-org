# Complete Gap Analysis + Upgrade Plan + Wishlist

> **Date**: 2026-09-01
> **Scope**: Every layer of the AIW org (state, agents, routing, eval, cost, safety, business)
> **Method**: Read every system, inventory what's there, identify what's missing, propose fixes
> **Audience**: Ivan (decision-maker), Kiki (technical executor), future agents

---

## TL;DR

The org has **strong foundations but ~60% of the designed system is not executing**. The architecture is well-documented (PROMPT.md files, dispatch rules, schemas, monitors) but most of the inter-agent plumbing is **declarative, not wired**. Major gaps:

1. **Routing/intake is designed but not built** (per last conversation)
2. **Drift detection has never fired** (no alerts in 30+ days)
3. **Eval gate enforcement is empty** (0 agents tracked)
4. **Cost tracking is estimated, not measured**
5. **Sales pipeline has 0 leads** (per D1=c, deferred to Q1 2027)
6. **Schema coverage is 9/13** (4 state files have no schema)
7. **Hard-stops only declared by 3/63 PROMPTs**
8. **No auto-remediation** (everything requires human approval)

---

## 1. INVENTORY (ground truth from live system)

### 1.1 What we have

| Resource | Count | Notes |
|---|---:|---|
| PROMPT.md files | 63 | Charter dept + sub-agents + DEMIURGE |
| PROMPT-monitor.md | 35 | 56% coverage |
| Cron jobs | 134 | 89 cron-expression, 22 ≤30min interval, 3 ≤5min, 2 >30min |
| Scripts (Python) | 16 | State, eval, cost, etc. |
| Scripts (shell) | 11 | Backup, sync, deploy, etc. |
| Test files | 32 | 119 tests passing |
| JSON schemas | 9 | 13 state files exist, 4 have no schema |
| State files (live) | 29 | Across /opt/data/state + /opt/data/agents/state |
| Research areas | ~52 | Across 7 dept catalogs |

### 1.2 Health snapshot

| Dept | Score | Status |
|---|---:|---|
| Operations | 90/100 | ✓ Best |
| Engineering | 96/100 | ✓ Best (inverted — actually best) |
| Finance | 48/100 | 🟡 |
| Sales | 48/100 | 🟡 (0 leads — D1=c deferred) |
| Research | 58/100 | 🟡 |
| People | 34/100 | 🔴 |
| Board | 34/100 | 🔴 |

### 1.3 Runtime signals

- **Cron errors**: 6/134 in error (95.5% healthy)
- **LLM providers**: 10/24 OK, 14/24 degraded (42% degraded — token-plan exhaustion)
- **Eval data**: 0 evals recorded (eval system has never run)
- **Cost**: $9.79/day = $293.41/mo (estimated, not measured)
- **Drift alerts**: 0 (drift system has never fired)
- **Business**: MRR=$240, runway=null, 0 leads

---

## 2. GAP ANALYSIS (by layer)

### Layer L1 — Hygiene (100% complete ✓)

- Lint: 63/63 PROMPTs ✓
- Smoke gate: 100% pass ✓
- Cron-sync: working ✓
- Tests: 119/119 ✓

**No gaps at L1.**

---

### Layer L2 — Foundation (95% complete)

**Gaps:**

- **G2.1**: PROMPT-monitor.md coverage is 56% (35/63). The 28 unmonitored agents are mostly DEMIURGE atomic agents + sister-repo coaches. Risk: silent failures.
  - Fix: Phase 26 #6 already started (audit), finish with PROMPT-monitor.md for the missing 28.
  - Effort: 8h

- **G2.2**: 4 state files have no schema (`funding.json`, `eval-per-agent.json`, `org-state.json`, `cron-error-watchdog.json`). They can drift silently.
  - Fix: Phase 28 candidate. Generate schemas from current JSON shape.
  - Effort: 4h

- **G2.3**: 16 schema gaps in 4 files (audit found 21 in latest run). Schemas are out of date vs reality.
  - Fix: Update each schema to match live state.
  - Effort: 4h

- **G2.4**: 18+ `.bak` files totaling 10MB in `/opt/data/state/`. `.gitignore` doesn't catch them.
  - Fix: Add `**/*.bak` to gitignore; clean up.
  - Effort: 1h

- **G2.5**: 2 stale tracked files (`outbox/counter.json`, `monitor-notes/_last-tick.json`) not gitignored.
  - Fix: Update gitignore.
  - Effort: 0.5h

- **G2.6**: Hard-stops declared by only **3/63 PROMPTs** (founder-bandwidth-watchdog, devops-monitor-30min, people-hr). 60 agents have no enforcement.
  - Fix: Phase 28 candidate. Generate default hard_stops per agent type.
  - Effort: 8h (Kiki review)

- **G2.7**: Cron-guard pre-commit hook has drift edge cases (caused Phase 27 commit retry).
  - Fix: Make drift check run cron-sync first.
  - Effort: 1h

---

### Layer L3 — Quality (40% complete)

**Built:**
- ✓ 4 PROMPT-monitor.md files with threshold rules (Phase 5)
- ✓ eval-aggregate-pass-rate.py (Phase 8)
- ✓ drift-calibrate.py (Phase 26)
- ✓ chaos-runner.py + 1 scenario PASS (Phase 26)
- ✓ eval-gate-enforce.py (Phase 27)
- ✓ schema-validate-write.py (Phase 27)

**Gaps:**

- **G3.1**: **Drift detection has never fired** — no alerts in 30+ days. Either:
  - (a) The system has zero drift (unlikely)
  - (b) Drift system is misconfigured (likely — no eval data, no schema mismatches caught)
  - (c) Alerts go to a path that's not being checked
  - Fix: Debug drift detector; verify alert pathway; force a synthetic drift to test.

- **G3.2**: **Eval gate has 0 agents tracked**. The eval system is wired but no eval-gate-runner cron has fired yet to populate `eval-per-agent.json`.
  - Fix: Wire `eval-gate-runner` to run on each agent's outbox; backfill historical data; OR start fresh and let it accumulate over 30d.

- **G3.3**: **Chaos engineering has 1/5 scenarios tested**. Scenarios 2-5 (Worker endpoint, LLM provider outage, monitor offline, schema mutation attack) untested.
  - Fix: Run scenario 5 (schema mutation attack) — easiest to test in isolation. Others need Ivan approval (prod-adjacent).

- **G3.4**: **Cost tracking is estimated, not measured**. Cost-tracker.json uses `runs_per_day × cost_per_run_usd` model. Real token usage is not measured at the API layer.
  - Fix: Add actual-token-usage reporting to agent execution layer.

- **G3.5**: **No quality trending**. We have point-in-time eval-aggregate but no time-series. Drift-calibrate is the only trending script, and it has 0 alerts.
  - Fix: Add weekly eval aggregate snapshots to a `state/eval-history/` directory.

- **G3.6**: **Hard-stops wrapper has bugs** (per BUG-HUNT C1: audit log no lock). Even though wrapper is now functional, audit trail is unreliable.
  - Fix: C1 fix (add file lock or use NDJSON append-only).

- **G3.7**: **State-write.sh has injection vector** (per BUG-HUNT M3). Heredoc with unquoted vars.
  - Fix: Use single-quoted heredoc + printf.

---

### Layer L4 — Self-running Org (DEFERRED per gate)

**Gate**: $1000+ MRR OR 30 days of L1-L3 stability.

**Current**: MRR=$240 + 0d L3 stability.

**Time to gate**: 4-8 months at current burn.

**Design is done** (per `OPERATIONS.md`); just needs L3 maturity first.

---

### Layer L5 — Soul-Improvement (DEFERRED per gate)

**Gate**: L4 fully operational for 30+ days.

**No design yet.**

---

## 3. INTER-DEPARTMENT AUTOMATION GAPS (the "secretary" question)

This is what you asked about. **The answer: partial + mostly designed, not built.**

### 3.1 What exists (declarative, not executing)

| Component | Status | Location |
|---|---|---|
| Composition field | ✓ Declared in all 63 PROMPT.md | "This agent calls: hermes-router-revenue, kronos-operations-lead" |
| Transfer targets | ✓ Declared | "Hand off to: sales-pipeline, finance-controller" |
| Dispatch rules | ✓ YAML (11+ rules) | `demiurge/router/dispatch-rules.yaml` |
| Timing rules | ✓ YAML | `demiurge/router/timing-rules.yaml` |
| Revenue signals | ✓ YAML | `demiurge/router/revenue-signals.yaml` |
| Hermes router PROMPT | ✓ Exists | `demiurge/agents/hermes-router-revenue/PROMPT.md` |
| Task DB table | ✓ Schema exists | `dashboards/dashboard-server.py` (tasks table) |
| Tier-2 leads | ✓ Apollo, Kronos, Athena, Hera | `demiurge/agents/` |
| Dept-lead monitors | ✓ 7 dept-leads monitored | Phase 5 |

### 3.2 What does NOT exist (gaps)

- **G3.8**: **No router executor**. `scripts/router.py` does not exist. No code reads `dispatch-rules.yaml` + matches signals + dispatches.
- **G3.9**: **No cron triggers Hermes Router**. `hermes-router-revenue` PROMPT exists but no cron invokes it.
- **G3.10**: **No intake agent**. There's no first-pass triager that breaks incoming signals into tasks + assigns them.
- **G3.11**: **No task writer**. Dashboard has `tasks` table but 0 INSERT INTO tasks. Nothing writes tasks for sub-agents.
- **G3.12**: **No results collector**. Sub-agent outputs go to outbox/ but nothing reads them, verifies against original signal, escalates failures.
- **G3.13**: **No quorum logic**. The router PROMPT says "Track quorum; execute fallback on timeout" but no code does this.
- **G3.14**: **No inter-agent messaging**. Each agent writes to its own outbox; no message queue, no pub/sub, no agent-to-agent handoff.
- **G3.15**: **No "secretary" / chief-of-staff pattern**. Each dept-lead PROMPT says it manages sub-agents, but no agent is explicitly the chief-of-staff or executive-assistant pattern.

### 3.3 What's actually happening (current runtime model)

```
cron → agent's PROMPT → LLM call → outbox/<date>.md → human reads
```

**Broadcast model.** No inter-agent communication. No routing. No task passing. No quorum. **Ivan is the human router** — he reads outboxes, decides what matters, takes action.

### 3.4 What the design implies (target model)

```
signal → router (matches dispatch-rules) → dept-lead (intake) → sub-agent (executes) → results-collector (verifies) → outbox/<date>.md
```

**Routed model.** Signals flow through a queue. Router applies rules. Intake agent assigns to sub-agents. Sub-agents do work. Results collector verifies. Outbox has verified results.

---

## 4. AUTOMATION WISHLIST (priority order)

### Tier A: Foundation gaps (do first, ~25h total)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| A1 | Wire router (read dispatch-rules + match signals) | 8h | Routing starts working |
| A2 | Wire intake per dept (chief-of-staff pattern) | 8h | Tasks get assigned |
| A3 | Wire results-collector | 4h | Outputs verified |
| A4 | Add 28 missing PROMPT-monitor.md | 8h | 100% monitoring coverage |
| A5 | Add 4 missing JSON schemas | 4h | 100% schema coverage |
| A6 | Refresh 4 out-of-date schemas (16+5 gaps) | 4h | Schemas match reality |
| A7 | Fix audit log file lock (BUG-HUNT C1) | 1h | Audit trail reliable |
| A8 | Fix state-write.sh heredoc (BUG-HUNT M3) | 1h | No injection vector |
| A9 | Clean up .bak files + gitignore | 1h | Clean state dir |
| A10 | Add chaos scenarios 2-5 (with approval) | 8h | Full chaos coverage |

### Tier B: Decision support (~20h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| B1 | Build cost trend dashboard (weekly) | 4h | See cost over time |
| B2 | Build eval trending dashboard | 4h | See quality over time |
| B3 | Build health score trending | 4h | See health over time |
| B4 | Build "what changed since last brief" tool | 4h | Auto-diff weekly briefs |
| B5 | Add Ivan bandwidth dashboard | 4h | See founder time usage |

### Tier C: Business automation (~30h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| C1 | Lead intake form (replaces rubicon-eas Worker) | 4h | Sales pipeline unblocked |
| C2 | Auto-discovery from new leads (Apollo + Cadmus) | 4h | New leads get enriched automatically |
| C3 | Auto-proposal drafting (Metis) | 4h | Proposals auto-drafted |
| C4 | Auto-invoicing on contract signed | 4h | Billing automated |
| C5 | Auto-renewal tracking | 4h | Renewals tracked |
| C6 | Auto-compliance check on outbound | 4h | Compliance enforced |
| C7 | Auto-trademark scrub on content | 4h | Trademark issues caught |
| C8 | Auto-financial reports (weekly) | 4h | CFO automation |

### Tier D: Research/Education (~25h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| D1 | Thesis active chapter tracking | 4h | Auto progress reports |
| D2 | Citation checker on every draft | 4h | Citations enforced |
| D3 | Course module draft → publish pipeline | 4h | Course production automated |
| D4 | Research-to-product conversion tracker | 4h | See which research becomes paid |
| D5 | Auto literature scan weekly | 4h | Stay current |
| D6 | Auto-format conversion (MD → PDF, MD → video) | 4h | Multi-format output |
| D7 | Student progress tracking (if coaching product grows) | 4h | Per-student dashboard |

### Tier E: People/Culture (~15h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| E1 | Kiki growth path tracker | 4h | See Kiki's skill progress |
| E2 | Auto-feedback collection (after every brief) | 4h | Quality feedback loop |
| E3 | Auto-engagement scoring | 4h | Detect burnout early |
| E4 | Auto-retention analysis | 4h | Who might leave |

### Tier F: Board/Governance (~15h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| F1 | Co-chair decision queue (Ivan + Kiki) | 4h | Decisions tracked |
| F2 | Quarterly review automation | 4h | Reviews auto-generated |
| F3 | Risk register live updates | 4h | Risks auto-scored |
| F4 | Constitutional amendment workflow | 4h | Doc changes tracked |

### Tier G: Engineering improvements (~25h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| G1 | Eval aggregate cron wiring + 30d data | 2h | Real eval data |
| G2 | Eval gate enforcement (block low-pass) | 4h | Quality enforced |
| G3 | Hard-stops wrapper for ALL destructive agents | 16h | 60 agents protected |
| G4 | Self-validating heartbeat | 4h | Detect heartbeat failures |
| G5 | Auto-remediation for known errors | 8h | Common errors auto-fixed |
| G6 | Schema migration tooling | 4h | Auto-update schemas |
| G7 | Cost optimization (find unused capacity) | 4h | Lower $/mo |

### Tier H: AI Safety (~25h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| H1 | Prompt injection detection on inbound | 4h | Defense layer 1 |
| H2 | PII redaction on outbound | 4h | Privacy enforced |
| H3 | Action whitelisting (not just blacklisting) | 8h | Default-deny mode |
| H4 | Audit trail review (weekly) | 4h | Catch policy violations |
| H5 | Red-team scenarios (adversarial test) | 4h | Stress-test defenses |
| H6 | Credential rotation automation | 4h | Secrets rotated on schedule |

### Tier I: User-facing features (~25h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| I1 | Public website (replacing rubicon-eas Worker) | 8h | Marketing surface |
| I2 | Customer dashboard | 8h | Customer self-service |
| I3 | Customer feedback loop | 4h | CSAT measurement |
| I4 | Mobile-friendly brief format | 4h | Read on phone |
| I5 | Voice summaries (TTS) | 4h | Audio brief option |

### Tier J: Analytics & observability (~20h)

| # | Item | Effort | Outcome |
|---|---|---:|---|
| J1 | Per-agent execution time tracking | 4h | Slow agents identified |
| J2 | Token usage per agent per run | 4h | Real cost (not estimate) |
| J3 | Outbox reading patterns (which gets read first) | 4h | Content prioritization |
| J4 | Decision latency (time from surfaced to decided) | 4h | Decision throughput |
| J5 | Brief quality scoring (manual → automated) | 4h | Scale quality measurement |

---

## 5. UPGRADE PLAN (recommended sequencing)

### Phase 28 — Foundation fixes (2 weeks)

**Goal**: Fix all Tier A items. Close L2 + L3 gaps.

**Week 1**:
- A7, A8, A9 (quick wins, 3h)
- A4 (28 monitors, 8h)
- A5, A6 (5 schemas, 8h)

**Week 2**:
- A1, A2, A3 (router/intake/collector, 20h)

**Deliverable**: 100% L2 coverage. First inter-agent routing working.

---

### Phase 29 — Decision support + business (3 weeks)

**Goal**: Add observability + unblock sales.

**Week 3-4**:
- B1-B5 (dashboards, 20h)

**Week 5**:
- C1-C4 (sales automation, 16h)

**Deliverable**: Ivan has visibility. Sales pipeline unblocked.

---

### Phase 30 — AI safety + engineering quality (2 weeks)

**Goal**: Close AI safety gaps.

**Week 6**:
- G1, G2, G4, G5 (quality, 18h)

**Week 7**:
- H1-H6 (safety, 28h)

**Deliverable**: Hard-stops on all 60 unprotected agents. PII/prompt-injection defenses.

---

### Phase 31 — L4 readiness (4 weeks)

**Goal**: Hit L4 gate ($1000 MRR or 30d L1-L3 stability).

**Week 8-11**:
- C5-C8 (financial automation, 16h)
- D1-D7 (research automation, 28h)
- E1-E4 (people automation, 16h)

**Deliverable**: Org runs itself for 7 days with 0 "is X live?" messages from Ivan.

---

### Phase 32 — L5 design (1 week)

**Goal**: Design soul-improvement layer.

**Week 12**:
- L5 design doc
- Identify triggers for soul-improvement (e.g., "agent improves its own prompt based on eval history")

**Deliverable**: L5 design ready for implementation when L4 gate fires.

---

## 6. EFFORT + COST ESTIMATE

| Phase | Weeks | Effort | Cost (at $50/hr blended) |
|---|---:|---:|---:|
| Phase 28 | 2 | 60h | $3,000 |
| Phase 29 | 3 | 60h | $3,000 |
| Phase 30 | 2 | 50h | $2,500 |
| Phase 31 | 4 | 80h | $4,000 |
| Phase 32 | 1 | 10h | $500 |
| **Total** | **12 weeks** | **260h** | **$13,000** |

At 2-person org (Ivan + Kiki) part-time (~20h/week combined):
- Calendar time: ~26 weeks (~6 months)
- Cost: ~$13K (mostly opportunity cost of Ivan's time)

---

## 7. ROI ANALYSIS

**Without automation** (current state):
- Ivan reads ~10 outboxes/day = 30 min/day = 15h/month
- Ivan makes decisions on 5+ items/week = 5h/week = 20h/month
- Sales pipeline at 0 leads = $0 revenue
- Cost: $293/mo + Ivan's opportunity cost

**With Phase 28-29** (foundation + decision support):
- Ivan reads 1 consolidated brief/day = 5 min/day = 2.5h/month
- Ivan makes decisions on 2-3 items/week = 2h/week = 8h/month
- Sales pipeline recovers = +$1K-3K MRR
- Cost: $300/mo + less Ivan time
- **Net: +$700-2700/mo + 24h/month Ivan time saved**

**With Phase 28-31** (full automation):
- Ivan reads 0 outboxes (alerts only) = 1h/week
- Decisions auto-escalated = 30 min/week
- Sales pipeline running = +$3K-10K MRR
- Cost: $400/mo (more agents but more revenue)
- **Net: +$2.6K-9.6K/mo + 100h/month Ivan time saved**

**L4 gate fires** at ~$1K MRR. Currently $240. Need 4× growth.

---

## 8. RISKS

| Risk | Mitigation |
|---|---|
| Phase 28 introduces bugs | Each Tier A item has tests; smoke gate before commit |
| Kiki bandwidth insufficient | Tier A items are mostly Ivan's work; Kiki reviews |
| Sales pipeline revival (D1=c) means no revenue growth | Workaround: lead intake form (C1) unblocks without Worker revival |
| LLM providers degraded (14/24) | Tier H (cost optimization) + manual credit topup |
| Cron errors persist (6/134) | Phase 28 #6 + #7 already addressed |

---

## 9. WISHLIST (not on critical path, but valuable)

| # | Wish | Why | Effort |
|---|---|---|---:|
| W1 | Self-documenting system (agent introspects + writes its own docs) | Reduces doc maintenance | 16h |
| W2 | Agent prompt versioning + A/B testing | Tests prompt changes safely | 16h |
| W3 | Agent "memory" across sessions (vector DB) | Smarter context per agent | 24h |
| W4 | Multi-modal briefs (charts, tables, screenshots) | Better decision-making | 16h |
| W5 | Mobile app for Ivan (push notifications) | Read briefs anywhere | 24h |
| W6 | Slack/Discord bridge for Ivan's preferred channel | Replaces WhatsApp | 16h |
| W7 | Auto-translation (English ↔ Spanish) | Kiki prefers Spanish | 16h |
| W8 | Auto-summarization of long documents | Save Ivan reading time | 8h |
| W9 | Sentiment analysis on inbound signals | Detect angry customers early | 8h |
| W10 | Auto-thesis writing assistant | Thesis is 18mo away from deadline | 16h |
| W11 | Auto-grant-application writing | Apply to 10 grants/month | 16h |
| W12 | Auto-investor update emails | Monthly investor comms | 8h |

---

## 10. DECISIONS NEEDED

| Decision | Owner | Options | Recommendation |
|---|---|---|---|
| Should we build router/intake now or wait for revenue? | Ivan | (a) build now (b) defer to L4 (c) build minimal version | **a** (closes biggest gap, unblocks future work) |
| Should I expand to 12 weeks or cut to 8? | Ivan | (a) 12 weeks full (b) 8 weeks core (c) 4 weeks foundation only | **b** (8 weeks for Phase 28-30, defer Phase 31-32) |
| Tier B/C/D/E priority | Ivan + Kiki | (a) all equal (b) revenue first (b) safety first | **b** (sales + safety = revenue + risk reduction) |
| Should we hire (FTE) to accelerate? | Ivan | (a) yes (b) no | Defer until L4 fires |

---

## Cross-references

- `analysis/BUG-HUNT-2026-09-01.md` — 31 bugs to fix
- `analysis/PHASE-27-FEEDBACK.md` — Phase 28 candidates
- `analysis/PHASE-26-FEEDBACK.md` — original 30 research areas
- `OPERATIONS.md` — org operational runbook
- `department-index.md` — per-dept file map
- `REVIEW-2026-Q4.md` — quarterly review
- `constitution/ORG-AGENTS.md` — agent matrix
- `deferred-roles.md` — triggers for un-built departments
- `demiurge/router/dispatch-rules.yaml` — routing rules (declared, not executed)
