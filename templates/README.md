# AI Whisperers — Templates

Per-repo scaffolding templates. Generated 2026-08-28.

## Files

| File | Purpose | Install |
|---|---|---|
| `gitignore.template` | Standard `.gitignore` for client repos (secrets, builds, agent scratch, IDE noise) | Copy to repo root as `.gitignore` |
| `AGENTS.md.template` | Standard agent entry-point doc | Copy to repo root as `AGENTS.md`, replace `{{...}}` placeholders |
| `pre-commit.template` | Combined secret-leak + trademark-scrub pre-commit hook | `bash install-hooks.sh` from the repo root |
| `install-hooks.sh` | One-liner installer for `pre-commit` (and optionally `AGENTS.md`, `.gitignore`) | `bash /opt/data/agents-v2/templates/install-hooks.sh --with-agents --with-gitignore` |

## Standard workflow

```bash
# One-time per repo:
cd /path/to/repo
bash /opt/data/agents-v2/templates/install-hooks.sh --with-agents --with-gitignore

# Then `git commit` will run secret-leak + trademark-scrub automatically.
```

## What these templates close (from GAP-AUDIT-2026-08-13)

- **Gap 3.3** (trademark pre-commit hook not wired): `pre-commit.template` wires it.
- **Gap 2.5** (no alerting on error state): `install-hooks.sh` is also callable from a cron to verify hook installation across all repos.
- **Secret leaks** (P0 advisory 2026-08-28): `secret-leak-check.sh` catches GH PAT, OpenAI/Anthropic/Stripe/AWS keys. Supabase JWTs (`eyJ...`) are NOT caught — see Known Limitations below.

## Known limitations

1. **Supabase JWTs** (`eyJ...` base64-prefix) are not in the secret regex. They look like base64 and would generate too many false positives. Add a Supabase-specific check if needed.
2. **Generic `api_key=...` patterns** are not covered (only provider-specific prefixes).
3. **Existing files** with banned terms or secrets already in history: pre-commit only checks staged files. Use `trufflehog` or `gitleaks` against full history for retroactive scanning.
4. **`--no-verify`** bypasses everything. Use it sparingly and file an issue.

## References

- `/opt/data/scratchpad/analysis/P0-SECURITY-ADVISORY.md` (active secret leaks)
- `/opt/data/scratchpad/analysis/agent-org-improvement.md` (Layer 1 commands + hook design)
- `/opt/data/agents/GAP-AUDIT-2026-08-13.md` (gap 3.3 origin)
