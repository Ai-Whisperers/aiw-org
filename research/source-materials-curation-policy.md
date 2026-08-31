# Source-Materials Curation Policy

> **Phase 8 Area #26** | Research & Education dept | Owner: source-curator + research-tracker
> **Date**: 2026-09-01
> **Status**: Initial policy; calibrate after first month

---

## The corpus

`~/source-materials/` (referenced by `01-operations/source-curator/PROMPT.md`) contains 300+ files. Manual curation breaks at this scale.

---

## The scoring system

Each file gets 4 dimensions, each 0-10:

| Dimension | What it measures | How scored |
|-----------|------------------|------------|
| **Fresh** | Last updated within 90 days | (10 = today, 0 = >1 year) |
| **Valid** | All citations resolve (HTTP 200) | (10 = all valid, 0 = all broken) |
| **Active** | Cited/used in last 6 months | (10 = 5+ uses, 0 = 0 uses) |
| **Original** | Substantive vs derivative | (10 = original research, 0 = copy-paste) |

**Composite score** = average of 4 dimensions (0-10).

---

## Per-file recommendations

| Composite | Recommendation |
|-----------|----------------|
| 8.0-10.0 | Keep, refresh quarterly |
| 6.0-7.9 | Keep, refresh within 90d |
| 4.0-5.9 | Review manually; either refresh or archive |
| 0-3.9 | Archive (move to `~/source-materials/_archive/`) |

---

## Automation plan

| Step | Tool | Schedule |
|------|------|----------|
| 1. Score freshness | `find ~/source-materials/ -mtime -90` | Daily cron |
| 2. Validate URLs | `httpx` async | Weekly cron |
| 3. Track citations | grep across `research/` | Weekly cron |
| 4. Compute composite | small Python script | Weekly cron |
| 5. Apply policy | `mv` to archive if score <4 | Weekly cron |
| 6. Notify Ivan | `state/source-curation-report.json` | Weekly cron |

---

## Implementation sketch (Python)

```python
#!/usr/bin/env python3
"""Score source-materials and apply curation policy."""
from pathlib import Path
from datetime import datetime, timezone, timedelta

SOURCE_DIR = Path.home() / "source-materials"
ARCHIVE_DIR = SOURCE_DIR / "_archive"

def score_file(path):
    # Freshness
    age_days = (datetime.now(timezone.utc) - datetime.fromtimestamp(path.stat().st_mtime)).days
    fresh = max(0, 10 - age_days / 9)
    
    # (Validity and active would require URL/citation scanning)
    # For initial policy, just use freshness + active (citation count)
    
    return {"fresh": round(fresh, 2), "composite": round(fresh, 2)}

def main():
    for f in SOURCE_DIR.glob("**/*"):
        if f.is_dir() or "_archive" in str(f):
            continue
        score = score_file(f)
        if score["composite"] < 4.0:
            target = ARCHIVE_DIR / f.name
            f.rename(target)
            print(f"Archived {f.name} (score={score['composite']})")

if __name__ == "__main__":
    main()
```

---

## What NOT to do

- ❌ Auto-archive files with valid citations (premature)
- ❌ Trust freshness alone (some sources are timeless — keep)
- ❌ Archive without review (human review for files with >5 citations)

---

## Rollout

| Phase | When | What |
|-------|------|------|
| 1. Deploy scoring script | 2026-09-15 | Generate first report |
| 2. Manual review pass | 2026-09-22 | Adjust scoring weights |
| 3. Apply auto-archive | 2026-10-01 | Archive <4 files |
| 4. Monthly recurring | Monthly | Ongoing curation |

---

**Cross-references**:
- `01-operations/source-curator/PROMPT.md` (cross-cut)
- `~/source-materials/` (corpus)
- `analysis/PHASE-7-dept-research/05-research-education-research-areas.md` Area #5
- `~/skills/arxiv/`

