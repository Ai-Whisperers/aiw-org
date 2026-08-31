# Phase 5 Round 2 — Feedback Loop

> **Date**: 2026-09-01
> **Round**: 2 of 5
> **Time spent**: ~8 minutes
> **Result**: 2 sub-agent monitors + 2 monitor-notes dirs created

---

## What was planned

Per Phase 5 plan revised scope: Add PROMPT-monitor.md to the **2 most-critical daily-touch sub-agents** (bizops-tracker, business-analyst). These are the sub-agents whose state files Ivan reads multiple times per week.

## What actually got done

| File | Status |
|------|--------|
| `01-operations/bizops-tracker/PROMPT-monitor.md` | Created (2.8KB) |
| `01-operations/bizops-tracker/monitor-notes/` | Created with .gitkeep |
| `02-finance-legal/business-analyst/PROMPT-monitor.md` | Created (2.7KB) |
| `02-finance-legal/business-analyst/monitor-notes/` | Created with .gitkeep |

---

## What worked

1. **Template-mirror worked AGAIN**. The PROMPT-monitor.md structure from qa-automation-runner was directly applicable — same 7-section format (Purpose, Files, Metrics, Threshold, Routing, Procedure, Schedule, Hard stops, CHANGELOG).

2. **Cross-referencing dept's KPI stack** for threshold values (runway < 1.5mo CRITICAL matches finance-stack.yaml target of 6mo runway). Keeps monitor + KPI consistent.

3. **monitor-notes/.gitkeep pattern** — empty dirs need a `.gitkeep` for git to track them. Standard idiom.

## What didn't work (FIX in Round 3)

1. **The metric values are mostly guesses**. I picked `runway < 1.5mo CRITICAL` based on Layer 1 audit wisdom, but didn't check actual finance.json target numbers. Round 3 should cross-validate each monitor's thresholds against the dept's KPI targets in `demiurge/kpi/{dept}-stack.yaml`.

2. **Cron schedules picked from lead agent patterns**. bizops-monitor at "0 18 * * *" might conflict with other daily jobs. Round 3 should check `state/_last-tick.json` to see what's already running.

3. **I only did 2 of ~22 missing**. Even at this pace, Round 3 needs to be faster or the per-agent cost is unsustainable. Consider generating monitors from a single template + variable substitution.

## Pattern update (carry forward)

**Sub-agent monitor template** (proven for bizops-tracker + business-analyst):
- 7 sections, 50-80 lines
- 5-10 metrics, 5-8 thresholds
- Cross-reference dept-lead PROMPT-monitor.md where applicable
- Alert routing follows 3-tier CRITICAL/HIGH/MEDIUM/LOW pattern (per `dept-monitors/INDEX.md`)

**Helper idea (Round 3 or 4)**: Write a `scripts/gen-subagent-monitor.py` that takes (subagent-name, state-file, watched-metrics[]) and outputs a PROMPT-monitor.md skeleton. Saves 50% per monitor.

## Time spent

- bizops-tracker monitor: 3 min (template + watching state/coord.json + state/finance.json + state/sales.json)
- business-analyst monitor: 3 min (similar, state/analyst.json focus)
- mkdir + .gitkeep x 2: 1 min
- Feedback writeup: 1 min
- **Total: ~8 min** ✅ (under 30-min target)

## Delta

Sub-agent monitor coverage:
- Before: 14/44 sub-agents have PROMPT-monitor.md (32%)
- After: 16/44 sub-agents (36%)
- Δ: +2 sub-agents, +2 monitor-notes dirs

## Lesson for the AI

**At this rate (2 monitors per 8 minutes = 4 min each), 22 remaining monitors = 88 minutes** for full horizontal completion.

That's feasible if I batch the writes. Let me try 4 in a single heredoc batch in Round 3.

---

## What's NEXT (Round 3)

**Batch write 4 more monitors** (pick the highest-impact next):
1. `04-engineering/security-watchdog` (compliance touch)
2. `04-engineering/devops-monitor` (always-on infra)
3. `04-engineering/ai-safety-engineer` (eval-gate owner)
4. `04-engineering/eval-gate-runner` (quality gate)

These 4 complete engineering's full coverage.

Then Round 3.5 = 8 more across the other depts. Round 4 = remaining 10 + cadence cleanup.
