#!/bin/bash
set -e
cd /opt/data/agents/security-watchdog-30min
DATE=$(date +%Y-%m-%d)
OUTBOX=/opt/data/agents/security-watchdog-30min/outbox/$DATE.md
mkdir -p /opt/data/agents/security-watchdog-30min/outbox
# Count API keys and tokens that look like secrets
CRED_COUNT=$(cat /opt/data/.env 2>/dev/null | grep -E '^[A-Z_]+=(sk-|xai-|sg-|hf_|eyJ|Bearer|gho_|ghu_|ghs_|ght_|glpat-|xoxb-|xoxp-|xoxr-|sq_|live_|sk_live_|sk_test_|rk_live_|rk_test_|AKIA|SG\\.|SECRET_KEY|API_KEY|AUTH_TOKEN|access_token|refresh_token)' | wc -l)
FAILED_LOGINS=$(grep -E 'Failed password|authentication failure' /var/log/auth.log 2>/dev/null | tail -n 100 | wc -l)
if [ "$CRED_COUNT" -gt 0 ]; then
    SEVERITY="high"
    EVIDENCE="Exposed credentials detected in `/opt/data/.env`. Found $CRED_COUNT potential credentials exposed."
elif [ "$FAILED_LOGINS" -gt 0 ]; then
    SEVERITY="medium"
    EVIDENCE="$FAILED_LOGINS failed login attempts detected in auth.log."
else
    SEVERITY=""
    EVIDENCE=""
fi
if [ -n "$SEVERITY" ]; then
    echo -e "ALERT: $SEVERITY\\n\\n$EVIDENCE\\n\\nAction: Alert Kiki to rotate these credentials. No auto-remediation performed." > $OUTBOX
    cat $OUTBOX
else
    if [ -f $OUTBOX ]; then
        rm $OUTBOX
    fi
    echo "[SILENT]"
fi