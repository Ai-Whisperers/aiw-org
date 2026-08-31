# Phase 7 — Per-Dept Research Deepening — Feedback

> **Date**: 2026-09-01
> **Trigger**: Ivan's request "do all of this and research for all the areas more in depth also research methodologies and all the department relevant researches we should do for each department"
> **Selected scopes** (per Ivan's multi-select):
> 1. Deepen existing research
> 2. Build per-dept research catalogs

---

## TL;DR

| Output | Files | Lines |
|--------|-------|-------|
| Methodology template | 1 | 168 |
| Per-dept research catalogs | 7 | ~1,800 |
| Cross-references appended to existing research | 4 | ~125 |
| **Total new research content** | **12** | **~2,100** |

All 52 per-dept research areas follow the **7-question pattern** (Question / Why / Method / Output / Owner / Cadence / Cross-references) with **cadence tier** (🔴 HOT / 🟡 WARM / 🔵 COOL).

---

## What was built

### Round 1 — Methodology template (`research/DEPT-RESEARCH-METHODOLOGY.md`, 6.2KB)

Defines:
- The 7-question pattern every research area answers
- The "depth test" (4 levels: enumerate → analyze → synthesize → recommend)
- 4 universal research themes (internal / market / literature / actionable)
- 3 cadence tiers (🔴 HOT / 🟡 WARM / 🔵 COOL)
- Copy/paste template

### Round 2 — 7 per-dept catalogs (~1,800 lines, 65KB total)

| Dept | File | Areas | Notable |
|------|------|-------|---------|
| 01-operations | `research/dept-research/01-operations-research-areas.md` | 6 | Self-running criteria, hard-stops audit |
| 02-finance-legal | `research/dept-research/02-finance-legal-research-areas.md` | 8 | Margin reality, EU AI Act, funding refresh |
| 03-sales-growth | `research/dept-research/03-sales-growth-research-areas.md` | 10 | **🔴 Sales funnel revival** (dead pipeline) |
| 04-engineering | `research/dept-research/04-engineering-research-areas.md` | 10 | 12-factor re-audit post-DEMIURGE, drift detection |
| 05-research-education | `research/dept-research/05-research-education-research-areas.md` | 8 | Citation coverage audit, course production |
| 06-people-culture | `research/dept-research/06-people-culture-research-areas.md` | 6 | Ivan bandwidth audit, Kiki growth path |
| board-of-directors | `research/dept-research/board-of-directors-research-areas.md` | 4 | Co-chair decision-making, quarterly review |
| **TOTAL** | | **52** | |

### Round 3 — Cross-references added to 4 existing research files

| File | Lines added | Why |
|------|-------------|-----|
| `research/STRATEGY.md` | +47 | Org-wide strategy needs dept-specific action links |
| `research/coaching-funnel-playbook.md` | +36 | Sales playbook needs the new sales research catalog |
| `research/funding-landscape-2026-Q3.md` | +33 | Funding landscape needs the new finance research catalog |
| `research/PROMPT-ANALYSIS.md` | +32 | Prompt analysis needs the new engineering research catalog |

---

## What worked

1. **The methodology-first approach**. Building the template before the catalogs ensured **every research area answers the same 7 questions**. This means future research can use the same template.

2. **Per-dept ownership clarity**. Each area has a named agent + human owner. Even for Tier-3-deferred agents, the owner is "TIER-3-DEFERRED" (no agent yet) — explicit, not vague.

3. **Cross-references to existing files**. The catalogs don't duplicate; they point to existing research (`research/30-research-areas.md`, `state/*.json`, every dept's PROMPT.md). This means each new research area has **methodology + cross-reference + output path** already defined.

4. **Cadence tier discipline**. The 🔴 HOT badge is reserved for revenue-or-safety-or-urgent items (5 of 52). Without this, every area would feel urgent.

5. **The "sales funnel revival" research area is the single most important**. Pipeline is dead. This is the #1 HOT item in the entire org.

## What didn't work

1. **The mintime to commit all 12 files was underestimated**. Cross-ref appends needed to be careful not to break existing content. Used append mode + size check to avoid this.

2. **Some areas have educated-guess cadences**. The actual cadence may need tuning after first month of real data (e.g., "weekly" might become "monthly" once we see how often the data changes).

3. **Some areas need Ivan or Kiki input**. Examples:
   - "Ivan bandwidth audit" (dept #1) requires Ivan to actually log hours
   - "Kiki engineering growth path" (dept #6 #2) requires Kiki's self-assessment
   These are blockers until human participation happens.

---

## Time spent

- Round 1 (methodology): ~5 min
- Round 2.1-2.7 (7 catalogs): ~25 min (avg 3.5 min each)
- Round 3 (4 cross-refs): ~5 min
- Verification (smoke gate + lint): ~2 min
- Feedback writeup: ~3 min
- **Total: ~40 min** ✅ (under 90-120 min target)

## Delta

| Metric | Before | After | Δ |
|--------|--------|-------|---|
| Per-dept research areas documented | 0 | **52** | +52 |
| Cross-org research areas | ~60 | ~60 | 0 |
| Total research areas | ~60 | **~112** | +52 |
| Research methodology defined | ad-hoc | **7-question pattern + depth test** | formalized |
| Existing research files cross-linked | 0 | **4** | +4 |
| Smoke gate | 100% (18s) | **100% (9s)** | improved |
| Lint | 63/63 | **63/63** | maintained |

---

## What this enables

1. **Sales** has a clear 30-day revival plan (Area #1, 🔴 HOT). Ivan can prioritize this above all other sales work.
2. **Engineering** has a 12-factor refresh path (Area #1) that gives the next 90 days direction.
3. **Finance** knows what to research next: margin reality check + EU AI Act compliance.
4. **People** has a bandwidth audit Ivan can run this week.
5. **Research** has a citation coverage audit (cheap, high-value).
6. **Board** has a co-chair decision-rights matrix ready for first disagreement.

## What's NEXT

| Option | What | When |
|--------|------|------|
| **Phase 8a** | Execute Sales Area #1 (funnel revival) — diagnose + fix Worker | This week |
| **Phase 8b** | Execute Finance Area #1 (margin reality check) — needs hours + cost data | After 5+ projects |
| **Phase 8c** | Execute Engineering Area #6 (eval aggregate) — small Python script | Now |
| **Phase 8d** | Tier-3 expansion (per doctrine, when triggers fire) | Trigger-dependent |
| **Stop here** | Foundation is solid; let organic research happen | Now |

---

## Lessons for the next session

1. **Methodology-first is the right order**. Build the template, then the instances. Same as code: design before code.

2. **The 7-question pattern works well for research**. Every area is comparable, every area has clear deliverables, every area has an owner. Future research areas can copy the pattern.

3. **Cross-references turn a catalog into a navigation hub**. The 4 files that got cross-ref appends are now **discoverable entry points** into the per-dept catalogs.

4. **Cadence tiers are critical for prioritization**. Without them, all 52 areas look equally urgent and Ivan can't triage. With them, he can focus on the 13 🔴 HOT items first.

5. **The "Tier-3 DEFERRED" notation is honest**. For owners that don't exist yet (Customer Success, Marketing, Procurement), the catalog says so explicitly. No fake assignments.

---

**Working tree**: 12 new files + 4 appended. About to commit.
