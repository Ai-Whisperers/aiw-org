# AIW Org Analysis (Erebus audit, 2026-08-31)

This directory contains the canonical analysis files produced by the
2026-08-28 Erebus audit session. They're here for GitHub discoverability
and to provide a single landing page for the org's department/agent/role
catalog.

## Reading order

1. **[DEPT-AGENTS-ROLES-COMPLETE.md](DEPT-AGENTS-ROLES-COMPLETE.md)** — start here.
   All 31 functional areas (6 Tier-1 active core + 8 Tier-2 cross-cutting
   + 17 Tier-3 deferred + 5 Tier-4 enterprise). Every role table, every
   sub-agent with its portmanteau name, every promotion trigger.

2. **[AGENT-NAMES-V2.md](AGENT-NAMES-V2.md)** — the portmanteau naming
   framework. 54 agents renamed following [Domain Root] + [Personal Suffix].
   Includes mapping table from portmanteau → formal name.

3. **[AGENT-NAMES-V2.json](AGENT-NAMES-V2.json)** — machine-readable version
   of the same mapping.

## What's NOT here

The *source of truth* lives in `/opt/data/agents-v2/` (the canonical org
charters and playbooks) and `/opt/data/agents/` (the legacy agent-infra
repo with the 47-agent handoff matrix). This analysis/ directory is a
derivative — it pulls everything into one place for readability.

For the actual charters:
- `/opt/data/agents-v2/constitution/01-operations.md` … `06-people-culture.md`
- `/opt/data/agents-v2/playbooks/07-cross-cutting-concerns.md`
- `/opt/data/agents-v2/playbooks/08-deferred-tier3.md`

## Updates

Files are regenerated from the canonical sources by Erebus (this directory
is the canonical copy pushed to GitHub). When charters change, regenerate
the analysis files and update this directory.
