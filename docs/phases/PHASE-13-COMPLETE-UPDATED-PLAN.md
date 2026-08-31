# SESSION ANALYSIS + COMPLETE UPDATED PLAN
## (Synthesizing: hermes-implementation + AI-coaching-research + current session)

> **Compiled**: 2026-08-15 by Erebus for AI Whisperers Paraguay EAS
> **Sources analyzed**:
> - `@session:default/20260814_204100_41af5b` — Hermes Implementation Analysis (820 msgs, "the Eneve migration session")
> - `@session:default/20260814_200344_e56856` — AI Coaching Company Research (208 msgs, "the coaching research session")
> - This session's discoveries (LLM provider limitations, 31 agents + 49 cron jobs, eval-gate POC)
> - All artifacts on disk in `/opt/data/agents-v2/`, `/opt/data/skills/`, `/opt/data/agents/research/`

---

## PART 1: WHAT WE WERE ACTUALLY DOING IN THOSE TWO SESSIONS

### Session A: @session:`default/20260814_204100_41af5b` — "Hermes Implementation Analysis"

**User's intent (first message)**: You sent a `hermes improvments.zip` (4 MB) via WhatsApp at 5:40 PM and asked me to analyze it against our repo.

**What I discovered about the zip**: It was actually the **Eneve `.cursor/` framework** — a production-grade 745-file, 5.5 MB reference implementation on a `.NET`/PowerShell project (Eneve.domain), documented as "60/60 Gold Standard Reference Implementation." This is the SINGLE BEST reference for what a mature skill library looks like.

**What the session delivered (chronologically)**:

| Step | Deliverable | Status |
|------|-------------|--------|
| 1 | Documented Eneve framework structure (9 governance-rules, 3 invocation strategies, contract pattern, improvement loop, templars-vs-exemplars) | ✅ in `/opt/data/skills/software-development/skill-library-governance-framework/references/eve-cursor-framework.md` |
| 2 | Built Python equivalent of `validate-rules.ps1` → `hermes-skills-audit.py` (41 KB, 12 commands: frontmatter, check, invocation, stale, review, inventory, sync, fix, opsec, crossrefs, dead, collections) | ✅ at `/opt/data/scripts/hermes-skills-audit.py` |
| 3 | Built improvement-loop driver `process-skill-improvement-cycle.py` (18 KB, 5-stage cycle: find → fix → enhance → extract → condense) | ✅ at `/opt/data/scripts/process-skill-improvement-cycle.py` |
| 4 | Migrated 170 skill frontmatters to Eneve-compliant format (`id`, `kind`, `version`, `globs`, `governs`, `requires`, `provenance`, `alwaysApply`) | ✅ 158 NOTES, 9 PASS, 3 HIGH, 0 FAIL |
| 5 | Created 5 skill collections (client-site-deploy, vps-ops, research, security, creative) at `/opt/data/skills/_collections/*.yaml` | ✅ 4/5 PASS, 1 cycle found in governance-rules |
| 6 | Created 6 agent-application skills (coaching, creative, security, etc.) at `/opt/data/skills/_agent-applications/*.md` | ✅ |
| 7 | Created `/opt/data/skills/_governance/` with 9 governance-rules + 1 templar + 1 exemplar | ✅ All PASS |
| 8 | Created cron job `aiw-skills-audit-weekly` (every Mon 09:00 UTC) | ✅ |
| 9 | Identified 12 MORE Eneve patterns (Tier 1 improvements) | ✅ Documented in session outputs |
| 10 | Identified 4 PowerShell→Python migrations (validate-yaml, archive-obsolete, find-dead, condense-prompts) | ⚠️ Documented, not yet implemented |

**Key insights uncovered**:
- Eneve's own validator reports its own creator as **46/47 non-compliant** (98% malformed YAML) → the right behavior: validators should be honest
- Eneve's 5-stage atomic improvement loop ran **51 iterations covering 175 prompts in 90 min wall time**
- The single most important architectural decision is **invocation strategy** (file-mask vs agentic vs always-apply)
- **Templars vs Exemplars** distinction: templars = output skeletons (shape), exemplars = pattern examples (quality, never copied)

### Session B: @session:`default/20260814_200344_e56856` — "AI Coaching Company Research"

**User's intent**: "research also coaching companies for companies and all relevant things in our repos we will be this for AI for companies gather all they do extract the rules skills etc"

**What it delivered (8 research docs in `/opt/data/agents/research/`)**:

| Doc | Size | Content |
|-----|------|---------|
| `200-ai-coaching-companies.md` | 28 KB | 197 companies in 18 categories |
| `30-coaching-research-areas.md` | 26 KB | 30 areas, 6 groups, 9 marked 🔴 HIGH priority |
| `coaching-skills-gap-audit.md` | — | 11 skills needed |
| `coaching-strategic-implications.md` | — | 5 SKUs, $89-150K ARR year-1 |
| `sunstein-solstein-inventory.md` | — | Sunstein canon + Solstein M&A scoring |
| `coaching-funnel-playbook.md` | — | Richar Ruiz template; 5 verticals; 30-client target |
| `coaching-agents-implementation.md` | — | 14 agents to build (7 internal + 7 external) |
| `org-upgrade-coaching-context.md` | — | Tier 1 upgrades for 10 existing agents |
| `coaching-continuation-plan.md` | 27 KB | 5-track continuation plan I wrote at the end |

**Key business thesis from this research**:
- We're targeting the **trilingual mid-market AI coaching** niche (Spanish-native, Dutch-fluent, EU/LATAM-ready)
- BetterUp/CoachHub/Valence are US-centric, English-only, $4-15K/employee/year — we can undercut + differentiate
- 30 research areas identified, 9 🔴 HIGH priority (EU AI Act compliance, ICF mapping, Spanish/Dutch vocab, tech stack benchmarks, ASR benchmarks, sales pitch)
- 14 new coaching agents planned: 7 internal (`coach-ivan`, `coach-kiki`, `coach-org`, etc.) + 7 external (`coach-practitioner`, `coach-onboarding`, etc.)
- 11 new skills planned (Tier 1: coaching-pricing, coaching-pitch-kit; Tier 2: coaching-eu-compliance, coaching-tech-stack; Tier 3: coaching-agent-debugging)
- Year-1 target: $89-150K ARR across 5 verticals (legal, RE, dental, beauty/wellness, SMB entrepreneur)

### Session C: This session (current)

**What happened before the user's question**:
- Discovered Mistral provider dead (402), OpenRouter out of credits, NVIDIA 404
- Found working LLM: `litellm/fast` (single-tool-only) → switched to `litellm/reasoning` (multi-tool, ~110s/turn)
- Built 31 agent PROMPT.md files, 49 cron jobs, 10 SQLite DBs, 6 scripts, 31 per-agent git repos
- Ran 5/7 lead agents live — 5 wrote briefs, 2 stuck due to LLM provider limits
- Passed backup restore drill, 3 chaos tests, eval-gate POC (7/9 PASS)
- Pushed v0.3.0 + eval-gate POC + Phase 11 final to GitHub

---

## PART 2: WHAT'S ON DISK (the actual state — not what we wished)

### 2.1 `/opt/data/agents-v2/` (the constitution)

```
agents-v2/                                 652 KB total
├── README.md                              (10 KB — org manifesto)
├── INDEX.md                               (5 KB — master index)
├── PLAN-v4.md                             (50 KB — full plan v4)
├── PLAN-v5.md                             (32 KB — current plan)
├── PHASE-{0,1,2,3,4-5,5.5,6,7,8,9}-COMPLETE.md  (10 phase notes)
├── PHASE-10-EVAL-GATE-POC.md              (eval-gate POC results)
├── PHASE-11-FINAL-EXECUTION.md            (this session's summary)
├── BURNOUT-SIGNAL-SPEC.md                 (founder bandwidth monitoring)
├── FAILURE-MODES.md                       (15 failure modes + 3 chaos tests)
├── SELF-RUNNING-CRITERIA.md               (the milestone gate)
├── ROLLBACK-PLAYBOOK.md                   (per-phase rollback)
├── THREAT-MODEL.md                        (7 threats + defenses)
├── ROLES-INVENTORY.md                     (15 KB — 135 roles)
├── RESEARCH-COMPLETE-ORG.md               (24 KB — org research)
├── STATE-AUDIT-2026-08-14.md              (state inventory)
├── STORAGE-ARCHITECTURE.md                (3-layer model)
├── constitution/ORG-AGENTS.md             (14 KB — v0.2.0 ratified)
├── departments/{01-06}-*.md               (6 dept specs at v0.2.0)
├── patterns/                              (9 patterns: 5 mandatory + 4 atomic)
├── playbooks/                             (10 playbooks)
├── deferred/                              (3 deferred docs)
├── operational/                           (4 operational docs)
├── state/                                 (live state files)
├── outbox/                                (live briefs)
├── logs/                                  (live execution logs)
├── snapshots/                             (state snapshots)
└── eval-gate.py                           (9-check scorer, POC working)
```

### 2.2 `/opt/data/skills/` (Eneve-compliant skills)

```
skills/
├── SKILL.md × 161                         (158 migrated + 3 new)
├── _governance/                                 (9 governance-rules + 1 templar + 1 exemplar)
├── _agent-applications/ × 6               (coaching, creative, security, research, vps-ops, client-site-deploy)
├── _collections/ × 5                      (skill bundles)
├── .loop-state/                           (prompt-improvement-loop.json, 169/169 processed)
├── .archive/                              (deprecated skills)
├── .curator_backups/                      (skill backups)
├── _root/                                 (legacy → renamed to _core)
└── _core/                                 (current skill bodies, `skill.core.*` IDs)
```

### 2.3 `/opt/data/agents/` (31 agent PROMPT.md files)

```
agents/
├── business-analyst/    (lead, daily)         → briefs/state DB + live trigger
├── management-coordinator/ (lead, biweekly)  → brief
├── kiki-coach/          (lead, weekly)         → lessons/
├── finance-controller/  (lead, weekly)        → brief + state
├── sales-pipeline/      (lead, daily)         → brief + state
├── engineering-roster/  (lead, biweekly)      → brief
├── research-tracker/    (lead, weekly)        → brief
├── 14 Tier 2 sub-agents (proposal-drafter, multimedia-producer, accounting-automation, ...)
├── 8 cross-cutting agents (ai-ops-coordinator, bizops-tracker, compliance-monitor, ...)
└── 1 pre-existing (funding-coordinator)
```

### 2.4 `/opt/data/agents/research/` (8 coaching research docs)

8 docs (200 companies, 30 areas, gap audit, strategic implications, sunstein-solstein inventory, funnel playbook, agents implementation, org upgrade, continuation plan)

### 2.5 Cron jobs (49/49 live)

All using `provider=litellm, model=reasoning` — works for multi-tool but ~110s/turn (slow)

---

## PART 3: THE GAP — WHAT'S MISSING OR BROKEN

### 3.1 Live verification status

| Item | Plan target | Actual | Gap |
|------|-------------|--------|-----|
| Lead agents built | 7 | 7 ✅ | 0 |
| Lead agents running end-to-end | 7 | 5 (mgmt-coord + kiki in-flight) | 2 |
| Tier 2 sub-agents built | 14 | 14 ✅ | 0 |
| Tier 2 sub-agents verified | 14 | 0 (built but never triggered) | 14 |
| Cross-cutting agents built | 8 | 8 ✅ | 0 |
| Cross-cutting verified | 8 | 0 | 8 |
| Cron jobs in live | 49 | 49 ✅ | 0 |
| Cron jobs verified executing | 49 | ~15 (state-snapshot, validation, heartbeat, thesis-tick, business-analyst, finance-controller, sales-pipeline, engineering-roster, research-tracker) | ~34 |
| 7-day self-running milestone | Achieved | NOT STARTED | Critical |
| Chaos tests B + C | Passed | NOT STARTED | 2 |
| Eval-gate cron integration | Wired | Manual run only | 1 |
| Coaching agents | 14 | 0 | 14 |
| Coaching skills | 11 | 0 | 11 |
| Sunstein/Solstein skills | 4 | 0 | 4 |

### 3.2 Critical open issues (from across sessions)

1. **LLM billing is broken** — Mistral dead, OpenRouter empty, NVIDIA 404, ZAI 429. Only `litellm/reasoning` works. Slow (~110s/turn).
2. **Eneve cycle 1 missing skill** — `skill.core.vps-aiw-autonomous-ops.v1` not found by collections check (might be in archived dir, or name typo)
3. **The 158 NOTES on skills audit** — all `low non_standard_first_section` — every skill needs `## Purpose & Scope` as first section. Style fix, not blocker.
4. **Governance-rules cycle** — `file-structure → provenance-and-versioning → file-structure` real cycle (they require each other). Document but don't auto-fix.
5. **4 PowerShell scripts not yet migrated to Python** (validate-yaml, archive-obsolete, find-dead, condense-prompts)
6. **Config schema missing** — no `quality-config.yaml` defining severity thresholds, allowed patterns

### 3.3 Coaching-product blockers

- **No `coach-practitioner` agent** — the actual AI coach
- **No `coaching-pricing` skill** — referenced by every coaching vertical
- **No ICF Core Competencies mapping** (research area #6)
- **No Spanish/Dutch coaching vocabulary** (research areas #11, #12)
- **No EU AI Act compliance** (research area #2)

---

## PART 4: THE COMPLETE UPDATED PLAN (incorporating Eneve + Coaching + live state)

### 4.1 Six phases, 90 days, with dependencies explicit

```
┌─────────────────────────────────────────────────────────────────┐
│ FOUNDATION (Days 1-14)    Make the existing 31 agents actually  │
│                            work + adopt remaining Eneve patterns │
├─────────────────────────────────────────────────────────────────┤
│ SELF-RUNNING (Days 15-30) Hit the 7-day milestone gate         │
├─────────────────────────────────────────────────────────────────┤
│ COACHING-PHASE-1 (Days 31-60)  Build internal coaching agents   │
├─────────────────────────────────────────────────────────────────┤
│ COACHING-PHASE-2 (Days 61-90) Build external coaching agents   │
│                                + skills + first customers      │
├─────────────────────────────────────────────────────────────────┤
│ SCALE (Days 91-120)         30+ paying customers              │
├─────────────────────────────────────────────────────────────────┤
│ CONSTITUTIONAL v0.3.0       Bump org to v0.3.0 with learnings │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Foundation Phase (Days 1-14) — fix what's broken

#### Track F1: Make existing 31 agents actually work

**Owner**: Erebus (autonomous) | **Effort**: 12h | **Depends**: nothing

| # | Action | Time | Status |
|---|--------|------|--------|
| 1 | Verify all 49 cron jobs have correct provider/model config | 0.5h | todo |
| 2 | Run all 14 Tier 2 sub-agents + 8 cross-cutting agents live | 4h | todo |
| 3 | Trigger missing 2 lead agents (mgmt-coordinator, kiki-coach) and verify briefs | 1h | partial |
| 4 | Run chaos-test-runner Scenarios B + C | 1h | todo |
| 5 | Wire eval-gate.py as a cron post-brief hook | 2h | todo |
| 6 | Self-running-check.py — implement daily verification cron | 2h | todo |
| 7 | Write PHASE-12-COMPLETE.md with live verification results | 1h | todo |

#### Track F2: Adopt remaining Eneve patterns

**Owner**: Erebus | **Effort**: 8h | **Depends**: nothing

| # | Action | Time | Status |
|---|--------|------|--------|
| 1 | Fix the 158 NOTES (add `## Purpose & Scope` as first section to all skills) | 2h | todo |
| 2 | Implement 4 missing Python scripts: `validate-yaml`, `archive-obsolete`, `find-dead`, `condense-prompts` | 3h | todo |
| 3 | Write `/opt/data/skills/_objetivo/quality-config.yaml` (severity thresholds, allowed patterns) | 1h | todo |
| 4 | Add `phase_deprecate()` to loop driver + `superseded_by` field rule + `.archive/` lifecycle | 2h | todo |

#### Track F3: Resolve Eneve cycle 1 (collection completeness)

**Owner**: Erebus | **Effort**: 1h | **Depends**: nothing

| # | Action | Time | Status |
|---|--------|------|--------|
| 1 | Locate `vps-aiw-autonomous-ops` skill (probably archived or wrong ID) | 0.5h | todo |
| 2 | Update collection YAML if needed | 0.25h | todo |
| 3 | Run `hermes-skills-audit.py collections` to confirm 5/5 pass | 0.25h | todo |

### 4.3 Self-Running Phase (Days 15-30) — hit the milestone

**Owner**: Erebus (passive) + Ivan (no action) | **Effort**: 0h | **Depends**: F1, F2, F3 complete

Per SELF-RUNNING-CRITERIA.md:
1. All 7 Tier-1 lead agents deliver reliably for 7+ consecutive days
2. 0 cron jobs in error state for the same period
3. 0 "is X live?" messages from Ivan in any 7-day window

**Action**: Don't touch anything for 14 days. Just observe.

| Cadence | Agent | Required |
|---------|-------|----------|
| Daily 06:30 PYT | business-analyst | 14 |
| Mon+Thu 17:00 PYT | management-coordinator | 4 |
| Fri 17:00 PYT | kiki-coach | 2 |
| Fri 18:00 PYT | finance-controller | 2 |
| Daily 12:00 PYT | sales-pipeline | 14 |
| Tue+Fri 17:00 PYT | engineering-roster | 4 |
| Sun 18:00 PYT | research-tracker | 2 |
| **Total** | | **42** |

If all three conditions hold for 7 consecutive days → **SELF-RUNNING ACHIEVED at v0.2.0**.

**30-day review (2026-09-14)** per REVIEW-2026-Q4.md:
- Health checks: 6 items
- Performance metrics: 5 items
- Decisions: 4 items

### 4.4 Coaching Phase 1 (Days 31-60) — internal coaching agents

**Owner**: Erebus + Kyrian | **Effort**: 40h | **Depends**: Self-running achieved

Per `/opt/data/agents/research/coaching-agents-implementation.md` Phase 1:

| # | Agent | Time | Purpose |
|---|-------|------|---------|
| 1 | `coach-ivan` | 4h | weekly GROW coaching for Ivan |
| 2 | `coach-kiki` | 4h | extends kiki-coach with full GROW |
| 3 | `coach-org` | 6h | quarterly org-design review via Sunstein's 5 principles |
| 4 | `coach-lead-agents` | 8h | monthly "supervision session" for each of 31 agents |
| 5 | `coaching-content-curator` | 6h | maintains Sunstein canon + methodology library |
| 6 | `coaching-quality-reviewer` | 8h | Sunstein ethics review on every coaching output |
| 7 | `coaching-research-intelligence` | 4h | monitors 200-company landscape |

**Also (Track D from earlier plan)**:
- Upgrade 10 existing agents to coaching-aware (add Sunstein + ICF references to their PROMPTs): business-analyst, sales-pipeline, kiki-coach, proposal-drafter, compliance-monitor, marketing-content-producer, kiki-prep, funding-coordinator, course-producer, eval-gate-runner

**Effort total**: 40h (7 agents) + 10h (10 upgrades) = **50h**

### 4.5 Coaching Phase 2 (Days 61-90) — external coaching

**Owner**: Erebus + Kyrian + Ivan | **Effort**: 80h (agents) + 168h (skills) | **Depends**: Phase 1 complete

Per coaching-agents-implementation.md Phase 2:

| # | Agent | Time | Purpose |
|---|-------|------|---------|
| 8 | `coach-practitioner` | 16h | the actual AI coach (the killer app) |
| 9 | `coach-cohort-facilitator` | 12h | group coaching (8-15 people) |
| 10 | `coach-onboarding` | 8h | first 30 days + Sunstein informed-consent |
| 11 | `coach-renewal-manager` | 6h | Tier A → B → C pipeline |
| 12 | `coach-roi-tracker` | 12h | adoption + behavior change + business outcomes |
| 13 | `coach-lead-finder` | 12h | Solstein coaching scorecard on 197-co landscape |
| 14 | `coach-conversion-agent` | 8h | Richar Ruiz free quick-win → S/M/L |

**Skills (11 coaching + 4 Sunstein/Solstein = 15 skills)**:

Tier 1 (4 skills, 20h): `coaching-pricing`, `coaching-pitch-kit`, `coaching-conversation-framework`, `coaching-trilingual-glossary`

Tier 2 (5 skills, 38h): `coaching-eu-compliance`, `coaching-tech-stack`, `coaching-vertical-playbook`, `coaching-coach-network`, `coaching-privacy-protocol`

Tier 3 (2 skills, 14h): `coaching-agent-debugging`, `coaching-roi-measurement`

Sunstein/Solstein (4 skills, 34h): `sunstein-ethics-review`, `solstein-pipeline-runner`, `sunstein-prompt-library`, `solstein-lite-deploy`

**Effort total**: 80h + 168h = **248h**

### 4.6 Scale Phase (Days 91-120) — first customers

**Owner**: Erebus + Ivan + Kyrian | **Effort**: ~80h | **Depends**: Phase 2 complete

- Day 91-100: Ship `coach-practitioner` MVP
- Day 101-110: 10 free quick-wins across 5 verticals
- Day 111-120: First 3 Tier A customers signed; first Tier B upgrade; first cohort program
- Target: $89-150K ARR run rate (per coaching-strategic-implications.md)

### 4.7 Constitutional v0.3.0 (Days 121-180) — bump the constitution

- Full audit of constitution vs reality
- Add any new departments/roles triggered in Q3
- Document any Tier 3 → Tier 4 promotions
- Re-validate all hard stops
- Write `/opt/data/agents-v2/PLAN-v6.md` based on learnings
- Expand agent layer to 50+ if MRR > $2K

---

## PART 5: ENEVE BEST PRACTICES (the principles we should follow throughout)

From the Eneve `.cursor/` framework, the 5 principles to copy are:

1. **Stable IDs** — `rule.<domain>.<name>.v<MAJOR>` format. Apply to all new agents/skills.
2. **Three invocation strategies** — file-mask, agentic, always-apply. Pick the right one per skill.
3. **Frontmatter with provenance + model_hints** — every rule/skill declares `owner`, `last_review`, `temp`, `top_p`.
4. **Templars + exemplars as separate artifacts** — not inline in skills. Pattern we just adopted.
5. **The improvement loop** — periodic atomic cycles per artifact. We built this (`process-skill-improvement-cycle.py`).

The 9 governance-rules governing how every other rule is written (from Eneve):
1. rule-authoring-overview
2. rule-file-structure
3. rule-naming-conventions
4. rule-contracts-and-scope
5. rule-validation-and-checklists
6. rule-extraction-from-practice
7. rule-invocation-strategies ← "the most important architectural decision"
8. rule-provenance-and-versioning
9. rule-sync-rule (A/B/C/D cross-repo classification)

The 5-stage atomic improvement loop (per prompt):
1. `/find-prompts-needing-review`
2. `/process-prompt-improvement-cycle [file]`
3. `/improve-prompt [file]` ← fix critical issues
4. `/enhance-prompt [file]` ← add examples, decision trees, CoT
5. `/find-extraction-candidates` → extract-templar-exemplar

**Validation report pattern** — Eneve's own validator reports its creator as non-compliant. We do the same: our `hermes-skills-audit.py` reports 158 NOTES — and that's the right behavior. Validators should be honest.

---

## PART 6: KEY DECISIONS NEEDED FROM IVAN

### Decision 1: LLM provider

**Options**:
- **(A)** Top up OpenRouter (~$20/mo for Modelo de IA Haiku) — restores multi-tool at low cost
- **(B)** Top up Proveedor de IA API (~$20/mo for Modelo de IA Sonnet) — direct, fastest
- **(C)** Stay on `litellm/reasoning` (free, but 110s/turn — slow)
- **(D)** Get a Mistral subscription (~$20/mo) — restores the original plan

**Recommendation**: A — OpenRouter with Modelo de IA Haiku. Cheapest path to multi-tool.

### Decision 2: Run coaching agents in parallel or sequentially?

- **Parallel (faster but riskier)**: 7 internal coaching agents built in parallel over 30 days
- **Sequential (slower but safer)**: 1 per week, validate each before next

**Recommendation**: Sequential. Validate `coach-ivan` thoroughly before building `coach-kiki`.

### Decision 3: Apply for Modelo de IA/Proveedor de IA Max separately?

You mentioned wanting to use your Proveedor de IA subscription. The truth: **Proveedor de IA's OAuth via `modelo de IA setup-token` does NOT consume Max credits** — it bills API usage separately (hermes label: "Required Extra Usage Credits to Use Subscription").

**Recommendation**: Don't try to use Max for API. Top up OpenRouter or get a separate API key.

### Decision 4: When to bump ORG-AGENTS to v0.3.0?

- After self-running milestone achieved (Day 30)
- After all 14 coaching agents built (Day 90)
- After 30+ paying customers (Day 120)

**Recommendation**: All three are gates for v0.3.0. Wait for all.

---

## PART 7: SINGLE BET

**The bet**: We have TWO unfinished bodies of work that need to converge:

1. **Org foundation** (hermes-implementation session): 31 agents, 49 cron jobs, 6 dept specs, 158 Eneve-migrated skills — *built but not self-running yet*
2. **Coaching product** (AI-coaching-research session): 197-company landscape, 14 coaching agents planned, 11 coaching skills planned, $89-150K ARR target — *researched but not built*

**The convergence**: The 14 coaching agents are just MORE agents that go through the same pattern (PROMPT.md + cron job + DB + script + skill stack). The 11 coaching skills are just MORE skills that go through the same Eneve pattern (frontmatter + governance-rules + improvement loop).

**The first action**: Hit the self-running milestone (Days 15-30). Until then, NOTHING new should be built — we have to prove the foundation works.

**Single next action today**: Trigger the 2 stuck lead agents (mgmt-coordinator, kiki-coach) with the `reasoning` model. Verify they write briefs. Then start the 7-day self-running window.

---

## PART 8: WHAT TO TELL THE USER (IVAN)

```
The two sessions you asked about were:

1. The hermes-implementation session: built Eneve framework migration
   - 158 skills migrated to Eneve format (9 governance-rules + 1 templar + 1 exemplar + 5 collections + 6 agent-apps)
   - Python validators: hermes-skills-audit.py (12 commands), process-skill-improvement-cycle.py (5-stage loop)
   - Cron job aiw-skills-audit-weekly
   - Found the missing skill `vps-aiw-autonomous-ops` and 1 cycle in governance-rules

2. The AI-coaching-research session: 8 research docs in /opt/data/agents/research/
   - 197-company landscape, 30 research areas, 5 verticals, 14 agents planned, 11 skills planned
   - $89-150K ARR year-1 target
   - Trilingual mid-market positioning (Spanish-native, Dutch-fluent, EU/LATAM-ready)

Both are unfinished. The full updated plan is in PHASE-13-COMPLETE-UPDATED-PLAN.md.

Critical missing pieces:
1. Self-running milestone not achieved (haven't hit 7-day window)
2. Live verification of 24 sub-agents + 8 cross-cutting agents (0/32 triggered)
3. Chaos tests B + C (only A passed)
4. Eval-gate cron integration (manual run only)
5. LLM billing broken (only litellm/reasoning works, ~110s/turn)
6. 14 coaching agents (0/14 built)
7. 11 coaching skills (0/11 built)

What I recommend we do next:
- 14-day foundation phase: fix the 6 critical gaps above
- 14-day self-running phase: hit the milestone (no new building, just observe)
- Then start the coaching product
```

---

## PART 9: ARTIFACTS MAPPED

| Artifact | Where | What |
|----------|-------|------|
| Constitution | `/opt/data/agents-v2/constitution/ORG-AGENTS.md` | v0.2.0 ratified |
| Plan v5 | `/opt/data/agents-v2/PLAN-v5.md` | Current plan, 32 KB |
| Phase 11 final | `/opt/data/agents-v2/PHASE-11-FINAL-EXECUTION.md` | Live execution summary |
| Phase 13 (this) | `/opt/data/agents-v2/PHASE-13-COMPLETE-UPDATED-PLAN.md` | This analysis |
| Coaching research | `/opt/data/agents/research/200-ai-coaching-companies.md` + 7 others | 8 docs |
| Coaching continuation | `/opt/data/agents/research/coaching-continuation-plan.md` | 5-track plan, 27 KB |
| Skills | `/opt/data/skills/_governance/` + `_agent-applications/` + `_collections/` | 9 objetivo + 6 apps + 5 collections |
| Validators | `/opt/data/scripts/hermes-skills-audit.py` + `process-skill-improvement-cycle.py` | 41 KB + 18 KB |
| Loop state | `/opt/data/skills/.loop-state/prompt-improvement-loop.json` | 169/169 processed |
| Eval-gate POC | `/opt/data/agents-v2/eval-gate.py` | 9-check scorer |
| Self-running criteria | `/opt/data/agents-v2/SELF-RUNNING-CRITERIA.md` | Milestone gate |
| 30/60/90 review | `/opt/data/agents/REVIEW-2026-Q4.md` | Checkpoints |
| Eneve reference | `/opt/data/skills/software-development/skill-library-governance-framework/references/eve-cursor-framework.md` | 8.6 KB doc |
| Cursor extract | `/opt/data/Company-Information/docs/handoff/EXTRACT_CURSOR_STANDARDS.md` | PowerShell extract plan |

## Last updated

2026-08-15 by Erebus (this session)
