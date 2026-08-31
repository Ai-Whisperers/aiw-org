# Operations cadences

> DEMIURGE-075, DEMIURGE-076, DEMIURGE-079

| hermes_cron_id | agent | schedule | PYT |
|----------------|-------|----------|-----|
| demiurge-kronos-operations-lead | kronos-operations-lead | 0 7 * * 1-5 | Mon–Fri 07:00 |
| demiurge-management-coordinator | management-coordinator | 0 17 * * 1,4 | Mon+Thu 17:00 |
| demiurge-business-analyst | business-analyst | 30 6 * * * | Daily 06:30 |
| demiurge-bizops-tracker | bizops-tracker | 0 17 * * 0 | Sun 17:00 |
| demiurge-ai-ops-coordinator | ai-ops-coordinator | 0 9 * * * | Daily 09:00 |
| demiurge-compliance-monitor | compliance-monitor | 0 8 * * 1 | Mon 08:00 |

All schedules use `timezone: America/Asuncion`. Register via `hermes cron add` when runtime available. Mirror to `cron-jobs-snapshot` on commit.

Legacy `agents-prompts/` schedules superseded by this file (DEMIURGE-079 schedule authority).
