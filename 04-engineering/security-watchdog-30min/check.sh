#!/bin/bash
set -e
cd /opt/data/agents/security-watchdog-30min
DATE=$(date +%Y-%m-%d)
OUTBOX=/opt/data/agents/security-watchdog-30min/outbox/$DATE.md
mkdir -p /opt/data/agents/security-watchdog-30min/outbox
# Count lines that look like KEY=value (value not empty and not just spaces)
CRED_COUNT=$(grep -E '^[A-Z_]+=[^[:space:]]' /opt/data/.env | grep -v '=$' | wc -l)
FAILED_LOGINS=$(grep -E 'Failed password|authentication failure' /var/log/auth.log 2>/dev/null | tail -n 100 | wc -l)
if [ $CRED_COUNT -gt 0 ]; then
    SEVERITY="high"
    EVIDENCE="Exposed credentials detected in /opt/data/.env. Found $CRED_COUNT potential credentials exposed."
elif [ $FAILED_LOGINS -gt 0 ]; then
    SEVERITY="medium"
    EVIDENCE="$FAILED_LOGINS failed login attempts detected in auth.log."
else
    SEVERITY=""
    EVIDENCE=""
fi
if [ -n "$SEVERITY" ]; then
    printf 'ALERT: %s\n\n%s\n\nAction: Alert Kiki to rotate these credentials. No auto-remediation performed.' "$SEVERITY" "$EVIDENCE" > $OUTBOX
    cat $OUTBOX
else
    if [ -f $OUTBOX ]; then
        rm $OUTBOX
    fi
    printf '[SILENT]'
fi
