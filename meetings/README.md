# Meetings

> **Design decisions live here.** Runtime org (agents, crons, prompts) lives in the rest of this repo.

## Source of truth (how to read)

| Need | File |
|---|---|
| Department-design decisions (freeze, PO, names, what not to build) | [`department-design/README.md`](department-design/README.md) |
| Ratified decisions from those sessions | [`department-design/DECISIONS.md`](department-design/DECISIONS.md) |
| What to cover next time | [`department-design/NEXT-AGENDA.md`](department-design/NEXT-AGENDA.md) |
| Live agent/dept catalog (implementation) | [`analysis/DEPT-AGENTS-ROLES-COMPLETE.md`](../analysis/DEPT-AGENTS-ROLES-COMPLETE.md) |
| Ivan’s next actions | [`analysis/2026-09-01-IVAN-DEPT-DESIGN-TODO.md`](../analysis/2026-09-01-IVAN-DEPT-DESIGN-TODO.md) |

**Conflict rule:** if a meeting note and the catalog disagree on *what exists in git*, the catalog plus `git log` win. If they disagree on *what we decided to do*, `department-design/DECISIONS.md` wins until a newer dated meeting supersedes it.

## How to add a session

1. Copy [`TEMPLATES/session.md`](TEMPLATES/session.md).
2. Save as `department-design/YYYY-MM-DD-short-slug.md` (or another topic folder if it is not org-design).
3. Update that topic’s `README.md` index and, if anything was ratified, `DECISIONS.md`.
4. Put leftovers on `NEXT-AGENDA.md`. Do not leave decisions only in WhatsApp or phone audio.

Owner of the written record: **Analisa** (`business-analyst`) after each department-design or weekly that touches org structure. Humans still ratify `DECISIONS.md`.
