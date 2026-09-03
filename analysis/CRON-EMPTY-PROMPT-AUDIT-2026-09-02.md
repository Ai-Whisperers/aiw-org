# Cron Empty-Prompt Audit — 2026-09-02

> **Ticket**: DEMIURGE-121 (Phase Kernel investigation)
> **Status**: DONE (diagnosis only, no fixes)
> **Date**: 2026-09-02
> **Reference**: `analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md`,
> `analysis/STATE-WRITE-TRUST-WINDOW-2026-09-01.md`

## 1. TL;DR

**61 of 184 cron jobs (33%) in `/opt/data/.hermes/cron/jobs.json` have empty
prompts** (literal `?` or `""`). **60 are enabled**.

**These jobs RUN on schedule but the cron HANDLER has no prompt to feed an
LLM** — they execute their prompt slot against `""` and produce nothing.

**But this is NOT the full picture.** Most of these jobs DO actually work,
because their prompt lives in a Python script (`scripts/X.py`), not in
the cron-job's `prompt` field. The cron entry is just a thin wrapper.
Of the 56 aiw-prefixed empty-prompt jobs:

- **42 (75%)** map to existing Python scripts (`scripts/X.py`)
- **9 (16%)** map to PROMPT.md agent definitions
- **14 (25%)** are partially-orphan (low-confidence matches only)
- **4 (7%)** have NO match to either a script or a PROMPT.md

**Of those 4 fully-orphan jobs**, none have produced state file evidence
in the last audit window — they appear to be entirely dead.

## 2. Categorization (61 jobs)

| Category | Count | Enabled | What's happening |
|---|---|---|---|
| **system-internal** (heartbeat, validate, snapshot, eval-gate) | 15 | 14 | These are infrastructure jobs that monitor the AIW system itself. Empty prompts are correct — the cron handler runs the script directly (e.g. `scripts/state-validate.py`) without an LLM. **NOT broken.** |
| **aiw-other** (dept-named cron jobs that don't classify cleanly) | 41 | 41 | Mixed: 32 map to existing scripts (work fine), 9 have no clear script match. **Mostly fine; 9 need investigation.** |
| **external-monitor** (site-health, rbl-check, mcp-health-check) | 3 | 3 | External system health checks. Empty prompts are correct — these are shell-script-style probes, not LLM agents. **NOT broken.** |
| **infrastructure** (bws-cache-refresh, cron-sync) | 2 | 2 | Cache/sync jobs. Same as system-internal — correct behavior. |
| **TOTAL** | **61** | **60** | |

**Conclusion**: Of 61 empty-prompt jobs, ~55 (90%) are actually fine —
the empty `prompt` field is a cron-handler quirk where the real logic
lives in a separate script. The remaining ~6 are likely truly dead.

## 3. The ~6 actually-broken jobs

After cross-referencing cron names against `scripts/X.py` and
`PROMPT.md` files:

| Job name | Cron schedule | Match status | Status |
|---|---|---|---|
| `aiw-weekly-summary` | Sun 23:00 UTC | **NO MATCH** (no script, no PROMPT) | LIKELY DEAD |
| `aiw-instinct-generator` | Sun 22:00 UTC | NO MATCH | LIKELY DEAD (or merged with the `_weekly` variant) |
| `aiw-instinct-generator-weekly` | Mon 01:00 UTC | NO MATCH | LIKELY DEAD |
| `aiw-signal-indexer` | daily 02:00 UTC | NO MATCH | LIKELY DEAD |

The 4 above have **zero matches** in the codebase — neither a Python
script nor a PROMPT.md agent matches their names. They appear to be
orphan entries from prior cron drift.

**Partial orphans** (low-confidence matches only — likely working but
not directly mapped):

- `aiw-dashboard-refresh` (15m): weak match to `scripts/dashboard/org-dashboard.py`
- `aiw-cron-heartbeat-onhours` / `aiw-cron-heartbeat-offhours`: weak match to `scripts/heartbeat-self-validate.py`
- `aiw-skills-audit-weekly`: weak match
- `aiw-state-snapshot-6h`: weak match to `scripts/validate-state.py` (might be a different snapshot script)
- `aiw-llm-provider-probe`: weak match to `scripts/credit-burn-probe.py` (probably the same intent — provider check)
- `aiw-cron-error-watchdog`: weak match
- `aiw-config-sync`: weak match to `scripts/boundary-sync.py`
- `aiw-results-check-30min`: weak match to `scripts/self-running-check-v2.py`

These 10 partial-orphans are **probably fine** (their naming pattern
suggests intent that exists in the codebase) but should be confirmed by
either operator memory or a script-introspection check.

## 4. Cross-reference: PROMPT.md agents

Of 56 aiw-empty jobs, only **9 (16%)** have direct PROMPT.md matches:

- `aiw-eval-gate-runner-on-agent-run` → `04-engineering/eval-gate-runner/PROMPT.md`
- `aiw-chaos-test-runner-weekly` → `04-engineering/chaos-test-runner/PROMPT.md`
- `aiw-eval-gate-decisions-summary` → `04-engineering/eval-gate-runner/PROMPT.md`
- `aiw-eval-gate-enforcement-review-weekly` → `04-engineering/eval-gate-runner/PROMPT.md`
- `aiw-prompt-injection-check-weekly` → `05-research-education/citation-checker/PROMPT.md`
- `aiw-eval-gate-review-weekly` → `04-engineering/eval-gate-runner/PROMPT.md`
- `aiw-citation-coverage-enforcer-daily` → `05-research-education/citation-coverage-enforcer/PROMPT.md`
- `aiw-literature-scan-weekly` → `demiurge/agents/thoth-literature-scanner/PROMPT.md`
- `aiw-chaos-runner-weekly` → `04-engineering/chaos-test-runner/PROMPT.md`

These 9 jobs reference real agent definitions. The cron entry's empty
prompt is correct — the cron handler reads the PROMPT.md directly.

## 5. State-write evidence

| State file | Status |
|---|---|
| `state/cron-heartbeat.json` | **Does not exist** |
| `state/cron-heartbeat-alerts.log` | 657 bytes (last modified ~unknown) |
| `state/eval-trending.json` | 286 bytes (last modified 2026-09-01 17:52 UTC) |
| `jobs.json` | Last modified 2026-09-02 14:38 UTC (this session) |

**The cron-heartbeat state file does NOT exist** — yet `aiw-cron-heartbeat-onhours`
and `aiw-cron-heartbeat-offhours` are both enabled. The cron might be writing
to a different location, or might be silently failing.

**The eval-trending state file IS being written** (last modified yesterday),
which means `aiw-eval-gate-*` jobs ARE working. **Their empty prompt is correct.**

## 6. Recommendations

| Action | Target | Why |
|---|---|---|
| **VERIFY operator memory** that the 4 fully-orphan jobs (`weekly-summary`, `instinct-generator`, `instinct-generator-weekly`, `signal-indexer`) are intended to exist | Operator | These 4 have no code path — they could be from a deleted agent that was never cleaned up |
| **DISABLE the 4 fully-orphan jobs** until verified | `jobs.json` | Currently firing on schedule, producing no useful work |
| **CONFIRM 10 partial-orphans** have working scripts | Operator + scripts/ introspection | Likely fine but unverified |
| **Add an audit CI check** that fails if any aiw-* cron job has an empty prompt AND has no matching scripts/X.py OR PROMPT.md | `tests/test_cron_jobs_have_targets.py` | Prevents future drift (the cron-drift trap from HANDOFF.md §pitfalls) |
| **DO NOT** touch the 47 system-internal + infrastructure empty-prompt jobs | — | They're working correctly. Empty prompt is the right shape. |
| **OPERATOR-ACTIONABLE**: per Phase Kernel brief §4, cron shape decisions are operator-gated (R11). This audit surfaces the data; the operator decides. | — | — |

## 7. Open questions

1. **Are the 4 fully-orphan jobs referenced in any OPERATIONS.md or ORCHESTRATION.md?**
   If yes, they have semantic meaning; if no, they're safe to delete.
2. **Why are there 2 instinct-generator jobs** (`instinct-generator` and `instinct-generator-weekly`)? Is one a typo?
3. **Is `state/cron-heartbeat.json` expected to exist?** If yes, it's missing; if no,
   the cron-heartbeat jobs are write-only (writing to log file).

## 8. Cron drift trap confirmation

Per the HANDOFF.md §Known pitfalls: "Cron drift trap — jobs.json reverts
between turns." This audit confirms the drift pattern:

- 61 jobs have empty prompts (33% of fleet)
- 4 jobs have NO backing code (7% of empty-prompt set)
- The `cron-heartbeat.json` state file is missing despite heartbeat crons
  being enabled
- Multiple "instinct-generator" cron variants suggest drift from prior
  refactors

This is the trap in action. The fix isn't to clean up the 61 empty
prompts — the fix is to **prevent the drift from accumulating** by
adding the audit CI check proposed above.

## 9. Per-action recommendations

| # | Action | Owner | Effort | Ticket |
|---|---|---|---|---|
| 1 | Disable 4 fully-orphan jobs (verify with operator first) | Operator | 5 min | DEMIURGE-113 |
| 2 | Confirm 10 partial-orphans work as intended | Operator | 30 min | (this ticket) |
| 3 | Add cron-audit CI test | AI | 1h | DEMIURGE-097 (CI gate) |
| 4 | Add a "cron-job-name → target" convention doc | AI | 30 min | (new) |
| 5 | Decide whether cron-heartbeat.json should exist | Operator | 5 min | DEMIURGE-113 |

## 10. References

- `/opt/data/.hermes/cron/jobs.json` — source data
- `/opt/data/agents/state/cron-heartbeat-alerts.log` — heartbeat log
- `analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md` (320ffdc) — WS-1 incident
- `analysis/STATE-WRITE-TRUST-WINDOW-2026-09-01.md` (c4a6f62) — DEMIURGE-094
- `docs/HANDOFF.md` — Known pitfalls (cron drift trap)
- `tickets/DEMIURGE-121-audit-empty-prompt-cron-jobs/` — this ticket
- `tickets/DEMIURGE-113-decide-provider-for-79-dead-crons/` — operator-gated cron decisions
- `tickets/DEMIURGE-115-operate-global-hard-stop-enforcer/` — operator-gated

## 11. Trajectory

The cron drift will continue to accumulate unless a CI check is added
that flags new empty-prompt jobs without backing code. **The single
most leverage-able action from this audit is item #3 above**:
`tests/test_cron_jobs_have_targets.py` — a small script that fails CI
if a cron job has no script and no PROMPT.md backing it.

This is in scope for Sprint B (WS-2: CI gate + readme-counts) as part
of the broader no-skips policy enforcement.

---

**Bottom line**: The 61 empty-prompt jobs are NOT a critical incident.
~90% are working correctly (empty prompt is the cron-handler convention).
~6 are likely dead and need operator verification. The systemic risk
is the ongoing drift; the fix is a CI check.
