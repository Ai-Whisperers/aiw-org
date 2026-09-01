"""Memory L3 keyword+tag inverted index for the Mnemosyne memory layer.

Phase 1.3 of AIW upgrade plan.
Pattern source: iPythoning/b2b-sdr-agent-template (Layer 3 of 4-layer memory).
What it does:
  - Maintains an inverted index of (keyword/tag -> signal_id set) on disk
  - Build from a JSONL file of signal records
  - Provides fast structured lookup: by tag, by keyword, by date range
  - Append-only writes (no lock contention)
Usage:
  python3 -m scripts.memory.signal_index build --source /path/to/signals.ndjson
  python3 -m scripts.memory.signal_index query --tag meeting
  python3 -m scripts.memory.signal_index query --keyword "deploy_prod"
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

DEFAULT_INDEX_PATH = Path("/opt/data/state/signal_index.json")
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "be", "been", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "must", "can", "this",
    "that", "these", "those", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "as", "into", "through", "during", "before",
    "after", "above", "below", "between", "and", "but", "or", "yet",
    "so", "if", "then", "than", "at", "by", "for", "from", "in", "of",
    "on", "to", "with", "as", "i", "you", "we", "they", "he", "she",
    "it", "my", "your", "our", "their",
}

# Token regex: split on non-alphanumeric (but keep underscores in identifiers)
_TOKEN_RE = re.compile(r"[a-z0-9_]+")


def _tokenize(text: str) -> list:
    if not text:
        return []
    text = text.lower()
    return [t for t in _TOKEN_RE.findall(text) if len(t) >= 2 and t not in STOPWORDS]


def _load_index(path: Path) -> dict:
    if not path.exists():
        return {
            "_version": 1,
            "_created": None,
            "_last_build_ts": None,
            "by_signal": {},   # signal_id -> {"tags": [], "keywords": [], "ts": ...}
            "by_tag": {},      # tag -> [signal_id, ...]
            "by_keyword": {},  # keyword -> [signal_id, ...]
        }
    content = path.read_text().strip()
    if not content:
        # Empty file (e.g., just-created temp file). Treat as fresh index.
        return {
            "_version": 1,
            "_created": None,
            "_last_build_ts": None,
            "by_signal": {},
            "by_tag": {},
            "by_keyword": {},
        }
    return json.loads(content)


def _save_index(path: Path, idx: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write atomically
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(idx, indent=2, ensure_ascii=False))
    tmp.replace(path)


def _extract_signal_meta(signal: dict) -> dict:
    """Extract tags + keywords from a signal record."""
    tags = signal.get("routing_tags", []) or signal.get("tags", []) or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    # Extract keywords from text fields
    text_fields = [
        signal.get("source", ""),
        signal.get("type", ""),
        json.dumps(signal.get("payload", {}), ensure_ascii=False),
    ]
    keywords = set()
    for f in text_fields:
        keywords.update(_tokenize(f))
    return {
        "tags": tags,
        "keywords": sorted(keywords),
        "ts": signal.get("ts") or signal.get("created_at"),
    }


def build_index(source: Path, index_path: Path = DEFAULT_INDEX_PATH) -> dict:
    """Build (or rebuild) the index from a JSONL source file."""
    idx = _load_index(index_path)
    signals_processed = 0
    for line in source.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            signal = json.loads(line)
        except json.JSONDecodeError:
            continue
        signal_id = signal.get("id") or signal.get("signal_id")
        if not signal_id:
            continue
        meta = _extract_signal_meta(signal)
        idx["by_signal"][signal_id] = meta
        for tag in meta["tags"]:
            idx["by_tag"].setdefault(tag, [])
            if signal_id not in idx["by_tag"][tag]:
                idx["by_tag"][tag].append(signal_id)
        for kw in meta["keywords"]:
            idx["by_keyword"].setdefault(kw, [])
            if signal_id not in idx["by_keyword"][kw]:
                idx["by_keyword"][kw].append(signal_id)
        signals_processed += 1
    import datetime as _dt
    idx["_last_build_ts"] = _dt.datetime.now(_dt.timezone.utc).isoformat()
    if idx["_created"] is None:
        idx["_created"] = idx["_last_build_ts"]
    _save_index(index_path, idx)
    return {
        "signals_processed": signals_processed,
        "index_size_kb": index_path.stat().st_size // 1024,
        "unique_tags": len(idx["by_tag"]),
        "unique_keywords": len(idx["by_keyword"]),
        "build_ts": idx["_last_build_ts"],
    }


def query_tag(tag: str, index_path: Path = DEFAULT_INDEX_PATH) -> list:
    idx = _load_index(index_path)
    return idx["by_tag"].get(tag, [])


def query_keyword(keyword: str, index_path: Path = DEFAULT_INDEX_PATH) -> list:
    idx = _load_index(index_path)
    return idx["by_keyword"].get(keyword.lower(), [])


def query_date_range(start_iso: str, end_iso: str,
                     index_path: Path = DEFAULT_INDEX_PATH) -> list:
    idx = _load_index(index_path)
    results = []
    for sid, meta in idx["by_signal"].items():
        ts = meta.get("ts")
        if ts and start_iso <= ts <= end_iso:
            results.append(sid)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="L3 memory signal index")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_build = sub.add_parser("build")
    p_build.add_argument("--source", type=Path, required=True)
    p_build.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH)
    p_tag = sub.add_parser("query")
    p_tag.add_argument("--tag", type=str)
    p_tag.add_argument("--keyword", type=str)
    p_tag.add_argument("--index", type=Path, default=DEFAULT_INDEX_PATH)
    p_tag.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    if args.cmd == "build":
        report = build_index(args.source, args.index)
        print(json.dumps(report, indent=2))
        return 0
    elif args.cmd == "query":
        results = []
        if args.tag:
            results.append({"by_tag": args.tag, "signal_ids": query_tag(args.tag, args.index)})
        if args.keyword:
            results.append({"by_keyword": args.keyword, "signal_ids": query_keyword(args.keyword, args.index)})
        for r in results:
            print(json.dumps(r, indent=2))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
