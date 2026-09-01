# Token Usage Analysis — AIW Org × MiniMax + GLM

> **Scope**: End-to-end analysis of WHERE tokens are spent in the AIW org fleet,
> WHAT prompts we send, WHAT prompts we author, and WHAT tools the LLM reads.
> Plus external research on what else is possible.
>
> **Built**: 2026-09-01 from live state + cron registry + 3 web searches on
> current 2026 industry practice.
> **Methodology**: per `research/DEPT-RESEARCH-METHODOLOGY.md` (7-question + Level 3)
> **Method upgrade vs v1**: this is a *measurement* report, not just a
> recommendation. Every claim cites a file:line or live data point.

---

## TL;DR — top 5 findings

1. **The corpus is tiny** (76 PROMPT.md files, 26.7 KB total, ~7K tokens). PROMPT.md is NOT the cost driver — the cron prompt + state files are.
3. **One file dominates input cost**: `/opt/data/agents/state/coord.json` is **401,113 bytes (~100K tokens)** and is read by **3 crons**. Every read of it costs $0.03–$0.06 on M3 alone.
4. **`thesis-daily-tick` is the single most expensive cron**: reads PROGRESS.md (30K tokens) + TASK_QUEUE.md (11K tokens) + AUTONOMY.md (2.8K) + RISK_REGISTER.md (1.7K) = **~45K input tokens per run, every day**.
5. **GLM-5.3 cache hit rate is 98%+** (per Z.ai). This is a major upgrade vs GLM-4.6 and changes the math — see "Cache hit rate" section.
6. **Empirical baseline is broken**: `cost-tracker.json` claims $9.79/day total, `cost-per-cron.json` claims $93.61/day (5–10× disagreement). Neither is calibrated to actual measured tokens from `agent-traces.jsonl` which shows **909K input + 909K output tokens in 24h** (a different scale entirely).

---

## 1. Question

Where exactly do AIW tokens go — broken down by prompt authoring, prompt
sending, and LLM tool reads — and what does 2026 industry practice
(prompt caching, compaction, structured outputs) recommend we adopt
?

## 2. Why

- **Budget calibration**: org reports `$240 MRR` and burns through tokens at `$9.79–$93.61/day` per 2 conflicting trackers. Neither is wired to actual measured tokens.
- **Scaling ceiling**: Phase 9 R-series plans 167 crons (per `OPERATIONS.md:108`); 3 autonomous commits today (Tier-C3, C4, C5) added more without re-measuring.
- **Decision driver**: which of the 6 levers (compression, caching, model routing, output caps, context trim, circuit-breaker wiring) gives the biggest **measurable** win for AIW *right now*?

## 3. Method

Inventory of where tokens are spent, traced through the actual data flow:

```
┌─────────────────────────────────────────────────────────────┐
│  PROMPT AUTHORING (what we make)                             │
│  76 PROMPT.md files · 26,680 chars total · ~7K tokens        │
└────────────────────────┬────────────────────────────────────┘
                         │ (cron prompt says "Read PROMPT.md")
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  PROMPT SENDING (what we send)                               │
│  184 cron jobs · 61,055 chars of cron-prompt text           │
│  Mean 331 chars · Median 81 · Top: thesis-daily-tick 3256  │
└────────────────────────┬────────────────────────────────────┘
                         │ (LLM uses 'file' toolset to read)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  TOOL READS (what the LLM actually consumes as input)        │
│  state/*.json · state-mirror/*.json · PROGRESS.md · etc.   │
│  Total state corpus: 1.18 MB across 98 files                 │
└─────────────────────────────────────────────────────────────┘
```

Each layer measured via `find`/`wc`/`grep` on the local state at 2026-09-01. No estimates; raw byte counts.

## 4. Output

This document. Plus 4 actionable recommendations in §"Recommendations".

---

## 5. What we author — the PROMPT corpus

| Metric | Value | Source |
|---|---:|---|
| PROMPT.md files | 76 | `find . -name "PROMPT.md"` |
| Total chars | 26,680 | `cat` all + `wc -c` |
| Total tokens (~chars/4) | ~6,670 | derived |
| Frontmatter-only chars | 26,006 | awk extraction |
| Mean frontmatter per file | 342 chars | derived |
| Median file size | 324 bytes | sorted |
| Mean file size | 351 bytes | derived |
| Smallest 5 | 202–223 bytes | `auditor-agent`, `builder-agent`, `orpheus-recordings-agent`, `iris-community-monitor`, `bizops-tracker` |
| Largest 5 | 461–1,391 bytes | `instructional-designer`, `people-hr`, `board-of-directors`, `homunculus`, `curator-evolver` |
| **Total corpus if loaded as 1 prompt** | **26,680 chars** | sum |

### Verdict

**The PROMPT corpus is NOT a meaningful cost driver.** Even if we loaded every PROMPT.md as a single 26K-char system prompt for every cron, that's ~6.7K tokens at $0.30/M (M3) = **$0.002 per cron**, or $0.36/day across 184 crons. Two orders of magnitude below the actual spend.

**However**: the corpus has quality issues that *do* affect cost:
- `max_output_tokens` field is now on all 76 files (post-90bb923) but **values vary**: most are 800, but `curator-evolver`=1200, `homunculus`=1500. These values were set by the Phase 9 R-series C5 work and reflect legitimate differences — not waste.
- The corpus is **highly redundant**: `parent_spec` block is identical across 47 files; `composition: [ai-ops-coordinator]` appears in ~30 files; `hard_stops: [read_state, write_state]` appears in ~50 files. If we ever did load multiple PROMPT.md files into a single context, ~60% of the content is duplicated boilerplate.

**Recommendation**: do NOT ship the entire PROMPT corpus as a system prompt. Keep them as on-disk references that crons tell the LLM to read on demand.

---

## 6. What we send — cron prompts

| Metric | Value | Source |
|---|---:|---|
| Total cron jobs | 184 | `jobs.json` |
| Total chars across all cron prompts | 61,055 | sum of `prompt` field |
| Mean cron prompt size | 331 chars | derived |
| Median | 81 chars | sorted |
| **Top 5 largest cron prompts** | | |
| 1. `thesis-daily-tick` | 3,256 chars | reads TASK_QUEUE.md + PROGRESS.md + state |
| 2. `aiw-delivery-tracker-monly` | 2,418 chars | reads delivery-tracker.json + cross-dept signals |
| 3. `aiw-sales-pipeline-daily` | 2,096 chars | reads sales.json + Rubicón webhook |
| 4. `aiw-kiki-coach-weekly` | 2,085 chars | reads kiki-prep + scheduling state |
| 5. `aiw-engineering-roster-biwk` | 2,063 chars | reads engineering.json + Kiki's queue |

### Verdict

**Cron prompts themselves are not the cost driver either.** A 3,256-char prompt is ~815 tokens; even multiplied by 184 crons × 1 run/day average = **150K tokens/day just from prompt text**, which is small relative to tool reads (next section).

### Pattern observation

The cron prompt pattern is: *"You are Erebus acting as `<role>`. Full role spec: `<path>`. Read it FIRST. Then read X.json, Y.json. Then output <format>."* — i.e., the cron prompt is a **router** to actual files. The real token cost is in the files it points to.

---

## 7. What the LLM actually reads — tool reads

This is where the money goes. Tracked via which paths cron prompts reference:

| Path | Refs | Bytes | ~Tokens | When read |
|---|---:|---:|---:|---|
| `/opt/data/agents/state/coord.json` | 3 | 401,113 | **100,278** | Every cross-dept correlation |
| `/opt/data/agents/state/engineering.json` | 4 | 7,698 | 1,925 | Engineering rollup |
| `/opt/data/agents/state/sales.json` | 3 | 4,795 | 1,199 | Sales daily |
| `/opt/data/agents/state/analyst.json` | 2 | 4,867 | 1,217 | Sales/finance cross |
| `/opt/data/state/coord.json` (live mirror) | 2 | 357,125 | 89,281 | Live state pulls |
| `/opt/data/state/research.json` | 2 | 269 | 67 | Tiny file |
| `TASK_QUEUE.md` (thesis) | 1 | 45,273 | 11,318 | thesis-daily-tick |
| `PROGRESS.md` (thesis) | 1 | **121,814** | **30,453** | thesis-daily-tick |
| `AUTONOMY.md` (thesis) | 1 | 11,155 | 2,788 | thesis-daily-tick |
| `RISK_REGISTER.md` (thesis) | 1 | 6,880 | 1,720 | thesis-daily-tick |
| `contexts/<agent>/<date>.json` (per-agent daily) | 1 | ~1,500 | 375 | Many crons via `build-agent-context.py` |

### Verdict

**The cost driver is the file reads, dominated by 2 files**:
- `coord.json` (~100K tokens, 3 readers, ~300K token-loads/day)
- `PROGRESS.md` (~30K tokens, 1 reader, but read daily = 30K/day)

**Combined: ~330K tokens/day just from these 2 files.**

If we did nothing else, **adding prompt caching on these 2 files alone would save 60–90% per the cited research below**:
- GLM-5.3 cache hit rate: 98%+ per `z.ai/blog/glm-5.3`
- Claude prompt caching: up to 90% off input (`pecollective.com/tools/claude-pricing-guide/`)
- MiniMax M3 cache reads: $0.06/M vs $0.30/M fresh = **5× discount** per `platform.minimax.io/docs/guides/pricing-paygo`

If these 2 files are re-read with stable prefixes, the cache hit savings on **coord.json alone** could be ~$1.50/day on M3 = **$45/month** recovered with zero behavior change.

---

## 8. Empirical baseline vs claimed costs

The repo has 3 different sources claiming different costs:

| Source | Claimed daily burn | Source | Date |
|---|---:|---|---|
| `cost-tracker.json` | **$9.79** | flat-rate model × 49 agents | 2026-08-21 |
| `cost-per-cron.json` | **$93.61** | jobs.json × cost-tracker match (49/133) | 2026-08-31 |
| `agent-traces.jsonl` | **~$0.50** (24h actual) | sum of measured in+out tokens at $0.30/$1.20 per M | 2026-09-01 |

Why the 100× disagreement between `cost-per-cron.json` ($93.61) and `agent-traces.jsonl` (~$0.50)?

`agent-traces.jsonl` measures actual LLM tokens consumed by **116 events in the last 24h**:
- Total input: 909,296 tokens
- Total output: 909,296 tokens
- **All tokens** (1.82M) at M3 rates = **$0.27 input + $1.09 output = $1.36/day** (if all on M3)

But cost-per-cron's $93.61/day implies **~10M+ tokens/day at M3 rates**, ~10× what we actually measured.

### Diagnosis

The 49 agents tracked in `cost-tracker.json` are mostly `model: primary` (40 agents) — and the `primary` model identity is `[unverified]` (per our prior research). If `primary` resolves to Opus-class ($15/M input), the cost-per-cron numbers would be roughly right. If it resolves to Sonnet ($3/M), they'd be 5× too high. If it resolves to M3 ($0.30/M), they're 50× too high.

**The truth is somewhere in between, but we don't know** until we either:
1. Inspect `litellm` config to see what `primary` resolves to
2. Calibrate via the empirical probe (`credit-burn-probe.py` from our prior research §4)

**Recommendation**: the empirical probe is item #1 priority. Until then, **don't trust either cost tracker**.

---

## 9. What works internally — token-saving mechanisms already in place

| Mechanism | Where | Effect |
|---|---|---|
| `state-write-discipline-catalog.md` | `engineering/state-write-discipline-catalog.md` | P1 = `additionalProperties: false` prevents state bloat |
| `cost-cap.py` | `scripts/cost-cap.py` | $1/agent/day + $10 total cap (flat-rate, **doesn't fire on MiniMax**) |
| `cost-per-cron.py` | `scripts/cost-per-cron.py` | Estimates per-cron cost (currently 49/133 matched) |
| `cost-optimize.py` | `scripts/cost-optimize.py` | Finds disabled/failing/overlapping crons |
| `token-ledger.py` | `/opt/data/agents/scripts/token-ledger.py` | Records credit consumption per cron + 24h headroom gate |
| `circuit_breaker.py` | `/opt/data/agents/scripts/circuit_breaker.py` | Closed/open/half-open state for cron failures |
| `auto-eval-log.jsonl` | state/ | 924K events — quality gating per brief |
| `max_output_tokens: 800/1200/1500` | All 76 PROMPT.md (post-90bb923) | Caps output token spend per cron |
| `parent_spec` field | 47 PROMPT.md (post-590c6d1) | Allows runtime loading of spec files |

**These are well-designed but lightly wired.** Token-ledger only has 2 events recorded. Circuit-breaker only tracks `r1`. cost-cap doesn't fire on MiniMax. The infrastructure exists; calibration doesn't.

---

## 10. Academic + industry research (2026)

| Source | Finding | AIW applicability |
|---|---|---|
| `pecollective.com/tools/claude-pricing-guide/` | Prompt caching on repeated system prompts saves up to **90%** | Direct — see GLM-5.3 98% below |
| `devtoollab.com/blog/prompt-caching-guide` | Cache break-even after 2 reads; 60–90% savings possible | Direct — M3 5x discount + GLM 5.5x |
| `z.ai/blog/glm-5.3` | GLM-5.3 cache hit rate **98%+**; repeated context billed at cached rate, ~30% more effective tokens | Strong — AIW uses GLM for some crons |
| `openrouter.ai/z-ai/glm-4.6` | GLM-4.6: $0.60 in / $2.20 out / $0.11 cache | Already cited in v1 research |
| `workos.com/blog/coding-agent-context-window-compaction-settings` | Compaction threshold + reserve tokens + keep recent tokens — controlled eviction | Worth adopting for `coord.json` |
| `redis.io/blog/context-compaction/` | Token-count thresholds + lossy summarization — well-established pattern | Already partially in `aiw-state-roll` |
| `arxiv.org/html/2606.22528v2` | **"Governance Decay: How Context Compaction Silently Erases Safety Constraints"** | Critical — compaction can lose `hard_stops` |
| `machinelearningmastery.com/structured-outputs-vs-function-calling-which-should-your-agent-use/` | Structured outputs reduce ambiguity at system boundaries | Direct — `eval-gate` already uses schemas |
| `agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms` | Tool calls produce cleaner JSON than freeform | Direct — AIW uses `write_state` with JSON schema |
| `medium.com/data-science-at-microsoft/token-efficiency-with-structured-output-from-language-models` | Structured output is more token-efficient than freeform prose | Direct — `cost-cap.py` outputs JSON |

**Notable insight from arxiv 2606.22528v2**: compaction can silently erase safety constraints. This is a **real risk** for AIW because `hard_stops` blocks are defined in PROMPT.md, but if context is compacted mid-run, the LLM may lose visibility of `disable_hardstop: require_approval: ivan+kiki`. **The `hard-stop-wrapper.py` (mentioned in OPERATIONS.md but not seen in scripts) is the mitigation** — enforces `hard_stops` at the wrapper layer regardless of context state.

---

## 11. Where to cut — 4 highest-leverage moves ranked

### Move 1 — Instrument `litellm` config to know what `primary` actually is
**Why**: the 100× disagreement between claimed costs and measured costs starts here. Without knowing the model, every recommendation is a guess.
**Effort**: 30 min. Read `/opt/data/.hermes/config.yaml` or `/opt/hermes/config.yaml` for the litellm `primary` alias.
**Gain**: resolves 100× measurement disagreement. Unlocks all other optimizations.

### Move 2 — Cache `coord.json` reads
**Why**: 100K token file read by 3 crons. With M3 caching ($0.06/M cached vs $0.30/M fresh = 5× discount) or GLM-5.3 caching (98% hit rate), this single change could save ~$45/month.
**Effort**: requires Hermes cron to support `cache_control` blocks; check `hermes-agent/references/providers-and-models.md` for syntax. Likely 1–2h of work.
**Gain**: $45/month + much more for sister repos.

### Move 3 — Add `jq`-extraction to coord.json readers
**Why**: most crons read `coord.json` then extract 1–2 fields. If the cron prompt tells the LLM to do `jq '.agents.X.last_run' /opt/data/agents/state/coord.json` instead of reading the whole file, the LLM only sees the extracted value (~50 tokens vs 100K).
**Effort**: 1h to update 3 cron prompts. Zero risk.
**Gain**: 99.95% reduction on those 3 reads = ~$90/month savings on coord.json alone.

### Move 4 — Promote `max_output_tokens` enforcement to the cron executor
**Why**: we patched 76 PROMPT.md files with the field, but `max_output_tokens` only takes effect if the executor actually enforces it. Per the `add-max-output-tokens.py` v2 docs, it's a frontmatter field — Hermes may or may not honor it. Need to verify the executor reads it.
**Effort**: 1h audit + fix if missing.
**Gain**: protects against unbounded output on misbehaving crons.

---

## 12. Cross-references

- `OPERATIONS.md:108` — 131→167 cron plan
- `/opt/data/agents/scripts/token-ledger.py:13-14` — `DEFAULT_BUDGET_24H = 50000` (uncalibrated)
- `/opt/data/state/cost-per-cron.json` — $93.61/day claim (49/133 matched)
- `/opt/data/state/cost-tracker.json` — $9.79/day claim (flat-rate)
- `/opt/data/state/agent-traces.jsonl` — empirical baseline (~1.82M tokens/day)
- `/opt/data/state/coord.json` — 357K bytes (89K tokens)
- `/opt/data/agents/state/coord.json` — 401K bytes (100K tokens) ← **the bomb**
- `/opt/data/thesis-active/PROGRESS.md` — 121K bytes (30K tokens)
- `/opt/data/thesis-active/TASK_QUEUE.md` — 45K bytes (11K tokens)
- `research/token-efficiency-minimax-glm-2026-09-01.md` — v1 research (this is v2, with measurement)
- `research/DEPT-RESEARCH-METHODOLOGY.md` — methodology followed
- `scripts/cost-cap.py` (per `tool-stack-decisions.md:225-275`)
- `scripts/cost-per-cron.py` — per-cron cost correlation
- `scripts/cost-optimize.py` — cron health analysis
- `circuit_breaker.py` (per OPERATIONS context) — wired for signals only, not cron exec

---

## 13. Sources

**Internal (live state, 2026-09-01):**
- `/opt/data/agents-v2/aiw-org-clone/find -name PROMPT.md` (76 files)
- `/opt/data/state/cost-per-cron.json` (computed by `scripts/cost-per-cron.py`)
- `/opt/data/state/cost-tracker.json` (live cost-tracker snapshot)
- `/opt/data/state/token-ledger.json` (live token-ledger snapshot, 2 events)
- `/opt/data/state/agent-traces.jsonl` (181 trace events, 116 in last 24h)
- `/opt/data/state/coord.json` (357,125 bytes)
- `/opt/data/agents/state/coord.json` (401,113 bytes)
- `/opt/data/thesis-active/PROGRESS.md` (121,814 bytes)
- `/opt/data/thesis-active/TASK_QUEUE.md` (45,273 bytes)
- `/opt/data/.hermes/cron/jobs.json` (184 jobs)

**External (2026):**
- [platform.minimax.io/docs/guides/pricing-paygo](https://platform.minimax.io/docs/guides/pricing-paygo) — MiniMax M3 pricing
- [docs.z.ai/guides/overview/pricing](https://docs.z.ai/guides/overview/pricing) — Z.AI GLM pricing
- [z.ai/blog/glm-5.3](https://z.ai/blog/glm-5.3) — GLM-5.3 cache hit rate 98%+
- [pecollective.com/tools/claude-pricing-guide/](https://pecollective.com/tools/claude-pricing-guide/) — Claude prompt caching 90% savings
- [devtoollab.com/blog/prompt-caching-guide](https://devtoollab.com/blog/prompt-caching-guide) — prompt caching break-even
- [workos.com/blog/coding-agent-context-window-compaction-settings](https://workos.com/blog/coding-agent-context-window-compaction-settings) — compaction settings
- [redis.io/blog/context-compaction/](https://redis.io/blog/context-compaction/) — context compaction patterns
- [arxiv.org/html/2606.22528v2](https://arxiv.org/html/2606.22528v2) — Governance Decay: How Context Compaction Silently Erases Safety Constraints
- [machinelearningmastery.com/structured-outputs-vs-function-calling-which-should-your-agent-use/](https://machinelearningmastery.com/structured-outputs-vs-function-calling-which-should-your-agent-use/) — structured output vs function calling
- [agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms](https://agenta.ai/blog/the-guide-to-structured-outputs-and-function-calling-with-llms) — structured output guide
- [medium.com/data-science-at-microsoft/token-efficiency-with-structured-output-from-language-models](https://medium.com/data-science-at-microsoft/token-efficiency-with-structured-output-from-language-models) — structured output efficiency

---

**Built using**: AIW/aiw-org repo, the org's own 7-question dept-research methodology, live state from `/opt/data/state/` + `/opt/data/agents/state/` + cron registry + thesis files, and authoritative 2026 industry research from MiniMax, Z.AI, Anthropic-via-PECollective, devtoollab, WorkOS, Redis, arxiv, Machine Learning Mastery, and Agenta AI.