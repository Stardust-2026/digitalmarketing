#!/usr/bin/env python3
"""Market Intel — scans for trending AI/business topics. v2 with better scraping."""
import json, urllib.request, sys, os, re
from datetime import datetime

def fetch_hn():
    results = []
    try:
        req = urllib.request.Request(
            "https://hn.algolia.com/api/v1/search?query=AI+agent+LLM&tags=story&hitsPerPage=10")
        data = json.loads(urllib.request.urlopen(req, timeout=10).read())
        for hit in data.get("hits", []):
            title = hit.get("title", "")
            url = hit.get("url", "") or f"https://news.ycombinator.com/item?id={hit.get('objectID','')}"
            points = hit.get("points", 0)
            results.append(f"  [{points}pts] {title[:100]}")
    except Exception as e:
        results.append(f"  HN Error: {e}")
    return ["=== Hacker News (AI/Agent stories) ==="] + (results or ["  No results"])

def fetch_reddit():
    results = []
    for sub in ["artificialintelligence", "LocalLLaMA", "LangChain"]:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot/.json?limit=5"
            req = urllib.request.Request(url, headers={"User-Agent": "GSA-MarketIntel/1.0"})
            data = json.loads(urllib.request.urlopen(req, timeout=10).read())
            for post in data["data"]["children"]:
                t = post["data"]["title"][:120]
                score = post["data"].get("score", 0)
                results.append(f"  r/{sub} [{score}] {t}")
        except Exception as e:
            results.append(f"  r/{sub}: {str(e)[:60]}")
    return ["=== Reddit Hot Posts ==="] + (results or ["  No results"])

lines = [
    f"# Market Intel Scan — {datetime.now().strftime('%Y-%m-%d %H:%M SGT')}",
    ""
]
lines += fetch_hn() + [""] + fetch_reddit()

out_dir = "/home/josh/Development/Projects/digitalmarketing/intel"
os.makedirs(out_dir, exist_ok=True)
fname = f"{out_dir}/intel_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
with open(fname, "w") as f:
    f.write("\n".join(lines))

print(f"✅ Intel saved to {fname}")
for l in lines:
    print(l)
