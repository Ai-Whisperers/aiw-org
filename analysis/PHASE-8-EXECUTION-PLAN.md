# Phase 8 — Execute the Autonomous Research Areas

> **Date**: 2026-09-01
> **Trigger**: Ivan's "work on all of this"
> **Scope**: Execute the **30 research areas** the AI can complete autonomously (no Ivan/Kiki/external blocker). Defer 20 that need human input.

---

## Scope analysis — 52 areas from Phase 7

| Category | Count | Action |
|----------|-------|--------|
| **Autonomous** (AI can do now) | **30** | **Execute in Phase 8** |
| Needs Ivan decision/input | 18 | Surface with options; don't execute |
| Needs Kiki input | 2 | Surface; Kiki co-chair |
| Blocked on Tier-3 triggers | 0 | (none triggered) |

---

## The 30 autonomous areas — grouped by dept

### Operations (5 areas) — all autonomous
1. **self-running-scorecard-2026.md** — collect signals, score 7 criteria
2. **hard-stops-enforcement-audit.md** — audit which agents invoke the wrapper
3. **cron-error-patterns-30d.md** — parse `state/cron-error-watchdog.json`
4. **monitor-threshold-calibration-2026.md** — first calibration from real data
5. **health-dashboard.md** — compute z-scores per dept from KPI stacks

### Engineering (10 areas) — all autonomous
6. **12-factor-audit-2026-q3.md** — refresh post-DEMIURGE
7. **ai-safety-posture-2026.md** — current safety posture
8. **drift-detection-methodology.md** — initial methodology (no real data yet)
9. **chaos-test-runbook.md** — build 5 scenario runbooks
10. **eval-aggregate-pass-rate.py** — Python script for aggregate metric
11. **state-write-discipline-catalog.md** — formalize the 5+ patterns
12. **cron-heartbeat-strategy.md** — analyze on/off-hours
13. **phase-25-revisit-2026.md** — status of 14 items
14. **mcp-maturity-tracking.md** — audit MCPs in use
15. **oss-dependency-audit.md** — run pip-audit + npm audit

### Finance (3 areas) — autonomous subset
16. **funding-landscape-2026-Q4.md** — refresh Q3 table
17. **compliance-jurisdiction-matrix.md** — research
18. **tax-structure-comparison.md** — research

### Sales (5 areas) — autonomous subset
19. **funnel-revival-2026.md** — diagnose Worker 404, propose fix
20. **whatsapp-outreach-playbook.md** — research + small test
21. **discovery-methodology-decision.md** — research
22. **lead-enrichment-pipeline.md** — test with 1 prospect
23. **customer-archaeology-2026.md** — mine own data
24. **competitive-positioning-matrix.md** — research

### Research (3 areas) — autonomous subset
25. **citation-coverage-audit-2026.md** — mine docs, verify citations
26. **source-materials-curation-policy.md** — define scoring
27. **peer-review-process.md** — research methodology

### Board (3 areas) — all autonomous
28. **co-chair-decision-rights.md** — draft from literature
29. **quarterly-review-template.md** — template + agenda
30. **risk-register-2026.md** — rate likelihood × impact

---

## Plan — 5 rounds (sequential by dept, 6 areas per round)

| Round | Focus | Areas |
|-------|-------|-------|
| R1 | Engineering (priority — closes safety holes) | #6-15 (10 areas) |
| R2 | Operations + Board | #1-5, #28-30 (8 areas) |
| R3 | Sales (revival focus) | #19-24 (6 areas) |
| R4 | Finance + Research | #16-18, #25-27 (6 areas) |
| R5 | Feedback + commit | All combined |

---

## Out of scope (correctly)

- Areas needing Ivan (margin analysis, bandwidth audit, etc.) → surface in feedback
- Areas needing Kiki (her growth path, coaching methodology) → surface in feedback
- Tier-3 expansion → correctly deferred per doctrine

---

## Success criteria

- 30 research artifacts produced (mix of markdown files + 1 Python script)
- All output paths per the Phase 7 catalog
- Lint + smoke gate still 100%
- 1 feedback doc listing what got done + what still needs Ivan/Kiki
- 1 commit

Estimated time: 2-3 hours (significant output).
