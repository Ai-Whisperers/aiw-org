# HERMES-UPGRADE-CHANGELOG.md (pointer)

> ⚠️ **This file is a pointer.** The canonical 10-day upgrade story is in
> `/opt/data/agents-v2/MASTER-UPGRADE-CHANGELOG.md` and mirrored to
> https://github.com/Ai-Whisperers/agents-v2/blob/master/MASTER-UPGRADE-CHANGELOG.md

---

## Why this pointer exists

The `/opt/data/agents/` repo contains 4 standalone upgrade reports (Tier 1, Tier 3, Tier 4, MCP)
all dated 2026-08-13. Those reports describe the **starting state** but are now 10 days stale:
- Cron jobs: 17 → **83**
- Agents: 3 PROMPT.md → **49**
- Profiles: 6 → **9**
- MCPs enabled: 14 → **25**
- 12-factor audit: n/a → **9.0/10 avg**
- Eval-gate: n/a → **86.6% pass rate**

The full timeline (Tier 1 → PHASE-24 → current state) lives in
`/opt/data/agents-v2/MASTER-UPGRADE-CHANGELOG.md`.

---

## The 4 original upgrade reports (now historical)

These describe what was done on 2026-08-13. They are **frozen** as historical artifacts.
Do not edit them — they are accurate snapshots of that day's work.

| File | Date | Status | Covers |
|------|------|--------|--------|
| [UPGRADE-REPORT.md](./UPGRADE-REPORT.md) | 2026-08-13 | ✓ historical | Tier 1: 5 critical fixes (blocklist, cron model drift, memory config) |
| [TIER3-UPGRADE-REPORT.md](./TIER3-UPGRADE-REPORT.md) | 2026-08-13 | ✓ historical | Tier 3: per-profile toolsets, source materials, dashboards |
| [TIER4-UPGRADE-REPORT.md](./TIER4-UPGRADE-REPORT.md) | 2026-08-13 | ✓ historical | Tier 4: dept-agent wiring, HTTP server, state files, 7-day history |
| [MCP-UPGRADE-REPORT.md](./MCP-UPGRADE-REPORT.md) | 2026-08-13 | ⚠️ stale | MCP servers (was 14, now 25 enabled / 41 registered) |

---

## Current state (TL;DR from MASTER-UPGRADE-CHANGELOG)

As of 2026-08-23 20:00 UTC:

| Surface | Value |
|---------|-------|
| Cron jobs | 83 (6 OK, rest pending/agent) |
| Total agents | 49 (with PROMPT.md) |
| Profiles | 9 (added `ivan`, `kiki`) |
| MCPs enabled | 25 (of 41 registered) |
| Total skills | 298 |
| Phase reports | 24 (PHASE-0 through PHASE-24) |
| 12-factor audit | 9.0/10 avg, 0 HIGH, 0 FAIL |
| Eval-gate | 86.6% pass rate (17/17 PASS on 2026-08-17) |
| Active dashboards | 7 (org + 6 dept) |
| LLM cost | ~$293/mo monitored |

**For everything else, read `MASTER-UPGRADE-CHANGELOG.md`.**

---

Last updated: 2026-08-23 by Erebus (autonomous, on Iván's request to consolidate the upgrade history).
