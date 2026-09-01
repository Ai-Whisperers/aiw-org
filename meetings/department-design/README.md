# Department design — source of truth

> **This folder is the canonical record of meetings that design AI Whisperers departments, roles, and agents.**
>
> Implementation (what is in git today) is [`analysis/DEPT-AGENTS-ROLES-COMPLETE.md`](../../analysis/DEPT-AGENTS-ROLES-COMPLETE.md).  
> Next work for Ivan is [`analysis/2026-09-01-IVAN-DEPT-DESIGN-TODO.md`](../../analysis/2026-09-01-IVAN-DEPT-DESIGN-TODO.md).

**Objective of this thread (from the Magic Tower board):** departments, roles, agents — not a second organigram in chat.

## How to use this in a meeting

1. Read [`DECISIONS.md`](DECISIONS.md) first (what is already locked).
2. Read [`NEXT-AGENDA.md`](NEXT-AGENDA.md) (what this session is for).
3. After the session, file a dated note from [`../TEMPLATES/session.md`](../TEMPLATES/session.md).
4. Promote only ratified items into `DECISIONS.md`. Leave speculation in the dated note.

## Session index

| Date | Session | Record |
|---|---|---|
| 2026-08-28 | John design brief (product owner, named agents, sell departments, talk via repo) | [2026-08-28-john-design-brief.md](2026-08-28-john-design-brief.md) |
| 2026-08-28 | Weekly (Kiki chair): departments scheduled for Monday; don’t run all depts | [2026-08-28-weekly.md](2026-08-28-weekly.md) |
| Week of 2026-08-28 | Magic Tower board (org line + named agents) | [2026-08-magic-tower-board.md](2026-08-magic-tower-board.md) |

Raw TurboScribe files (truncated at 30 min) are **evidence**, not the source of truth. Do not paste them into this repo. Summaries above replace them.

## Locked picture (one screen)

```
Shareholders → Board → CEO (Ivan)
                 CTO (Kiki) · CFO/COO still hats, not extra depts

Six charter depts only (Phase 30 freeze):
  01 Operations     Analisa (meetings/briefs) + coord
  02 Finance-legal
  03 Sales-growth   Prospia, Markina/Calliope, Saleina/Apollo
  04 Engineering    Devin, Qualis, Safina
  05 Research       Renata
  06 People         Kiki-coach (sister repo)

Not a seventh charter yet: Product Management / PO (John’s #1 gap).
```

## Name map (spoken → repo)

| Spoken on the board / in the room | Agent id | Notes |
|---|---|---|
| DEVIN / Rosterina / “Rostercho” | `engineering-roster` | **Devin**. Duplicate label, one agent |
| Qualis | `qa-automation-runner` | Delivery QA, not AI-safety |
| Safina | `ai-safety-engineer` | Reviews Devin’s *agent* work |
| Analisa | `business-analyst` | Meetings, transcripts, briefs |
| Prospia | `lead-enrichment` | Leads / email / follow-up |
| MaxRina (unreliable spelling) | `marketing-content-producer` | Heritage **Markina**; DEMIURGE **Calliope** |
| Renata | `research-tracker` | |
| Athena / Clio | product-discovery leads | Discovery, **not** product owner |

One spoken name per agent. If two names appear, that is a bug in the notes — fix here, then in `AGENT-NAMES-V2.md`.
