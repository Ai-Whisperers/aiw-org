# Thesis Defense Prep — Master Timeline

> **Built 2026-09-01** — Phase 7 R6 (methodology docs).
>
> **Purpose**: Standardized timeline for thesis defense preparation. AIW's
> GeoData v2 thesis needs this. Used by `thesis-tracker` + Ivan.

---

## Master timeline (6-month pre-defense)

| Month | Phase | Activities | Deliverable |
|---|---|---|---|
| **T-6mo** | **Scope finalization** | Final research questions, hypotheses, scope document | Signed scope (Ivan + Kiki) |
| **T-6mo** | **Reading list lock** | 50-80 papers, organized into themes | Annotated bibliography |
| **T-5mo** | **Methodology chapter** | Draft chapter 3 (methods) | Chapter 3 draft |
| **T-4mo** | **Results chapter** | Run experiments, collect data | Chapter 4 draft + raw data |
| **T-4mo** | **Discussion chapter** | Interpret results, address research questions | Chapter 5 draft |
| **T-3mo** | **Full draft** | Integrate all chapters, intro + conclusion | Complete draft (v1) |
| **T-3mo** | **Internal review (round 1)** | Kiki + 1 external reader review | Annotated v1 |
| **T-2mo** | **Revision #1** | Address major feedback, restructure if needed | v2 draft |
| **T-2mo** | **Internal review (round 2)** | Kiki + 2 external readers | Annotated v2 |
| **T-2mo** | **Citation audit** | Run `citation-coverage-enforcer`, target 90%+ | Coverage report |
| **T-1mo** | **Final revision** | Address remaining feedback, polish prose | v3 (camera-ready) |
| **T-1mo** | **Defense slides** | 20-25 slides, 20-min talk + 10-min Q&A | Slides v1 |
| **T-1mo** | **Mock defense #1** | Kiki plays adversarial examiner | Feedback + revise |
| **T-3wk** | **Mock defense #2** | External advisor plays examiner | Final polish |
| **T-2wk** | **Defense package** | Final thesis PDF + slides + abstract | Submission to committee |
| **T-2wk** | **Pre-defense checklist** | Verify formatting, citations, references | Checklist signed |
| **T-1wk** | **Final rehearsal** | Full talk, timed, Q&A practice | Confidence |
| **T-0** | **DEFENSE DAY** | 60-90 min presentation + Q&A | **DEFENDED** |

---

## Defense format (60-90 min)

| Phase | Duration | Content |
|---|---|---|
| Opening | 2 min | Title, committee, gratitude |
| Motivation | 5 min | Problem + why it matters |
| Background | 5 min | Prior work, gap |
| Research questions | 3 min | What you investigated |
| Methods | 8 min | How you investigated |
| Results | 15 min | Key findings (3-5) |
| Discussion | 10 min | Implications + limitations |
| Conclusions | 3 min | What we learned |
| Q&A | 20-30 min | Committee + audience questions |
| Closing | 2 min | Acknowledgments |

---

## Defense committee (3-5 members)

| Role | Profile | AIW context |
|---|---|---|
| **Chair** | Senior researcher in field | External academic |
| **Internal examiner** | Methodology expert | Kiki or external |
| **External examiner** | Field expert (different institution) | External academic |
| **Optional 2nd external** | Statistics or methods expert | External |
| **Optional industry** | Practitioner perspective | Industry contact |

---

## Common defense pitfalls (avoid)

- ❌ **Defending too hard** — "I was right" loses; "I learned X" wins
- ❌ **Skipping limitations** — Every study has them; own them upfront
- ❌ **Reading slides** — Slides are headlines; speak to them
- ❌ **Going over time** — Practice 3x; 20 min talk = 18 min actual
- ❌ **Burying the contribution** — Lead with "what's new", not literature review

---

## Pre-defense checklist (T-2wk)

- [ ] Thesis PDF compiles cleanly on 3 machines (Mac/Windows/Linux)
- [ ] All citations resolve (no broken refs)
- [ ] All figures have alt text
- [ ] Plagiarism check passes (Turnitin < 10% match)
- [ ] Defense slides exported as PDF (no font issues)
- [ ] Backup thesis copy on 2 USB drives + cloud
- [ ] Committee received final thesis 2 weeks before defense
- [ ] 5 hardcopies printed (committee + library + backup)
- [ ] 30-min talk practiced 3x with timer
- [ ] Q&A prep: 20 likely questions answered

---

## Post-defense (T+0 to T+1mo)

| Phase | Activity |
|---|---|
| T+0 | Thank committee, accept feedback gracefully |
| T+1wk | Receive committee's written feedback |
| T+2wk | Final corrections, sign-off |
| T+3wk | Submit final corrected thesis to library |
| T+1mo | Deposit in institutional repository, update CV |
| T+3mo | First journal submission (per academic-liaison agent) |

---

## AIW-specific notes (GeoData v2)

- **Target date**: TBD (per `state/research.json` `target_date`)
- **Committee**: Kiki + 2 external (TBD by Ivan)
- **Special considerations**:
  - LATAM geographic focus needs validation
  - Bilingual (Spanish/English) terminology matters
  - Data sovereignty (Paraguayan datasets)

---

## Agent handoff

When defense is scheduled:

1. `thesis-tracker` updates `state/research.json` with `defense_date`
2. `editorial-calendar.py` adds defense milestone
3. `research-tracker` adds to weekly brief: "T-N weeks to defense"
4. At T-1mo: trigger mock defense scheduling

---

## Version history

- v0.1.0 (2026-09-01): Initial timeline

**Owner**: thesis-tracker
**Review cadence**: per-thesis
**Last reviewed**: 2026-09-01

---

## Sources & Standards

This runbook draws on:

- **Council of Graduate Schools (US), *Professional Development & Mentoring of Doctoral Students*** (2018). <https://cgsnet.org/resources/>
- **UNAM Reglamento General de Estudios de Posgrado** (2018) — Mexican graduate-program defense norms applied to FPUNA context.
- **Phillips & Pugh (2015), *How to Get a PhD* (6th ed.), Open University Press**, ch. 9 (the viva). ISBN 978-0-335-26467-2.
- **Bastalich, W. (2017), *Re-thinking Doctoral Education*, in: *The Routledge Companion to Higher Education Research* — framework for viva preparation as identity work.