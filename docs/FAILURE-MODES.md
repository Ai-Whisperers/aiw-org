# Failure Modes Catalog

> Catalog of expected failures + responses. Phase 9 chaos test input.
> **Last updated**: 2026-08-14

---

## Reading guide

Each failure mode has:
- **What happens**: the visible symptom
- **Root cause**: why
- **Detection**: how we know
- **Response**: what the system does
- **Recovery**: how to restore

---

# Tier 1: Infrastructure failures

## F-1: Cron job in error state

**What happens**: A cron job's `last_status` becomes `error`. No agent runs on schedule.

**Root cause** (common):
- Model drift (provider/model changed since job created)
- Tool unavailability (gh API down, Proveedor de IA rate limit)
- State file corruption
- Network partition

**Detection**:
- `cron-heartbeat.sh` (every 15 min off-hours, 30 min on-hours)
- `health.sh` (every 15 min)
- `validate-state.py` (every 15 min)

**Response**:
1. Heartbeat posts alert to origin chat with job name + error
2. If error > 24h, escalates to Ivan
3. Job remains in error state until manual fix

**Recovery**:
1. Check `hermes cron list` for the job
2. Inspect error message
3. Common fix: delete `provider_snapshot` + `model_snapshot` from jobs.json
4. Re-pin to current model
5. Manual run to verify

---

## F-2: State file corruption

**What happens**: JSON or SQLite state file is invalid. Agent reads fail. Brief not delivered.

**Root cause**:
- Concurrent write (two agents write to same file)
- Disk corruption
- Agent bug (writes malformed JSON)

**Detection**:
- `validate-state.py` (every 15 min, schema check)
- Agent runtime exception during read

**Response**:
1. Validate-state alerts on schema violation
2. Agent falls back to last good state (from snapshot)
3. If snapshot also corrupted: agent halts + alert

**Recovery**:
1. Restore from snapshot: `cp state/snapshots/{date}/{file} state/`
2. Or restore from DB snapshot: `sqlite3 .restore`
3. Validate restored file
4. Resume agent

---

## F-3: LLM provider down

**What happens**: Agent starts but LLM call fails with 5xx.

**Root cause**:
- Provider outage (Proveedor de IA, Proveedor de IA, local model)
- Rate limit exceeded
- Network partition

**Detection**:
- Agent runtime catches exception
- Agent logs `llm_unavailable` event
- Falls back to secondary model

**Response**:
1. Retry primary with exponential backoff (3 attempts)
2. Fall back to `litellm/primary`
3. If both fail: exit + alert (no silent halt)
4. Cron-heartbeat detects missed run, alerts

**Recovery**:
- Provider comes back online
- Next scheduled run succeeds
- No manual intervention needed unless outage > 1 hour

---

## F-4: Network partition (Hermes to external services)

**What happens**: Agent can't reach GH API, Evolution API, CF Workers, etc.

**Root cause**:
- Internet outage
- VPN down
- Cloudflare outage

**Detection**:
- Tool call timeout
- Agent logs `tool_unavailable: <name>`

**Response**:
1. Skip tool call, log to degraded-mode
2. Agent delivers brief with `data_source: stale` flag
3. Next run after network recovery works normally

**Recovery**:
- Network restored
- Next scheduled run succeeds
- No manual intervention needed

---

## F-5: Hard stop triggered

**What happens**: Agent attempts action blocked by hard stop (e.g., `send_external_message`).

**Root cause**: Agent prompt invoked action not authorized for it.

**Detection**:
- `hard-stop-wrapper.py` blocks action, logs to `escalations` table

**Response**:
1. Action blocked
2. Logged to escalation log with context
3. Agent surfaces in next brief: "X action blocked"

**Recovery**:
- Review escalation log
- If action should be allowed: update hard_stops in PROMPT.md
- If action shouldn't be attempted: improve agent prompt to not request it

---

# Tier 2: Agent-level failures

## F-6: Agent produces garbage output

**What happens**: Agent delivers brief that's nonsense, off-topic, or factually wrong.

**Root cause**:
- LLM hallucination
- Bad input data
- Prompt corruption

**Detection**:
- Ivan reviews brief, flags it
- Eval gate (when shipped) catches obvious failures
- Heart-of-Stone pattern: self-critique score < threshold

**Response**:
1. Ivan flags: "this brief is bad"
2. Agent re-runs with override
3. Investigation: was it prompt? input? model?

**Recovery**:
- Update prompt if needed
- Update input filters
- Roll back model if regression

---

## F-7: Agent infinite loop

**What happens**: Agent run never completes. CPU pinned.

**Root cause**:
- Reflection loop has no max iterations
- Tool call returns confusing response
- LLM gets stuck in reasoning

**Detection**:
- Cron-heartbeat sees no completion
- Cost-cap.sh sees token burn
- Run timeout (default 30 min)

**Response**:
1. Run timeout kills agent
2. Cost-cap halts over-budget agent
3. State marked `failed`, idempotency key not updated
4. Next run is allowed (different run, fresh start)

**Recovery**:
- Manual investigation of agent logs
- Update prompt to bound reflection iterations
- Add explicit "if stuck, exit + escalate" instruction

---

## F-8: Idempotency window collision

**What happens**: Agent runs twice within idempotency window. Second run skipped.

**Root cause**:
- Cron fired twice (rare)
- Manual run + cron run in same window

**Detection**:
- Idempotency check returns DUPLICATE_SKIP
- Logged to state.idempotency table

**Response**:
- Agent exits gracefully with "duplicate_run" log
- Brief NOT delivered (avoids double-send)
- State NOT updated (preserves prior state)

**Recovery**:
- No action needed — this is the design
- If duplicate was unintentional: Ivan uses override_token

---

## F-9: Trademark violation in agent output

**What happens**: Agent output contains banned trademark (e.g., mentions Canal de comunicacion).

**Root cause**:
- Agent prompt has accidental mention
- Output went to customer-facing surface

**Detection**:
- `trademark-scrub.sh` on every artifact
- Pre-commit hook on git commits
- Manual review of customer-facing surfaces

**Response**:
1. Block commit / refuse publication
2. Alert: "trademark violation in <artifact>"
3. Ivan reviews + edits

**Recovery**:
- Edit artifact
- Add to prompt: "do not mention [banned brands]"
- Re-run scrub

---

# Tier 3: Org-level failures

## F-10: Ivan offline > 2 days

**What happens**: Briefs queue up, decisions blocked, agents stall on approvals.

**Root cause**: Ivan unreachable (travel, illness, etc.).

**Detection**:
- Decisions queue length grows
- Time-since-last-approval metric grows

**Response**:
- Agents continue delivering operational briefs (no approval needed)
- Decisions queue: surfaced for next Ivan check-in
- HITL_AGENT briefs accumulate but don't send externally
- AUTO_SEND limit: agents won't send to external without approval

**Recovery**:
- Ivan returns, clears decision queue
- HITL drafts reviewed, sent or discarded
- Org catches up within 1-2 cycles

---

## F-11: Multiple agents write to same state

**What happens**: Race condition. Last write wins, prior data lost.

**Root cause**: Two agents share state file/DB without coordination.

**Detection**:
- State snapshot diff shows rollback
- validate-state reports anomaly

**Response**:
- SQLite has built-in locking (WAL mode)
- JSON files: use `cp + mv` for atomic writes
- Cross-agent state: only via handoff matrix (per ORG-AGENTS.md)

**Recovery**:
- Restore from snapshot
- Fix the bug that caused concurrent writes
- Add lockfile if not present

---

## F-12: Cost cap breached

**What happens**: Agent's daily cost > cap.

**Root cause**:
- Reflection loop with too many iterations
- Runaway tool calls
- Large context windows

**Detection**:
- `cost-cap.sh` (hourly)
- Agent runtime cost tracking

**Response**:
1. Agent halted, alert posted
2. Daily cost resets at midnight PYT
3. Ivan reviews: legitimate use vs runaway

**Recovery**:
- If legitimate: temporarily raise cap via `cost-tracker.json` override
- If runaway: investigate + fix prompt
- If recurring: lower cap (signal that this agent isn't efficient)

---

# Tier 4: External failures

## F-13: GitHub API rate-limited

**What happens**: Agent calls `gh api` get 429.

**Root cause**: Too many calls in short window.

**Detection**:
- Tool call returns 429
- Agent logs `gh_rate_limited`

**Response**:
1. Skip GH-dependent sections
2. Brief delivered with `data_source: gh_unavailable` flag
3. Next run after rate-limit window succeeds

**Recovery**:
- Add caching layer (Qdrant for repo metadata)
- Reduce GH call frequency per run

---

## F-14: Cloudflare Worker down

**What happens**: Rubicon EAS lead form not capturing.

**Root cause**: CF Worker outage, DNS issue, etc.

**Detection**:
- `site-health` cron catches HTTP errors
- sales-pipeline sees zero new leads

**Response**:
- Alert: "Rubicon EAS Worker down"
- Fall back to manual form (if possible)
- Track incident in `engineering.json`

**Recovery**:
- CF Worker restored
- Backfill any leads captured via fallback
- Post-incident review

---

## F-15: Billing dispute / chargeback

**What happens**: Client disputes a charge. Pasarela de pagos (banned vendor — using OSS alternative) flags it.

**Root cause**: Service quality issue, miscommunication, fraud.

**Detection**:
- finance-controller sees chargeback in billing feed
- Or: client emails directly

**Response**:
1. Pause service for client (HITL)
2. Investigate, respond within 48h
3. Refund if justified (requires Ivan approval)
4. Log to `compliance_flags`

**Recovery**:
- Resolve with client
- Update service to prevent recurrence
- Update SOP if gap

---

# Chaos test scenarios (Phase 9B)

These are the 3 scenarios we test:

## CT-1: Kill LLM mid-run
1. Start a long agent run
2. At T+30s, block all outbound to LLM provider
3. Verify: agent retries 3x with backoff, then exits + alert
4. Verify: state NOT updated (clean for next run)
5. Verify: cron-heartbeat flags the failed run

## CT-2: Corrupt state mid-run
1. Start an agent run
2. At T+15s, replace state file with garbage
3. Verify: agent detects corruption, exits gracefully
4. Verify: snapshot is intact, restore possible
5. Verify: next run after restore succeeds

## CT-3: Malformed tool response
1. Mock GH API to return malformed JSON
2. Start management-coordinator
3. Verify: agent logs tool error, skips GH-dependent section
4. Verify: brief delivered with `data_source: stale` flag
5. Verify: no infinite loop, no crash

---

**Document path**: `/opt/data/agents-v2/FAILURE-MODES.md`
**Version**: 0.1.0
**Last updated**: 2026-08-14
