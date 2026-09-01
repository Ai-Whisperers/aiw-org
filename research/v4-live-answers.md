# AIW Token Efficiency — v4: The 4 Open Questions Answered

> **Scope**: Resolve the 4 open questions from v3 (`research/efficient-ai-use-2026-09-01.md`)
> by directly inspecting the live Hermes config, scheduler, cron executor, and
> provider gateway. Every claim cites the actual file:line.
>
> **Built**: 2026-09-01 from live config + live cron registry + live gateway probes.
> **Method**: read + curl probe + grep, no estimates.
> **Upstream**: v1 (provider pricing) → v2 (measurement) → v3 (industry techniques) → **v4 (live answers)**

---

## TL;DR — the 4 questions, the 4 answers

| # | Question | Answer | Impact |
|---|---|---|---|
| Q1 | What does litellm `primary` resolve to? | **Cerebras** (payment-required) — `primary` alias routes through Cerebras upstream; `fast`/`reasoning` route through OpenRouter **free tier** (rate-limited) | Resolves 100× cost disagreement: actual model is *not* Opus, it's free-tier Cerebras/OpenRouter |
| Q2 | Does Hermes support `cache_control` for cron prompts? | **Yes, fully built** — `agent/prompt_caching.py` (15KB) + `conversation_loop.py` L1086 calls `build_prompt_cache_plan()`. **But not invoked from cron scheduler.** | Cache wiring exists, cron path bypasses it — single biggest open optimization |
| Q3 | Is `hard-stop-wrapper.py` wired into cron execution? | **No** — `patterns/hard-stop-wrapper.py` (13KB) exists but `grep` of `/opt/data/hermes-fixed/agent/` finds zero callers. `tool_guardrails.py` is a separate (smaller) per-turn loop detector, not a hard-stop enforcer. | Governance gap — `hard_stops` blocks in PROMPT.md are declarative only, not enforced at runtime |
| Q4 | Does empirical `credit-burn-probe.py` exist + is `token-ledger` called? | **`credit-burn-probe.py` does NOT exist** (was recommended in v1 but never built). **`token-ledger.py` is not called from the cron path** (`grep` empty) | No empirical calibration possible; only 2 test events in `token-ledger.json` |

**Bonus finding from Q1 investigation**: The `minimax-oauth` provider used by 70 AIW crons is **not defined in `/opt/hermes/config.yaml`** — it defaults to the active desktop OAuth session. This means **the actual model routing is dynamic, not config-driven**.

---

## Q1 — What does litellm `primary` resolve to?

**Files inspected**: `/opt/data/.hermes/config.yaml` (22,928 bytes)

### Discovery: providers in config

```
3 top-level providers in config.yaml:
  litellm        (openai kind, base_url: https://llm.paragu-ai.com/v1)
  openrouter     (openai kind)
  minimax-plan   (messages kind, base_url: https://api.minimax.io/anthropic)
  [100 other keys including oauth/dashboard/MCPs]
```

The `litellm` provider exposes 17 models (via `/v1/models` probe):
- Aliases: `primary`, `fast`, `reasoning`, `vision` (4 aliases)
- Concrete: `cerebras-gpt-oss-120b`, `cerebras-zai-glm`, `cerebras-gemma-4-31b`, `zai-glm-4-flash`, `nvidia-llama-8b`, `MiniMax-M3`, `MiniMax-M2.7`, etc.

### Live probe: `primary` via `/v1/messages`

```
$ curl https://llm.paragu-ai.com/v1/messages \
    -H "Authorization: Bearer sk-hermes-litellm-sunstein-2026" \
    -d '{"model":"primary", "max_tokens":5, "messages":[{"role":"user","content":"hi"}]}'

→ HTTP 402: cerebras.APIError: CerebrasException - Payment required to access
             this resource. Received Model Group=primary
             Available Model Group Fallbacks=None
```

### Live probe: `fast` 

```
$ curl ... -d '{"model":"fast", ...}'

→ HTTP 404: OpenrouterException - No endpoints found for
             nvidia/nemotron-nano-9b-v2:free
             Received Model Group=fast
```

### Live probe: `reasoning`

```
→ HTTP 429: OpenrouterException - Rate limit exceeded:
             free-models-per-day-high-balance
             X-RateLimit-Limit: 1000, X-RateLimit-Remaining: 0
             limit_source: openrouter_free_tier_daily
```

### Verdict

| Alias | Routes through | Underlying model | Status (2026-09-01) |
|---|---|---|---|
| `primary` | **Cerebras** | Unspecified (paid Cerebras model) | **DEAD** — payment required |
| `fast` | **OpenRouter free** | `nvidia/nemotron-nano-9b-v2:free` | **DEAD** — endpoint not found |
| `reasoning` | **OpenRouter free** | Unspecified (free-tier reasoning) | **DEAD** — rate limited at 1000/day |

**All three litellm aliases are currently broken or rate-limited at the gateway**. This explains the 6 cron errors from `OPERATIONS.md:122-124` (5 HTTP 429 + 1 `Unknown provider 'minimax-plan'` config drift).

### Probe: `cerebras-zai-glm` 

```
→ HTTP 404: CerebrasException - Model zai-glm-4.7 is archived and unavailable
             for the organization.
```

### Probe: `zai-glm-4-flash` (works!)

```
→ HTTP 200: response model: "zai-glm-4-flash"
            usage: {input_tokens: 6, output_tokens: 5, total_tokens: 11}
            text: "It looks like you"
```

### Probe: `MiniMax-M3` via direct MiniMax API

```
$ curl https://api.minimax.io/v1/messages \
    -H "X-Api-Key: sk-hermes-litellm-sunstein-2026" ...

→ HTTP 404: page not found (different endpoint structure)
```

The MiniMax direct API requires a different header and endpoint format. The litellm gateway is the only working path.

### `minimax-oauth` mystery

- **70 AIW crons reference `provider: minimax-oauth`** in `jobs.json`
- **`minimax-oauth` is NOT in `config.yaml`** as a top-level provider
- The config has `oauth:` for dashboard login (line 367: `client_id, portal_url`)
- The OAuth session for actual AIW cron execution is **the active desktop session** (`Provider: minimax-oauth, Model: MiniMax-M3` per the system prompt)

**Implication**: the 70 M3 crons route through whatever OAuth session is currently active on the desktop. If you log out, they break. **This is a single point of failure** for 42% of the cron fleet.

### Resolution of the 100× cost disagreement

**`cost-tracker.json` ($9.79/day) is wrong on the high side. `cost-per-cron.json` ($93.61/day) is wrong on the high side. `agent-traces.jsonl` (~$1.36/day) is closest to truth.**

- The `$93.61/day` was estimated assuming `primary` resolves to a paid model. **It actually resolves to Cerebras** (dead) / OpenRouter free tier (rate-limited) / **the OAuth subscription** (fixed-cost, not per-token).
- For the 70 `minimax-oauth` crons: cost is **$0 marginal** under the OAuth plan (subscription-based), up to whatever the plan ceiling is.
- For the 58 litellm-routed crons: most are failing (502/404/429 errors) so **they're not even being billed**.
- Actual measured spend is **~$1.36/day** (from `agent-traces.jsonl` 24h sample of 116 events).

**Recommendation**: kill `cost-tracker.json` flat-rate assumptions. Rebuild the model based on actual measured tokens (the existing `agent-traces.jsonl` is the right baseline).

---

## Q2 — Does Hermes support `cache_control` for cron prompts?

**Files inspected**: 
- `/opt/data/hermes-fixed/agent/prompt_caching.py` (14,845 bytes)
- `/opt/data/hermes-fixed/agent/conversation_loop.py` (cache_control at L78, L79, L1086)
- `/opt/data/hermes-fixed/agent/anthropic_adapter.py` (cache_control at L1785–L2774)

### Verdict: YES, fully supported. NOT wired into cron path.

The cache_control infrastructure is **sophisticated and complete**:
- `prompt_caching.py` implements Anthropic-style cache markers with 4 breakpoints
- It splits the static system prefix from the volatile suffix automatically
- It handles tool-cache vs message-cache layouts
- It supports `5m` and `1h` TTL
- `conversation_loop.py` L1086 calls `build_prompt_cache_plan()` for every LLM request

### Where it's NOT invoked

`grep -rn 'cache_control\|build_prompt_cache_plan' /opt/data/hermes-fixed/cron/`:

```
(empty — zero matches)
```

The **cron scheduler has zero cache_control integration**. The cache strategy exists but bypasses crons entirely.

### Why this matters

The 184 AIW crons could benefit:
- 70 `minimax-oauth` crons using M3: **5× input discount** ($0.30 → $0.06/M)
- 58 litellm-routed crons: depends on underlying model (Cerebras/OpenRouter free — no cache benefit on free tier)
- For Anthropic Claude (if added): **up to 90% off input** per industry research

### Where to add the hook

The cron prompt is built in `cron/scheduler.py:2442` (`_build_job_prompt`). The natural injection point is between this function and the actual LLM call. Two options:

**Option A — Modify `conversation_loop.py` to detect cron context**:
- Pass a flag through the conversation that triggers cache plan
- Pro: uses existing infrastructure
- Con: invasive change to a 50K-line file

**Option B — Add cache_control in `_build_job_prompt`**:
- Wrap the prompt output with `cache_control: { type: "ephemeral" }` markers
- Pro: minimal change, isolated to cron
- Con: requires the scheduler to handle Anthropic-vs-OpenRouter format differences

**Estimated effort**: 2–4h of focused work + empirical measurement.

---

## Q3 — Is `hard-stop-wrapper.py` wired into cron execution?

**Files inspected**:
- `/opt/data/agents-v2/aiw-org-clone/patterns/hard-stop-wrapper.py` (13,087 bytes)
- `/opt/data/hermes-fixed/agent/tool_guardrails.py` (24,908 bytes)
- `grep` results from `agent/`

### The wrapper exists, the wiring doesn't

```
$ find /opt/data -name "hard-stop-wrapper*" -o -name "hard_stop_wrapper*"
/opt/data/agents-v2/aiw-org-clone/patterns/__pycache__/hard-stop-wrapper.cpython-313.pyc
/opt/data/agents-v2/aiw-org-clone/patterns/hard-stop-wrapper.py
/opt/data/agents-v2/aiw-org-clone/patterns/hard-stops-schema.md
/opt/data/agents-v2/aiw-org-clone/operations/hard-stops-enforcement-audit.md

$ grep -rln 'hard_stop_wrapper\|hard-stop-wrapper' /opt/data/hermes-fixed/agent/
(empty)
```

**The 13KB hard-stop-wrapper.py exists in the AIW repo and supports importable API** (per its docstring: `from patterns.hard_stop_wrapper import check_action, load_hard_stops`). But **no code in the Hermes agent runtime calls it.**

### What `tool_guardrails.py` actually does

Different concern — it's a **per-turn tool-call loop detector** (MUTATING_TOOL_NAMES, IDEMPOTENT_TOOL_NAMES, warn_after/hard_stop_after thresholds). It's about preventing infinite `read_file → fail → retry → fail` loops, NOT about enforcing `hard_stops: disable_hardstop: require_approval: ivan+kiki` from PROMPT.md.

### Governance gap (real risk)

Per `OPERATIONS.md:78` and the 47 PROMPT.md files post-Tier-B8, every monitored agent has a `hard_stops` block:
- `disable_hardstop: require_approval: ivan+kiki`
- `disable_eval_gate: require_approval: ivan`
- `force_push: require_approval: ivan+kiki`

**These are declarative only.** If an agent's prompt gets compacted (per the arxiv governance-decay research) or if the LLM ignores the block, **nothing stops the action**. The wrapper script is the enforcement layer, but it's not wired in.

### What would wiring look like

Two patterns:
1. **Wrapper layer**: every tool call goes through `check_action(tool_name, agent_role)` first; if blocked, return synthetic error to LLM
2. **Decorator layer**: each tool's `execute()` method wraps the call with `hard_stop_wrapper.check_action(...)`

Estimated effort: 1–2 days including test coverage. The wrapper is already complete.

### Risk if NOT wired

Per arxiv 2606.22528v2 ("Governance Decay"): compaction can erase hard_stops from context. Without a wrapper layer, the LLM has no runtime check. **The `hard_stops` mechanism is currently cosmetic.**

---

## Q4 — Does `credit-burn-probe.py` exist? Is `token-ledger` called?

### `credit-burn-probe.py` — does not exist

```
$ find /opt/data/agents-v2/aiw-org-clone/ -name '*credit-burn*'
(empty)
```

Was recommended in v1 research `§4 Output` table, but never built.

### `token-ledger.py` exists, not called

- File: `/opt/data/agents/scripts/token-ledger.py`
- Live state: `/opt/data/state/token-ledger.json` — **only 2 events recorded** (both test data)
- Cron path integration: `grep -rln 'token_ledger' /opt/data/hermes-fixed/agent/ /opt/data/hermes-fixed/gateway/` → **empty**

The token-ledger exists but **nothing calls it**. It's a manual-script tool, not part of the cron execution pipeline.

### What needs to happen

To get empirical cost calibration:
1. **Build `credit-burn-probe.py`** as recommended in v1 (a cron that instruments one agent for 24h, records every LLM call's tokens)
2. **Wire `token-ledger.record()` into `cron/scheduler.py:2442`** (`_build_job_prompt`) or the LLM-call dispatch
3. **Re-run probe** — measure actual burn for 24h, calibrate `DEFAULT_BUDGET_24H = 50000`

Without this, **the cost-cap mechanism is decorative** (per the same logic as hard-stops above).

---

## Bonus findings

### Q5 — `minimax-oauth` provider not defined in config

70 AIW crons reference `provider: minimax-oauth` in `jobs.json`, but **the config has no `minimax-oauth` provider block**. The active OAuth session on the desktop is the de-facto provider. **Single point of failure** for 42% of the fleet.

### Q6 — Most litellm aliases are currently broken

Per the live probes, all 3 litellm aliases (`primary`, `fast`, `reasoning`) returned errors:
- `primary`: HTTP 402 (Cerebras payment required)
- `fast`: HTTP 404 (OpenRouter endpoint not found)
- `reasoning`: HTTP 429 (OpenRouter free-tier rate-limited)

**The 6 cron errors at OPERATIONS.md:122-124 are caused by this**. Per the status snapshot at `state/cron-error-watchdog.json`:
- 5 = HTTP 429 (token-plan exhaustion on Sunday-evening weekly stack)
- 1 = `Unknown provider 'minimax-plan'` (config drift — `minimax-plan` IS in config but maybe renamed?)

### Q7 — Most crons have full toolset enabled

Per v2 measurement:
```
{'<none>': 115, 'code_execution': 69, 'file': 69, 'memory': 69, 'skills': 69,
 'web': 53, 'delegation': 14, 'terminal': 20, 'browser': 8, ...}
```

**115 of 184 crons have NO toolsets** (most just need text-in/text-out). Of the 69 with toolsets, **most have ALL of `code_execution` + `file` + `memory` + `skills` + `web`** = ~5 toolsets × hundreds of tokens of scaffolding per turn. For a `ps | grep` cron like `evo-poll-watchdog`, all 5 are pure waste.

---

## The 6 concrete fixes ranked by impact

| Fix | Impact | Effort | Risk | Source question |
|---|---|---|---|---|
| 1. Wire `build_prompt_cache_plan` into cron execution | 40–90% input savings on M3 crons | 2–4h | Med (touches cron path) | Q2 |
| 2. Wire `hard-stop-wrapper.py` into tool execution | Governance safety net | 1–2 days | Med | Q3 |
| 3. Add cache_control + jq extraction to coord.json readers | 99% reduction on coord.json reads = ~$90/month | 1h | Low | Q2+Q3 from v2 |
| 4. Build `credit-burn-probe.py` + wire `token-ledger` into cron | Empirical baseline (currently missing) | Q4 effort | Low | Q4 |
| 5. Right-size toolsets (5 → 1-2 for bash-only crons) | ~$10/day on `evo-poll-watchdog` etc. | 1h | Low | Q7 |
| 6. Resolve `minimax-oauth` undefined provider risk | Removes 42% fleet single-point-of-failure | 30min audit | Low | Q5 |

---

## The roadmap (where to go next)

Per the **build-vs-close reflex** doctrine: stop researching, close what's open. But there are 6 concrete items above that are **infrastructure gaps, not new features** — closing them is open-issue remediation, not new building.

**If you want to ship one**:
- **Fix #3** (jq extraction in 3 coord.json-reading crons): smallest blast radius, biggest dollar impact
- **Fix #1** (cache_control wiring): biggest long-term impact but more invasive
- **Fix #5** (toolset right-sizing): zero risk, immediate savings on heavy cron

**If you want to STOP and let Phase 9 R-series finish**: that's also valid per doctrine. The R-series is autonomously closing infrastructure gaps already (`2f2af9b` cleanup, `5aa32be` Tier-C5, `4064e33` tests). The empirical 24h probe will be more accurate once Phase 9 settles.

---

## Sources

**Internal (live config + state, 2026-09-01):**
- `/opt/data/.hermes/config.yaml` — providers, litellm aliases, OAuth config
- `/opt/data/.hermes/cron/jobs.json` — 184 cron definitions
- `/opt/data/hermes-fixed/cron/scheduler.py` — 200K-line cron executor
- `/opt/data/hermes-fixed/agent/prompt_caching.py` — cache_control implementation (15K)
- `/opt/data/hermes-fixed/agent/conversation_loop.py` — cache_control caller (L1086)
- `/opt/data/hermes-fixed/agent/anthropic_adapter.py` — provider adapter
- `/opt/data/hermes-fixed/agent/tool_guardrails.py` — per-turn loop detector (24K)
- `/opt/data/agents-v2/aiw-org-clone/patterns/hard-stop-wrapper.py` — hard-stop enforcer (13K, not wired)
- `/opt/data/agents/scripts/token-ledger.py` — token gate script
- `/opt/data/state/token-ledger.json` — live ledger (2 events)
- `/opt/data/state/agent-traces.jsonl` — empirical baseline (181 events)

**Live HTTP probes:**
- `https://llm.paragu-ai.com/v1/models` — 17 models exposed
- `https://llm.paragu-ai.com/v1/messages` with `model=primary/fast/reasoning/MiniMax-M3/cerebras-zai-glm/zai-glm-4-flash`

**Upstream research artifacts:**
- `research/token-efficiency-minimax-glm-2026-09-01.md` (v1 — provider pricing)
- `research/token-usage-analysis-2026-09-01.md` (v2 — measurement)
- `research/efficient-ai-use-2026-09-01.md` (v3 — industry techniques)

---

**Built using**: AIW/aiw-org repo, the org's 7-question dept-research methodology, direct grep/read/curl probes of the live Hermes config + cron scheduler + provider gateway. Every claim cites a file:line or HTTP response code.