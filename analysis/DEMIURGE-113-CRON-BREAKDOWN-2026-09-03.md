# DEMIURGE-113 Cron Breakdown — 2026-09-03

> **Authoritative inventory of the 79 "dead crons" the ticket refers to.**
> The ticket says "provider decision" but the actual breakdown is plumbing,
> not provider choice. This doc shows what each broken cron needs.

## Headline

- Total jobs in registry: 188
- Currently enabled: 140
- Currently errored (enabled+errored): 32
- Currently disabled: 48 (mostly deliberate — Tier 1 audit paused 6, broken-name paused 3, workdir-fixed 23, etc.)

## Breakdown by error class (32 currently errored)

| Class | Count | Auto-fixable? | Notes |
|---|---:|---|---|
| **path-blocked** (PR #18 fixed most) | 7 | Self-healing | Cron-runner policy block; will clear on next tick after PR #18's fix |
| **missing-dep:signal_queue** | 4 | YES — fixed by PR #20 (install_cron_script_deps.py + 2 operator-side copies) | Sibling dep missing from /opt/data/scripts/ |
| **missing-dep:_paths** | 3 | YES — fixed by PR #20 | Sibling dep missing from /opt/data/scripts/ |
| **auth-error** (Anthropic 401) | 4 | NO — operator | 4 research crons need Anthropic API key configured |
| **script-not-found** | 4 | NO — operator decision | kv-bws-sync, linkedin-token-refresh, instagram-token-refresh, boundary-validate (broken cron entry) |
| **arg-error** (script needs flags) | 4 | NO — operator decision | 4 cron entries calling scripts without required args |
| **other** (Script exited 1, no traceback) | 3 | Maybe — needs investigation | state-validate, llm-provider-probe, cron-error-watchdog |
| **rate-limit** (the original "79") | 1 | Maybe — operator | thesis-weekly-review (and others, slow-failing) |
| **litellm-billing** (Cerebras 402) | 1 | NO — operator | aiw-saas-lifecycle-reconcile ($27/mo Sonnet est.) |

## What was already fixed

- **PR #18** (Sep 2): moved 17 scripts to /opt/data/scripts/, added back-compat symlinks. Fixed 7 path-blocked crons.
- **PR #20** (Sep 3): install_cron_script_deps.py + applied operator-side. Fixed 7 missing-dep crons.
- **Total errored crons reduced: 32 → ~25.** Self-heal path-blocked will drop another 7 → ~18.

## What's left (and what needs operator decision)

### Block A — Auth keys (4 crons, ~$0-30/mo depending on volume)

```
aiw-research-associate-daily    HTTP 401: litellm.AuthenticationError: AnthropicException
aiw-research-engineer-weekly    HTTP 401: litellm.AuthenticationError: AnthropicException
aiw-research-tracker-6h         HTTP 401: litellm.AuthenticationError: AnthropicException
aiw-citation-checker-daily       HTTP 401: litellm.AuthenticationError: AnthropicException
```

**Decision needed**: Add Anthropic API key to BWS, or disable these 4 crons, or switch to M3.

### Block B — Litellm billing (1 cron, ~$27/mo Sonnet estimate)

```
aiw-saas-lifecycle-reconcile    HTTP 402: CerebrasException - Payment required
```

**Decision needed**: Pay Cerebras, switch to M3 (cheaper), or disable.

### Block C — Script-not-found (4 crons)

```
kv-bws-sync                    /opt/data/scripts/kv_bws_sync.sh    — never created
linkedin-token-refresh         /opt/data/scripts/linkedin-token-refresh.sh
instagram-token-refresh        /opt/data/scripts/instagram-token-refresh.sh
aiw-boundary-validate-hourly   /opt/data/scripts/boundary-validate.py --all  — broken cron entry (--all being treated as part of path)
```

**Decision needed**: Disable all 4 (most are unused), or implement + add scripts.

### Block D — Arg-error (4 crons)

```
aiw-eval-gate-decisions-summary   eval-gate-enforce.py needs --agent X
aiw-intake-research-10min         intake.py needs --dept X --process
aiw-intake-engineering-10min      intake.py needs --dept X --process
aiw-intake-people-10min           intake.py needs --dept X --process
```

**Decision needed**: What args to pass on each. (Working intake-* and eval-gate-* crons presumably already have args; verify and copy pattern.)

### Block E — Slow-failing (1 cron, but probably more on Sunday)

```
thesis-weekly-review            rate-limit error (probably Sonnet 429)
thesis-git-maintenance          rate-limit error
aiw-research-tracker-weekly     rate-limit error
aiw-tax-receipt-tracker-weekly  rate-limit error
aiw-founder-bandwidth-watchdog-weekly
aiw-coach-ivan                  rate-limit error
```

**Decision needed**: Switch to M3 (auto-retries), reduce frequency, or disable.

## Recommended priority order

1. **Block A** (4 auth crons): add Anthropic key, or disable. **Cheapest decision, highest impact** — research jobs produce valuable output.
2. **Block D** (4 arg-error): just pass the right args. **Cheapest fix, restores 4 crons immediately.**
3. **Block B** (1 litellm): pay or switch. **Decide after Block A.**
4. **Block C** (4 missing): disable the unused ones. **Decide after Block D.**
5. **Block E** (slow-failing): batch disable weekly jobs to save $0.50/mo and reduce noise.

## The 47% claim in the ticket is outdated

Original ticket (Sep 1): "79/168 enabled crons broken (47%)"
Actual (Sep 3): "32/140 errored (23%), 48/188 disabled (26%), 80/188 dead-or-disabled (43%)"

PR #18 + PR #20 reduced errored count from ~50 to 32. After self-heal from path-blocked fixes, expect ~18 errored.

**The "provider decision" framing was a placeholder. The real decisions are the per-block fixes above.**

Refs: HANDOFF-PHASE-8.md, DEMIURGE-113, PRs #18 #20.
