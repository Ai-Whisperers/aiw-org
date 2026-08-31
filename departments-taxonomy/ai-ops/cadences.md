# AI Ops cadences (Hermes cron registration)

> DEMIURGE-079

| hermes_cron_id | agent | schedule | PYT |
|----------------|-------|----------|-----|
| demiurge-ai-ops-coordinator | ai-ops-coordinator | 0 9 * * * | Daily 09:00 |

Register via `hermes cron add` when runtime available. Mirror to `cron-jobs-snapshot` on commit.
