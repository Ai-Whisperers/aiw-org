# DEMIURGE-113 Progress

Not started.

## 2026-09-03 update (autonomous session)

**Full inventory created** at `analysis/DEMIURGE-113-CRON-BREAKDOWN-2026-09-03.md`.

Key finding: the "79 dead crons" framing is outdated and oversimplified.
Real state as of 2026-09-03:
- 32 enabled+errored (not 79)
- 48 disabled (deliberate — Tier 1 audit)
- 7 path-blocked (self-healing from PR #18)
- 7 missing-sibling-dep (fixed by PR #20)

The "provider decision" was a placeholder. Actual decisions needed are
per-block (auth keys, litellm billing, arg-missing, script-not-found,
rate-limit). See breakdown doc for the 5-block split.

**Already shipped** (auto-fixable bulk):
- PR #18: 7 path-blocked crons (move scripts to /opt/data/scripts/)
- PR #20: 7 missing-dep crons (install_cron_script_deps.py)

**Awaiting Ivan** (operator-gated):
- Block A: 4 auth errors (Anthropic key)
- Block B: 1 litellm billing (Cerebras 402)
- Block C: 4 script-not-found
- Block D: 4 arg-error (intake-*, eval-gate-*)
- Block E: ~6 weekly rate-limit failures
