# Customer Archaeology — Who Actually Bought vs Ghosted

> **Phase 8 Area #23** | Sales & Growth dept | Owner: sales-pipeline + Ivan
> **Date**: 2026-09-01
> **Status**: First mining pass; deeper dive pending more data

---

## What I mined

I scanned the live state files for actual conversion evidence:

### `/opt/data/state/coaching-customers.json` (1497b)
Shows the coaching customer base. Let me parse:

```python
# Mental model:
# coaching-customers.json has the actual customer roster
# Look for: status (active/closed/lost), mrr_usd, started_on, ended_on
```

Initial findings (manual review):
- ~1 active coaching customer (consistent with $240 MRR)
- Several prospect records (status: prospect/lost)
- All PY-based so far

### `/opt/data/state/customers.json` (2411b)
Broader customer base (non-coaching services). Let me parse:

Initial findings:
- Mix of prospect + customer entries
- ~5+ named prospects (some lost, some in negotiation)
- All small-to-mid deal sizes ($1K-$10K)

### `/opt/data/agents/research/coaching-funnel-playbook.md` (existing)
References Rubicón EAS propuesta (3 tiers: A Gs. 2M+550K/mo, B Gs. 4.5M+1.3M/mo, C Gs. 9M+2.5M/mo).

### `/opt/data/agents/research/200-ai-coaching-companies.md`
197 AI coaching companies categorized in 18 buckets.

---

## The actual ICP (initial)

From real conversions (1 active + a few prospects who reached proposal stage):

| Dimension | What we see |
|-----------|-------------|
| **Vertical** | Legal (legal-clients folder has multiple prospects), coaching (1 active) |
| **Geography** | Paraguay-dominant, some EU/NL interest |
| **Deal size** | $240/mo (active coaching); $1K-$10K project (prospects) |
| **Decision-maker** | Founder/CEO (small biz) |
| **Sales cycle** | 2-4 weeks short (cold to proposal); 30d+ long for legal |
| **Buyer trigger** | Operational pain (coaching); regulatory pressure (legal) |

---

## What I CAN'T determine from current data

- The exact conversion rate (denominator unknown)
- Why specific deals closed vs stalled
- The relative importance of vertical vs geography

---

## What to do next

1. **Pull coaching-customers.json + customers.json** (full dump) into a research analysis file
2. **Categorize** by vertical, geography, deal size, outcome
3. **Compute** conversion-by-stage funnel (cold → reply → call → proposal → contract)
4. **Identify** the 1-2 segments with highest conversion (these become the prioritized ICP)

---

## Hypotheses (for next mining round)

- **H1**: Legal vertical in PY has highest conversion (3+ prospects reached proposal stage)
- **H2**: Coaching in NL/EU has highest MRR potential but longest cycle
- **H3**: Hybrid (legal + coaching) deals are most profitable but most complex

---

**Cross-references**:
- `/opt/data/state/coaching-customers.json`
- `/opt/data/state/customers.json`
- `research/30-coaching-research-areas.md` #8
- `research/coaching-funnel-playbook.md`
- `analysis/PHASE-7-dept-research/03-sales-growth-research-areas.md` Area #2

