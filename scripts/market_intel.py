#!/usr/bin/env python3
"""Market Intel — scans for trending AI/business topics from Reddit and HN."""
import json, urllib.request, sys, os
from datetime import datetime

def fetch_hn():
    try:
        req = urllib.request.Request("https://hacker-news.firebaseio.com/v0/topstories.json")
        top = json.loads(urllib.request.urlopen(req, timeout=10).read())[:15]
        items = []
        for sid in top:
            try:
                item = json.loads(urllib.request.urlopen(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5).read())
                if item.get("title") and "AI" in (item.get("title","") + (item.get("url",""))):
                    items.append(f"- {item['title']} ({item.get('url','')[:80]})")
            except: pass
        return ["=== HN AI Stories ==="] + (items or ["- No AI stories in top 15"])
    except Exception as e:
        return [f"=== HN Error: {e}"]

def fetch_reddit():
    results = ["=== Reddit AI Signals ==="]
    for sub in ["artificialintelligence", "LocalLLaMA", "LangChain"]:
        try:
            req = urllib.request.Request(
                f"https://www.reddit.com/r/{sub}/hot/.json?limit=5",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            data = json.loads(urllib.request.urlopen(req, timeout=10).read())
            for post in data["data"]["children"]:
                t = post["data"]["title"]
                u = post["data"]["url"][:60]
                results.append(f"  r/{sub}: {t}")
        except: pass
    return results

lines = [f"# Market Intel Scan — {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
lines += fetch_hn() + [""] + fetch_reddit()

out_dir = "/home/josh/Development/Projects/digitalmarketing/intel"
os.makedirs(out_dir, exist_ok=True)
fname = f"{out_dir}/intel_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
with open(fname, "w") as f:
    f.write("\n".join(lines))

print(f"✅ Intel saved to {fname}")
for l in lines[:20]:
    print(l)
