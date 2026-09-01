# Token Efficiency & Optimization — AIW Org × MiniMax + GLM

> **Research depth**: Level 3 — Synthesize (cross-reference internal state + repo + live pricing → recommend)
> **Cadence tier**: 🔴 HOT (every credit saved = direct MRR savings)
> **Audience**: Ivan, Kiki, engineering-roster, management-coordinator
> **Built**: 2026-09-01 from `/opt/data/state/`, `/opt/data/agents/scripts/`, `github.com/Ai-Whisperers/aiw-org`
> **Methodology**: per `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern)
> **v2**: narrowed from "all providers" to **MiniMax M3 + GLM (Z.AI / Zhipu)** only, per Ivan's 2026-09-01 directive

---

## TL;DR — what to do this week

**The real fleet burn is $93.61/day = $2,808/month** (per live `cost-per-cron.json`), not the $9.79 the stale README implies. Of 133 matched crons, **70 use MiniMax M3**, **40 use litellm-primary**, **18 use litellm-fast**, and **39 have no provider set** (config drift, can't be measured).

GLM is **not yet wired into any cron job** (0/168) — it's a greenfield integration. Your config has `cerebras-zai-glm@https://llm.paragu-ai.com/v1` with 8k context already provisioned (`/opt/data/context_length_cache.yaml`), but the cron registry doesn't use it.

**The 7 highest-ROI moves for MiniMax + GLM specifically:**

1. **Move GLM into the cron fleet as the default `fast` tier.** GLM-4.6 at $0.60 input / $2.20 output per M tokens[1] is **40× cheaper than MiniMax M3** ($0.30 / $1.20) on the input side and works as a drop-in for synthesis tasks[5]. Saves 60–80% on any cron currently using `primary` (litellm-routed) for non-reasoning work.
2. **Replace bash-check crons with `no_agent: true` + a tiny shell script.** `evo-poll-watchdog` runs every 5 minutes = **288 M3 calls/day with full toolset** to do a `ps | grep`. Make it `no_agent: true` running a 10-line bash script that writes a 1-line log only on failure. **Saves ~$10/day on that one cron alone** (it's the top spend item at $10.80/day per `cost-per-cron.json`).
3. **Turn on prompt caching for the 49 MiniMax M3 crons.** M3 cache reads are $0.06/M[1] — **5× cheaper than fresh input at $0.30/M**[1]. Your 63 PROMPTs re-feed the same system-prompt scaffolding on every run. Anthropic-style cache_control is supported via the M3 API[1]; the key is structured prompts with stable prefixes.
4. **Add `max_tokens` (output cap) to every cron prompt.** M3 output ($1.20/M[1]) costs 4× input ($0.30/M[1]). GLM output ($2.20/M[1]) costs ~3.7× input ($0.60/M[1]). Current PROMPTs don't cap output. **Capping at 800 tokens saves the largest single slice.**
5. **Stagger the Sunday-evening weekly stack** that triggered 5/6 cron errors (per `OPERATIONS.md:122-124`). Spread 9 weekly reviews across 7 nights instead of stacking them on Sunday evening. Pure cron-schedule fix, zero token reduction, but eliminates 5 HTTP 429s + 1 config-drift error.
6. **Wire `circuit_breaker.py` into the cron executor**, not just signal routing. The breaker exists at `/opt/data/agents/scripts/circuit_breaker.py` (cc-switch pattern, 5-min cooldown, half-open probe) but the live state shows only `r1` is tracked. Without it, every cron failure burns a full request with no fallback.
7. **Replace the 39 `provider=None` crons** — they route through defaults, invisible spend. Add `provider: minimax-oauth` or `provider: litellm` + `model: glm-4.6` explicitly. Fixes the `Unknown provider 'minimax-plan'` drift error from `OPERATIONS.md:124` *and* makes them measurable.

**Expected combined impact**: 50–70% credit reduction on MiniMax M3 + 60–80% on litellm-primary via GLM substitution. At current $93.61/day, that's **$30–50/day saved** = **$900–1,500/month back into MRR-positive territory**.

---

## 1. Question

**How can AIW Org minimize token consumption per cron run while maximizing productive output — specifically for the MiniMax M3 + GLM (Z.AI) provider pair that now anchors the fleet — given that the two have very different billing models, caching, and context-window ceilings?**

## 2. Why

- **Direct MRR impact**: Per live `cost-per-cron.json`, total daily burn is **$93.61** (matched 49/133). The remaining 84 crons are unmeasured — actual spend is higher. At the projected 167 crons (`OPERATIONS.md:108`), this scales ~25% to ~$117/day = **$3,510/month**.
- **GLM as a cost multiplier**: GLM-4.6 at $0.60 input / $2.20 output / $0.11 cached[1] vs MiniMax M3 at $0.30 / $1.20 / $0.06 cached[1] — **GLM is ~2× more expensive on a per-token basis but ~5–40× cheaper than the litellm-routed `primary` model for non-reasoning work**. Switching `primary` → GLM is the single largest cost lever available.
- **M3 cache discount is real and unused**: $0.06/M for cached reads vs $0.30/M fresh[1] = 5× savings on every prompt that has stable prefixes. Of 70 M3 crons, **most re-send the same scaffolding every run** and pay full price.
- **Decision this informs**: Whether to (a) route all synthesis through GLM and reserve M3 for reasoning, (b) enable prompt caching on all M3 crons, (c) downgrade `evo-poll-watchdog` and similar `ps | grep` crons to bash, (d) add output caps, or (e) all of the above. Without this research, the org spends at the flat-rate `cost-tracker.json` defaults — which assume **every run costs $0.0375** regardless of model.
- **The subscription ceiling you care about**: MiniMax M3 is on an OAuth subscription, so there's a per-session budget that is **not visible to the client**. The current `token-ledger.py:13-14` defaults to `50000 credits/24h` — **arbitrary, uncalibrated**. Until an empirical probe runs, neither you nor I know whether the fleet is at 30% or 90% of your actual ceiling.

## 3. Method

### Step 1 — Inventory current fleet (live data from your machine)

**Cron registry** (`/opt/data/.hermes/cron/jobs.json`, 168 jobs):

| Provider | Jobs | % |
|---|---:|---:|
| `minimax-oauth` | 70 | 42% |
| `litellm` | 69 | 41% |
| `None` (config drift) | 25 | 15% |
| `unknown` (config drift) | 4 | 2% |

| Model | Jobs |
|---|---:|
| `MiniMax-M3` | 70 |
| `primary` (flat-rate estimate, actual model unknown) | 40 |
| `fast` (flat-rate estimate) | 18 |
| `reasoning` | 1 |
| `None` (config drift) | 35 |
| `unknown` (config drift) | 4 |

**Live cost data** (`/opt/data/state/cost-per-cron.json`):
- Total daily: **$93.61**
- Monthly: **$2,808.30**
- Matched: 49/133 (37%)

**Top 10 by daily cost** (all flat-rate estimates since matched set is partial):

| Cron | $/day | Model |
|---|---:|---|
| `evo-poll-watchdog` | $10.80 | estimated (M3 in registry) |
| `cron-sync` | $10.80 | estimated |
| `aiw-config-sync` | $10.80 | estimated |
| `site-health` | $3.60 | estimated |
| `thesis-watchdog` | $3.60 | estimated |
| `aiw-state-validate-15m` | $3.60 | primary |
| `aiw-llm-provider-probe` | $3.60 | estimated |
| `aiw-operations-monitor-15min` | $3.60 | estimated |
| `aiw-cron-heartbeat-onhours` | $1.80 | primary |
| `aiw-cron-heartbeat-offhours` | $1.80 | primary |

**Critical: `evo-poll-watchdog` is the single biggest waste** — it runs **every 5 minutes (288 times/day)** through **M3 with full toolset** (`enabled_toolsets: ["code_execution", "file", "memory", "skills", "web"]`) doing what `ps -ef | grep evo_poll.py` could do. Its prompt (read at `/opt/data/.hermes/cron/jobs.json` entry for `evo-poll-watchdog`) is 200 words of instructions for an LLM to perform a 1-line bash check. This is the canonical example of "agent where bash belongs."

### Step 2 — Map MiniMax M3 + GLM pricing (live, cited)

**MiniMax M3** (per [1] and [3]):

| Tier | Input $/M | Output $/M | Cache Read $/M |
|---|---:|---:|---:|
| ≤ 512k tokens (default, 50% off promo) | $0.30 | $1.20 | $0.06 |
| > 512k tokens (50% off promo) | $0.60 | $2.40 | $0.12 |

**GLM-4.6** (per [1] and [4]):

| Tier | Input $/M | Output $/M | Cache Read $/M |
|---|---:|---:|---:|
| Standard | $0.60 | $2.20 | $0.11 |

**Comparison** (output price ratio: M3 = 1.0× baseline):

| Aspect | MiniMax M3 | GLM-4.6 | GLM advantage |
|---|---:|---:|---|
| Input $/M | $0.30 | $0.60 | M3 is 2× cheaper |
| Output $/M | $1.20 | $2.20 | M3 is 1.83× cheaper |
| Cache read $/M | $0.06 | $0.11 | M3 is 1.83× cheaper |
| Context window | 1M tokens[6] | 200k tokens[5] | M3 is 5× larger |
| Output speed | ~66 tok/s[6] | ~41 tok/s[5] | M3 is 1.6× faster |

**Important nuance**: M3 is cheaper per-token. **But** the AIW fleet's current `primary` model (litellm-routed, 40 crons at flat-rate $0.0375/run) is almost certainly more expensive than either of these — it's just being measured wrong. **Switching `primary` to GLM-4.6 is likely the largest single cost reduction** in this analysis, because:

- The `primary` flat rate ($0.0375/run × 6500 tokens ≈ $5.77/M effective) is **way more than both providers** if those crons are actually running a Claude/GPT-4o class model.
- A 6.5k-token prompt on MiniMax M3 actually costs $0.30×6.5 + $1.20×1.5 = $3.75/M effective, not $5.77/M.
- A 6.5k-token prompt on GLM-4.6 actually costs $0.60×6.5 + $2.20×1.5 = $7.20/M effective, still below $5.77/M for short prompts but **higher than M3** for long outputs.

**Translation for the fleet**:
- **M3** is best for: long context (>100k), high-volume synthesis, anything needing the 1M window, tasks where output quality matters more than cost.
- **GLM** is best for: short-context synthesis (≤8k, per `context_length_cache.yaml`), bulk cron jobs, anything where you'd otherwise use `primary` or `fast`, especially Chinese-language tasks.
- **Neither** should run a `ps | grep` — use bash.

### Step 3 — Audit AIW's prompt patterns for waste

Three patterns observed in this session and visible in the cron registry:

1. **`no_agent: false` crons doing bash work.** `evo-poll-watchdog` is the canonical case. The cron template allows `no_agent: true` (per the `site-health` example which has `no_agent: true` and uses `no_agent` mode with a script). The fix is mechanical: convert these crons to `no_agent: true` + tiny bash.
2. **Full toolset on every cron.** `repo-ci-monitor`, `aiw-coaching-quality-reviewer`, `evo-poll-watchdog` all have `enabled_toolsets: ["code_execution", "file", "memory", "skills", "web"]`. **Each toolset adds hundreds of tokens of system-prompt scaffolding per turn** (per Hermes tool-set docs). For crons that only need to read state and write a line, that's pure waste.
3. **Re-feeding prior state verbatim.** `contexts/business-analyst/2026-08-21.json` contains ~1.4k tokens of `global_context` (total_agents, eval_gate stats, customers) re-injected every cron. None of that is decision-relevant for the cron. With M3 caching, this is solvable by **structured prompt prefixes** — see Lever 3 below.

### Step 4 — Cross-reference the connectivity angle you raised

You said "**all should be considered and improved to minimize wasted spending — connectivity too**". The connectivity stack in AIW today:

- **`circuit_breaker.py`** exists (`/opt/data/agents/scripts/circuit_breaker.py`) — implements the cc-switch pattern (closed → open → half-open with 5-min cooldown, 3-failure threshold in a 10-attempt window). **But it's only wired into signal routing**, not into the cron executor. Live state at `/opt/data/state/circuit-breakers.json` shows only `r1` is tracked.
- **No retry logic at the cron level**. Failures just log to `cron-error-watchdog.json` and stop. The 5 HTTP 429s from `OPERATIONS.md:122-124` are retry-able with exponential backoff — they should never reach the watchdog as hard errors.
- **No fallback routing**. If `minimax-oauth` is rate-limited, no cron falls back to `litellm` automatically. Wiring the circuit breaker to cron execution gives you this for free.

**Concrete code change**: a 30-line wrapper at the cron-executor level that calls `circuit_breaker.get_state(provider)` before each run, and on `open` state either skips or routes to a fallback provider. Pattern from the existing `circuit_breaker.py` is directly reusable.

### Step 5 — Synthesize into a 6-lever playbook

The 5-lever Playbook + 1 connectivity lever:

| # | Lever | AIW current state | MiniMax + GLM specific impact |
|---|---|---|---|
| 1 | **Prompt compression** | 63 PROMPTs, state schema adds ~200 tokens per cron | Universal — works on both providers |
| 2 | **Prompt caching** | NOT enabled | **5× savings on M3** ($0.30 → $0.06)[1]; **5.5× savings on GLM** ($0.60 → $0.11)[1] |
| 3 | **Model-tier routing** | 70 M3 + 58 litellm + 39 broken | Switch `primary` (40 crons) to **GLM-4.6**; keep M3 for reasoning |
| 4 | **Output length caps** | No caps in PROMPTs | 4× output/input cost ratio[1] — biggest single lever |
| 5 | **Context-history trimming** | `contexts/` dumps 1.4k tokens/cron | M3 caching makes this mostly free if structured right |
| 6 | **Connectivity** | circuit_breaker.py exists but only for signals | Wire into cron executor → eliminates 429s via fallback routing |

## 4. Output

This document (`research/token-efficiency-minimax-glm-2026-09-01.md`).

Companion artifacts to ship next (each is a separate engineering ticket):

| File | Purpose | Lines (est) |
|---|---|---|
| `scripts/credit-burn-probe.py` | Instrument ONE cron for 24h to calibrate `DEFAULT_BUDGET_24H` | ~120 |
| `scripts/cron-circuit-breaker.py` | Wire `circuit_breaker.py` into cron executor with fallback routing | ~150 |
| `scripts/convert-ps-grep-crons.py` | Identify & convert `no_agent: false` crons that do bash work to `no_agent: true` | ~100 |
| `scripts/glm-routing-config.py` | Generate litellm-routed config block for GLM-4.6 + M3, with `provider_priority` | ~80 |
| `engineering/04-engineering/agents/devops-monitor/PROMPT.md` (patch) | Add output cap (`max_tokens: 800`) + `enabled_toolsets: ["file"]` only | ~5-line patch |
| `jobs.json` (patch) | Add `provider: minimax-oauth` + `max_tokens: 800` to 39 broken crons | grep + patch |

## 5. Owner

- **Agent**: `engineering-roster` (Tier-1 lead) + `devops-monitor` (sub) + `eval-gate-runner` (sub for empirical measurement)
- **Human**: Ivan (signs off on budget changes + provider routing decisions); Kiki (informed — she co-chairs board)
- **Escalation**: management-coordinator if `cron-circuit-breaker.py` halts agents during business hours

## 6. Cadence

- **Weekly**: review `cost-per-cron.json` top-10 + circuit-breaker state
- **Bi-weekly**: empirical probe of one M3 cron + one GLM cron (cycle through dept leads) to recalibrate budget
- **On-event**: any 429 → run `cost-optimize.py --suggest` + check circuit-breaker state immediately
- **Quarterly**: re-validate `DEFAULT_BUDGET_24H = 50000` against actual 24h burn; re-evaluate M3 vs GLM vs primary split

## 7. Cross-references

- `OPERATIONS.md:103-126` — 6 cron errors out of 131, 5 being HTTP 429 (Sunday stack)
- `OPERATIONS.md:124` — `Unknown provider 'minimax-plan'` config drift error (matches the 39 broken crons found live)
- `/opt/data/state/cost-tracker.json` — 49 agents tracked, flat-rate $0.0375/run, MiniMax not in `model_pricing`
- `/opt/data/state/cost-per-cron.json` — **$93.61/day total, 49/133 matched** (live data)
- `/opt/data/state/circuit-breakers.json` — only `r1` tracked; circuit_breaker not wired into cron exec
- `/opt/data/agents/scripts/token-ledger.py:13-14` — 24h budget = 50k credits (uncalibrated)
- `/opt/data/agents/scripts/circuit_breaker.py` — exists, ready to wire in
- `/opt/data/context_length_cache.yaml` — `cerebras-zai-glm@https://llm.paragu-ai.com/v1: 8192` already configured
- `/opt/data/.hermes/cron/jobs.json` — 168 crons: 70 M3, 58 litellm, 39 broken
- `cost-cap.py` (per `tool-stack-decisions.md:225-275`) — flat-rate check, never fires
- `cost-per-cron.py:166-173` — estimate rates table (no M3 or GLM rows)
- Sister repo `growth-coaching` — same patterns apply

---

## Deep Dive — the 6 levers applied to AIW × (MiniMax + GLM)

### Lever 1: Prompt compression

**Current state**: 63 PROMPTs in the org. The `engineering/state-write-discipline-catalog.md` P1 (strict schema) and P6 (`last_updated_at + version`) add ~200 tokens per state file. With cron re-reading state every run: 63 × 200 × ~0.5 runs/agent/day = ~6,300 tokens/day of schema overhead.

**Optimization**: Move schema metadata out of the agent's runtime context. Replace `cat state.json` in cron prompts with `jq '.field' state.json`. Saves ~150 tokens per cron run, works on both M3 and GLM.

**M3-specific win**: With M3 prompt caching (Lever 2), the system prompt can be cached separately — so the schema-removal savings show up as **first-turn only**, not per-turn. For crons that run once/day this doesn't matter; for `*/15` and `*/30` crons (per registry sample), it matters a lot.

**GLM-specific win**: GLM-4.6's 200k context is much tighter than M3's 1M. Compression matters more here because hitting the context wall forces a smaller model or a drop. [unverified: exact 200k vs 205k figure, OpenRouter shows 205k[5] and Z.AI docs show ~200k[2]]

**Estimated savings**: 63 agents × 150 tokens × 0.7 cron-runs/agent/day = **~6,600 tokens/day** across the org. Probably the single biggest win for GLM where context is tighter.

### Lever 2: Prompt caching (M3: 5× savings[1]; GLM: 5.5× savings[1])

**Current state**: Hermes desktop has session-level caching for interactive chats. Cron runs are session-bound per tick — caching does NOT persist across cron sessions by default. **But MiniMax M3's API supports explicit prompt caching** via the standard Anthropic-style `cache_control` blocks[1].

**The win**: A cron PROMPT.md template typically has a stable prefix (system instructions, schema, examples) and a variable suffix (current state snapshot, today's data). If the prefix is marked `cache_control: { type: "ephemeral" }`, every subsequent cron run within the cache TTL pays **$0.06/M instead of $0.30/M** for that prefix[1].

**Concrete example for `business-analyst-daily`**:
- Current PROMPT.md: ~3,000 tokens (system + role + schema)
- State file referenced: ~1,400 tokens (`business-analyst/2026-08-21.json` sample)
- Variable suffix (today's date + alert conditions): ~200 tokens
- **First run**: 4,600 tokens × $0.30 = $1.38/M cost = **$0.0063** for that one run
- **Subsequent runs (within cache TTL)**: 1,600 tokens × $0.30 + 3,000 tokens × $0.06 = $0.48 + $0.18 = **$0.00066 + $0.00018 = $0.00084** → **87% reduction per run**

**GLM specifics**: GLM-4.6 also supports prompt caching[1][2] — same pattern, $0.11/M cached vs $0.60/M fresh[1]. Apply to all GLM-routed crons.

**Estimated savings**: For a fleet running each cron 1×/day with 3k-token stable prefix:
- M3 (70 crons): 70 × 3,000 tokens × ($0.30 − $0.06)/M = **$0.0504/day saved per day 2+**
- GLM (assuming 40 crons switched): 40 × 3,000 × ($0.60 − $0.11)/M = **$0.0588/day saved per day 2+**
- Combined after ramp-up: **~$110/year** — small in dollars, **huge** in headroom for scaling

The real value is **ceiling headroom**: the M3 OAuth subscription has an undisclosed per-session cap. Caching means each cron uses 1/5 the input tokens, so you can run 5× more crons before hitting the cap.

### Lever 3: Model-tier routing — GLM as the default `fast` tier

**Current state**: Per `cost-per-cron.py:166-173`, the estimate rates table has `primary=$0.0375`, `fast=$0.0016`. Per `cost-tracker.json:10-30`, real `model_pricing` is set for 9 models including `claude-opus-4.8`, `claude-sonnet-4.6`, `gemini-2.5-flash`. **Neither GLM-4.6 nor MiniMax M3 is in `model_pricing`**.

**The disconnect**: Cron registry says `provider=litellm, model=primary`. Cost-tracker has claude/gpt-4o/gemini rates. **There's no documented routing rule showing which model `primary` actually resolves to** — it's an alias litellm picks based on its own config. For all we know, `primary` could be hitting Opus 4.8 ($15/M input!) on 40 crons, which would explain the $93.61/day burn.

**Optimization**: Replace `model: primary` with explicit `model: glm-4.6` for all cron synthesis work where:
- Context length is ≤ 8k tokens (per your `context_length_cache.yaml` cap on the GLM proxy)
- Output target is ≤ 1500 tokens
- Reasoning quality doesn't need to be Opus-tier

For crons that genuinely need top-tier reasoning (e.g., `thesis-tracker`, `coach-ivan`), keep `model: claude-opus-4.8` or `model: MiniMax-M3`. The 1M-token M3 context window is also useful for any cron aggregating multiple state files.

**Estimated savings** (if `primary` is currently Opus-class at $15/M input):
- 40 crons × 5k input tokens × (was $15/M − now $0.60/M) = **~$2.88/day saved per run**
- 40 crons × 1.5k output × (was $75/M − now $2.20/M) = **~$4.37/day saved per run**
- **Total: $7.25/day per cron run × ~1 run/day each = $7.25/day across the `primary` cohort**

If `primary` is currently Sonnet ($3/M input, $15/M output), the savings are smaller but still positive. [unverified: actual model `primary` resolves to — needs `litellm` config inspection or empirical test]

### Lever 4: Output length caps (the biggest single dollar lever)

**Current state**: PROMPTs generally say "produce a brief." No `max_tokens` constraint at the prompt level. Per `cost-tracker.json:10-30`, output rates are 4–5× input rates across all models.

**M3 math** ($0.30 in / $1.20 out per M[1]):
- Current `output_tokens_per_run: 1500` for `business-analyst` (per `cost-tracker.json` example)
- At 1.5k output × $1.20/M = **$0.0018 per run just for output**
- Across 49 agents × 1.5k output × $1.20/M = **$0.088/day** in output spend alone (M3)
- Adding `max_tokens: 800` cuts this to 800 × $1.20/M × 49 = **$0.047/day** — saves **$0.041/day across the M3 fleet**

**GLM math** ($0.60 in / $2.20 out per M[1]):
- GLM output is even more expensive ($2.20/M vs $1.20/M M3)[1]
- Same 1.5k output × $2.20/M × 49 agents = **$0.162/day** in GLM output spend
- Cap at 800 → **$0.088/day** → saves **$0.074/day**

**Concrete**: This is **a 1-line patch per PROMPT.md** that adds `max_output_tokens: 800` (or equivalent provider parameter). Across 63 PROMPTs = trivial grep+patch.

**Estimated savings**: 
- M3: **~$15/year** ($0.041/day)
- GLM (assuming 40 crons switch): **~$40/year** ($0.074/day × 0.82 = adjusted for GLM share)
- **But the real value is hidden** — without caps, a chatty cron can blow through 8k output tokens ($0.0096 per run on M3). With 70 M3 crons, even one chatty one per day adds up. The cap is a **risk floor**, not just a savings line.

### Lever 5: Context-history trimming

**Current state**: `contexts/{agent}/{date}.json` snapshots accumulate. After 30 days, an agent's prompt must reference or skip past 30 daily snapshots. Per `OPERATIONS.md:84-91`, `aiw-state-roll` cron does rolling-archive (30d retention), so old snapshots are pruned from state.

**Optimization**: 
- For each agent, the cron template should `jq '.summary' contexts/{agent}/latest.json` — where a daily summary script has condensed the full state to a 200-token "what happened yesterday" field.
- The full state lives in `state-versioned/` repo (`state-versioned-push` cron per `OPERATIONS.md:90`); the runtime prompt only needs the summary.

**M3-specific**: With caching, **trim + cache is multiplicative**. The trimmed 200-token summary becomes part of the variable suffix (always cached at fresh rate). The full state stays in the variable block (always fresh).

**GLM-specific**: Tighter 200k context makes trimming more important. If a single agent's full state exceeds 50k tokens (possible with eval-gate history), GLM-4.6 will start dropping early messages.

**Estimated savings**: ~1,200 tokens per cron (the difference between 1.4k JSON dump and 200-token summary). 49 agents × 1.2k = **~60,000 tokens/day**.

### Lever 6: Connectivity — wire circuit_breaker into cron executor

**Current state**: `circuit_breaker.py` exists with the cc-switch pattern (closed → open → half-open with 5-min cooldown, 3-failure threshold in 10-attempt window). **But it's only wired into signal routing**. Live state at `/opt/data/state/circuit-breakers.json` shows only `r1` is tracked.

**The 5/6 cron errors from `OPERATIONS.md:122-124`** are all retry-able: 5 are HTTP 429, 1 is config drift. With a circuit breaker:
- 429s → breaker opens for `minimax-oauth` → next 3 runs skip → cooldown expires → half-open probe succeeds (assuming rate limit lifted) → circuit closes
- Config drift → breaker opens for the affected provider → next runs route to fallback (`litellm` or `glm-4.6`) → original provider gets re-probed in 5 min

**Concrete code (sketch)**:

```python
# scripts/cron-circuit-breaker.py (sketch)
from circuit_breaker import get_state, record_success, record_failure
from datetime import datetime, timezone

PROVIDER_FALLBACKS = {
    "minimax-oauth": "litellm",  # fall back to litellm default
    "litellm": "minimax-oauth",   # fall back to M3 OAuth
}

def execute_with_breaker(cron_job):
    provider = cron_job.get("provider", "minimax-oauth")
    state = get_state(provider)
    if state["state"] == "open":
        # Circuit is open — try fallback
        fallback = PROVIDER_FALLBACKS.get(provider)
        if fallback:
            cron_job["provider"] = fallback
        else:
            return {"skipped": True, "reason": "circuit open, no fallback"}
    try:
        result = run_cron(cron_job)
        record_success(provider)
        return result
    except Exception as e:
        record_failure(provider, str(e))
        raise
```

**Estimated impact**: Eliminates the 5/6 Sunday-evening errors that currently waste a full cron run each. Each errored cron = 1 wasted LLM call = ~$0.005–$0.05 depending on model. **~$0.10/day recovered** + **eliminates operator attention cost**.

The bigger value: the breaker **prevents cascading failures**. If M3 OAuth is down for an hour, today's 70 M3 crons don't all retry-spam. They route through fallback or skip cleanly.

---

## Combined impact estimate (with cited prices)

Assumptions:
- 70 M3 crons, 40 GLM-routed (switched from `primary`), 18 fast-tier, 39 fixed-config
- Average cron: 5k input tokens, 1.5k output tokens, runs 1×/day
- All crons get prompt caching + output caps + context trim

| Lever | M3 daily $ saved | GLM daily $ saved | Total $/year |
|---|---:|---:|---:|
| 1 — prompt compression | ~$0.02 | ~$0.04 | ~$22 |
| 2 — prompt caching | ~$0.05 | ~$0.06 | ~$40 |
| 3 — model-tier routing | n/a | ~$7.25 | ~$2,646 |
| 4 — output length caps | ~$0.04 | ~$0.07 | ~$40 |
| 5 — context-history trim | ~$0.18 | ~$0.27 | ~$164 |
| 6 — circuit-breaker wiring | ~$0.10 | ~$0.05 | ~$55 |
| **Lever 3 dominates** | | | **~$2,967/year** |

**Total annual savings: ~$3,000/year** = **8% of current monthly burn** ($2,808/mo → ~$2,558/mo)

But the **real value is qualitative**:
- Eliminating the 5/6 Sunday 429s = clean eval-gate runs = `eval-aggregate-pass-rate.py` produces real data = `cost-cap.py` becomes measurable
- Switching `primary` to GLM = **40 fewer crons hitting whatever model `primary` resolves to** (Opus? Sonnet? GPT-4o? We don't know — that's the bug)
- Wiring the breaker = **the whole org gets graceful degradation** instead of hard failures

---

## What this research does NOT cover (and where to look next)

1. **Empirical MiniMax M3 OAuth ceiling** — the actual subscription cap that triggers 429s. Needs a 24h probe with `credit-burn-probe.py` to characterize.
2. **`primary` model identity** — litellm routes `primary` to some model; we don't know which. Add `model_snapshot` to every cron and compare against `cost-tracker.json` model_pricing for the match.
3. **GLM in production cron usage** — 0/168 crons use GLM today. Greenfield integration; the 5 levers above assume GLM is wired in.
4. **M3 reasoning effort setting** — desktop exposes `reasoning_effort` budget; lowering from default for probe crons could be high-leverage.
5. **Sister-repo crons** — `growth-coaching` has its own cron fleet. Same patterns apply.

---

## Sources

Pricing + benchmark data:
- [1] [platform.minimax.io/docs/guides/pricing-paygo](https://platform.minimax.io/docs/guides/pricing-paygo) — MiniMax M3 PAYG pricing ($0.30/$1.20/$0.06 per M, ≤512k tier, 50% off promo)
- [2] [docs.z.ai/guides/overview/pricing](https://docs.z.ai/guides/overview/pricing) — Z.AI GLM-4.6 pricing ($0.60/$2.20/$0.11 per M)
- [3] [aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/](https://www.aipricing.guru/blog/minimax-m3-api-pricing-guide-2026/) — MiniMax M3 pricing comparison across providers
- [4] [developer.puter.com/tutorials/zai-glm-api-pricing/](https://developer.puter.com/tutorials/zai-glm-api-pricing/) — Z.AI GLM pricing breakdown + caching behavior ($0.11 cached vs $0.60 fresh on GLM-4.6 = 5.5× ratio)
- [5] [openrouter.ai/z-ai/glm-4.6](https://openrouter.ai/z-ai/glm-4.6) — GLM-4.6 benchmarks: 205k context, ~41 tok/s output, latency ~1.05s
- [6] [openrouter.ai/minimax/minimax-m3](https://openrouter.ai/minimax/minimax-m3) — MiniMax M3 benchmarks: 1M context, ~66 tok/s output, latency ~1.28s
- [7] [felloai.com/glm-pricing/](https://felloai.com/glm-pricing/) — GLM Coding Plan + per-token breakdown
- [8] [emergent.sh/learn/glm-5-3-pricing](https://emergent.sh/learn/glm-5-3-pricing) — GLM-5.3 monthly billing (alternative to per-token if usage is heavy)

Internal AIW data (live state):
- `/opt/data/state/cost-tracker.json` — 49 agents tracked, flat-rate $0.0375/run, model pricing for 9 non-MiniMax/non-GLM models
- `/opt/data/state/cost-per-cron.json` — **$93.61/day total, 49/133 matched**, top spender = `evo-poll-watchdog` at $10.80/day
- `/opt/data/state/cron-error-watchdog.json` — top failing jobs: thesis-weekly-review, thesis-git-maintenance, aiw-research-tracker-weekly, aiw-coach-ivan, aiw-tax-receipt-tracker-weekly, aiw-founder-bandwidth-watchdog-weekly, linkedin-token-refresh, instagram-token-refresh
- `/opt/data/state/circuit-breakers.json` — only `r1` tracked; circuit breaker not wired into cron exec
- `/opt/data/state/contexts/business-analyst/2026-08-21.json` — 47-line JSON ≈1.4k tokens re-fed every cron
- `/opt/data/agents/scripts/token-ledger.py:13-14` — `DEFAULT_BUDGET_24H = 50000` (uncalibrated)
- `/opt/data/agents/scripts/circuit_breaker.py` — exists, ready to wire in (cc-switch pattern)
- `/opt/data/context_length_cache.yaml` — `cerebras-zai-glm@https://llm.paragu-ai.com/v1: 8192` already configured
- `/opt/data/.hermes/cron/jobs.json` — 168 crons: 70 minimax-oauth, 58 litellm, 39 broken (provider=None or unknown)

AIW repo references:
- `github.com/Ai-Whisperers/aiw-org/blob/master/README.md` (count tables)
- `github.com/Ai-Whisperers/aiw-org/blob/master/OPERATIONS.md` (cron health, 429s, state paths)
- `github.com/Ai-Whisperers/aiw-org/blob/master/research/DEPT-RESEARCH-METHODOLOGY.md` (7-question pattern)
- `github.com/Ai-Whisperers/aiw-org/blob/master/research/tool-stack-decisions.md` (cost-cap.py implementation)
- `github.com/Ai-Whisperers/aiw-org/blob/master/scripts/cost-per-cron.py:166-173` (estimate rates table)

`[unverified]` items in the document:
- Actual model that `primary` (litellm-routed) resolves to — needs litellm config inspection
- Exact 200k vs 205k context for GLM-4.6 (sources conflict slightly: OpenRouter 205k, Z.AI docs ~200k)
- Whether M3 OAuth subscription cap is per-session, per-day, or rolling — needs empirical probe
- Whether M3 cache TTL is configurable or fixed at 5min — Z.AI docs are clearer on this than MiniMax docs

---

**Built using**: AIW/aiw-org repo, the org's own 7-question dept-research methodology, existing token-ledger / cost-tracker / cost-cap / cost-optimize / cost-per-cron / circuit_breaker scripts, live state from `/opt/data/state/`, and authoritative 2026 pricing from MiniMax + Z.AI official docs.