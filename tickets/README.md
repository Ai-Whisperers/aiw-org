# DEMIURGE Tickets

Ticket prefix: `DEMIURGE-NNN`. Story size: **15–60 minutes** per ticket.

## Folder structure

Each ticket lives at `tickets/DEMIURGE-NNN/`:

| File | Purpose |
|------|---------|
| `plan.md` | Objective, acceptance criteria |
| `context.md` | Current status, focus, blockers |
| `progress.md` | Append-only chronological log |
| `tracker.md` | Phase/task tracker |

## Conventions

- AI-owned tickets: implement and mark done in tracker when deliverable exists in repo
- Human-owned tickets (`Ivan/John`): remain `pending` until explicit sign-off in `context.md`
- Link deliverables from `plan.md` to paths under `docs/demiurge/`, `departments/`, `sources/`, `demiurge/agents/`
- Commits should reference ticket id: `DEMIURGE-027: Hera marketing lead soul`

## Index

See [INDEX.md](INDEX.md) for all 55 tickets.

## Sprints

| Sprint | Tickets | Theme |
|--------|---------|-------|
| 0 | 001–008 | Domain model |
| 1 | 009–015 | Foundation |
| 2 | 016–025 | Literature + community scanner |
| 3 | 026–033 | Marketing |
| 4 | 034–041 | Sales |
| 5 | 042–047 | Product Discovery |
| 6 | 048–055 | Monitoring + feedback |
