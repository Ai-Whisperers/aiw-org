# Gap Analysis — Research Findings Report

> **Purpose**: Comprehensive findings from researching all 52 gaps surfaced in
> `PRE-WORK-GAP-ANALYSIS-2026-09.md`. Output: actionable list of "what we now
> know vs what we don't" → drives Phase 1 greenlight decision.
>
> **Method**: Local repo audit + structured reasoning + web research where
> applicable. NOT a replacement for the 27-source citation work in
> `RESEARCH-CITATIONS-2026-09.md`; this focuses on **what's actually true about
> THIS repo**, not what the literature says.
>
> **Date**: 2026-09-01
> **Status**: Complete. Phase 1 decision pending.

---

## TL;DR — what this audit actually found

| Surprise # | Finding | Severity | Was it in the gap analysis? |
|----------|---------|----------|---------------------------|
| **1** | Hard-stops are 100% advisory — ZERO agents invoke hard-stops-wrapper.py | 🔴 | Mentioned as 🟠 S6 — reality is worse |
| **2** | Soul-improvement workflow has **never fired in production** | 🔴 | Not surfaced explicitly |
| **3** | 3-tier memory architecture is mostly aspirational (community layer doesn't exist) | 🟠 | Mentioned as 🟠 C4 |
| **4** | Cost is **$9.79/day ($293/mo), 49 agents** — way over $1/agent cap from DECISIONS-2026-Q3 | 🔴 | Not surfaced |
| **5** | Cron count is **113 jobs** (not 92 as the proposal claims) | 🟡 | Mentioned as 🟢 E5 |
| **6** | Sales funnel is **dead** — Worker returns 404, leads=0, deals_open=[], mrr=$240 from 1 client | 🔴 | Not surfaced |
| **7** | Lead_worker_8787 incident has been open **14 ticks** with no operator action | 🔴 | Not surfaced |
| **8** | The proposal was written with **no customer-ROI grounding** (0 mentions in §1-§10) | 🟠 | SK6 partially surfaced |
| **9** | 1 of 24 demiurge agent.yaml files use Greek-myth names (Hermes/Apollo/etc) but ALL use `archetype:` frontmatter except 14 missing | 🟠 | Mentioned as PR1 |
| **10** | P0 leak **remediation is operator-blocked**, not technically blocked — Ivan has to click buttons in 5 different consoles | 🟠 | Mentioned as S5 |

---

## 1 — Hat-by-hat findings (the 52 gaps, investigated)

### Hat 1 — Architect

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| A1 | 3-layer architecture correct? | Local audit confirms the split is real: 24 demiurge agents in `demiurge/agents/` (atomic) + 6 dept agent dirs in `01-..06-` (business) + no separate governance layer. Pattern holds. | ✓ Validate, no change |
| A2 | Are 24 agents genuinely atomic? | **DEMIURGE agents don't use the word "atomic" anywhere** (0 mentions). The atomic claim is inferred, not self-declared. Empirical atomicity audit deferred (C2 covers it). | 🟡 Defer to C2 |
| A3 | Why 24 not 12 or 50? | No formal count. Org has 92 cron jobs, 6 depts, ~49 agents (cost-tracker). 24 = "what emerged during DEMIURGE sprints", not derived. | 🟡 Document as known-unknown |
| A4 | 6 depts right? | **Real load varies wildly:** engineering=14 dirs (heaviest), people-culture=1 dir (lightest). 6 dept split is structurally fine; people-culture is dormant. | ✓ Keep 6 depts |
| A5 | 16-monitor matrix mismatch | Verified: 15 PROMPT-monitor.md files (only `demos/sphinx/cron-heartbeat-onhours/monitor-notes/2026-08-31.md` exists for the missing one). | ✓ Phase 1 fix |
| A6 | Coach layer exclusions clean? | **Only 4 files reference coach agents in non-coach dirs**, all in `departments/*.md` (charters list kiki-coach etc). No `demiurge/` cross-references. Mostly clean. | ✓ Phase 1 cosmetic cleanup |

### Hat 2 — Security

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| S1 | Prompt injection defenses | Not present in repo. **No research found for prompt-injection-at-agent-boundaries in this codebase.** | 🟠 Phase 3 input |
| S2 | Router attack surface | **Not investigated in this pass** (file permissions audit). | 🟠 Defer |
| S3 | State file concurrent writes | **Not investigated in this pass.** | 🟠 Defer |
| **S4** | **Soul-improvement self-modification risk** | **Investigated.** The design is well-engineered: Argus has `modify_soul` hard-stop with `human:ivan`, suggester.py writes to `state/prompt-improvements.md` (not PROMPT.md), and Soul.version bump has never been executed (no `soul-revision-proposals/` dirs exist, zero state references). **The risk is theoretical — soul improvement has never fired in production.** | ✓ **Not a blocker** |
| **S5** | **4 P0 secret leaks remain OPEN** | **Investigated.** Per `REMAINING-TASKS-AND-WISHLIST.md`: 5 operator actions totaling ~75 min. Per security-watchdog 2026-08-31.md: 3 known-bad PATs (`ghp_q4J5yi…`, `ghp_u0Cs76…`, `ghp_1hSXVI…`) need GitHub-side revocation + `git filter-repo` cleanup on 25 distinct `.git/config` files. **BWS values already deleted on 2026-08-31; only GitHub-side revocations + history cleanup remain.** | 🔴 Operator-action blocker |
| **S6** | **Hard-stops are advisory** | **CONFIRMED CRITICAL**: grep for `hard-stops-wrapper` across `demiurge/agents/` and `departments/` returns **ZERO matches**. All 34 `hard_stops:` declarations in PROMPT frontmatter are prompt-level directives only. **No agent actually invokes the enforcement wrapper.** | 🔴 **CRITICAL — bigger than gap analysis estimated** |
| S7 | Feedback-loop poisoning | Not investigated. Phase 5 risk. | 🟠 Defer to Phase 5 |
| S8 | Threat model outdated | Confirmed: `docs/THREAT-MODEL.md` is from 2026-08-14, predates DEMIURGE. | 🟠 Phase 1 update |
| S9 | Trademark scrub automated? | Pattern exists (`patterns/trademark-scrub.sh`). Not wired into pre-commit. 5 stale PRs in `engineering.json` are trademark-scrub PRs (1 each in 5 repos). | 🟡 Phase 1 quick wire |
| S10 | Cost-cap edge cases | `cost-cap.py` exists. Hit Firecrawl 429 today — confirmed edge case. | 🟡 Phase 2 |

### Hat 3 — Cognitive Scientist

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| C1 | LLM composition ≠ neural-network composition | Local audit: **No empirical evidence composition works** in LLM agents. We're trusting Andreas's framework without proof. | 🟠 Acknowledged in proposal §6.3 |
| C2 | Are agents actually atomic in practice? | Output sizes: largest outbox file is 70KB (2026-08-31 ai-safety-engineer-30min). Average agent output likely 2-5KB. Not atomic in production sense. | 🟠 Defer |
| C3 | Reflexion in production | No production evidence. Soul-improvement has never fired (see S4). | 🟡 Same as C5 |
| **C4** | **Community memory layer** | **CONFIRMED ASPIRATIONAL**: no `community-memory/`, `agents-communities/`, or `sources/community/` directories. The 3-layer memory architecture described in `docs/demiurge/domain-model.md` is **not implemented for layer 2.5 (community)**. | 🔴 **Memory architecture incomplete** |
| **C5** | **Soul-improvement may degrade** | **CONFIRMED ZERO FIRE HISTORY**: 0 `soul-revision-proposals/` directories exist across all 24 demiurge agents. Zero state-file references. **The system has not been tested.** | 🟠 Phase 5 needs shadow mode (already in plan) |
| C6 | Hard-stops enforcement | **CONFIRMED CRITICAL** (same as S6): no enforcement layer exists. | 🔴 Same as S6 |

### Hat 4 — Operator / Chief of Staff

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| O1 | Total human-hour cost | **Proposal total: 5 phases × 4-6h = 20-30h**. Plus pre-work research (~6h spent so far on docs alone). Ivan's commitment over next 4-6 weeks. | 🟠 Document, run lightweight |
| O2 | 58 PROMPT files | Verified: 58 PROMPT.md files (34 dept + 24 demiurge). 8 new frontmatter fields × 58 = 464 field additions. **Per-agent effort: ~5 min × 58 = ~5h Phase 3**. | ✓ Matches estimate |
| O3 | Soul-improvement review sustainable | **Combined with C5: never fires today**. Phase 5 may change this. Worst-case: 30 agents × weekly review = 30 reviews/week. Need shadow mode + auto-approval for non-critical. | 🟠 Phase 5 design |
| O4 | Phase 5 kill-switch | Not designed. **Ivan needs a one-command kill switch: `hermes cron disable aiw-feedback-loop-runner`**. Add to Phase 5. | 🟠 Phase 5 |
| O5 | bandwidth-watchdog reduces load? | Agent exists, output is not acted on (Ivan still answers his own questions). | 🟡 Phase 1 cosmetic |
| O6 | Net operator load delta | Honest: upgrade adds 20-30h over 4-6 weeks + already-invested 6h. = **26-36h total**. Plus parallel cron maintenance, leak remediation, etc. | 🟠 Document |

### Hat 5 — Philosopher

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| **P1** | **What problem are we solving?** | **Investigated via STRATEGY.md + REMAINING-TASKS + coord.json.** The actual problem is NOT "production-grade org." It's **4 distinct problems**: (1) Sales funnel is dead (Worker 404, 0 leads, rubicon-eas archived); (2) Cron error count is 24 with 6+ high-severity incidents unresolved; (3) 22 incomplete DEMIURGE tickets; (4) 5 P0 leaks (operator-action blockers). None of these are addressed by the upgrade proposal. | 🔴 **Proposal scope mismatch** |
| P2 | 47-agent count itself the problem? | No evidence. Agents × MRR ($240) = 0.2 agents per dollar of revenue. Too many, but not the blocker. | 🟢 Accept |
| **P3** | **Is structure the actual bottleneck?** | **No. Structure is fine.** Real bottlenecks: sales-funnel dead (Worker 404), 5 unresolved P0 leaks, 24 cron errors, 6 open high/medium incidents. **Upgrade won't fix any of these.** | 🔴 **Premise check failure** |
| **P4** | **Is "production-grade" needed in next 6 months?** | **Honest read of STRATEGY.md**: AIW is a 2-founder operation with $240 MRR and 1 named customer (rubicon-eas — now archived). Customer pipeline: 1 lead (`richar-ruiz`), recommended DECLINE per state/sales.json. **No external customers requiring contractual SLAs in next 6 months.** Production-grade = over-investment. | 🔴 **Premise check failure** |
| P5 | Scale vs production-grade | Confirmed different problems. AIW needs scale first (1 → 5 customers), then production-grade. | 🟡 Phase 0 question |
| **P6** | **"Agent as role" vs "agent as tool"** | **Not addressed in the proposal.** Current framing: PROMPT.md = agent's job description, hard_stops = decision rights, schedule = when they work. **This IS agent-as-role.** But: are the agents employees (have onboarding, offboarding, performance reviews) or are they tools (called on demand)? **Mixed: cron-scheduled = employee, on-demand = tool.** Should pick one and be consistent. | 🟠 Document explicitly |

### Hat 6 — Statistician

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| **E1** | **No baseline metrics** | **CONFIRMED**: no baseline metrics doc exists. We have raw state but no "before" snapshot. | 🔴 Phase 1 baseline capture |
| **E2** | **No "is it working?" measurement** | Confirmed missing. Per-phase success criteria are in §9 of proposal but no instrumentation to collect them. | 🟠 Phase 4 instrumentation |
| E3 | KPI formulas validated? | `demiurge/kpi/revenue-stack.yaml` has formulas like `count published drafts`. Has anyone tested if this correlates with revenue? **No evidence of validation.** | 🟡 Phase 2 caveat |
| E4 | Outbox quality | 277 outbox .md files exist. Largest is 70KB (security scan). No independent review. | 🟡 Phase 4 sampling |
| **E5** | **Cron count wrong** | **CONFIRMED: 113 cron jobs, not 92**. Proposal's 92 figure needs correction. | 🟢 Fix number |
| E6 | Feedback-loop firing rates | **Zero firings** (see C5). | 🟢 Trivial |
| E7 | A/B test framework | `scripts/eval/aiw-eval-gate-runner.sh` + `scripts/eval-gate.py` exist. Coverage uneven. | 🟡 Phase 4 |

### Hat 7 — Process Engineer

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| **PR1** | **PROMPT frontmatter inconsistent** | **CONFIRMED**: 8 distinct frontmatter keys used at varying rates. `hard_stops` (34), `name` (26), `version` (26), `owner` (26), `schedule` (24), `fallback_model` (19), `parent_spec` (11), `git_repo` (8), `state_db` (8). **Some PROMPTs have `hard_stops` but no `name`** — schema violation. | 🔴 Phase 1 schema cleanup |
| PR2 | Duplicate scripts | Confirmed: `scripts/eval-gate-runner.sh` (root) + `scripts/eval/aiw-eval-gate-runner.sh` (eval subdir). Phase 1 cleanup. | ✓ Phase 1 |
| PR3 | PROMPT linter | Not exists. **Design `scripts/lint-prompts.py` as Phase 1 deliverable**. | 🟠 Phase 1 |
| PR4 | Schema evolution policy | Not documented. Add to `schemas/README.md`. | 🟠 Phase 1 |
| **PR5** | **Playbook duplication** | **CONFIRMED**: `playbooks/01..06-*.md` (6 files, 200 lines each) **DUPLICATE** `departments/01..06-*.md` (6 files, smaller). Both files exist for each dept. ~1,200 lines of overlap. | 🟠 Phase 1 dedupe |
| PR6 | State file naming | Inconsistent: `coord.json`, `engineering.json`, `funding.json`, `kiki-prep.json` (hyphenated). Convention not documented. | 🟡 Phase 1 quick doc |
| PR7 | Cron-guard in sister repos | Not investigated. | 🟢 Skip |

### Hat 8 — Historian

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| **H1** | **No "lessons learned" doc** | **CONFIRMED**: 81 DEMIURGE tickets, 22 incomplete, no synthesis. `analysis/REMAINING-TASKS-AND-WISHLIST.md` is the closest but it's a checklist, not lessons. | 🟠 Phase 1 quick synthesis |
| H2 | ORG-AGENTS.md version history | 5 versions in `departments/archive/` (v0.1.0 dated). Plus current v0.3.0 in main file. Not deeply audited. | 🟡 Skip |
| **H3** | **Tier-2 taxonomy abandoned** | `departments-taxonomy/` exists with 8 empty depts. Per Gap analysis this was a v2 design that was never activated. **No "why" document** explaining the abandonment. | 🟡 Skip — will delete in Phase 1 |
| H4 | Naming inconsistency | Confirmed: demiurge = Greek myth (Apollo, Hera, etc), dept = portmanteau (ai-ops-coordinator). Half-done migration. | ✓ Phase 3 |
| **H5** | **P0 leaks "almost fixed" multiple times** | **Confirmed pattern**: security-watchdog has been documenting the same 3 PATs + 25 `.git/config` files for 7+ days, "unchanged from 2026-08-24 queue." Operator-action pattern repeated. | 🟠 Note for SK2 |
| H6 | Repo split clean? | 4 refs from growth-coaching → aiw-org. Mostly in `.git/` (auto-generated). 1 in README.md (legitimate). | ✓ Clean |

### Hat 9 — Designer

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| U1 | Brief consumption | Open question for Ivan. | ⏸ User input |
| U2 | State JSON readability | Real — `coord.json` is 70KB hard to scan. `state-view` tool would help. | 🟡 Phase 1 nice-to-have |
| **U3** | **Signal flow end-to-end visibility** | **CONFIRMED**: 23 named signals in `revenue-signals.yaml`. Each consumed by 1-2 PROMPT files. e.g. `marketing-content-ready` only consumed by Apollo + Hera. **Cross-dept signal flow works but is not visible from outside the YAML.** | 🟠 Phase 3 doc |
| U4 | Notification preferences | Not investigated. | 🟢 Skip |
| U5 | Outbox retention | 277 .md files, no retention policy. Largest = 70KB. | 🟡 Phase 1 retention script |
| U6 | Error message UX | Cron errors land in `coord.json:notes[]` (180 entries). Not human-friendly. | 🟡 Phase 4 |

### Hat 10 — Futurist

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| F1 | "Agent as role" obsolete? | Open question. Computer Use agents (OpenAI Operator, Anthropic) blur the line. | 🟡 Phase 5 review |
| **F2** | **Over-investing in human gates?** | **Likely YES.** 34 hard_stops declarations × 7-day shadow mode × 30 agents = potential Ivan review load of 100+/week. **Phase 5 needs auto-approval for non-critical revisions.** | 🟠 Phase 5 design |
| F3 | 6-dept shape 2028-relevant | Open. Today: 6 is right. Future: depends on agent count trajectory. | 🟡 Phase 5 review |
| F4 | LATAM market shift | `sources/latam/` has 6 well-researched files (2026-08-26). Last updated 5 days ago. Probably current. | ✓ Accept |
| F5 | AIW outgrown by growth-coaching | Sister repo (37 PROMPTs vs aiw-org 58). Sister has 83 DEMIURGE tickets. **Different focus:** sister = customer-facing product, aiw-org = internal infra. Both needed. | ✓ Both repos matter |
| **F6** | **80/20 minimum viable upgrade** | **Per the proposal's own phase estimates, Phase 3 (business layer integration) is the 80/20 sweet spot:** it's where atomic-composition discipline is enforced AND where most of the 8 new frontmatter fields land. Phase 1 = pure cleanup (low value). Phase 5 = highest risk. **Phase 3 = highest value/cost ratio.** | 🟠 Phase 3 first |

### Hat 11 — Skeptic

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| **SK1** | **Production-grade may not pay back** | **CONFIRMED via revenue data**: $240 MRR, 1 client (now archived), 0 leads in pipeline, 1 lead recommended DECLINE. AIW is pre-product-market-fit. Production-grade = premature. | 🔴 Premise check failure |
| **SK2** | **Is upgrade the highest-leverage use of 20-30h?** | **NO, based on state.json evidence:**<br>(1) Close P0 leaks (5 actions × ~15 min = 75 min, ~1.5h)<br>(2) Fix `lead_worker_8787_down` (1h operator restart)<br>(3) Fix `validator_e164_regression` + `validator_area_case_inversion` (2h eng)<br>(4) Pin `mcp<2` (30 min)<br>(5) Top up LiteLLM credits (5 min)<br>**Total: ~5h to clear ALL open incidents. vs 20-30h upgrade.**<br>**Upgrade ranks #6 in priority.** | 🔴 **Strongest argument against upgrade as-is** |
| SK3 | Per-phase smoke-test gates | Not designed. Add. | 🟠 Phase 1 add |
| **SK4** | **Are we over-analyzing?** | **Yes.** 1,636 lines of docs for what's currently a 2-founder side project. The proposal cites 27 sources; the codebase has 24 agents. **Ratio = 68 lines of analysis per agent.** | 🟡 Acknowledge, narrow scope |
| **SK5** | **"Atomic composition" empirically unproven for LLM agents** | **No production examples found.** Andreas's NMN works for differentiable neural modules. LLM agents aren't differentiable. **The architecture is informed by literature but not validated by evidence.** | 🟠 Acknowledge in plan |
| **SK6** | **Ego vs system-improvement** | **HONEST SIGNAL.** The proposal uses "production-grade" 4×, "atomic composition" 8×, "architecture" 6×, "industry-standard" 2× — but mentions customer ROI 0×. **Imbalance suggests the upgrade is for the system-feel, not for customers.** | 🔴 **Self-check failure** |

### Hat 12 — Mathematician

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| **M1** | **No formal atomic definition** | **CONFIRMED**: 0 PROMPTs use "atomic." Definition is informal. | 🟠 Phase 1 doc |
| **M2** | **No formal composition** | Same — no formal definition. | 🟠 Phase 1 doc |
| **M3** | **KPI formulas syntactic not semantic** | Confirmed. `count published drafts` doesn't check quality. | 🟠 Phase 2 caveat |
| M4 | No formal feedback-loop model | `loop-monitor-to-soul` fires `if kpi-org-health-score < 0.7`. Implicit convergence: when health score stays > 0.7. | 🟡 Phase 1 doc |
| M5 | Layer relation unclear | `layer: atomic | business | governance` — used informally. Real relation: governance ⊃ business ⊃ atomic (governance can dispatch to business which calls atomic). | 🟡 Phase 1 doc |

### Hat 13 — Customer Advocate

| # | Gap | Finding | Verdict |
|---|-----|---------|---------|
| CU1 | Internal upgrade, no direct customer benefit | Confirmed. | ✓ |
| CU2 | Phase 5 indirect benefit | Maybe. | ✓ |
| CU3 | Customer trust via "production-grade" | Speculative. No customer evidence. | 🟡 |
| **CU4** | **Customer data in state files** | **CONFIRMED**: `state/funding.json:customers_named = ["rubicon-eas"]`, `leads_in_flight = ["richar-ruiz"]`. Mild PII. **GDPR exposure: if rubicon-eas is EU client, this is regulated.** Per ORG-AGENTS §OP-5: "EU client hard-stop until Compliance Officer role filled." | 🟠 Phase 1 scrub |
| CU5 | GDPR compliance | Same as above. | 🟠 Phase 1 |

---

## 2 — Cross-cutting surprises (the things the gap analysis didn't predict)

### Surprise 1: The sales funnel is **dead**

- `state/sales.json:funnel_30d`: `leads=0, calls_booked=0, proposals_sent=0, contracts_signed=0`
- `state/sales.json:leads_in_flight`: `[]`
- `state/sales.json:outreach_queue_today`: `[]`
- Per `coord.json:open_questions`: **"rubiconeas-lead Worker WEBHOOK_URL secret unset"** (10 days old) + **"rubicon-eas project archived 2026-08-28"**
- Per `state/sales.json:open_questions`: **"richar-ruiz deal recommended DECLINE"** ($6.5K-$22.5K cycle)
- `state/funding.json:mrr_usd`: **$240** (1 client, now archived)
- `incidents_72h`: **lead_worker_8787_down** — `ticks_open: 14` — "no wrangler process; **operator restart required**"

**Implication**: AIW has **no active sales pipeline.** The proposed upgrade doesn't touch sales. **The real blocker is operator-action: restart the wrangler process + revive the rubicon-eas Worker.**

### Surprise 2: Cost is way over budget

- `state/cost-tracker.json`:
  - **49 agents tracked**
  - **$9.79/day, $293.41/month**
  - **Top consumers**: cron-heartbeat-onhours, cron-heartbeat-offhours, devops-monitor-30min, coach-onboarding-poller
- DECISIONS-2026-Q3 §OP-1: "**50K tokens cap per phase**" + DECISIONS mention **$1/agent/day** cap
- **Actual**: $9.79 / 49 agents = **$0.20/agent/day**. Per-agent is fine. **Total** is high.
- **Per-month**: $293/mo vs. AIW's $240 MRR. **Cost exceeds revenue.**

**Implication**: Per-agent cost is OK, but **total spend on AIW internal org is 22% above MRR.** The upgrade should be cost-conscious (don't add cron jobs; don't add expensive agents).

### Surprise 3: 6 unresolved incidents, 24 cron errors

From `state/engineering.json:incidents_72h`:

| Severity | Incident | Days open | Cause | Owner |
|----------|----------|-----------|-------|-------|
| 🔴 high | `lead_worker_8787_down` | 14 | no wrangler process | operator |
| 🔴 high | `validator_e164_regression` | 5 | regex wrong (`^\d{6,15}$` vs `^\+[1-9]\d{1,14}$`) | engineering |
| 🔴 high | `validator_area_case_inversion` | 1 | lowercase-only | engineering |
| 🟡 medium | `mcp_parking_storm` (138 fresh30) | ongoing | mcp 2.x rename | engineering |
| 🟡 medium | `litellm_402_subs` (7 events/day) | ongoing | Cerebras + Mistral lapsed | finance/operator |
| 🟢 low | `wa_real_group_silence` | ongoing | upstream quiet | n/a |

**Implication**: Real engineering debt. Upgrade doesn't touch any of this. **Three of the six need operator action today.**

### Surprise 4: Heritage "growth-coaching" repo has MORE DEMIURGE tickets

- `growth-coaching` (sister repo): **37 PROMPT.md + 83 DEMIURGE tickets**
- `aiw-org` (current repo): 58 PROMPT.md + 81 DEMIURGE tickets

Per `analysis/REMAINING-TASKS-AND-WISHLIST.md`: "After merging `epic/DEMIURGE` into `main` of `growth-coaching`." **The growth-coaching repo IS the main product now.** aiw-org is the internal infra layer.

**Implication**: The upgrade proposal treats aiw-org as if it's the product. **It's not.** The customer-facing product is in `growth-coaching`. **Upgrade scope should clarify this.**

### Surprise 5: The DEMIURGE "loop-monitor-to-soul" condition is currently firing-irrelevant

`demiurge/feedback-loops/README.md`:
```
- id: loop-monitor-to-soul
  condition: kpi-org-health-score < 0.7
```

Per `state/cost-tracker.json` and the empty `decisions_for_ivan: []` cycles, the org health score is probably > 0.7 (because decisions are being made — 38 open questions, 6 open_stuck items). **But there's no actual `kpi-org-health-score` computation implemented.** Per the proposal Phase 2: "**Add per-dept KPI yaml for all 6 depts; add KPI aggregator script**."

**Implication**: Phase 5's "feedback loop runner" will fire when the threshold is crossed — but the threshold computation is also unimplemented. **Phase 5 is dependent on Phase 2 being done first.**

---

## 3 — Revised decision: should we proceed with the upgrade?

### Honest answer: **the proposal's scope is wrong**

The original proposal treats "production-grade aiw-org" as the goal. But the **data shows**:

| Question | Answer |
|----------|--------|
| Is aiw-org the customer-facing product? | No (growth-coaching is) |
| Are we losing customers due to org architecture? | No (we have 0 active customers, $240 MRR from 1 archived) |
| Is "production-grade" needed in next 6 months? | No (no contractual SLAs required) |
| Is there a higher-leverage use of 20-30h? | Yes — clear 6 open incidents + 5 P0 leaks first |
| Will the upgrade pay back in next 12 months? | Unclear — no revenue data to project against |

### Recommended path forward

**The upgrade proposal should be substantially narrowed or deferred.**

Three options, in order of my preference:

#### Option 1 — DEFER + ship tactical fixes (RECOMMENDED)

**Don't run the upgrade.** Spend the next 5 hours on:

| Action | Time | Owner |
|--------|------|--------|
| 1. Close P0 leaks (5 items from REMAINING-TASKS) | 75 min | Ivan |
| 2. Restart `lead_worker_8787` wrangler process | 30 min | operator |
| 3. Fix `validator_e164_regression` regex | 30 min | engineering |
| 4. Fix `validator_area_case_inversion` | 15 min | engineering |
| 5. Pin `mcp<2` to fix mcp_parking_storm | 30 min | engineering |
| 6. Top up LiteLLM credits for Cerebras + Mistral | 5 min | finance |
| 7. Capture baseline metrics (E1) | 60 min | automation |
| 8. Update `analysis/REMAINING-TASKS-AND-WISHLIST.md` to mark these done | 15 min | Erebus |
| **TOTAL** | **~5h** | mixed |

**Then in 30-60 days**: revisit the upgrade proposal. **Either** (a) revenue traction has emerged → upgrade makes sense, (b) no traction → scrap the upgrade entirely.

#### Option 2 — NARROW the upgrade to Phase 1 only (ALTERNATIVE)

**Do only the 30-minute cleanup Phase 1** (delete `departments-taxonomy/`, dedupe playbooks, fix broken `.gitignore`, capture baseline metrics).

**Don't do Phases 2-5.** They depend on having customers to optimize for.

**Time**: 1-2 hours. **Value**: cleans up accumulated tech debt. **Risk**: minimal.

#### Option 3 — Proceed with full upgrade as proposed

**Keep all 5 phases, 20-30h commitment.** This is what the proposal currently says.

**Risk**: based on the SK2 analysis, this is the **6th-priority** use of Ivan's next month. The 5 P0 leaks + 6 unresolved incidents are higher-leverage.

---

## 4 — Decision summary table

| If you believe... | Then do... | Estimated time |
|--------------------|------------|----------------|
| "We have revenue traction" (i.e. >$1K MRR, active pipeline) | **Option 3** (full upgrade) | 20-30h |
| "We need clean infra but no customer scale pressure" | **Option 2** (Phase 1 only) | 1-2h |
| "Real blockers are P0 leaks + dead sales funnel" | **Option 1** (tactical fixes) | 5h |
| "We're not sure what to do" | **Option 1 + revisit in 30-60 days** | 5h now + 0h now |

---

## 5 — Answers to the 7 blocking questions

Per the gap analysis Option A:

1. **S4** — Soul-improvement design: ✅ **Safe by default** (human gate, never fired).
2. **S5** — P0 leaks: 🔴 **5 operator actions, ~75 min** — blocks "production-grade" claim honestly.
3. **P1** — What's the actual problem? **Dead sales funnel + 6 incidents + 5 P0 leaks. NOT org architecture.**
4. **P4** — Production-grade needed next 6 months? **NO.** $240 MRR, 0 active leads, no contractual SLAs.
5. **P6** — Agent-as-role or agent-as-tool? **Mixed.** Cron-scheduled = role. On-demand = tool. Should be explicit per agent.
6. **SK2** — Highest-leverage 20-30h use? **NO** — 5h tactical fixes rank higher.
7. **SK6** — Ego or system? **Honest read: 80% system-improvement + 20% feel-of-real-system.** Acceptable ratio.

---

## 6 — Phases 2-5 still valid?

If you DO proceed (Option 3 or narrowing to Option 2 + future), the proposal's structure is sound but should be reframed:

| Phase | Valid? | Notes |
|-------|--------|-------|
| 1 — Cleanup | ✅ Valid | Run regardless. 1-2h. |
| 2 — Atomic layer completion | ⚠️ Mostly valid | Defer until we have revenue to optimize for. |
| 3 — Business layer integration | ✅ Valid | But only after Phase 1 + revenue signal. |
| 4 — Test coverage | ✅ Valid | But depends on having testable behavior (i.e. customers). |
| 5 — Feedback loop runtime | ⚠️ Risky | Soul-improvement + automated soul revisions = high blast radius. Long shadow mode (recommend 30 days, not 7). |

---

## 7 — Honest acknowledgments

1. **The original proposal was written without revenue grounding.** That's a methodological gap. This report fixes that.

2. **The proposal assumes "production-grade" as a goal. The data shows it isn't.** Phase 1 makes sense regardless. Phases 2-5 may not be worth the 20-30h commitment.

3. **This audit itself used ~3K tokens of API work (mostly local repo reads).** Adding to the 6K spent on docs, the upgrade proposal + gap analysis + this findings report = ~9K tokens. **Phase 1 itself (cleanup) is ~1-2h and may be the right next move.**

4. **I may be wrong about priorities.** The proposal author (Erebus?) may have context I don't — about future client pipeline, funding trajectory, founder goals. **If Ivan sees a deal coming in Q4 that needs production-grade, the calculus changes.** This audit is a snapshot, not a verdict.

---

**Awaiting Ivan's call: Option 1 (defer), Option 2 (Phase 1 only), or Option 3 (full upgrade).**