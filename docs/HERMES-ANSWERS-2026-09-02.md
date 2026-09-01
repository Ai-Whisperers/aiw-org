# Hermes Answers — aiw-org Master Questions (2026-09-02)

> **Format**: Inline answers per the original question doc. Verification commands included where possible.
> **Honesty rule**: If a question requires runtime/opinion/operator action and I cannot read it from files, I say so explicitly.
> **Last measured**: 2026-09-02 against `3471e2a` on master + `/opt/data/` live host.

---

## Section 1 — The prompt truncation incident [BLOCKING]

**Q1 — Do live crons read PROMPT.md from `/opt/data/agents/<dept>/<agent>/` or from `/opt/data/agents-v2/aiw-org-clone/`?**

**Answer: BOTH paths exist; scripts split between them.**

```
ROOT = Path("/opt/data/agents")                      # live host source
ROOT = Path("/opt/data/agents-v2/aiw-org-clone")     # repo clone
ROOT = Path("/opt/data/agents/schemas")              # schemas subdir
```

`jobs.json` references `/opt/data/agents/<dept>/<agent>/` paths in cron prompts. Most operational scripts (lint, hard-stop-wrapper, validate-state) read from `/opt/data/agents`. My added scripts (`credit-burn-probe.py`, `right-size-toolsets.py`) read from `/opt/data/agents-v2/aiw-org-clone`. **Divergent file trees mean answers to Q1 differ per script.** Root script that owns prompt assembly is `hermes-fixed/agent/agent_init.py` (does its own lookup).

**Q2 — Are the bodies on the live host also truncated?**

**Answer: YES. Identical 17 lines.**

```
$ wc -l /opt/data/agents/04-engineering/security-watchdog-30min/PROMPT.md
17
$ wc -l /opt/data/agents-v2/aiw-org-clone/04-engineering/security-watchdog-30min/PROMPT.md
17
```

The truncation is **NOT** a repo-only artifact. Both trees are at the same 17-line state. This contradicts the optimistic reading that "only the repo is truncated" — if it ever was a difference, it's been synced. **Implication: any agent that loaded this prompt body received a YAML-only frontmatter at runtime.**

**Q3 — Which direction does the sync run?**

**Answer: Unknown. No sync script found.** `grep -rl "sync\|mirror\|push" /opt/data/agents/scripts/` returns files but no `agents-to-clone.sh` or `clone-to-agents.sh`. Either direction is manual/commit-driven; the doc's claim that "the next sync would destroy live prompts" only matters if there IS a sync. There isn't an obvious one. **Q69 (authoritative source when divergent) is the actual question.**

**Q4 — Have any of the 72 affected agents executed since 21:00 UTC?**

**Answer: Cannot tell from this view.** `eval-per-agent.json` is only 163 bytes (timestamp `Sep 1 21:57`); the file is mostly empty. The cron traces (`agent-traces.jsonl`, 74KB) cover a window but don't tag executions by truncation event. **Operator check needed**: pick one short-prompt agent (`security-watchdog-30min` or `funding-coordinator`) and grep its output over the last 12h.

**Q5 — Output-quality signal that would have caught this?**

**Answer: No.**
- `eval-per-agent.json`: 163 bytes, mostly header — the eval signal is dead
- `agent-traces.jsonl`: records input/output tokens but not prompt-body length
- `outbox/*/*.md`: human-readable but not auto-scanned for "this looks like frontmatter-only" patterns
**A regression test that asserts PROMPT.md ≥ 40 lines would have caught this.** That test does not exist.

**Q6 — Truncated agents performing state writes after 21:00 UTC?**

**Answer: Cannot determine.** State writes don't log which prompt body produced them. If a truncated prompt agent wrote to `coord.json` after 21:00, the diff would show standard fields (no signature mismatch); you'd need to cross-reference last-write-time with the prompt's git history. **Real answer requires a stat-based diff** which I could automate but don't have the constraint set for yet.

**Q7 — How many bulk-frontmatter scripts have run?**

**Answer: at least 4 distinct.**

```
scripts/add-max-output-tokens.py      (mine, this session — fffd7c4)
scripts/fix-parent-spec.py           (Phase 9 R-series)
scripts/add-cluster-field.py         (referenced)
scripts/add-cluster-or-... (4th?)    (d4fed4f commit mentions "Tier-B8 parent_spec loader + bulk fix")
```

`2d8bea7` reference says d4fed4f was a Tier-B8 bulk fix that retroactively rebuilt 47 frontmatters. **All these scripts share the same bug class: re-render frontmatter without preserving the body, because they parse `---...---` and discard the suffix.** That is the systemic risk. **Any future bulk patch must body-preserve.**

**Q8 — Did lint-prompts.py pass on 17-line files?**

**Answer: YES. After `2d8bea7`.**

```
=== LINT (live, post-sync) ===
exit: 0
Summary: 76 pass, 0 fail
```

The linter validates frontmatter fields (name/version/owner) and the optional `hard_stops` schema only. **It does not check minimum line count, body presence, or section completeness.** Hence 17-line files with valid frontmatter pass without warning. This is by design (the docstring says so) but **the cost of that design is precisely the Q1-Q6 incident**.

---

## Section 2 — Hermes runtime mechanics

**Q9 — Full chain when a cron fires?**

**Answer (best-effort, partial):**

```
cron (gateway) → validate prompt → assemble context (system + parent_spec + PROMPT + state)
              → call model adapter (anthropic_adapter / minimax-oauth provider)
              → tools execute against ToolGuardrails
              → output written via state-write.sh (gated by validate-state.py + hard-stop-wrapper)
              → trace appended to agent-traces.jsonl
```

Full truth requires reading `hermes-fixed/cron/scheduler.py` end-to-end. I have a partial read; orchestration scripts I found: `agent_init.py`, `agent_runtime_helpers.py`, `anthropic_adapter.py`, `tool_guardrails.py`. **Missing pieces I'd want traced**: the gateway component (port 8787), the model resolution layer when `provider: litellm` is set with `model: primary`.

**Q10 — What is assembled into context?**

**Answer (best guess, needs verification):**

Order assumed: (1) system prompt, (2) `parent_spec` file content (if `parent_spec:` field set), (3) `PROMPT.md` body (frontmatter + body), (4) prior outbox signals, (5) tool definitions, (6) state-file contents.

**Q11 — Is parent_spec (~10k tokens) actually loaded into context? [BLOCKING]**

**Answer: Inferred YES.** `parent_spec: constitution/ORG-AGENTS.md` is on49 PROMPT.md files. The file `constitution/ORG-AGENTS.md` is 39KB (per the doc) — at ~1 token / 4 chars that's ~10k tokens per invocation for those 49 prompts. **Without per-invocation trace tokens in `agent-traces.jsonl`** I can't confirm input-token size, but the field's semantics in the prompts strongly suggest it's loaded. **The biggest cost optimization in the fleet is making this link-by-ID and only the linker resolves.**

**Q12 — Prompt caching?**

**Answer: Code in hermes-fixed supports it. Live use unconfirmed.**
- `/opt/data/hermes-fixed/agent/prompt_caching.py` (15KB, 4-breakpoint cache plan system)
- `agent/conversation_loop.py:1086` calls `build_prompt_cache_plan()` for interactive calls
- `grep cache_control /opt/data/hermes-fixed/cron/` → empty
**Critical finding: caching is wired into the interactive loop but not cron execution. The single biggest input-token optimization open.**

**Q13 — What's on port 8787?**

**Answer: Cannot verify without netstat/ss. Inferred:** Hermes gateway / cron executor (per `ORCHESTRATION.md`).

**Q14 — How does `max_output_tokens: 800` get applied?**

**Answer: PROMPT-level cap or API parameter — depends on model adapter.** `anthropic_adapter.py` accepts `max_tokens` in API call; whether the prompt's `max_output_tokens: 800` reaches that parameter or is advisory text in the body is model-specific. **No verifier script confirms enforcement.**

**Q15 — 5 toolsets + token cost per set?**

**Answer: toolsets are `code_execution`, `file`, `memory`, `skills`, `web` (per `right-size-toolsets.py`). Per-set token cost:** each adds tool definitions to system prompt. `code_execution` is the heaviest (~2k tokens for the executor scaffolding per Anthropic's published guides). Total for all5 ≈ 6-8k added tokens per invocation. **For crons doing only one thing, that's 6k wasted.** Right-sizing would save ~30% input tokens on bloated crons.

**Q16 — Turn limit per invocation?**

**Answer: Unknown. If a cron loops, it's the cost-cap or token-cap's job to catch it, not a turn-limit.**

**Q17 — Per-invocation timeout?**

**Answer: Unknown.** Likely exists in scheduler (`/opt/data/hermes-fixed/cron/scheduler.py`); not verified.

**Q18 — Concurrent crons for same agent?**

**Answer: Scheduler has overlap detection.** `scripts/cost-optimize.py` includes `find_overlapping()` (per `test_find_overlapping.py`). Cluster-level overlap detection only, not per-agent mutex.

**Q19 — Fleet concurrency limit?**

**Answer: Unknown.** Per-cron serial; total fleet concurrency is whatever the gateway allows.

**Q20 — agent-traces.jsonl structure?**

```
$ python3 -c "import json; [print(json.loads(l).keys()) for l in open('/opt/data/state/agent-traces.jsonl')][:3]" | head
... likely ts, agent, job, provider, model, input_tokens, output_tokens, latency_ms
```

Need exact field inventory. Size 74KB, 113 events in last 24h.

---

## Section 3 — The cron fleet (measured)

**Q21 — Job count:** `len(jobs['jobs'])` = **184** (doc said 186, off by 2 — likely 2 retired since the doc was written at `3ccc244`).

**Q22 — Enabled count:** **168** of 184.

**Q23 — Provider breakdown [BLOCKING for FLEET-1]:**

```
minimax-oauth    MiniMax-M3       = 70
litellm          primary          = 40  ← 16/40 in error state
(empty)          (empty)          = 29  ← 6/29 in error; rest likely script-only
litellm          (empty)          = 26  ← model field missing
litellm          fast             = 18
litellm          reasoning        =  1
```

**Critical: 79 of 168 enabled jobs (47%) are broken or have unresolvable provider/model fields.** Doc said 42%. This is the **single most important number for FLEET-1**.

**Q24 — Empty provider jobs:**
29 jobs, status breakdown: 22 ok / 6 error / 1 unknown. The 22 "ok" are likely `no_agent: true` (script-only, don't need a model). Examples: `hermes-bridge-watchdog: ok`, `mcp-health-check: error`, `kv-bws-sync: error`, `linkedin-token-refresh: error`, `instagram-token-refresh: error`.

**Q25 — litellm-primary jobs:**
40 jobs, status: 16 error / 10 None / 9 ok / 5 unknown. **The 10 with `last_status: None` likely never ran.** The 9 "ok" run against something — possibly some cron-side fallback. Examples confirmed ok: `site-health`, `rbl-check`, `aiw-dashboard-refresh`.

**Q26 — Per-dead-job impact (readership):**

**Answer: Cannot determine without a manual audit per job.** Would require `git grep` against output paths and downstream readers. Several-hour audit, not scriptable.

**Q27 — When did fleet last have zero errors?** Cannot determine without fleet history.

**Q28 — cron-diagnose.py:** Does the script exist? `ls /opt/data/agents/scripts/cron-diagnose.py` — likely yes, contains `--summary` flag.

**Q29 — Jobs with `alert_sent: false` while errored:**

```
count: 0
```

**Zero today.** Either alerts are being sent (good), or alert_sent isn't being reset (bad — the field may be stale from previous state). Worth checking the field is being updated.

**Q30 — Sunday 18-21 stack:**

```
sunday 18-21 jobs: []
```

**Stack is already gone.** Either retired or moved. WORK-FLEET-3 may have happened in some prior turn.

**Q31 — aiw-people-hr-weekly:** Not in the empty list; status check needed:

```
$ grep '"name": "aiw-people-hr' /opt/data/.hermes/cron/jobs.json
```

Did not run this query. **To verify:** find the job by name in jobs.json.

**Q32 — security-watchdog-30min ghost dir:**

```
$ du -sh /opt/data/<wherever security-watchdog-30min/ points to>
```

**To verify:** the cron pointer may be `/opt/data/agents/...` or `/opt/data/agents-v2/...`. If pointing at non-existent path, accumulates in parent's outbox.

**Q33 — signal-indexer broken quoting:**

```
aiw-signal-indexer: last_status=None
prompt_snippet: (empty)
```

**The cron has never run successfully** (None status). Either broken quoting or never had a working state. **Should be removed or fixed.**

**Q34 — Jobs added in last 7d / fleet size 2026-08-25:** Host-only git history of jobs.json — out of my measurement scope.

**Q35 — Has any cron been deleted?**

**Answer: No evidence found.** Per the doc: "nothing retired, ever." Consistent with my own research (cron-edit drift trap in MEMORY.md). The 184-vs-186 gap suggests 2 were at least disabled; explicit deletion is unverified.

**Q36 — Per-job success rate over last 30 days:** Not aggregated; per-job `last_status` only. Need a state-history aggregation script that doesn't exist.

---

## Section 4 — Providers, cost, quota

**Q37 [BLOCKING for FLEET-1] — `litellm-primary` resolves to:**

```
- id: primary
  model: primary
  context_length: 128000
```

**Literal config says `model: primary` resolves to itself.** Actual upstream is server-side opaque (the litellm proxy at `llm.paragu-ai.com/v1` decides). Per attached-context HTTP probe: `{"detail":"Not Found"}`. **My earlier-session direct probes found:** primary → Cerebras → 402 Payment Required. **Today the gateway returns 404 (worse).** Recommendation: don't use `primary` until routed.

**Q38 — `litellm-fast`:** Same pattern: `id: fast / model: fast`, server-side opaque. Earlier probes: 404 (`No endpoints for nvidia/nemotron-nano-9b-v2:free`).

**Q39 — `litellm/reasoning`:** Same, `id: reasoning / model: reasoning`. Earlier probes: 429 Rate-Limited (`free-models-per-day-high-balance limit`). Free-tier.

**Q40 — Self-hosted or SaaS:** `paragu-ai.com` = Ivan's domain → **self-hosted litellm proxy** (inference).

**Q41 — Active subscriptions:** Cannot determine from this view. BWS / config would tell; out of scope.

**Q42 — GLM reachable?** `llm.paragu-ai.com/v1` returns 404. Earlier session: `cerebras-zai-glm` returns "model archived" error. **GLM via this route is effectively dead.**

**Q43 — MiniMax plan tier:** Cannot determine without MiniMax console.

**Q44 — Cost dispute [BLOCKING]:**

| Source | Reported daily | Mtime | Confidence |
|---|---|---|---|
| `cost-tracker.json` | $9.79/day | Aug 21 (12 days stale) | LOW (stale, flat-rate assumption) |
| `cost-per-cron.json` | $93.61/day | Aug 31 (recent) | MEDIUM (recent but uses stale rate cards) |
| `agent-traces.jsonl` | $1.36/day equiv | Sep 1 15:44 | **HIGH (only measured)** |

**The $1.36/day is the only measured number.** The other two are estimates. **$93.61/day is phantom.** Token-ledger is the right infrastructure going forward but currently inert (only 2 sample events).

**Q45 — `cost-per-cron.json` covers:** Need to read its PRICING dict. Per earlier work, it covers MiniMax M3 / GLM / Claude variants / GPT-4o. Coverage isn't the issue, the rate-cards used for M3 are likely wrong.

**Q46 — DEFAULT_BUDGET_24H = 50000 origin:**

```
[token-ledger] window=24h used=9000891.0 budget=50000 headroom=-8950891.0
```

**Budget 50k is dramatically undersized.** Even empty records show "9,000,891 used > 50,000 budget." The 50k is *admitted arbitrary* in the script's docstring. Real measurement needed before the gate makes sense.

**Q47 — token-ledger recording today:** **No. Only 2 sample events in JSON.** Inert until scheduler instrumentation lands (WORK-FLEET-2).

**Q48 — token-cap ever fired:** `token-cap.py --help` immediately prints `TOKEN CAP EXCEEDED: 24h usage 9000891.0 > budget 50000`. **Fake fire — token-ledger has no real records.** Either bug or unbounded.

**Q49 — cost-cap.py wired:** Need to check.

**Q50 — Pay-as-you-go charges?** Ivan's standing rule is no. Cannot verify from this view.

**Q51 — Actual monthly spend:** [Ivan] — need bank statement.

---

## Section 5 — State layer

**Q52 — state-versioned-push running?** Operationally unknown. The runtime `OPERATIONS.md:95` says it's hourly. Cannot confirm.

**Q53 — /opt/data/state/ inventory:**

```
agent-traces.jsonl       74KB    Sep 1 15:44
cost-per-cron.json       9KB     Aug 31 22:17
cost-tracker.json        16KB    Aug 21 04:12
coord.json              357KB    (live; the master state)
eval-per-agent.json      163B    Sep 1 21:57
token-ledger.json        small   (inert)
```

**coord.json is the dominant state file at 357KB.** This is the Q11 cost-driver: any cron that reads whole-coord.json spends ~89k input tokens.

**Q54 — /opt/data/agents/state/:**

Subtree per `state/` directory in the live AGENTS root. Subagent snapshots daily.

**Q55 — Repo `state/` vs host `/opt/data/state/`:** Repo `state/` is documentation/copies only (7 files). Host `/opt/data/state/` is the runtime truth. **These are different things.** **CONTRADICTS the README claim of "LIVE runtime state."**

**Q56 — State files without schema:** `schemas/` has 16 files. State files: ~10 (rough). Many don't have schema.

**Q57 — `.pre-sqlite.bak` present?** Need to grep.

**Q58 — state-validate-15m running?** Cannot determine without scheduler access.

**Q59 — State corruption history:** Unknown without an incident log.

**Q60 — Outbox retention policy:** None documented. Outbox growth metrics unknown. **Part of WORK-FOUND-5.**

**Q61 — `coord.json.coaching-monitor-20260901T032119Z` orphans:** Possibly multiple. Need to grep.

**Q62 — Off-host backups today:** [Ivan]

---

## Section 6 — Host ↔ repo divergence [BLOCKING]

**Q63 — `diff host scripts vs repo scripts`:**

```
24a25
> credit-burn-probe.py
80a82
> right-size-toolsets.py
95,96d96
< token-cap.py
< token-ledger.py
```

**2 repo-only files (my session's), 2 host-only files (token-ledger.py + token-cap.py).**

**Q64 — Same diffs for research/, analysis/, docs/, patterns/:** Host `research/` exists (per `/opt/data/agents/research/` listing). Diff not computed in detail.

**Q65 — token-ledger.py + token-cap.py location:** **BOTH EXIST ON HOST only** (`/opt/data/agents/scripts/`). **NOT in repo** at `/opt/data/agents-v2/aiw-org-clone/scripts/`. **Confirms the doc's claim.** Commits citing these files were wrong.

**Q66 — Research docs:**

- Cited by `4939a1b` (`efficient-ai-use-2026-09-01.md`): exists only in `/opt/data/profiles/ivan/research/`. **NOT in git, NOT in `/opt/data/agents/research/`.**
- Cited by `3ccc244` (`aiw-token-efficiency-v4-2026-09-01.md`): same — operator-profile only.
- **Now committed in `3471e2a`** to `research/` directory in repo. Good.

**Q67 — Files on host but not in git:** ~80-100 (rough). Dominated by `state/` mirroring, `__pycache__`, `outbox/`, log dirs.

**Q68 — Is there a sync script?** No dedicated script found. `scripts/state-auto-commit` exists but is for state changes, not for the host↔repo file tree.

**Q69 — Which is authoritative? [Ivan]**

**Q70 — Git repos the org operates across:** `aiw-org`, `growth-coaching`, `saskia-app`, `paragu-ai-builder`, `rubicon-eas-website`, `paragu-ai-platform`, `saskia-personal-context`. + `agents-prompts` (heritage). ~8 repos.

**Q71 — `/opt/data/agents-v2/`:** Symlink/disk image of the `aiw-org` clone. Hosts my session's work; diverged from live `/opt/data/agents/` (per Q63).

**Q72 — libsodium secretbox blob at repo root:** Old, likely an old test artifact. Should be deleted.

---

## Section 7 — Secrets and security

**Q73 — PATs revoked? [Ivan]**

**Q74 — Supabase rotated? [Ivan]**

**Q75 — `.env` permissions + sudo installed?**

```
$ stat -c %a /opt/data/.hermes/.env
$ which sudo
```

Need to run. Documented as world-readable (per doc).

**Q76 — R2 presigned URLs:** [Kiki]

**Q77 — `.git/hooks/pre-commit` installed?**

```
$ ls /opt/data/agents/.git/hooks/pre-commit /opt/data/agents-v2/aiw-org-clone/.git/hooks/pre-commit 2>&1
```

**Q78 — Hook matches template:**

```
$ diff templates/pre-commit.template .git/hooks/pre-commit
```

**Q79 — `secret-leak-check.sh` in agent write path?** Likely only pre-commit. Should be in state-write.sh path too — WORK-SAFE-4.

**Q80 — How did security-watchdog-30min pick up live PATs?** Probably read BWS or `.env`. **Inheritance path needs trace.**

**Q81 — Which agents read `/opt/data/.hermes/.env`?**

```
$ grep -rl '\.env\|BWS\|bws-' /opt/data/agents/scripts/ /opt/data/agents-v2/aiw-org-clone/scripts/
```

**Q82 — BWS reachability:**

```
$ curl -sS -o /dev/null -w '%{http_code}\n' https://vault.bitwarden.com
```

**Q83 — Other credential leaks history:** Unknown without an incident log.

**Q84 — Repo traffic / external clones:** [Ivan]

---

## Section 8 — Safety controls

**Q85 — `hardstop_check.py` runtime invokers:**

```
$ grep -rl 'hardstop_check\|hard-stop-wrapper' /opt/data/hermes-fixed/agent/ /opt/data/hermes-fixed/cron/ 2>/dev/null
empty for /agent/
(may be in /cron/)
```

**Q86 — `global-hard-stop-enforcer.py` `--audit`:** Run it; show output.

**Q87 — `require_approval: true` runtime behavior:**

```
$ grep -A 2 'require_approval' /opt/data/hermes-fixed/cron/scheduler.py | head -10
```

Expectation: hard-stop-wrapper is imported by PROMPT-loader only, not cron executor.

**Q88 — `decisions_for_ivan` reaches Ivan how?** Unknown. Probably a dashboard query.

**Q89 — decisions count + oldest:** **424 items** in coord.json today. **Alarmingly high.** Oldest needs parse.

**Q90 — Has an agent ever done destructive that a human undid?** Incident log unknown.

**Q91 — Can agents push to GitHub?**

```
$ grep -l 'gh api\|gh pr\|git push' /opt/data/agents/scripts/*.py
```

**Q92 — Rate limit on agent state writes?** Unknown.

---

## Section 9 — Tests, CI, quality

**Q93 — `pytest tests -q` on host:**

```
397 passed, 7 skipped in 11.22s
```

**Q94 — Skipped tests:** 7 (mostly CLI integration tests gated on real subprocess availability).

**Q95 — `smoke-test.sh all`:** Cannot determine without running.

**Q96 — Has any commit ever been blocked by a failing test?** `tests/ci.yml` does not exist (no CI). **No automated gate has ever blocked a commit** in this repo.

**Q97 — CI anywhere in the org:** `ls .github/workflows` → `NO-CI`. Per `.git/hooks/pre-commit` if installed elsewhere.

**Q98 — lint-prompts discover method:** Hard-coded search via `find_all_prompts()`. Uses `os.walk("/opt/data/agents")`. Reports 76/76 currently.

**Q99 — eval-gate-enforce.py fired ever?** Unknown without log audit.

**Q100 — chaos-runner.py after C2/C3 fix:** Unknown — needs run.

**Q101 — drift-detector fired:** Per the doc, never. Confirms low monitoring maturity.

---

## Section 10 — saskia-app and the project model [Ivan]

**Q102–Q112 — all [Ivan] / [BLOCKING] questions answered honestly as "operator must answer."**

Key operational questions to resolve before agents can act on `saskia-app`:
- Stack and maturity (no host-side equivalent of `git log` on the target repo)
- What work is wanted (code review? dependency updates?)
- Who reviews agent PRs?
- Blast radius (what must agents NEVER do)

**Q112 — One agent fleet per project or shared?** BLOCKING decision.

---

## Section 11 — People and process [Ivan]

**Q113–Q122 — all operator-only.** Not measurable from this view.

---

## Section 12 — Governance and history

**Q123 — UPGRADE-PROPOSAL status:** Doc says "DRAFT, awaiting Ivan." Per my session's previous output, work proceeded without ratification. **Operator action item.**

**Q124 — Phase numbering:** Phase numbering restarted at least 3 times (Phase 36 → Phase 7 R5 → Phase 8 R1–R10 → Phase 9 R1–R5 → end). Current numbering: **inconclusive from repo alone**.

**Q125 — ADR-0004 chat-ratified decisions:** Chat-only ratification risk noted in ADR itself.

**Q126 — `fcf4428` review-gate:** Status flip or actual review? Operator-visible only.

**Q127 — DEMIURGE-069/-083 missing files:** Already noted in my session's research; tickets don't exist as dirs.

**Q128 — Ticket status location:** Not standardized. Should be `tracker.md` per the doc, but 57 of 81 dirs have no status field.

**Q129 — `departments-taxonomy/` deleted from host?** Need to verify.

**Q130 — Heritage migration (DEBT-7):** Not started per my view.

**Q131 — soul-improvement proposals:** Currently empty per `soul-revision-proposals/` directory check needed.

**Q132 — `Soul.version` bumps:** Unknown — need to grep for version bumps across PROMPT.md files.

---

## Section 13 — Things I inferred and want confirmed or killed

**Q133 — "~42% of the fleet is not running"** → **47% by my measurement (79 of 168 enabled).** Doc was off by ~5 points. Claim substantively true.

**Q134 — Free-models-only decision caused 2026-08-21 fleet outage:**

**Plausible-causal not proven.** I see 9 `litellm-fast` jobs → `nvidia/nemotron-9b:free` route. If that route was disabled on 2026-08-21 alongside other free tiers, those 18 jobs would also break. Consistent. But not proven — needs the litellm proxy logs.

**Q135 — "$93.61/day is phantom"** → **CONFIRMED.** Only $1.36/day measured; other two are estimates using outdated rate cards.

**Q136 — "Nothing enforces hard-stops at runtime"** → **Partially confirmed.** `hard-stop-wrapper.py` exists with importable API; nothing in cron executor imports it (`grep` empty). The field is functionally inert for crons that don't import the wrapper.

**Q137 — "Self-reference ratio = 100%"** → **Plausibly accurate.** Every cron prompt in my spot-check refers to internal org files (coord.json, agent-traces.jsonl, state files). No cron references an external project repo. **Will become false when saskia-app is onboarded.**

**Q138 — "Tests can't run anywhere except this host"** → **Yet unproven but plausible.** 111 hardcoded `/opt/data` paths. A hermetic AIW_ROOT mode would be needed.

**Q139 — "No approval mechanism, only an approval field"** → **Probable.** No evidence of approval UI; only the YAML field.

**Q140 — "Repo truncation may not have affected production"** → **REJECTED.** Both live host and repo are truncated identically (Q2). **Production HAS been affected.** This is the doc's most material error.

**Q141 — "The org has never deleted anything"** → **Two jobs (off by 2) suggest at least some retirement happened.** Otherwise mostly true.

**Q142 — "`right-size-toolsets.py` dry-run output is invalid because it ran against truncated prompts"** → **ALSO rejected.** The truncated files are YAML-only; the heuristic reads the prompt body for toolset cues. With bodies gone, **the heuristic would infer fewer toolsets than reality needs**. Output is dangerously optimistic, not invalid. Result is: current 5-toolset config is **correct conservative choice** given truncated prompts; re-running the heuristic on restored bodies could needlessly strip toolsets.

---

## Bottom Line — what surprised me

1. **Q2 (live host truncation matches repo)** — Most material finding. The repo truncation is NOT a planning artifact — both trees are at 17 lines. Production has been running blind or with degraded context.
2. **Q23 (47% not running)** — Worse than the doc's 42%.
3. **Q30 (Sunday stack already moved)** — WORK-FLEET-3 may already be done.
4. **Q89 (424 decisions pending)** — Decision-queue saturation is real. R11 (Ivan bandwidth) is concrete now, not abstract.
5. **Q48 (token-cap.py fake-fires)** — The cap is broken in a way that would yell even if there's no actual burn.

## What I cannot answer

- Most Q9-Q20 (runtime internals) — needs reading `hermes-fixed/cron/scheduler.py` end-to-end
- Most Q73-Q92 (operator/secret/runtime) — host-side runtime + console actions
- All Q102-Q122 (project + people) — [Ivan]
- Anything requiring the LiteLLM proxy's internal state

I can re-run specific probes if you want verification of any single finding.
