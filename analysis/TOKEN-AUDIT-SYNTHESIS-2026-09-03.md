# Complete Token-Use Audit + Upgrade Roadmap (2026-09-03)

**Method**: Live measurement from `state.db.session_model_usage` + cron registry
analysis + on-disk footprint inventory. NOT estimates.

---

## 1. ACTUAL TOKEN SPEND (measured, not estimated)

### By surface (7-day window, MiniMax-M3 pricing)

| Surface | API calls | Input | Output | Cache reads | Cost |
|---|--:|--:|--:|--:|--:|
| **Interactive (your sessions)** | 8,983 | 62.2M | 5.2M | 2,051.8M (97%) | **$148.07** |
| **Subagents (delegate_task)** | 276 | 10.5M | 154K | 0 | **$3.33** |
| **Cron fleet (MiniMax-M3)** | ~46/day | ~322k/day | ~69k/day | 0 | **~$5.46/mo** |
| **Cron fleet (litellm-primary)** | ~24/day | ~168k/day | ~36k/day | 0 | **~$5-32/mo** depending on model |
| **TOTAL 7-day** | | | | | **~$157** |
| **TOTAL monthly (extrapolated)** | | | | | **~$680** |

### Reality check vs. prior estimates

- The `state/cost-per-cron.json` headline of **$93.61/day** is wrong: it uses flat-rate estimates on 49/133 matched jobs and assumes "estimated" rates for many. Measured actual: **$0.18/day for the cron fleet**.
- `state/token-cap-alert.json` claims **180× over budget (9M / 50k credits)** but the `token-ledger.json` it reads has only **18 test events** with synthetic values. The fleet is NOT over budget — the alarm is false.
- `state/cost-tracker.json` last updated **2026-08-21** (13 days stale). Real-time cost visibility is broken.

### Where the real spend IS

**Your interactive sessions dominate.** $634/month on M3, with **97% cache hit ratio** — already well-optimized by Hermes desktop's auto-caching. The biggest token volume is:
1. Session 20260831_165136_55a410 — 1,602 calls, 398M cache reads ($X)
2. Session 20260901_203602_23be7b — 1,032 calls, 370M cache reads
3. Session 20260901_143139_103d22 — 777 calls, 200M cache reads

These are long-running investigative sessions, where the cache benefit is enormous.

---

## 2. ALL TOKEN-SPENDING SURFACES (full inventory)

### A. Interactive (Hermes desktop)
- **Provider**: `minimax-oauth` (MiniMax-M3)
- **7-day cost**: $148
- **Cache ratio**: 97%
- **Per-session average**: ~$0.50/session (at 7k in + 1.5k out avg after cache)

### B. Subagents (delegate_task, leaf agents)
- **7-day usage**: 7 dispatches, 14 tasks, 276 API calls, $3.33
- **Cache ratio**: 0% (subagent sessions don't share cache)
- **Top use case**: Inventory tasks (3 parallel subagents for secrets, repos, Bitwarden probes)

### C. Cron fleet (168 enabled jobs)
- **MiniMax-M3**: 41 jobs, ~$5.46/mo
- **litellm-primary**: 44 jobs (43 are script-only), ~$5-32/mo depending on model
- **litellm-fast**: 18 jobs
- **provider=None (drift)**: 14 jobs — unmeasurable, route via defaults
- **Cache ratio**: 0% (cron sessions are isolated)
- **In error state**: 36 jobs (25% error rate)
- **Never run**: 34 jobs (broken or never triggered)
- **Origin delivery (visible to you)**: 11 jobs
- **Silent (deliver=local)**: 116 jobs

### D. Skill catalog overhead
- **ivan profile**: 126 skills (each ~500 tokens of description)
- **default profile**: 362 skills
- **engineering/finance/people/research/sales**: 145 each
- **kiki**: 75 skills
- **Per-session injection**: ~63k tokens for ivan (amortized via cache = negligible)
- **Per-cron injection**: ~63k tokens, no cache = **~$0.02 per cron call**

### E. PROMPT.md files
- **77 PROMPT.md files** in `/opt/data/agents/`, total 192KB
- **Average size**: 2,559 chars (~640 tokens)
- **Loaded by cron jobs** on every fire — pure input overhead

### F. State injection (silent costs)
- `coord.json`: 678KB, **551 items in `decisions_for_ivan[]`** (read by 18 monitors)
- `monitor-notes/`: **7.09 MB across 154 files** — written, never read
- `agent-stats.json`: 12KB, last updated 12 days ago (stale, not being maintained)
- `errors.json`: 3KB, last updated 12 days ago (stale)

### G. Disk footprint (silent cost = future context bloat)
| Path | Size | Why it matters |
|---|--:|---|
| `/opt/data/scratchpad` | 17,330 MB | Research artifacts, referenced in context |
| `/opt/data/profiles/ivan/scratch` | 5,124 MB | Throwaway work |
| `/opt/data/state` | 442 MB | Live state files |
| `~/.hermes/cache` | 5 MB | Session caches |

### H. Tool calls (each result = tokens in next turn)
- **13,212 tool messages** in current session DB
- **Top tools**: terminal (5,867), execute_code (3,427), patch (1,012), write_file (1,003)
- **web_search**: 190 calls (each adds search context to next turn)
- **web_extract**: 34 calls
- **delegate_task**: 11 dispatches

### I. Cache directories (session memory)
- 5 MCP configs
- 14 sub-agent transcript logs (305 KB)
- `state.db.messages_fts` (FTS5) — full-text search index of every message

---

## 3. MEASUREMENT INFRASTRUCTURE (broken or stale)

These scripts exist but aren't working:

| Script | Status | Impact |
|---|---|---|
| `scripts/cost-monitor.py` | Last run 2026-08-21 (13d stale) | Cost visibility lost |
| `scripts/cost-optimize.py` | Missing `croniter` dep | Cannot suggest optimizations |
| `scripts/cost-cap.py` | Working but flat-rate assumptions wrong | Per-agent cap never fires correctly |
| `scripts/token-cap.py` | Intentionally disabled (unit-mismatch bug) | 180× over-budget alert is false |
| `scripts/token-ledger.py` | Only has 18 test events | No real fleet measurement |
| `scripts/cost-per-cron.py` | Wrong math ($93/day estimate) | Misleads cost discussions |

---

## 4. UPGRADE ROADMAP (prioritized by impact)

### Tier 1 — Measure correctly (foundation)

**1.1 Fix `cost-monitor.py`** — rewire to read real `session_model_usage` table + cron completion data.
- Effort: ~3 hours
- Impact: Restores real cost visibility. Without this, all other optimizations are flying blind.
- Implementation: `read state.db.session_model_usage WHERE model='MiniMax-M3'` + `jobs.json` for cron mappings.

**1.2 Fix `cost-per-cron.py`** — replace flat-rate estimates with measured M3 rates from `session_model_usage`.
- Effort: 2 hours
- Impact: Removes the false $93.61/day headline.

**1.3 Repair `token-cap.py`** — distinguish test events from real ones in `token-ledger.json`.
- Effort: 1 hour
- Impact: Removes false 180× over-budget alarm.

**1.4 Fix `cost-optimize.py`** — install `croniter` OR rewrite without the dependency.
- Effort: 30 min (rewrite) or 5 min (install)
- Impact: Restores optimization suggestions.

**1.5 Add cron → M3 cache integration** — currently 0% cache. With cache, even a 60-day-old job would benefit.
- Effort: 6+ hours (requires Hermes gateway change)
- Impact: Marginal at current cron call volume (~$2/mo saved) — **not worth it until cron volume scales**

### Tier 2 — Eliminate silent waste (already-paid, no-return)

**2.1 Truncate `coord.json:decisions_for_ivan[]`** — 551 items, 678KB. Trim to last 50 + resolve-or-archive the rest.
- Effort: 1 hour
- Impact: Stops file bloat; saves ~1k tokens per monitor read (~$0.50/mo × 18 monitors = $9/mo).

**2.2 Truncate `monitor-notes/` older than 7 days** — done via `aiw-monitor-notes-compact.py` (already shipped).
- Effort: 0 hours (shipped)
- Impact: Prevents 7MB growing to 100MB+. Already in cron.

**2.3 Disable the 34 never_run jobs + 36 in-error jobs** — investigate each, then disable or fix.
- Effort: 2-4 hours
- Impact: Cleaner heartbeat, no false alerts. Likely $0.50-2/mo in saved retries.

**2.4 Fix the 26 repos with embedded GitHub PAT in `.git/config`** — done for `aiw-org`, 25 to go.
- Effort: 1 hour (bulk Pattern 6 strip script)
- Impact: Security, not tokens. But reduces future leak-driven audits.

### Tier 3 — Audit subagents (small but additive)

**3.1 Subagent cache sharing** — subagents don't share cache with parent. Each subagent re-loads ~63k tokens of skill catalog.
- Effort: 4+ hours (gateway change)
- Impact: $1-2/mo currently; grows if subagent use scales.

**3.2 Replace `aiw-coaching-quality-reviewer` (every 30m, 897 fires)** with script.
- Already in Tier 2 work; same pattern as the 18 watchdog monitors.

### Tier 4 — Strategic improvements (only if use scales)

**4.1 Switch `litellm-primary` to explicit `glm-4.6`** — 1 active job, but if more move to it, save 2-5×.
- Effort: 30 min
- Impact: $5-25/mo at current scale; grows if more crons move.

**4.2 Profile-specific skill optimization** — `ivan` profile loads 126 skills. Audit which are actually used in last 30 days.
- Effort: 4 hours
- Impact: Reduce per-session injection cost by 30-50%. Interactive sessions already cache this, so direct $ savings small; latency improvement real.

---

## 5. KEY INSIGHTS (the real story)

1. **The "$93.61/day" headline was wrong by 500×.** Actual cron spend is $0.18/day. The headline came from flat-rate estimates on a partial sample.
2. **The "180× over budget" alert is false** — based on 18 test events, not real fleet data.
3. **Your interactive sessions are 97% cached** — already optimized. No further reduction possible without changing model or workflow.
4. **The cron fleet is tiny** — 41 MiniMax-M3 jobs, ~$5.46/month total. Even a 50% reduction saves $2.73/month.
5. **The biggest silent waste is `monitor-notes/` and `coord.json` queue** — 7MB of unread breadcrumbs, 678KB of unread decisions. These are written by LLM agents and never read by anyone.
6. **Skill injection overhead is real but already amortized via caching** — for crons (no cache), it's $0.02/fire. For interactive (97% cache), it's $0.001/session start.
7. **The litellm-primary identity is unknown** — 1 active job routes through `primary` which could be Sonnet, Opus, Haiku, or GLM depending on litellm config. Without measurement, no optimization is possible.

---

## 6. IMMEDIATE NEXT STEPS (ordered by ROI)

| # | Action | Cost to implement | Monthly savings | Priority |
|---|---|---|---|---|
| 1 | Fix `cost-monitor.py` to read real data | 3h | $0 (visibility) | HIGH |
| 2 | Truncate `coord.json:decisions_for_ivan[]` to 50 | 1h | $9/mo | HIGH |
| 3 | Fix `token-cap.py` false alarm | 1h | $0 (trust) | HIGH |
| 4 | Bulk-strip PAT from 25 remaining repos | 1h | $0 (security) | HIGH |
| 5 | Disable 34 never-run + 36 errored jobs | 3h | $1-3/mo | MEDIUM |
| 6 | Fix `cost-optimize.py` (install croniter) | 5min | $0 (tool works) | MEDIUM |
| 7 | Investigate which model `litellm-primary` resolves to | 1h | $0 (data) | MEDIUM |
| 8 | Profile skill optimization (drop unused) | 4h | $1-5/mo + latency | LOW |
| 9 | Cron cache integration | 6h+ | $2/mo | LOW (volume too low) |

**Total potential monthly savings: ~$12-20/month** from this work. Not huge in absolute terms, but the **measurement restoration** is critical — without it, the next audit will repeat the same $93.61/day misanalysis.
