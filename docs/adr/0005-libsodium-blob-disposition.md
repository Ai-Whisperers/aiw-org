# ADR 0005: Disposition of libsodium secretbox blob `a1d64864-77f9-4e6a-8d6e-b4a90137189a`

- **Date:** 2026-09-03
- **Status:** PROPOSED — awaiting operator decision
- **Deciders:** Ivan (operator-gated per HANDOFF-PHASE-8.md `## HIGH` + R11 doctrine)
- **Affects:** `/opt/data/agents/.quarantine/a1d64864-77f9-4e6a-8d6e-b4a90137189a`

## Context

A 1972-byte libsodium-encrypted `crypto_box_seal` blob with UUID
`a1d64864-77f9-4e6a-8d6e-b4a90137189a` appeared in the working tree
during the 2026-09-01 Phase 9 R3 audit. The blob's provenance is
unknown — not in git history, not referenced by any tracked file,
first seen during a routine audit.

The blob is now isolated at `/opt/data/agents/.quarantine/` (alongside
a README documenting the discovery). The decision now is: keep,
delete, or commit-and-encrypt. Per Phase Kernel brief §4 + R11, file
disposition with unclear provenance is operator-gated.

This ADR records the options. The decision is Ivan's.

## Decision

**This ADR documents three options; no decision has been recorded
yet. Operator selects one of the three below and we record the
selection in this ADR + a follow-up commit.**

## Alternatives Considered

### Alternative 1: Keep in quarantine (status quo)

Leave the blob at `/opt/data/agents/.quarantine/a1d64864-...`. The
README explains the discovery and the unverified provenance. The
blob stays accessible if its origin is later discovered.

- **Pros:**
  - Zero information loss. If the blob is a critical credential
    backup (e.g. sealed state snapshot, recovery key), the data is
    preserved.
  - No operator decision needed yet — revisit when more context is
    available.
  - Default safe choice under uncertainty.
- **Cons:**
  - File accumulates on disk indefinitely.
  - Future operators find it and re-litigate the same question.
  - No git trail of the decision; relies on the README staying
    accurate.
- **Why not the best:** Doesn't actually resolve the question; just
defers it. If the file is genuinely orphaned data, leaving it
forever wastes audit cycles every time someone discovers it again.

### Alternative 2: Delete permanently

Remove `/opt/data/agents/.quarantine/a1d64864-...` and update the
quarantine README to record the deletion.

- **Pros:**
  - Clean state. Removes the question entirely.
  - Stops consuming disk space.
  - The audit trail (this ADR + the previous README + the
    HANDOFF-PHASE-8.md reference) preserves the discovery for
    historical record.
- **Cons:**
  - **Irreversible** — if the blob was a credential backup, the
    plaintext is lost forever (decryption requires the recipient's
    private key, which we don't have access to either).
  - Requires high confidence that the blob is dead data, which we
    don't have.
- **Why not the best:** Too risky without further investigation.
  Even if 99% likely dead data, the cost of losing a credential
  backup is unbounded.

### Alternative 3: Commit ciphertext + store key in BWS

Commit the ciphertext to `state/quarantine/a1d64864-...` in this
repo, and document the libsodium recipient public key (if known)
in BWS (`/opt/data/.hermes/bws-secrets-cache.tsv`) so a future
operator with the corresponding private key can decrypt it.

- **Pros:**
  - Preserves the blob in version control with full provenance.
  - Key is in BWS, not in the repo (good key-hygiene).
  - Git history records the disposition decision.
- **Cons:**
  - **We don't know the recipient's private key** (the README
    confirms the blob was found, not decrypted). So the blob is
    encrypted in the repo but inaccessible.
  - Adds noise to the repo (`state/quarantine/<uuid>`).
  - The recipient's public key, if recoverable, would need to be
    stored somewhere — and we don't have it.
- **Why not the best:** Looks like a "do something" option, but
without the recipient key it's just a different shape of
quarantine. Genuinely un-decryptable ciphertext in the repo is
worse than in `.quarantine/` (it pretends to be tracked).

## Consequences

### Positive (of recording this decision)

- Three options are now documented with rationale.
- Future operators don't have to re-derive the analysis.
- Operator has a checklist, not a blank-page decision.

### Negative / Costs

- **None** at this stage — the ADR ships no destructive action.

### Risks + Mitigations

- **Risk:** Operator decides to delete; turns out the blob was a
  credential backup.
  **Mitigation:** Default recommendation is Alternative 1
  (keep in quarantine). Only delete after operator confirms "I
  know what this is and it's safe to delete" — and even then,
  archive the ciphertext hash in the ADR before deletion so
  the SHA256 of what was deleted is recoverable.

- **Risk:** Operator decides to commit; ciphertext sits in git
  history forever (even if later deleted) because git history is
  immutable.
  **Mitigation:** If operator wants to commit, also rotate the
  recipient keypair (so the committed ciphertext is permanently
  un-decryptable even if the old key leaks).

- **Risk:** Operator never decides; the question recurs.
  **Mitigation:** This ADR sets a 30-day decision deadline. If no
  decision by 2026-10-03, the default Alternative 1 (keep in
  quarantine) becomes permanent.

## Recommended Default

**Alternative 1 (keep in quarantine) is the safest default** —
preserves data, isolates it from active paths, makes the decision
reversible. The operator can later choose Alternative 2 or 3
without losing data.

## Provenance

- Triggered by: HANDOFF-PHASE-8.md `## HIGH` item (encrypted
  libsodium blob at repo root, never committed)
- Investigation trail: `/opt/data/agents/.quarantine/README.md`
- Format identification: `2.Ek` prefix → libsodium `crypto_box_seal`
  (anonymous public-key encryption)

## Related

- [ADR 0004](0004-tier-2-decisions-batch-2026-09-01.md) — Tier-2
  Decision Batch (operator-gated items)
- `/opt/data/profiles/ivan/plans/2026-09-03_012000-aiw-org-baseline-recovery.md`
  — Plan that called out this ADR
