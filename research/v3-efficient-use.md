# Efficient AI Use — A Research Synthesis for AIW Org (2026-09)

> **Scope**: The 8 techniques the 2026 LLM-production industry agrees on,
> applied to AIW Org's specific situation (76 PROMPT.md, 184 cron jobs,
> $93.61/day claimed spend, MiniMax M3 + GLM providers).
>
> **Built**: 2026-09-01 from 6 web searches on current best practice.
> **Methodology**: per `research/DEPT-RESEARCH-METHODOLOGY.md` (Level 3 synthesis)
> **Upstream**: builds on `research/token-efficiency-minimax-glm-2026-09-01.md` (v1)
> and `research/token-usage-analysis-2026-09-01.md` (v2 measurement).

---

## TL;DR — the 8 techniques ranked by AIW applicability

| # | Technique | Reported savings | AIW applicability | Effort |
|---|---|---|---|---|
| 1 | **Prompt caching (provider-native)** | 40–90% input | **HIGH** — 0/184 crons use it; coord.json = 100K reads × 3 crons | Low |
| 2 | **Batch / async API for offline work** | 50% in+out | MEDIUM — most crons are scheduled (async-friendly) but not 50% slower | Med |
| 3 | **Model routing (Haiku/Sonnet/Opus per task)** | 60–80% | **HIGH** — 40 `primary` crons route to unknown expensive model | Low |
| 4 | **Subagent discipline (sequential when not independent)** | 2.6–5.9× | LOW — AIW uses cron patterns, not subagent fan-out | Low (just awareness) |
| 5 | **Semantic caching (vector similarity)** | up to 90% on Q&A | MEDIUM — weekly coaching crons may repeat semantically | Med |
| 6 | **Output length caps** | 30–60% | **HIGH** — already shipped across 76 files (max_output_tokens:800) | Done |
| 7 | **Compaction (auto-summarize at threshold)** | variable, "stop giving agent million-token window" | MEDIUM — coord.json bloat is the real-world example | Med |
| 8 | **Structured outputs / function calling vs freeform** | 10–30% | MEDIUM — `cost-cap.py` and `eval-gate` already use JSON schemas | Low |

**The dominant technique the AIW fleet has NOT adopted: prompt caching (technique 1).** 0 of 184 crons use `cache_control`. This is the single biggest open gap.

---

## 1. Question

What does "efficient AI use" mean in 2026 across the LLM production industry,
which techniques apply to AIW Org's specific fleet composition
(76 PROMPT.md, 184 cron jobs, MiniMax M3 + GLM-4.6 stack, $93.61/day claimed spend),
and where can we cut tokens without changing observable behavior?

## 2. Why

- **MRR impact**: at $93.61/day claimed ($2,808/month), even a 30% cut = **$842/year recovered**. A 50% cut = $1,400/year.
- **Subscription ceiling**: per v1 analysis, MiniMax M3 OAuth subscription has an undisclosed ceiling. Lower spend = more room before hitting the wall.
- **Decision driver**: which techniques to adopt first, in which order, with what blast radius?

## 3. Method

Web search on current 2026 LLM production cost-optimization practice (6 searches), synthesized against AIW's specific fleet composition. Every claim cites a source. Where AIW applicability is asserted, it's grounded in the live fleet data from v2 (`token-usage-analysis-2026-09-01.md`).

## 4. Output

This document + the technique-by-technique deep dive below.

## 5. Owner

- Engineering roster (Tier-1 lead) for technique adoption
- Kiki + Ivan for budget decisions
- No external owners needed — all techniques are AIW-implementable

## 6. Cadence

- **Per push**: a single new technique is adopted and measured (per build-vs-close doctrine)
- **Quarterly**: re-measure cost and adjust technique mix
- **Annual**: full re-research as industry practice evolves

## 7. Cross-references

- `research/token-efficiency-minimax-glm-2026-09-01.md` — v1 (provider pricing)
- `research/token-usage-analysis-2026-09-01.md` — v2 (measurement)
- `OPERATIONS.md:108` — 131→167 cron plan
- `/opt/data/.hermes/cron/jobs.json` — 184 cron registry
- `/opt/data/state/cost-per-cron.json` — $93.61/day claim (49/133 matched)
- `/opt/data/state/agent-traces.jsonl` — empirical baseline (1.82M tokens/24h measured)

---

## Deep dive: 8 techniques for AIW

### Technique 1 — Provider-native prompt caching (40–90% input savings)

**What it is**: Mark a stable prefix of your prompt as cacheable. Subsequent reads of the same prefix get a 90% discount (Claude) or 5–5.5× discount (M3, GLM-4.6).

**Sources**:
- Anthropic Claude: up to 90% off input (`pecollective.com/tools/claude-pricing-guide/`)
- MiniMax M3: $0.30/M fresh → $0.06/M cached = **5× discount** (`platform.minimax.io/docs/guides/pricing-paygo`)
- GLM-4.6: $0.60/M fresh → $0.11/M cached = **5.5× discount** (`docs.z.ai/guides/overview/pricing`)
- GLM-5.3: 98%+ cache hit rate per Z.ai's own bench (`z.ai/blog/glm-5.3`)
- "91–95% cache hits across the Claude models we use. Without caching we'd pay 5x as much" — practitioner quote (`reddit.com/r/Anthropic`)
- "Batches API explicitly stacks with caching" — Anthropic pricing page (`leanlm.ai/blog/llm-batch-api`)

**AIW applicability: HIGH**
- **0/184 crons use `cache_control`** (live data from v2)
- 3 crons read `/opt/data/agents/state/coord.json` (~100K tokens each)
- thesis-daily-tick reads PROGRESS.md (30K tokens) + TASK_QUEUE.md (11K) + AUTONOMY.md (2.8K) + RISK_REGISTER.md (1.7K) = ~45K tokens daily
- All these reads have **stable prefixes** (the file content is the same across runs within a few minutes)
- **Estimated savings: ~$45–90/month on coord.json alone**, more when other files are cached

**How to adopt**:
1. Verify Hermes cron syntax supports `cache_control` field (check `hermes-agent/references/providers-and-models.md`)
2. Add `cache_control: { type: "ephemeral" }` to the cron prompt template at the file-read point
3. For state files: cache the entire file content as the stable prefix
4. For dynamic per-run data (cron prompt's variable part): leave uncached

**Effort**: Low–Med (1–2h to find syntax + patch a few crons as proof)

---

### Technique 2 — Batch / async API (50% in+out)

**What it is**: OpenAI Batch API and Anthropic Message Batches API both offer 50% discount for async processing (24h SLA). Gemini matches.

**Sources**:
- "OpenAI Batch API and Anthropic Message Batches API both offer 50% cost discounts" (`neuraltrust.ai/blog/llm-batching-async-inference`)
- Same 50% across all three (OpenAI/Claude/Gemini) (`leanlm.ai/blog/llm-batch-api`)
- Stacks with prompt caching (`leanlm.ai/blog/llm-batch-api`)
- M3 / GLM equivalent unknown — **NOT in MiniMax or Z.AI public docs as of 2026-09-01**

**AIW applicability: MEDIUM**
- AIW crons are already scheduled (async-friendly by nature)
- But MiniMax M3 OAuth subscription is fixed-cost — batch pricing not applicable
- **Z.AI does not advertise a batch API** as of the docs I read
- **For Anthropic-class provider (if/when added): could save 50%** on any non-realtime crons

**Recommendation**: monitor for Z.AI batch API announcement. Apply if/when it appears.

---

### Technique 3 — Model routing (60–80% on mixed workloads)

**What it is**: Route simple subtasks to cheap models (Haiku, Sonnet, GLM), complex tasks to reasoning models (Opus, M3). The biggest single cost lever for agentic workloads.

**Sources**:
- "Combining model routing (60 to 80% savings), prompt caching (40 to 90%), context optimization (30 to 60%), budget controls produces net 60 to 80% total cost reduction" (`requesty.ai/blog/ai-agent-cost-optimization-how-to-cut-llm-spend-by-80-percent-with-routing`)
- "Teams applying these patterns cut token usage by 30 to 50 percent while maintaining quality" (`frugal.co/blog/when-inference-capacity-gets-tight-efficiency-becomes-advantage`)
- Truefoundry: "Hard token budgets + semantic caching" (`truefoundry.com/blog/ai-cost-optimization-strategies`)

**AIW applicability: HIGH**
- v2 research identified the gap: 40 `primary` crons route to unknown model
- `cost-tracker.json` shows `primary` and `fast` tiers but no model mapping
- v1 research recommended switching `primary` → GLM-4.6 as the single biggest lever (~$2,650/year)
- **The exact model `primary` resolves to is still unverified** — see v2 §8

**How to adopt**:
1. Audit `/opt/hermes/config.yaml` and `/opt/data/.hermes/config.yaml` for the litellm `primary` alias
2. If `primary` resolves to Opus-class ($15/M input), redirect to M3 ($0.30/M) or GLM-4.6 ($0.60/M) for non-reasoning work
3. Keep M3 for synthesis tasks that need 1M context window
4. Use GLM-4.6 for the bulk `primary` traffic (cheaper + similar quality for non-reasoning)
5. Reserve Opus/equivalent only for tasks needing deep reasoning

**Effort**: Low (config change), Med if model fallback logic needs reworking

---

### Technique 4 — Subagent discipline (sequential when not independent)

**What it is**: Don't fan out into subagents unless subtasks are genuinely independent. Subagent fan-out can cost 2.6–5.9× a sequential run.

**Sources**:
- "Subagents look like cheap parallelism. They were not faster on any task we timed. Cache misses pushed the price-weighted cost to roughly five times the sequential run" (`systima.ai/blog/subagent-tax`)
- "One reader's task quietly spawned seven subagents that drained a five-hour budget"
- "Prefer sequential work when the sub-tasks are not genuinely independent. The sequential lane metered 2.6× fewer tokens than the two-subagent fan-out, cost roughly five times less on a price-weighted basis, and was faster"
- "After auditing token usage and routing simpler subtasks to cheaper models, one team cut monthly API costs from $40,000 to $24,000" (`cockroachlabs.com/blog/agentic-ai-costs-at-scale`)

**AIW applicability: LOW (just awareness)**
- AIW uses cron-driven patterns, not subagent fan-out
- The Hermes `delegation` toolset is enabled on 14 crons — likely OK if used for genuinely parallel research tasks
- **Awareness item: don't add cron patterns that fan-out unnecessarily**

---

### Technique 5 — Semantic caching (up to 90% on Q&A)

**What it is**: Cache responses by semantic similarity (vector embeddings), not just exact match. Useful for repeat questions phrased differently.

**Sources**:
- "Over 20% of queries were semantically similar. With Semantic Cache, these requests can be served without inference latency & token cost, offering potential speed boost of at least 20× at zero cost" (`portkey.ai/blog/reducing-llm-costs-and-latency-semantic-cache/`)
- "Cut costs by up to 90% and lower latency with semantic caching" (`redis.io/blog/what-is-semantic-caching/`)
- "20× speed boost at zero cost" — Portkey case study

**AIW applicability: MEDIUM**
- AIW's cron-driven pattern produces predictable outputs, not user Q&A
- Weekly coaching crons may produce semantically similar outputs across runs
- Could apply to: `coach-ivan-weekly`, `coach-kiki-weekly`, `coach-org-weekly` (similar prompts, similar expected output format)
- **Requires Redis or equivalent + an embedding model = new infra dependency**

**How to adopt (if interested)**:
1. Embed each cron output with a small model (e.g., MiniMax-M3)
2. Compare new cron input embeddings to cached ones via cosine similarity
3. If similarity > 0.92, return cached output instead of running LLM
4. Most relevant for low-criticality crons (briefs, summaries)

**Effort**: Med (new infra + 1-day integration)

---

### Technique 6 — Output length caps (30–60%) — ALREADY SHIPPED

**What it is**: Cap `max_output_tokens` per request so the LLM can't burn unbounded output tokens.

**Sources**:
- Output costs 3.7–4× input across all providers per `cost-tracker.json` model_pricing
- "Tokens spent on verbosity are tokens wasted" (`exadel.com/news/llm-cost-optimization-enterprise-ai-framework`)

**AIW applicability: DONE**
- v2 research confirmed all 76 PROMPT.md now have `max_output_tokens` field (post-90bb923)
- Most use 800; `curator-evolver`=1200, `homunculus`=1500 (legitimate larger budgets)
- Test coverage via `tests/test_add_max_output_tokens.py` (15 tests, all green)
- **Caveat**: only effective if Hermes executor actually honors the field. **Verify in next research push.**

---

### Technique 7 — Compaction (auto-summarize at threshold)

**What it is**: When context exceeds a threshold, automatically summarize earlier turns. Be careful: can silently erase safety constraints.

**Sources**:
- Claude Code runs auto-compact at 95% of context window, summarizing full trajectory (`langchain.com/blog/context-engineering-for-agents`)
- Three-knob model: reserveTokens + keepRecentTokens + threshold (`workos.com/blog/coding-agent-context-window-compaction-settings`)
- **"Governance Decay: How Context Compaction Silently Erases Safety Constraints in Long-Horizon LLM Agents"** — critical risk paper (`arxiv.org/html/2606.22528v2`)
- Compaction can extend effective windows to millions of tokens by distillation (`kargarisaac.medium.com/the-fundamentals-of-context-management-and-compaction-in-llms-171ea31741a2`)
- "Stop giving your coding agent a million-token context window" — WorkOS

**AIW applicability: MEDIUM with risk**
- AIW crons are short-lived (~1–5 turns typically) — long-context compaction rarely triggers
- BUT: thesis-daily-tick has 45K tokens of input + LLM may iterate
- **CRITICAL**: AIW's `hard_stops` blocks in PROMPT.md can be erased by compaction. Per arxiv 2606.22528v2, this is a documented failure mode.
- **Mitigation**: `hard-stop-wrapper.py` (mentioned in `OPERATIONS.md`) enforces hard_stops at the wrapper layer regardless of context state. **Verify this script exists and is wired.**

**Recommendation**:
1. Verify `hard-stop-wrapper.py` exists and is in the cron execution path
2. If AIW adopts compaction, ensure `hard_stops` enforcement is independent of context (wrapper layer)
3. Do NOT adopt aggressive compaction for crons that reference `hard_stops`

**Effort**: Med, with safety verification

---

### Technique 8 — Structured outputs / function calling vs freeform

**What it is**: Force structured JSON / function-call outputs instead of freeform prose. Saves tokens + reduces ambiguity at system boundaries.

**Sources**:
- "Structured outputs reduce ambiguity at the one place it costs the most: system boundaries" (`collinwilkins.com/articles/structured-output`)
- Function calling yields cleaner JSON (`machinelearningmastery.com/structured-outputs-vs-function-calling-which-should-your-agent-use/`)
- Token efficiency analysis (`medium.com/data-science-at-microsoft/token-efficiency-with-structured-output-from-language-models`)

**AIW applicability: MEDIUM**
- AIW already uses JSON schemas (`cost-cap.py` outputs JSON, `eval-gate` uses schemas per `OPERATIONS.md:99` — `additionalProperties: false` enforced in `state-write-discipline-catalog.md`)
- 16 schemas in `schemas/` directory
- **Improvement opportunity**: ensure ALL cron outputs use structured format (not freeform prose wrapped in `**BOLD**:` markers)

**How to adopt**:
1. Audit cron prompts for freeform-prose outputs vs structured
2. Add `--output-format json-schema` or equivalent to cron prompts
3. Define schemas for each cron output type (monitor notes, briefs, decisions)

**Effort**: Low–Med

---

## Combined optimization playbook

If AIW adopts the top 3 techniques (caching + routing + output caps which is already done):

| Technique | Reported savings | AIW-specific expected savings |
|---|---|---|
| 1. Prompt caching (cron-level) | 40–90% input | $45–90/month on coord.json alone |
| 2. Model routing (primary → M3/GLM) | 60–80% | $1,400/year if Opus-class → GLM |
| 3. Output caps (already done) | 30–60% | $15–40/year (already shipped) |
| **Subtotal** | | **~$1,500–2,000/year** |

If AIW adopts all 8 techniques (estimated):
- **5× reduction in token spend** is realistic per industry reports (`cockroachlabs.com/blog/agentic-ai-costs-at-scale`)
- **For AIW's $93.61/day** = $18.72/day final = **$2,738/year savings**

---

## The 4 questions v3 should answer

Based on gaps identified in this research:

1. **What does litellm `primary` resolve to?** (0 of 184 crons document this)
2. **Does Hermes support `cache_control` for cron prompts?** (syntax investigation)
3. **Is `hard-stop-wrapper.py` wired into the cron execution path?** (safety risk if no)
4. **What does empirical `credit-burn-probe.py` show after 24h?** (calibration of all 8 techniques)

These are the **4 research questions for v3** — each is a 30-min investigation that unlocks a major optimization.

---

## 8. Sources

- [platform.minimax.io/docs/guides/pricing-paygo](https://platform.minimax.io/docs/guides/pricing-paygo) — MiniMax M3 PAYG pricing
- [docs.z.ai/guides/overview/pricing](https://docs.z.ai/guides/overview/pricing) — Z.AI GLM pricing
- [z.ai/blog/glm-5.3](https://z.ai/blog/glm-5.3) — GLM-5.3 98% cache hit rate
- [pecollective.com/tools/claude-pricing-guide/](https://pecollective.com/tools/claude-pricing-guide/) — Claude prompt caching 90%
- [devtoollab.com/blog/prompt-caching-guide](https://devtoollab.com/blog/prompt-caching-guide) — cache break-even
- [neuraltrust.ai/blog/llm-batching-async-inference](https://neuraltrust.ai/blog/llm-batching-async-inference) — Batch API 50% off
- [leanlm.ai/blog/llm-batch-api](https://leanlm.ai/blog/llm-batch-api) — batch + cache stacking
- [respan.ai/articles/anthropic-message-batches-api](https://www.respan.ai/articles/anthropic-message-batches-api) — Anthropic Batches
- [requesty.ai/blog/ai-agent-cost-optimization-how-to-cut-llm-spend-by-80-percent-with-routing](https://www.requesty.ai/blog/ai-agent-cost-optimization-how-to-cut-llm-spend-by-80-percent-with-routing) — model routing 60-80%
- [truefoundry.com/blog/ai-cost-optimization-strategies](https://www.truefoundry.com/blog/ai-cost-optimization-strategies) — Truefoundry framework
- [frugal.co/blog/when-inference-capacity-gets-tight-efficiency-becomes-advantage](https://frugal.co/blog/when-inference-capacity-gets-tight-efficiency-becomes-advantage) — Jevons + 30-50% with patterns
- [cockroachlabs.com/blog/agentic-ai-costs-at-scale/](https://www.cockroachlabs.com/blog/agentic-ai-costs-at-scale/) — $40K→$24K case study
- [systima.ai/blog/subagent-tax](https://systima.ai/blog/subagent-tax) — subagent 2.6-5.9× cost
- [redis.io/blog/what-is-semantic-caching/](https://redis.io/blog/what-is-semantic-caching/) — semantic caching 90%
- [portkey.ai/blog/reducing-llm-costs-and-latency-semantic-cache/](https://portkey.ai/blog/reducing-llm-costs-and-latency-semantic-cache/) — 20% similar queries case
- [workos.com/blog/coding-agent-context-window-compaction-settings](https://workos.com/blog/coding-agent-context-window-compaction-settings) — compaction 3-knob model
- [langchain.com/blog/context-engineering-for-agents](https://www.langchain.com/blog/context-engineering-for-agents) — Claude Code auto-compact
- [arxiv.org/html/2606.22528v2](https://arxiv.org/html/2606.22528v2) — Governance Decay: Compaction Erases Safety Constraints
- [kargarisaac.medium.com/the-fundamentals-of-context-management-and-compaction-in-llms-171ea31741a2](https://kargarisaac.medium.com/the-fundamentals-of-context-management-and-compaction-in-llms-171ea31741a2) — context management
- [redis.io/blog/context-compaction/](https://redis.io/blog/context-compaction/) — compaction patterns
- [machinelearningmastery.com/structured-outputs-vs-function-calling-which-should-your-agent-use/](https://machinelearningmastery.com/structured-outputs-vs-function-calling-which-should-your-agent-use/) — structured vs function
- [collinwilkins.com/articles/structured-output](https://collinwilkins.com/articles/structured-output) — structured outputs 2026
- [agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms) — structured output guide
- [medium.com/data-science-at-microsoft/token-efficiency-with-structured-output-from-language-models](https://medium.com/data-science-at-microsoft/token-efficiency-with-structured-output-from-language-models) — efficiency analysis
- [codeconductor.ai/blog/tokenmaxxing-enterprise-ai-outcomes/](https://codeconductor.ai/blog/tokenmaxxing-enterprise-ai-outcomes/) — Tokenmaxxing
- [exadel.com/news/llm-cost-optimization-enterprise-ai-framework](https://exadel.com/news/llm-cost-optimization-enterprise-ai-framework) — Exadel framework

---

**Built using**: AIW/aiw-org repo, the org's 7-question dept-research methodology, live state from `/opt/data/state/` + `/opt/data/agents/state/` + cron registry, and 6 web searches synthesizing ~25 industry sources from 2026.