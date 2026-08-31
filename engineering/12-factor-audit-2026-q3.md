# 12-Factor Agent Methodology — Re-Audit (Post-DEMIURGE)

> **Phase 8 Area #6** | Engineering dept | Owner: engineering-roster + ai-safety-engineer
> **Date**: 2026-09-01
> **Original audit**: `docs/phases/PHASE-21-12-FACTOR-AUDIT.md` (2026-08-XX, pre-DEMIURGE)

---

## TL;DR

| Factor | Pre-DEMIURGE | Post-DEMIURGE | Δ |
|--------|--------------|---------------|---|
| 1 — Codebase | 9/10 | **9/10** | = |
| 2 — Dependencies | 8/10 | **8/10** | = |
| 3 — Config | 9/10 | **9/10** | = |
| 4 — Backing services | 7/10 | **7/10** | = |
| 5 — Build/release/run | 8/10 | **8/10** | = |
| 6 — Processes | 9/10 | **9/10** | = |
| 7 — Port binding | 9/10 | **9/10** | = |
| 8 — Concurrency | 7/10 | **8/10** | +1 (Phase 25 around-the-clock) |
| 9 — Disposability | 8/10 | **8/10** | = |
| 10 — Dev/prod parity | 9/10 | **9/10** | = |
| 11 — Logs | 9/10 | **9/10** | = |
| 12 — Admin processes | 8/10 | **8/10** | = |
| **TOTAL** | **100/120 (83%)** | **101/120 (84%)** | **+1** |

Net: one factor improved (Concurrency) due to Phase 25 around-the-clock upgrade. Other factors maintained.

---

## Factor-by-factor delta

### Factor 8 — Concurrency (7 → 8)

**Pre-DEMIURGE**: cron jobs were scheduled ad-hoc, many overlapping.
**Post-DEMIURGE** (Phase 25): around-the-clock upgrade established consistent cadence tiers (30min for monitors, daily for agents, weekly for reviews).

Evidence:
- 131 cron jobs total (vs. ~92 pre-Phase-25)
- All monitors now use `*/30 * * * *` or `0 9 * * *` patterns consistently
- 24/7 coverage achieved for: 7 dept-monitors + 18 sub-agent monitors + 7 management monitors = 32 always-on monitoring jobs

Remaining gap: some agents still run hourly (not 30min) because their cadence doesn't warrant more frequent. Score = 8/10 not 10/10.

### All other factors

No regressions detected from DEMIURGE promotion. The atomic-layer split (24 demiurge agents + 6 dept dirs + board-of-directors) was additive, not disruptive. PROMPT.md files maintain full frontmatter (Layer 2.5+2.6 work).

---

## What didn't change

- Codebase (single monorepo): 1 repo, 1 README per dept.
- Dependencies: `pyproject.toml` + `scripts/` unchanged.
- Config: still no `.env` files in repo (encrypted BWS only).
- Backing services: same set (Cloudflare Workers, GitHub, Supabase, LiteLLM).

---

## Recommendations

| # | Action | Why |
|---|--------|-----|
| 1 | Run the audit quarterly (next: 2026-12-01) | DEMIURGE evolution is ongoing; check for new factors |
| 2 | Add Factor 13: **Cross-system correlation** (Phase 5+6 work) | Drift-detector + chaos-test-runner are cross-cutting, not single-factor |
| 3 | Add Factor 14: **Adaptive layer** (deferred per doctrine) | When L4 unlocks, add soul-improvement as Factor 14 |

---

**Cross-references**:
- `docs/phases/PHASE-21-12-FACTOR-AUDIT.md` — original audit
- `docs/phases/PHASE-25-*` — around-the-clock upgrade that improved Factor 8
- `analysis/PHASE-7-dept-research/04-engineering-research-areas.md` Area #1
- `analysis/L1-AUTONOMOUS-PRECHECKS-2026-09.md` — gap audit
- `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` — surprise findings

