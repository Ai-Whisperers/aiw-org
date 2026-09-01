# DEMIURGE-112: rotate-four-credentials

**Sprint**: Phase Kernel
**Size**: 45m
**Owner**: Ivan

## Objective

Rotate/revoke the 4 leaking credentials.

## Acceptance criteria

- [ ] SUPABASE_SERVICE_ROLE_KEY rotated (Supabase console)
- [ ] 3 GitHub PATs revoked (github.com/settings/tokens)
- [ ] 16 R2 presigned URLs replaced (Kiki-task, ~2h)
- [ ] /opt/data/.hermes/.env chmod 600 + sudo installed

## Deliverables (paths)

- `(operator console actions)`

## Verification

```bash
# See progress.md for verification output (once started)
```
