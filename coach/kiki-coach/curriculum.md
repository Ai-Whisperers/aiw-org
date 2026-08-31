# Kiki Coach — Curriculum (rolling 8-week plan)

> Topic queue. Kiki reorders, skips, or adds. This file is hers to edit.
> The coach reads `current_focus` and `next_topic` from `/opt/data/agents/state/kiki.json`, not this file.

| #  | Topic | Why now | Status |
|----|-------|---------|--------|
| 1  | Git rebase vs. merge in a 2-person team | Solo branch discipline before 3rd hire | ⏳ queued |
| 2  | Reading a Next.js App Router stack trace | She deploys daily; logs are the bottleneck | ⏳ queued |
| 3  | CODEOWNERS that actually owns | When team grows; sets the precedent | ⏳ queued |
| 4  | Env vars across surfaces: .env.local vs GH Secret vs CF Worker | Reduces credential leaks | ⏳ queued |
| 5  | Tailwind v4 design tokens vs inline styles | ParaguAI Builder lesson; applies everywhere | ⏳ queued |
| 6  | Reading a CF Worker trace — KV, R2, subrequest limits | Live in production for rubicon-eas-lead | ⏳ queued |
| 7  | Docker Swarm deploy logs: the 5 lines that matter | Less than 5 min to debug if she knows | ⏳ queued |
| 8  | Husky + lint-staged pre-commit | Catches problems before CI | ⏳ queued |

## Topics to add later (when #1-8 done)

- Reading the rubicon-eas-lead webhook flow end-to-end
- Migrating from Pages Router → App Router (paragu-ai-platform example)
- Traefik middleware patterns (paragu-ai-platform uses 4)
- CF R2 signed URLs (used in client sites)
- Bash trap-based cleanup in cron scripts (she'll touch infra soon)
- Postgres EXPLAIN for the paragu-ai-platform DB
- Supabase RLS for multi-tenant SaaS

## Product-Engineering Track (added 2026-08-28)

> Engineering discipline for owning delivery. All topics fit under
> "software engineering craft" in the charter (line 16) — scoping,
> estimation, and scope discipline are craft, not business.

| #  | Topic | Why now | Status |
|----|-------|---------|--------|
| 9  | Decomposing a proposal into deliverables before saying yes | Ivan closes the deal, she builds it — the handoff starts here | ⏳ queued |
| 10 | Effort estimation: T-shirt sizing, the "2x your gut" rule, story points | Required before committing a delivery date | ⏳ queued |
| 11 | Saying no to scope creep (change order template, "yes, and..." pattern) | She is one person; every unspoken extra is a slipped date | ⏳ queued |
| 12 | Breaking a 3-month project into 2-week milestones | Replaces "I'll ship when it's done" with predictable cadence | ⏳ queued |
| 13 | What "done" means: acceptance criteria, demo checklist, signal-early-on-slip | Sales and engineering must agree before the project starts | ⏳ queued |
| 14 | Reading the open-PR queue as a bandwidth signal | Tells her when to accept new work and when to refuse | ⏳ queued |
| 15 | Async status updates that don't take 30 minutes to write | Sales team needs to know what's shipping without a meeting | ⏳ queued |

**How this track is taught:**

- Each lesson is one craft pattern, with a concrete example from
  her current backlog (Saskia, Vete, Taller, ISTQB, or 24-site
  conversion).
- Lessons end in a work *she* does (charter rule 2). For example:
  - Topic 9 lesson: pick the next proposal in her queue, write the
    deliverable list, compare it to what was sold.
  - Topic 10 lesson: take her own 2x-gut estimate, write it down,
    calendar when she'll know if she was right.
- No lesson longer than 700 words (charter rule 3).
- Spanish first, English fallback (charter rule 6).

## Topics explicitly OUT (per charter)

- Pricing, ICPs, sales copy
- Client relationship management
- Strategic org decisions
- Legal / financial
- **How much to charge, when to hire, when to push back on Ivan** —
  1:1 with Ivan, not a coach's call (charter line 29)

Last updated: 2026-08-28 (added Product-Engineering Track, items 9-15)