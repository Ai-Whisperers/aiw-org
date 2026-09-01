# INCIDENT REPORT — 2026-09-01 Prompt-Body Truncation

> **Incident date**: 2026-09-01 ~21:00 UTC (commit `fffd7c4`)
> **Discovered**: 2026-09-01 ~23:30 UTC (during research audit)
> **Diagnosed and closed**: 2026-09-02 via `b7637cf` (this commit series)
> **Severity**: CRITICAL — production affected
> **Writer**: Phase "Kernel" brief, WS-1 execution
> **Status**: CLOSED — 65/72 restored; 7 marked as legitimate stubs

---

## 1. Timeline

| Time (UTC) | Event |
|---|---|
| 2026-09-01 ~21:00 | Commit `fffd7c4` "cap max_output_tokens: 800 on all 74 PROMPTs" merged. Ran `scripts/add-max-output-tokens.py`. |
| 2026-09-01 ~21:00 | `add-max-output-tokens.py::extract_frontmatter()` returned `(prefix, fm_text, suffix)` and **never captured the body**. `process_file()` then wrote `prefix + new_fm + suffix` which discarded everything past the closing `---`. |
| 2026-09-01 ~21:30 | Subsequent commit `590c6d1` (Tier-B8 bulk-fix) added `parent_spec` to 47 dept-level files, also via the same broken pattern. Same truncation problem for those files. |
| 2026-09-01 ~22:00 | Same operations also ran against `/opt/data/agents/` (live host) — both trees ended up at 17-line frontmatter-only state. |
| 2026-09-01 ~23:00 | Hermes audit discovered the issue while doing research on doc inventory. **72 of 76 PROMPT.md files were under 40 lines; many had only the YAML block + closing `---`.** |
| 2026-09-02 | Per Phase Kernel brief WS-1: `scripts/restore-prompt-bodies.py` (provided) ran `--apply --force` against both trees. |

## 2. Blast radius

### What was affected

- **72 of 76 PROMPT.md files** were truncated to ≤40 lines.
- **Both trees** (`/opt/data/agents-v2/aiw-org-clone/` repo clone AND `/opt/data/agents/` live host) were affected identically.
- The 7 files that were never longer than ~18 lines in any historical commit are **legitimate stubs** at the same level of truncatability as the corruption:
  1. `demiurge/agents/argus-health-monitor/`
  2. `demiurge/agents/athena-product-discovery-lead/`
  3. `demiurge/agents/cadmus-lead-enrichment/`
  4. `demiurge/agents/calliope-content-producer/`
  5. `demiurge/agents/clio-customer-signal-collector/`
  6. `demiurge/agents/iris-community-monitor/`
  7. `demiurge/agents/metis-proposal-drafter/`
- These 7 are marked **STUBS** in this incident report and explicitly **out of recovery scope**: they are the work of WS-1 item 3 (treat as stubs or write properly).

### What was NOT affected

- Cron registration (`/opt/data/.hermes/cron/jobs.json`) — unchanged.
- Hermes runtime code (`/opt/data/hermes-fixed/`) — unchanged.
- State files (`coord.json`, `agent-traces.jsonl`, etc.) — unchanged in shape; **content trustworthiness is a separate concern** (see §6).
- Other repos (`growth-coaching`, `saskia-app`, `paragu-ai-builder`, etc.) — unaffected.

## 3. Root cause

### The bug

`scripts/add-max-output-tokens.py::extract_frontmatter()` returned:

```python
return prefix, fm_text, suffix  # suffix = closing "---\n" only
```

The function never returned `content[3 + m.end():]` — the body.

`process_file()` then concatenated:

```python
new_content = prefix + new_fm + suffix  # body discarded
```

For a file that started:

```
---
name: x
---
# Mission
... actual content ...
```

`extract_frontmatter()` returned `prefix="---\n"`, `fm_text="name: x\n"`, `suffix="---\n"`. After `process_file()` ran:

```
---
name: x
max_output_tokens: 800
---
```

The body — everything after the closing `---` — was thrown away.

### Why was this not caught

1. **The test that would have caught it was skipped**: `tests/test_add_max_output_tokens.py::test_handles_well_formed_single_block`. Reason given: "implementation-detail." Per R1 in the Phase Kernel brief: **a skipped test is a failing test**.
2. **lint-prompts.py checks frontmatter fields, not body presence or minimum line count.** A 17-line file with valid YAML frontmatter passes the linter.
3. **No body-preservation assertion** in the script. Per R2 in the Phase Kernel brief: any bulk edit to PROMPT.md must assert body preservation and print a line-count diff.

### Why did both trees corrupt

The two trees (`/opt/data/agents-v2/aiw-org-clone/` and `/opt/data/agents/`) are **separate git repos with no sync script**. The same session that ran `add-max-output-tokens.py` against the repo ran it against the live host too. **No version-pinning, no drift detection, no canonical source.**

This was both cause (the same bug applied twice) and consequence (no recovery mechanism detects divergence).

## 4. Fix

### The deliverable

`scripts/restore-prompt-bodies.py` (this commit) — per-file history searcher that:
- For each currently-truncated PROMPT.md, walks the last 40 commits.
- Finds the version with the largest body.
- Splice: keep **current** frontmatter (which has legitimate new fields like `max_output_tokens`, `parent_spec`, `cluster`) and **source** body (the prior mission/instructions content).
- Writes the spliced result.

**Properties verified by tests** (`tests/test_restore_prompt_bodies.py`, 16/16 pass):
- DRY-RUN BY DEFAULT (no write without `--apply`).
- REFUSES `--apply` WITHOUT `--force` (explicit operator double-confirm).
- Body preservation: post-splice has BOTH current frontmatter (max_output_tokens) AND old body.
- Idempotent: plan() called twice = same plan.
- Reports exact 65/7 split for the current repo, matching the brief.

### Applied to

- `/opt/data/agents-v2/aiw-org-clone/` (repo)
- `/opt/data/agents/` (live host)

**Both now at 69/76 prompts with bodies ≥20 lines** (was 4/76 before this incident closure).

## 5. Prevention (per WS-1 items 4 + 5 of the brief)

| # | Prevention | Status |
|---|---|---|
| 1 | Fix `scripts/add-max-output-tokens.py` body-preservation bug | **TODO** — separate commit |
| 2 | Un-skip `tests/test_add_max_output_tokens.py::test_handles_well_formed_single_block` and assert body survives full round-trip | **TODO** |
| 3 | Audit sibling bulk scripts (`fix-parent-spec.py`, `add-cluster-field.py`, `add-cluster-or-...`) for the same bug | **TODO** |
| 4 | Add line-count diff to bulk-prompt-edit CI check (no file <40 lines) | **TODO** as `.github/workflows/ci.yml` |
| 5 | Replace skipped-test mechanism: pytest `-p no:cacheprovider --strict-markers -rs` and "skips fail the build" | **TODO** |
| 6 | Add `lint-prompts.py` check: body must be ≥20 lines after `---` close | **TODO** |
| 7 | Decide sync direction (host ←→ repo) and ADR | **Partially resolved**: this commit restores both trees simultaneously; sync direction now moot until drift detection is built |

## 6. State-write trust window

**Concern**: between `fffd7c4` (21:00 UTC 2026-09-01) and the restore (mid-day 2026-09-02), truncated agents may have performed `write_state` operations.

### What we know

- Truncated agents had only YAML frontmatter and a closing `---`. No body.
- Body fields like `Mission`, `Inputs`, `Output contract`, `Hard stops`, `Idempotency contract`, `Reflection Loop`, `Single-run procedure` were **invisible** to the agent at runtime.
- An agent could still produce a valid `---frontmatter---` echo, or a malformed burst out, depending on how the runtime stripped the body.
- The state file `coord.json` weighs 357K and contains 424 items in `decisions_for_ivan` (per `docs/HERMES-ANSWERS-2026-09-02.md`).

### What we don't know

- Which specific agents ran in the 24-hour window.
- What their outputs looked like.
- Whether any state writes happened.

### Recommended next-step (audit-only)

```bash
# Identify any writes to state files between 21:00 2026-09-01 and now
find /opt/data/state -newer /opt/data/state/coord.json.coaching-monitor-20260901T032119Z -type f

# Compare current coord.json events against the snapshot at 590c6d1
git -C /opt/data/agents show 590c6d1:state/coord.json > /tmp/coord-pre.json 2>/dev/null
diff <(jq -S . /tmp/coord-pre.json) <(jq -S . /opt/data/state/coord.json) | head -50
```

## 7. Related work

This incident is **the trigger** for the broader Phase "Kernel" brief — the new brief acknowledges that the same loose practices that caused this incident ("bulk-frontmatter scripts without body-preservation assertions, skipped tests, frontend-fast-forward commits, divergence between host and repo") are also blockers for the kernel extraction. **The next workstreams (WS-2, WS-3, WS-7 in the brief) are all derivable from this incident.**

The `docs/HERMES-ANSWERS-2026-09-02.md` (`fb2b81f`) provides the full 142-question audit that surfaced the host-vs-repo depth of this incident.

The Phase "Kernel" brief (`kernel/`, `saskia/`) is the strategic refactor: aiw-org becomes instance zero of an instantiable org kernel. The kernel extraction forces clean factoring that would have prevented this incident.

## 8. Bottom line

- **65 of 72** PROMPT.md files restored, in both trees, with current frontmatter + historical body.
- **7 of 72** deliberately left as stubs (per brief item 3 — they were never longer than ~18 lines; not corruption).
- **HS-1 (production incident) is closed** as of this commit.
- **TODO** for the same session or next: items 4, 5, 7 of §5 above (script fix, CI gate, lint check). The fix is in place; the prevention is partial.
