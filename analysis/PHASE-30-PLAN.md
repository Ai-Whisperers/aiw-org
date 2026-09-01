# Phase 30 — Eng + DevOps + AI Safety Scope Pivot

> **Date**: 2026-09-01
> **Trigger**: Ivan "i dont want to make any more departments for now i want to focus only on the develoment and on QA all of the internal software depts of a company all the engeneering deparmtnets only"
> **Decisions**: 1 c (eng+devops), 2 b (keep non-eng), 3 c (Tier G+H together), 4 c (keep research/edu), 5 c (keep sales/people/board)
> **Scope**: Tier G (eng quality) + Tier H (AI safety) from the 12-week plan

---

## What this means

### In scope (this phase)
- **Tier G**: Engineering quality work
  - G1: Eval aggregate cron wiring + 30d data (2h)
  - G2: Eval gate enforcement (4h)
  - G3: Hard-stops wrapper for ALL 60 destructive agents (16h) — **biggest safety hole**
  - G4: Self-validating heartbeat (4h)
  - G5: Auto-remediation for known errors (8h)
  - G6: Schema migration tooling (4h)
  - G7: Cost optimization (4h)

- **Tier H**: AI safety work
  - H1: Prompt injection detection on inbound (4h)
  - H2: PII redaction on outbound (4h)
  - H3: Action whitelisting — default-deny (8h)
  - H4: Audit trail review (4h)
  - H5: Red-team scenarios (4h)
  - H6: Credential rotation automation (4h)

### Out of scope (deferred, NOT deleted)
- Tier B: decision support (cost trend, eval trending)
- Tier C: business automation (sales, billing)
- Tier D: research/education work
- Tier E: people/culture work
- Tier F: board/governance work
- Tier I: user-facing features (website, customer dashboard)
- Tier J: analytics work

### Why this order
- G3 (hard-stops for 60 agents) is the biggest **current safety hole**
  - Only 3 of 63 PROMPTs declare hard_stops
  - Phase 27 fixed the wrapper to actually enforce, but 60 agents are unprotected
- H1 (prompt injection detection) is the biggest **inbound safety hole**
- G1 + G2 (eval data + enforcement) unblocks quality measurement for the whole org
- H2 + H3 (PII + whitelisting) close the biggest **outbound safety holes**

---

## Execution plan (this session: ~40 min for quick wins)

**Round 1** (~10 min): Tier G1+G4+G6 — quick infrastructure wins
- G1: Wire eval-aggregate cron nightly (already wired in Phase 26; verify + backfill)
- G4: Self-validating heartbeat cron
- G6: Schema migration tooling

**Round 2** (~15 min): Tier H1+H2 — inbound safety
- H1: Prompt injection detection on inbound
- H2: PII redaction on outbound

**Round 3** (~15 min): Tier G2+H4 — enforcement + audit
- G2: Eval gate enforcement (block low-pass agents)
- H4: Audit trail review cron

**Round 4**: Tier G3 (hard-stops for 60 agents) — biggest, defer to next session
**Round 5**: Tier G5+G7+H3+H5+H6 — defer to Phase 31

---

## Cross-references

- `analysis/GAP-ANALYSIS-2026-09-01.md` — Tier G + Tier H sections
- `analysis/BUG-HUNT-2026-09-01.md` — 31 bugs; Phase 28-29 fixed C/H items
- `analysis/PHASE-28-FEEDBACK.md` + `analysis/PHASE-29-FEEDBACK.md` — context
- `OPERATIONS.md` — Tier G/H items fit into the 5-layer model
- `04-engineering/` — Tier G target dept
- `patterns/hard-stop-wrapper.py` — G3 starting point (already functional)
- `scripts/eval-gate-enforce.py` — G2 starting point (already functional)
