# Phase 26 Decisions — Pending Ivan + Kiki

> **Date**: 2026-09-01
> **Status**: Awaiting decisions. Phase 26 autonomous work complete; these 3 items need human authorization.
> **Format**: Decision / Recommendation / Effort / Why this matters / Counter-arguments

---

## D1 (Ivan) — Sales funnel revival

**The question**: Formspree (1-2h) vs Worker revival (8-16h)?

**Recommendation**: **Formspree**

| | Formspree | Worker revival |
|---|---|---|
| Effort | 1-2h | 8-16h |
| Cost | $8/mo (free tier available) | $5/mo CF Workers |
| Reliability | SaaS (99.9% SLA) | DIY (we own uptime) |
| Data ownership | Formspree owns (acceptable per doctrine) | We own |
| Setup | Click + paste endpoint | Restore dead repo + redeploy |
| Debug | Formspree dashboard | Cloudflare logs |

**Why this matters**:
- Sales funnel currently has 0 leads in pipeline (state/sales.json: 5 leads, 0 qualified)
- $240 MRR stuck because no new leads entering
- Formspree unblocks in 1-2h; Worker revival unblocks in 1-2 days
- We can migrate to Worker later when $5K MRR justifies the engineering cost

**Counter-arguments** (in case Ivan disagrees):
- Worker revival restores self-hosting (philosophical)
- Formspree introduces third-party (data residency concerns)
- Formspree free tier is rate-limited (might need to upgrade at scale)

**Source**: `sales/funnel-revival-2026.md`, `state/sales.json`

---

## D2 (Kiki) — Hard-stops wrapper invocation

**The question**: Globally invoke the hard-stops wrapper from all agents with destructive actions?

**Recommendation**: **YES — invoke wrapper globally (8-16h implementation)**

**Why this matters**:
- Phase 8 audit found: wrapper exists (`patterns/hard-stop-wrapper.py`) but **0 of 49 agents invoke it**
- Any destructive action currently executes unblocked (no PII redaction, no rate-limit, no audit trail)
- This is the **biggest AI-safety hole** in the org (per `engineering/ai-safety-posture-2026.md`)
- 1 catastrophic mistake (mass-delete state, leak customer PII) > 16h of prevention work

**Effort**: 8-16h implementation (4 phases)
1. Refactor wrapper to be importable (1h)
2. Add wrapper invocation to all PROMPTs with destructive actions (2-3h)
3. Write audit log per invocation (2-3h)
4. Add test coverage (3-5h)

**Counter-arguments**:
- Wrapper adds latency to every action (~50-200ms per call)
- False positives block legitimate work (need fine-grained allowlist)
- Wrapper itself becomes a single point of failure

**Source**: `operations/hard-stops-enforcement-audit.md`, `engineering/ai-safety-posture-2026.md`

---

## D8 (Kiki) — Eval gate enforcement (block low-pass agents)

**The question**: Should eval gate enforcement block agents with <50% pass_rate from running?

**Recommendation**: **YES — but with override (8h implementation)**

**Why this matters**:
- Currently no enforcement: any agent can run regardless of quality
- eval-aggregate-pass-rate.py now computes the metric (Phase 8 #10)
- Phase 26 #3 wires it nightly (so we'll have real data soon)
- Blocking low-pass agents prevents:
  - Bad state writes (corrupted JSON from confused LLMs)
  - Wasted tokens ($9.79/day → could be $5/day)
  - Brand damage (broken deliverables)

**Effort**: 8h implementation
1. Add pre-run hook that checks eval-trending.json (2h)
2. Block agents below threshold (2h)
3. Add override mechanism (Ivan can force-run with note) (2h)
4. Test + alert on first block (2h)

**Counter-arguments**:
- Eval data is incomplete (we just wired the cron, no historical data)
- False positives kill productive agents (we'll lose work)
- Without historical baseline, threshold of 50% is a guess

**Source**: `engineering/eval-pass-rate-baseline-2026.md` (Phase 8 #10), `state/eval-per-agent.json`

---

## How to decide

Each item has been analyzed. Decisions should be:
- **D1 (Ivan)**: One-word disposition per memory doctrine ("do all of this")
- **D2 (Kiki)**: One-word disposition (she's technical lead)
- **D8 (Kiki)**: One-word disposition (technical, follows from D2)

If no answer in 7 days: default to recommendation (Formspree, wrapper invocation, eval gate enforcement).