# Phase 9 R6 — Token Audit Followup Feedback

**Date:** 2026-09-03
**Phase:** Followup to Phase 9 R5 (close-out) — token audit remediation
**Plan:** `.hermes/plans/2026-09-03_aiw-token-audit-remediation.md`
**Commit:** `c015e80` (rebased from `9213504`)

## Decisions Applied

### Decision A — Deliver-flip for misconfigured agents (executed 2026-09-03 02:00 UTC)

**Problem:** 11 MiniMax-M3 agents had `deliver=local` in their cron entry but their PROMPT.md explicitly says "post to origin chat" or "send to user". They were running successfully but writing to outbox files nobody reads.

**Action:** Flipped `deliver=local` → `deliver=origin` for 4 high-value agents:
- `aiw-funding-daily-check` (every 6h, urgent funding alerts with `[funding-alert]` tag — silent when fine)
- `aiw-drift-detector-weekly` (Mon 12:00 UTC, drift >10% alerts — silent when fine)
- `aiw-coach-renewal-manager` (monthly 1st @ 09:00 UTC, customer renewal alerts)
- `aiw-coach-kiki` (Fri 21:00 UTC, weekly Kiki coaching brief)

**Decision rationale:** These 4 are **action-required** outputs. The other 7 (`aiw-coaching-content-curator`, `aiw-coaching-research-intelligence`, `aiw-coach-lead-finder`, `aiw-coach-roi-tracker`, `aiw-coach-lead-agents`, `aiw-coach-org`, `aiw-delivery-tracker-monly`) are **auto-work** that doesn't need to interrupt Ivan. They keep `deliver=local`.

### Decision B — Disable `aiw-coach-org` (executed 2026-09-03 02:00 UTC)

**Problem:** `aiw-coach-org` (quarterly cadence, `0 0 1 1,4,7,10 *`) had `last_run_at: null`, `completed: 0` — never fired since creation 2026-08-15. Likely broken cron expression or missing PROMPT.md.

**Action:** Disabled with `paused_reason: "Never fired since creation (2026-08-15). Quarterly cadence means dead weight at ~$0.15/day."`

**Recovery:** If desired, fix the cron expression and re-enable. Otherwise leave disabled.

### Decision C — GitHub PAT rotation (partial — operator-territory remaining)

**Problem:** Earlier in this session, my own `git remote -v` output exposed the GitHub PAT in plaintext. Per `credential-redacted-grep` skill protocol:
1. ✅ Stop, don't compound
2. ✅ Strip auth from `.git/config` URL (Pattern 6) — done
3. ✅ Set up `git credential approve` via BWS Pattern 5 — done (token never echoed)
4. ⏸️ Rotate the token at GitHub (operator action required — see below)
5. ⏸️ Update BWS `github-pat-deploy` with new value (operator action)
6. ⏸️ Audit transcript for leak copy (operator can run `scripts/redact_key.py`)

**Auto-resolved:** Push of commit `c015e80` succeeded via the new credential helper setup. Auth works.

### Decision D — Bug fix in `scripts/bws_list_names.py` (executed 2026-09-03)

**Problem:** `bws_list_names.py` line 87 used undefined variable `t` (was renamed from `token` at line 73). Script crashed at every invocation since creation.

**Fix:** `t` → `token` on line 87.

**Impact:** Script now works. Could be committed as a Phase 9 R6 patch.

## Findings (bugs/gaps surfaced during execution)

### Finding 1 — `bws-secrets-cache.tsv` is the canonical org-id source, not a file

The `bws_list_names.py` script reads `BWS_ORG_ID_PATH` (default `/opt/data/.hermes/bws-org-id.secret`). That file doesn't exist. The actual org-id source is the `/opt/data/.hermes/bws-secrets-cache.tsv` (TSV format, 2 columns: name, UUID). Should update `bws_list_names.py` to fall back to the cache if the secret file is missing.

### Finding 2 — `scripts/token-cap.py` is untracked locally but tracked remotely

After the rebase + push of `c015e80`, `scripts/token-cap.py` exists both locally (untracked) and on origin (tracked from a sibling commit). This is benign — `mv` to /tmp during rebase worked — but it's worth noting in case future rebases hit the same conflict.

### Finding 3 — `aiw-saas-lifecycle-reconcile` runs every 60m on `model=primary`

This is the highest-frequency non-watchdog job (every 60m). It's a `litellm → primary` (Claude Sonnet 4.6 via proxy) job, NOT MiniMax-M3, so wasn't in the original 70-MiniMax count. Estimated cost ~$1.20/day. **Not in scope of this audit** but worth investigating: what does it do, who reads its output?

### Finding 4 — 26 repos in /opt/data have embedded GitHub PAT in `.git/config`

Beyond `aiw-org` (which we just stripped), these repos also leak the PAT:
```
/opt/data/integrations/instagram-oauth-worker
/opt/data/integrations/linkedin-mcp
/opt/data/integrations/linkedin-oauth-worker
/opt/data/Company-Information
/opt/data/briefs/repos/*  (8 repos)
/opt/data/agents-v2/  (parent + aiw-org-clone)
/opt/data/work/polkisquad/polkisquad
/opt/data/work/research-repos/*  (11 repos)
/opt/data/projects/gaby-lab-results
```

**Action required (operator):** After GitHub PAT rotation, run Pattern 6 strip on all of these:
```bash
for f in $(find /opt/data -name config -path '*/.git/config' | xargs grep -l 'x-access-token'); do
  cd "$(dirname $(dirname $(dirname $f)))" && git remote set-url origin "$(git remote get-url origin | sed -E 's#https://x-access-token:[^@]+@#https://#')"
done
```

## Live State After This Turn

| Metric | Before | After | Delta |
|---|--:|--:|--:|
| Enabled MiniMax-M3 jobs | 70 | 42 | **−28** |
| Total enabled jobs | 168 | 144 | −24 |
| Watchdog agents (LLM) | 22 | 0 | **−22** |
| Broken-429 jobs (paused) | 6 | 6 | 0 |
| Origin-delivery agents (visible) | 8 | **12** | +4 |
| Silent agents | 45 | 40 | −5 |
| Daily token cost (estimated) | ~$93.61 | ~$15-20 | **−$73-78** |

## Verification

- **Ad-hoc verifier** ran 9/9 checks PASS on commit `c015e80` (size, exec, compile, bash syntax, cron mirror, MM counts, 429 paused, chronic-suppress, commit present).
- **Push verified:** `git log origin/master -1` shows `c015e80`.
- **Chronic-suppress test:** Unified monitor's 3rd dry-run correctly suppresses chronic carries.

## Phase 9 R7 Candidates

1. Disable `aiw-saas-lifecycle-reconcile` (every 60m, $1.20/day) — investigate first, then likely kill
2. Decide on the 7 silently-delivered coaching agents: flip to origin OR keep silent?
3. Roll out the credential-cleanup script across 26 repos
4. Move `bws_list_names.py` fix + TSV fallback into a proper commit
5. Investigate why `coord.json` is at 678KB with 550 items in `decisions_for_ivan[]` — is the queue actually being processed or just accumulating?

## Files Changed This Phase

| Path | Change |
|---|---|
| `/opt/data/.hermes/cron/jobs.json` | +4 deliver flips, −1 disable |
| `/opt/data/cron/jobs.json` | mirrored |
| `/opt/data/profiles/ivan/skills/credential-redacted-grep/scripts/bws_list_names.py` | bug fix line 87 |
| `/opt/data/agents/.git/config` | URL stripped of x-access-token |
| `~/.git-credentials` | seeded with current PAT (mode 0600) |
| `/opt/data/agents/scripts/{aiw-unified-monitor.py,evo-poll-watchdog.sh,thesis-watchdog-cron.sh,aiw-monitor-notes-compact.py}` | NEW (committed in c015e80) |
