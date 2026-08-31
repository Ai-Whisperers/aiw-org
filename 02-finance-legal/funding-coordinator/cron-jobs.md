# Funding Coordinator Cron Jobs

Two cron jobs to register:
1. Weekly deep sweep (Monday 09:00 PYT)
2. Daily light check (every 6h)

## Cron 1 - Weekly deep sweep

```yaml
name: aiw-funding-weekly-sweep
schedule: "0 9 * * 1"
deliver: origin
skills:
  - trademark-compliance-scrub
  - web_search
```

Prompt for the weekly sweep:

```
You are the funding-coordinator agent for Ai-Whisperers.

1. Read /opt/data/agents/funding-coordinator/PROMPT.md (your full instructions)
2. Read /opt/data/agents/state/funding.json (current state)
3. Read /opt/data/agents/research/funding-landscape-2026-Q3.md (catalog)
4. Read /opt/data/agents/research/funding-landscape-AUDIT-2026-Q3.md (audit)
5. Run weekly sweep:
   a. Discover 3-5 new programs via web_search (LATAM accelerators, EU grants, PY gov)
   b. Score each against Tier S/A/B/C criteria
   c. For Tier S programs: prepare draft application via application-form.md
   d. Update state/funding.json with all findings
6. Check follow-up dates for all in-flight applications:
   - If follow_up_date <= today + 7 days, send reminder to origin chat
7. Update cron reminder queue
8. Post weekly brief to /opt/data/agents/funding-coordinator/outbox/<today>-weekly-brief.md

DO NOT submit applications directly - draft only. Ivan reviews and submits.
DO NOT apply to programs that violate the trademark banlist.
DO NOT spend >4 hours per application draft.

Output: weekly brief with [NEW], [IN-FLIGHT], [DECIDED], [NEXT-ACTIONS] sections.
```

## Cron 2 - Daily light check

```yaml
name: aiw-funding-daily-check
schedule: "0 */6 * * *"
deliver: local
skills:
  - trademark-compliance-scrub
```

Prompt for the daily check:

```
You are the funding-coordinator agent.

1. Read /opt/data/agents/state/funding.json
2. Check for application responses / status changes since last run
3. Check for upcoming deadlines (next 7 days)
4. If anything urgent:
   - Post to origin chat with [FUNDING-ALERT] tag
   - Include: program name, deadline, action needed
5. If nothing urgent: exit silently

Silent unless alert.
```

## Setup instructions

```bash
# Register the weekly sweep (requires Ivan approval - signature-bearing agent)
hermes cron create --name aiw-funding-weekly-sweep \
  --schedule "0 9 * * 1" \
  --deliver origin \
  --skills trademark-compliance-scrub,web_search \
  --prompt /opt/data/agents/funding-coordinator/cron/weekly-sweep-prompt.md

# Register the daily check (silent unless alert)
hermes cron create --name aiw-funding-daily-check \
  --schedule "0 */6 * * *" \
  --deliver local \
  --skills trademark-compliance-scrub \
  --prompt /opt/data/agents/funding-coordinator/cron/daily-check-prompt.md
```

Status: Both cron jobs documented, NOT yet registered. Ivan to confirm before registration.

## Why deliver local for daily check

The daily check is a silent watchdog - only fires when there is an alert. No need to flood origin chat with "no new findings" messages every 6 hours.

## Why deliver origin for weekly sweep

The weekly brief is actionable: new programs to review, follow-ups due, next-actions. Ivan needs to see this in the main feed.

## Trademark scrub discipline

Every cron run must:
1. Load trademark-compliance-scrub skill
2. Apply to any draft before writing to disk
3. Verify org name is clean
4. Log scrub results in state/funding.json

If scrub fails, abort the application draft and flag in outbox.
