# Work Plan — Phase "Kernel" (2026-09+)

> **Generated**: 2026-09-02
> **Purpose**: One-page orientation for future sessions (human or AI).
> **Tickets**: 38 total — 9 done, 21 pending AI work, 8 [Ivan]-gated decisions.
> **See**: `tickets/INDEX.md` for the full table; `docs/KERNEL-DESIGN-2026-09-02.md` for the architectural intent; `docs/HERMES-ANSWERS-2026-09-02.md` (fb2b81f) for the audit this plan emerged from.

---

## Strategic frame

`aiw-org` is **instance zero** of an instantiable org kernel. Saskia gets her own instance on this kernel; AIW remains instance zero. The kernel is generic structure, the instance is per-business content. Designs are shipped; implementation is partially done; deployment is deliberately deferred.

The org went through a **prompt-body destruction incident** on 2026-09-01 (commit fffd7c4). 72 of 76 PROMPT.md files were truncated to frontmatter-only on BOTH live host and repo clone. WS-1 closed the production incident; WS-2..WS-7 close the systemic root causes.

---

## What this session shipped (DONE)

| Commit | Work | Ticket |
|---|---|---|
| `4939a1b` | right-size-toolsets.py + safety tests | DEMIURGE-083 |
| `3ccc244` | credit-burn-probe.py + 16 tests (P0.6) | DEMIURGE-084 |
| `2d8bea7` | Close 4 pre-existing lint failures | DEMIURGE-085 |
| `3471e2a` | Phase 0 research artifact consolidation | DEMIURGE-086 |
| `fb2b81f` | 142-question audit responses (HERMES-ANSWERS) | DEMIURGE-087 |
| `b7637cf` | Kernel design + Saskia instance design | DEMIURGE-088 |
| `320ffdc` | WS-1: restore 65 PROMPT.md bodies + INCIDENT report | DEMIURGE-089 |
| `e03a52a` | Disable broken token-cap.py + safety tests | DEMIURGE-090 |
| `94a73ce` | Correct REMAINING-WORK-INVENTORY P0 lie | DEMIURGE-091 |

---

## What's pending (PENDING tickets)

### WS-1 remaining (close root causes)

- **DEMIURGE-092** — fix add-max-output-tokens.py body-preservation bug (so next bulk patch cannot recur)
- **DEMIURGE-093** — audit sibling scripts (fix-parent-spec.py, add-cluster-field.py) for the same defect
- **DEMIURGE-094** — audit state-write trust window (which agents ran between fffd7c4 and 320ffdc, what did they write)
- **DEMIURGE-095** — mark 7 unrecoverable stubs explicitly (write proper bodies or label as STUB)

### WS-2 (Verifiable)

- **DEMIURGE-096** — readme-counts.py + CI check
- **DEMIURGE-097** — CI with no-skips gate (.github/workflows/ci.yml)

### WS-3 (Portable — biggest single-quality win)

- **DEMIURGE-098** — scripts/_paths.py with AIW_ROOT env var, threaded through 111 files in batches
- **DEMIURGE-099** — Hermetic test suite (conftest.py + tmp_path fixtures; AIW_ROOT=/nonexistent exits 0)
- **DEMIURGE-100** — host-vs-repo divergence reconciliation (ADR direction + commit missing)
- **DEMIURGE-101** — Backup + DR runbook + restore drill

### WS-4 (Decision queue drain — R11 critical)

- **DEMIURGE-102** — Categorize 424 items in coord.json:decisions_for_ivan; auto-close with rules; add priority + age + batching + rate limit; deliver digest

### WS-5 (Kernel implementation — design done at b7637cf)

- **DEMIURGE-103** — Implement kernel/ extraction (move + de-AIW + parameterize)
- **DEMIURGE-104** — Build scripts/bootstrap-instance.sh + 5-step smoke test
- **DEMIURGE-105** — Author docs/KERNEL.md (kernel contract + versioning + upgrade protocol)

### WS-7 (Truth and debt)

- **DEMIURGE-107** — Correct README counts (every count reproducible)
- **DEMIURGE-108** — Banner-mark historical docs (ORCHESTRATION.md, OPERATIONS.md, PHASE-* -> history/)
- **DEMIURGE-109** — Normalize ticket status vocabulary (one vocab; 57 of 81 dirs missing status)
- **DEMIURGE-110** — HANDOFF-PHASE-8 debt (security-watchdog ghost dir, signal-indexer, libsodium blob)
- **DEMIURGE-111** — Re-aim prompt-injection detection for indirect injection (vs extraction)

### Optional refactor

- **DEMIURGE-120** — consolidate-ticket-format (4-files-per-ticket may be overkill)

---

## What requires operator action (R11)

| Ticket | What | Why blocking |
|---|---|---|
| **DEMIURGE-106** | Answer 7 Saskia operator questions | Blocks WS-6 deployment |
| **DEMIURGE-112** | Rotate 4 credentials (SUPABASE, 3 GitHub PATs, R2 URLs, .env) | Per brief WS-2 §1 + audit Q73-Q75 |
| **DEMIURGE-113** | Decide provider for 79 dead crons (47% of fleet) | Per brief §4 "leave dead for now" — Ivan decides later |
| **DEMIURGE-114** | Decide Sunday cron schedule | Per brief FLEET-3 |
| **DEMIURGE-115** | Wire or delete global-hard-stop-enforcer.py | Per brief SAFE-1; calculus changes before client instance |
| **DEMIURGE-116** | Install sudo + chmod .env | Per audit Q75 |
| **DEMIURGE-117** | Define engineering-tier stability criteria | Per brief GATE-2 |
| **DEMIURGE-118** | Project architecture decision | Per brief PLAT-0 (superseded by kernel — confirm) |
| **DEMIURGE-119** | Decide public-repo policy | Per brief SAFE-6 |

---

## How to use this plan

1. **Daily session start**: read `docs/HANDOFF-PHASE-9.md` (or whatever the live handoff is), then this file.
2. **Pick one PENDING ticket per session** (per build-vs-close reflex — don't cascade).
3. **For [Ivan] tickets**: do NOT execute without explicit "yess" per MEMORY.md.
4. **For tickets blocked by other tickets**: check `tickets/INDEX.md` for the dependency tree (see `Blocked by` column).
5. **Verify before commit**: per AGENTS.md and the brief, use `tests/run-all.sh` + ad-hoc verify per system protocol.
6. **Update ticket at completion**: status -> done; mark acceptance criteria; append to progress.md.

---

## Sprint totals

```
9 done (083-091) -- 7 AI-owned, 0 [Ivan]-gated
21 pending AI work (092-105, 107-111)
8 [Ivan]-gated decisions (106, 112-119)
1 refactor ticket (120)

Total: 38 ticketized work items.
```

---

## Production-incident postmortem

See `analysis/INCIDENT-2026-09-01-PROMPT-TRUNCATION.md`. Key facts:

- 72 of 76 PROMPT.md files were truncated to ≤40 lines on **both** live host and repo clone.
- Root cause: `add-max-output-tokens.py::extract_frontmatter()` never captured body.
- A test that would have caught this was **skipped** as "implementation-detail" (per R1 in brief).
- `lint-prompts.py` validates frontmatter fields only — does NOT check body presence or minimum line count.

**Lesson**: any bulk-prompt-script MUST assert body preservation + print line-count diff. WS-1 items 4-5 (DEMIURGE-092, -093) are the preventive fixes.

---

## How to onboard a new session

1. Read this file
2. Read `tickets/INDEX.md` for the status snapshot
3. Read `docs/HANDOFF.md` (or live equivalent)
4. Pick one ticket from PENDING
5. If a ticket is `[Ivan]`-gated, do not execute
6. Verify-before-claim per system protocol
7. Commit with `DEMIURGE-NNN: <one verifiable claim>` format

Done tickets already include verification output in `progress.md`. Use that as your starting template for the next batch.
