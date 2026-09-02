# DEMIURGE-122 Context

**STATUS**: PENDING
**TITLE**: youtube-channel-fetcher + david-ondrej-analysis
**OWNER**: AI
**SIZE**: 30m

## Focus

YouTube returned 401 on direct `/@DavidOndrej/videos` fetch. Built
a no-auth helper using RSS feed + yt-dlp flat-playlist that fetched
394 grounded videos. Ship the helper + the analysis doc.

## Sprint / Phase

Phase "Kernel" (Phase Kernel brief). Adjacent to DEMIURGE-121 (cron audit)
but addresses a different operator request: "search also for recent
videos and all insights we can get from him to upgrade our aiw-org".

## What ships

1. `scripts/fetch-youtube-channel.py` — no-auth YouTube data fetcher
   (RSS + yt-dlp flat-playlist). Email to operator: install yt-dlp
   via `uv tool install yt-dlp` before first use.
2. `tests/test_fetch_youtube_channel.py` — 9 tests, all pass.
3. `analysis/DAVID-ONDREJ-CONTENT-ANALYSIS-2026-09-02.md` — analysis doc.
4. `analysis/DAVID-ONDREJ-VIDEOS.json` — the 394-video corpus.
