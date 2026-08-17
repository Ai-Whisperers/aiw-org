# Coaching Agents — Full Analysis & Implementation Plan

> Compiled 2026-08-14 by Erebus for AI Whisperers Paraguay EAS. The user's brief:
> *"analyze all the agents we should setup for the coaching? for ourself we want to first upgrade AI whisperes fully and then implement it to others and find them with this data"*
>
> **Two-phase mandate**:
> 1. **Phase 1 — Internal first**: Build AI coaching agents that upgrade AI Whisperers itself (Ivan + Kyrian + the 24-cron org)
> 2. **Phase 2 — External**: Same agents become the product; sell to other companies; find them via Solstein scoring
>
> **This doc = (a) what we already have (audit), (b) what we need to build (gap), (c) the phased rollout, (d) the data layer.**

## Reading guide

1. **Section 1: Audit of current agents** — what we already have
2. **Section 2: Gap analysis** — what coaching requires that we don't have
3. **Section 3: The data layer** — what powers the agents (sources, scoring, signals)
4. **Section 4: 14 agents to build** (7 internal + 7 external-productized)
5. **Section 5: Two-phase rollout** — internal first, external second
6. **Section 6: 90-day implementation plan**
7. **Section 7: Risks + single bet**

---

## Section 1: Audit of current agents (what we already have)

### The org layer (built 2026-08-13/14, v0.2.0)

| Layer | Component | Status |
|-------|-----------|--------|
| **Constitution** | `ORG-AGENTS.md` (v0.2.0) | Active, 6 depts + 8 Tier-2 cross-cutting + 12 Tier-3 deferred |
| **Departments** | 6 specs in `/opt/data/agents/departments/` | Active |
| **Lead agents** | 7 (business-analyst, management-coordinator, kiki-coach, sales-pipeline, finance-controller, engineering-roster, research-tracker) | All cron-driven |
| **Sub-agents** | ~14 planned | Most not yet built |
| **Cross-cutting** | 8 (health.sh, snapshots, validation, heartbeat, db-snapshot, etc.) | Active |
| **Cron jobs** | 24 verified | Running |
| **Roles catalog** | ~135 roles in `agents-v2/ROLES-INVENTORY.md` | Defined, not staffed |
| **Storage** | SQLite per-agent + git repos | Phase 5.5 complete |
| **State files** | 13 JSON files in `/opt/data/agents/state/` | Active, rolling caps |
| **Decision rights** | Per-department matrix | Defined, $50/$500/$5K thresholds |

### What's running daily (the operational baseline)

| Cron | Schedule | Owner | What it does |
|------|----------|-------|--------------|
| `morning-brief` | 06:00 PYT daily | Erebus | Infrastructure + sites + infra status |
| `business-analyst` | 06:30 PYT daily | Erebus | Revenue/pipeline/sites snapshot |
| `sales-pipeline` | 09:00 + 16:00 PYT daily | Erebus | Lead triage + outreach drafts |
| `management-coordinator` | Mon/Thu 17:00 PYT | Erebus | Cross-repo stuck/stale/PR review |
| `kiki-coach` | Fri 17:00 PYT | Erebus | Weekly lesson for Kyrian |
| `finance-controller` | Fri 18:00 PYT | Erebus | Cash + contracts + compliance |
| `engineering-roster` | Tue/Fri 17:00 PYT | Erebus | Deploy health + PRs + Kiki workload |
| `research-tracker` | Sun 18:00 PYT | Erebus | Thesis + research backlog |
| `site-health` | Every 15m | watchdog | HTTP checks on live sites |
| `repo-ci-monitor` | Daily 11:00 UTC | watchdog | CI status across repos |
| `rbl-check` | Daily 12:00 UTC | watchdog | R2 bucket listing |
| `thesis-daily-tick` | Daily | Erebus | Thesis progress |
| `thesis-watchdog` | Every 15m | watchdog | Thesis cron health |
| `thesis-weekly-review` | Weekly | Erebus | Thesis summary |
| `thesis-git-maintenance` | Daily | Erebus | Repo hygiene |
| `evo-poll-watchdog` | Every 5m | watchdog | Hermes Evolution polling |
| 8 more | — | — | Heartbeat, snapshot, validation |

### Critical insight: we're already coaching-adjacent

Three existing agents are functionally coaching, just not labeled as such:

1. **kiki-coach** (Fri 17:00) — already runs GROW-style lessons for Kyrian
2. **business-analyst** (Daily 06:30) — already monitors performance → that's coaching-adjacent
3. **management-coordinator** (Mon/Thu 17:00) — already surfaces blockers + recommends next actions

**We have a coaching operating system. We just haven't productized it.**

---

## Section 2: Gap analysis (what coaching requires that we don't have)

### Gap A — Coaching methodology (no IP layer)

| Missing | Why it matters |
|---------|----------------|
| **GROW/CLEAR framework prompts** | The conversation backbone of every AI coaching session |
| **ICF 8 competencies mapping** | Industry-standard methodology for "what a coach does" |
| **Sunstein-aligned prompt library** | Our unique methodology IP (canonical authority) |
| **Behavior change models** | Prochaska + BJ Fogg + Duhigg patterns for nudge design |
| **Trilingual prompt library (es/en/nl)** | Our trilingual edge |

### Gap B — Coaching skills (no skill layer)

From `coaching-skills-gap-audit.md`, **11 skills need to be built**:

- `coaching-pricing`, `coaching-pitch-kit`, `coaching-conversation-framework`, `coaching-trilingual-glossary`
- `coaching-eu-compliance`, `coaching-tech-stack`, `coaching-vertical-playbook`, `coaching-coach-network`, `coaching-privacy-protocol`
- `coaching-agent-debugging`, `coaching-roi-measurement`

### Gap C — Coaching-specific agents (the missing layer)

The org currently has agents for **operations, finance, sales, engineering, research, people** — but **zero agents for coaching**.

| Missing agent | Why |
|---------------|-----|
| **coach-practitioner** | The actual AI coach that runs 1:1 sessions with users |
| **coaching-quality-reviewer** | Reviews every AI coaching output for ethics + quality |
| **coaching-cohort-facilitator** | Runs group coaching cohorts (8-15 people) |
| **coaching-content-curator** | Builds the methodology library + Sunstein canon |
| **coaching-onboarding** | Walks new customers through the first 30 days |
| **coaching-renewal-manager** | Manages upgrades from A → B → C |
| **coaching-research-intelligence** | Monitors 200-company landscape for changes |

### Gap D — Data layer (the engine)

| Missing | Source |
|---------|--------|
| **Per-user coaching memory** | Long-term state of each user's goals, progress, blockers |
| **Per-cohort state** | Cohort-level analytics, completion rates, breakthroughs |
| **Methodology taxonomy** | The 8 ICF competencies + GROW stages + Sunstein principles + Sunstein's 5 categories — all linked |
| **Benchmarks** | Industry baseline data for "what good looks like" |
| **Sunstein canon** | 10+ books of Sunstein scholarship, indexed by principle |
| **Solstein coaching scorecard** | 8-dimension scoring framework for coaching companies (NEW) |

### Gap E — External sales infrastructure

| Missing | Source |
|---------|--------|
| **Lead scoring for coaching prospects** | Solstein coaching scorecard (8 dimensions) |
| **Trilingual discovery scripts** | Spanish + Dutch + English for 30-min discovery calls |
| **Case studies (3 verticals minimum)** | Need legal, dental, RE playbooks as proof |
| **Pricing published externally** | Currently only in `paraguai-proposal-pricing` skill |

### Gap F — Internal application (the user's primary ask)

The user said "first upgrade AI Whisperes fully." We need to:

| Need | What it looks like |
|------|-------------------|
| **Ivan gets an AI coach** | Weekly 30-min GROW session + async daily check-in |
| **Kyrian gets an AI coach** | Weekly 30-min GROW session + methodology lessons (extends kiki-coach) |
| **Both founders coached on the coaching practice itself** | Meta-coaching: "how to be a good coaching practice operator" |
| **The 6 dept lead agents coached** | Each lead agent gets monthly coaching: blockers, priorities, growth |
| **The org layer coached** | Quarterly org-design review with AI coaching methodology |

---

## Section 3: The data layer (what powers the agents)

The agents need a **structured data layer**. Without it, they're just prompts.

### Data layer components

```
/opt/data/agents/coaching/
├── methodology/
│   ├── icf-8-competencies.json          # 8 ICF competencies with AI prompt patterns
│   ├── grow-clear-oskar-models.json     # Coaching conversation models
│   ├── sunstein-5-principles.json       # Choice architecture, defaults, sludge, attention, autonomy
│   ├── bj-fogg-tiny-habits.json         # Behavior change patterns
│   └── behavior-coaching-patterns.json  # Prochaska + Duhigg + Clear
├── prompts/
│   ├── es/                              # Spanish prompt library (90 prompts)
│   ├── en/                              # English prompt library (90 prompts)
│   └── nl/                              # Dutch prompt library (90 prompts)
├── memory/
│   ├── users/{user_id}/                 # Per-user long-term coaching memory
│   │   ├── goals.json
│   │   ├── progress.json
│   │   ├── blockers.json
│   │   └── session-history.jsonl
│   └── cohorts/{cohort_id}/             # Per-cohort analytics
│       ├── attendance.json
│       ├── breakthroughs.json
│       └── completion.json
├── state/
│   ├── users.json                       # Master user list (rolling 90-day window)
│   ├── cohorts.json                     # Active cohorts
│   ├── renewals.json                    # Tier A → B → C pipeline
│   └── qa-flags.json                    # Quality issues to review
├── benchmarks/
│   ├── icf-baselines.json               # What good coaching looks like
│   ├── sunstein-baselines.json          # What good nudging looks like
│   ├── betterup-architecture.md         # Competitor reference (provenance)
│   ├── coachhub-architecture.md
│   └── valence-architecture.md
├── scorecard/
│   └── coaching-solstein-scorecard.json # 8-dimension coaching scoring
└── canon/
    ├── sunstein-nudge-summary.md
    ├── sunstein-sludge-taxonomy.md
    ├── sunstein-default-rules.md
    └── sunstein-ethics-policy.md
```

### Data sources for the Solstein coaching scorecard

For **finding prospects** (Phase 2), the Solstein pipeline extends from 8 to 13 dimensions:

**Original 8 (M&A-focused)**:
1. Ownership attractiveness
2. Revenue scale fit
3. Geographic fit
4. Tech stack modernity
5. Customer lock-in
6. Vertical depth
7. Integration potential
8. Growth trajectory

**New 5 (coaching-focused)**:
9. Coach supply network quality
10. Methodology IP (ICF + Sunstein alignment)
11. EU AI Act compliance
12. Trilingual depth
13. Mid-market ACV fit

### The Sunstein canon data source

The 10 books that anchor the methodology library:

| Book | Year | Author(s) | Use |
|------|------|-----------|-----|
| **Nudge: The Final Edition** | 2021 | Thaler + Sunstein | Foundation (9-nudge framework) |
| **Sludge** | 2021 | Sunstein + Reisch | Friction taxonomy |
| **Choosing Not to Choose** | 2015 | Sunstein | Default rules |
| **On Freedom** | 2019 | Sunstein | Ethics |
| **Too Much Information** | 2020 | Sunstein | Attention budgets |
| **Republic.com** | 2001 | Sunstein | Personalization warning |
| **The Cost-Benefit State** | 2023 | Sunstein | ROI measurement |
| **#Republic** | 2017 | Sunstein | Polarization + social |
| **Look Again** | 2024 | Sunstein | Noticing blind spots |
| **On Liberalism** (in progress) | 2026 | Sunstein | Forthcoming |

---

## Section 4: 14 agents to build (7 internal + 7 productized)

### Internal agents (Phase 1 — upgrade AI Whisperers)

These agents coach **Ivan, Kyrian, the 7 lead agents, and the org itself**. They're the first to be built and used.

#### 1. `coach-ivan` — weekly coaching for Ivan

- **Cadence**: Fri 16:00 PYT (30 min GROW session + async daily check-in)
- **Owner**: Ivan
- **Methodology**: GROW hybrid, Sunstein-aligned
- **Output**: `/opt/data/agents/coaching/state/ivan.json` (rolling 30-day coaching state)
- **Time to ship**: 4h
- **What it does**: Asks GROW questions on the founder's stated topic. Surfaces 1 blocker, 1 insight, 1 action per session. Maintains long-term memory of goals, progress, patterns.

#### 2. `coach-kiki` — weekly coaching for Kyrian

- **Cadence**: Fri 16:30 PYT (extends kiki-coach, adds GROW methodology)
- **Owner**: Kyrian
- **Methodology**: GROW + CLEAR hybrid, ICF-aligned
- **Output**: `/opt/data/agents/coaching/state/kiki.json`
- **Time to ship**: 4h
- **What it does**: Extends existing kiki-coach with full GROW methodology. Tracks technical growth milestones, blockers, breakthroughs.

#### 3. `coach-org` — quarterly org-design coaching

- **Cadence**: Quarterly (Jan/Apr/Jul/Oct 15th, 10:00 PYT)
- **Owner**: Erebus (autonomous)
- **Methodology**: Sunstein's choice architecture applied to org design
- **Output**: `/opt/data/agents/coaching/outbox/org-YYYY-Q.md`
- **Time to ship**: 6h
- **What it does**: Reviews ORG-AGENTS.md + dept specs + cron jobs + state files. Surfaces structural improvements using Sunstein's 5 principles. Recommends agent additions/removals.

#### 4. `coach-lead-agents` — monthly coaching for each lead agent

- **Cadence**: 1st of each month, 09:00 PYT (7 agents in series)
- **Owner**: Erebus
- **Methodology**: CLEAR (Celebrate/Look ahead/Explore options/Action/Review)
- **Output**: `/opt/data/agents/coaching/outbox/<agent>-YYYY-MM.md`
- **Time to ship**: 8h
- **What it does**: Each lead agent gets a 30-min "supervision session" — what's working, what's stuck, what to try. Like a 1:1 with a manager.

#### 5. `coaching-content-curator` — Sunstein canon + methodology library

- **Cadence**: Weekly Sun 14:00 PYT
- **Owner**: Erebus
- **Methodology**: Source-of-truth keeper
- **Output**: `/opt/data/agents/coaching/methodology/` updates
- **Time to ship**: 6h
- **What it does**: Maintains the canonical library. Reads new Sunstein material + competitor moves + ICF updates. Updates methodology files. Flags new prompts needed.

#### 6. `coaching-quality-reviewer` — review every coaching session

- **Cadence**: After every session (event-driven)
- **Owner**: Erebus
- **Methodology**: ICF ethics + Sunstein autonomy principle
- **Output**: `/opt/data/agents/coaching/state/qa-flags.json`
- **Time to ship**: 8h
- **What it does**: Every AI coaching session output goes through ethics + quality review. Flags: manipulation risk, factual errors, off-topic, scope creep. Queues for human review if needed.

#### 7. `coaching-research-intelligence` — monitor landscape

- **Cadence**: Weekly Sun 18:00 PYT
- **Owner**: Erebus
- **Methodology**: ddgs-based scanning + 200-co landscape diff
- **Output**: `/opt/data/agents/coaching/outbox/landscape-YYYY-MM-DD.md`
- **Time to ship**: 4h
- **What it does**: Monitors the 197-company coaching landscape for changes (new funding, new products, regulatory updates). Flags threats + opportunities.

### External agents (Phase 2 — productize)

These agents become part of the product sold to other companies. Each is a sub-component of the AI coaching SaaS.

#### 8. `coach-practitioner` — the actual AI coach

- **Cadence**: Event-driven (per user session)
- **Owner**: Customer's org
- **Methodology**: GROW + CLEAR + Sunstein
- **Output**: Coaching session transcript + reflection prompt + action item
- **Time to ship**: 16h (the core product)
- **What it does**: Runs the 1:1 AI coaching sessions. Trilingual. ICF + Sunstein aligned. Per-user memory. Adapts to user's progress.

#### 9. `coach-cohort-facilitator` — group coaching

- **Cadence**: Weekly per cohort (8-15 people)
- **Owner**: Customer's org
- **Methodology**: Group GROW + peer learning
- **Output**: Cohort summary + breakthrough log + action assignments
- **Time to ship**: 12h
- **What it does**: Facilitates group coaching sessions. Tracks cohort attendance, breakthroughs, completion. Sends personalized nudges.

#### 10. `coach-onboarding` — first 30 days

- **Cadence**: Daily per new user (first 30 days)
- **Owner**: Customer's org
- **Methodology**: Sunstein informed-consent + GROW kick-off
- **Output**: Onboarding state per user
- **Time to ship**: 8h
- **What it does**: Walks new users through informed-consent flow (Sunstein ethics). Sets up goals. Schedules first session. Tracks activation metrics.

#### 11. `coach-renewal-manager` — Tier A → B → C pipeline

- **Cadence**: Daily per org
- **Owner**: Customer's org
- **Methodology**: Usage-based upgrade triggers
- **Output**: Renewal pipeline per org
- **Time to ship**: 6h
- **What it does**: Monitors org's usage. Surfaces when Tier A is maxed → trigger upgrade pitch. Tracks renewal dates. Coordinates with sales agent.

#### 12. `coach-roi-tracker` — measure coaching impact

- **Cadence**: Monthly per org
- **Owner**: Customer's org
- **Methodology**: Adoption + behavior change + business outcomes
- **Output**: ROI report per org
- **Time to ship**: 12h
- **What it does**: Tracks adoption metrics (active users, session frequency). Behavior change signals (goal completion, breakthroughs). Business outcomes (when customer shares — engagement scores, retention, perf reviews).

#### 13. `coach-lead-finder` — find new customers (Solstein-driven)

- **Cadence**: Daily 11:00 PYT
- **Owner**: Ivan (sales)
- **Methodology**: Solstein coaching scorecard + 200-co landscape
- **Output**: `/opt/data/agents/coaching/outbox/leads-YYYY-MM-DD.md`
- **Time to ship**: 12h
- **What it does**: Runs Solstein coaching scorecard on prospect universe (existing 95 clients + new leads from landscape). Identifies top 10 prospects/day. Drafts outreach using b2b-cold-outreach-pitch skill.

#### 14. `coach-conversion-agent` — run free quick-win + upgrade funnel

- **Cadence**: Event-driven (per prospect)
- **Owner**: Ivan (sales)
- **Methodology**: Richar Ruiz playbook (free quick-win → S/M/L)
- **Output**: Per-prospect state in `/opt/data/agents/coaching/state/prospects/`
- **Time to ship**: 8h
- **What it does**: For each qualified lead, schedules free quick-win (1-h audit + 3 mock sessions). Tracks engagement. Triggers Tier S pitch at day 7, Tier M at day 30, Tier L at day 90.

### Total time to ship all 14 agents: ~120 hours (3-4 weeks at 30h/week)

---

## Section 5: Two-phase rollout (internal first, external second)

### Phase 1 — Internal first (Weeks 1-4)

The user's primary ask: **"first upgrade AI Whisperes fully."**

This is the **internal application** of the coaching methodology to ourselves.

#### Week 1 — Foundation (data layer + first agent)

- [ ] Build `/opt/data/agents/coaching/` directory structure
- [ ] Save Sunstein canon (10 books, indexed by principle)
- [ ] Save ICF 8 competencies (canonical source)
- [ ] Save GROW + CLEAR + OSKAR + T-GROW methodology
- [ ] **Build `coach-ivan`** (4h) — first real test of methodology on a founder
- [ ] Run first coaching session with Ivan (Fri 16:00 PYT)
- [ ] Build Solstein coaching scorecard (8 dimensions, new)

#### Week 2 — Activate Ivan + Kyrian coaching

- [ ] **Build `coach-kiki`** (4h) — extends kiki-coach with full GROW
- [ ] Run first coaching session with Kyrian (Fri 16:30 PYT)
- [ ] Capture 2 weeks of session transcripts
- [ ] Refine methodology based on what actually worked
- [ ] **Build `coaching-quality-reviewer`** (8h) — every session gets reviewed
- [ ] Establish QA flag rate baseline

#### Week 3 — Activate org coaching

- [ ] **Build `coach-org`** (6h) — quarterly org-design review
- [ ] **Build `coach-lead-agents`** (8h) — monthly supervision sessions
- [ ] First monthly "supervision" sessions for 7 lead agents
- [ ] **Build `coaching-content-curator`** (6h) — methodology library
- [ ] **Build `coaching-research-intelligence`** (4h) — landscape monitoring
- [ ] First landscape diff vs. the 200-company baseline

#### Week 4 — Internal proof + decision to go external

- [ ] After 1 month: Ivan + Kyrian both have weekly coaching
- [ ] 7 lead agents have had 1 monthly supervision session
- [ ] Org-design has had 1 quarterly review
- [ ] 50+ session transcripts captured
- [ ] QA flag rate stable
- [ ] **Decision**: proceed to Phase 2 if (a) founders find value, (b) methodology proven, (c) QA < 5% flag rate

### Phase 2 — External productization (Weeks 5-12)

Same agents become the product. Build the customer-facing versions.

#### Week 5-6 — Build the core product agent

- [ ] **Build `coach-practitioner`** (16h) — the actual AI coach for customers
- [ ] Wire to trilingual prompt library
- [ ] Wire to per-user memory schema
- [ ] Test with 3 internal users (Ivan, Kyrian, +1)
- [ ] Test in all 3 languages (es, en, nl)

#### Week 7-8 — Build the supporting agents

- [ ] **Build `coach-onboarding`** (8h)
- [ ] **Build `coach-cohort-facilitator`** (12h)
- [ ] **Build `coach-roi-tracker`** (12h)
- [ ] **Build `coach-renewal-manager`** (6h)

#### Week 9-10 — Build the sales agents

- [ ] **Build `coach-lead-finder`** (12h) — runs Solstein coaching scorecard
- [ ] **Build `coach-conversion-agent`** (8h) — runs the Richar funnel
- [ ] Wire to existing sales-pipeline agent
- [ ] Wire to existing b2b-cold-outreach-pitch skill
- [ ] Wire to existing paraguai-proposal-pricing skill

#### Week 11-12 — Pilot + first paying customer

- [ ] Ship MVP (coach-practitioner + coach-onboarding + coach-renewal-manager)
- [ ] Run 3 free quick-wins (1 legal, 1 dental, 1 beauty)
- [ ] First Tier A customer signed (any of the 3)
- [ ] First case study written

### Why this phasing works

1. **Internal = dogfooding**. We test the methodology on ourselves first. Ivan + Kyrian are the perfect canaries because (a) they have high standards, (b) they'll spot methodology gaps immediately, (c) the agents get real feedback before customers see them.
2. **External = same agents, productized**. The internal agents are the prototype. The customer-facing agents are the same logic with multi-tenant + UI + payments layered on.
3. **The data flows both ways**. Internal sessions become benchmark data. Customer sessions become methodology refinements. The two feed each other.

---

## Section 6: 90-day implementation plan

### Days 1-30 (Phase 1 — Internal)

| Week | Owner | Deliverable |
|------|-------|-------------|
| 1 | Erebus | Data layer + Sunstein canon + ICF + GROW methods; coach-ivan v0.1 |
| 2 | Erebus + Ivan + Kyrian | coach-kiki v0.1; first 2 weeks of sessions; methodology refinements |
| 3 | Erebus | coach-org + coach-lead-agents + coaching-quality-reviewer + coaching-content-curator + coaching-research-intelligence |
| 4 | Erebus + Ivan | First monthly supervision sessions; first quarterly org review; go/no-go decision |

### Days 31-60 (Phase 2 — Productize)

| Week | Owner | Deliverable |
|------|-------|-------------|
| 5-6 | Erebus + Kyrian | coach-practitioner MVP; trilingual prompts; tested with 3 internal users |
| 7-8 | Erebus | coach-onboarding + coach-cohort-facilitator + coach-roi-tracker + coach-renewal-manager |
| 9-10 | Erebus + Ivan | coach-lead-finder (Solstein coaching scorecard) + coach-conversion-agent (Richar funnel) |
| 11-12 | Erebus + Ivan | 3 free quick-wins; first Tier A customer; first case study |

### Days 61-90 (Scale)

| Week | Owner | Deliverable |
|------|-------|-------------|
| 13-14 | Erebus + Ivan | 10 free quick-wins across 5 verticals; 3 Tier A signups |
| 15-16 | Erebus + Ivan | First Tier B upgrade; first cohort program |
| 17-18 | Erebus + Kyrian | EU AI Act compliance pass; launch EU-friendly version |
| 19-20 | Erebus + Ivan | First Tier C enterprise close; first case study published |

### Year-1 targets (from coaching-funnel-playbook.md)

- 30 paying customers across 5 verticals
- $89-150K ARR run rate
- 14 agents all running
- 50+ ICF + Sunstein methodology patterns documented
- 3 case studies per vertical (15 total)

---

## Section 7: Risks + single bet

### Top 5 risks

| Risk | Mitigation |
|------|-----------|
| **Internal coaching fails** (Ivan/Kyrian don't find value) | Phase 1 go/no-go at day 30; pivot methodology before any customer-facing work |
| **Methodology IP isn't defensible** | Sunstein canon is canonical; we add the AI implementation layer + trilingual + ICF alignment — 3 layers of unique value |
| **Coaching quality flags too high** (>5%) | coaching-quality-reviewer in place from day 1; QA flags trigger methodology revision, not customer blame |
| **Customer onboarding friction** | coach-onboarding agent handles first 30 days; Sunstein informed-consent flow handles ethical disclosure upfront |
| **EU AI Act enforcement breaks our model** | coach-eu-compliance skill from day 1; we position as "EU AI Act + GDPR Article 9 ready" from the start |

### What NOT to do

- ❌ **Don't skip the internal-first phase**. The user explicitly said "first upgrade AI Whisperes fully." Phase 1 isn't optional.
- ❌ **Don't build external before internal proven**. Day-30 go/no-go is real.
- ❌ **Don't add a 7th department before Phase 2 ships**. The 6 existing departments are the canonical structure.
- ❌ **Don't build agents without data layer**. An agent without state is just a prompt.
- ❌ **Don't confuse coaching with therapy**. Sunstein's "On Freedom" framework draws the line. coach-quality-reviewer enforces it.

### Single biggest mistake to avoid

**Mistake**: Building all 14 agents in parallel before testing any of them on Ivan.

**Fix**: Ship `coach-ivan` in week 1. Run 4 weekly sessions with Ivan. Use what works. Drop what doesn't. THEN scale.

### The single bet

**The bet**: AI Whisperers can become the **first trilingual Sunstein-aligned AI coaching practice** by:
1. **Dogfooding internally first** (Phase 1: 7 internal agents coaching the org)
2. **Productizing externally** (Phase 2: same 7 + 7 external agents sold as a SaaS)
3. **Finding customers via Solstein** (the 13-dimension coaching scorecard)

**Year-1 revenue target**: $89-150K ARR run rate from 30 clients across 5 verticals.

**Single next action**: **Today, run a GROW session with Ivan.** Use the methodology we have. Capture the transcript. Use it as the seed for `coach-ivan` v0.1.

---

## Files cited

- `/opt/data/agents/ORCHESTRATION.md` — agent orchestration
- `/opt/data/agents/departments/ORG-AGENTS.md` — org constitution v0.2.0
- `/opt/data/agents/departments/01-operations.md` through `06-people-culture.md`
- `/opt/data/agents-v2/ROLES-INVENTORY.md` — 135 roles catalog
- `/opt/data/agents-v2/STORAGE-ARCHITECTURE.md` — SQLite + git storage
- `/opt/data/agents/business-analyst/PROMPT.md` — agent prompt template
- `/opt/data/agents/sales-pipeline/PROMPT.md` — agent prompt template
- `/opt/data/agents/state/` — 13 state JSON files
- `/opt/data/agents/research/200-ai-coaching-companies.md` — landscape
- `/opt/data/agents/research/30-coaching-research-areas.md` — research areas
- `/opt/data/agents/research/coaching-skills-gap-audit.md` — 11 skills
- `/opt/data/agents/research/coaching-strategic-implications.md` — strategy
- `/opt/data/agents/research/sunstein-solstein-inventory.md` — Sunstein + Solstein
- `/opt/data/agents/research/coaching-funnel-playbook.md` — funnel playbook

## Source data

- 24 cron jobs verified (org v0.2.0)
- 7 lead agents + ~14 sub-agents + 8 cross-cutting
- 6 departments + 135 roles across 30 functional areas
- Cass Sunstein canon: 10 books indexed
- ICF 8 competencies (canonical public)
- 200-company coaching landscape (the prospect universe)

## Last updated

2026-08-14 by Erebus (autonomous AI agent, AI Whisperers Paraguay EAS)