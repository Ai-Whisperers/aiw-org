# Circuit Breaker Wiring — Status

**Date:** 2026-09-03
**Context:** AIW token audit Tier 2 / Tier 3

## Current state

- `scripts/circuit_breaker.py` (203 lines) exists with cc-switch pattern
  - States: closed / open / half-open
  - Persisted to `/opt/data/state/circuit-breakers.json`
  - Threshold: 3 failures in 10-attempt window, 5-min cooldown
- Only **1 recipient** tracked: `r1` (not a provider, possibly a signal recipient)
- **Not wired into cron execution** — cron jobs retry-spam failures with no fallback

## What "wiring" would require

A wrapper at the cron executor level (~150 LOC):
```python
def execute_with_breaker(cron_job):
    provider = cron_job.get("provider", "minimax-oauth")
    state = get_state(provider)
    if state["state"] == "open":
        fallback = PROVIDER_FALLBACKS.get(provider)
        if fallback:
            cron_job["provider"] = fallback
        else:
            return {"skipped": True, "reason": "circuit open"}
    try:
        result = run_cron(cron_job)
        record_success(provider)
        return result
    except Exception as e:
        record_failure(provider, str(e))
        raise
```

Plus fallback map:
```python
PROVIDER_FALLBACKS = {
    "minimax-oauth": "litellm",   # 70 jobs
    "litellm": "minimax-oauth",   # 44 jobs (but litellm is broken — see model-probe.py)
}
```

## Empirical findings (model-probe.py, 2026-09-03)

| Alias | Resolves to | Status |
|---|---|---|
| `primary` | Cerebras | **HTTP 402 Payment Required** |
| `fast` | Nvidia NIM | **HTTP 410 Gone** |
| `reasoning` | Nvidia NIM | timeout |

This means:
- All 4 jobs with `model=primary` are currently failing (402)
- Any cron job routing to `fast` or `reasoning` is failing (410/timeout)
- The 70 jobs with `model=MiniMax-M3` (provider `minimax-oauth`) ARE working

## Why this work is deferred

The wiring itself is 4-6 hours of careful work on the Hermes gateway cron
executor. The fallback map is non-trivial because the current litellm
aliases are ALL broken — there's no working fallback for them. So the
implementation would need to either:
1. Disable all primary/fast/reasoning jobs until billing is fixed
2. Route them through minimax-oauth with a model translation

Either way, this requires an operator decision on the litellm billing
situation. Until that's resolved, wiring the breaker would just route
to more broken providers.

## Recommended next step

**Operator decision required** before breaker wiring:
1. Pay the Cerebras bill? (4 jobs resume)
2. Switch the 4 primary-model jobs to M3? (manual cron edit)
3. Disable those jobs entirely? (already partially done in Phase 9 R6)

## Files

- `/opt/data/agents/scripts/circuit_breaker.py` — exists, ready to wire
- `/opt/data/state/circuit-breakers.json` — only `r1` tracked
- `/opt/data/agents/scripts/model-probe.py` — empirical probe results
- `/opt/data/state/model-probe-result.json` — last probe results
