# ADR-0004: Tier-2 Decision Batch (8 calls, 2026-09-01)

- **Date:** 2026-09-01
- **Status:** Accepted (all 8 decisions ratified by Ivan)
- **Deciders:** Ivan (operator), audit agent (analysis + recommendation)
- **Affects:** departments-taxonomy (none — already deleted), naming convention, repo topology, risk register R1, sales funnel, funding pipeline, open-source plan, public repo posture

## Context

On 2026-09-01 Ivan requested a professional review of 8 open Tier-2
decisions that had been blocking autonomous execution for ~10 phases.
The audit (`docs/adr/0004-tier-2-decisions-batch-2026-09-01.md`
prerequisite: `analysis/PRE-EXEC-AUDIT-ALL-LAYERS-2026-09.md` and the
incoming audit from `@session:ivan/20260901_175348_46e9b0`) found:

- The decisions are blocking ~6-12 months of autonomous execution.
- Each decision has its own recommendation already in the repo's own
  analysis docs (UPGRADE-PROPOSAL, Q4 review, risk register, wishlist).
- Three of the eight were *already executing* de facto even though
  they were officially deferred (departments-taxonomy was empty/deleted;
  agents were being added under portmanteau names like
  `research-engineer`; growth-coaching was operating as a separate repo).

The previous session committed `docs/HANDOFF-PHASE-8.md` listing these
8 decisions as "blocking" and asking Ivan to resolve them. Ivan
resolved all 8 in a single message. This ADR records the resolutions
and the consequences that flow from them.

## Decision

8 decisions, ratified 2026-09-01:

| # | Decision | Choice | Status change |
|---|----------|--------|---------------|
| 1 | Delete Tier-2 `departments-taxonomy/`? | **Delete (already done)** | Tier-2 effectively gone; doc references need cleanup |
| 2 | Greek vs portmanteau naming? | **Portmanteau wins** | Migration ticket DEMIURGE-082 scope confirmed |
| 3 | Merge `aiw-org` ↔ `growth-coaching`? | **Don't merge** | Coaching = separate product department (when revenue exists) |
| 4 | R1 hard-stops enforcement? | **Accept the risk** | R1 downgraded from CRITICAL → ACCEPTED in risk register |
| 5 | Formspree for sales lead form? | **Defer** | No work on non-engineering depts yet |
| 6 | Start-Up Chile application? | **Defer** | Until engineering tier is stable |
| 7 | Open-source the framework? | **Defer** | Until engineering tier is stable |
| 8 | Repo privacy? | **Keep public** | Deliberate posture; threat model acknowledges external exposure |

## Alternatives Considered

### Per-decision alternatives are documented in the source proposals:

- Decision 1: UPGRADE-PROPOSAL §2.2 (recommends delete) vs.
  LAYER-2-FOUNDATION-SCOPE (recommends keep). Delete wins because
  Tier-2 directories were already empty.
- Decision 2: Wishlist 52 (Greek canon vs portmanteau vs coexist).
  Portmanteau wins because `agents-prompts/` (portmanteau) has 31
  tracked files in active use, while `demiurge/agents/` (Greek) has
  28 directories most of which are still in migration.
- Decision 3: Wishlist 64, 104-106 (merge / keep separate / sync
  state). Keep separate + treat coaching as future department wins
  because revenue from coaching is a precondition for any product
  department that would consume it.
- Decision 4: Risk register R1 mitigation (8-16h to invoke wrapper)
  vs accept + downgrade. Accept wins because the audit showed the
  wrappers are declared but unenforced in 0/63 invocation paths,
  meaning the 8-16h work would only be the first half; full
  enforcement needs ops discipline + regression tests = ~40h.
  At $240 MRR and zero active customers the cost is not justified.
- Decision 5-7: Do now vs defer vs never. Defer wins on all three
  because (a) Tier-1 close-out is not finished, (b) the same analysis
  identifies multiple P0 engineering items still open, and (c) the
  revenue gate for these is R2 (Formspree) which is itself deferred.
- Decision 8: Privatize (delete public repo) vs keep public vs
  selectively archive sensitive parts. Keep public wins because
  (a) the audit identifies no credential leaks currently public (the
  4 P0 leaks are in private worktrees), (b) the public surface is
  being used as portfolio material, and (c) the threat model can
  acknowledge the public posture as deliberate.

## Consequences

### Positive

- Decisions 1, 2, 3, 4, 8 are now executable. Documentation cleanup
  for stale references proceeds; the migration ticket gets a clear
  scope; growth-coaching stays separate; R1 stops blocking engineering
  work; public posture is documented as deliberate.
- Decisions 5, 6, 7 being explicitly deferred (not blocked, not lost)
  means they can be revisited at any future "engineering tier is
  stable" trigger without re-deriving the analysis.
- The repo's analysis-to-decision latency drops materially. The audit
  said the repo generates findings faster than it closes them; this
  decision batch closes 8 of the largest findings at once.

### Negative / Costs

- R1 acceptance: hard-stops declarations remain unenforced. Any
  agent prompt that says `disable_hardstop: require_approval: true`
  is still advisory, not enforced. **The 100%-declared / 0%-enforced
  gap continues.** Mitigated by: (a) every commit now passes through
  the pre-commit secret-leak guard wired in Phase 9 R1 (this batch's
  Tier 1 item), (b) human operator (Ivan + Kiki) remains in the loop
  for all destructive actions via cron-guard's state-mutation checks.
- Deferred decisions 5-7: no revenue, no funding, no credibility lift
  in the near term. The Q4 review's recommendation to apply to
  Start-Up Chile was conditional on engineering tier being stable;
  that condition is not yet met.
- Repo stays public: agents continue to ingest untrusted external
  content with the prompt structure visible to attackers. Mitigated
  by: red-team scenarios now at 38/38 (Phase 36), prompt-injection
  detection at 15 languages, pre-commit secret-leak + trademark-scrub
  guards in place.

### Risks + Mitigations

- **Risk:** R1 acceptance is treated as a "fix" rather than a
  documented acceptance, and the dashboard continues to show 63/63
  hard-stops declared as a green metric.
  **Mitigation:** Risk register is amended (see Tier-1 commit) to
  explicitly mark R1 as ACCEPTED with a written rationale, separate
  from the "mitigation in progress" tier.

- **Risk:** Stale references to `departments-taxonomy/` in
  analysis docs lead future readers to think it still exists.
  **Mitigation:** This ADR + the doc-cleanup commit notes the
  effective deletion; future passes will rewrite the analysis docs
  to remove the references.

- **Risk:** The 8 decisions are ratified in chat only and not
  reflected in the source-of-truth tickets.
  **Mitigation:** This ADR is the canonical record. DEMIURGE-082
  ticket gets updated to reflect the portmanteau-canonical decision
  in the same commit.

## Provenance

- Source audit: incoming `@session:ivan/20260901_175348_46e9b0`
  (audit document from the incoming-session agent reading the repo at 7ed8676).
- Ivan's responses: chat session 20260901_18xx, single message with
  all 8 decisions inline.
- ADR author: Hermes agent (this repo's own `aiw-ops-discipline` flow).

## Related

- `analysis/UPGRADE-PROPOSAL-2026-09.md` §2.2 (delete Tier-2)
- `analysis/PRE-EXEC-AUDIT-ALL-LAYERS-2026-09.md` (R1 evaluation)
- `analysis/REMAINING-TASKS-AND-WISHLIST.md` items 52, 64, 104-106
- `board/risk-register-2026.md` (R1 row updated)
- `tickets/DEMIURGE-082-legacy-agents-migration-docs/` (scope updated)
- `docs/HANDOFF-PHASE-8.md` (the original blocker inventory)
- `docs/adr/0000-template.md` (this template)
