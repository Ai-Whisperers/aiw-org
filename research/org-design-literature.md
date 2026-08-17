# Org Design Literature — Synthesis

> The distillation of 20+ sources on small/medium business org design and AI-native
> company structure, mapped to our 6-department canonical model.

**Last updated**: 2026-08-14
**Sources**: See `/opt/data/source-materials/topics/org-design/INDEX.md` (the provenance catalog)

---

## Reading guide

This doc is the **synthesis**; the INDEX.md is the **provenance**. Every claim here
has a source. If you need to defend a position or pick between frameworks, start at
the INDEX, not here.

Sections:
- 1 — What "good org design" actually means (the 4 invariants)
- 2 — The 6-department shape and why it works
- 3 — Roles inside each department (the per-role anatomy)
- 4 — The AI-native shift (what changes when AI joins the org)
- 5 — The agent-as-role model (our specific application)
- 6 — What we explicitly reject
- 7 — Open questions for the user

---

## 1 — What "good org design" actually means (the 4 invariants)

Across Drucker, Grove, Bossidy, Collins, Mintzberg, Peters, and Blank, four invariants
emerge. Every functional org has them. Every dysfunctional one violates at least one.

### Invariant 1 — Decision rights are explicit

> Drucker (1954): "Management by Objectives works only when objectives are assigned,
> not negotiated upward."
> Grove (1983): "High-leverage activities are the ones where a small change in input
> produces a large change in output. Decision rights ARE the leverage."

**Our application**: `ORG-AGENTS.md` lines 58-75 — the decision rights matrix with USD
thresholds. Every agent knows what it can decide (< USD 50 logged, USD 50-500 surface,
USD 500-5K Ivan, > USD 5K Ivan + Kiki).

### Invariant 2 — Boundaries are exclusive

> Mintzberg (1979): "Every organizational form is a coherent configuration. Hybrid
> configurations fail because each part pulls toward a different center."
> Bossidy (2002): "If two people own the same process, neither owns it."

**Our application**: Each of the 6 dept specs has a "What this department does NOT own"
section pointing to the dept that does. No overlap allowed.

### Invariant 3 — Cadence beats heroics

> Grove (1983): "A manager's output = the output of their organization × the leverage
> of their activities. Leverage comes from process, not cleverness."
> Collins (2001): "Great companies have disciplined people, thought, and action."

**Our application**: Cron-agent layer (`ORCHESTRATION.md`). Every recurring decision has
a fixed cadence. The agents do the work; the founders review the outputs.

### Invariant 4 — Specialization beats generalization (below ~50 people)

> Mintzberg (1979): "Below 50 people, a divisional structure doesn't pay for itself."
> Organimi SMB playbook: "Hire your first specialist when you've done the role
> yourself for 90 days and have a clear playbook."

**Our application**: We have 6 specialist departments, not 1 "generalist ops" role.
Each role inside a dept is specialized. We don't hire "general helpers" — we hire the
specific role when its playbook is mature.

---

## 2 — The 6-department shape and why it works

Salesforce SMB, Organimi, and Business News Daily all converge on **6 functional
departments** as the right shape for small businesses (1-50 people): Operations,
Finance, Sales/Marketing, Engineering/Product, Research, People/HR. Variations exist
(Legal merges into Finance, Marketing splits from Sales) but the 6-function spine is
canonical.

### Why these 6 (in this exact order)

| # | Dept | What it owns | Why it can't merge with anything |
|---|------|--------------|----------------------------------|
| 1 | **Operations** | The platform itself — cron jobs, repos, infra health, cross-cutting | If the platform dies, every other dept dies too. Must be its own thing. |
| 2 | **Finance & Legal** | Money + contracts + compliance | Legal and finance share a USD threshold (spend = contract = liability). Merge. |
| 3 | **Sales & Growth** | Revenue-producing activity | Sales and marketing share an ICP and a funnel. Merge. |
| 4 | **Engineering & Delivery** | Product + infra + code | Engineering without delivery = endless prototypes. Engineering without ops = outages. All three belong together. |
| 5 | **Research & Education** | IP + thesis + courses | This is our flagship asset. Has its own cadence (Sun review) and its own consumer (academic / course audience). Cannot be a sub-dept. |
| 6 | **People & Culture** | Founder growth + contractor mgmt | Small now, but won't be. Has its own emotional dynamics that don't fit any other dept. |

### What collapses at 2-person scale

Ivan named 15 departments in the recording. Our canonical model collapses them to 6:

| Ivan's 15 named | Maps to | Why collapsed |
|---|---|---|
| Finance | Dept 2 | Direct match |
| HR | Dept 6 | Merged into People & Culture (deferred until first FTE hire) |
| Legal | Dept 2 | Merged into Finance & Legal (shared spend thresholds) |
| Development | Dept 4 | Direct match |
| QA | Dept 4 sub-role | A QA engineer is a specialist inside Engineering, not a separate dept |
| Operational | Dept 1 | Direct match |
| Research | Dept 5 | Direct match |
| Management | Cross-cutting (board + coordinators) | A layer above the depts, not a peer |
| Board of directors | Ivan + Kiki | 2 people = board |
| Inventory | Dept 1 sub-process | Asset tracking is a SOP, not a dept |
| Buying / Procurement | Dept 2 sub-process | Vendor mgmt is a SOP, not a dept |
| Accounting | Dept 2 sub-process | Bookkeeping is a SOP, not a dept |
| Marketing | Dept 3 sub-process | Has same ICP as sales |
| Multimedia | Dept 3 sub-process | Marketing deliverable |
| OpSec | Dept 4 sub-process | Security is a specialist role inside Engineering |

**The principle**: at 2-person scale, only **outcomes that have different decision
rights, different cadences, or different consumers** warrant separate departments.
Everything else is a role inside an existing dept.

---

## 3 — Roles inside each department (the per-role anatomy)

The full glossary is in `/opt/data/agents/research/roles-glossary.md` (90+ roles).
This section gives the per-dept overview — what each dept needs at minimum, what's
overkill, and what we'd hire first if we scaled.

### Department 1 — Operations (target: 5-7 roles)

Core roles: **Operations Lead, Repo Steward, Asset Tracker, Vendor Coordinator,
Compliance Watchdog, Watchdog Engineer.**

At 2-person scale: Operations Lead = Ivan (oversight), Asset Tracker + Vendor
Coordinator = sub-agents of `management-coordinator`, Compliance Watchdog = sub-agent
of `finance-controller`, Watchdog Engineer = Kiki (technical).

### Department 2 — Finance & Legal (target: 6-9 roles)

Core roles: **CFO/Controller, Accountant, Bookkeeper, AP/AR Specialist, Procurement
Officer, Legal Counsel, Compliance Officer, Tax Specialist, Contract Drafter.**

At 2-person scale: CFO = Ivan (signoff), Procurement + Bookkeeping + Tax =
sub-agents of `finance-controller`, Legal Counsel = external contractor on retainer,
Compliance Officer = `trademark-compliance-scrub` skill (sub-agent).

### Department 3 — Sales & Growth (target: 5-7 roles)

Core roles: **Head of Sales, SDR / Outbound Rep, Account Executive, Proposal Writer,
Marketing Manager, Content Producer, Multimedia Designer.**

At 2-person scale: Head of Sales = Ivan (signoff), SDR + AE + Proposal Writer =
sub-agents of `sales-pipeline`, Marketing Manager + Content Producer + Multimedia
= future agents (Tier 2 / Tier 3 in Session 4).

### Department 4 — Engineering & Delivery (target: 8-12 roles)

Core roles: **CTO/Eng Lead, Backend Engineer, Frontend Engineer, Full-stack Engineer,
DevOps / SRE, QA Engineer, Security Engineer, Data Engineer, Mobile Engineer,
Solutions Architect, Tech Writer.**

At 2-person scale: CTO = Kiki (oversight), Backend + Frontend + Full-stack = Kiki
(consolidated), DevOps = Kiki (sub-agent `engineering-roster`), QA = automated
test suite (CRON_WORKFLOW), Security = `security-watchdog` (sub-agent).

### Department 5 — Research & Education (target: 4-6 roles)

Core roles: **Research Lead, Researcher, Writer/Editor, Course Designer, Course
Producer, Academic Liaison.**

At 2-person scale: Research Lead = Ivan, Researcher = `research-tracker` agent +
Ivan's own thinking, Writer/Editor = Ivan + sub-agent for grammar check, Course
Designer = Ivan, Course Producer = sub-agent for video/slides.

### Department 6 — People & Culture (target: 3-5 roles)

Core roles: **Head of People, Recruiter, Onboarding Specialist, Performance Coach,
Recognition Lead.**

At 2-person scale: Head of People = Ivan + Kiki (co-owned), Coach = `kiki-coach`
agent, Recruiter = not until first FTE hire. Per `people-culture.md` lines 102-108,
HR sub-functions are explicitly deferred until then.

---

## 4 — The AI-native shift (what changes when AI joins the org)

The pre-2020 literature (Drucker through Collins) was written for **human-only orgs**.
The 2020+ literature (MetaGPT, CrewAI, ASTELD, Anthropic) is written for **agent-augmented
orgs**. Three changes matter:

### Change 1 — Roles become configurable, not hired

> MetaGPT (2023): "Code = SOP(Team)." The same outcome can be produced by different
> team configurations. The team is a function of the SOP, not the other way around.

**Before AI**: You hire a person for the role. The role is fixed by headcount.
**After AI**: You write a SOP. The SOP can be filled by an agent, a human, or a hybrid.
Headcount becomes a **budgeting question**, not a structural one.

### Change 2 — Decision rights can be enforced in code

> ASTELD (2026): The 6-axis classification (autonomy, scope, tools, persistence,
> memory, collaboration) lets you define agent boundaries **before deployment**.

**Before AI**: Decision rights live in policy docs. Violations get caught in post-hoc audits.
**After AI**: Decision rights live in `PROMPT.md` guardrails. Violations get caught at
prompt-time. Our constitution's "Hard rules" sections (per dept spec) are the
implementation.

### Change 3 — Cadence becomes free

> Anthropic (2024): Agents can be triggered by event (webhook), time (cron), or
> condition (state threshold). The cost of an additional cadence slot is near-zero.

**Before AI**: One manager per N reports. Adding cadences (weekly 1:1s, monthly
reviews) costs linear in headcount.
**After AI**: Adding a cron job is a config change. We can have 20 different cadences
running simultaneously. Our `ORCHESTRATION.md` has 11 cadences already (3 dept leads,
3 cross-cutting, 5 watchdogs) at 2 people — physically impossible pre-AI.

---

## 5 — The agent-as-role model (our specific application)

Every role in our glossary has one of four classifications (full taxonomy in
Session 4 — automation-map.md):

| Class | Definition | Examples |
|-------|-----------|----------|
| **FULL_AGENT** | Replaceable today by an LLM agent with current tools | "Daily LinkedIn post drafter", "Weekly expense categorizer", "Monthly invoice generator" |
| **HITL_AGENT** | Agent drafts / recommends; human approves | "Proposal writer", "Contract reviewer", "Pricing decision for new vertical" |
| **CRON_WORKFLOW** | Deterministic script; no LLM reasoning needed | "Daily HTTP health check", "Weekly backup verification", "Monthly P&L roll-up" |
| **HUMAN_ONLY** | Judgment + relationships that don't reduce to pattern | "Sales closing call", "Crisis management", "Co-founder conflict resolution", "Thesis chapter sign-off" |

The current state of our org (per `ORCHESTRATION.md` and the 6 dept specs):

| Dept | FULL_AGENT | HITL_AGENT | CRON_WORKFLOW | HUMAN_ONLY |
|------|-----------|-----------|---------------|-----------|
| Operations | 1 (`management-coordinator`) | 0 | 4 (`health.sh`, `site-health`, `thesis-watchdog`, `evo-poll-watchdog`) | 1 (Ivan's escalation review) |
| Finance & Legal | 1 (`finance-controller`, not yet wired) | 0 | 0 | 2 (Ivan signs contracts; Kiki reviews delivery) |
| Sales & Growth | 1 (`sales-pipeline`, not yet wired) | 0 | 0 | 1 (Ivan sends outreach) |
| Engineering & Delivery | 1 (`engineering-roster`, not yet wired) | 0 | 3 (`ometzdental-weekly-refresh`, `repo-ci-monitor`, `rbl-check`) | 1 (Kiki merges prod PRs) |
| Research & Education | 1 (`research-tracker`, not yet wired) | 0 | 3 (`thesis-daily-tick`, `thesis-weekly-review`, `thesis-git-maintenance`) | 1 (Ivan signs thesis chapters) |
| People & Culture | 1 (`kiki-coach`) | 0 | 0 | 2 (Kiki picks lesson topic; co-founder conflict resolution) |

**Total**: 6 agents wired + 3 to wire (already specified but not running) + 10
watchdogs/workflows. The Session 4 work is to classify every other role in the glossary
and decide which to add next.

---

## 6 — What we explicitly reject

Three things the literature suggests but we are not doing:

### Reject 1 — Hiring a full-time HR person at 2 people

Mintzberg, Collins, and Bossidy all say "people is a specialist function." True at 50
people. Premature at 2. We keep People & Culture as a **future-ready** dept (so the
constitution is already shaped), but we don't staff it. Per `06-people-culture.md`
lines 102-108: "When AI Whisperers hires its first employee (not contractor), this
department expands."

### Reject 2 — Building an "AI Governance Committee"

HBR pieces from 2023-2025 advocate for an AI governance committee. We don't have one
because the agents' decision rights **are** the governance — encoded in each
`PROMPT.md`'s "Hard rules" section and enforced at prompt-time. Adding a committee
adds a layer of human review for decisions the agents already can't make.

### Reject 3 — Adopting agile/scrum

Jan Bosch (2026) and other 2026-era sources argue agile is obsolete for AI-native teams.
We never adopted it. Our cron-agent layer is the post-agile operating model — every
recurring decision has a fixed cadence, every state change is logged to a JSON file,
every escalation path is encoded in a department spec. No standups. No sprints. No
retros. Just cadence + state + escalation.

---

## 7 — Open questions for Ivan

Three questions the literature surfaces but we can't answer autonomously:

### Q1 — When do we hire the first FTE?

The Organimi playbook says "after 90 days of clear SOPs in the role." For us, that
means: when does a role have a SOP mature enough that the playbook can be handed to a
human? Currently the closest candidates are: (a) Sales SDR (we have a documented
outreach playbook in `b2b-cold-outreach-pitch`), (b) Operations Coordinator (we have
the management-coordinator agent doing the work). 

**Recommendation**: revisit at $5K MRR (currently $240/mo MRR per `state/finance.json`).

### Q2 — Do we ever add a 7th department (Customer Success)?

Customer Success is the canonical 7th dept in B2B SaaS. We currently subsume CS into
Operations (post-delivery retention) and Sales (pre-sale discovery). If our
retention/expansion motion grows past 20% of revenue, we'd split it out.

**Recommendation**: defer until we have 5+ recurring clients to manage.

### Q3 — Board of directors — when does it grow beyond 2?

Current board = Ivan + Kiki. The literature says boards add independent directors at
$1-5M ARR or pre-Series A. We're nowhere near that. 

**Recommendation**: revisit at $50K MRR.

---

## See also

- `INDEX.md` (this folder) — source provenance catalog
- `cheatsheet.md` (this folder) — org-size decision table
- `/opt/data/agents/research/roles-glossary.md` — the role inventory (90+ roles)
- `/opt/data/agents/departments/ORG-AGENTS.md` — our constitution
- `/opt/data/agents/research/STRATEGY.md` — overall org strategy
- `/opt/data/agents/research/30-research-areas.md` — research agenda
