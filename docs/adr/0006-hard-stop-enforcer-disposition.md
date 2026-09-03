# ADR 0006: Disposition of `scripts/global-hard-stop-enforcer.py`

- **Date:** 2026-09-03
- **Status:** PROPOSED — awaiting operator decision (per DEMIURGE-115)
- **Deciders:** Ivan (operator-gated per ADR-0004 #4)
- **Affects:** `scripts/global-hard-stop-enforcer.py`

## Context

Per ADR-0004 #4 (Sep 1, Tier-2 decision batch), R1 hard-stops are accepted as unenforced for AIW internal use. The mitigating controls are:
1. Pre-commit secret-leak guard (wired Sep 1, Phase 9 R1)
2. Human operator (Ivan + Kiki) in the commit loop

The script `scripts/global-hard-stop-enforcer.py` exists (9.4 KB) but is unwired — no cron, no pre-commit hook, no entry point. DEMIURGE-115 asks: **wire or delete?**

The calculus changes before client deployment: clients need enforced safety rails (we ship the framework with hard-stops ON, not advisory).

## Three options

### Option A: Delete the script

`rm scripts/global-hard-stop-enforcer.py`. Document the deletion in this ADR.

- **Pros:** Removes the dead-code ambiguity; future maintainers don't wonder why an unused 9.4 KB script sits in the repo; aligns with ADR-0004 #4 ("unenforced for AIW internal").
- **Cons:** Have to re-author it when client deployment happens (no good).
- **Why not the best:** Lossy.

### Option B: Keep but mark as "lint-only" with explicit "DO NOT WIRE FOR INTERNAL USE" notice

Add a 50-line docstring at the top: this is the future enforcement script. For AIW internal, do NOT wire it. When client-deployment happens, wire it then.

- **Pros:** Preserves the work, makes the safety intent clear, prevents premature wiring.
- **Cons:** File stays in repo as "almost-but-not-quite" code.
- **Why not the best:** Leaves the dead-code ambiguity in place; future readers will still wonder.

### Option C: Wire a soft-enforcement check now (pre-commit hook that WARNS, doesn't block)

Add a pre-commit hook that runs `global-hard-stop-enforcer.py --check` on every commit. If hard-stops aren't declared in the affected files, the hook prints a warning to stderr but exits 0 (success). This makes the safety posture VISIBLE without blocking work.

- **Pros:** Live visibility into R1 posture; no enforcement (per ADR-0004); educational for new contributors.
- **Cons:** Adds pre-commit noise; risk of "warning fatigue" (operators start ignoring).
- **Why not the best:** Warning fatigue is real. The pre-commit already does secret-leak; adding another warning layer may not improve outcomes.

## Recommended default

**Option A (delete).** Rationale:
- The script is **not the only place** R1 enforcement would live — at minimum it would need pre-commit + CI integration + cron-driven scan.
- Preserving dead code creates a "TODO trap" that future operators think is half-done when it's actually intentional-not-done.
- If we ever ship to clients, we'll author a NEW enforcement pipeline (probably in CI, not in cron scripts), informed by 3+ more months of internal use.

## Consequences

### Positive (of recording this decision)

- Operator has a clear 3-option menu.
- Future maintainers know the rationale.
- DEMIURGE-115 ticket can be closed with the decision recorded.

### Negative / Costs

- **None at this stage** — this ADR ships no destructive action until Ivan picks Option A.

### Risks + Mitigations

- **Risk:** Operator picks A; later realizes they need the script for client work.
  **Mitigation:** Git history preserves the file at the SHA it was deleted from. `git checkout <sha> -- scripts/global-hard-stop-enforcer.py` restores it in seconds.

- **Risk:** Operator picks B or C and the file rots / becomes confusing.
  **Mitigation:** Add an ADR-0007 in 90 days if the script is still unwired.

## Recommended deadline

Pick by **2026-09-15**. Past that, the script will likely continue accumulating 1-line updates and confusing future readers.

## Provenance

- Triggered by: HANDOFF-PHASE-8.md `## MED` #1 (8 deferred gaps)
- Investigation trail: `tickets/DEMIURGE-115-operate-global-hard-stop-enforcer/`
- ADR-0004 #4 acceptance basis: "R1 downgraded from CRITICAL → ACCEPTED in risk register"
- Client-deployment calculus: TBD per go-to-market plan

## Related

- [ADR 0004](0004-tier-2-decisions-batch-2026-09-01.md) — Tier-2 decisions including R1 unenforcement
- [ADR 0005](0005-libsodium-blob-disposition.md) — parallel operator-gated decision template
- `/opt/data/agents/docs/HANDOFF.md` — Known pitfalls (R1 gap noted)
