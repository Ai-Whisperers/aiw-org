# revops-pipeline-analyzer-daily — Output sink only

> **Status**: Outbox-only directory. **No PROMPT.md** by design.
>
> This dir is the **output sink** for `revops-pipeline-analyzer` running at daily cadence.
> The parent agent (`revops-pipeline-analyzer`) writes its daily output here.

## Why this exists

After Phase 25 (around-the-clock upgrade), the daily variant of `revops-pipeline-analyzer` was:
1. **Folded into the parent** — single PROMPT.md, single cron
2. **Output goes here** — keeps different cadences visually separated for human review

## Files in this dir

| File | Purpose |
|------|---------|
| `outbox/` | Parent agent's daily output (review-only) |

## If you want to delete this dir

**DON'T** — it's referenced by the parent cron. Instead:
1. First check the parent cron schedule (`/opt/data/cron/jobs.json`)
2. Find the parent agent's PROMPT.md and change its `outbox:` path
3. THEN delete this dir

