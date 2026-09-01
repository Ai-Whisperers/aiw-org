# Engineering & Research Depts — Implementation Plan (Filtered)

> **Built 2026-09-01** — Phase 7 R4 (decision + plan).
>
> **Purpose**: Filter the 3 prior research docs (charter + 2 v2 catalogs +
> compiled findings) through Ivan's doctrine ("don't care about EU AI Act /
> compliance theater"). Decide what is relevant vs noise. Produce a concrete,
> prioritized implementation plan with file paths, agent names, and timing.
>
> **Replaces**: nothing. Supersedes the recommendations in
> `04-05-compiled-findings.md` with a **filtered, opinionated** plan.
>
> **Methodology**: Direct, decisive, gated to AIW's actual state ($240 MRR,
> 2 people, 131 cron jobs, L1-L3 wired, L4-L5 deferred per gate).

---

## Reading guide

1. **The doctrine** — what AIW is and isn't
2. **What's RELEVANT** — kept from the research wave
3. **What's NOISE** — explicitly rejected (with reasons)
4. **The implementation plan** — phased, file-paths, agents, timing
5. **What this plan does NOT do** — explicit scope guard

---

## 1 — The doctrine (AIW as it actually is)

Per `OPERATIONS.md`, `ORCHESTRATION.md`, `ORG-AGENTS.md`:

- **2-person co-founder org** (Ivan + Kiki)
- **$240 MRR** (per `state/finance.json`); gate to L4 is **$1000+ MRR + 30d L1-L3 stability**
- **49 agents** across **6 charter depts + 1 board**
- **131 cron jobs**, **35 PROMPT-monitors**
- **L1-L3 wired**; **L4-L5 deferred per gate** (this is *the doctrine* — don't promote what's not earned)
- **5-layer model**: Hygiene → Foundation → Quality → Self-run Org → Soul-Improvement
- **State discipline**: 7 patterns (P1-P7) in `engineering/state-write-discipline-catalog.md`
- **Phase 3 just wired**: two-phase build pipeline (architect-agent → router → auditor-agent)
- **Storage**: 3-layer (L1 JSON, L2 SQLite, L3 per-agent git — L3 not yet auto-created)

**The key implication for any "research-driven" plan**: anything that doesn't move us toward **L3 quality** or the **L4 unlock triggers** ($1000 MRR, 30d stability) is premature.

---

## 2 — What's RELEVANT (kept from research wave)

Filtered through Ivan's doctrine. These are the things that map onto **real work AIW needs to do**.

### R1 — Team Topologies (Skelton + Pais 2019) — **RELEVANT**

**Why**: Our PROMPT frontmatter already has `topology:` field (stream-aligned /
platform / enabling / complicated-subsystem). Team Topologies gave us the
vocabulary. Confirms our `devops-monitor` is correctly tagged "platform".

**Concretely adopted in v2 catalog**: 4 team types mapped to our agents.
**No new build needed.** Read-only reference.

### R2 — DORA / Accelerate 4 metrics — **RELEVANT but partially premature**

**Why**: We have `scripts/eval-aggregate-pass-rate.py` (Phase 8) for
pass_rate, but no deploy frequency, no lead time, no MTTR tracker.

**Concrete adoption** (per Phase 7 R3 finding):
- Build `scripts/dora-metrics-aggregator.py` — computes the 4 DORA metrics
  from git log + deploy log + incident log. **Effort: 4 hours.**
- Wire as cron `aiw-dora-metrics-weekly` (Monday 09:00 PYT).

### R3 — Google SRE book principles — **RELEVANT for the SLO piece**

**Why**: SLO/error-budget thinking is the missing piece in our SRE posture.
We have monitors but no SLOs. Per `04-engineering/v1 research area #1` and
our own `04-engineering-delivery.md` line 1 — "12-factor compliance
re-audit post-DEMIURGE" is HOT.

**Concrete adoption**:
- Build `scripts/slo-error-budget-tracker.py` — computes SLO per service
  (availability + latency), tracks budget, alerts when <25%. **Effort: 1 day.**
- Wire as cron `aiw-slo-tracker-daily` (08:00 PYT).
- Apply to: `nexaparaguay.com.py`, `ometzdental.com`, + 5 most-critical
  client sites.

### R4 — theorgchart.com Run/Build/Enable split — **RELEVANT, validates our model**

**Why**: We already have this implicitly. The 3-cluster classification
matches our 13 wired agents exactly (Run = monitors; Build = deploys;
Enable = scope-intake/feasibility-gate).

**Concrete adoption** (per Phase 7 R3 R1):
- Add `cluster:` field to PROMPT.md frontmatter. **Effort: 1 hour.**
- This is a discoverability win — not a functional change.

### R5 — kdeldycke/awesome-engineering-team-management — **RELEVANT as reference**

**Why**: The "Building Teams" + "Engineering" + "KPIs/OKRs" + "Re-organizations"
sections are practical reading. The "Paper we love: Software Engineering
Organizations" pointer to academic papers on eng orgs is the bridge we need.

**Concrete adoption**: add to Engineering dept's reading list in PROMPT.md
or charter. **Effort: 30 min.** No new code.

### R6 — TnTo/awesome-research (academic tools canon) — **PARTIALLY RELEVANT**

**Why**: We're a small org; Zotero/Overleaf/ORCID are real tools we'd use
when publishing. The subset that matters NOW:

- **arXiv** ✅ already used via `~/skills/arxiv/`
- **Connected Papers** ✅ cited in research areas
- **LanguageTool** 🟡 = open-source Grammarly alternative; peitho is similar
- **Zotero** 🟡 deferred until first paper
- **ORCID** 🟡 deferred until first paper
- **OpenAlex** 🟡 useful for citation verification at scale
- **OJS (Open Journal Systems)** 🟡 useful when first paper submitted

**Concrete adoption**:
- NOW: nothing. We don't publish yet.
- WHEN FIRST PAPER: install Zotero + ORCID + register OJS instance (2 days).

### R7 — MDPI 2026 KM paper (5 KM factors) — **PARTIALLY RELEVANT**

**Why**: The KU (Knowledge Utilization) gap finding is real — we capture
knowledge well, but our weekly briefs don't drive action.

**Concrete adoption**:
- Add `## What should we DO with this?` section to every research-tracker
  weekly brief outbox template. **Effort: 30 min.**
- This is the cheapest KU intervention — forces action-oriented briefs.

### R8 — Meta FAIR / DeepMind Research Engineer vs Research Scientist distinction — **RELEVANT**

**Why**: Our ROLES-INVENTORY has 5.2 (Researcher) and 5.10 (Research Engineer
— Tier-2 deferred). The DeepMind description maps cleanly: Researcher =
"creative, hold PhD, scientific questions"; Research Engineer =
"experimentalist, bridge between theory and implementation".

**Concrete adoption**: no new build; the role definitions in ROLES-INVENTORY
already match. The distinction becomes important **when we hire FTE**.

### R9 — Meta FAIR $184K-$257K pay range — **RELEVANT, file for later**

**Why**: When we hire the first FTE (per the open question in
`research/org-design-literature.md` §7 Q1), we need a pay-band reference.
Not relevant now (no hire).

**Concrete adoption**: write `people-hr/pay-band-research-2026.md` with
Meta FAIR / DeepMind / Allen ranges + Paraguay cost-of-living adjustment.
**Effort: 1 hour.** Defer until first FTE trigger.

### R10 — MIT Career Ladders (3 research role tracks) — **RELEVANT, file for later**

**Why**: Maps Research Scientist / Research Engineer / Research Associate
to our 5.2/5.10/(missing). The third role (Research Associate = supports
experiments) is **not in our ROLES-INVENTORY**. Should be added when we
have research execution volume.

**Concrete adoption**:
- NOW: add `5.13 Research Associate` (🟡 T2, deferred) to ROLES-INVENTORY.md.
  **Effort: 5 min.**
- WHEN FTE HIRED: activate.

### R11 — OWASP LLM Top 10 2025 (relevant subset) — **PARTIALLY RELEVANT**

**Why**: Our org is LLM-agent-based. Some risks are real, some are
theater. Filter:

| LLM risk | Real for us? | Why |
|---|---|---|
| LLM01 Prompt injection | ✅ REAL | Already mitigated via hard-stop-wrapper |
| LLM02 Sensitive disclosure | ✅ REAL | Mitigated via peitho + security-watchdog |
| LLM05 Improper output | ✅ REAL | eval-gate-runner covers this |
| LLM06 Excessive agency | ✅ REAL | hard-stop-wrapper blocks destructive actions |
| LLM09 Misinformation | ✅ REAL | citation-checker is the #1 Research dept gap |
| LLM03 Supply chain | 🟡 DEFER | Only relevant when we depend on 3rd-party models |
| LLM04 Data poisoning | 🟡 DEFER | We don't train models; only relevant if we do |
| LLM07 System prompt leak | ⚪ N/A | Our system prompts aren't secrets |
| LLM08 Vector/embedding | ⚪ N/A | We don't use RAG today |
| LLM10 Unbounded consumption | 🟡 DEFER | PROMPT max_tokens covers this already |

**Concrete adoption**: nothing new. Our existing mitigations cover the
real risks. The defer-list is the right call.

### R12 — Cloudairy / Organimi / theorgchart.com IT org guides — **PARTIALLY RELEVANT**

**Why**: Cloudairy's "Review quarterly" recommendation is good practice.
Organimi's 4 structural types (Functional/Matrix/Flat/Product) is useful
vocabulary. theorgchart.com's Run/Build/Enable split is R4 above.

**Concrete adoption**:
- NOW: add quarterly org-chart review cron `aiw-org-chart-review` (1 day).
- WHEN WE GROW: adopt Functional split (FE/BE separate).

### R13 — GitHub Enterprise "Best practices for orgs and teams" — **MINIMAL**

**Why**: We use GitHub but our org structure (private repos, simple team)
doesn't need enterprise patterns. Skip.

### R14 — awesome-knowledge-management tools — **DEFER**

**Why**: We don't need a unified KM tool yet. Per ROLES-INVENTORY, KM
roles (9.1-9.4) are Tier-2/3 deferred. When we hire FTE, revisit.

**Concrete adoption**: none. Add to deferred list.

### R15 — BLS Computer Research Scientist (22% growth, 8,400 new jobs) — **MARKET DATA ONLY**

**Why**: Useful for understanding future FTE hiring market. No action.

**Concrete adoption**: file in pay-band doc (per R9).

---

## 3 — What's NOISE (explicitly rejected with reasons)

Per Ivan's directive ("don't care about laws / practices shooting
themselves in the foot"), and my own filtering.

### N1 — EU AI Act — **REJECTED as planning input**

**Why reject**: 
- Enforced August 2026 but enforcement actions targeting AIW-class orgs
  are unlikely in 2026-2028 (the AI Office prioritizes high-risk systems:
  credit scoring, hiring, medical, biometric)
- AIW doesn't ship high-risk AI to EU consumers; we ship to B2B clients
  (Paraguay primary; some Netherlands)
- Compliance overhead (DPO, conformity assessment, post-market monitoring)
  doesn't fit our 2-person org or our LLM-agent architecture
- Most EU AI Act guidance is written for BigCo; we're not a BigCo

**However, monitor for**:
- If we ever ship a product where EU residents are *consumers* (not
  clients), EU AI Act becomes relevant
- If a client specifically requires EU AI Act compliance, project-specific

**Concrete adoption**: ZERO. Do not plan around this. If a client asks,
project-price it separately.

### N2 — NIST AI Risk Management Framework — **REJECTED**

**Why reject**: Voluntary framework; same BigCo-bias as EU AI Act;
overlaps with our existing hard-stop pattern. Adds paperwork, no value.

**Concrete adoption**: NONE.

### N3 — OWASP GenAI Top 10 risks we don't face — **REJECTED subset**

Per R11, the LLM03 / LLM04 / LLM07 / LLM08 / LLM10 items are
not relevant to our architecture today. We're not going to add a
"supply chain mitigation strategy" for an LLM model we don't train.

### N4 — "AI Governance Committee" — **REJECTED**

Per `research/org-design-literature.md` §6.2 (already documented
rejection): "Adding a committee adds a layer of human review for
decisions the agents already can't make."

**Concrete adoption**: NONE. Our hard-stop wrappers ARE the governance.

### N5 — Hire-first patterns from Cloudairy / Organimi / SaaS Org Chart — **REJECTED for now**

**Why reject**: Cloudairy describes 100-1000+ employee IT orgs. We're 2
people. The SaaS Org Chart 50/125/400/1000 blueprints don't apply.

**Concrete adoption**: NONE. Revisit at 5+ employees.

### N6 — "Compliance Officer" / "Privacy Counsel / DPO" — **REJECTED**

**Why reject**: Tier-3 / T4 deferred in our ROLES-INVENTORY for good
reason — at 2 people, Ivan wears the hat. Naming a separate role
adds overhead without value.

**Concrete adoption**: NONE until first FTE hire.

### N7 — Allen Institute / Google Research geographic specialization — **REJECTED**

**Why reject**: We don't have geographic distribution. We're 2 people
in Paraguay. Specializing by location is anti-pattern at our scale.

**Concrete adoption**: NONE.

### N8 — Industrial Liaison Officer (ERC) — **REJECTED for now**

**Why reject**: Activates only when we have joint research projects
with industry partners. Today Ivan's thesis is solo academic work.

**Concrete adoption**: NONE until first joint research project.

### N9 — Papers-we-love / academic papers on eng orgs — **DEFERRED**

**Why defer**: Not yet read. Reading list item for slow time.

**Concrete adoption**: file in `engineering/reading-list.md` for later
consumption. **Effort: 5 min.**

### N10 — MIT 3 research role tracks (Research Associate specifically) — **DEFERRED ADD**

**Why defer**: R10 above adds it as Tier-2 deferred. Adding as a real
role would imply we need to hire. We don't, yet.

### N11 — "Comprehensive" course / curriculum design (instructional
designer, ADDIE, Bloom) — **REJECTED until course scales**

**Why reject**: We have 1 module/week. Instructional Designer is
Tier-3 deferred per ROLES-INVENTORY. Adding pedagogy framework
now is over-engineering.

**Concrete adoption**: NONE until course crosses 2 modules/week.

### N12 — "Editorial calendar" / structured publishing — **REJECTED until we publish**

**Why reject**: We don't publish externally. Editorial calendar assumes
publishing cadence we don't have.

**Concrete adoption**: NONE until first external publication.

### N13 — AI safety posture doc refresh — **PARTIAL**

**Why partial**: Our `engineering/ai-safety-posture-2026.md` exists but
the 5 gaps identified there (per Phase 6 audit) need work, not a
"refresh the posture doc." **Action over documentation.**

**Concrete adoption**: address the 5 gaps as engineering work, not
paperwork (see §4 Phase 1).

---

## 4 — The implementation plan

Phased. Gated to current state ($240 MRR, 2 people, L1-L3 wired).

### Phase 1 — Engineering dept hardening (NEXT, 1-2 weeks)

**Goal**: close the 5 AI safety gaps + get DORA metrics visible.

| # | Action | File / location | Effort | Owner |
|---|---|---|---|---|
| 1.1 | Build `scripts/dora-metrics-aggregator.py` (4 metrics) | `/opt/data/agents/scripts/dora-metrics-aggregator.py` | 4h | engineering-roster |
| 1.2 | Wire `aiw-dora-metrics-weekly` cron | `jobs.json` | 30m | engineering-roster |
| 1.3 | Build `scripts/slo-error-budget-tracker.py` | `/opt/data/agents/scripts/slo-error-budget-tracker.py` | 1d | devops-monitor + ai-safety-engineer |
| 1.4 | Wire `aiw-slo-tracker-daily` cron | `jobs.json` | 30m | devops-monitor |
| 1.5 | Apply SLOs to top 5 client sites | state files | 4h | devops-monitor |
| 1.6 | Add `cluster:` field to PROMPT frontmatter (13 agents) | `prompts/*/PROMPT.md` | 1h | ai-ops-coordinator |
| 1.7 | Wire hard-stop-wrapper globally (per Phase 6 audit: 0/49 agents) | `scripts/hard-stop-wrapper.py` | 2d | ai-safety-engineer |
| 1.8 | Compute aggregate pass_rate (Phase 8 script already done) | `state/eval-trending.json` | 2h | eval-gate-runner |

**Total Phase 1 effort**: ~5 days work
**Trigger**: NOW (no gate dependency)

### Phase 2 — Research dept hardening (2-4 weeks)

**Goal**: fix the #1 gap (citation coverage 15%).

| # | Action | File / location | Effort | Owner |
|---|---|---|---|---|
| 2.1 | Build `citation-coverage-enforcer` agent | `demiurge/agents/citation-coverage-enforcer/` (NEW) | 4h | research-tracker |
| 2.2 | Wire as git-hook: blocks merges with 0 unverified citations | `.git/hooks/pre-commit` + config | 2h | research-tracker |
| 2.3 | Add KU section to research-tracker brief outbox template | `research-tracker/outbox/template.md` | 30m | research-tracker |
| 2.4 | Run citation coverage audit weekly, target 50% by end of Q3 2026 | cron `aiw-citation-audit-weekly` | 1d | citation-checker |
| 2.5 | Add `5.13 Research Associate` (🟡 T2 deferred) to ROLES-INVENTORY | `docs/ROLES-INVENTORY.md` | 5m | Ivan |
| 2.6 | Build `editorial-calendar-keeper` CRON_WORKFLOW | `scripts/editorial-calendar.py` + cron | 3h | research-tracker |
| 2.7 | Add quarterly org-chart review cron `aiw-org-chart-review` | `jobs.json` | 1d | ai-ops-coordinator |

**Total Phase 2 effort**: ~3 days work
**Trigger**: NOW

### Phase 3 — Cross-cutting quality (4-6 weeks)

**Goal**: address the 5 gaps in `engineering/ai-safety-posture-2026.md`.

| # | Action | File / location | Effort | Owner |
|---|---|---|---|---|
| 3.1 | drift-detector calibration run (30 days, then tune thresholds) | `state/drift-eval-30d.json` | 30 days | drift-detector |
| 3.2 | chaos-test-runner — run 5 scenarios, document learnings | `engineering/chaos-test-runbook.md` | 3d | chaos-test-runner |
| 3.3 | security-auditor — first OSS dependency audit | `engineering/oss-dependency-audit.md` | 1d | security-auditor + security-watchdog |
| 3.4 | eval-gate-runner — first aggregate trend report | `state/eval-trending.json` | 4h | eval-gate-runner |
| 3.5 | ai-safety-engineer — global hard-stop enforcement audit | `engineering/ai-safety-posture-2026-q4.md` | 2d | ai-safety-engineer |

**Total Phase 3 effort**: ~7 days work + 30 days drift calibration
**Trigger**: AFTER Phase 1 completes

### Phase 4 — L4 unlock prep (8-12 weeks, gated)

**Goal**: hit the L4 unlock triggers ($1000+ MRR + 30d L1-L3 stability).

**Tracked by**: state/finance.json (MRR) + cron-error-watchdog.json (stability)

| # | Action | File / location | Effort | Owner |
|---|---|---|---|---|
| 4.1 | Sales funnel revival (per `sales/funnel-revival-2026.md`) | `sales-pipeline` cron fix | 2h | sales-pipeline |
| 4.2 | Hit $1000 MRR — sales motion + service expansion | n/a | TBD | Ivan + sales-pipeline |
| 4.3 | 30 days L1-L3 stability check | cron-error-watchdog.json | 30d | ai-ops-coordinator |
| 4.4 | Self-running declaration (L4 unlock) | docs/phases/PHASE-N-SELF-RUNNING.md | 1d | ai-ops-coordinator + Ivan |

**Total Phase 4 effort**: TBD (depends on revenue)
**Trigger**: MRR + stability gates

### Phase 5 — Deferred (gated, AFTER L4 unlock)

| # | Action | Trigger |
|---|---|---|
| 5.1 | First FTE hire | $1000+ MRR + 30d stability |
| 5.2 | First external paper submitted | Ivan decides |
| 5.3 | Zotero + ORCID setup | First paper |
| 5.4 | Pay-band doc | First FTE hire |
| 5.5 | Allen-style geographic specialization | 5+ employees |
| 5.6 | Industrial Liaison Officer role | First joint research project |
| 5.7 | OJS instance | First journal submission |
| 5.8 | KM tool adoption (AFFiNE/Outline) | 50+ source-materials |

---

## 5 — What this plan does NOT do (scope guard)

Explicitly **out of scope** for this plan:

- ❌ EU AI Act compliance (N1)
- ❌ NIST AI RMF (N2)
- ❌ AI Governance Committee (N4)
- ❌ Hire-first org-chart patterns (N5)
- ❌ Compliance Officer / DPO hiring (N6)
- ❌ Geographic specialization (N7)
- ❌ Industrial Liaison Officer role (N8)
- ❌ ADDIE / Bloom instructional design (N11)
- ❌ Editorial calendar for non-existent publications (N12)
- ❌ Allen Institute / Google Research geographic patterns (N7)
- ❌ Refreshing posture docs as the goal (N13)
- ❌ Postmortem-analyzer / DORA dashboard as separate projects (covered by Phase 1)
- ❌ Anything in compiled findings R2/R5 deferred items (Zotero, pay-band) — see Phase 5

---

## 6 — Decision summary (Ivan approves or rejects)

| # | Decision | Status |
|---|---|---|
| D1 | Adopt Run/Build/Enable cluster field in PROMPT frontmatter | RECOMMENDED (1h) |
| D2 | Build DORA metrics aggregator | RECOMMENDED (4h) |
| D3 | Build SLO/error-budget tracker | RECOMMENDED (1d) |
| D4 | Global hard-stop enforcement | RECOMMENDED (2d) — closes Phase 6 gap |
| D5 | Build citation-coverage-enforcer | RECOMMENDED (4h) — fixes #1 Research gap |
| D6 | KU-action-oriented brief template | RECOMMENDED (30m) |
| D7 | Quarterly org-chart review cron | RECOMMENDED (1d) |
| D8 | Add Research Associate role to ROLES-INVENTORY | RECOMMENDED (5m) |
| D9 | Defer all EU AI Act / NIST / Compliance Officer work | RECOMMENDED |
| D10 | Defer Zotero/ORCID until first paper | RECOMMENDED |
| D11 | Defer pay-band doc until first FTE | RECOMMENDED |

**Total Phase 1+2 work**: ~8 days spread over 4 weeks (1-2 items/day, parallel where possible).

---

## 7 — Concrete next-step (the one thing to do first)

**Build `scripts/slo-error-budget-tracker.py` (1d, 2 files)**.

**Why first**: Closes the largest Engineering gap (per `04-engineering/v1 research
area #1` — 12-factor audit, Factor 11 incomplete without SLOs). The script is
also the foundation for DORA's "reliability" metric (MTTR).

**Files to write**:
1. `/opt/data/agents/scripts/slo-error-budget-tracker.py` — Python script
2. `/opt/data/agents/state/slo-budget.json` — state schema

**Ad-hoc verification** (per Ivan's pattern):
- `/opt/data/profiles/ivan/scratch/hermes-verify-slo-tracker.py`
- 20-30 assertions
- Delete after verification

---

**Document path**: `/opt/data/agents/research/dept-research/04-05-implementation-plan.md`
**Last updated**: 2026-09-01
**Author**: Phase 7 R4 (implementation plan), Ivan approval pending
**Length**: ~400 lines of decision + plan, not "research"
**Doctrine applied**: AIW-state-fit, no compliance theater, no premature FTE patterns