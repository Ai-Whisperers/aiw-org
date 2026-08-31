# Department Expansion Roadmap

**Created**: 2026-08-28  
**Last updated**: 2026-08-31 (status snapshot)  
**Scope**: Scale from 3 active DEMIURGE departments to full org + meta-agent framework  
**Philosophy**: Identify fast → flesh out one → extract meta-skills → scale with those skills

---

## Status snapshot (2026-08-31)

| Phase | Item | Status | Evidence |
|-------|------|--------|----------|
| 1 | Identify + Stabilize | ✅ Done | `docs/INDEX.md`, `docs/ROLES-INVENTORY.md` updated; 24 DEMIURGE agents shipped |
| 2 | Operations reference build | ✅ Done | `Kronos` ops lead + Hermes router wired (DEMIURGE-075, 076, 079, 080) |
| 3 | Meta-agent framework | 🟡 Partial | Department Researcher (Thoth) + Echo shipped; Decorator/Finder/Coach pending |
| 4 | Scale all departments | ⏳ Pending | 1 dept per session — Operations done, 5 remaining for next quarter |

**Open Tier-1 dept activations (in priority order)**: Operations (done) → Engineering → Finance & Legal → AI Ops → Customer Success → RevOps → Research → People → Compliance → Knowledge Mgmt → Product Mgmt → Data Science → BD → Design → Executive Office

**Files to keep updated**:
- `docs/ROLES-INVENTORY.md` — 137 roles
- `docs/MASTER-UPGRADE-CHANGELOG.md` — session log
- `docs/phases/REMAINING-TASKS-AND-WISHLIST.md` — 135-item wishlist
- `docs/phases/PHASE-25-AROUND-THE-CLOCK-UPGRADE.md` — most recent session

---

## Current state

| Layer | Count | Status |
|-------|-------|--------|
| DEMIURGE active (`departments/`) | 3 | marketing, sales, product-discovery |
| Constitution legacy (`agents-prompts/`) | 6 | operations, finance-legal, engineering, research, people, sales-growth |
| Taxonomy skeleton | 20+ | Tier 2/3/4 — defined, no agents |
| Ivan's Hermes dept profiles | unknown count | Running as Hermes system prompts → need formalization |

---

## Gap summary (from 2026-08-28 gap analysis)

**New departments to add to taxonomy (not in any tier):**
- Executive Office
- IT / Enterprise IT
- Business Development & Partnerships
- Design / Creative Studio
- Program Management Office (PMO)
- Field / Professional Services
- Meta-agent framework dept (AI Org Platform)

**Partial — exist as roles/stubs, need promotion to full dept:**
- Product Management (separate from Product Discovery)
- Data Science & Analytics (beyond RevOps BI)
- Cybersecurity / InfoSec (separate from AI Safety)
- Corporate Communications & PR
- Customer Experience
- Multimedia Production (was in original org, dropped from taxonomy)

**Critical doc-impl mismatches to fix:**
- README says "16 deptos" → real count is 3 active
- `ai-safety` and `operations` flagged "active" in taxonomy but no `departments/` folder
- ORGANIGRAM doc says "51 agents, 18 deptos" → outdated

---

## Phase 0 — Done ✓

Revenue stack: marketing → product-discovery → sales, with Hermes router + Argus monitor.

---

## Phase 1 — Identify + Stabilize (now)

**Goal**: Everything identified, taxonomy correct, Ivan's Hermes profiles registered. Not 100% perfect — directionally correct.

| Task | Ticket | Output |
|------|--------|--------|
| Fix taxonomy: add 7 New depts + promote 6 Partial | DEMIURGE-070 | Updated `department-taxonomy-v1.md` |
| Fix doc-impl drift: README counts, ai-safety/operations status | DEMIURGE-071 | Corrected files |
| Inventory Ivan's Hermes dept profiles → stub agent.yaml per profile | DEMIURGE-072 | `demiurge/agents/<id>/agent.yaml` stubs |
| Define AI Org Platform as a department (the meta-framework dept) | DEMIURGE-073 | `departments/ai-org-platform/department.md` skeleton |

**Exit criteria**: `department-taxonomy-v1.md` is the single source of truth, no contradictions with README or ORGANIGRAM.

---

## Phase 2 — Reference Department (one full buildout)

**Goal**: Take one Tier 1 skeleton department and build it to full DEMIURGE standard. The process produces the patterns we'll extract into meta-agents.

**Pick**: `operations` — it exists in constitution, has legacy agents, is Tier 1, and every company needs it.

| Task | Ticket | Output |
|------|--------|--------|
| Research operations dept: sources, frameworks, state-of-the-art (signal-driven ops) | DEMIURGE-074 | `sources/operations/catalog.yaml` + `sources/operations/gaps.md` |
| Define Operations dept: mission, roles, signals, KPIs, cadences | DEMIURGE-075 | `departments/operations/department.md` + `signals.yaml` + `cadences.md` |
| Design + wire Operations lead agent soul | DEMIURGE-076 | `demiurge/agents/kronos-operations-lead/` |

**Exit criteria**: Operations dept self-running at same level as marketing/sales/product-discovery.

---

## Phase 3 — Extract Meta-Agent Framework

**Goal**: Everything we did manually in Phase 2 becomes a prompt/rule/agent. These are the tools Ivan uses to stand up any department.

| Meta-agent | What it does | Feeds from |
|------------|-------------|-----------|
| **Department Researcher** | Given a dept name, finds best sources (books, papers, communities, frameworks). State-of-the-art science on running that dept. | Generalized Thoth + Echo — parameterized by dept |
| **Department Decorator** | Given a skeleton dept (mission + roles), produces full `department.md` + `signals.yaml` + `cadences.md` | Phase 2 process → rule/prompt |
| **Department Finder** | Given company size/stage/vertical, recommends which depts to activate and in what order | Taxonomy + trigger logic |
| **Department Coach** | Given a dept + its KPIs, coaches the founder on how to run it using current science | Signal data + frameworks from Researcher |
| **Role Finder** | Given a dept + current headcount, recommends which roles to fill next | ROLES-INVENTORY + dept context |
| **Role Researcher** | Given a role, researches state-of-the-art on what good looks like (OKRs, tools, benchmarks) | Same pattern as Dept Researcher |
| **Role Decorator** | Given a role definition, produces a full role spec with evaluation criteria, tools, signals | Same pattern as Dept Decorator |

**Output artifacts**: prompts in `prompts/`, rules in constitution/rules, agents in `demiurge/agents/`.

**Note on Ivan's profiles**: If Ivan is running Hermes as a "Marketing Head" profile, "Sales Head" profile, etc. — those ARE the Department Coach agent. Formalize the profiles as `PROMPT.md` files in the right agent folders.

---

## Phase 4 — Scale: All Departments

Use Phase 3 meta-agents to stand up each remaining department, one session at a time.

**Order** (based on build-order from taxonomy + business priority):

| # | Department | Trigger / Why now |
|---|-----------|-------------------|
| 1 | Operations | Phase 2 — reference build |
| 2 | Engineering | Revenue stack needs eng support |
| 3 | Finance & Legal | First paying customers require invoicing |
| 4 | AI Ops | Agent layer grows, needs dedicated ops |
| 5 | Customer Success | After first 5 recurring clients |
| 6 | RevOps | After $2K MRR |
| 7 | Research | Ongoing — knowledge backbone |
| 8 | People | After first FTE |
| 9 | Compliance | After first EU client |
| 10 | Knowledge Mgmt | After 100+ source files |
| 11 | Product Management | When roadmap has >3 parallel tracks |
| 12 | Data Science | When data volume justifies |
| 13 | Business Development | First partnership deal |
| 14 | Design / Creative | First design hire |
| 15 | Executive Office | When >5 active depts need coordination |
| 16+ | PMO, Field Services, etc. | On trigger |

Each department = one sprint, using the meta-agent framework from Phase 3.

---

## Meta-pattern: how each department session works

```
1. Department Researcher runs → source catalog + framework summary
2. Department Finder confirms priority + trigger met
3. Department Decorator produces department.md + signals + cadences
4. Agent design session → lead agent soul + sub-agents
5. Wire to router (Hermes)
6. Monitor via Argus (or per-dept monitor if Phase 3 builds one)
7. Department Coach configured → ongoing signal-driven coaching
```

---

## What we are NOT doing (intentional deferral)

- Per-department git repos split (CONVERSATION-NOTES item 11) — after Phase 3
- Tooling tiers doc (1-5, 5-20, 20+) — after first customer
- Generic customer template (the sellable product) — after first paying customer using it
- Tier 3+ departments not on the list above — on their stated triggers only

---

## Timeline (rough)

| Phase | Sessions | Outcome |
|-------|----------|---------|
| Phase 1 | 1-2 | Taxonomy clean, profiles registered |
| Phase 2 | 2-3 | Operations fully active |
| Phase 3 | 3-4 | Meta-agent framework extracted |
| Phase 4 | 1 session per dept | Each dept live |

No fixed calendar. Each phase starts when previous exits.
