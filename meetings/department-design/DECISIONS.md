# Department design — ratified decisions

> **Source of truth for what we decided**, not for what code exists.  
> Newer dated session + explicit “supersedes” wins.  
> Last updated: 2026-09-01 (codified from 28 Aug sessions + Magic Tower board + Ivan Phase 30).

Status key: **LOCKED** = do not reopen without a new dated meeting. **OPEN** = still needs a human call.

---

## LOCKED

| ID | Decision | Source | Notes |
|---|---|---|---|
| DD-01 | Design meetings exist to set **departments, roles, agents** — not to run a 20-dept organigram. | Magic Tower objective; John 28 Aug | Long list preserved in `docs/CONVERSATION-NOTES-AND-LONG-DEPT-LIST.md` as history only |
| DD-02 | **Do not add more charter departments.** Six + board is the freeze. Run agents, not empty folders. | Weekly 28 Aug (John); Ivan Phase 30 commit `3ae8f67` | Matches John’s “you set up all departments but shouldn’t run them all yet” |
| DD-03 | Agents get **person names** for talk (Devin, Qualis, …). Formal ids stay in git. | John 28 Aug | Map: [`README.md`](README.md) |
| DD-04 | Agents communicate through **repos + messages**, not a single god-Hermes and not raw agent-to-agent chat. | John 28 Aug | Implemented later as router/intake (Phases 28–29) — implementation detail is the catalog |
| DD-05 | **Limit tools per department.** Product owner does not need a coding toolchain. | John 28 Aug | Whitelists exist (Phase 33); still audit that they match this rule |
| DD-06 | Ask **agents** for Ivan/Kiki status; do not make the other founder the router. | John 28 Aug | Analisa / management-coordinator first |
| DD-07 | **Conflicting roles on purpose.** Safina checks Devin. Qualis is QA. Do not merge safety and delivery QA. | John 28 Aug; Magic Tower | |
| DD-08 | **Sales funnel revival deferred to Q1 2027.** | Ivan D1=c, Phase 27 | Reopen only with a new decision, not in a Magic Tower session |
| DD-09 | **H6 credential-rotation automation deferred.** Key cycling is a later ops ritual unless a live leak forces it. | Phase 30; John 28 Aug (“half a year”) | PAT untrack `195e055` is a human GitHub task, not a new dept |
| DD-10 | Nexa does **not** get a parallel 6-dept org. Extend the existing layer. | `departments/NEXA-DEPARTMENT-SETUP-PLAN.md` | Do not use department-design meetings to clone Nexa |

---

## OPEN (must close in a dated session)

| ID | Question | Default until decided | Owner |
|---|---|---|---|
| DD-O1 | Who is the **human product owner**? | Unset. John’s #1 gap. | Ivan + Kiki |
| DD-O2 | PO as **Athena expansion** vs one new `product-owner` agent (still **not** a 7th charter dept)? | Unset | Ivan |
| DD-O3 | Written **product list** (in/out, audience, what sales may promise)? | Unset — do not market undefined SKUs | PO once named |
| DD-O4 | Freelancer content: Drive-only vs Hermes later? | Drive first (John: don’t dump Hermes on day one) | Kiki |
| DD-O5 | Reopen D1 funnel before Q1 2027? | No | Ivan |
| DD-O6 | Token-plan / credits for the 6 failing crons | Unset | Kiki + Ivan |
| DD-O7 | Confirm GitHub PAT rotation after `195e055` | Unset | Ivan |

---

## Explicitly rejected (do not put back on the board)

- A seventh live charter dept for Product, Marketing-standalone, CS, KM, or CoS before taxonomy triggers fire (`docs/demiurge/department-taxonomy-v1.md`).
- Treating “Rostercho” and Devin as two people.
- Using **MaxRina** as the canonical marketing name (use **Markina** / Calliope).
- Selling “buy this department” as an `aiw-org` design task (that is growth-coaching product work).
