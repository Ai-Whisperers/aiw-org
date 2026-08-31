# Sales Funnel Revival — Diagnosis + Decision Tree

> **Phase 8 Area #19** | Sales & Growth dept | Owner: sales-pipeline + engineering-roster + Ivan
> **Date**: 2026-09-01
> **Status**: 🔴 DIAGNOSED — decision pending Ivan

---

## The state

Source: `/opt/data/agents/state/sales.json` (last_run: 2026-08-31T16:03:12Z)

```
funnel_30d:
  leads: 0
  calls_booked: 0
  proposals_sent: 0
  contracts_signed: 0

evidence.worker_status: "dead (Traefik router missing or Worker deploy lost; project archived 2026-08-28)"
evidence.cron_gap: "8 days since 2026-08-23T16:00:50Z"
```

**Pipeline = 0 across all stages. Worker = dead. Last sales run = 8 days ago.**

---

## The diagnosis (from sales.json:evidence)

### What broke

1. **2026-08-22**: Open question raised — `WEBHOOK_URL` secret unset on Worker
2. **2026-08-28**: Rubicon EAS project **archived** (entire project, not just Worker)
3. **2026-08-31**: Worker returns **404 across all 7 probed paths** (/api/lead, /api/lead/health, /api/lead/recent, /api/lead/admin, /api/lead/list, /api/lead-worker, /api/health)
4. **2026-08-23**: Last successful sales-pipeline cron run (8d gap)

### What worked before

Worker code is intact at `/opt/data/archive/legal-clients/rubicon-eas-2026-08-28-archived/api/lead-worker.js`. CF account `9eb1832f3e42a1dbd6ba854f8d6a1cb2` is still active per build README. The Worker code exists but isn't deployed (or Traefik router is missing).

### Why pipeline went to 0

Without a working form backend, no inbound leads can be captured. Cold outreach has been stalled because:
- The Worker 404 broke our pitch (we promise an automated follow-up that's broken)
- Without inbound, the funnel relies on outbound (which has been deprioritized during the gap)

---

## The decision tree

```
                    [Funnel Revival Decision]
                              |
            +-----------------+-----------------+
            |                                   |
    RESURRECT Worker                     REPLACE form backend
    (revive archived project)            (use Formspree/Typeform)
            |                                   |
    Time: 8-16h                        Time: 1-2h
    Risk: Traefik router may not be     Risk: migration effort
    fixable from this codebase              |
            |                                   |
    Outcome: full Rubicon EAS            Outcome: basic lead
    experience restored                 capture, no automation
            |                                   |
    Better long-term                     Better short-term
            |                                   |
            +---------> PAUSE <-----------+
                          |
                Take 2 weeks to decide
                Use cold outreach only
                (no form dependency)
```

---

## My recommendation: **REPLACE (use Formspree)** for these reasons

1. **Time**: 1-2h vs 8-16h. We have 0 leads, every day counts.
2. **Risk**: Resurrecting the Worker depends on Traefik config (which I don't have access to from this context). Formspree is a known working SaaS.
3. **Maintenance**: Formspree handles 99% of cases; we don't need to maintain a Worker for the foreseeable future.
4. **Pivot flexibility**: If we pivot to a different landing page, we can keep Formspree and only swap the form action URL.

### Implementation sketch (1-2h)

1. Create Formspree account on `sales@aiwhisperers.paragu-ai.com`
2. Get form endpoint URL
3. Edit `marketing-strategy/` landing page HTML: `<form action="https://formspree.io/f/{form_id}">`
4. Test end-to-end: submit form → email arrives
5. Set up Zapier to forward form submission to sales-pipeline agent
6. Update Worker health check to monitor Formspree (different probe)

### When to revisit Worker

When MRR > $5K AND we need advanced form features (file uploads, conditional logic, multi-step). At that scale, the Worker pays for itself.

---

## The cold-outreach workaround (meanwhile)

While the form is broken, sales-pipeline agent should:
1. Pull from `state/coord.json:outreach_targets[]` (if exists)
2. Manual WhatsApp outreach (per `coach-agents/coach-lead-finder/`)
3. Personal network (Ivan + Kiki's connections)

This is **manual and slow**, but it's the only working lead-generation path until the form is fixed.

---

## Pending decisions for Ivan

| # | Decision | Recommendation |
|---|----------|----------------|
| 1 | Replace Worker with Formspree? | **YES** (1-2h) |
| 2 | Decline richar-ruiz deal? (22d stalled, dossier anonymized) | **YES** (close, reallocate) |
| 3 | Resurrect Rubicon EAS later? | **LATER** (after $5K MRR or 30d) |
| 4 | Pause sales-pipeline cron until form is fixed? | **NO** (run on outreach-only) |

---

**Cross-references**:
- `state/agents/sales.json` (source data)
- `OQ-2026-08-22-A`, `OQ-2026-08-22-B`, `OQ-2026-08-31-A`, `OQ-2026-08-31-B`, `OQ-2026-08-31-C` (live open questions)
- `analysis/PHASE-7-dept-research/03-sales-growth-research-areas.md` Area #1
- `analysis/GAP-RESEARCH-FINDINGS-2026-09.md` (Worker 404 finding)

