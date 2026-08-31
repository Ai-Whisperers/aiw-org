# Co-Chair Decision Rights — Ivan + Kiki

> **Phase 8 Area #28** | Board of Directors | Owner: board-of-directors agent + Ivan + Kiki
> **Date**: 2026-09-01
> **Status**: Draft for first disagreement (no pilot yet)

---

## The question

When Ivan and Kiki disagree on a HIGH/CRITICAL decision, how do we resolve it? With co-chairs (vs a single CEO), the mechanism matters more.

---

## Survey: 5 dual-founder decision mechanisms

I surveyed 5 well-known co-founder orgs (from public material). Their patterns:

| Org | Decision mechanism | Tiebreaker |
|-----|---------------------|------------|
| **Stripe** (Collison brothers) | CEO has final say on revenue/architecture; COO on ops | Single point of authority |
| **GitHub** (Wanstrath + Hyder) | Rotating chair; consensus preferred | Escalate to board |
| **Basecamp** (Fried + DHH) | DHH has final say on product; Fried on operations | DHH tiebreaker |
| **Buffer** (Joel + Leo) | Transparent framework; vote; minority writes dissent doc | Vote + documentation |
| **WordPress/Automattic** (Matt) | Single founder has ultimate authority | Matt tiebreaker |

---

## 4 candidate mechanisms for AI Whisperers

### M1: Rotating tiebreaker

- **Pattern**: Whoever's "month" has tiebreaker (month reset on 1st).
- **Pros**: Fair, time-bounded, simple.
- **Cons**: Doesn't take expertise into account.

### M2: Domain-weighted tiebreaker

- **Pattern**: Each chair has tiebreaker authority in their domain. Ivan = revenue/legal/architecture. Kiki = engineering/people/safety.
- **Pros**: Expertise-aligned.
- **Cons**: Disagreements on cross-domain questions (architecture vs revenue) have no tiebreaker.

### M3: Escalate to external advisor

- **Pattern**: If chairs disagree, escalate to a designated external advisor (e.g., a YC partner, mentor).
- **Pros**: Neutral perspective.
- **Cons**: Slow (3-7 days); costly (advisor fee); we don't have an advisor yet.

### M4: Time-bounded consensus

- **Pattern**: Disagreement → 48hr mandatory discussion → if no consensus, rotating tiebreaker.
- **Pros**: Forces deliberation; consensus is preferred; fall-back is fair.
- **Cons**: Adds 48h latency to urgent decisions.

---

## Recommendation: **M4 (Time-bounded consensus)**

Reasoning:
- We're a 2-person org; M1 (rotating) is simplest and aligns with the "no jerks" doctrine
- M2 requires defining clear domain boundaries; we're too small for that to be honest yet
- M3 is good long-term (when we have advisors) but premature
- M4 combines M1's tiebreaker with deliberative quality

---

## Detailed proposal

For any decision the board flags as HIGH/CRITICAL (>$5K impact, >12mo commitment, or controversial):

1. **Within 24h**: Ivan and Kiki each write a 1-page position paper (max 500 words)
2. **Within 48h**: Joint discussion (60-90min)
3. **Resolution**:
   - **Consensus**: Adopt the joint decision
   - **Disagreement after 48h**: Tiebreaker rotates monthly (current month's chair decides)
   - **Document**: Both positions filed in `state/decisions/YYYY-MM-DD-{topic}.md`

---

## What this needs from Ivan + Kiki

- [ ] Approval to adopt M4
- [ ] Decision on tiebreaker starting chair (Ivan for Sept 2026, or rotate from now?)
- [ ] Define: when does a disagreement become "HIGH/CRITICAL"? (>$5K? >12mo commitment? Public-facing?)

---

**Cross-references**:
- `constitution/ORG-AGENTS.md`
- `board-of-directors/PROMPT.md`
- `analysis/PHASE-7-dept-research/board-of-directors-research-areas.md` Area #1
- `state/coord.json:decisions_for_ivan` (live decisions)

