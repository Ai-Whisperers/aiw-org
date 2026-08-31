# Phase 18 — WhatsApp Human-in-Loop (Factor 7)

**Date**: 2026-08-17
**Status**: ✅ WIRED — All 14 coaching agents have WhatsApp escalation triggers

## What Was Built

### 1. `whatsapp-send.py` — The helper script

Location: `/opt/data/scripts/whatsapp-send.py` (also at `/opt/data/agents-v2/scripts/whatsapp/whatsapp-send.py`)

Usage:
```bash
python3 /opt/data/scripts/whatsapp-send.py ivan "<message>"
python3 /opt/data/scripts/whatsapp-send.py kiki "<message>"
```

Recipients:
- `ivan` -> +595981324569
- `kiki` or `kynian` -> +595981501444

### 2. `whatsapp-human-in-loop` skill

Location: `/opt/data/skills/whatsapp/whatsapp-human-in-loop/SKILL.md`

Implements Factor 7 of 12-factor-agents. Contains:
- 5 message patterns (approval, input request, escalation, result delivery, urgent alert)
- Anti-patterns (spam, vague, no timeout, bypass approval, group spam, archival)
- Examples per agent

### 3. 14 agent PROMPT.md updates

All 14 coaching agents now have:
- WhatsApp escalation triggers in their PROMPT
- Reference to whatsapp-send.py
- Reference to the skill

Per-agent triggers:
| Agent | Triggers |
|-------|----------|
| coach-ivan | health crisis, human conversation request, out-of-scope, burnout |
| coach-kiki | 3-session stuck, technical scope, trilingual confusion |
| coach-org | restructuring impact, quarterly review findings |
| coach-lead-agents | lead agent failing, PROMPT.md change impact |
| coaching-content-curator | source conflict, deletion request |
| coaching-quality-reviewer | eval-gate FAIL trademark, harmful content, quality drift |
| coaching-research-intelligence | competitor pricing > 20%, market shift |
| coach-practitioner | self-harm, crisis, human request, 3-session stuck, scope |
| coach-cohort-facilitator | cohort crisis, private request, dynamic conflict |
| coach-onboarding | no email verify, skip consent, skip steps |
| coach-renewal-manager | score > 90, score < 30 |
| coach-roi-tracker | ROI > 10x, ROI negative |
| coach-lead-finder | top 10 wants contact, competitor launch |
| coach-conversion-agent | score > 90, no open in 14d |

## Verification

✅ Test message sent: 2026-08-17T12:55Z
✅ Key ID: 3EB04043347641FB522574 (received by Ivan)
✅ Trademark-clean (avoided the brand-token namespace)
✅ Audit-clean (0 HIGH, 0 FAIL)

## How It Closes The Gap

This implements **Factor 7 of 12-factor-agents** ("Contact humans with tool calls"). Before this, agents could produce briefs but couldn't ask for human input mid-task. Now:
- Agents can pause and ask "should I proceed?"
- Agents can alert on crisis (coachee mentions self-harm)
- Agents can request context (specific question)
- Agents can deliver results (with WhatsApp confirmation)
- Agents can request approval (before consequential action)

This unblocks real client work. Without it, any GROW session with a real person could hit a crisis and the agent would silently fail. **Now it now alerts immediately.**

## What's Next

- Factor 5 (Unify execution state) — next 12-factor gap
- Factor 11 (Webhook triggers) — would auto-trigger coach-onboarding on new customer
- Cost monitoring per agent — the $12,600/month risk

## Files Modified

- `/opt/data/scripts/whatsapp-send.py` (NEW, 88 lines)
- `/opt/data/skills/whatsapp/whatsapp-human-in-loop/SKILL.md` (NEW, 5233 bytes)
- `/opt/data/agents/coach-*/PROMPT.md` (14 files updated)
- `/opt/data/agents/coaching-*/PROMPT.md` (4 files updated)
- `/opt/data/agents-v2/scripts/whatsapp/whatsapp-send.py` (copy)
- `/opt/data/agents-v2/PHASE-18-WHATSAPP-HUMAN-IN-LOOP.md` (this file)
