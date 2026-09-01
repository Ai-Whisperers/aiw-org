# DEMIURGE-098 Context

**STATUS**: PENDING
**TITLE**: paths-aiw-root-env-var-threading
**OWNER**: AI
**SIZE**: 45m

## Focus

WS-3 item 1: 'scripts/_paths.py exposing AIW_ROOT = Path(os.environ.get(AIW_ROOT, /opt/data)) plus derived constants. Thread through all ~107 files. Mechanical; commit in batches by directory.'

## Sprint / Phase

Phase "Kernel" (per docs/HERMES-ANSWERS-2026-09-02.md + design docs).

## Blocked by

DEMIURGE-099 (hermetic test infrastructure)

