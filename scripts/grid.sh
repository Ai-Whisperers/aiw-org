#!/usr/bin/env bash
# grid.sh — visualize the weekly agent schedule grid
# Usage: bash /opt/data/agents/scripts/grid.sh
# Shows what runs at each hour, to verify no collisions

set -uo pipefail

# All known cron jobs (hard-coded — when adding a job, add it here too)
cat <<'EOF'
Weekly Agent Schedule (PYT = UTC-4 winter, UTC-3 summer)

     Mon        Tue        Wed        Thu        Fri        Sat        Sun
───── ────────── ────────── ────────── ────────── ────────── ────────── ──────────
06:00 morning    morning    morning    morning    morning    morning    morning
06:30 analyst    analyst    analyst    analyst    analyst    analyst    analyst
09:00 sales      sales      sales      sales      sales      sales      sales
11:00 ci-monitor ─          ─          ci-monitor ─          ─          ─
12:00 rbl-check  rbl-check  rbl-check  rbl-check  rbl-check  rbl-check  rbl-check
12:00 sales      sales      sales      sales      sales      sales      sales
17:00 coord      eng        ─          coord      eng+kiki   ─          ─
18:00 ─          ─          ─          ─          finance    ─          research
23:00 ─          ─          ─          ─          ─          ─          thesis-maint

Watchdogs (silent unless firing, every X minutes):
  site-health        every 15m
  thesis-watchdog    every 15m
  evo-poll-watchdog  every 5m
  health.sh          every 5m

Notes:
  - "morning" = morning-brief cron
  - "analyst" = business-analyst cron (06:30 PYT daily)
  - "sales" = sales-pipeline cron (09:00 + 12:00 PYT daily)
  - "ci-monitor" = repo-ci-monitor (11:00 UTC = 07:00 PYT winter)
  - "rbl-check" = 12:00 UTC = 08:00 PYT winter
  - "coord" = management-coordinator (Mon+Thu 17:00 PYT)
  - "eng" = engineering-roster (Tue+Fri 17:00 PYT)
  - "kiki" = kiki-coach (Fri 17:00 PYT)
  - "finance" = finance-controller (Fri 18:00 PYT)
  - "research" = research-tracker (Sun 18:00 PYT)
  - "thesis-maint" = thesis-git-maintenance (Sun 23:00 UTC = 19:00 PYT winter)

Times shown in PYT. UTC schedules differ by ±1h (PYT = UTC-4 winter, UTC-3 summer).
Verify by running: hermes cron list
EOF