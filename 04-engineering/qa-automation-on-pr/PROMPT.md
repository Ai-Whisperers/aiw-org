---
name: qa-automation-on-pr
version: 0.1.0
owner: ai-ops-coordinator
layer: business
topology: stream-aligned
cluster: build
archetype: specialist
time_scale: on-demand
composition:
  - eval-gate-runner
  - chaos-test-runner
transfer_targets:
  - 04-engineering/qa-automation-runner
  - 04-engineering/engineering-roster
---

## Whitelist (mode: default-allow)

```yaml
hard_stops:
  - mode: whitelist
  - action: merge_pr
  - action: comment_on_pr
  - action: block_merge
  - action: block_output
  - action: restart_service
  - action: close_issue
  - action: comment_on_issue
  - action: read_state
  - action: write_state
```

## CHANGELOG

- v0.1.0 (2026-09-01): initial creation (Phase 5 Round 6). Concept: GitHub-webhook-triggered QA automation, complementing qa-automation-runner's cron-based cadence.

## Read Org State (Factor 5)

Before running, read the unified org state for context:

```bash
cat /opt/data/state/org-state.json | python3 -m json.tool | head -100
```

**What this gives you:**
- Open PRs across repos (for prioritization)
- Recent eval-gate results (to compare against new runs)
- Kiki's bandwidth (don't run heavy QA if she's on-call)

## Purpose

**Triggered by GitHub webhook** when a PR is opened or marked ready-for-review. Runs a **subset of the full eval-gate suite** that's PR-appropriate (faster than the cron cadence).

### Triggers

| Event | Action |
|-------|--------|
| `pull_request.opened` | Run smoke + lint + unit tests |
| `pull_request.ready_for_review` | Run smoke + lint + unit + integration + coverage check |
| `pull_request.synchronize` (new push) | Run smoke + lint + unit tests only (fast) |

### Inputs

- PR URL + branch name (from webhook payload)
- Changed files (from GitHub API)

### Outputs

- PR comment with: ✅ / ❌ per check, coverage delta, link to full report
- Update `qa-automation-on-pr/outbox/{pr_number}.md`

## Run procedure

1. Receive webhook payload.
2. Identify changed files.
3. Run targeted checks:
   - Lint on changed files only
   - Unit tests touching changed files
   - Coverage delta on changed lines
4. Post comment to PR.
5. Write outbox file.

## Threshold rules

| Metric | Condition | Severity |
|--------|-----------|----------|
| Any test failure | — | **HIGH** (block merge) |
| Coverage delta < -2% | — | **MEDIUM** |
| Lint error | — | **MEDIUM** (block merge) |
| Build failure | — | **HIGH** (block merge) |

## GitHub integration

- Webhook URL: needs to be configured per repo (Ivan + Kiki action)
- Auth: GitHub PAT from BWS (Kiki has one)
- Trigger repos: Ai-Whisperers/aiw-org, Ai-Whisperers/coach-agents, Ai-Whisperers/growth-coaching

## Suggested trigger

`webhook` (GitHub PR events) — alias: `aiw-qa-on-pr`.

## Hard stops

- DO NOT auto-merge PRs (Kiki approves).
- DO NOT post comments without Kiki's GitHub PAT.
- DO NOT run heavy integration tests on PR — that's qa-automation-runner's job (daily).
- DO NOT skip security checks (security-watchdog owns).

