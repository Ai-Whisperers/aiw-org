# Layer 1 — Operational Hygiene — Completion Report

> **Status**: PARTIAL — operator parts pending Ivan; autonomous parts DONE; baseline captured.
> **Date**: 2026-09-01
> **AI hours spent**: ~2h autonomous execution
> **Ivan hours required**: ~3h operator work (P0 leaks + LiteLLM topup + wrangler decision)

---

## TL;DR

| Task | Status | Owner | Notes |
|------|--------|-------|-------|
| 1.1 Close 5 P0 secret leaks | ⏳ PENDING | Ivan | Runbook Batch A — web console actions |
| 1.2 Fix `validator_e164_regression` | ✅ DONE | AI | **STALE INCIDENT** — code already had correct regex `^\+[1-9]\d{1,14}$` in `templates/legal-lead-worker/api/lead-worker.js` |
| 1.3 Fix `validator_area_case_inversion` | ✅ DONE | AI | **STALE INCIDENT** — code already uses `.toLowerCase().trim()` |
| 1.4 Pin `mcp<2` | ✅ DONE | AI | **STALE INCIDENT** — `hermes-agent/pyproject.toml` already pins `mcp==1.28.1` (effectively `<2`) |
| 1.5 Top up LiteLLM credits | ⏳ PENDING | Ivan | 5-min web console action |
| 1.6 Restart wrangler process | ⏸ AWAITING IVAN | AI pending decision | Worker is dead; validator code fixed but Worker process not running |
| 1.7 Capture baseline metrics | ✅ DONE | AI | `analysis/BASELINE-METRICS-2026-09-01.json` |
| 1.8 Update wishlist | ✅ DONE | AI | `analysis/REMAINING-TASKS-AND-WISHLIST.md` updated |
| 1.9 Write completion report | ✅ DONE | AI | This file |
| 1.10 Smoke gate | ✅ DONE | AI | All 13 state files validate; pytest runs via /opt/data/.venv/ |

**Plus**: 4/5 `.env` files chmod'd to 600 (1 needs root sudo).

---

## What AI did autonomously (Doctrine 1: AI self-fixes)

### Closed 3 stale incidents
Per `state/engineering.json` updates:

- `validator_e164_regression` — **stale**. Code in `/opt/data/templates/legal-lead-worker/api/lead-worker.js` already has `^\+[1-9]\d{1,14}$` per REGRESSION GUARD comment. Incident closed.
- `validator_area_case_inversion` — **stale**. Code uses `.toLowerCase().trim()`. Incident closed.
- `mcp_parking_storm` — **stale**. `hermes-agent/pyproject.toml` pins `mcp==1.28.1` already. Incident closed.

### Captured baseline metrics
- File: `analysis/BASELINE-METRICS-2026-09-01.json` (1609b)
- Includes: cost, incidents, cron, sales, p0_leaks, security

### Fixed file permissions
- `/opt/data/.env`: 644 → 600
- `/opt/data/profiles/engineering/.env`: 644 → 600
- `/opt/data/work/research-repos/paragu-ai-builder/.env`: 644 → 600
- `/opt/data/scratchpad/round3-backup/.env`: 644 → 600
- `/opt/data/.hermes/.env`: SKIPPED (owned by root, needs operator sudo)

### Updated state files (live, not in git)
- `state/engineering.json`: 3 incidents closed with AI auto-notes
- `state/coord.json`: appended wrangler note (awaiting Ivan decision)
- `analysis/REMAINING-TASKS-AND-WISHLIST.md`: added Layer 1 update section

### Verified state schema validity
- All 13 state files validate per `scripts/validate-state.py`

---

## What Ivan needs to do (operator work)

### Batch A — 5 P0 secret leaks (75 min)
Per `LAYER-1-HYGIENE-RUNBOOK.md`:

1. **Supabase service-role rotate** (5 min): the leak is in `work/research-repos/paragu-ai-builder/.env` (confirmed via Q4 audit). Tell AI the new value is in BWS so AI can update the BWS secret.
2. **Revoke `ghp_u0Cs76…` PAT** (1 min): GitHub Settings → Tokens → Delete
3. **Revoke `ghp_Rfi9…` PAT** (1 min): same
4. **`saskia-personal-context` → private** (5 min): GitHub Settings → Danger Zone
5. **Replace 16 R2 presigned URLs in `rubicon-eas-website/worker.js`** (2h, Kiki): per `REMAINING-TASKS-AND-WISHLIST.md`

### Batch B — LiteLLM topup (5 min)
Cerebras + Mistral subscriptions lapsed (5+ cron jobs down). Add $50-100 to LiteLLM billing. Tell AI when done.

### Batch C — Wrangler decision (5 min)
Choose:
- **(a) RESURRECT** — AI restarts wrangler + revives WEBHOOK_URL secret
- **(b) PERMANENT ARCHIVE** — AI marks rubicon-eas Worker as archived; closes `lead_worker_8787_down` incident
- **(c) DEFER** to Layer 4 (or beyond) — incident remains open

### Bonus — One chmod AI can't do
```
sudo chmod 600 /opt/data/.hermes/.env
```
(15 sec; AI lacks root)

---

## Baseline metrics snapshot

```
cost:        $9.79/day, $293.41/month, 49 agents
incidents:   3 closed by AI; 3 still open (lead_worker, litellm_402, wa_real_group_silence)
cron:        24 cron errors, 6 open_stuck items
sales:       $240 MRR, 1 customer (rubicon-eas, archived), 0 leads in pipeline
funnel_30d:  leads=0, calls=0, proposals=0, contracts=0
```

Per-department KPIs not yet defined (Layer 2 deliverable).

---

## What was NOT done (Doctrine 5: pause for big decisions)

- Task 1.6 wrangler restart — waiting for Ivan's decision (a/b/c above)
- Task 1.5 LiteLLM topup — operator-only action (Ivan)
- Task 1.1.1-1.1.5 P0 leaks — operator-only (Ivan, Batch A)
- 5th `.env` chmod — needs root (Ivan, sudo)

---

## Risks remaining after Layer 1

| Risk | Severity | Mitigation |
|------|----------|------------|
| P0 leaks remain (operator action pending) | High | Runbook Batch A; ~75 min |
| LiteLLM credits lapsed | Medium | Batch B; 5 min |
| Wrangler dead | High | Batch C decision; 5 min + 30 min AI exec |
| State files have gitignore bug (untracked despite policy) | Low | Layer 2 scope (`EXECUTION-SCOPE §2`) |
| Hard-stops wrapper not invoked | Low | Layer 3 scope |

---

## Time accounting

| Activity | AI | Ivan |
|----------|----|----|
| Search for validator/MCP/.env | 30 min | 0 |
| Read + verify code correctness | 15 min | 0 |
| Close stale incidents | 5 min | 0 |
| Update state files | 5 min | 0 |
| chmod .env files | 5 min | 0 |
| Capture baseline metrics | 10 min | 0 |
| Update wishlist | 5 min | 0 |
| Write completion report | 15 min | 0 |
| Write baseline JSON | 5 min | 0 |
| **AI total** | **~1.5h** | — |
| **Ivan total (pending)** | — | **~3h** (P0 leaks + LiteLLM + wrangler decision + sudo chmod) |

---

## Layer 1 → Layer 2 transition

Layer 1 is "complete" per the AI's part of the scope. **Layer 2 cannot start until:**

1. ✅ All5 P0 leaks closed (Ivan, Batch A)
2. ✅ LiteLLM credits topped up + stable 24h (Ivan, Batch B)
3. ✅ Wrangler decision made (Ivan, Batch C)
4. ✅ Sudo chmod done (Ivan, 15 sec)
5. **Optional**: rubicon-eas Worker back online (if Ivan chose resurrect)

Once all 4 are DONE, Ivan says "Layer 2 go" and AI writes `LAYER-2-FOUNDATION-SCOPE.md` per Doctrine 2 (per-layer scope docs before layer starts).

---

**Awaiting Ivan's 4 Batch actions + decision (a/b/c for wrangler).**

**AI is PAUSED for operator actions. Will resume when operator parts complete.**
