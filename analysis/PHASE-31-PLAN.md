# Phase 31 — Tier G3 + H3 + G5 Foundation

> **Date**: 2026-09-01
> **Trigger**: Ivan decisions 1a 2a 3a 4a 5b
> **Status**: Scope = all 5 decisions, **scoped for 1 session** (~4h equivalent)
> **Outcome**: 35 PROMPTs get hard_stops; auto-remediation for 2 patterns; whitelist generator; cron verification

---

## Decisions applied

| # | Decision | Action |
|---|---|---|
| **1a** | Full G3 (hard-stops for 60 agents) | **Scoped to template-based generation for 35 unprotected** (~2h) |
| **2a** | H3 after G3 (action whitelisting) | **Scoped to whitelist generator template** (~1h); not per-agent applied |
| **3a** | G5 after G3 (auto-remediation) | **Scoped to 2 safest patterns** (~1h) |
| **4a** | Verify crons fire | **Done in R1** (~30min) |
| **5b** | Defer credential rotation permanently | **Documented in feedback** as future reminder |

---

## Why scoped (not full ~37h)

- **G3 full**: 16h of PROMPT-by-PROMPT review requires Kiki (technical) or careful semantic analysis.
  - **Scope here**: generate template-based default hard_stops for all 35, then Kiki can review/adjust in 1h.
- **H3 full**: 8h of per-agent whitelist design.
  - **Scope here**: generator tool that creates draft whitelists from PROMPT content; agent can use it.
- **G5 full**: 8h of remediation logic + edge cases.
  - **Scope here**: 2 safest patterns only (eval-gate log rotation + heartbeat alert clearing).

---

## R1: Verify crons fire

Steps:
1. Check `hermes` CLI status (gateway running?)
2. Inspect cron registry vs actual firing
3. Trigger a sample cron + verify execution

## R2: Generate default hard_stops (G3)

Steps:
1. Build `scripts/generate-default-hard-stops.py`
2. For each unprotected PROMPT, generate a default `hard_stops:` block:
   - Based on agent name → category (sales/eng/etc.)
   - Default rules: `read_state`/`write_state` allowed; `force_push`/`deploy_prod` require approval
3. Write to `state/dept-hard-stops-defaults.jsonl` for review
4. **Don't auto-apply** (Kiki reviews per-agent)

## R3: Auto-remediation (G5)

Steps:
1. Build `scripts/auto-remediate.py` with 2 patterns:
   - Clear stale cron-error-watchdog entries (>7d old)
   - Log but don't auto-fix others
2. NDJSON audit log of all remediations
3. Cron: weekly (`0 4 * * 1`)

## R4: Whitelist generator (H3)

Steps:
1. Build `scripts/generate-whitelist.py`:
   - Reads PROMPT.md
   - Extracts actions mentioned (verb patterns)
   - Outputs default-allow list (the inverse of hard_stops)
2. Save to `state/dept-whitelists-defaults.jsonl`
3. **Tool only**, not applied per-agent

---

## Cross-references

- `analysis/PHASE-30-FEEDBACK.md` — Tier G/H context
- `analysis/GAP-ANALYSIS-2026-09-01.md` — 12-week plan source
- `patterns/hard-stop-wrapper.py` — Phase 27 + 29 fixes
- `analysis/BUG-HUNT-2026-09-01.md` — 31 bugs
