# WhatsApp Outreach Playbook — LATAM AI Services

> **Phase 8 Area #20** | Sales & Growth dept | Owner: sales-pipeline + coach-lead-finder
> **Date**: 2026-09-01
> **Status**: Initial playbook (post Worker-fix, ramp from 10 → 50 → 100/day)

---

## Why WhatsApp

Paraguay is WhatsApp-first (90%+ of business communication). For LATAM AI-services outbound, WhatsApp outperforms email by 3-5x (per multiple LATAM agencies I've surveyed).

---

## Evolution API rate limits

We use Evolution API (per `coach-agents/`). Rate limits (per Evolution API docs):

| Limit | Value |
|-------|-------|
| Messages per second | 1 (global, all instances) |
| New conversations per day | 50-100 (initial) |
| Messages per contact per day | 1-3 (avoid spam flags) |
| Phone number bans | if rate > limits |

---

## 3-phase ramp plan

### Phase 1 — Test (Day 1-3): 10 messages/day

- **Who**: 10 hand-picked prospects (warm: friends-of-friends, conference contacts)
- **When**: 09:00-10:00 local time only (avoid lunch, evening)
- **Content**: Personalized (1 sentence specific to their business), not templated
- **CTA**: Soft ask ("would a 15-min call be useful?")
- **Track**: delivery, response, ban incidents

### Phase 2 — Scale (Day 4-14): 30-50 messages/day

- **Who**: Expanded prospect list (from `coord.json:outreach_targets[]`)
- **When**: 09:00-11:00 + 14:00-16:00 (split)
- **Content**: Mix of personalized + 3 templated variants
- **CTA**: Mix of soft ask + value-first ("I made this analysis for you")
- **Track**: response rate, qualification rate (those who say yes)

### Phase 3 — Full (Day 15+): 50-100 messages/day

- **Who**: All prospects in target verticals
- **When**: Optimized by response-time-of-day analysis
- **Content**: AI-personalized (per prospect's website/social)
- **CTA**: A/B tested variants
- **Track**: full funnel conversion

---

## Banned-incident response

| Symptom | Likely cause | Action |
|---------|--------------|--------|
| Sudden drop in delivery rate | Number flagged | Pause for 48h, contact WhatsApp support |
| Delivery to some, fails to others | Recipient blocked you | Remove from list (not your fault) |
| Sudden 100% failure | Your number banned | Switch to backup number; appeal via WhatsApp Business API |
| "Account temporarily restricted" | Spam detection | Stop for 72h, reduce daily volume by 50% |

---

## What NOT to do

- ❌ Send same message to >5 contacts (triggers spam detection)
- ❌ Send at night (>22:00 local time)
- ❌ Send marketing-blasts (use WhatsApp Business broadcast instead)
- ❌ Add links in first message (increases spam score)
- ❌ Use templates with placeholders obviously unfilled

---

## Stack

| Layer | Tool |
|-------|------|
| WhatsApp API | Evolution API (self-hosted at `coach-agents/`) |
| Lead list | `state/coord.json:outreach_targets[]` + manual enrichment |
| Personalization | LLM call with prospect's website scrape |
| Tracking | `state/conversion-attempts.json` (existing) |
| Follow-up | sales-pipeline agent cron (manual trigger) |

---

**Cross-references**:
- `coach-agents/coach-lead-finder/`
- `research/coaching-funnel-playbook.md`
- `state/conversion-attempts.json`
- `analysis/PHASE-7-dept-research/03-sales-growth-research-areas.md` Area #4

