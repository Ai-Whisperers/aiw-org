# Layer 1 — Operational Hygiene — Operator Runbook

> **Purpose**: Step-by-step guide for Ivan to execute the operator-action
> parts of Layer 1. AI handles everything else (Doctrine 1: AI self-fixes).
>
> **Audience**: Ivan only. No technical knowledge assumed beyond "click around
> web consoles and confirm."
>
> **Time estimate**: 2-3h total operator time (broken into chunks below)
> **Sequencing**: Can be done in any order EXCEPT the 5 P0 leaks should be done together as one batch.

---

## Pre-flight: what to have ready

Before starting, gather these on a notepad:

| Item | Where to find |
|------|---------------|
| Browser with logged-in sessions to Supabase, GitHub, Cloudflare | Your normal setup |
| Supabase project URL | `state/funding.json` references AIW projects; ask AI to print current value |
| GitHub PAT to revoke | Look in `state/security-watchdog-30min/outbox/2026-08-31.md` for the canonical names (already known: `ghp_u0Cs76…`, `ghp_Rfi9…`) |
| LiteLLM account login | (your own — billing dashboard) |
| 15-20 minutes of uninterrupted time | Block it on your calendar |

---

## Batch A — P0 Secret Leaks (75 minutes)

These are security blockers. **Do them in one sitting.** Even if you can only
do 1 or 2, that's progress — note which you did in the verification log below.

### Step A1 — Rotate Supabase service-role key (5 min)

1. Go to https://supabase.com/dashboard
2. Select the AIW project (find it via `state/funding.json:key_metrics.projects` — ask AI for current value if unsure)
3. Go to Settings → API
4. Find "service_role" key (NOT anon key)
5. Click "Roll" or "Generate new" — copy new value to a password manager
6. **Action for AI**: Tell AI "Supabase service-role key rotated, new value in Bitwarden". AI will update BWS secret.

**Verification (you do this)**:
- [ ] New key in Bitwarden under `SUPABASE_SECRET_KEY` (or whatever the canonical name is — ask AI)
- [ ] AI confirmed BWS write
- [ ] AI confirmed old key removed

### Step A2 — Revoke `ghp_u0Cs76…` PAT (1 min)

1. Go to https://github.com/settings/tokens
2. Find token starting with `ghp_u0Cs76`
3. Click "Delete" → confirm
4. **Check the scope it had**: was it `agent-infra`? `agent-scratch`? Note in verification log.

### Step A3 — Revoke `ghp_Rfi9…` PAT (1 min)

Same as A2 but for `ghp_Rfi9…` token.

### Step A4 — `saskia-personal-context` repo → private (5 min)

1. Go to https://github.com/Ai-Whisperers/saskia-personal-context
2. Settings → Danger Zone → "Change repository visibility"
3. Select "Make private" → confirm
4. Verify: repo is no longer visible to non-collaborators

**Verification**:
- [ ] `gh repo view Ai-Whisperers/saskia-personal-context --json visibility` shows `"visibility": "PRIVATE"`

### Step A5 — Replace 16 R2 presigned URLs in `worker.js` (2 hours)

**This is Kiki's task per the wishlist.** Ivan, do this yourself only if Kiki
is unreachable for >1 week. Otherwise: handoff + skip in this layer.

1. Go to https://dash.cloudflare.com → R2 → Manage R2 API Tokens
2. Generate new presigned URL with appropriate scope
3. Edit `/opt/data/agents-v2/rubicon-eas-website/worker.js` (or wherever it lives — ask AI for path)
4. Replace all 16 URLs
5. Deploy the worker (Cloudflare dashboard → Workers → your-worker → Deploy)
6. Verify: hit the URL, check response is valid

**Verification**:
- [ ] AI confirms no `?token=` patterns remain in the file
- [ ] Worker deploys successfully
- [ ] Worker responds 200 to a test request

---

### Verification log (Batch A)

After Batch A, copy-paste this into chat for AI to verify:

```
P0 Leak Remediation Status:
- A1 Supabase rotate:    [DONE/SKIP] — value in Bitwarden at <name>
- A2 ghp_u0Cs76 revoke:  [DONE/SKIP]
- A3 ghp_Rfi9 revoke:    [DONE/SKIP]
- A4 saskia private:      [DONE/SKIP]
- A5 R2 URLs replaced:    [DONE/SKIP/KIKI]
```

AI will then run verification scripts + update `analysis/REMAINING-TASKS-AND-WISHLIST.md`.

---

## Batch B — LiteLLM credit topup (5 minutes)

1. Go to https://litellm.ai/ (or whatever billing portal you use)
2. Top up credits — add $50-100 to cover Cerebras + Mistral subscriptions
3. Verify: billing page shows new balance
4. **Action for AI**: Tell AI "LiteLLM topped up". AI will restart the failed cron jobs and verify no HTTP 402 errors in the next 24h.

**Verification**:
- [ ] LiteLLM dashboard shows new credit balance
- [ ] AI confirms 0 HTTP 402 errors in next 24h
- [ ] Cron jobs unblock

---

## Batch C — Wrangler restart decision (5 min chat + 30 min AI work)

This is the most decision-heavy part. **Don't skip the chat.**

### Step C1 — Decide on rubicon-eas

Look at `state/sales.json:open_questions` and answer:

> **Question**: Should `rubicon-eas` Worker be resurrected or permanently archived?

| Option | Implication | Your choice |
|--------|-------------|-------------|
| **(a) Resurrect** | Restart wrangler; revive Worker; restore WEBHOOK_URL secret | AI does this (Task 1.6a) |
| **(b) Permanent archive** | Stop trying; remove from cron; archive code | AI does this (Task 1.6b) |

**Tell AI your decision** + any context. AI executes accordingly.

### Step C2 — If resurrecting (Task 1.6a)

AI will:
1. Find wrangler.toml + worker config
2. Re-deploy to Cloudflare
3. Restore `WEBHOOK_URL` secret (you'll need to provide the value or have AI look in Cloudflare)
4. Smoke-test with curl

### Step C3 — If archiving (Task 1.6b)

AI will:
1. Stop any running wrangler processes
2. Move worker code to `/opt/data/archive/`
3. Remove from any cron jobs
4. Update `state/sales.json` to reflect the archive decision
5. Update `analysis/REMAINING-TASKS-AND-WISHLIST.md`

---

## Batch D — AI handles everything else (no operator action)

You don't do anything for these — AI does them per Doctrine 1:

| Task | What AI does | Time |
|------|-------------|------|
| 1.2 | Fix `validator_e164_regression` regex | 30 min |
| 1.3 | Fix `validator_area_case_inversion` | 15 min |
| 1.4 | Pin `mcp<2` to fix parking-storm | 30 min |
| 1.7 | Capture baseline metrics | 60 min |
| 1.8 | Update wishlist | 15 min |
| 1.9 | Write completion report | 30 min |
| 1.10 | Run smoke gate | 30 min |

AI will commit these as they complete. You'll get a notification when each
lands. **No action required from you except "looks good" or "fix this" on
each commit.**

---

## Verification: how to know Layer 1 is done

You'll get a "Layer 1 complete" message from AI when:

1. All 10 tasks are committed
2. Smoke gate (Task 1.10) passes
3. Completion report is at `analysis/LAYER-1-HYGIENE-COMPLETION-REPORT.md`
4. AI tells you the commit hash + summary

**Your review** (~15 min):
1. Read the completion report
2. Spot-check 2-3 commits
3. Say "Layer 2 go" or "hold on, fix X first"

---

## What to do if something goes wrong

| Symptom | What it means | What to do |
|---------|---------------|------------|
| AI asks a question in chat | AI hit Doctrine 5 big-decision boundary | Answer briefly; AI continues |
| AI commits something you didn't expect | AI self-fix went sideways | `git revert <commit>`; tell AI what went wrong |
| Smoke gate fails | A fix broke something else | AI investigates; may pause |
| Cron jobs still error after Layer 1 | Upstream issue (not AIW) | AI documents; Layer 4 carry-forward |
| New P0 leak emerges during Layer 1 | Layer 1 expands | AI pauses; new scope doc |

---

## Time budget for Ivan

| Batch | Time | When |
|-------|------|------|
| Pre-flight | 10 min | Now |
| Batch A (P0 leaks) | 75 min | Single sitting when you have 90 min uninterrupted |
| Batch B (LiteLLM) | 5 min | Same sitting as A, or anytime |
| Batch C decision | 5 min | Anytime, just answer the question |
| Layer 1 review | 15 min | After AI's "Layer 1 complete" message |
| **TOTAL** | **~110 min (1h50m)** | Spread over 1-2 days |

Plus: ~30 min of check-ins during AI's autonomous work (Tasks 1.2-1.4, 1.7-1.10)
where AI may pause to surface a small decision.

---

## Rollback: if you need to abandon Layer 1 mid-execution

If something goes catastrophically wrong (e.g. a P0 leak fix triggers a
cascading failure), and you want to abort:

```bash
# Revert all Layer 1 commits
git log --oneline | grep "Layer 1" | head -20  #  identify commits
git revert <commit-hash-1> <commit-hash-2> ...
git push origin master
```

Then: tell AI "Layer 1 aborted, reverted to <commit>". AI writes a Layer 1
abort report + we discuss next steps.

**AI never reverts without your explicit instruction** — Doctrine 5 says
big decisions (like "abandon this layer") are yours.

---

## After Layer 1

Once you say "Layer 2 go":
- AI starts Layer 2 scope doc (`LAYER-2-FOUNDATION-SCOPE.md`)
- AI works on cleanup + structural foundation
- Light review cadence: ~1-2h/week from you
- Same reporting: granular commits + weekly summary + layer-end report

---

**Questions while executing**: just ask. Per Doctrine 5, AI pauses for big
decisions. Per Doctrine 1, AI handles small ones.

**Next**: greenlight Layer 1 → AI starts with Batch D autonomous tasks in
parallel with you doing Batch A operator actions.