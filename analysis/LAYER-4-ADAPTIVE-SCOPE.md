# Layer 4 — Adaptive (Soul-Improvement) — Scope

> **Status**: ⏸ **DEFERRED — gated by customer traction**
>
> Per `UPGRADE-PROPOSAL §12` and `EXECUTION-SCOPE §2 Layer 4`:
> Layer 4 (soul-improvement) execution is BLOCKED until gates pass.
>
> **Gate status (2026-09-01):**
> - Customer traction: ❌ FAIL ($240 MRR, 1 archived customer — required: ≥$1000 MRR or ≥5 customers)
> - Layers 1-3 stable: ⏳ PENDING (L1/L2/L3 completed 2026-09-01 — required: ≥30 days)
> - Smoke gates: ✓ PASS (100% — required: ≥95%)
>
> Per Ivan's directive ("go for all layers all phases") this scope doc is
> written but execution is DEFERRED per the gate check.

---

## Gate-check artifact

This scope doc itself IS the gate-check artifact. It documents what
Layer 4 would do, then refuses to execute. Layer 4 unblocks when:

| Trigger | Current | Required | Action to unblock |
|---------|---------|----------|-------------------|
| $1000 MRR | $240 | $1000 | Sales + product pipeline work (out of scope for L4 itself) |
| OR 5+ customers | 1 archived | 5 | Same as above |
| AND L1-L3 ≥30 days stable | 0 days | 30 days | Wait |

**To re-evaluate the gate**:
```bash
./scripts/smoke-test.sh L4
```

---

## What Layer 4 would do (when gates pass)

### L4.1 — Soul-improvement agent

**What**: Add 1 soul-improvement agent that can read its own PROMPT.md, suggest improvements based on signals, and stage them for review. Per Proposal §12.

**Acceptance criteria**:
- New agent `soul-improvement-suggester` in `demiurge/agents/`
- Runs weekly (cron `0 12 * * 1`)
- Output: `state/soul-revisions/{date}/proposal-{agent-name}.md`
- Per Proposal §12: staged rollout — NEVER on main souls
- First deployment: a non-main agent (e.g., a beta agent)

### L4.2 — Cross-agent learning

**What**: Soul-improvement agent proposes patterns learned from one agent's signals to be applied to similar agents (transfer learning).

**Acceptance criteria**:
- Pattern-detection algo (per Proposal §12)
- Diff-based PR-style output for review
- Auto-PR creation via `gh` API (requires PAT scope: `repo:write`)

### L4.3 — Eval-gate tightening

**What**: As eval-gate confidence increases (from 50%+ to 80%+), tighten the gate to block more agents. Per `GAP-RESEARCH-FINDINGS Surprise 4: hard-stops advisory only`.

**Acceptance criteria**:
- Wire `hard-stops-wrapper.py` as pre-action gate (currently 0 agents invoke it per Layer 1 audit)
- Verify wrapper correctness via replay tests

### L4.4 — Continuous improvement loop

**What**: Tighten the eval-gate → measure impact → loosen if false-positives → tighten further. Per `EXECUTION-SCOPE §3 Layer 4 loop`.

**Acceptance criteria**:
- Track false-positive rate of gate
- Auto-loosen if rate > 5%
- Auto-tighten if rate < 1% AND ≤95% pass-rate held

---

## Why deferred

The whole Layer 4 thesis is: **"the system gets better at being itself"**.

For that to be valuable, there must be **value being delivered**. The current state:

- 1 archived customer (richar-ruiz deal was recommended DECLINE)
- $240 MRR (vs $293/mo burn — net negative)
- 0 deals open
- 0 leads in pipeline (Worker returns test-mode briefs)

There is no "self" for the system to be better at being. Layer 4 would optimize a non-existent value flow. Per `EXECUTION-SCOPE §2 Layer 4 (Adaptive)`: "do deferred indefinitely".

---

## Threat model (L4 specific — already drafted in L2.8)

Per `THREAT-MODEL.md ADDENDUM B`:

- **SAA-1**: Soul agent runaway (mitigated by staged rollout §12)
- **SAA-2**: Soul agent compromise (mitigated by git versioning + cron gates)

Both are documented. No new work needed in L4; gates are pre-defined.

---

## Revocation criteria

Layer 4 revokes DEFERRED status (becomes ACTIVE) when:

```bash
# Script: scripts/check-l4-gate.sh (NOT YET WRITTEN)
# Will be added when L4 unblocks; for now: ./scripts/smoke-test.sh L4
# reports current status
```

Required conditions (ALL must hold):
1. `state/coaching-customers.json:active_customers >= 5` OR `state/finance.json:mrr_usd >= 1000`
2. `date_diff_days(layer_3_completion_date, today) >= 30`
3. `smoke_test.sh L3 --runtime < 10s` (currently 3s — already passes)

---

## What AI WILL NOT do

Per gate-check semantics + Ivan's directive:

- ✗ Will NOT write a soul-improvement agent (deferred)
- ✗ Will NOT enable eval-gate tightening (deferred)
- ✗ Will NOT propose cross-agent learning (deferred)
- ✗ Will NOT modify any PROMPT.md beyond what L2.5/L2.6 already did

---

## Status

**Layer 4 = DEFERRED.** This scope doc is committed for reference. To unblock:
- Sales pipeline work (out of scope)
- Wait 30 days for stability
- Then run `./scripts/smoke-test.sh L4` again

---

**Author**: AI (autonomous)
**Date**: 2026-09-01
**Commit**: (pending)
**Companion**: `THREAT-MODEL.md ADDENDUM B`, `UPGRADE-PROPOSAL §12`, `EXECUTION-SCOPE §2 Layer 4`