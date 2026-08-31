# PHASE 14: COMPLETE UPDATED PLAN — All Remaining Areas of Work
## Synthesizing: hermes-implementation (`41af5b`) + AI-coaching-research (`e56856`) + 3 prior phases of agents-v2 buildout

> **Compiled**: 2026-08-15 by Erebus for AI Whisperers Paraguay EAS
> **Source sessions analyzed**:
> - `@session:default/20260814_204100_41af5b` — "Hermes Implementation Analysis" (820 msgs, Eneve migration)
> - `@session:default/20260814_200344_e56856` — "AI Coaching Company Research" (208 msgs, 8 research docs)
> - Earlier phases (0-13) documented in `/opt/data/agents-v2/`
>
> **Current state verified on disk**:
> - 182 skills in registry (10 PASS, 166 NOTES, 6 HIGH, 0 FAIL)
> - 5/5 collections passing
> - 11 governance-rules + ENEVE-PATTERNS.md (575 lines) + UPGRADE-GUIDE.md (462 lines)
> - 6 agent-applications deployed
> - 31 agent PROMPT.md files, 49 cron jobs, 10 SQLite DBs
> - **SELF-RUNNING ACHIEVED** at v0.2.0 (all 7 lead agents delivered in 7-day window)

---

## PART 1: WHAT'S STILL PENDING FROM SESSION `41af5b` (Eneve migration)

The session ended with "ALL COMPLETE" but claimed vs. disk tells a different story. Here's the honest gap:

### 1.1 Tier A — High-impact operational (claimed done, partially verified)

| # | Pattern | Claimed in session | Actually on disk | Status |
|---|---------|--------------------|-------------------|--------|
| 1 | agent-application rules (per domain) | 6 files written | ✅ 6 files in `_agent-applications/` | ✅ DONE |
| 2 | sync-log.md (audit trail) | Identified as missing | ❌ **STILL MISSING** | TODO (4h) |
| 3 | disable-model-invocation support | Identified as missing | ❌ **NOT IN AUDIT** | TODO (1h) |
| 4 | cross-references.mdc | Added as `rule-cross-references.md` | ✅ 373 lines | ✅ DONE |
| 5 | validate-yaml.py standalone | Identified as missing | ❌ **NOT EXTRACTED** | TODO (30 min) |
| 6 | collections validator | Added as `audit collections` | ✅ 5/5 passing | ✅ DONE |
| 7 | OPSEC check pattern | Added as `audit opsec` | ✅ Done | ✅ DONE |
| 8 | recommended-models.yaml | Identified as missing | ❌ **STILL MISSING** | TODO (4h) |
| 9 | catalog-diagnostics | Identified as missing | ❌ **NOT IMPLEMENTED** | TODO (6h) |
| 10 | condense logic | Identified as flag-only | ⚠️ Partial (flag, not condense) | TODO (1 day) |
| 11 | improvement-cycle scoring | Identified as missing | ❌ **NOT IMPLEMENTED** | TODO (4h) |
| 12 | merge-orchestrator | Identified as missing | ❌ **NOT IMPLEMENTED** | TODO (1 day) |

**Remaining Tier A: 7 patterns × ~30h = ~30 hours of work**

### 1.2 Tier B — Medium leverage (claimed "next")

| # | Pattern | Status |
|---|---------|--------|
| 1 | PR-time MUST-PASS enforcement (GitHub Actions workflow) | ❌ Missing (1 day) |
| 2 | Tag-based versioning automation (`process-skill-bump.py`) | ❌ Missing (1 day) |
| 3 | CSL community skill import (`process-skill-import.py`) | ❌ Missing (1 day) |
| 4 | `model_hints` actually passed to LLM (currently metadata only) | ❌ Missing (4h) |
| 5 | 5-9 per-governance-rule exemplars (currently only 1 total) | ⚠️ Partial (2-3 days) |
| 6 | `sync-log.md` writer (cron-driven) | ❌ Missing (4h) |
| 7 | 18-tier gate expansion (11 more gates) | ⚠️ 11/18 done, 7 more (3 days) |
| 8 | templar auto-extraction (>30 line blocks) | ❌ Missing (1 day) |

**Remaining Tier B: 8 patterns × ~10 days of work**

### 1.3 Tier 1 from session 20672 (claimed "do next")

| # | Pattern | Status |
|---|---------|--------|
| 1 | PowerShell scripts → Python migration | ❌ Missing (1-2 days) |
| 2 | quality-config.yaml (severity thresholds, allowed patterns) | ❌ Missing (4h) |
| 3 | Skill deprecation workflow (90-day timeline) | ❌ Missing (6h) |
| 4 | Per-governance-rule exemplars (5-9 more) | ⚠️ Partial (2-3 days) |

**Remaining Tier 1: 4 patterns × ~5-7 days of work**

---

## PART 2: WHAT'S STILL PENDING FROM SESSION `e56856` (Coaching research)

### 2.1 Research deliverables — ALL DONE (8 docs in `/opt/data/agents/research/`)

| Doc | Status |
|-----|--------|
| 200-ai-coaching-companies.md | ✅ |
| 30-coaching-research-areas.md | ✅ |
| coaching-skills-gap-audit.md | ✅ |
| coaching-strategic-implications.md | ✅ |
| sunstein-solstein-inventory.md | ✅ |
| coaching-funnel-playbook.md | ✅ |
| coaching-agents-implementation.md | ✅ |
| coaching-continuation-plan.md | ✅ |
| org-upgrade-coaching-context.md | ✅ |

### 2.2 Buildable artifacts (per the research docs)

**7 internal coaching agents** (per coaching-agents-implementation.md):
1. `coach-ivan` (4h) — weekly GROW for Ivan
2. `coach-kiki` (4h) — extends kiki-coach with full GROW+CLEAR
3. `coach-org` (6h) — quarterly org-design via Sunstein's 5 principles
4. `coach-lead-agents` (8h) — monthly supervision session
5. `coaching-content-curator` (6h) — Sunstein canon + methodology
6. `coaching-quality-reviewer` (8h) — Sunstein ethics review
7. `coaching-research-intelligence` (4h) — monitors 200-company landscape

**Subtotal: 40h**

**7 external coaching agents** (Phase 2):
1. `coach-practitioner` (16h) — the actual AI coach (killer app)
2. `coach-cohort-facilitator` (12h) — group coaching
3. `coach-onboarding` (8h) — first 30 days + Sunstein informed-consent
4. `coach-renewal-manager` (6h) — Tier A → B → C pipeline
5. `coach-roi-tracker` (12h) — adoption + behavior change + business outcomes
6. `coach-lead-finder` (12h) — Solstein coaching scorecard
7. `coach-conversion-agent` (8h) — Richar Ruiz funnel

**Subtotal: 80h**

**11 coaching skills** (per coaching-skills-gap-audit.md):
- Tier 1 (4 skills, 20h): coaching-pricing, coaching-pitch-kit, coaching-conversation-framework, coaching-trilingual-glossary
- Tier 2 (5 skills, 38h): coaching-eu-compliance, coaching-tech-stack, coaching-vertical-playbook, coaching-coach-network, coaching-privacy-protocol
- Tier 3 (2 skills, 14h): coaching-agent-debugging, coaching-roi-measurement

**Subtotal: 72h**

**4 Sunstein/Solstein skills** (per sunstein-solstein-inventory.md):
1. sunstein-ethics-review (4h)
2. solstein-pipeline-runner (6h)
3. sunstein-prompt-library (8h)
4. solstein-lite-deploy (16h)

**Subtotal: 34h**

**10 existing agent upgrades** (per org-upgrade-coaching-context.md):
- business-analyst, sales-pipeline, kiki-coach, proposal-drafter, compliance-monitor, marketing-content-producer, kiki-prep, funding-coordinator, course-producer, eval-gate-runner

**Subtotal: 10h**

---

## PART 3: WHAT'S STILL PENDING FROM PRIOR PHASES

### 3.1 From PHASE-11 (final execution)

| Item | Status |
|------|--------|
| management-coordinator 8/14 brief | ✅ Written (8/15) |
| kiki-coach 8/14 lesson | ❌ Still pending (kiki-coach trigger stuck in queue — slow reasoning model) |
| 7-day self-running milestone | ✅ Achieved this session |
| Eval-gate cron integration | ✅ Wired (eval-gate cron `7a22b3f3c2cc`) |
| Chaos tests B + C | ✅ Passed |
| Agent-specific eval scripts | ❌ eval-gate assumes business-analyst format (catches other agents as FAIL — need per-agent eval) |

### 3.2 From PHASE-13 (foundation phase)

| Item | Status |
|------|--------|
| 49/49 cron jobs with valid schedules | ✅ Fixed (28 broken schedules repaired) |
| Tier 2 sub-agents verified live | ❌ Not yet triggered (24/24 unverified) |
| Cross-cutting agents verified live | ❌ Not yet triggered (8/8 unverified) |
| 158 NOTES from skill audit (add `## Purpose & Scope` to all) | ❌ Not done |
| 6 HIGH items in current audit | ❌ Not fixed |
| LLM billing fix (only `litellm/reasoning` works, 110s/turn) | ❌ Blocked on money |

### 3.3 From this session (PHASE-14 prep)

| Item | Status |
|------|--------|
| Self-running verified | ✅ |
| Eval-gate cron wired | ✅ |
| 28 broken schedules fixed | ✅ |
| mgmt-coordinator 8/15 brief written | ✅ |

---

## PART 4: THE COMPLETE REMAINING WORK — Consolidated Plan

### Total remaining work: ~265 hours over 90 days

This is everything not yet done across all sessions. I'm grouping it into 7 streams:

```
PHASE 14-20 (Days 1-90): Complete the work across 7 streams
├── Stream A: Skill framework completion (Eneve Tier A/B/1) — 30h
├── Stream B: Coaching internal agents (Phase 1) — 40h
├── Stream C: Coaching external agents (Phase 2) — 80h
├── Stream D: Coaching skills + Sunstein/Solstein — 106h
├── Stream E: Existing agent upgrades (coaching-aware) — 10h
├── Stream F: Tier 2/cross-cutting agent live verification — 4h
└── Stream G: Skill audit cleanup (158 NOTES + 6 HIGH) — 6h
```

### 4.1 Stream A: Skill framework completion (Days 1-14)

**Owner**: Erebus (autonomous) | **Effort**: 30h | **Depends**: nothing

| # | Action | Time | Priority |
|---|--------|------|----------|
| A1 | Create `/opt/data/skills/_objetivo/quality-config.yaml` (severity thresholds) | 4h | 🔴 P1 |
| A2 | Create `sync-log.md` writer script + initial log | 4h | 🔴 P1 |
| A3 | Implement `disable-model-invocation` field support in audit | 1h | 🟡 P2 |
| A4 | Extract `validate-yaml.py` standalone tool | 30m | 🟡 P2 |
| A5 | Create `recommended-models.yaml` + `apply-models` subcommand | 4h | 🟡 P2 |
| A6 | Implement `audit score` (improvement-cycle scoring) | 4h | 🟡 P2 |
| A7 | Add 7 missing audit gates (target 18/18) | 3 days | 🟢 P3 |
| A8 | Implement real condense logic (regex substitution) | 1 day | 🟢 P3 |
| A9 | Implement `process-skill-bump.py` (auto SemVer) | 1 day | 🟢 P3 |
| A10 | Skill deprecation workflow (90-day timeline) | 6h | 🟢 P3 |
| A11 | GitHub Actions workflow for PR-time validation | 1 day | 🟢 P3 |
| A12 | `process-skill-import.py` (CSL community import) | 1 day | 🟢 P3 |
| A13 | Implement `model_hints` actually passing to LiteLLM | 4h | 🟢 P3 |
| A14 | Write 5 more per-governance-rule exemplars | 2-3 days | 🟢 P3 |
| A15 | Templar auto-extraction (>30 line blocks) | 1 day | 🟢 P3 |

### 4.2 Stream B: Internal coaching agents (Days 1-30)

**Owner**: Erebus + Kyrian | **Effort**: 40h | **Depends**: Stream D1 (coaching-conversation-framework)

| # | Agent | Time | Cron |
|---|-------|------|------|
| B1 | `coach-ivan` | 4h | Weekly Sun 18:00 PYT, private delivery |
| B2 | `coach-kiki` (extends existing) | 4h | Replaces existing kiki-coach |
| B3 | `coach-org` | 6h | Quarterly (Jan/Apr/Jul/Oct) |
| B4 | `coach-lead-agents` | 8h | Monthly (1st of month) |
| B5 | `coaching-content-curator` | 6h | Weekly Mon |
| B6 | `coaching-quality-reviewer` | 8h | After every coaching output |
| B7 | `coaching-research-intelligence` | 4h | Weekly Wed |

### 4.3 Stream C: External coaching agents (Days 31-60)

**Owner**: Erebus + Kyrian + Ivan | **Effort**: 80h | **Depends**: Stream B complete + first customers

| # | Agent | Time | Cron |
|---|-------|------|------|
| C1 | `coach-practitioner` (MVP) | 16h | On-demand (customer trigger) |
| C2 | `coach-cohort-facilitator` | 12h | Weekly (cohort sessions) |
| C3 | `coach-onboarding` | 8h | Once per new customer |
| C4 | `coach-renewal-manager` | 6h | Monthly |
| C5 | `coach-roi-tracker` | 12h | Weekly |
| C6 | `coach-lead-finder` | 12h | Weekly |
| C7 | `coach-conversion-agent` | 8h | On-demand (webhook from CF Worker) |

### 4.4 Stream D: Coaching + Sunstein/Solstein skills (Days 1-45)

**Owner**: Erebus + Kyrian | **Effort**: 106h | **Depends**: nothing (parallel to B/C)

| # | Skill | Tier | Time |
|---|-------|------|------|
| D1 | coaching-conversation-framework (GROW + CLEAR + Sunstein) | 1 | 4h |
| D2 | coaching-pricing | 1 | 4h |
| D3 | coaching-pitch-kit | 1 | 4h |
| D4 | coaching-trilingual-glossary (ES/NL/EN) | 1 | 8h |
| D5 | coaching-eu-compliance (EU AI Act + GDPR Art 9) | 2 | 8h |
| D6 | coaching-tech-stack (LLM + RAG + voice benchmarks) | 2 | 8h |
| D7 | coaching-vertical-playbook (5 verticals × 4h) | 2 | 20h |
| D8 | coaching-coach-network (ICF LATAM/EU partner model) | 2 | 6h |
| D9 | coaching-privacy-protocol (encryption + retention) | 2 | 8h |
| D10 | coaching-agent-debugging | 3 | 8h |
| D11 | coaching-roi-measurement | 3 | 6h |
| D12 | sunstein-ethics-review | Sunstein | 4h |
| D13 | solstein-pipeline-runner | Solstein | 6h |
| D14 | sunstein-prompt-library (30 prompts × 3 langs) | Sunstein | 8h |
| D15 | solstein-lite-deploy (public research tool) | Solstein | 16h |

### 4.5 Stream E: Existing agent upgrades (coaching-aware) (Days 1-7)

**Owner**: Erebus | **Effort**: 10h | **Depends**: D1 (framework)

| # | Agent | Time | Change |
|---|-------|------|--------|
| E1 | business-analyst | 1h | Add Sunstein-aligned framing + coaching-MRR sub-line |
| E2 | sales-pipeline | 1h | Add ICF active-listening + coaching-vertical pricing |
| E3 | kiki-coach | 1h | Upgrade to full GROW+CLEAR+Sunstein |
| E4 | proposal-drafter | 1h | Use coaching-pricing skill |
| E5 | compliance-monitor | 1h | EU AI Act risk classification |
| E6 | marketing-content-producer | 1h | Sunstein-aligned methodology in testimonials |
| E7 | kiki-prep | 1h | ICF 8 competencies in lesson plans |
| E8 | funding-coordinator | 1h | Coaching-vertical as sub-track |
| E9 | course-producer | 1h | ICF-aligned content for coaching courses |
| E10 | eval-gate-runner | 1h | Add Sunstein ethics gate |

### 4.6 Stream F: Live verification of 32 unverified agents (Days 1-3)

**Owner**: Erebus | **Effort**: 4h | **Depends**: nothing

| # | Action | Time |
|---|--------|------|
| F1 | Trigger all 14 Tier 2 sub-agents and verify brief output | 2h |
| F2 | Trigger all 8 cross-cutting agents and verify output | 1h |
| F3 | Build agent-specific eval scripts (10 of them) | 1h |

### 4.7 Stream G: Skill audit cleanup (Days 1-2)

**Owner**: Erebus | **Effort**: 6h | **Depends**: nothing

| # | Action | Time |
|---|--------|------|
| G1 | Add `## Purpose & Scope` to 158 skills (auto-fix style) | 3h |
| G2 | Investigate + fix 6 HIGH items in current audit | 1h |
| G3 | Update 158 skills with `provenance.last_review` | 2h |

---

## PART 5: ENEVE BEST PRACTICES (the principles — distilled)

From the session's deep analysis, the 5 pillars to internalize:

1. **Stable IDs** — `rule.<domain>.<name>.v<MAJOR>` format. Apply to every new agent/skill/template.
2. **Three invocation strategies** — file-mask (globs/governs), agentic (description), always-apply. Pick the right one.
3. **Frontmatter with provenance + model_hints** — every artifact declares `owner`, `last_review`, `temp`, `top_p`.
4. **Templars + exemplars as separate artifacts** — output shapes (templars) vs pattern examples (exemplars, never copied).
5. **The improvement loop** — periodic atomic cycles per artifact (improve → enhance → extract → condense → script-extract).

The 9 rule-authoring governance-rules governing how every other rule is written. We have all 9 + 2 new ones (cross-references, templars-and-exemplars) = **11 governance-rules total**.

The 5-stage atomic improvement cycle:
1. `find-prompts-needing-review`
2. `process-prompt-improvement-cycle`
3. `improve` ← fix critical issues
4. `enhance` ← add examples, decision trees, CoT
5. `find-extraction-candidates` → extract-templar-exemplar

The 18-tier validation pipeline (Eneve's `validate-pre-merge.ps1`):
1. YAML parse ✅
2. Frontmatter completeness ✅
3. ID format ✅
4. alwaysApply field ✅
5. Invocation strategy ✅
6. Contract presence ✅ (NEW)
7. Body structure ✅
8. Cross-references resolve ✅
9. Checklist presence ✅
10. Checklist item count ✅
11. Examples present ✅ (NEW)
12. Anti-patterns present ✅ (NEW)
13. References present ⚠️ Deferred (only when `requires:` non-empty)
14. Provenance present ✅
15. last_review within 90 days ✅
16. OPSEC check ✅
17. Sync log entry ❌
18. Test pass (if applicable) ❌

**Current coverage: 11/18 → 13/18 after this session → target 18/18 by end of PHASE-14**

---

## PART 6: DAY-BY-DAY EXECUTION (90-day calendar)

### Days 1-14 — Foundation + Skill framework + Verify existing
- Day 1-2: Stream G (skill cleanup, 6h) + Stream F (live verify, 4h)
- Day 3: A1 (quality-config.yaml) + A2 (sync-log)
- Day 4-5: Stream E (10 existing agent upgrades)
- Day 6-7: A3 + A4 + A5 + A6 (4 Eneve quick wins)
- Day 8-9: D1 + D2 (coaching-conversation-framework + coaching-pricing)
- Day 10-11: B1 (coach-ivan) + first session
- Day 12-14: B2 (coach-kiki extends existing) + D3 + D4

**Deliverables end of Week 2**:
- ✅ 158 skills have `## Purpose & Scope`
- ✅ 32 unverified agents triggered + verified
- ✅ quality-config.yaml + sync-log live
- ✅ 5 Eneve Tier-A patterns complete
- ✅ 10 existing agents coaching-aware
- ✅ 2 coaching skills built (conversation-framework + pricing)
- ✅ 2 internal coaching agents (coach-ivan + coach-kiki)

### Days 15-30 — Internal coaching + Sunstein/Solstein
- Day 15-17: B3 (coach-org) + B4 (coach-lead-agents)
- Day 18-20: B5 (coaching-content-curator) + B6 (coaching-quality-reviewer)
- Day 21-22: B7 (coaching-research-intelligence) + D12 (sunstein-ethics-review)
- Day 23-25: D5 + D6 + D8 (3 coaching Tier 2 skills)
- Day 26-28: D7 (vertical playbooks) + D13 (solstein-pipeline-runner)
- Day 29-30: 30-day review per REVIEW-2026-Q4.md

**Deliverables end of Week 4**:
- ✅ All 7 internal coaching agents built
- ✅ 4 Sunstein/Solstein skills started
- ✅ 5 coaching verticals have playbooks
- ✅ 30-day review complete

### Days 31-60 — External coaching agents
- Day 31-37: C1 (coach-practitioner MVP) + D9 + D10 (privacy + debugging)
- Day 38-44: C2 (coach-cohort-facilitator) + D11 (roi-measurement) + D14 (sunstein-prompt-library)
- Day 45-50: C3 (coach-onboarding) + C4 (coach-renewal-manager)
- Day 51-58: C5 (coach-roi-tracker) + C6 (coach-lead-finder)
- Day 59-60: C7 (coach-conversion-agent) + D15 (solstein-lite-deploy)

**Deliverables end of Week 8**:
- ✅ All 7 external coaching agents built
- ✅ 11 coaching skills + 4 Sunstein/Solstein skills
- ✅ First free quick-win delivered

### Days 61-90 — Scale + constitutional v0.3.0
- Day 61-70: 10 free quick-wins across 5 verticals
- Day 71-80: 3 Tier A customers signed; first Tier B upgrade
- Day 81-88: EU AI Act compliance; first EU client
- Day 89-90: 90-day review per REVIEW-2026-Q4.md

**Deliverables end of Week 12**:
- ✅ 30+ customers across 5 verticals
- ✅ $89-150K ARR run rate
- ✅ Constitutional v0.3.0 ready

---

## PART 7: DECISION FRAMEWORK — What to do TODAY

The 7 streams have different urgencies and dependencies. Recommended ordering:

### 🔴 Priority 1 (Days 1-7) — Fix what we already built

| # | Action | Time | Why |
|---|--------|------|-----|
| 1 | Live-verify 32 unverified agents | 4h | Untested code is unknown code |
| 2 | Add `## Purpose & Scope` to 158 skills | 3h | Closes the 166 NOTES in audit |
| 3 | Fix 6 HIGH items in current audit | 1h | Final cleanup |
| 4 | Build quality-config.yaml | 4h | Foundation for everything else |
| 5 | Build sync-log.md | 4h | Audit trail for future changes |

**Total: 16h over 7 days**

### 🟡 Priority 2 (Days 8-14) — Coaching foundation

| # | Action | Time | Why |
|---|--------|------|-----|
| 6 | coaching-conversation-framework skill | 4h | IP backbone for all coaching agents |
| 7 | coach-ivan + first session | 5h | Personal value + methodology test |
| 8 | 5 Eneve quick wins (A3-A6) | 12h | Foundation tooling |
| 9 | 10 existing agent upgrades | 10h | Backward compat with coaching product |

**Total: 31h over 7 days**

### 🟢 Priority 3 (Days 15-90) — Coaching buildout + framework completion

See Streams A-D in Part 4.

---

## PART 8: WHAT TO TELL IVAN (THE BOTTOM LINE)

You have 7 streams of remaining work totaling ~265 hours over 90 days:

1. **Skill framework completion (30h)** — 15 Eneve patterns not yet built (Tier A + Tier B + Tier 1)
2. **Coaching internal agents (40h)** — 7 agents for Ivan, Kiki, org, lead-agents, content, quality, research
3. **Coaching external agents (80h)** — 7 agents for the actual coaching product
4. **Coaching + Sunstein/Solstein skills (106h)** — 15 skills for methodology, pricing, EU compliance, etc.
5. **Existing agent upgrades (10h)** — Add Sunstein + ICF references to 10 existing agents
6. **Live verification (4h)** — Trigger 32 unverified agents
7. **Skill audit cleanup (6h)** — Fix 158 NOTES + 6 HIGH

The single highest-value action today: **live-verify the 32 unverified agents** (4h). Until we know they work, we don't know if the foundation is solid.

The single highest-value action this week: **build coaching-conversation-framework skill** (4h). It blocks all 7 coaching agents — until it exists, every coaching agent has to reinvent GROW+CLEAR.

**No new code needs to be written** until the LLM billing is fixed or until you accept the slow `litellm/reasoning` model. The coaching agents are just MORE agents that go through the same pattern.

## Single bet

Hit the self-running milestone (DONE ✅). Now:
- Week 1: verify 32 unverified + clean 158 skill audit notes
- Week 2: build coaching-conversation-framework + coach-ivan
- Week 3-12: build out the 14 coaching agents + 15 skills per the priority framework
- Day 90: constitutional v0.3.0 with $89-150K ARR + 30+ customers

## Files cited

### From session `41af5b` (Eneve migration):
- `/opt/data/skills/_objetivo/ENEVE-PATTERNS.md` (23 KB, 575 lines)
- `/opt/data/skills/_objetivo/UPGRADE-GUIDE.md` (16 KB, 462 lines)
- `/opt/data/skills/_objetivo/rule-cross-references.md` (11 KB, 373 lines)
- `/opt/data/skills/_objetivo/rule-templars-and-exemplars.md` (8.5 KB, 267 lines)
- `/opt/data/skills/_objetivo/loop/prompt-improvement-loop.json`
- `/opt/data/skills/_agent-applications/*.md` (6 files)
- `/opt/data/skills/_collections/*.yaml` (5 files, all passing)
- `/opt/data/scripts/hermes-skills-audit.py` (12 commands, 11/18 gates)
- `/opt/data/scripts/process-skill-improvement-cycle.py` (5-stage loop)

### From session `e56856` (coaching research):
- `/opt/data/agents/research/200-ai-coaching-companies.md`
- `/opt/data/agents/research/30-coaching-research-areas.md`
- `/opt/data/agents/research/coaching-skills-gap-audit.md`
- `/opt/data/agents/research/coaching-strategic-implications.md`
- `/opt/data/agents/research/sunstein-solstein-inventory.md`
- `/opt/data/agents/research/coaching-funnel-playbook.md`
- `/opt/data/agents/research/coaching-agents-implementation.md`
- `/opt/data/agents/research/coaching-continuation-plan.md`
- `/opt/data/agents/research/org-upgrade-coaching-context.md`

### From agents-v2 buildout:
- `/opt/data/agents-v2/PHASE-0..13-COMPLETE.md` (14 phase notes)
- `/opt/data/agents-v2/PLAN-v5.md`
- `/opt/data/agents-v2/SELF-RUNNING-CRITERIA.md`
- `/opt/data/agents-v2/REVIEW-2026-Q4.md`
- `/opt/data/agents-v2/scripts/self-running-check.py`
- `/opt/data/agents-v2/scripts/eval/aiw-eval-gate-runner.sh`
- `/opt/data/agents-v2/eval-gate.py`

### This document:
- `/opt/data/agents-v2/PHASE-14-COMPLETE-UPDATED-PLAN.md` (this file)

## Last updated

2026-08-15 by Erebus (this session)
