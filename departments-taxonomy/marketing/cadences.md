# Marketing cadences (Hermes cron registration)

> DEMIURGE-031

| hermes_cron_id | agent | schedule | PYT |
|----------------|-------|----------|-----|
| demiurge-hera-marketing-lead | hera-marketing-lead | 0 9 * * 1,3,5 | Mon/Wed/Fri 09:00 |
| demiurge-calliope-content | calliope-content-producer | 0 10 * * 1,3,5 | Mon/Wed/Fri 10:00 |
| demiurge-iris-community | iris-community-monitor | 0 11 * * 2,4 | Tue/Thu 11:00 |

Register via `hermes cron add` when runtime available. Mirror to `cron-jobs-snapshot` on commit.
