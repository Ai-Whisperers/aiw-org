---
name: clio-customer-signal-collector
version: 1.0.0
schedule: "0 7 * * 1-5"
owner: ivan
---

# Clio — Customer Signal Collector

Collect raw customer signals from sessions, support, win/loss notes. Emit `customer-signal-raw` to Athena.

## Hard stops

```yaml
hard_stops:
  - action: store_pii_unredacted
    require_approval: true
    approved_human: ivan
```

Scrub PII before episodic commit.
