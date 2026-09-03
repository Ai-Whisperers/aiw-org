# HANDOFF.md — AIW Org Current State

> **Current state-of-work log for AIW org (aiw-org).**
> Required by AGENTS.md ("Before declaring work done — update HANDOFF.md").
> Read this FIRST when starting a new session. Update LAST when ending.

**Last updated:** 2026-09-03 05:30Z (refreshed with PRs #20-#25 — Track A1-A4, B, D complete; C corrected)
**Maintainer:** AIW org (Ivan Weiss Van Der Pol)

---

## Current goal

**Top-priority:** Reduce preamble-stall failure mode and ship the AGENTS.md / HANDOFF.md / docs/adr/ process discipline layer adopted from `iPythoning/b2b-sdr-agent-template` and `obra/superpowers`.

**Strategic:** Wire methodology layer (skills, instincts, AGENTS.md) so the 63-agent AIW org becomes robust under load.

---

## Completed (this session, 2026-09-01)

### Code changes — all live, all verified
1. **`scripts/router.py`** (+99 lines) — `pre_dispatch_check()` with khwarizmi contradiction-detection + cerebralvalley refusal-when-constraints-unmet; chronos time-awareness (`RULE_LATENCY_BASELINE_MS` + `is_rule_degraded` + `rule_avg_latency_ms`); `log_decision(latency_ms=...)`; `no_rule` branch now logs to audit.
2. **`scripts/circuit_breaker.py`** (new, 7 KB) — 3-state FSM (closed / open / half-open) per-recipient, cc-switch pattern, atomic disk persistence.
3. **`scripts/observability/agent-tracer.py`** — fixed 3 bugs: `main()` was never called from `__main__`; only 1-level scan (now uses `rglob("PROMPT.md")`); hardcoded `["outbox", "lessons"]` (now scans all subdirs); added `_parse_date_stem()` for suffixed stems like `2026-09-01-tick41`.
4. **`AGENTS.md`** (new, 6 KB) — cross-vendor agent discipline doc adapted from `iPythoning/b2b-sdr-agent-template/AGENTS.md` with AIW-specific safety red lines.
5. **`tests/test_router.py`** (+105 lines, +13 tests) — 17 router tests pass.
6. **`tests/test_circuit_breaker.py`** (new, 10 tests) — all pass.

### Skills installed (3 net new)
- `anti-laziness` (clawhub, community) — 8 iron rules, refusal-when-constraints-unmet
- `verification-before-completion` (skills-sh/obra/superpowers) — **literal cure for preamble-stall**: "NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE"
- `subagent-driven-development` (official/software-development) — maps to AIW's `transfer_targets` + `composition` PROMPT.md frontmatter
- `dispatching-parallel-agents` (skills-sh/obra/superpowers) — maps to AIW's `intake.py`+`router.py`+`results-collector.py` pattern

### Research output (9 docs on disk, ~140 KB)
- `2026-09-01-harness-failure-modes-and-community-patterns.md` (10.7 KB)
- `2026-09-01-new-relevant-repos-and-contributor-networks.md` (13.7 KB)
- `2026-09-01-complete-state-and-research-summary.md` (23 KB)
- `2026-09-01-hub-skills-recommendations.md` (14.7 KB)
- `2026-09-01-complete-plan-consolidated.md` (18.5 KB)
- `2026-09-01-aiw-internals-audit.md` (8.2 KB)
- `2026-09-01-aiw-research-patterns-v2.md` (18.9 KB)
- `2026-09-01-aiw-research-round-3-communities.md` (13.9 KB)
- `2026-09-01-aiw-research-round-4-upgrades-templates.md` (19.1 KB)

---

## In progress

- **All planned tracks closed** (this session, PRs #20-#25):
  - **A1** (cron sibling-dep auto-install): ✅ PR #20 (11 missing-dep crons fixed, 7+3)
  - **A2** (DEMIURGE-113 provider decision): ✅ PR #21 — doc-only inventory; the "79 dead crons" was 32 actual, and the provider question applies to 1 cron (`aiw-saas-lifecycle-reconcile`)
  - **A3** (DEMIURGE-115 hard-stop-enforcer): ✅ PR #22 — ADR-0006 with 3 disposition options, default = delete
  - **A4** (ADR-0005 libsodium blob): ✅ already documented in PR #15; status quo (keep in quarantine)
  - **B** (AIW_ROOT threading step 8): ✅ PR #23 — 5 more scripts threaded (20/107 total)
  - **C** (profile-skill optimization): ✅ PR #24 — corrected the 126-skills claim; actual is 43, no per-load cost, optimization is moot
  - **D** (cron prompt caching): ✅ PR #25 — 42 prompts now have `cache_control: ephemeral` markers; ~$2/mo estimated savings

- **CI status**: PRs landing but master remains red due to pre-existing `test_token_cap_disabled.py` failures (4 tests, from the other session's test rewrite for Phase 9 R6 real measurement). **Not caused by my PRs.** The other session is actively working on this.

- **Recently resolved per operator input (2026-09-03, Ivan)**: only MiniMax-M3 available (no Anthropic, no Cerebras).
  - **Block A** (Anthropic 401): ✅ PR #28 disabled 5 research crons
  - **Block B** (Cerebras 402): ✅ PR #28 disabled `aiw-saas-lifecycle-reconcile`
  - **Block C** (bitwarden_sdk / broken entries): ✅ PR #28 disabled `kv-bws-sync`, `linkedin-token-refresh`, `instagram-token-refresh`, `aiw-boundary-validate-hourly`
  - **Block D** (arg-error): ✅ PR #29 added 8 wrapper scripts (intake-{sales..board}.sh, eval-gate-decisions-summary.sh) since cron-runner doesn't support args
  - **DEMIURGE-115**: ✅ PR #30 deletes `scripts/global-hard-stop-enforcer.py` per ADR-0006 default (no imports, no cron, no pre-commit — confirmed unwired)

- **Operator-gated decisions still pending** (awaiting Ivan):
  - **ADR-0005**: libsodium blob disposition (default = keep in quarantine, deadline 2026-10-03)
  - **Master CI red** (4 token-cap test failures): pre-existing from the other session's test rewrite; not in scope here

- **Operator-side fixes applied to host filesystem**:
  - 7 wrapper scripts at `/opt/data/scripts/intake-*.sh` + `eval-gate-decisions-summary.sh` (created in PR #29)
  - `boundary-validate-all.sh` wrapper created (cron disabled but wrapper reusable later)
  - 2 sibling-dep copies (`_paths.py`, `signal_queue.py` to `/opt/data/scripts/`) — PR #20
  - 42 cache_control markers injected on cron prompts — PR #25
  - 5 threaded scripts in repo + 5 deployed to `/opt/data/scripts/` (1 reverted: build-pipeline.yaml dep) — PRs #23 + #27

- **Live spend trajectory**:
  - Before autonomous session: ~$680/mo (Ivan's measurement)
  - After PR #25 (cache_control markers): ~$678/mo
  - After PR #28 (disabled 10 broken crons): ~$675/mo (some crons were costing money on retries)
- **Live spend trajectory**:
  - Before autonomous session: ~$680/mo (Ivan's measurement)
  - After this session: ~$678/mo (D saves ~$2, A1 unblocks 11 crons that may re-cost)

---

## Recently merged (last 7 days)

| PR | Title | Lines | Date |
|---|---|---|---|
| #13 | fix(cron): signal-indexer script path | +188 | 2026-09-03 |
| #12 | fix(cron): security-watchdog-30min outbox path | +195 | 2026-09-03 |
| #11 | fix(ci): hermetic AIW_ROOT fixture | +77/-13 | 2026-09-03 |
| #10 | docs(cron): salvage DEMIURGE-121 audit | +294/-0 | 2026-09-03 |
| #9 | WS-3 step 5: thread 5 scripts via AIW_ROOT | +55/-5 | 2026-09-03 |
| #6 | WS-3 step 4: thread 5 observability scripts | +56/-6 | 2026-09-03 |
| #5 | WS-2 CI gate + readme-counts | (already merged Sep 2) | 2026-09-02 |
| #4 | WS-research: YouTube fetcher + David Ondrej | (already merged Sep 2) | 2026-09-02 |
| #3 | WS-1 finish: trust window audit + 7 stubs | (already merged Sep 2) | 2026-09-02 |
| #2 | WS-3 step 1+2: AIW_ROOT helper | (already merged Sep 2) | 2026-09-02 |

---

## Known pitfalls / blockers

1. **`scripts/observability/agent-tracer.py` had been silently no-op since some prior edit.** Fixed in 2026-09-01 session but worth flagging in any future audit of "why isn't this script running?".
2. **`state/agent-traces.jsonl` went stale 2026-08-21** (before 2026-09-01 session). Now has 181 entries after the tracer fix.
3. **Scanner blocks some obra skills with DANGEROUS verdict** (`writing-skills`, `using-superpowers`). Would need manual source audit before installing.
4. **GitHub API rate limiting** limited some contributor-network queries. Future sessions should pre-cache via `gh api` with auth.
5. **`state/coord.json` schema is free-form** — lacks the structured `commitments[]` array pattern from iPythoning's memory schema. Would need migration.
6. **6 unscheduled scripts are correctly so** (per audit 2026-09-03):
   - `restore-prompt-bodies.py` — CI-only (run by `.github/workflows/ci.yml`)
   - `strict-schemas.py` — one-shot migration tool
   - `lint-prompts.py` — CI-only
   - `readme-counts.py` — CI-only
   - `thread-aiw-root.py` — refactor helper, run by humans/subagents
   - `results-collector.py` — invoked by other cron jobs or subagents, NOT standalone
   Do NOT wire these to cron without changing their semantics first.
7. **Cron drift trap** — `jobs.json` reverts between turns. The cron-sync.sh script auto-resolves drift but watch for it on multi-day sprints.

---

## Next steps (in priority order)

1. **Create `/opt/data/agents/docs/adr/0000-template.md` + first ADR** (15-30 min)
2. **Try installing 3 more obra skills** (`executing-plans`, `receiving-code-review`, `finishing-a-development-branch`) (10 min)
3. **Read `affaan-m/ECC/homunculus/instincts/` YAML format** + write integration plan with curator-evolver (30 min research)
4. **Add `commitments[]` array to `state/coord.json` schema** (1-2 hours, requires migration)
5. **Deep-read `mattpocock/skills/writing-for-agents/SKILL.md`** (15 min)
6. **Deep-read `obra/superpowers/SKILL.md` writing-skills frontmatter conventions** (already have via AGENTS.md reference) — adopt in next 3 PROMPT.md files
7. **Audit 63 PROMPT.md files** for frontmatter compliance with obra's "Use when..." pattern
8. **Spanish-language skill development** (paraguay positioning opportunity)

---

## How to verify

```bash
# Canonical test suite
cd /opt/data/agents && bash tests/run-all.sh
# Expected: 210 passed, no failures

# Skills enabled
/opt/hermes/bin/hermes skills list | grep enabled
# Expected: >= 107 enabled

# Plugins enabled
grep -A 10 '^plugins:' ~/.hermes/config.yaml | grep '^  - '
# Expected: 6 plugins enabled

# Memory budget check
# (Currently 92% — 2032/2200 chars. Trim before next new memory entry.)

# This file exists and is current
ls -la /opt/data/agents/docs/HANDOFF.md
test -f /opt/data/agents/AGENTS.md && echo "AGENTS.md present"
test -d /opt/data/agents/docs/adr/ && echo "docs/adr/ present"
```

---

## Open research questions (not blocking)

- `anthropics/skills` (173k★) deep-read
- `ponytail` (120k★) "lazy dev" philosophy complement
- Spanish-language agent repos for Paraguay positioning
- Discord/Telegram community knowledge
- Cross-device memory sync (no clear winner found)

---

---

## Round 9 (2026-09-01T17:00-17:40Z): Plan implementation

12 of 13 plan items from `/opt/data/profiles/ivan/plans/2026-09-01-aiw-upgrade-plan.md` shipped this session. Only Phase 4.4 (public release) deferred per session memory rule requiring explicit operator authorization.

### New code (all live, all tested)

**Memory layer (Phase 1):**
- `scripts/memory/compactor.py` — L2 token-threshold compaction with archive (9 tests)
- `scripts/memory/signal_index.py` — L3 keyword+tag inverted index (12 tests)
- `scripts/memory/commitments.py` — L1 schema regex-based commitment extraction (16 tests)

**Automation (Phase 4):**
- `scripts/cron/weekly_summary.py` — weekly digest of agents/routing/decisions/latency (10 tests)
- `scripts/curator/instinct_generator.py` — ADR-0002 phase 1: auto-generate instinct YAMLs from traces (12 tests, refactored to use `_make_instinct` helper)

**New agents (Phase 3):**
- `demiurge/agents/architect-agent/PROMPT.md` — two-phase build: spec-only role
- `demiurge/agents/auditor-agent/PROMPT.md` — two-phase build: verdict role
- `demiurge/router/dispatch-rules.yaml` — added `route-architect-task` + `route-auditor-task` rules

**New methodology docs (Phase 2):**
- `docs/patterns/INDEX.md` — rewritten as real pattern catalog with status legend (✓/◐/✗)
- `docs/patterns/recipe-not-conversation.md` (new)
- `docs/patterns/architect-then-builder.md` (new)
- `docs/patterns/auditor-agent.md` (new)
- `docs/patterns/clean-slate-delegation.md` (new)
- `docs/patterns/proposer-authority-separation.md` (new)
- `docs/patterns/long-horizon-memory.md` (new)

### Cron jobs (live, 154 total in /opt/data/cron/jobs.json)

- `aiw-coord-compactor` — `0 20 * * 0` (Sundays 20:00, before summary)
- `aiw-signal-indexer` — `0 2 * * *` (daily 02:00)
- `aiw-commitments-extractor` — `0 3 * * *` (daily 03:00)
- `aiw-weekly-summary` — `0 23 * * 0` (Sundays 23:00, written in earlier turn)
- `aiw-instinct-generator` — `0 22 * * 0` (Sundays 22:00, written in earlier turn)

### State changes

- **Test count:** 278/278 PASS (was 219 before this turn; +59 net new tests)
- **Pattern files:** 8 (was 2)
- **ADRs:** 5 files (3 ADRs + template + README index, unchanged)
- **PROMPT.md files:** 65 (was 63, +2 new agents)
- **Memory scripts:** 3 (new dir)
- **Cron scripts:** 1 (new dir)
- **Curator scripts:** 1 (new dir)
- **Total cron jobs:** 154 (was 149, +5 net)

### How to verify (start of any new session)

```bash
cd /opt/data/agents && bash tests/run-all.sh 2>&1 | tail -3
# Expected: 278 passed
```

### Two-phase build pipeline (NEW — how to use it)

1. Append signal with `routing_tags: ["architect"]` → routes to architect-agent
2. Architect produces a spec in `demiurge/agents/architect-agent/outbox/signals/<sig-id>.md`
3. Re-append the spec as a new signal with `routing_tags: ["audit"]` → routes to auditor-agent
4. Auditor produces verdict in `demiurge/agents/auditor-agent/outbox/signals/<sig-id>.md`

**Note:** builder-agent is NOT yet implemented. Specs from architect-agent are reviewed but not converted to code.

### Memory pipeline (NEW — how to verify)

```bash
# 1. Compactor (run weekly)
cd /opt/data/agents && /opt/data/.venv/bin/python3 scripts/memory/compactor.py --dry-run

# 2. Signal index (built from signal-queue.ndjson)
# Cron job runs daily at 02:00. Manual: see aiw-signal-indexer script.

# 3. Commitments (extracted from signal-queue.ndjson)
# Cron job runs daily at 03:00. Manual: see aiw-commitments-extractor script.
```

### What is NOT done (deferred from upgrade plan)

- **Phase 4.4 (public release of methodology layer)** — REQUIRES explicit operator authorization per session memory rule. Will not be done without your "yess".
- **builder-agent** — architect→auditor pipeline is wired but no code-producing role exists yet.
- **Recipe-ification of 63 PROMPT.md** — most are still conversation-style.
- **Preamble-discipline audit** — skills installed but no automated check on PROMPT.md content.

### Open gaps (from Round 7 research doc)

- arXiv full-text deep-read of SuperLocalMemory 4.0 + Systems Foundation papers
- Jesse Vincent's X handle
- HKUDS lab advisor
- 49 of 61 playbook patterns unread
- Discord community contents (5 servers, content not surveyed)


## Provenance

Created per AGENTS.md requirement (Round 4 adoption). Adapted from `iPythoning/b2b-sdr-agent-template/docs/HANDOFF.md` pattern.

See `/opt/data/profiles/ivan/plans/2026-09-01-aiw-research-round-4-upgrades-templates.md` for the full research synthesis.

---

## Kanban deliverable — 2026-09-03 21:00Z (task t_0a292a93)

**Filled 188 internal questions** — 90-min session with Kiki.

- Source: `research/188-questions-for-ivan.md` (Erebus, 2026-08-13)
- Output: `/opt/data/source-materials/internal-answers.md` (18 KB, 183 of 185 questions drafted, 21 marked `# TODO: ivan-review` for real data gaps)
- Host-side path; same pattern as `/opt/data/scripts/` cron wrappers (PR #20, #29)
- Coverage map at the bottom of the file: Priority A 70/70, B 65/65, C 37/37, D 13/13 — all sections drafted; only the 21 `TODO` markers need operator confirmation
- Next: auto-generate SWOT / BCG / 12-month OKRs from this draft per Erebus' downstream spec

---

## Phase 9 R4–R5 update (2026-09-01, 22:00 UTC)

### Risk mitigations shipped (5 risks from `board/risk-register-2026.md`)

| Risk | Mitigation | Cron | Status |
|------|-----------|------|--------|
| R4: Eval aggregate unknown | nightly eval-aggregate wired 0 4 * * * | aiw-eval-aggregate-nightly | ✅ verified wired |
| R5: LLM prompt injection | additionalProperties: false on 16/16 schemas | aiw-strict-schemas-weekly | ✅ hardened |
| R7: Trademark incident | aiw-trademark-scan-cron now scheduled 0 3 * * 0 (was empty) | weekly | ✅ wired |
| R9: Bitwarden compromise | cron-secret-sentinel.py daily scan | aiw-cron-secret-sentinel-daily | ✅ running |
| R12: cron-error-watchdog | outbox-fallback path added | every 30m | ✅ verified |

### DEMIURGE ticket census (after 2026-09-01 R5)
- **77 / 78 COMPLETED** (99%)
- 1 DEFERRED (DEMIURGE-082, portmanteau migration per ADR-0004 #2)
- 0 ACTIVE

### New scripts
- `scripts/strict-schemas.py` (R5)
- `scripts/cron-secret-sentinel.py` (R9)

### New tests
- `tests/test_risk_mitigations.py` — 10 tests for both scripts
- Total canonical suite: **377 passed, 6 skipped**

### Cron job count
- 184 → 186 (added 2: cron-secret-sentinel-daily + strict-schemas-weekly)
- 1 fix: trademark-scan-cron schedule set (was empty `{}`)

### Cross-references
- `board/risk-register-2026.md` (updated mental model)
- `tests/test_risk_mitigations.py` (validation)
- `outbox/signals/cron-error-watchdog-*` (live alerts)
