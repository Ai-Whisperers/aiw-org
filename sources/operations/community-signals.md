# Operations — Community Signals

> DEMIURGE-074 — maintained by Echo community scanner

## Monitored communities

| Platform | Target | Scan cadence |
|----------|--------|--------------|
| Reddit | r/startups, r/Entrepreneur, r/operations, r/devops | weekly |
| Hacker News | ops, startup, SaaS tooling threads | weekly |
| First Round Review | ops / org design articles | monthly |
| Lenny's Newsletter | org design, ops scaling posts | monthly |
| RevOps Co-op | cross-functional ops practitioners (Tier 2 overlap — see catalog note) | monthly |
| Operations Nation | startup ops community | monthly |
| Indie Hackers | founder ops / burn rate / tooling threads | weekly |

## Signal types to extract

### Process & coordination

- New async coordination patterns (briefs, decision queues, Loom over meetings)
- Anti-patterns: meeting creep, status-update theater
- Tool recommendations for ops at <50 headcount (OSS preferred)

### Goal-setting & metrics

- OKR implementations that worked/failed at seed stage
- Leading vs lagging indicator choices for ops
- Kill criteria examples for quarterly objectives

### Incident & reliability

- Runbook templates and postmortem formats
- MTTR benchmarks for small teams
- On-call patterns without dedicated SRE

### Cost & vendor management

- SaaS stack audits and cost-cutting playbooks
- Vendor negotiation tactics for startups
- Burn rate tracking tools and benchmarks

### AI-native ops

- How AI-native companies (<50 people) structure ops without middle management
- Agent orchestration patterns (relevant to ai-ops-coordinator)
- Eval gate and drift detection practices

## Output

Writes to `sources/operations/community-signals.md` (append by date).

## Feeds DEMIURGE-075

Extracted signal types map to `departments/operations/signals.yaml` cadence definitions:

| cadence | signal categories |
|---------|-------------------|
| daily | incident health, cron errors, stale repos, decision queue |
| weekly | OKR progress, cycle time, vendor renewals, cross-dept blockers, decision latency |
| monthly | burn rate, cost per transaction |
| quarterly | tool sprawl audit, OKR reset |
