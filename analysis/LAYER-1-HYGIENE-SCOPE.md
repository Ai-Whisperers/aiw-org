# Layer 1 — Operational Hygiene — Scope

> **Status**: Ready for execution. Awaiting Ivan greenlight.
> **Owner**: AI (3-4h) + Ivan (2-3h operator actions)
> **Total time**: 5-7h
> **Reversibility**: Full — every action has a documented rollback

---

## Goal

Stop the bleeding. Close 5 P0 secret leaks, fix 3 high-severity incidents,
restart the dead wrangler process, capture baseline metrics. After Layer 1:
**zero known-broken things in the org.**

---

## Scope summary

| Task | Owner | Time | Doctrines applied |
|------|-------|------|-------------------|
| 1.1 Close 5 P0 secret leaks | Ivan | 75 min | Operator action — see runbook |
| 1.2 Fix `validator_e164_regression` (regex) | AI | 30 min | Doctrine 1: AI self-fixes |
| 1.3 Fix `validator_area_case_inversion` (case) | AI | 15 min | Doctrine 1: AI self-fixes |
| 1.4 Pin `mcp<2` to fix parking-storm | AI | 30 min | Doctrine 1: AI self-fixes |
| 1.5 Top up LiteLLM credits for Cerebras + Mistral | Ivan | 5 min | Operator action |
| 1.6 Restart `lead_worker_8787` wrangler process | AI | 30 min | Doctrine 1: AI self-fixes (wrangler is operator-toolable) |
| 1.7 Capture baseline metrics | AI | 60 min | Doctrine 1: AI self-fixes |
| 1.8 Update `REMAINING-TASKS-AND-WISHLIST.md` | AI | 15 min | Doctrine 1: AI self-fixes |
| 1.9 Write Layer 1 completion report | AI | 30 min | Doctrine 4 |
| 1.10 Verify all fixes (smoke gate) | AI | 30 min | Per Doctrine 2 |

**Total**: AI ~3-4h, Ivan ~1h45m (75+5 min + 15-30 min coordination).

---

## Task 1.1 — Close 5 P0 secret leaks

### Acceptance criteria
- [ ] Supabase service-role key rotated in Supabase dashboard
- [ ] New value written to BWS (only Ivan does this; AI does not touch BWS secrets)
- [ ] `ghp_u0Cs76…` PAT revoked in GitHub settings
- [ ] `ghp_Rfi9…` PAT revoked in GitHub settings
- [ ] `saskia-personal-context` repo visibility set to private
- [ ] All 16 R2 presigned URLs replaced in `rubicon-eas-website/worker.js` (Kiki's task, 2h)
- [ ] AI verification: no committed PAT prefixes in repo (per S5 audit script)

### Files affected
- Ivan-only: web console clicks
- AI: writes verification script, does NOT modify BWS or web consoles

### Rollback
- Per-action; documented in `LAYER-1-HYGIENE-RUNBOOK.md`

### Tokens to execute
~200 tokens for verification script

---

## Task 1.2 — Fix `validator_e164_regression`

### Problem statement
Per `state/engineering.json:incidents_72h`:
> `validator_e164_regression` — high severity — 5 ticks confirmed
> root_cause: `^\d{6,15}$` enforced instead of `^\+[1-9]\d{1,14}$`

### Acceptance criteria
- [ ] Regex updated to `^\+[1-9]\d{1,14}$` (E.164 international phone format)
- [ ] Tests added for E.164 validation (valid + invalid cases)
- [ ] Smoke test: at least 5 valid international numbers pass
- [ ] Smoke test: at least 5 invalid numbers fail
- [ ] Commit message references `validator_e164_regression` incident
- [ ] No new validation regressions (run full validator suite)

### Files affected
- The validator script (location TBD — AI finds it via grep)
- Test file for the validator

### Rollback
- `git revert <commit>`

### Tokens to execute
~500 tokens (find file + read context + write fix + tests + verify)

---

## Task 1.3 — Fix `validator_area_case_inversion`

### Problem statement
Per `state/engineering.json:incidents_72h`:
> `validator_area_case_inversion` — high severity — 1 tick confirmed
> root_cause: validator now lowercase-only (penal/civil); inverse of prior finding

### Acceptance criteria
- [ ] Root cause identified (which field, which file)
- [ ] Case-handling restored to original behavior
- [ ] Tests added for case sensitivity
- [ ] Smoke test: "Penal" and "penal" both accepted (or whatever the original intent was — verify with comment history)

### Files affected
- Same validator file (likely alongside 1.2)

### Rollback
- `git revert <commit>`

### Tokens to execute
~300 tokens (smaller scope than 1.2)

---

## Task 1.4 — Pin `mcp<2` to fix parking-storm

### Problem statement
Per `state/engineering.json:incidents_72h`:
> `mcp_parking_storm` — medium severity — fresh30_count: 138
> root_cause: mcp 2.x rename `mcp.server.fastmcp` → `mcp.server.mcpserver.MCPServer`; pin `mcp<2` to fix

### Acceptance criteria
- [ ] All `requirements.txt` files that pin `mcp` use `mcp<2`
- [ ] Smoke test: at least one cron job that depends on MCP runs without parking error
- [ ] 7-day observation: parking_storm count stays at 0

### Files affected
- All `requirements.txt` in aiw-org + dependent repos
- Possibly `pyproject.toml` if AIW uses Poetry

### Rollback
- `git revert <commit>`

### Tokens to execute
~400 tokens (find files + edit + verify)

---

## Task 1.5 — Top up LiteLLM credits

### Problem statement
Per `state/coord.json:open_stuck` and `state/engineering.json:incidents_72h`:
> `litellm_402_subs` — medium severity — events_today: 7
> root_cause: Cerebras + Mistral subscriptions lapsed; 5+ cron jobs erroring

### Acceptance criteria
- [ ] LiteLLM account topped up for Cerebras
- [ ] LiteLLM account topped up for Mistral
- [ ] AI verification: 0 HTTP 402 errors in last 24h after topup
- [ ] Cron jobs unblocked within 24h

### Files affected
- Web console only (Ivan)

### Rollback
- N/A (can't un-spend)

### Tokens to execute
~50 tokens (verification script)

---

## Task 1.6 — Restart `lead_worker_8787` wrangler

### Problem statement
Per `state/engineering.json:incidents_72h`:
> `lead_worker_8787_down` — high severity — ticks_open: 14
> root_cause: no wrangler process; operator restart required

### Acceptance criteria
- [ ] Wrangler process running (check via `ps` or systemd)
- [ ] Worker responds 200 to health check
- [ ] Lead intake resumes within 1h
- [ ] `state/sales.json:funnel_30d.leads` increments on next inbound

### Files affected
- Possibly a systemd unit file (if AI finds it)
- Possibly a deployment script

### Rollback
- Stop the wrangler; document the previous (broken) state

### Tokens to execute
~600 tokens (find wrangler config + restart + verify)

### Note
- Ivan decision required: **resurrect vs permanent-archive rubicon-eas**?
- Per `state/sales.json:open_questions`: "rubicon-eas project archived 2026-08-28"
- If Ivan says permanent archive: close the Worker, archive the code, remove from cron, **do not restart wrangler**
- If Ivan says resurrect: full restart + verify intake

---

## Task 1.7 — Capture baseline metrics

### Problem statement
Per gap analysis E1: no baseline metrics exist. We can't measure improvement without a "before" snapshot.

### Acceptance criteria
- [ ] Per-dept state file snapshot at T0 (this moment)
- [ ] Cost snapshot: `$/agent/day`, total daily/monthly
- [ ] Cron health snapshot: errors count, last-24h error list
- [ ] Incident snapshot: open + recent-resolved
- [ ] Brief delivery latency snapshot (last 7 days)
- [ ] Output file: `analysis/BASELINE-METRICS-2026-09-01.json` (or similar)
- [ ] Committed to master

### Files affected
- New file: `analysis/BASELINE-METRICS-2026-09.md`
- Possibly new dir: `state/baselines/2026-09-01/`

### Rollback
- File delete (it's a snapshot, not a change)

### Tokens to execute
~1K tokens (aggregate state files + format as JSON + commit)

---

## Task 1.8 — Update wishlist

### Acceptance criteria
- [ ] `analysis/REMAINING-TASKS-AND-WISHLIST.md` updated to mark:
  - Tasks 1-5 of Layer 1 (P0 leaks) as ✅ DONE
  - Incidents 1.2-1.4 (validators + MCP) as ✅ DONE
  - Task 1.5 (LiteLLM topup) as ✅ DONE
  - Task 1.6 (wrangler) per Ivan's decision
  - Task 1.7 (baseline) as ✅ DONE
- [ ] Any new tasks discovered during Layer 1 added to wishlist

### Files affected
- `analysis/REMAINING-TASKS-AND-WISHLIST.md`

### Rollback
- `git revert`

### Tokens to execute
~200 tokens

---

## Task 1.9 — Layer 1 completion report

### Acceptance criteria
- [ ] `analysis/LAYER-1-HYGIENE-COMPLETION-REPORT.md` written
- [ ] Contains:
  - What shipped (per-task completion status)
  - What didn't ship + why
  - Lessons learned (e.g. "AI self-fixed 4 of 5 tasks; operator action on P0 leaks was efficient")
  - Time spent per task
  - Time spent vs estimate (5-7h estimate, actual)
  - Discovered issues for Layer 2 or Layer 3
- [ ] Committed to master

### Files affected
- New file

### Rollback
- File delete

### Tokens to execute
~800 tokens

---

## Task 1.10 — Smoke gate (Layer 1 → Layer 2 transition)

### What this gate verifies
Before Layer 2 starts, ALL of these must be true:

- [ ] 0 high-severity incidents open (`state/engineering.json:incidents_72h[*].severity`)
- [ ] 0 medium-severity incidents open **OR** documented carry-forward to Layer 4
- [ ] 5 P0 leaks all closed (per Task 1.1 verification)
- [ ] LiteLLM credits topped up and stable for 24h
- [ ] Baseline metrics captured (per Task 1.7)
- [ ] `pre-commit` hook passes (cron-sync clean)
- [ ] `tests/` pass (run existing pytest suite)
- [ ] No untracked files committed (per `.gitignore` — even though it's currently broken, AI self-fixes this in Layer 2)

### Gate failure handling (per Doctrine 5)
- **Small failures** (e.g. one test fails, one incident is "mostly resolved"): AI fixes autonomously
- **Big failures** (e.g. P0 leak reverted by GitHub, wrangler won't restart): AI pauses and asks Ivan
- **Documentation**: AI writes a "Layer 1 gate failure report" before continuing

---

## Layer 1 exit criteria

Layer 1 is DONE when:

1. All 10 tasks above are completed (or documented as N/A with reason)
2. Smoke gate (Task 1.10) passes
3. `LAYER-1-HYGIENE-COMPLETION-REPORT.md` is committed
4. AI announces "Layer 1 complete" with commit hash
5. Ivan reviews the completion report and confirms greenlight for Layer 2

---

## Dependencies

- **None before Layer 1**: cleanest entry point
- **Layer 2 depends on Layer 1 baseline metrics** (Task 1.7) for pre/post comparison

---

## Risks specific to Layer 1

| Risk | Mitigation |
|------|------------|
| Ivan's P0 leak remediation gets interrupted | AI documents partial state; resumption is easy |
| Wrangler restart fails (config drift, missing deps) | AI diagnoses first; pauses for Ivan if not 5-min fix |
| Baseline metrics reveal MORE broken things | Add to Layer 2 or Layer 3 backlog; don't expand Layer 1 scope |
| AI self-fix breaks something else | Per-phase commit; per-task rollback; smoke gate catches before Layer 2 |

---

## Token budget

| Task | Estimate |
|------|----------|
| 1.1 | 200 (verification only) |
| 1.2 | 500 |
| 1.3 | 300 |
| 1.4 | 400 |
| 1.5 | 50 |
| 1.6 | 600 |
| 1.7 | 1000 |
| 1.8 | 200 |
| 1.9 | 800 |
| 1.10 | 500 |
| **TOTAL** | **~4,550 tokens** |

This is the budget. AI self-monitors and pauses if any single task exceeds
2x its estimate.

---

**Next**: `LAYER-1-HYGIENE-RUNBOOK.md` (step-by-step operator guide for Tasks 1.1, 1.5, 1.6's decision point).
**Awaiting**: Ivan's "go Layer 1" to start.