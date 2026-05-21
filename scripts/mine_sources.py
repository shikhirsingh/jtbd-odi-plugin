#!/usr/bin/env python3
"""
mine_sources.py — Lightweight helpers for the data-miner agent. Wraps
public-API fetches for Reddit, StackExchange, Apple App Store RSS, and
a generic RSS reader. Used by the data-miner agent to populate
mining-out/raw-posts.json.

Important: this script ONLY uses official, ToS-friendly endpoints.
- Reddit: /r/<sub>/search.json (read-only public JSON)
- StackExchange: api.stackexchange.com /2.3/search/advanced
- App Store: itunes.apple.com /rss/customerreviews/...
- Generic RSS / Atom

Twitter/X is intentionally NOT wrapped — it requires per-user credentials.

Usage:
    python mine_sources.py reddit "best wireless earbuds" --sub headphones --limit 100 --out reddit.json
    python mine_sources.py stackexchange "headphones offline music" --site superuser --limit 50 --out se.json
    python mine_sources.py appstore-rss 1142110895 --country us --out appstore.json
    python mine_sources.py rss "https://example.com/feed.xml" --out feed.json
"""

import argparse
import json
import sys
import time
from pathlib import Path

import requests


USER_AGENT = "jtbd-odi-plugin/1.0 (research; +https://github.com/shikhirsingh/jtbd-odi-plugin)"


def fetch_reddit(query: str, sub: str | None, limit: int) -> list[dict]:
    if sub:
        url = f"https://www.reddit.com/r/{sub}/search.json"
        params = {"q": query, "restrict_sr": "on", "limit": min(limit, 100), "sort": "relevance"}
    else:
        url = "https://www.reddit.com/search.json"
        params = {"q": query, "limit": min(limit, 100), "sort": "relevance"}
    r = requests.get(url, params=params, headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    posts = []
    for child in r.json().get("data", {}).get("children", []):
        d = child["data"]
        posts.append({
            "id": f"reddit-{d.get('subreddit')}-{d.get('id')}",
            "text": (d.get("title", "") + "\n\n" + d.get("selftext", ""))[:800],
            "source": "reddit",
            "source_url": "https://reddit.com" + d.get("permalink", ""),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(d.get("created_utc", 0))),
            "engagement_norm": min(1.0, d.get("score", 0) / 500),
            "language": "en",
        })
    return posts


def fetch_stackexchange(query: str, site: str, limit: int) -> list[dict]:
    url = "https://api.stackexchange.com/2.3/search/advanced"
    params = {"q": query, "site": site, "pagesize": min(limit, 100), "sort": "votes", "order": "desc"}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    posts = []
    for item in r.json().get("items", []):
        posts.append({
            "id": f"stackexchange-{site}-{item['question_id']}",
            "text": item.get("title", "")[:800],
            "source": f"stackexchange/{site}",
            "source_url": item.get("link"),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(item.get("creation_date", 0))),
            "engagement_norm": min(1.0, item.get("score", 0) / 50),
            "language": "en",
        })
    return posts


def fetch_appstore_rss(app_id: str, country: str = "us") -> list[dict]:
    url = f"https://itunes.apple.com/{country}/rss/customerreviews/id={app_id}/sortBy=mostRecent/json"
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    posts = []
    for entry in r.json().get("feed", {}).get("entry", [])[1:]:  # first entry is metadata
        if isinstance(entry, dict) and "content" in entry:
            text = entry["content"].get("label", "")[:800]
            rating = int(entry.get("im:rating", {}).get("label", "3"))
            posts.append({
                "id": f"appstore-{app_id}-{entry.get('id', {}).get('label')}",
                "text": text,
                "source": f"appstore/{app_id}",
                "source_url": entry.get("link", {}).get("attributes", {}).get("href", ""),
                "timestamp": entry.get("updated", {}).get("label", ""),
                "engagement_norm": (rating - 3) / 2.0,  # -1..+1
                "language": "en",
                "rating": rating,
            })
    return posts


def fetch_rss(url: str) -> list[dict]:
    from xml.etree import ElementTree as ET
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    root = ET.fromstring(r.text)
    posts = []
    for item in root.iter("item"):
        title = item.findtext("title", "")
        desc = item.findtext("description", "")
        link = item.findtext("link", "")
        pub = item.findtext("pubDate", "")
        posts.append({
            "id": f"rss-{hash(link) & 0xffffffff:x}",
            "text": (title + "\n\n" + desc)[:800],
            "source": f"rss/{url}",
            "source_url": link,
            "timestamp": pub,
            "engagement_norm": 0.5,
            "language": "en",
        })
    return posts


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p1 = sub.add_parser("reddit")
    p1.add_argument("query")
    p1.add_argument("--sub")
    p1.add_argument("--limit", type=int, default=100)
    p1.add_argument("--out", required=True)

    p2 = sub.add_parser("stackexchange")
    p2.add_argument("query")
    p2.add_argument("--site", default="stackoverflow")
    p2.add_argument("--limit", type=int, default=50)
    p2.add_argument("--out", required=True)

    p3 = sub.add_parser("appstore-rss")
    p3.add_argument("app_id")
    p3.add_argument("--country", default="us")
    p3.add_argument("--out", required=True)

    p4 = sub.add_parser("rss")
    p4.add_argument("url")
    p4.add_argument("--out", required=True)

    args = parser.parse_args()

    if args.cmd == "reddit":
        posts = fetch_reddit(args.query, args.sub, args.limit)
    elif args.cmd == "stackexchange":
        posts = fetch_stackexchange(args.query, args.site, args.limit)
    elif args.cmd == "appstore-rss":
        posts = fetch_appstore_rss(args.app_id, args.country)
    elif args.cmd == "rss":
        posts = fetch_rss(args.url)
    else:
        parser.error("unknown cmd")

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump({"source": args.cmd, "n": len(posts), "posts": posts}, f, indent=2)
    print(f"[ok] {args.out} — {len(posts)} posts", file=sys.stderr)


if __name__ == "__main__":
    main()
