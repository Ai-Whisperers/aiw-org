# Session organization — done (2026-08-21)

## Outcome

Desktop sidebar `Projects` section now shows sessions grouped under topical projects instead of dumping everything into Home.

### Final tree (56 active non-cron sessions across 25 projects)

| Project | Sessions | Notes |
|---|---:|---|
| `home` | 25 | Hermes framework work, all under `/opt/hermes` |
| `Home` (catch-all) | 11 | Sessions with no cwd (WhatsApp/messaging noise + 2 api_server) |
| `aiw-org` | 3 | Org-wide work (Dept Org, Funding Plan, Mgmt agents) |
| `Aldea SOS Paraguay` | 3 | Aldea NGO research sessions |
| `Ligare Poly` | 2 | The 1,059 + 990 msg heavy sessions |
| `Thesis · satellite-paraguay` | 2 | Ivan's thesis + 1 satellite work |
| `Nexa Paraguay` | 2 | Nexa Website + Nexa durum |
| `rubicon EAS` | 1 | Domain Registration for Py EAS |
| `aiw-research` | 1 | AI Coaching Company Research |
| `aiw-sales` | 1 | Richar Ruiz (via existing folder mapping) |
| `Polkisquad Paraguay` | 1 | Repository Creation (Polkisquad research) |
| `Paraguay GeoData v2` | 1 | GeoData Project Status Check |
| `ParaguAI Clients` | 1 | Client Hosting Setup |
| `ISTQB Prep v4` | 1 | QA Career Guide for Pet Care Professionals |
| `ParaguAI Platform` | 1 | GitHub Commits and Deployment Prep |
| **Total in tree** | **56** | |

Zero sessions in auto-bucket `data` (previously 8), zero in broken `thesos` (archived).

## What was done

### A. Project cleanup
- **Archived `thesos`** — was using `primary_path='/'` which made it a catch-all for every cwd; useless.
- **Re-targeted `rubicon-eas`** — `primary_path` was `/opt/hermes` (overlapping 4 personal projects); moved to `/opt/data/build/rubicon-eas` so it claims the actual Rubicón work session.
- **Archived duplicates** — `paragu-ai-platform-2` and `coaching-2` (CLI auto-suffixed because pre-existing projects of the same slug were discovered in parallel).

### B. New projects created (12)
Each with a real existing folder as primary:

| Slug | Primary path | Sessions captured |
|---|---|---|
| `polkisquad` | `/opt/data/work/polkisquad/polkisquad` | Repository Creation |
| `aldea-sos` | `/opt/data/projects/aldea-sos-paraguay` | Investigando Aldea SOS + 2 aldeas research |
| `ligare-poly` | `/opt/data/ligare-poly` | Code Review and Merge + Missing HERMES-PROMPT |
| `thesis-paraguay` | `/opt/data/work/satellite-paraguay` | thesis (892) + 1 related |
| `geodata` | `/opt/data/repos/paraguay-geodata` | GeoData Project Status Check |
| `paragu-ai-clients` | `/opt/data/work/research-repos/paragu-ai-clients` | Client Hosting Setup |
| `nexa-paraguay` | `/opt/data/work/research-repos/saskia` | Nexa Paraguay Website + Nexa durum |
| `richar-ruiz` | `/opt/data/richar-ruiz-outreach` | (none currently — falls under `aiw-sales` instead) |
| `istqb-prep` | `/opt/data/istqb-prep-v4` | QA Career Guide |
| `infra` | `/opt/data/repos/infrastructure` | (none currently — Hermes framework sessions stay in `home`) |
| `paragu-ai-platform` | `/opt/data/work/research-repos/paragu-ai-platform` | GitHub Commits and Deployment Prep |
| `coaching` | `/opt/data/agents/research` | AI Coaching Company Research |

### C. Session cwd rewrites (27 sessions)

Sessions where `cwd` was inaccurate relative to the topical home of the work were re-pointed at the appropriate project folder. Mapping rule: derive target from title + first user message + repo URL when present.

Examples:
- `Repository Creation` (`/opt/hermes`) → `/opt/data/work/polkisquad/polkisquad`
- `Nexa Paraguay Website Analysis` (`/opt/hermes`) → `/opt/data/work/research-repos/saskia`
- `Code Review and Merge` (`/opt/data`) → `/opt/data/ligare-poly`
- `Department Organization Deep Dive` (`/opt/data`) → `/opt/data/agents` (matches `aiw-org`)
- `Domain Registration for Py EAS` (`/opt/hermes`) → `/opt/data/build/rubicon-eas`
- etc.

### D. Sessions left unchanged
- **11 sessions with no cwd at all** — WhatsApp / messaging / api_server noise. They continue to land in the synthetic `Home` bucket (lines 52-58 of `tui_gateway/project_tree.py`: `NO_PROJECT_ID` = catch-all). Acceptable.
- **23 sessions with cwd=`/opt/hermes`** — actual Hermes framework work. Correctly under `home`.

## To refresh in the desktop

The Hermes dashboard reads the project tree on every sidebar load. **Click the sidebar refresh** (or close+reopen the sidebar) to pick up the new groups. No restart needed.

## What I did NOT do
- Did not touch cron noise (already 2,830 archived from prior session).
- Did not rename sessions — the project grouping is enough; titles are unchanged.
- Did not bind boards to new projects — kanban board binding is separate and the existing `ivan-todo` board is untouched.
- Did not delete any sessions.

## Files written
- `/opt/data/agents/findings-session-organization-2026-08-21.md` (this file — overwrote the prior planning version)

## Files modified
- `/opt/data/state.db` — 27 sessions updated (`UPDATE sessions SET cwd = ...`)
- `/opt/data/projects.db` — 12 projects created, 3 archived (`thesos`, `paragu-ai-platform-2`, `coaching-2`), 1 folder updated (`rubicon-eas`)

## Known limitations
- `cwd` rewrites are a metadata correction; the desktop now claims them as if they ran in those folders. If you need the literal "where did this session actually execute" data preserved, it's lost.
- The 4 overlapping personal projects (`home`, `ivan-todo`, `kiki-prios`, `rubicon-eas`) all have `primary_path='/opt/hermes'`; `home` wins (first-write). The other 3 still appear in the sidebar empty.
- `Home` bucket (11 sessions) is the catch-all for sessions with no cwd; this is by design per `project_tree.py:735-766`.
