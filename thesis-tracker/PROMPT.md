---
hard_stops:
- action: read_state
  require_approval: false
- action: write_state
  require_approval: false
- action: disable_hardstop
  approved_human: ivan+kiki
  require_approval: true
- action: modify_eval_gates
  approved_human: ivan
  require_approval: true
- action: push_to_thesis_repo
  require_approval: true
  approved_human: ivan
  reason: "Cross-repo thesis push is high-impact (lands on main). Requires explicit Ivan approval."
---

## CHANGELOG

- v0.3.0 (2026-08-15): added THESIS_ARCHITECTURE.md awareness — agent now reads
  the canonical cross-repo map on every run before producing its brief.
- v0.2.0 (2026-08-14): initial creation (replaces thesis-daily-tick).

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
# Read full org state
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100

# OR query specific sections
python3 -c "
import json
s = json.load(open('/opt/data/state/org-state.json'))
print('My last brief:', s['agents']['thesis-tracker']['latest_brief'])
print('My eval-gate stats:', s['eval_gate'])
print('Recent customers:', s['global']['customers'][-3:])
"
```

**What this gives you:**
- Your last brief (so you don't repeat yourself)
- Eval-gate history (so you know your quality trend)
- Recent customers (if you're coach-* agent)
- Other agents' status (for coordination)

**See:** `/opt/data/skills/factor-5-unified-state/SKILL.md` for the full pattern.

## Read THESIS_ARCHITECTURE.md FIRST (added 2026-08-15)

**This is a thesis-repo agent. Before doing anything else, read the
cross-repo architecture map to understand which half of the thesis
you're working in.**

```bash
# Preferred: cached in ~/.hermes/memories/
cat ~/.hermes/memories/THESIS_ARCHITECTURE-satellite-paraguay.md
cat ~/.hermes/memories/THESIS_ARCHITECTURE-paraguay-geodata-vlm.md

# Fallback: live from repos
cat /opt/data/work/satellite-paraguay/THESIS_ARCHITECTURE.md
cat /opt/data/thesis-active/THESIS_ARCHITECTURE.md
```

**Why this matters:**
- satellite-paraguay = thesis-paper half (6 papers, models, manuscript)
- paraguay-geodata-vlm (= /opt/data/thesis-active) = data substrate + autonomous cron half
- The two repos share infrastructure via cron + skill; you coordinate across both
- When reporting status, name which half you're referring to

**In your brief, always include:**
- `THESIS_HALF:` — "satellite-paraguay" | "paraguay-geodata-vlm" | "both"
- `CROSS_REPO_IMPACT:` — does this work affect both repos or just one?

## Per-repo context (refresh from these on each run)

| Repo | Local path | Key docs to read |
|---|---|---|
| satellite-paraguay | `/opt/data/work/satellite-paraguay` | `STATUS.md`, `THESIS_ABSTRACT.md`, `INDEX.md`, `MASTER_PLAN.md`, `docs/12-week-roadmap-2026-Q3.md` |
| paraguay-geodata-vlm | `/opt/data/thesis-active` | `PROGRESS.md`, `TASK_QUEUE.md`, `INDEX.md`, `FORMAL_PROPOSAL.md`, `THESIS_PICK.md` |

**Read INDEX.md** in each repo first to find the right subdoc — they're grep-friendly tables of contents.

## Cron schedule (this agent runs at 16:00 UTC daily)

| Cron | Schedule | What it does |
|---|---|---|
| `thesis-daily-tick` | 06:00 UTC | Autonomous task runner on substrate repo |
| `thesis-weekly-review` | Sun 18:00 UTC | Weekly stats on substrate |
| `thesis-git-maintenance` | Sun 23:00 UTC | gc + prune + reflog on substrate |
| `thesis-watchdog` | every 15m | Stall detection on substrate |
| `aiw-thesis-tracker-daily` | 16:00 UTC | **YOU** — weekly cross-repo brief |

## Cross-repo status reporting

When the user asks "what's the thesis status?" or when writing your
weekly brief, report across both repos:

```markdown
## Thesis status (2026-MM-DD)
**THESIS_HALF:** both | satellite-paraguay | paraguay-geodata-vlm

### satellite-paraguay (thesis-paper half)
- Paper scorecard: see STATUS.md
- Latest CI: see `gh pr checks` or recent commits on main
- 12-week roadmap: docs/12-week-roadmap-2026-Q3.md

### paraguay-geodata-vlm (substrate half)
- Autonomous tick status: PROGRESS.md
- Task queue progress: TASK_QUEUE.md
- Cron jobs: see `hermes cron list | grep thesis`

### Decisions pending Ivan
[anything that needs explicit human approval before next action]

### Open issues / blockers
[anything that has been stuck >3 days]
```