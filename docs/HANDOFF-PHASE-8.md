# Phase 8 Handoff — Remaining Work for Next Sessions

> **Written**: 2026-09-01 (Ivan's @session:ivan/20260901_173041_466a28 batch)
> **State at write**: aiw-org master @ `04e5398` (Phase 8 R9), 278/278 tests green
> **Companion to**: `/opt/data/agents/docs/HANDOFF.md` (governance baseline)
> **Audience**: next autonomous-session agents + Ivan

This document captures the work **left undone** after Phase 8 R1–R9, organized
by repo. Each item has: file paths, what needs to happen, why it matters,
effort estimate, and which session/skill it should be picked up in.

---

## TL;DR — what's blocking

| Severity | Item | Repo | Effort |
|----------|------|------|--------|
| 🔴 CRITICAL | `aiw-security-watchdog-30min` cron points at the **wrong** PROMPT path (repo root, not `04-engineering/`) | aiw-org | 30 min |
| 🔴 CRITICAL | Cron-guard script `aiw-signal-indexer` has broken shell quoting in its inline `-c` payload | aiw-org | 30 min |
| 🟠 HIGH | `a1d64864-77f9-4e6a-8d6e-b4a90137189a` — encrypted libsodium secretbox blob at repo root, never committed (intentionally). Audit origin + decide keep/quarantine/delete | aiw-org | 1 h |
| 🟠 HIGH | Ghost `security-watchdog-30min/` dir at repo root (created by cron pointing at wrong path) — accumulating ~700KB of orphan data daily | aiw-org | 30 min (rolls into CRITICAL fix) |
| 🟠 HIGH | `commitments-extractor` cron writes coord.json daily even when nothing changed → qa-monitor fires false positives | aiw-org | 1 h |
| 🟡 MED | 8 deferred gaps from `research/dept-research/04-engineering-gap-audit.md` (Drucker/Laloux/Gallup/Sunstein deltas) | aiw-org | 4–6 h total |
| 🟡 MED | All 9 Phase 8 R5 scripts need cron entries (currently import-only, not scheduled) | aiw-org | 1 h |
| 🟡 MED | `AGENTS.md` referenced in 9 commits but **no vendor pointer files** (CLAUDE.md, AGENTS.md per-repo, etc.) yet | aiw-org | 30 min |
| 🟢 LOW | `state/coord.json.coaching-monitor-20260901T032119Z` — orphan backup file, never cleaned up | aiw-org | 5 min |
| 🟢 LOW | `demiurge/agents/{architect,auditor,builder,cadmus}/outbox/signals/*.md` — gitignore excludes `**/outbox/*.md` only at one level; the nested `outbox/signals/*.md` files leak into `git status` | aiw-org | 15 min |

---

## 🔴 CRITICAL #1 — security-watchdog cron points at wrong PROMPT path

### Symptom
The cron `aiw-security-watchdog-30min` reads
`/opt/data/agents/security-watchdog-30min/PROMPT.md` — but that file
doesn't exist at that path. The canonical agent is at
`/opt/data/agents/04-engineering/security-watchdog-30min/PROMPT.md`.

### Evidence
```
$ ls /opt/data/agents/security-watchdog-30min/
outbox/   scratch/    (no PROMPT.md)
$ ls /opt/data/agents/04-engineering/security-watchdog-30min/
PROMPT.md  PROMPT-monitor.md  check.sh  check.sh.bak  monitor-notes
$ grep "security-watchdog-30min" /opt/data/cron/jobs.json
  "prompt": "Read /opt/data/agents/security-watchdog-30min/PROMPT.md ..."
```

### Why it matters
Every 30 min the cron spawns an agent that:
1. Can't read its own spec (file doesn't exist)
2. Falls back to the prompt's preamble only
3. Writes to `/opt/data/agents/security-watchdog-30min/outbox/YYYY-MM-DD.md` (wrong location, no gitignore coverage)
4. Accumulates ~70KB/day of orphan data

### Fix path
1. Update `/opt/data/cron/jobs.json` AND `/opt/data/.hermes/cron/jobs.json`:
   `Read /opt/data/agents/04-engineering/security-watchdog-30min/PROMPT.md`
2. Run `bash /opt/data/scripts/cron-sync.sh`
3. Decide what to do with the ghost dir at repo root:
   - Option A: Delete it (data is presumably noise anyway)
   - Option B: Move to `.archive/security-watchdog-30min/` (keep history)
4. Add `security-watchdog-30min/` to `.gitignore` to prevent re-creation

### Effort
30 min

### Pick-up skill
`aiw-ops-discipline` + `hermes-source-readonly-staging`

---

## 🔴 CRITICAL #2 — aiw-signal-indexer cron has broken shell quoting

### Symptom
The cron job `aiw-signal-indexer` uses an inline `python3 -c "..."`
with single-quoted paths inside double-quoted bash arg. Python sees
`\'` which is a syntax error.

### Evidence
```
$ cat /opt/data/cron/jobs.json | jq '.jobs[] | select(.name=="aiw-signal-indexer") | .script'
"/opt/data/.venv/bin/python3 -c \"import sys; sys.path.insert(0, \\'/opt/data/agents/scripts/memory\\'); ...\""
```

### Why it matters
The signal index never builds. Any agent that queries signals via the
index gets empty results. `process_pending()` in router.py still works
because it doesn't depend on the index — but visibility tooling is blind.

### Fix path
1. Move the inline `-c` payload into a script: `scripts/cron/signal-indexer-tick.py`
2. Update both cron files to call the script: `/opt/data/.venv/bin/python3 /opt/data/agents/scripts/cron/signal-indexer-tick.py`
3. Resync with `cron-sync.sh`

### Effort
30 min

### Pick-up skill
`aiw-ops-discipline`

---

## 🟠 HIGH #3 — Encrypted blob at repo root

### Symptom
`/opt/data/agents/a1d64864-77f9-4e6a-8d6e-b4a90137189a` (1972 bytes)
looks like a libsodium secretbox envelope:
`2.<salt>|<iv>|<ciphertext>|<hmac>`.

### Audit questions to answer
1. Where did it come from? (git log, file mtime, search cron jobs)
2. What's inside? (decrypt with the org's secret key — only if justified)
3. Does it contain a credential? (check against banlist)
4. Should it move to a vault, get quarantined, or be deleted?

### Decision options
- **Keep + ignore**: add to `.gitignore`, document as known-runtime-output
- **Quarantine**: move to `/opt/data/.archive/quarantine/<date>-<uuid>` with a README
- **Delete**: if confirmed to be ephemeral runtime noise

### Effort
1 h (audit + decision + cleanup)

### Pick-up skill
`credential-incident-reporting` (if credential leaked) OR `safe-credential-scrub` (if general secret hygiene)

---

## 🟠 HIGH #4 — Ghost security-watchdog dir at repo root

See CRITICAL #1 above — this is the same root cause.

### Effort
Rolled into CRITICAL #1 fix (30 min total).

---

## 🟠 HIGH #5 — commitments-extractor cron writes coord.json daily even when nothing changed

### Symptom
`scripts/cron/commitments-extractor.py` (or equivalent — verify exact
path) writes to `state/coord.json` every day. coord.json mtime updates
even when no commitments were extracted, so the qa-monitor fires a
"coord-changed" alert every 24h. ~365 false positives/year.

### Fix path
1. Read coord.json content before write; only write if diff is non-empty
2. Use atomic write pattern: write to `coord.json.tmp`, compare, rename
3. Add a test that verifies no-write on empty extraction

### Effort
1 h

### Pick-up skill
`aiw-state-file-write-discipline`

---

## 🟡 MED #6 — 8 deferred gaps from engineering gap-audit

See `/opt/data/agents/research/dept-research/04-engineering-gap-audit.md`.

Of the 12 gaps identified, 4 were addressed in Phase 8 R4–R6:
- ✅ Gap 1: devops-monitor recipe (Phase 8 R4)
- ✅ Gap 2: memory subsystem (Phase 8 R4)
- ✅ Gap 5: circuit breaker reliability (Phase 8 R5)
- ✅ Gap 7: weekly summary automation (Phase 8 R5)

Deferred to Phase 9:
- ⏳ Gap 3: peer-review process for engineering deliverables
- ⏳ Gap 4: coaching pipeline for engineering team growth
- ⏳ Gap 6: chaos-engineering practice (was mentioned but never stood up)
- ⏳ Gap 8: post-mortem template + blameless culture
- ⏳ Gap 9: capacity planning model
- ⏳ Gap 10: on-call rotation + escalation policy
- ⏳ Gap 11: knowledge-base search + discovery
- ⏳ Gap 12: technical-debt tracking + repayment cadence

### Effort
4–6 h total (1–2 sessions)

### Pick-up skill
`aiw-org-research-deliverables` (for the analytical work) OR domain-specific
agent (devops-monitor, ai-safety-engineer) per gap.

---

## 🟡 MED #7 — Phase 8 R5 scripts need cron entries

The 9 scripts from Phase 8 R5 are importable and CLI-runnable but not
scheduled. Each should have a cron entry with a documented cadence:

| Script | Suggested cadence | Reasoning |
|--------|-------------------|-----------|
| `build-missing-research-agents.py` | weekly | scaffold any missing agents vs roles-inventory |
| `circuit_breaker.py` (sweep) | every 15m | reset half-open circuits, log state |
| `cron/weekly_summary.py` | weekly (Mon 06:00 UTC) | roll-up per agent |
| `curator/instinct_generator.py` | weekly | trace → skill distillation |
| `editorial-calendar-escalate.py` | hourly | escalates empty slots |
| `literature-scan-cron.py` | weekly | arxiv + openalex sweep |
| `peer-review-trigger.py` | every 6h | review-queue check |
| `source-materials-scorer.py` | on-demand | runs from brief-build flow |
| `submission-tracker.py` | daily | journal status refresh |

### Effort
1 h (add to `jobs.json` + `cron-sync.sh` + smoke test each)

### Pick-up skill
`aiw-ops-discipline`

---

## 🟡 MED #8 — Vendor pointer files missing

`AGENTS.md` is the canonical rulebook but no vendor-specific pointer
files exist yet. Add (or symlink) per-repo:
- `CLAUDE.md` → "See `AGENTS.md`. Conflicts resolved in favor of `AGENTS.md`."
- `.cursorrules` → same
- `.windsurfrules` → same
- `AGENTS.md` (other-repo variant, if this repo is included as submodule)

### Effort
30 min

### Pick-up skill
`hermes-agent-skill-authoring` (for the pointer template)

---

## 🟢 LOW #9 — Orphan coord backup

`state/coord.json.coaching-monitor-20260901T032119Z` is a coaching
monitor's coord mirror backup. `.gitignore` excludes `state/*.pre-*.bak`
but not this timestamped variant. Either:
- Add `state/*.coaching-monitor-*` to `.gitignore`, OR
- Update the coaching-monitor cron to write to `.bak` extension

### Effort
5 min

---

## 🟢 LOW #10 — gitignore `**/outbox/*.md` only matches one level

`outbox/signals/*.md` (two levels deep) leaks into `git status`. The
guard script `scripts/pre-commit-citation-coverage.sh` correctly skips
these, but they clutter `git status` output and require manual
`.gitignore`-escape every time.

Fix: change `**/outbox/*.md` to `**/outbox/**/*.md` in `.gitignore`.

### Effort
15 min

---

## Per-repo remaining work

### `/opt/data/agents` (aiw-org) — Phase 8 complete, Phase 9 pending

**What's done**:
- Phases 27 → 36 (commit history shows R1–R9 of Phase 8 on top)
- 278/278 tests passing
- AGENTS.md governance baseline
- Two-phase build pipeline (architect → audit → build → verify)
- Research-education dept expanded to 12 agents
- 9 new operational scripts + 6 tests + memory subsystem
- Citation-coverage methodology + engineering gap-audit

**What's left**: items #1–10 above, plus ongoing:
- Phase 9 candidates: see `research/dept-research/04-05-implementation-plan.md`
- Tier-3/4 dept upgrades still in queue (compliance, board, people)
- Cost monitoring integration with the new router time-awareness

### `/opt/data/agents-v2` (growth-coaching) — clean, scope-down complete

**What's done**:
- Scope down to product-only at `a8c38c6`
- Org layer handed off to aiw-org
- 200-company competitive map, coaching-skills-gap audit, etc.

**What's left**:
- Phase 9 of coaching product roadmap (specific items in `/opt/data/agents-v2/plans/`)
- Client onboarding flow for the first paying customer
- Coaching curriculum v2 (use the new `research/methodology/` docs as input)

### `/opt/data/Company-Information` — behind 1 commit (now pulled)

**What's done**:
- Synced to `fc5c5fd` (Luana partner accepted renegotiated terms)
- Archived final state
- Vendor + partner + client docs all on main

**What's left**:
- New branch `cursor/gabi-pane-presupuesto` exists on origin — needs
  decision: merge into main? Keep separate? It's a local-only Gabi
  dashboard pane (probably Kiki's personal budget view).
- Saskia client engagement: see `/opt/data/agents-v2/plans/` for the
  full context

### `/opt/data/PARAGUAY-CIVICTECH-RESTORE-KIT` — docs only, not a git repo

**What's done**: deployment playbook + restore scripts + data-sources
**What's left**: not in scope for AIW phases — restore kit for the
civictech site itself.

---

## How to use this document

Next session that picks up AIW work:

1. Read `/opt/data/agents/docs/HANDOFF.md` (governance baseline)
2. Read this file (`HANDOFF-PHASE-8.md`) for the deferred queue
3. Pick the highest-severity item first (#1, #2, then #3-5)
4. Use the suggested `skill` for the work
5. Update this file when items land (move to "Done" section)

When Phase 9 begins, rename this to `HANDOFF-PHASE-8-DONE.md` and
write `HANDOFF-PHASE-9.md`.

---

**Status**: Phase 8 R1–R9 complete and pushed. 9 commits, +5543 lines.
278/278 tests green. 4 sync gaps remaining (see HIGH/MED/LOW items above).
