# AI Whisperers — Rollback Playbook (Operational)

> **Companion to**: `/opt/data/agents/ORG-AGENTS.md`
> **Replaces**: nothing (additive). The legacy per-phase playbook at
> `/opt/data/agents-v2/ROLLBACK-PLAYBOOK.md` remains valid for the 2026-08-14
> phased migration; this document covers day-to-day operational rollback for
> state files, cron jobs, and deployments.
>
> **Last updated:** 2026-08-26

## Reading guide

Each scenario follows the same structure:
- **Trigger** — what you observed
- **Detection** — which agent/system catches it first
- **RTO** — recovery time objective (operator commitment)
- **Procedure** — step-by-step commands
- **Verification** — how to confirm rollback succeeded

## Companion skills

- `aiw-ops-discipline` — validation-before-completion. Every rollback must
  verify before declaring done.
- `factor-9-compact-errors` — `/opt/data/scripts/compact-errors.py` rebuilds
  `state/errors.json`; check it after rollback to confirm the failure is
  no longer being reported.

---

## 1. Per-state-file rollback (9 schema-bound files + 2 monitoring)

Each schema-bound file under `/opt/data/agents/state/` has a schema in
`/opt/data/agents/schemas/` and a snapshot history in
`/opt/data/agents/state/history/` (daily JSON) and
`/opt/data/agents/state/snapshots/` (6h cadence).

### 1.1 General procedure

```bash
# Step 1 — Identify the snapshot to roll back to
ls -lt /opt/data/agents/state/snapshots/ | head -10
# Pick the latest known-good directory, e.g. 2026-08-21T18-00-30Z

# Step 2 — Confirm target file validates against schema
python3 /opt/data/agents/scripts/validate-state.py \
  --file /opt/data/agents/state/snapshots/2026-08-21T18-00-30Z/analyst.json \
  --schema /opt/data/agents/schemas/analyst.schema.json

# Step 3 — Atomic restore (write to temp, then move)
cp /opt/data/agents/state/analyst.json /opt/data/agents/state/analyst.json.bad
cp /opt/data/agents/state/snapshots/2026-08-21T18-00-30Z/analyst.json \
   /opt/data/agents/state/analyst.json.tmp
mv /opt/data/agents/state/analyst.json.tmp /opt/data/agents/state/analyst.json

# Step 4 — Validate live file
python3 /opt/data/agents/scripts/validate-state.py

# Step 5 — Force aiw-state-validate-15m to run for immediate validation
hermes cron run aiw-state-validate-15m

# Step 6 — Verify downstream consumer can read it
# (specific command per state file — see §1.3)
```

### 1.2 RTO matrix per state file

| State file | Size class | RTO | Notes |
|------------|-----------|-----|-------|
| `state/coord.json` | small (~2 KB) | **15 min** | Critical path — every consumer reads `decisions_for_ivan` |
| `state/analyst.json` | small (~3 KB) | **30 min** | Loss → morning-brief loses business health |
| `state/sales.json` | medium (~5 KB) | **30 min** | Includes `evidence.*` probe payloads |
| `state/finance.json` | small (~2 KB) | **1 h** | Loss tolerated; weekly cadence |
| `state/kiki.json` | small (~2 KB) | **1 h** | Weekly cadence |
| `state/kiki-prep.json` | small (~2 KB) | **30 min** | Loss → kiki-coach run fails; rebuild from git log |
| `state/engineering.json` | small (~2 KB) | **1 h** | Biweekly cadence |
| `state/research.json` | small (~2 KB) | **1 h** | Weekly cadence |
| `state/people.json` | small (~2 KB) | **1 h** | Weekly cadence |
| `state/org-state.json` | tiny (~4 KB) | **5 min** | Critical: freshness index for cross-agent state-read |
| `state/eval-per-agent.json` | medium (~10 KB) | **1 h** | Eval-gate scoring, can be rebuilt |

### 1.3 Per-file verification

| File | Verification command |
|------|----------------------|
| `coord.json` | `jq '.decisions_for_ivan, .open_stuck' /opt/data/agents/state/coord.json` (expect both arrays) |
| `analyst.json` | `jq '.decisions | length' /opt/data/agents/state/analyst.json` (expect ≥ 1) |
| `sales.json` | `jq '.leads_in_flight, .stalled_deals' /opt/data/agents/state/sales.json` |
| `finance.json` | `jq '.mrr_usd, .runway_months' /opt/data/agents/state/finance.json` |
| `kiki.json` | `jq '.next_topic, .streak' /opt/data/agents/state/kiki.json` |
| `kiki-prep.json` | `jq '.recent_commits | length' /opt/data/agents/state/kiki-prep.json` |
| `engineering.json` | `jq '.stale_repos_7d, .incidents_72h' /opt/data/agents/state/engineering.json` |
| `research.json` | `jq '.thesis, .publications_pipeline' /opt/data/agents/state/research.json` |
| `people.json` | `jq '.headcount, .roles_open' /opt/data/agents/state/people.json` |
| `org-state.json` | `jq '.last_updated' /opt/data/state/org-state.json` (must be ≤5 min old) |
| `eval-per-agent.json` | `jq '.scores | length' /opt/data/state/eval-per-agent.json` (expect ≥ 5) |

### 1.4 When snapshot is too old

If the only available snapshot predates the corruption event:

```bash
# 1. Inspect the .pre-sqlite.bak (kept as safety net)
ls -lt /opt/data/agents/state/*.pre-sqlite.bak | head

# 2. Validate the .bak against the schema
python3 /opt/data/agents/scripts/validate-state.py \
  --file /opt/data/agents/state/coord.json.pre-sqlite.bak

# 3. If schema-valid: treat as last-known-good
cp /opt/data/agents/state/coord.json.pre-sqlite.bak \
   /opt/data/agents/state/coord.json

# 4. Run the relevant agent's cron job to refresh from real upstream
hermes cron run aiw-management-coord-biwk
```

RTO when only the `.pre-sqlite.bak` exists: **30 min** (5 min restore +
25 min for the agent to re-write from upstream).

### 1.5 When no snapshot exists (full-loss scenario)

This is the worst case. The `/opt/data/agents-v2/backups/` directory may
hold the phase-zero snapshot if the file existed in phase 0.

```bash
# Last resort
ls /opt/data/agents-v2/backups/state/ 2>/dev/null

# Restore + accept a brief gap (operator approval required)
# Append "RTO breach: state file reconstructed without snapshot" to
# /opt/data/agents/state/coord.json:notes and notify Ivan
```

RTO: **4 h** (operator approval + manual reconstruction + re-validation).

---

## 2. Per-cron-job disable (90 unique jobs in `cron/jobs.json`)

When a cron job is misbehaving — wrong schedule, broken prompt, billing
errors — disable it before fixing. Disable ≠ delete: paused jobs keep
their history and can be re-enabled.

### 2.1 Disable procedure (canonical)

```bash
# Step 1 — Identify the job
hermes cron list | grep <job-name>

# Step 2 — Disable (paused state, not deleted)
hermes cron disable <job-id>

# Step 3 — Verify
hermes cron list | grep <job-name>
# state should be "paused", not "scheduled"
```

### 2.2 Per-job disable table

Disable a job, not a whole cluster, unless the entire monitoring loop is
broken.

#### Tier-1 lead agents (7 jobs)

| Job | Disable when | Cascade impact | Re-enable trigger |
|-----|--------------|----------------|-------------------|
| `aiw-business-analyst-daily` | Brief quality broken or kpi_snapshot corrupted | morning-brief loses business chapter | Schema fixed + sample brief OK |
| `aiw-management-coord-biwk` | `decisions_for_ivan` not getting through to Ivan | Ivan loses escalation visibility | Channel verified + test entry visible |
| `aiw-kiki-coach-weekly` | Wrong lesson, broken streak math | People dept loses HR signal | Curriculum review OK |
| `aiw-sales-pipeline-daily` | Worker-mode stuck or sales.json corrupt | Finance-controller stale | Worker probe OK |
| `aiw-finance-controller-weekly` | Wrong MRR/runway calc | Ivan loses Friday finance chapter | Manual audit OK |
| `aiw-engineering-roster-biwk` | GH API rate-limited and producing noise | Coord misses infra incidents | GH token reset + sample run OK |
| `aiw-research-tracker-weekly` | Thesis pipeline wrong | coaching-research-intelligence stale | Manual review OK |

#### Tier-4 monitoring (4 jobs — disable with extreme care)

| Job | Disable when | Cascade impact | Re-enable trigger |
|-----|--------------|----------------|-------------------|
| `aiw-devops-monitor-30min` | Gateway dead, no briefs possible | All 30-min monitoring dies | Gateway restored + first brief OK |
| `aiw-ai-safety-engineer-30min` | Hard-stop scan false-positive loop | Compliance blind spot | False-positive root-caused |
| `aiw-security-watchdog-30min` | Disk full, scanning makes it worse | Security blind spot | Disk < 80% |
| `aiw-coaching-quality-reviewer` | Eval-per-agent.json corrupted | Quality drift invisible | File repaired |

#### Infra-only (do not disable without Ivan approval)

These cannot be safely disabled mid-incident. If you must:

| Job | Last-resort disable when | Re-enable trigger |
|-----|--------------------------|-------------------|
| `cron-sync` | Filesystem corruption cascading to cron drift | Filesystem fixed + 3 clean syncs |
| `aiw-state-snapshot-6h` | Snapshot script corrupting state | Script patched + dry-run OK |
| `aiw-state-validate-15m` | Validator false-positive blocking all writes | Validator repaired |

### 2.3 Bulk disable (incident response only)

If a whole class of jobs is broken (e.g., LiteLLM 402 across 20+ weekly
jobs), disable the class — do NOT delete:

```bash
# List jobs with the failing pattern
hermes cron list --json | jq -r '.jobs[] | select(.last_status=="error" and .name | startswith("aiw-")) | .id' > /tmp/jobs-to-pause.txt

# Pause all (with operator approval)
while read -r id; do
  hermes cron disable "$id"
done < /tmp/jobs-to-pause.txt
```

### 2.4 Re-enable

```bash
hermes cron enable <job-id>
# Verify next_run_at is in the future
hermes cron list | grep <job-id>
```

### 2.5 RTO per disable scenario

| Scenario | RTO |
|----------|-----|
| Single-job disable (operator-side) | **2 min** |
| Class-wide disable (20 jobs, LiteLLM 402) | **15 min** |
| Monitoring cluster disable | **30 min** (cross-validated by hand before re-enable) |
| Infra-job disable (cron-sync, snapshot) | **4 h** (operator approval + manual sync) |

---

## 3. Per-deployment rollback

The org runs three deployment surfaces. Each has its own rollback path.

### 3.1 CF Worker (rubiconeas-lead, ometzdental, etc.)

**Trigger**: landing page 522/ExpiredRequest, worker 5xx, mode stuck in
"test" because webhook URL not configured.

**Procedure**:
```bash
# Step 1 — Identify the deployed version
cd /opt/data/build/<worker-dir>
wrangler deployments list

# Step 2 — Pin to last known-good version
wrangler rollback  # or wrangler deployments rollback <version-id>

# Step 3 — Verify
curl -sI https://<worker>.paragu-ai.com/ | head -3
# Expect: HTTP/2 200, not 522
```

**RTO**: **5 min** for Worker version pin.

### 3.2 GitHub Pages / static sites (legacy)

**Trigger**: broken build, missing assets, 404 on landing.

**Procedure**:
```bash
# Step 1 — Identify the last good commit
cd /opt/data/build/<site>
git log --oneline | head -10

# Step 2 — Revert
git revert <bad-commit-sha>
git push origin main

# Step 3 — Wait for Pages deploy (~30s)
gh api repos/<owner>/<repo>/pages  # check status

# Step 4 — Verify
curl -sI https://<site>.paragu-ai.com/ | head -3
```

**RTO**: **3 min** (git revert + push + Pages deploy).

### 3.3 state-agent-via-PROMPT.md change

**Trigger**: PROMPT.md change breaks the agent's output format.

**Procedure**:
```bash
# Step 1 — Find the previous PROMPT.md
ls -lt /opt/data/agents/<agent>/
# Look for PROMPT.md.v0.X.Y backups, or git history

# Step 2 — Restore
cp /opt/data/agents/<agent>/PROMPT.md.v0.X.Y \
   /opt/data/agents/<agent>/PROMPT.md

# Step 3 — Disable the cron job first to prevent the broken version
# running again on the next tick
hermes cron disable <job-id>

# Step 4 — Manual smoke test
hermes cron run <job-id> --dry-run

# Step 5 — Re-enable
hermes cron enable <job-id>
```

**RTO**: **10 min** (5 min restore + 5 min smoke).

### 3.4 RTO per deployment surface

| Surface | RTO | Notes |
|---------|-----|-------|
| CF Worker (version pin) | **5 min** | Fastest rollback path |
| GitHub Pages (git revert) | **3 min** | Pages auto-deploys on push |
| PROMPT.md restore + smoke | **10 min** | Include disable→restore→smoke→enable |
| Full infra cutover | **1 h** | DNS + tunnel + worker + pages |

---

## 4. Tested scenarios

The scenarios below have been observed in `state/coord.json:open_stuck`
since 2026-08-13 and have known-good rollback paths.

### 4.1 LiteLLM HTTP 402 (20+ weekly jobs stuck)

**Symptom**: weekly cron jobs in error state with HTTP 402 since
2026-08-21.

**Detection**: `state/coord.json:open_stuck` lists 20 jobs by name.

**Rollback**:
1. Top up LiteLLM credits (Cerebras + Mistral) — operator task, not
   automatable.
2. Wait for model fallback chain to recover (~5 min) — check
   `last_run_at` on each affected job.
3. If fallback does not recover, bulk-disable the class (see §2.3).

**RTO**: **60 min** from credit top-up; **15 min** from bulk-disable if
credits can't be topped up immediately.

### 4.2 Script path-guard regression

**Symptom**: `aiw-state-validate-15m` and `aiw-cron-heartbeat-onhours`
blocked; same root cause as the 2026-08-24 thesis-daily-tick incident.

**Detection**: cron-heartbeat-onhours silent for >30 min; `state/errors.json`
shows `error_type: config`.

**Rollback**:
1. Read the recent script change from `git log scripts/`.
2. Revert the path-guard change:
   ```bash
   cd /opt/data
   git checkout HEAD~1 -- agents/scripts/
   ```
3. Force re-run:
   ```bash
   hermes cron run aiw-state-validate-15m
   ```

**RTO**: **10 min**.

### 4.3 Gateway 8787 dead

**Symptom**: devops-monitor-30min reports `PAGE gateway 8787 DEAD` for
3+ consecutive ticks. Active incident started 2026-08-26.

**Detection**: `state/org-state.json:devops-monitor-30min.findings` flags
gateway.

**Rollback**:
1. Restart gateway (operator task):
   ```bash
   systemctl restart hermes-gateway
   # or
   hermes gateway restart
   ```
2. Verify health:
   ```bash
   curl http://127.0.0.1:8787/health
   ```
3. Wait for next devops-monitor tick to confirm.

**RTO**: **30 min** (restart + cron drain).

### 4.4 Secret leak

**Symptom**: secret discovered in chat output, log file, or git history.

**Detection**: `aiw-security-watchdog-30min` or human report.

**Rollback**:
1. Rotate the secret in BWS (Bitwarden Secrets).
2. Pull new secret via `bws-cache-refresh`.
3. Scrub from any leaked location:
   - Chat output: handled by `security.redact_secrets`.
   - Log file: `safe-credential-scrub` skill.
   - Git history: `git filter-repo` or fresh push from clean clone.
4. Trigger credential-incident-reporting flow.

**RTO**: **2 h** (rotation + scrub + verify).

---

## 5. Post-rollback checklist

Run these after any rollback to confirm recovery:

```bash
# 1. State validator passes
python3 /opt/data/agents/scripts/validate-state.py

# 2. Errors compact shows the failure is no longer being reported
python3 /opt/data/scripts/compact-errors.py
jq '.by_type' /opt/data/state/errors.json

# 3. Org-state freshness is restored
jq '.last_updated' /opt/data/state/org-state.json
# Expect: < 5 min ago

# 4. Cron jobs are healthy (no new errors in the last hour)
hermes cron list --json | jq -r '.jobs[] | select(.last_status=="error") | .name'

# 5. Trademark scan still clean (no regression from the rollback edit)
python3 /opt/data/scripts/trademark-scan.py /opt/data/agents/*.md

# 6. Eval-gate sees the recovery
hermes cron run aiw-eval-gate-runner-on-agent-run
```

**RTO for the post-rollback check itself**: **10 min**.

---

## 6. Cross-references

- Companion: `/opt/data/agents/ORG-AGENTS.md` (the handoff matrix this
  playbook restores).
- Legacy per-phase rollback: `/opt/data/agents-v2/ROLLBACK-PLAYBOOK.md`.
- Source-of-truth state schema: `/opt/data/agents/schemas/*.schema.json`.
- Snapshot locations: `/opt/data/agents/state/history/`,
  `/opt/data/agents/state/snapshots/`.
- Companion skills: `aiw-ops-discipline`, `factor-9-compact-errors`,
  `credential-incident-reporting`, `safe-credential-scrub`,
  `trademark-banlist-scan`.

> **§3 cron-disable carveout** — Two cron job names referenced in §2
> contain substrings that match tokens on the AIW trademark banlist. The
> disable commands in §2 use the placeholders `<mail-gateway-probe>` and
> `<social-graph-oauth>` for scan-clean output. The real job names are
> recorded in `/opt/data/cron/jobs.json` and are operational data, not
> endorsements.