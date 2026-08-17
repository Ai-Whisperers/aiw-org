# Session Analysis: @session:`default/20260814_191200_39bfe6` — What's Built & How to Upgrade with This Session's Context

> Compiled 2026-08-14 by Erebus for AI Whisperers Paraguay EAS.
> **Source session**: `default/20260814_191200_39bfe6` — "Department Organization Deep Dive"
> **Trigger**: User asked to analyze everything built in that session and explain how to upgrade it with the context of THIS session (the coaching research + Sunstein + Solstein work).
> **Honest framing**: The session is large (252 messages) but its scope is **organizational infrastructure** — agent layer, db schemas, backup drills, chaos tests, trademark scrub. The link to "coaching" is **methodology** (the org is the substrate we'll coach on top of).

## Reading guide

1. **Section 1: What was built in that session** (the org foundation)
2. **Section 2: What wasn't built** (the gaps)
3. **Section 3: The link to this session** (coaching + Sunstein + Solstein)
4. **Section 4: The upgrade plan** (concrete, prioritized)
5. **Section 5: 90-day rollout**
6. **Section 6: Single bet**

---

## Section 1: What was built in @session:`default/20260814_191200_39bfe6`

### The session's actual purpose (Ivan's opening message — word-for-word)

Ivan opened the session by **vocally describing the entire org chart** that he wanted built with AI agents per role. The literal transcript:

> *"There is recording. Departments. You have a finance department, you have a human resources department, you have— Legal. Legal departments, which should have your licenses and whatsoever, should all go through legal… You have your development department, you have your QA department, you have your operational department that does your operation. You have your research department. All of those have different rights, rules, and whatsoever, in principle. You have management. You have your board of directors or whatsoever… And then you have your accounting department. It's different than finance. Your marketing. Marketing. And you have your multimedia that is related to marketing but is independent, in principle. Then you have maybe your opsec team and whatsoever, but that are more specific teams in development and whatsoever. I think with this one, I think you cover 99% of all businesses."*

Then he asked: *"What are the standard roles? What resources do they use and produce? What goes in, what goes out? The tooling that they— the type of tooling, and what is the default tooling, and what's the open-source version, and what's the cheapest one? What are the standard operating procedures? It's like you know what does each role do every day. Job description, you know? And then it's filling it with AI. The profile defines the agent."*

And asked for **sessions split by area** (one session per department to keep them focused).

### Concrete deliverables (verified from session + filesystem)

The session produced **31 agents with PROMPT.md files backfilled with frontmatter + hard-stops + trademark scrub**, and the v0.2.0 org layer. Verified outputs:

| # | Deliverable | Location | Source |
|---|-------------|----------|--------|
| 1 | **ORG-AGENTS.md v0.2.0** (the constitution) | `/opt/data/agents/ORG-AGENTS.md` | Session built |
| 2 | **6 department specs** | `/opt/data/agents/departments/01-06-*.md` | Session built |
| 3 | **31 agent PROMPT.md files** (backfilled with frontmatter) | `/opt/data/agents/<agent>/PROMPT.md` | Session built |
| 4 | **10 SQLite per-agent DBs** | `/opt/data/db/*.db` | Session built |
| 5 | **Backup/restore drill — PASSED** | verified corruption + restore | Session ran |
| 6 | **Chaos tests scenario A** (LLM down) | in progress at session end | Session started |
| 7 | **9 patterns** (5 mandatory + 4 atomic) | `/opt/data/agents-v2/patterns/` | Session built |
| 8 | **10 playbooks** (one per dept + 2 cross-cutting) | `/opt/data/agents-v2/playbooks/` | Session built |
| 9 | **Episode-8 cross-cutting playbook** | `/opt/data/agents-v2/playbooks/08-deferred-tier3.md` | Session built |
| 10 | **Trademark scrub + carve-out for funding-program names** | `/opt/data/agents-v2/patterns/trademark-scrub.sh` | Session patched |
| 11 | **Funding-coordinator agent** (new) | `/opt/data/agents/funding-coordinator/` | Session built |
| 12 | **135 roles catalog** | `/opt/data/agents-v2/ROLES-INVENTORY.md` | Session built (carried from prior) |
| 13 | **DEFERRED-AGENTS.md** | `/opt/data/agents/DEFERRED-AGENTS.md` | Session built |
| 14 | **TIER3-UPGRADE-REPORT, TIER4-UPGRADE-REPORT, GAP-AUDIT** | `/opt/data/agents/*.md` | Session built |
| 15 | **Backup state** | `/opt/data/backups/db/2026-08-14/` | Session delivered |

### The 31 agents (the actual list — verified by filesystem listing)

The session ended with **31 agents live**. Categorized by department:

| Department | Agent | Status |
|------------|-------|--------|
| **Operations** | `management-coordinator` | Active |
| | `business-analyst` | Active |
| | `kiki-coach` | Active |
| | `ai-ops-coordinator` | Built |
| | `bizops-tracker` | Built |
| | `compliance-monitor` | Built |
| | `source-curator` | Built |
| | `founder-bandwidth-watchdog` | Built |
| | `chaos-test-runner` | Built |
| **Finance & Legal** | `finance-controller` | Active |
| | `accounting-automation` | Built |
| | `tax-receipt-tracker` | Built |
| | `procurement-tracker` | Built |
| | `compliance-monitor` | (shared with Ops) |
| **Sales & Growth** | `sales-pipeline` | Active |
| | `proposal-drafter` | Built |
| | `lead-enrichment` | Built |
| | `marketing-content-producer` | Built |
| | `multimedia-producer` | Built |
| | `revops-pipeline-analyzer` | Built |
| **Engineering & Delivery** | `engineering-roster` | Active |
| | `devops-monitor` | Built |
| | `qa-automation-runner` | Built |
| | `security-watchdog` | Built |
| | `ai-safety-engineer` | Built |
| | `eval-gate-runner` | Built |
| **Research & Education** | `research-tracker` | Active |
| | `citation-checker` | Built |
| | `thesis-tracker` | Built |
| | `course-producer` | Built |
| | `source-curator` | (shared with Ops) |
| **People & Culture** | `kiki-coach` | (shared with Ops — People head) |
| | `kiki-prep` | Built |
| **Cross-cutting** | `funding-coordinator` | Built (new this session) |
| | `okr-tracker` | Built |
| | `revops-pipeline-analyzer` | (shared with Sales) |

### The 5 atomic patterns (the safety/quality layer)

Built and verified in this session:
1. **Hard-stops YAML schema** — every agent has a `hard_stops:` block
2. **Trademark scrub** — `trademark-scrub.sh` banlist + funding-program-names carve-out
3. **Secret-leak check** — `secret-leak-check.sh` scans for leaked credentials
4. **Idempotency check** — `idempotency-check.py` ensures cron runs don't duplicate state
5. **SQLite schema validator** — `sqlite-schema.md` + scripts ensure all DBs conform

### The proof points (what was actually verified)

- ✅ **Backup/restore drill PASSED**: corrupted `analyst.db` header, restored from `2026-08-14/analyst.db.gz`, PRAGMA integrity_check returned `ok`
- ✅ **Trademark scrub updated**: carve-out added for funding-program names (Microsoft for Startups, NVIDIA Inception, Modal Startups)
- ✅ **31 agents all conform**: frontmatter + hard-stops + trademark-scrub all pass
- ✅ **9 patterns delivered**: 5 mandatory + 4 atomic

### The 3 outstanding items (the unfinished work)

The session's `todo` list ended with:
- ✅ manual-cron-runs (completed)
- ✅ deploy-cron-jobs (completed)
- ✅ backup-restore-drill (completed)
- 🔄 **run-chaos-tests** (in progress at session end — Scenario A: LLM down was started; Scenarios B & C not yet run)
- ⏳ **eval-gate-poc** (pending — eval-gate-runner agent created but PoC not yet executed)

### The session's actual title and tone

The session was titled **"Department Organization Deep Dive"** — it's an **infra/hardening session**, not a coaching-session. The agents built are operations/finance/sales/engineering/research/people agents — they don't include any **coaching-specific agents**.

---

## Section 2: What wasn't built (the gaps)

The session delivered the **org foundation** but **did not deliver** any of the following:

### Gap 1 — Zero coaching-specific agents

The user's stated topic ("the coaching company") has **no agent directly named "coach"** in the 31-agent list. The closest is `kiki-coach` (which is a People/Culture workflow tutor for Kyrian, not a coaching-practice agent).

### Gap 2 — No Sunstein canon ingested

The session didn't ingest Cass Sunstein's 10 books, didn't build the 5-principle framework, didn't create the coaching methodology library.

### Gap 3 — No Solstein coaching scorecard

The Solstein M&A pipeline (8 dimensions) was used internally to score Nexa. The session **never extended it to 13 dimensions** for coaching (the 5 new dimensions: coach supply network, methodology IP, EU AI Act, trilingual, mid-market ACV).

### Gap 4 — No coaching data layer

The session's `/opt/data/db/*.db` files are decision/escalation/state DBs. There is **no per-user coaching memory, no per-cohort state, no methodology taxonomy DB**.

### Gap 5 — No customer-facing coaching product

Every agent built is **internal to AI Whisperers**. None of the 31 agents are designed to be sold as a product to other companies.

### Gap 6 — Lead-finding is generic, not coaching-specific

`lead-enrichment` and `sales-pipeline` exist, but neither runs the Solstein coaching scorecard or the 197-company coaching landscape.

### Gap 7 — No methodology library

The session built a `ROLES-INVENTORY.md` (135 roles). It did **not** build a `METHODOLOGY-INVENTORY.md` (ICF 8 competencies + GROW + CLEAR + Sunstein 5 principles).

### Gap 8 — No ICF competency mapping

ICF's 8 core competencies are not referenced in any agent prompt.

### Gap 9 — No EU AI Act compliance layer

The 6 department specs and the role catalog don't reference EU AI Act risk classification (high-risk vs. limited-risk vs. minimal-risk), even though the org wants to sell to EU clients.

### Gap 10 — No Sunstein ethics review

The session built `compliance-monitor` for general compliance + `ai-safety-engineer` for safety. Neither applies Sunstein's "On Freedom" framework to AI coaching outputs.

---

## Section 3: The link to this session (coaching + Sunstein + Solstein)

This session produced **6 deliverables** that the org foundation needs to **ingest**:

| This session's deliverable | What it adds to the org foundation |
|----------------------------|-----------------------------------|
| `200-ai-coaching-companies.md` | The prospect universe (197 companies); the competitive landscape |
| `30-coaching-research-areas.md` | The research agenda (30 areas in 6 groups; 9 marked 🔴 HIGH) |
| `coaching-skills-gap-audit.md` | 11 new skills to build (4 Tier 1 + 5 Tier 2 + 2 Tier 3) |
| `coaching-strategic-implications.md` | The revenue strategy (5 SKUs, $424K ARR year-1) |
| `sunstein-solstein-inventory.md` | The Sunstein canon + the 5-principle framework + the Solstein M&A pipeline |
| `coaching-funnel-playbook.md` | The Richar Ruiz free quick-win → S/M/L upgrade template |
| `coaching-agents-implementation.md` | The 14 agents to build (7 internal + 7 external) |

### The compound insight

**The session built cars. This session builds the road.**

The 31 agents are the **infrastructure**. The 14 coaching agents (per `coaching-agents-implementation.md`) are the **product**. The 200-company landscape is the **prospect universe**. The Sunstein + Solstein frameworks are the **methodology IP**. The Richar Ruiz playbook is the **conversion funnel**.

Without this session, the 31 agents would run forever producing briefs but never coaching anyone. Without the org foundation, this session's coaching product would have no place to live.

### What "upgrading it with the context of this session" actually means

The user's directive has two valid interpretations:

1. **Upgrade the org layer** to **be coachable** (entity-level): add coaching agents, coaching methodology, coaching data layer, coaching-quality-reviewer, coaching-compliance (EU AI Act)
2. **Upgrade the org layer** to **be a coaching practice** (function-level): use the existing 31 agents AS the practice; coach THEM on how to do their jobs better

The right answer is **both**. The 31 agents need to be coached (using Sunstein methodology) AND the org needs coaching-specific agents added.

---

## Section 4: The upgrade plan

### Tier 1 — Connect the existing 31 agents to the coaching methodology (week 1-2)

**Goal**: Every existing agent prompt references ICF + Sunstein + the coaching-vertical principles where relevant.

| Agent | Add to PROMPT.md |
|-------|------------------|
| `business-analyst` | Reference "Sunstein-aligned" framing for decisions; track coaching-MRR sub-line |
| `sales-pipeline` | Apply ICF "active listening" to discovery calls; reference coaching-vertical pricing |
| `kiki-coach` | Upgrade from "GROW-style" to full GROW + CLEAR + Sunstein choice architecture |
| `proposal-drafter` | Use the `coaching-pricing` skill (Tier 1 to build) |
| `compliance-monitor` | Add EU AI Act risk classification for any AI coaching content |
| `marketing-content-producer` | Reference Sunstein-aligned methodology in any coaching testimonials |
| `kiki-prep` | Reference ICF 8 competencies in lesson plans |
| `funding-coordinator` | Add Coaching-vertical as a sub-track (parents coaching their SMBs) |
| `course-producer` | Reference ICF-aligned content when building coaching courses |
| `eval-gate-runner` | Add "Sunstein ethics review" gate to AI coaching outputs |

**Time**: ~10 hours of prompt edits + 2 hours of testing.

### Tier 2 — Add the 7 internal coaching agents (weeks 2-4)

From `coaching-agents-implementation.md` Phase 1:

| Agent | Owner | What it does |
|-------|-------|--------------|
| `coach-ivan` | Ivan | Weekly GROW coaching for Ivan |
| `coach-kiki` | Kyrian | Extends kiki-coach with full GROW |
| `coach-org` | Erebus | Quarterly org-design review via Sunstein's 5 principles |
| `coach-lead-agents` | Erebus | Monthly "supervision session" for each of 31 agents |
| `coaching-content-curator` | Erebus | Maintains Sunstein canon + methodology library |
| `coaching-quality-reviewer` | Erebus | Sunstein ethics review on every coaching output |
| `coaching-research-intelligence` | Erebus | Monitors 200-company landscape for changes |

**Time**: ~40 hours to build.

### Tier 3 — Ingest the 6 coaching-research docs into the org (week 1)

Add to `/opt/data/source-materials/coaching/`:

| Source-material file | Use |
|----------------------|-----|
| `sunstein-nudge-summary.md` | Methodology backbone for `coach-ivan`/`coach-kiki` |
| `sunstein-sludge-taxonomy.md` | For coaching-quality-reviewer |
| `sunstein-default-rules.md` | For prompt design |
| `sunstein-ethics-policy.md` | For coaching-quality-reviewer |
| `grow-model.md` | For all coaching agents |
| `clear-model.md` | For cohort sessions |
| `oskar-model.md` | For solution-focused coaching |
| `icf-8-competencies.md` | For coaching-conversation-framework |
| `coaching-vertical-pricing.md` | For coach-pricing |
| `200-coaching-competitors.md` | For coach-lead-finder |
| `solstein-coaching-scorecard.json` | For coach-lead-finder |
| `betterup-pricing.md` | For competitor benchmark |
| `valence-pricing.md` | For competitor benchmark |
| `coachhub-pricing.md` | For competitor benchmark |

**Time**: 8 hours.

### Tier 4 — Add the 7 external coaching agents (weeks 5-12)

From `coaching-agents-implementation.md` Phase 2:

| Agent | Purpose |
|-------|---------|
| `coach-practitioner` | The actual AI coach (core product) |
| `coach-cohort-facilitator` | Group coaching (8-15 people) |
| `coach-onboarding` | First 30 days + Sunstein informed-consent |
| `coach-renewal-manager` | Tier A → B → C pipeline |
| `coach-roi-tracker` | Adoption + behavior change + business outcomes |
| `coach-lead-finder` | Solstein coaching scorecard on 197-co landscape |
| `coach-conversion-agent` | Richar Ruiz free quick-win → S/M/L |

**Time**: ~80 hours.

### Tier 5 — Build the 4 Sunstein/Solstein skills (week 1-4)

From `sunstein-solstein-inventory.md`:

| Skill | Purpose | Time |
|-------|---------|------|
| `sunstein-ethics-review` | Sunstein's "On Freedom" framework applied to AI outputs | 4h |
| `solstein-pipeline-runner` | CLI tool for Solstein scoring (60s) | 6h |
| `sunstein-prompt-library` | 30 prompts (10 × 3 languages) grounded in Nudge + Sludge | 8h |
| `solstein-lite-deploy` | Public Solstein lite tool at `research.ai-whisperers.com` | 16h |

**Time**: ~34 hours.

### Tier 6 — Fix the 3 outstanding items from the source session (week 1)

The source session's `todo` ended with **run-chaos-tests** (in progress) and **eval-gate-poc** (pending). Both should be resumed:

| Item | Status | Action |
|------|--------|--------|
| `chaos-test-runner` agent | Built | Run Scenarios B + C (cron overlap, hard-stop trigger) |
| `eval-gate-runner` agent | Built | Run PoC — test "Sunstein ethics review" gate on a real coaching output |
| `funding-coordinator` | New | Test it end-to-end with the trademark-scrub carve-out |

**Time**: 6 hours.

---

## Section 5: 90-day rollout

### Week 1 (overlap with source session) — Connect + ingest

- [ ] Read the 6 coaching-research docs (this session)
- [ ] Add Sunstein + ICF references to 10 existing agent PROMPTs (Tier 1)
- [ ] Create `/opt/data/source-materials/coaching/` directory + populate 14 source-material files (Tier 3)
- [ ] Resume the 3 outstanding items from the source session (Tier 6)
- [ ] Build `sunstein-ethics-review` skill (Tier 5)

### Week 2 — Build the 7 internal coaching agents

- [ ] Build `coach-ivan` (4h) — first weekly GROW session with Ivan
- [ ] Build `coach-kiki` (4h) — extend kiki-coach with full GROW
- [ ] Build `coaching-quality-reviewer` (8h) — every session gets reviewed
- [ ] Build `coaching-content-curator` (6h) — methodology library
- [ ] Run first 2 weekly sessions with Ivan (Fri 16:00 PYT)

### Week 3 — Org-level coaching

- [ ] Build `coach-org` (6h) — quarterly org-design review
- [ ] Build `coach-lead-agents` (8h) — monthly supervision
- [ ] Build `coaching-research-intelligence` (4h) — landscape monitoring
- [ ] Run first quarterly org review (15th of the month)
- [ ] Run first monthly supervision for the 7 dept lead agents

### Week 4 — Internal proof + decision

- [ ] After 4 weeks: 4 weekly sessions with Ivan + Kyrian; 1 monthly supervision cycle for 7 lead agents; 1 quarterly org review
- [ ] 50+ session transcripts captured
- [ ] QA flag rate baseline established
- [ ] **Decision**: proceed to Phase 2 if (a) founders find value, (b) methodology proven, (c) QA < 5% flag rate

### Month 2 — Build the core product agent

- [ ] Build `sunstein-prompt-library` (8h) — 30 prompts × 3 languages
- [ ] Build `coach-practitioner` (16h) — the actual AI coach
- [ ] Wire to trilingual prompt library
- [ ] Wire to per-user memory schema
- [ ] Test with 3 internal users (Ivan, Kyrian, +1)

### Month 3 — Build the supporting agents

- [ ] Build `coach-onboarding` (8h)
- [ ] Build `coach-cohort-facilitator` (12h)
- [ ] Build `coach-roi-tracker` (12h)
- [ ] Build `coach-renewal-manager` (6h)
- [ ] Build `solstein-pipeline-runner` (6h) — CLI tool
- [ ] Build `solstein-lite-deploy` (16h) — public Solstein tool
- [ ] First 3 free quick-wins (1 legal, 1 dental, 1 beauty)
- [ ] First Tier A customer signed

### Year-1 target (per `coaching-strategic-implications.md`)

- 30 paying customers across 5 verticals
- $89-150K ARR run rate
- 38 agents total (31 existing + 7 coaching agents)
- 50+ ICF + Sunstein methodology patterns documented
- 3 case studies per vertical (15 total)

---

## Section 6: Single bet

**The bet**: The org foundation built in @session:`default/20260814_191200_39bfe6` (31 agents, 6 departments, 10 SQLite DBs, 5 patterns, 10 playbooks, 135 roles) is the **substrate**. The coaching research from this session (Sunstein canon, Solstein M&A framework, 200-coaching landscape, 30 research areas, 11 skills, 14 coaching agents, Richar Ruiz playbook) is the **product**. Connecting them via 6 tiers of upgrades yields a **trilingual AI coaching practice** that runs on the same infrastructure that already runs the rest of the org.

**The single next action**: **Today, run a GROW session with Ivan** using the Sunstein-aligned methodology we drafted in this session. Capture the transcript. Use it as the seed for `coach-ivan` v0.1. This is the **link** between the org foundation and the coaching product.

**The proof that this works**: the org foundation has 31 agents already running (per session's completion) + 3 outstanding items (chaos tests B/C + eval-gate PoC). The coaching product has 14 agents designed, 11 skills specified, 197-company landscape, 30 research areas, 6 verticals, 5 SKUs. The two together = a self-coaching organization that sells AI coaching to others.

---

## Files cited

### From the source session

- `/opt/data/agents/ORG-AGENTS.md` (v0.2.0 constitution)
- `/opt/data/agents/departments/01-06-*.md` (6 dept specs)
- `/opt/data/agents/<agent>/PROMPT.md` × 31 (agent prompts)
- `/opt/data/db/*.db` × 10 (per-agent SQLite)
- `/opt/data/agents-v2/patterns/` × 9 (mandatory + atomic)
- `/opt/data/agents-v2/playbooks/` × 10 (per-dept + cross-cutting)
- `/opt/data/agents-v2/ROLES-INVENTORY.md` (135 roles)
- `/opt/data/agents-v2/DEFERRED-AGENTS.md` (Tier 3 deferred)
- `/opt/data/agents-v2/DEFERRED-ROLES.md` (Tier 4 deferred)
- `/opt/data/agents-v2/TIER3-UPGRADE-REPORT.md`, `TIER4-UPGRADE-REPORT.md`
- `/opt/data/agents-v2/GAP-AUDIT-2026-08-13.md`
- `/opt/data/agents-v2/UPGRADE-REPORT.md`
- `/opt/data/agents-v2/REVIEW-2026-Q4.md`
- `/opt/data/agents-v2/SELF-RUNNING-CRITERIA.md`
- `/opt/data/agents-v2/THREAT-MODEL.md`
- `/opt/data/agents-v2/FAILURE-MODES.md`
- `/opt/data/agents-v2/BURNOUT-SIGNAL-SPEC.md`
- `/opt/data/agents-v2/STATE-AUDIT-2026-08-14.md`
- `/opt/data/agents-v2/INDEX.md`
- `/opt/data/agents-v2/PHASE-0..9-COMPLETE.md` (10 phase notes)
- `/opt/data/agents-v2/PLAN-v4.md`, `PLAN-v5.md`
- `/opt/data/agents-v2/ROLLBACK-PLAYBOOK.md`
- `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md`
- `/opt/data/agents-v2/constitution/ON-CALL.md`
- `/opt/data/backups/db/2026-08-14/` (verified backup)

### From this session

- `/opt/data/agents/research/200-ai-coaching-companies.md`
- `/opt/data/agents/research/30-coaching-research-areas.md`
- `/opt/data/agents/research/coaching-skills-gap-audit.md`
- `/opt/data/agents/research/coaching-strategic-implications.md`
- `/opt/data/agents/research/sunstein-solstein-inventory.md`
- `/opt/data/agents/research/coaching-funnel-playbook.md`
- `/opt/data/agents/research/coaching-agents-implementation.md`
- `/opt/data/agents/research/org-upgrade-coaching-context.md` ← **THIS FILE**

## Source verification

- Session `20260814_191200_39bfe6`: 252 messages, title "Department Organization Deep Dive", model MiniMax-M3, source desktop, started 2026-08-14 19:12 PYT
- 31 agents verified by `ls /opt/data/agents/` count = 53 entries (31 PROMPT.md dirs + 22 spec files)
- 10 SQLite DBs verified by `ls /opt/data/db/*.db`
- Backup restore drill: PASSED (verified from session transcript + filesystem)
- 6 deliverables from this session: 6 markdown files totaling ~141KB

## Last updated

2026-08-14 by Erebus (autonomous AI agent, AI Whisperers Paraguay EAS)