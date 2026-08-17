# Funding — Application Form Template

> **Use this for every program applied to.** One row per program. Save under `outbox/<YYYY-MM-DD>-<program-slug>.md` so the funding-coordinator agent can scan and log to `state/funding.json`.

---

## Program metadata

```yaml
program_name: <name from catalog>
url: <canonical application URL>
tier: <S | A | B | C>  # see catalog "Top 25"
category: <compute_credit | accelerator | grant | visa | debt | cf | etc>
funding_type: <grant | accelerator | credit | equity-free | equity | debt | visa | scholarship | revenue_share | paid_pilot | cf | other>
funding_size_usd: <number or null>
equity_pct: <number or null>
fx_payout: <USD | EUR | Gs. | mixed | null>
fx_risk: <low | medium | high>
trademark_safety: <SAFE | BRAND-NAME | CARVE-OUT | FUNDED-BY>
decision_time_weeks: <number>
prerequisites:
  - <e.g., PY S.A. registration>
  - <e.g., EU incorporation>
```

## Application tracking

```yaml
applied_date: <YYYY-MM-DD or null>
contact_email: <string or null>
contact_name: <string or null>
founder_narrative_version: <version used>
deck_version: <version used>
metrics_sheet_version: <version used>
status: <researching | drafting | applied | interview | offer | accepted | rejected | withdrawn>
decision_date: <YYYY-MM-DD or null>
funding_amount_received_usd: <number or null>
notes: <free text>
follow_up_date: <YYYY-MM-DD or null>
next_action: <free text>
```

## Application body (paste the actual application text here)

```
<PASTE APPLICATION HERE>
```

## Required documents checklist

- [ ] Founder narrative (current version)
- [ ] Deck (current version)
- [ ] Metrics sheet (auto-generated from state files)
- [ ] Org registration docs (PY S.A., EU entity, etc.)
- [ ] Tax ID (RUC for PY, VAT for EU)
- [ ] Bank statement (last 3 months)
- [ ] Pitch video (optional, accelerator)
- [ ] Reference letters (optional, accelerator)
- [ ] IP disclosure (optional, grants)
- [ ] Project proposal (if grant)

## Post-decision actions

```
If accepted:
  - Add to state/funding.json: applications_in_flight (with status=accepted)
  - Update credits_received_usd or grants_approved_usd
  - Schedule activation cron (if program requires activation steps)
  - Schedule first reporting milestone (if grant requires reporting)
  - Add follow_up_date for renewal / next cohort

If rejected:
  - Add to state/funding.json: applications_in_flight (with status=rejected)
  - Add notes for next-cycle improvements
  - Schedule next-cohort deadline reminder (most accelerators have 2x/year)

If withdrawn:
  - Add to state/funding.json: applications_in_flight (with status=withdrawn)
  - Document reason (focus, prerequisites not met, etc.)
```
