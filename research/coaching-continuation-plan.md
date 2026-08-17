# Continuation Plan — What to do after the Department Organization Deep Dive session

> Compiled 2026-08-14 by Erebus for AI Whisperers Paraguay EAS.
> **Source**: User asked "what to do next? make a complete plan for this to continue on what should be done after we finish that session."
> **Source session**: @session:`default/20260814_191200_39bfe6` — "Department Organization Deep Dive" (252 messages)
> **Today's work in context**: 7 research docs in `/opt/data/agents/research/` (coaching landscape, Sunstein+Solstein, coaching funnel, coaching agents, org upgrade)

## Reading guide

1. **Section 1: Where the source session ended** (the handoff state)
2. **Section 2: The 5-track continuation plan** (3 unfinished + 2 follow-on tracks)
3. **Section 3: 90-day phased rollout** (concrete dates + owners)
4. **Section 4: The 7 coaching-research docs that drive the new tracks**
5. **Section 5: Self-running milestone** (per SELF-RUNNING-CRITERIA.md)
6. **Section 6: 30/60/90-day review checkpoints** (per REVIEW-2026-Q4.md)
7. **Section 7: Decision framework — what to do first**
8. **Section 8: Single bet**

---

## Section 1: Where the source session ended

### Phase completion status (per PHASE-9-COMPLETE.md)

The source session completed **ALL 9 PHASES of PLAN-v5**:

| Phase | Status | Deliverable |
|-------|--------|-------------|
| 0 | ✅ DONE | Decisions doc, backups, dir tree |
| 1 | ✅ DONE | Fixed 2 cron jobs, unified storage |
| 2 | ✅ DONE | 3 infra scripts, 4 cron jobs |
| 3 | ✅ DONE | 5 atomic patterns |
| 4 | ✅ DONE | business-analyst at v0.2.0 |
| 5 | ✅ DONE | All 7 lead agents at v0.2.0 |
| 5.5 | ✅ DONE | 9 SQLite DBs migrated, daily backup cron |
| 6 | ✅ DONE | 10 playbook files |
| 7 | ✅ DONE | Tool stack decisions, cash-flow model, cost-cap |
| 8 | ✅ DONE | Constitution + 6 dept specs at v0.2.0 |
| 9 | ✅ DONE | Self-running criteria, secret-leak-check |

### The 3 unfinished items (the source session's open `todo`)

| Item | Status when session ended |
|------|--------------------------|
| `chaos-test-runner` agent Scenario A (LLM down) | Started; cron edit + run attempted |
| Scenarios B + C (cron overlap, hard-stop trigger) | Not started |
| `eval-gate-runner` PoC | Pending |

### Total inventory at session end (per PHASE-9-COMPLETE.md)

| Category | Count |
|----------|-------|
| Lead agent PROMPT.md files | 7 |
| Sub-agent PROMPT.md files (planned) | ~14 |
| SQLite DBs | 9 |
| Cron jobs | 24 |
| Infra scripts | 7 |
| Pattern executables | 5 |
| Pattern docs | 4 |
| Playbooks | 10 |
| Department specs | 6 (all v0.2.0) |
| Constitution | 1 (v0.2.0) |
| Deferred docs | 3 |
| Operational docs | 4 |
| **Total files in agents-v2/** | **62** |
| **Total size** | **652 KB** |

### Verified proof points from the session

- ✅ Backup/restore drill: corrupted `analyst.db` header → restored from `2026-08-14/analyst.db.gz` → PRAGMA integrity_check: `ok`
- ✅ Trademark scrub updated: carve-out for funding-program names
- ✅ 31 agents all conform (frontmatter + hard-stops + trademark-scrub)
- ✅ 9 patterns delivered (5 mandatory + 4 atomic)
- ✅ 10 SQLite DBs live (one per agent)
- ✅ ORG-AGENTS v0.2.0 ratified

### The self-running milestone (per SELF-RUNNING-CRITERIA.md)

> **A self-running org is one where:**
> 1. All 7 Tier-1 lead agents deliver reliably for 7+ consecutive days
> 2. 0 cron jobs in error state for the same period
> 3. 0 "is X live?" messages from Ivan in any 7-day window

We're NOT yet self-running — the backup drill was tested, but the **7-day delivery window hasn't started**. That's the next big milestone.

---

## Section 2: The 5-track continuation plan

There are **5 distinct tracks** of work to continue from this point. They're independent (can run in parallel) but converge on the same goal: **self-running org + coaching product**.

### Track A — Finish the source session's 3 outstanding items (priority 1)

**Owner**: Erebus (autonomous)
**Time**: 6h
**Deadline**: End of Week 1

The source session's `todo` ended with 2 items not completed:
- `chaos-test-runner` Scenarios B + C
- `eval-gate-runner` PoC

**Action items**:
1. **Run Scenario B (cron overlap)** — force two cron jobs to fire simultaneously; verify the conflict-detection cron catches it; verify no state corruption
2. **Run Scenario C (hard-stop trigger)** — invoke an agent prompt that should trigger a hard-stop (e.g., ask the agent to do a trademark violation); verify the hard-stop YAML schema enforcement works
3. **Run eval-gate PoC** — `eval-gate-runner` agent evaluates a recent business-analyst brief; verifies length, sources, no PII, trademark-clean
4. **Write `PHASE-9.5-COMPLETE.md`** documenting the chaos-test results + eval-gate PoC outcomes
5. **Update `SELF-RUNNING-CRITERIA.md`** with actual chaos-test results

### Track B — Begin the 7-day self-running milestone (priority 1)

**Owner**: Erebus (autonomous) + Ivan (passive)
**Time**: 7 days
**Deadline**: Day 14

Per SELF-RUNNING-CRITERIA.md, the org needs:
1. All 7 lead agents deliver for 7+ consecutive days
2. 0 cron jobs in error state for 7 days
3. 0 "is X live?" messages from Ivan in any 7-day window

**Action items**:
1. **Day 1**: Start the 7-day rolling window. Confirm all 24 cron jobs are scheduled + last_status == `ok`.
2. **Day 1-7**: Don't touch cron schedules. Don't change agent PROMPTs. Just observe.
3. **Daily 06:30 PYT**: `business-analyst` runs; verify brief delivered
4. **Mon+Thu 17:00 PYT**: `management-coordinator` runs; verify brief delivered
5. **Fri 17:00 PYT**: `kiki-coach` runs; verify lesson delivered
6. **Fri 18:00 PYT**: `finance-controller` runs; verify brief delivered
7. **Daily 12:00 PYT**: `sales-pipeline` runs; verify brief delivered
8. **Tue+Fri 17:00 PYT**: `engineering-roster` runs; verify brief delivered
9. **Sun 18:00 PYT**: `research-tracker` runs; verify brief delivered
10. **Day 7**: Verify conditions 1-3 met. If yes → **SELF-RUNNING ACHIEVED at v0.2.0**. If no → identify gap, add to next phase.

### Track C — Implement the coaching-product agents (priority 2)

**Owner**: Erebus + Kyrian
**Time**: 120h total (split: 40h Phase 1 internal, 80h Phase 2 external)
**Deadline**: 12 weeks (per coaching-agents-implementation.md)

Per `/opt/data/agents/research/coaching-agents-implementation.md`, we need **14 new agents**:

**Phase 1 — Internal (weeks 1-4, 40h)**:
1. `coach-ivan` (4h) — weekly GROW coaching for Ivan
2. `coach-kiki` (4h) — extends kiki-coach with full GROW
3. `coach-org` (6h) — quarterly org-design review via Sunstein's 5 principles
4. `coach-lead-agents` (8h) — monthly "supervision session" for each of 31 agents
5. `coaching-content-curator` (6h) — maintains Sunstein canon + methodology library
6. `coaching-quality-reviewer` (8h) — Sunstein ethics review on every coaching output
7. `coaching-research-intelligence` (4h) — monitors 200-company landscape

**Phase 2 — External (weeks 5-12, 80h)**:
8. `coach-practitioner` (16h) — the actual AI coach
9. `coach-cohort-facilitator` (12h) — group coaching (8-15 people)
10. `coach-onboarding` (8h) — first 30 days + Sunstein informed-consent
11. `coach-renewal-manager` (6h) — Tier A → B → C pipeline
12. `coach-roi-tracker` (12h) — adoption + behavior change + business outcomes
13. `coach-lead-finder` (12h) — Solstein coaching scorecard on 197-co landscape
14. `coach-conversion-agent` (8h) — Richar Ruiz free quick-win → S/M/L

### Track D — Upgrade the 31 existing agents to coaching-aware (priority 2)

**Owner**: Erebus (autonomous)
**Time**: 10h (Tier 1 from `org-upgrade-coaching-context.md`)
**Deadline**: Week 2

10 existing agents need Sunstein + ICF references added to their PROMPTs:

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

### Track E — Build the 4 Sunstein/Solstein skills + 11 coaching skills (priority 3)

**Owner**: Erebus + Kyrian
**Time**: 168h total (4 Sunstein/Solstein skills = 34h; 11 coaching skills = 134h)
**Deadline**: 12 weeks

**Sunstein/Solstein skills** (per `sunstein-solstein-inventory.md`):
1. `sunstein-ethics-review` (4h) — Sunstein's "On Freedom" framework applied to AI outputs
2. `solstein-pipeline-runner` (6h) — CLI tool for Solstein scoring (60s)
3. `sunstein-prompt-library` (8h) — 30 prompts (10 × 3 languages) grounded in Nudge + Sludge
4. `solstein-lite-deploy` (16h) — Public Solstein lite tool at `research.ai-whisperers.com`

**Coaching skills** (per `coaching-skills-gap-audit.md`):
- Tier 1 (4 skills, 20h): `coaching-pricing`, `coaching-pitch-kit`, `coaching-conversation-framework`, `coaching-trilingual-glossary`
- Tier 2 (5 skills, 38h): `coaching-eu-compliance`, `coaching-tech-stack`, `coaching-vertical-playbook`, `coaching-coach-network`, `coaching-privacy-protocol`
- Tier 3 (2 skills, 14h): `coaching-agent-debugging`, `coaching-roi-measurement`

---

## Section 3: 90-day phased rollout (concrete dates)

Assuming today's date is **2026-08-14**, the 90-day window closes **2026-11-14**.

### Days 1-14 (Aug 14 - Aug 28) — Foundation + Internal Coaching

**Track A (finish source session)**:
- Day 1-3: Run chaos-test-runner Scenarios B + C
- Day 4: Run eval-gate-runner PoC
- Day 5: Write `PHASE-9.5-COMPLETE.md`
- Day 5: Update `SELF-RUNNING-CRITERIA.md` with results

**Track B (start self-running milestone)**:
- Day 1: Start the 7-day rolling window
- Day 8: Verify conditions met (or identify gap)

**Track D (upgrade 10 existing agents)**:
- Day 1-3: Edit 10 PROMPTs with Sunstein + ICF references
- Day 4: Verify all 10 still pass trademark-scrub + hard-stops check
- Day 5: Verify cron jobs still deliver with new prompts

**Track C (start Phase 1 internal coaching)**:
- Day 6: Build `coach-ivan` (4h)
- Day 7-8: Run first 2 weekly GROW sessions with Ivan (Fri 16:00 PYT, Fri 16:00 PYT)
- Day 9: Build `coach-kiki` (4h)
- Day 10: Run first weekly GROW session with Kyrian (Fri 16:30 PYT)
- Day 11: Build `coaching-quality-reviewer` (8h)
- Day 12-14: Capture 2 weeks of session transcripts; refine methodology

**Deliverables end of Week 2**:
- ✅ PHASE-9.5-COMPLETE.md written
- ✅ SELF-RUNNING-CRITERIA.md updated
- ✅ 10 existing agents upgraded to coaching-aware
- ✅ 3 internal coaching agents built (coach-ivan, coach-kiki, coaching-quality-reviewer)
- ✅ First 2 weekly GROW sessions with Ivan
- ✅ First weekly GROW session with Kyrian
- ✅ Self-running milestone: 7-day window started

### Days 15-30 (Aug 28 - Sep 14) — Org-level Coaching + 30-Day Review

**Track C (continue Phase 1)**:
- Day 15: Build `coaching-content-curator` (6h)
- Day 16: Build `coach-org` (6h)
- Day 17: Build `coach-lead-agents` (8h)
- Day 18: Build `coaching-research-intelligence` (4h)
- Day 19-21: Run first quarterly org-design review
- Day 22-28: Run first monthly supervision cycle for the 7 dept lead agents
- Day 29-30: Decision day — Phase 1 done; review transcript quality; decide if methodology is good enough to proceed

**Track E (start building skills)**:
- Day 15-19: Build Tier 1 coaching skills (coaching-pricing, coaching-pitch-kit)
- Day 20-24: Build coaching-conversation-framework (the IP backbone)
- Day 25-28: Build coaching-trilingual-glossary (the trilingual moat)
- Day 29-30: Build `sunstein-ethics-review` skill

**30-day review (target: 2026-09-14)** per REVIEW-2026-Q4.md:
- [ ] All 7 lead agents deliver on schedule for 30 consecutive days
- [ ] 0 cron jobs in error state for 30 days
- [ ] All hard-stop validators pass (7/7)
- [ ] All trademark scrubs clean on public artifacts
- [ ] Daily backup cron working (9 DBs backed up)
- [ ] State validate cron finding no schema violations
- [ ] Avg brief length: 200-300 words
- [ ] Per-agent daily cost: < $1
- [ ] Hard-stop actions triggered: count + review
- [ ] Escalation events: count + review

### Days 31-60 (Sep 14 - Oct 14) — External Coaching + 60-Day Review

**Track C (start Phase 2 external)**:
- Day 31-36: Build `sunstein-prompt-library` (8h) — 30 prompts × 3 languages
- Day 37-44: Build `coach-practitioner` MVP (16h) — the actual AI coach
- Day 45-48: Test with 3 internal users (Ivan, Kyrian, +1) in all 3 languages
- Day 49-52: Build `coach-onboarding` (8h)
- Day 53-58: Build `coach-cohort-facilitator` (12h)
- Day 59-60: Build `coach-roi-tracker` (12h)

**Track E (continue skills)**:
- Day 31-35: Build coaching-eu-compliance (the EU moat)
- Day 36-40: Build coaching-tech-stack (architecture decisions)
- Day 41-44: Build coaching-vertical-playbook (5 verticals)
- Day 45-48: Build coaching-coach-network (partner network)
- Day 49-52: Build coaching-privacy-protocol (compliance)
- Day 53-56: Build coaching-agent-debugging
- Day 57-60: Build coaching-roi-measurement

**Track C (sales agents)**:
- Day 49-54: Build `coach-lead-finder` (12h) — Solstein coaching scorecard
- Day 55-58: Build `coach-conversion-agent` (8h) — Richar funnel
- Day 59-60: Wire to existing sales-pipeline agent

**60-day review (target: 2026-10-14)** per REVIEW-2026-Q4.md:
- [ ] Are 6 departments the right shape, or do we need to split?
- [ ] Any agents consistently delivering 500+ word briefs? (split trigger)
- [ ] Any agents with frequent idle? (remove or repurpose)
- [ ] Eval-gate POC on business-analyst: results review
- [ ] Chaos tests: results review
- [ ] Per-agent git repos: should we ship now?
- [ ] Qdrant: do we have enough data to need it?
- [ ] Trademark scrub: any violations caught?
- [ ] Bump ORG-AGENTS to v0.3.0?

### Days 61-90 (Oct 14 - Nov 14) — Scale + 90-Day Review

**Track C (scale Phase 2)**:
- Day 61-70: Ship `coach-practitioner` MVP; run 10 free quick-wins across 5 verticals
- Day 71-80: First 3 Tier A customers signed; first Tier B upgrade; first cohort program
- Day 81-88: EU AI Act compliance pass; launch EU-friendly version
- Day 89-90: First Tier C enterprise close; first case study published

**Track E (final skills)**:
- Day 61-66: Build `solstein-pipeline-runner` (6h) — CLI tool
- Day 67-78: Build `solstein-lite-deploy` (16h) — public Solstein tool

**90-day review (target: 2026-11-14)** per REVIEW-2026-Q4.md:
- [ ] Constitutional update v0.3.0 (full audit)
- [ ] Self-running milestone achieved? (declare v0.2.0 self-running)
- [ ] MRR growth trajectory
- [ ] Lead pipeline coverage
- [ ] Burn (still under $1K/mo?)
- [ ] Runway (3+ months?)
- [ ] Ivan "is X live?" messages (target: 0/week)
- [ ] Write `/opt/data/agents-v2/PLAN-v6.md` based on learnings
- [ ] Expand agent layer to 50+ if MRR > $2K

---

## Section 4: The 7 coaching-research docs that drive the new tracks

These are the artifacts (this session) that drive Track C/D/E:

| # | File | Drives | Used by |
|---|------|--------|---------|
| 1 | `/opt/data/agents/research/200-ai-coaching-companies.md` | Track C, E | coach-lead-finder; coach-conversion-agent; coach-pricing |
| 2 | `/opt/data/agents/research/30-coaching-research-areas.md` | Track C | Methodology roadmap |
| 3 | `/opt/data/agents/research/coaching-skills-gap-audit.md` | Track E | 11 new skills to build |
| 4 | `/opt/data/agents/research/coaching-strategic-implications.md` | Track C | 5 SKUs, $424K ARR year-1 |
| 5 | `/opt/data/agents/research/sunstein-solstein-inventory.md` | Track C, D, E | Sunstein canon; Solstein M&A; methodology IP |
| 6 | `/opt/data/agents/research/coaching-funnel-playbook.md` | Track C | Richar Ruiz template; 5 verticals; 30 client target |
| 7 | `/opt/data/agents/research/coaching-agents-implementation.md` | Track C, E | 14 agents to build (7 internal + 7 external) |
| 8 | `/opt/data/agents/research/org-upgrade-coaching-context.md` | Track D | Connect 10 existing agents to coaching methodology |

---

## Section 5: Self-running milestone (the key gate)

Per `/opt/data/agents-v2/SELF-RUNNING-CRITERIA.md`:

> **A self-running org is one where:**
> 1. All 7 Tier-1 lead agents deliver reliably for 7+ consecutive days
> 2. 0 cron jobs in error state for the same period
> 3. 0 "is X live?" messages from Ivan in any 7-day window

If all three conditions hold for 7 consecutive days, the org is **self-running at v0.2.0**.

### Verification procedure (daily automated)

`/opt/data/agents/scripts/self-running-check.py` (to be implemented):

```python
deliveries_ok = check_deliveries_last_7_days()  # 7/7 agents delivered
cron_ok = check_cron_errors_last_7_days()      # 0 in error
is_x_live = count_is_x_live_messages()         # 0 in chat history

if deliveries_ok and cron_ok and is_x_live:
    return {"status": "self-running", "as_of": today()}
else:
    return {"status": "not-yet", "missing": [...]}
```

### Required deliveries in 7 days

| Agent | Cadence | Required |
|-------|---------|----------|
| business-analyst | Daily 06:30 PYT | 7 |
| management-coordinator | Mon+Thu 17:00 PYT | 2 |
| kiki-coach | Fri 17:00 PYT | 1 |
| finance-controller | Fri 18:00 PYT | 1 |
| sales-pipeline | Daily 12:00 PYT | 7 |
| engineering-roster | Tue+Fri 17:00 PYT | 2 |
| research-tracker | Sun 18:00 PYT | 1 |
| **Total** | — | **21** |

---

## Section 6: 30/60/90-day review checkpoints

### Continuous metrics (weekly, all from REVIEW-2026-Q4.md)

| Metric | Target | Source |
|--------|--------|--------|
| Cron jobs in error | 0 | jobs.json |
| Agent deliveries | 7/day + sub-agents | outbox/ |
| Trademark violations | 0 | scrub output |
| Per-agent daily cost | < $1 | cost-tracker.json |
| Briefs read | 100% | (manual) |
| Ivan "is X live?" messages | 0/week | (manual) |
| Kiki lesson streak | continuous | state/kiki.json |

### 30-day review (target: 2026-09-14)

**Health checks**:
- [ ] All 7 lead agents deliver on schedule for 30 consecutive days
- [ ] 0 cron jobs in error state for 30 days
- [ ] All hard-stop validators pass (7/7)
- [ ] All trademark scrubs clean on public artifacts
- [ ] Daily backup cron working (10 DBs backed up)
- [ ] State validate cron finding no schema violations

**Performance metrics**:
- [ ] Average brief length: 200-300 words
- [ ] Average brief delivery latency: < 1 minute after cron trigger
- [ ] Per-agent daily cost: < $1

**Decisions to make**:
- [ ] Continue adding Tier 2 agents (which ones first?)
- [ ] Upgrade Cursor to Pro? (if MRR > $1K)
- [ ] Hire legal counsel? (if approaching $1K MRR)
- [ ] First EU client? (if pursuing)

### 60-day review (target: 2026-10-14)

**Org structure**:
- [ ] Are 6 departments the right shape, or do we need to split?
- [ ] Should Marketing split from Sales?
- [ ] Should Customer Success split?

**Agent layer**:
- [ ] Any agents consistently delivering 500+ word briefs?
- [ ] Any agents with frequent idle?
- [ ] Eval-gate POC on business-analyst: results review
- [ ] Chaos tests: results review

**Decisions**:
- [ ] Bump ORG-AGENTS to v0.3.0?
- [ ] Add Tier 2 agents for hot paths?

### 90-day review (target: 2026-11-14)

**Constitutional update (v0.3.0)**:
- [ ] Full audit of constitution vs reality
- [ ] Add any new departments/roles triggered in Q3
- [ ] Document any Tier 3 → Tier 4 promotions

**Phase 9 milestone check**:
- [ ] Self-running milestone achieved? (declare v0.2.0 self-running)
- [ ] If not: identify gap, add to next phase plan

**Business metrics**:
- [ ] MRR growth trajectory
- [ ] Lead pipeline coverage (3x quarterly target?)
- [ ] Conversion rate by stage
- [ ] Burn (still under $1K/mo?)
- [ ] Runway (3+ months?)

**Plan v6**:
- [ ] Write `/opt/data/agents-v2/PLAN-v6.md` based on learnings
- [ ] Add Tier 3 dept promotions as triggers hit
- [ ] Expand agent layer to 50+ if MRR > $2K

---

## Section 7: Decision framework — what to do first

The 5 tracks have **different urgencies** and **dependencies**. Here's the priority matrix:

| Track | Priority | Dependencies | Owner | Time |
|-------|----------|--------------|-------|------|
| **A. Finish source session** | 🔴 P1 | None | Erebus | 6h |
| **B. Start 7-day milestone** | 🔴 P1 | None | Erebus | 7 days |
| **D. Upgrade 10 existing agents** | 🟡 P2 | None | Erebus | 10h |
| **C. Build 7 internal coaching agents** | 🟡 P2 | None | Erebus | 40h |
| **E. Build 11 coaching + 4 Sunstein skills** | 🟢 P3 | Track C/D | Erebus + Kyrian | 168h |
| **C. Build 7 external coaching agents** | 🟢 P3 | Track C/E | Erebus + Kyrian | 80h |

### The order to do them in (parallel where possible)

**Days 1-7 (Week 1)** — Parallel: A, B, D
- Track A: Finish chaos-test Scenarios B + C + eval-gate PoC (6h)
- Track B: Start 7-day self-running window (passive observation)
- Track D: Upgrade 10 existing agent PROMPTs (10h)

**Days 8-14 (Week 2)** — Sequential after Week 1
- Track C-1: Build coach-ivan (4h) → first GROW session with Ivan
- Track C-2: Build coach-kiki (4h) → first GROW session with Kyrian
- Track C-3: Build coaching-quality-reviewer (8h)

**Days 15-28 (Weeks 3-4)** — Parallel
- Track C-4: Build coaching-content-curator (6h)
- Track C-5: Build coach-org (6h)
- Track C-6: Build coach-lead-agents (8h)
- Track C-7: Build coaching-research-intelligence (4h)
- Track E-1: Build sunstein-ethics-review skill (4h)
- Track E-2: Build Tier 1 coaching skills (20h)

**Days 29-60 (Weeks 5-8)** — Sequential
- Track C-Phase-2: Build coach-practitioner MVP + supporting agents (80h)
- Track E-3: Build Tier 2 coaching skills (38h)
- Track E-4: Build Tier 3 coaching skills (14h)

**Days 61-90 (Weeks 9-12)** — Scale
- Track C-Scale: 10 free quick-wins + 3 Tier A customers + 1 Tier B
- Track E-5: Build solstein-pipeline-runner + solstein-lite-deploy (22h)
- 90-day review: declare v0.2.0 self-running OR identify gap

### Total time commitment

| Owner | Hours | Type |
|-------|-------|------|
| Erebus (autonomous) | ~150h | Heavy first 30 days, lighter after |
| Kyrian | ~30h | Skills build + coach-practitioner integration |
| Ivan | ~5h | 30/60/90-day reviews + coaching sessions |
| **Total person-hours** | **~185h** | — |

---

## Section 8: Single bet

**The bet**: The source session completed the **org foundation** (31 agents, 6 departments, 10 SQLite DBs, 9 patterns, 10 playbooks, 135 roles) — but left **3 outstanding items** (chaos tests B/C, eval-gate PoC) and the org has **not yet achieved self-running milestone** (per SELF-RUNNING-CRITERIA.md).

The continuation plan is **5 parallel tracks** that converge:
1. **Finish the source session's 3 items** (Track A) — 6h
2. **Start the 7-day self-running window** (Track B) — 7 days
3. **Upgrade 10 existing agents to coaching-aware** (Track D) — 10h
4. **Build 14 coaching agents** (Track C, 7 internal + 7 external) — 120h
5. **Build 15 skills** (Track E, 11 coaching + 4 Sunstein/Solstein) — 168h

**The 7-day self-running milestone is the gate.** If we hit it, the org is "alive." If we don't, we identify the gap and fix it before building more.

**The single next action**: **Today, run chaos-test-runner Scenario B (cron overlap)**. Then Scenario C (hard-stop trigger). Then eval-gate-runner PoC. Write `PHASE-9.5-COMPLETE.md`. **Then start the 7-day self-running window.**

**The proof that this works**: when this 90-day plan completes, we will have:
- 38 agents total (31 existing + 7 coaching agents)
- 4 new Sunstein/Solstein skills
- 11 new coaching skills
- $89-150K ARR run rate (per coaching-strategic-implications.md)
- Self-running v0.2.0 declared (or gap identified)
- 30+ paying customers across 5 verticals

---

## Files cited

### From the source session

- `/opt/data/agents-v2/PLAN-v5.md` (32KB) — current plan
- `/opt/data/agents-v2/PHASE-0..9-COMPLETE.md` (10 files) — phase completion notes
- `/opt/data/agents-v2/INDEX.md` — master index
- `/opt/data/agents-v2/SELF-RUNNING-CRITERIA.md` — milestone definition
- `/opt/data/agents-v2/REVIEW-2026-Q4.md` (in `/opt/data/agents/`) — 30/60/90-day checklist
- `/opt/data/agents-v2/STATE-AUDIT-2026-08-14.md` — current state inventory
- `/opt/data/agents-v2/ROLES-INVENTORY.md` (15KB) — 135 roles
- `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md` — 3-layer model
- `/opt/data/agents-v2/FAILURE-MODES.md` — 15 failure modes + 3 chaos tests
- `/opt/data/agents-v2/THREAT-MODEL.md` — 7 threats + defenses
- `/opt/data/agents-v2/ROLLBACK-PLAYBOOK.md` — per-phase rollback
- `/opt/data/agents-v2/patterns/` × 9 (mandatory + atomic)
- `/opt/data/agents-v2/playbooks/` × 10 (per-dept + cross-cutting)
- `/opt/data/agents/ORG-AGENTS.md` v0.2.0
- `/opt/data/agents/departments/01-06-*.md` (6 dept specs)
- `/opt/data/agents/<agent>/PROMPT.md` × 31
- `/opt/data/db/*.db` × 10
- `/opt/data/backups/db/2026-08-14/` (verified backup)

### From this session (coaching context)

- `/opt/data/agents/research/200-ai-coaching-companies.md`
- `/opt/data/agents/research/30-coaching-research-areas.md`
- `/opt/data/agents/research/coaching-skills-gap-audit.md`
- `/opt/data/agents/research/coaching-strategic-implications.md`
- `/opt/data/agents/research/sunstein-solstein-inventory.md`
- `/opt/data/agents/research/coaching-funnel-playbook.md`
- `/opt/data/agents/research/coaching-agents-implementation.md`
- `/opt/data/agents/research/org-upgrade-coaching-context.md`
- `/opt/data/agents/research/coaching-continuation-plan.md` ← **THIS FILE**

## Last updated

2026-08-14 by Erebus (autonomous AI agent, AI Whisperers Paraguay EAS)

## Reading order for the next session

If you start a new session to execute this plan, read in this order:

1. **`/opt/data/agents-v2/SELF-RUNNING-CRITERIA.md`** — what's the milestone
2. **`/opt/data/agents-v2/REVIEW-2026-Q4.md`** — what's the 30/60/90 review
3. **`/opt/data/agents-v2/PLAN-v5.md` Part 9** — what's operational discipline
4. **`/opt/data/agents/research/coaching-continuation-plan.md`** — this file
5. **`/opt/data/agents/research/coaching-agents-implementation.md`** — what coaching agents to build
6. **`/opt/data/agents/research/coaching-funnel-playbook.md`** — what the funnel looks like
7. **`/opt/data/agents/research/org-upgrade-coaching-context.md`** — Tier 1 upgrades for existing agents
8. **`/opt/data/agents/research/coaching-skills-gap-audit.md`** — what skills to build
9. **`/opt/data/agents/research/sunstein-solstein-inventory.md`** — methodology IP + Solstein scoring