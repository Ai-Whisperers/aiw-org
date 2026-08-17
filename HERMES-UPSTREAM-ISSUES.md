# Hermes upstream issues found — 2026-08-13

> Two issues confirmed while debugging a cron outage at Ai-Whisperers Paraguay.
> Both are **already tracked upstream**. AIW is on Hermes 0.20.0, which predates
> the user-facing fix in PR #73532 (merged 2026-07-28).
>
> **Status as of 2026-08-13**:
> - Issue A (silent no-op) → tracked in upstream **#70050** (master) and **#85215** (duplicate). Fixed in main by PR #73532 but not in 0.20.0.
> - Issue B (cron-store path drift) → independent of A. No dedicated upstream issue exists yet. AIW comment on #70050 documents this; suggested filing a new issue if maintainers agree.

---

## Issue A: `hermes cron edit --provider/--model` is a silent no-op

**Severity**: High — causes prod cron failures that look like LLM errors.

**Tracked upstream**: #68380 (closed as fixed in main by PR #73532), #70050 (master issue), #85215 (duplicate report).

**Repro** (Hermes **0.20.0**; predates the fix):

```
$ hermes cron edit --provider custom:litellm --model primary 31e08c310e01
$ # exits 0, prints "Updated job", nothing else
$ cat /opt/data/.hermes/cron/jobs.json | jq '.jobs[] | select(.id=="31e08c310e01") | {provider, model}'
{
  "provider": null,   # ← still null!
  "model": null       # ← still null!
}
```

**What happens under the hood** (traced via `cronjob(action="update")`):

1. CLI calls `_cron_api(action="update")` with `{"id": "...", "provider": "custom:litellm", "model": "primary"}`.
2. CLI trusts gateway's success response (`rc=0`).
3. CLI does **not** re-read the stored value to confirm persistence.
4. Internally: `update_job()` → `_normalized_inference_axes()` → `inference_fields_changed` flow snapshots provider/model. But the stored provider/model fields themselves only update if they were explicitly part of the normalized write — and `--provider/--model` flags don't pass through the same code path as `cronjob(action="update")`'s `kwargs` payload.

**Visible symptom**: gateway keeps using old provider/model. Cron jobs error with the wrong model name.

**Workaround** (in use at AIW since 2026-08-13): direct JSON edit to `/opt/data/cron/jobs.json` (the gateway-readable store). Documented in `ORG-AGENTS.md`.

**Suggested fix**:
1. After successful `_cron_api(action="update")`, CLI should re-read the stored job and confirm the requested field actually changed. If not, raise.
2. OR: refuse to use the success response as proof of persistence; require a follow-up read.

---

## Issue B: Cron store path inconsistency

**Severity**: Medium — causes silent drift between user-facing canonical store and gateway-readable store.

**Tracked upstream**: not yet. AIW commented on #70050 with full repro + workaround. Suggested filing a dedicated issue if maintainers confirm the layout-drift is independent of #68380.

**Repro** (with `HERMES_HOME=/opt/data`):

- `get_hermes_home()` returns `/opt/data` → `JOBS_FILE = /opt/data/cron/jobs.json` (`/opt/hermes/cron/jobs.py` line 87).
- But `get_hermes_home()`'s docstring says it follows "context-local override → HERMES_HOME → platform default", and many other Hermes code paths compute `JOBS_FILE = HERMES_HOME / ".hermes" / "cron" / "jobs.json"`.
- Result: depending on which path the writer uses, edits land in either `/opt/data/cron/jobs.json` (read by gateway ticker) or `/opt/data/.hermes/cron/jobs.json` (the "canonical" name from the docstring).
- Both files coexist; the user-visible `hermes cron list` reads whichever the ticker last wrote, but `hermes cron edit` writes to a path that may be ignored.

**Workaround**: see `/opt/data/scripts/cron-sync.sh` (cron job runs every 5m; syncs the two stores).

**Suggested fix**:
1. Make `JOBS_FILE` resolution a single helper (already exists in `hermes_constants.py`), used everywhere.
2. Add a unit test that asserts `hermes cron edit --provider=X` actually changes the value the gateway ticker reads.
3. Document the canonical path in `cron/jobs.py`'s module docstring (currently inconsistent with the constant).

---

## How to file these upstream

1. ✅ Issue A: posted corroborating comment on **#70050** (master issue, https://github.com/NousResearch/hermes-agent/issues/70050#issuecomment-5286031145) and **#85215** (duplicate, https://github.com/NousResearch/hermes-agent/issues/85215#issuecomment-5286032627). Both comments link to AIW's working workaround and offer to upstream the scripts.
2. ⏳ Issue B: described in same #70050 comment, with suggestion to file a dedicated issue if maintainers confirm it's independent of #68380.
3. Reference issue numbers in AIW's `/opt/data/agents/GAP-AUDIT-2026-08-13.md` so future agents find them.

## AIW-side mitigations (in place)

| Issue | Mitigation | File |
|-------|-----------|------|
| A (silent no-op) | Direct JSON edit via `cron-sync.sh` | `/opt/data/scripts/cron-sync.sh` |
| A (silent no-op) | Pre-commit hook blocks commits while drift exists | `/opt/data/agents/scripts/pre-commit-cron-guard.sh` |
| B (path inconsistency) | Both files maintained by cron-sync | `/opt/data/scripts/cron-sync.sh` |
| B (path inconsistency) | Cron-heartbeat watchdog alerts on drift | `/opt/data/scripts/cron-heartbeat-check.sh` |