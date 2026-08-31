# Compliance cadences (Hermes cron registration)

> DEMIURGE-079

| hermes_cron_id | agent | schedule | PYT |
|----------------|-------|----------|-----|
| demiurge-compliance-monitor | compliance-monitor | 0 8 * * 1 | Mon 08:00 |

Register via `hermes cron add` when runtime available. Mirror to `cron-jobs-snapshot` on commit.
