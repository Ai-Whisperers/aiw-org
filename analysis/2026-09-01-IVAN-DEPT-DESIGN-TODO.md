# Ivan — Department design to-do

> **For**: Ivan Weiss van der Pol  
> **Date**: 2026-09-01  
> **Verified against**: `origin/master` HEAD `7ed8676` (Phase 36, same day)  
> **Inputs**: Magic Tower board notes; Friday 28 Aug transcripts (11.24 John design brief, 11.54 weekly); `DEPT-AGENTS-ROLES-COMPLETE.md`; Phase 26–36 feedback.
> **Meeting source of truth**: [`meetings/department-design/README.md`](../meetings/department-design/README.md) (do not treat this TODO as the decision log).

**Rule from John (28 Aug) and from your own Phase 30 pivot:** do not stand up more departments. Run the agents you already named. Close Product Management. Make Analisa / Devin / Qualis / Safina / Prospia / Markina do their jobs.

---

## 0. Current state (verified)

| Fact | Evidence |
|---|---|
| Latest commit | `7ed8676` — Phase 36 multilingual + cron auto-fix apply + wrapper wildcard (2026-09-01) |
| Scope lock | Phase 30: no new depts; keep existing six; focus eng + QA + AI safety |
| Six Tier-1 dirs | `01-operations/` … `06-people-culture/` + `board-of-directors/` |
| Magic Tower names in repo | Devin, Qualis, Safina, Analisa, Prospia, Markina (`analysis/AGENT-NAMES-V2.md`) |
| DEMIURGE souls | 24 under `demiurge/agents/` (Hera, Apollo, Calliope, Cadmus, Metis, Athena, Clio, Kronos, …) |
| Routing | Built Phase 28, crons wired Phase 29 (`aiw-router-5min`, per-dept intake, results-collector) |
| Hard-stops | 63/63 PROMPTs (Phase 33); wrapper actually enforces (Phase 27 bugfix) |
| Whitelists | 63/63 (Phase 33) |
| Red-team | 38/38 pass, 15 languages (Phase 36) |
| Tests / lint | 219/219, lint 63/63, audit-fresh 12/12 |
| Crons | 149 total, 133 enabled; 22 staggered; 6 still failing on **token-plan 429** (Sunday auto-recover) |
| Sales funnel | **Deferred Q1 2027** (your D1=c, Phase 27) |
| Credential rotation (H6) | Permanently deferred; PAT leak was untracked in `195e055` — rotation still a human task |
| Product Management | **Not a live department.** Taxonomy Tier 3 (`>3 parallel roadmap tracks`). Athena/Clio = discovery only, not PO |

**Stale docs (do not trust as live):** `GAP-ANALYSIS-2026-09-01.md` still says “no router.py”. That was true before Phase 28. Routing exists now.

**Missing charters:** `department-index.md` points at `departments/01-operations.md`, `02-finance-legal.md`, `05-research-education.md`. Only `03`, `04`, `06` charters exist under `departments/`.

---

## 1. Do this week — design, not more agents

### 1.1 Freeze the org chart (30 min)

- [ ] Write one page: **six depts + board is the freeze**. Product Management is the only candidate to promote; everything else stays deferred (`DEFERRED-ROLES.md` / taxonomy Tier 3–4).
- [ ] Put that freeze in `DECISIONS-2026-Q3.md` (or a 2026-09-01 decision note) so the next Hermes session cannot “add a department”.
- [ ] Stop generating new heritage names. Magic Tower roster is enough for talk: Devin, Qualis, Safina, Analisa, Prospia, Markina, plus DEMIURGE (Apollo, Calliope, Athena, …).

### 1.2 Close the Product Owner hole (John’s #1, Magic Tower section 2)

John (11.24): you are missing **product management / PO**. Engineering is fine. Sales must not invent a custom product per client.

- [ ] Decide the **human PO** (you, Kiki, or split: you own commercial product, Kiki owns delivery scope).
- [ ] Write a **one-page product list**: name, who it is for, what is in / out, what sales may promise. Only products you already ship or will ship this quarter. Do not spec products you will never build.
- [ ] Add a **Product Owner agent** (do not create a seventh Tier-1 folder yet). Recommended placement:
  - DEMIURGE already has **Athena** (`athena-product-discovery-lead`) + **Clio** (signals).
  - That is discovery, not ownership.
  - Either promote Athena’s brief to include PO (roadmap, “this is the SKU”, pushback to sales) **or** add one heritage agent (`product-owner` / named) under `03-sales-growth/` or a thin `product/` dir that is **not** a new charter dept until the taxonomy trigger is met.
- [ ] Wire PO handoffs: Sales (Saleina/Apollo/Prospia) → PO → Devin/Qualis. Consultants/sales wishes go to PO, not straight to Devin.
- [ ] Explicit anti-goal: no per-client fork of the product without PO sign-off.

### 1.3 Align the Magic Tower board to the catalog (1–2 h)

Board vs repo (fix naming, don’t add agents):

| Board | Repo (keep this) | Action |
|---|---|---|
| DEVIN | `engineering-roster` / **Devin** | Confirm Kiki is human head; Devin is roster/chief agent |
| Qualis | `qa-automation-runner` | Expand mission: **delivery QA**, not only test runner (Nexa language errors) |
| Safina | `ai-safety-engineer` | Keep as “checks Devin”, not QA of client copy |
| Analisa | `business-analyst` | Expand: meetings, weeklies, transcripts, next-meeting briefs (John + Friday weekly) |
| Prospia | `lead-enrichment` | Email + hot/cold/follow-up; blocked until Gmail/CRM is reliable **or** Q1 2027 funnel |
| MaxRina | **Markina** / Calliope | Fix the spelling in any board photo notes; one name only |
| Renata | `research-tracker` | Confirm; not a second research dept |
| Rostercho | Devin / Rosterina | Same person as Devin — delete the duplicate label |

- [ ] Add missing charters so the index is not a lie: `departments/01-operations.md`, `02-finance-legal.md`, `05-research-education.md` (copy shape from `03` / `04` / `06`).
- [ ] One paragraph on the Magic Tower org line (shareholders → board → CEO → CTO/CFO/COO) mapped to humans: Ivan CEO, Kiki CTO, CFO/COO still hats not agents.

### 1.4 Make Analisa the meeting secretary (Friday 11.54)

You and Kiki still move phone audio by hand. That is Analisa’s job.

- [ ] Define Analisa’s weekly output: dated recap, **topic-split** (so Nexa / departments / sales don’t mix), open actions, Monday agenda.
- [ ] Point Analisa at the meeting-transcriptions repo / Drive weekly+monthly folders — do not build a new department for this.
- [ ] First live test: ingest 28 Aug 11.24 + 11.54 + Magic Tower notes into one Analisa brief for Kiki.

### 1.5 Qualis on real deliveries (Friday 11.54)

John: delivery must go through quality control. Nexa had a fake “official translations” string.

- [ ] Add a **pre-publish checklist** Qualis owns: every language pass, obvious non-language, links, WhatsApp number 0985 724 135 only.
- [ ] Devin does not ship client sites to Luana/Sonia without Qualis.
- [ ] Safina stays AI-safety (hard-stops, injection); Qualis stays product/QA. Do not merge them.

### 1.6 Marketing content path (Markina / Calliope)

Friday: freelancer → monthly posts → Drive → auto-publish. John: person must fit the AI company; don’t dump them into Hermes on day one.

- [ ] Decide: Drive drop-folder vs Hermes agent for the freelancer (John: Hermes later, if they stay).
- [ ] Markina/Calliope stores drafts and calendar; human still writes until the person is onboarded.
- [ ] PO (1.2) must own **which products get posts**. Do not market an undefined product list.

---

## 2. Next 2 weeks — use the org you already built

Routing and safety exist. You are still the human router until you actually talk to agents.

- [ ] **Stop asking Kiki for Ivan-status.** Ask Analisa / management-coordinator: “what did Devin commit, what’s pending?”
- [ ] Confirm live: signal → `aiw-router-5min` → dept intake → `state/<dept>/tasks.jsonl` → results-collector. If that path is idle, it is an **ops** problem, not a missing department.
- [ ] Per-dept tools: John said PO should not have a coding toolchain. Audit that whitelists (Phase 33) match that. Tighten if every agent still loads every skill.
- [ ] Founder-bandwidth-watchdog: treat overwhelm (Friday) as a signal, not a new people department.

### Sales / Prospia (respect your own deferral)

- [ ] Do **not** revive the public funnel until Q1 2027 unless you reopen D1.
- [ ] Until then: Prospia may watch **existing** inbound (Gmail once it works on Kiki’s machine) and write research docs. No new SKU, no Formspree/Worker debate in this sprint.
- [ ] Instagram/LinkedIn/Gmail for Kiki is **engineering/ops** (Devin/Ivan hands-on), not a new sales dept.

### Research (Renata)

- [ ] Keep research as process/tech upgrades for other depts (Magic Tower). Do not spin “Research & Ideation” as a seventh charter.
- [ ] Funding hunt stays in `funding-coordinator` (finance), not a new dept. Friday: hunt grants; don’t dump a new idea pile on Kiki.

---

## 3. Engineering track (only if you stay on Phase 30–37)

You already said no more departments. If the next Hermes session is another phase, keep it **inside** Devin/Qualis/Safina:

| Priority | Item | Notes |
|---|---|---|
| 1 | Remaining 5 cron staggers | Phase 36 leftover (~5 min) |
| 2 | Token-plan decision with Kiki | 6 jobs fail HTTP 429; not a code bug |
| 3 | Confirm PAT rotation from `195e055` | Human GitHub settings; do not commit new tokens |
| 4 | Chaos scenarios 2–5 | Needs your approval (prod-adjacent) |
| 5 | Drift detector never fired | Debug or accept; don’t add a monitor dept |
| 6 | Real token cost vs estimate | Tier J; optional |
| 7 | More languages / wrapper rate-limit | Phase 37 nice-to-haves, not org design |

**Do not do:** H6 credential-rotation automation (you deferred it). Cycle keys as a later ops ritual (John: half-year), unless the PAT incident forces it now.

**Do not do:** new Tier-3 depts (CS, standalone Marketing, KM, CoS, …) until triggers in `docs/demiurge/department-taxonomy-v1.md` fire.

---

## 4. Explicitly out of scope (so you don’t rebuild the tower)

- Another full org-chart session that adds agents for every WPG analogue.
- Selling “buy this department” SKUs (that is growth-coaching product work, not `aiw-org` design).
- Nexa as a 6-dept clone (`departments/NEXA-DEPARTMENT-SETUP-PLAN.md` already says Nexa is too small — extend existing layer).
- Running all 49 agents “because the folders exist.” John: **agents that are needed**, not the organigram.
- Mixing Safina (AI safety) with Qualis (QA of sites/copy).
- Reopening sales funnel engineering before Q1 2027 without a new written decision.

---

## 5. Decisions that need Kiki (not more Ivan agents)

| Decision | Why |
|---|---|
| Token plan / provider credits | Unblocks 6 failing crons |
| Confirm PAT rotation done | Safety, not a department |
| Human PO vs you | 1.2 cannot ship without this |
| Qualis on Nexa/Luana publish | Delivery quality |
| Freelancer vs Markina for Sept content | Marketing path |
| Whether you reopen D1 (funnel) | Currently locked to Q1 2027 |

---

## 6. Suggested order for Ivan’s next working session

1. Freeze + missing charters (1.1, 1.3).  
2. Product list + PO agent brief (1.2).  
3. Analisa meeting-brief prompt (1.4).  
4. Qualis pre-publish checklist (1.5).  
5. Talk to Analisa/Devin instead of expanding folders.  
6. Only then: Phase 37 cron stagger + token-plan with Kiki.

If a session starts generating new department folders, stop. That contradicts both John’s 28 Aug brief and your Phase 30 commit message.
