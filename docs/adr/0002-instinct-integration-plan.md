# Instinct Integration Plan for AIW Org

**Author:** Hermes (ivan profile)
**Date:** 2026-09-01
**Purpose:** Plan how AIW's `curator-evolver` plugin should adopt the ECC homunculus/instincts pattern.

---

## 0. What is an "instinct"?

From `affaan-m/ECC/.claude/homunculus/instincts/inherited/everything-claude-code-instincts.yaml`:

```yaml
---
id: everything-claude-code-conventional-commits
trigger: "when making a commit in everything-claude-code"
confidence: 0.9
domain: git
source: repo-curation
source_repo: affaan-m/everything-claude-code
---

# Everything Claude Code Conventional Commits

## Action
Use conventional commit prefixes (feat, fix, docs, test, chore, refactor).

## Evidence
- Mainline history consistently uses conventional commit subjects.
- Release and changelog automation expect readable commit categorization.
```

**Key properties:**
- `trigger` — when this instinct applies (string match in conversational context)
- `confidence` — 0.0 to 1.0, how often the action was correct
- `domain` — git / code-style / testing / etc.
- `source_repo` — where it was learned
- `Action` — what to do
- `Evidence` — why this is correct

**Instincts vs Skills:**
- **Instinct** = auto-triggered, low-ceremony, learned from observation, YAML-form
- **Skill** = explicit invocation by user, structured SKILL.md with sections, agent-loadable

The lifecycle: observed behavior → instinct → evolve (cluster) → promote (skill/command/agent)

---

## 1. AIW's current state — what `curator-evolver` does today

**File:** `/opt/data/agents/plugins/curator-evolver/`

(Per `/opt/data/profiles/ivan/config.yaml` it's enabled, per session memory it's "evidence-backed skill curation with optional embedding ranking".)

**Gap:** No public source code for `curator-evolver` was found in this session's audit. It exists as a plugin (per config) but its implementation isn't visible in `/opt/data/agents/scripts/` or similar.

**What AIW currently has for state:**
- `state/coord.json` — rolling decisions log (270 KB)
- `state/agent-traces.jsonl` — 181 traces (after this session's tracer fix)
- `state/auto-eval-log.jsonl` — 924k lines of eval-gate data
- `state/audit-summary.jsonl` — 4 weekly audit summaries
- `state/coaching-customers.json`, `state/funding.json`, etc. — per-domain state

**What's missing:**
- No "instinct" schema — no `trigger`, `confidence`, `domain`, `Action`, `Evidence` fields anywhere
- No lifecycle (observe → instinct → evolve → promote)
- No cross-repo pattern learning

---

## 2. The integration plan

### Phase 1 — Define the instinct schema (2-3 hours, 1 session)

Add to AIW's state schema:

```yaml
# File: /opt/data/state/instincts/<source_repo>.yaml
---
schema_version: 1
source_repo: aiw-org
generated_at: 2026-09-01
instincts:
  - id: aiw-org-pre-dispatch-rejects-empty-tags
    trigger: "when router.process_pending sees signal with empty routing_tags"
    confidence: 0.85
    domain: routing
    source_repo: aiw-org
    action: "pre_dispatch_check rejects with code='empty_routing_tags'"
    evidence: "Tests test_router.py:test_pre_dispatch_check_empty_tags confirms behavior since 2026-09-01"
    learned_from:
      - "scripts/router.py:pre_dispatch_check"
      - "tests/test_router.py:test_pre_dispatch_check_empty_tags"
    created_at: 2026-09-01
    last_confirmed: 2026-09-01
    confirmation_count: 1
```

### Phase 2 — Generate instincts from existing data (3-4 hours, 1 session)

Script: `scripts/instinct_extractor.py` that scans:
- `state/agent-traces.jsonl` — for patterns like "agent X consistently takes action Y after trigger Z"
- `state/auto-eval-log.jsonl` — for eval-gate outcomes that recur
- `state/coord.json` — for decisions that keep getting re-made
- `git log` per repo — for commit-message conventions, file-naming patterns, etc.

Output: YAML files in `/opt/data/state/instincts/<source_repo>.yaml`

### Phase 3 — Wire instinct output to curator-evolver (4-6 hours, 1-2 sessions)

Modify `curator-evolver` plugin to:
1. Read `/opt/data/state/instincts/*.yaml` on load
2. Inject relevant instincts into `pre_llm_call` (similar to `ivan-behavioral-overlay`)
3. Track when an instinct "fires" — increment `confirmation_count`, update `last_confirmed`
4. When confidence drops below 0.3 OR last_confirmed > 90 days, mark `stale: true`

### Phase 4 — Evolve + Promote lifecycle (mirror ECC's commands)

Create AIW equivalents of ECC's three commands:

```
/opt/data/agents/commands/instinct-evolve.md   (analyzes + clusters instincts)
/opt/data/agents/commands/instinct-prune.md    (removes stale/low-confidence)
/opt/data/agents/commands/instinct-promote.md  (instinct → skill, when confidence > 0.8)
```

Wire into the same `hermes skills` ecosystem so they show up in skill listings.

### Phase 5 — Per-repo instinct files (long-term, ongoing)

Eventually each AIW repo (`aiw-org`, `coach-agents`, `growth-coaching`, etc.) gets its own `instincts.yaml` generated from its git history.

---

## 3. Specific instincts AIW already has (manual extraction, this session)

These should be in Phase 1's seed data — they're known patterns from the work this session did:

1. **`aiw-org-routing-rejects-malformed-signals`** — confidence 0.9
   - Trigger: "when pre_dispatch_check sees signal without id/ts/source/routing_tags"
   - Action: "Reject with code=missing_required_fields"
   - Evidence: 6 unit tests pass

2. **`aiw-org-routing-tracks-per-rule-latency`** — confidence 0.8
   - Trigger: "when router.py processes a signal"
   - Action: "Measure time.monotonic() and log latency_ms to audit"
   - Evidence: chronos pattern; test_router.py:Rule 14 validates log_decision signature

3. **`aiw-org-tracer-was-silently-broken`** — confidence 1.0 (verified)
   - Trigger: "before declaring any agent-tracer work complete"
   - Action: "Run python3 scripts/observability/agent-tracer.py and verify 'Collected N new traces' > 0"
   - Evidence: this session fixed 3 bugs that caused main() to never run

4. **`aiw-org-preamble-stall-detection`** — confidence 0.9
   - Trigger: "when an assistant says 'writing now' or 'shipping X' without a write_file/patch/terminal call in the same turn"
   - Action: "Treat as preamble-stall, intervene with user"
   - Evidence: 4× occurrence in 36h per session log

5. **`aiw-org-bws-for-secrets`** — confidence 1.0
   - Trigger: "when needing any API key, PAT, or token"
   - Action: "Use bws secret get <name>; never embed in code/URLs"
   - Evidence: 3 PAT rotations logged in session memory

---

## 4. What to NOT do (anti-patterns from ECC lessons)

- ❌ Don't let `confidence` decay silently — track `last_confirmed` and prune when stale
- ❌ Don't store instincts as inline PROMPT.md text — keep them as separate YAML, loaded on demand
- ❌ Don't auto-promote instinct → skill unless confidence ≥ 0.8 AND confirmation_count ≥ 5
- ❌ Don't generate instincts from `state/coord.json` decisions that are 1-off (use confirmation_count ≥ 3)
- ❌ Don't skip the Evidence field — every instinct must cite its source

---

## 5. Effort estimate

| Phase | Effort | Sessions | Status |
|---|---|---|---|
| 1. Schema definition | 2-3 hours | 1 | Not started |
| 2. Generator script | 3-4 hours | 1 | Not started |
| 3. curator-evolver wire | 4-6 hours | 1-2 | Not started |
| 4. Lifecycle commands | 3-4 hours | 1 | Not started |
| 5. Per-repo instincts | ongoing | continuous | Not started |
| **Total** | **12-17 hours** | **4-5 sessions** | |

**Recommended next step:** Phase 1 (schema definition + 5 seed instincts above) as a single focused session.

---

## 6. Honest gaps

1. **Don't have access to `curator-evolver` source code** — assumptions above about its current behavior are inferred from `/opt/data/profiles/ivan/config.yaml` + session memory, not source inspection.
2. **Don't have a CLI for instincts yet** — Phase 4 commands assume we'd build them, not adopt ECC's `instinct-cli.py` directly (it's at `continuous-learning-v2/scripts/instinct-cli.py`, ~500 lines, Python, can be forked).
3. **No measurement of how often instincts would actually fire** — would need telemetry after Phase 1.

---

## 7. One-line summary

Instincts are the missing link between `curator-evolver` (generates skills) and `commit-before-preamble` (enforces rules) — they let the system auto-learn per-repo conventions from observed behavior, then promote high-confidence patterns to first-class skills. 4-5 sessions of work, worth doing.
