#!/usr/bin/env python3
"""fetch-youtube-channel.py — Fetch YouTube channel data without auth.

Per Phase Kernel investigation (2026-09-02): the official `/@channel/videos`
URL returns 401 when not logged in. This helper sidesteps that by using
two auth-free channels:

1. **RSS feed** at `https://www.youtube.com/feeds/videos.xml?channel_id=ID`
   — public, returns the most recent 15 videos with titles, IDs, dates.
2. **yt-dlp with --flat-playlist** for playlists + the `/videos` tab
   — public metadata extraction (titles, durations, view counts, dates).

Together these give 200-400 grounded videos per channel.

Per AIW conventions:
- No credentials stored; uses public YouTube endpoints only
- No rate-limit concerns for low-frequency use (analyzing 1 channel/week)
- yt-dlp is installed via `uv tool install yt-dlp` (see setup notes)

Usage:
    uv tool install yt-dlp
    python3 scripts/fetch-youtube-channel.py --channel-id UCPGrgwfbkjTIgPoOh2q1BAg --output ./out.json

This script is for AIW-internal analysis (per R11: not deployed for Saskia).
"""
import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


def fetch_rss(channel_id: str) -> list:
    """Fetch the public RSS feed for a YouTube channel."""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    r = subprocess.run(
        ["curl", "-s", "-L", "--max-time", "30", url],
        capture_output=True, text=True
    )
    if r.returncode != 0 or "<entry>" not in r.stdout:
        return []
    root = ET.fromstring(r.stdout)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }
    videos = []
    for entry in root.findall("atom:entry", ns):
        title_el = entry.find("atom:title", ns)
        link_el = entry.find("atom:link", ns)
        published_el = entry.find("atom:published", ns)
        vid_el = entry.find("yt:videoId", ns)
        if title_el is None or vid_el is None:
            continue
        videos.append({
            "title": title_el.text,
            "video_id": vid_el.text,
            "url": link_el.get("href") if link_el is not None else None,
            "published": published_el.text if published_el is not None else None,
            "source": "rss",
            "view_count": None,
            "duration": None,
        })
    return videos


def fetch_yt_dlp(url: str, source: str = "yt-dlp",
                 max_videos: int = 500) -> list:
    """Fetch playlist/channel metadata via yt-dlp flat-playlist."""
    r = subprocess.run(
        ["yt-dlp", "--flat-playlist", "--no-warnings", "--skip-download",
         "--extractor-args", "youtubetab:approximate_date",
         "--print", "%(title)s\t%(id)s\t%(duration_string)s\t%(view_count)s\t%(upload_date>%Y-%m-%d)s",
         url],
        capture_output=True, text=True, timeout=180
    )
    if r.returncode != 0:
        return []
    videos = []
    for line in r.stdout.strip().split("\n"):
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        videos.append({
            "title": parts[0],
            "video_id": parts[1],
            "duration": parts[2] if parts[2] != "NA" else None,
            "view_count": int(parts[3]) if parts[3] and parts[3] != "NA" else None,
            "upload_date": parts[4] if parts[4] != "NA" else None,
            "source": source,
        })
        if len(videos) >= max_videos:
            break
    return videos


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--channel-id", required=True,
                    help="YouTube channel ID (not handle)")
    ap.add_argument("--handle", help="Optional handle like @DavidOndrej for display")
    ap.add_argument("--output", "-o", required=True,
                    help="Output JSON path")
    ap.add_argument("--include-videos-tab", action="store_true", default=True,
                    help="Include the /videos tab (default true)")
    ap.add_argument("--playlists", nargs="*", default=[],
                    help="Optional playlist URLs to include")
    args = ap.parse_args()

    print(f"Fetching YouTube data for channel {args.channel_id}...")
    all_videos = []
    counts = {}

    # RSS
    rss = fetch_rss(args.channel_id)
    counts["rss"] = len(rss)
    all_videos.extend(rss)

    # /videos tab
    if args.include_videos_tab:
        videos_url = (
            f"https://www.youtube.com/@{args.handle}/videos"
            if args.handle
            else f"https://www.youtube.com/channel/{args.channel_id}/videos"
        )
        vids = fetch_yt_dlp(videos_url, source="videos_tab")
        counts["videos_tab"] = len(vids)
        all_videos.extend(vids)

    # Playlists
    for p_url in args.playlists:
        vids = fetch_yt_dlp(p_url, source=p_url)
        counts[p_url] = len(vids)
        all_videos.extend(vids)

    # Dedupe by video_id
    seen = set()
    unique = []
    for v in all_videos:
        if v["video_id"] not in seen:
            seen.add(v["video_id"])
            unique.append(v)
    counts["unique"] = len(unique)

    output = {
        "channel_id": args.channel_id,
        "handle": args.handle,
        "fetched_at": datetime.now().astimezone().isoformat(),
        "method": "RSS + yt-dlp flat-playlist (no auth)",
        "counts": counts,
        "total": len(unique),
        "videos": unique,
    }

    out_path = Path(args.output)
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nSaved {len(unique)} unique videos to {out_path}")
    print(f"Counts: {counts}")


if __name__ == "__main__":
    sys.exit(main())
