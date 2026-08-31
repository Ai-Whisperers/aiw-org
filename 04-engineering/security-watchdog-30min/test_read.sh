#!/bin/bash
set -e
cd /opt/data/agents/security-watchdog-30min
DATE=$(date +%Y-%m-%d)
OUTBOX=/opt/data/agents/security-watchdog-30min/outbox/$DATE.md
mkdir -p /opt/data/agents/security-watchdog-30min/outbox
# Just try to read the file and see if we can
cat /opt/data/.env