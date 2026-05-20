#!/usr/bin/env python3
"""Generate content based on the schedule. Run daily to check if content is needed."""
import json, os, sys
from datetime import datetime

# Read schedule
schedule_file = "/home/josh/Development/Projects/digitalmarketing/CONTENT-SCHEDULE.md"
if not os.path.exists(schedule_file):
    print("No schedule file found")
    sys.exit(1)

with open(schedule_file) as f:
    content = f.read()

# Map dates to topics
import re
posts = []
for match in re.finditer(r'\|\s*(\w+\d+P\d+)\s*\|\s*(\d+\s+\w+)\s*\|([^|]+)', content):
    post_id = match.group(1)
    date_str = match.group(2)
    topic = match.group(3).strip()
    posts.append({"id": post_id, "date": date_str, "topic": topic})

# Check if today has a post
today = datetime.now().strftime("%-d %b")
today_posts = [p for p in posts if p["date"] == today]

if today_posts:
    for p in today_posts:
        print(f"📋 Today's post: {p['id']} - {p['topic']}")
        # Call content_engine.py with this topic
        topic = p["topic"].split("—")[0].strip() if "—" in p["topic"] else p["topic"]
        os.system(f'DS_API_KEY="$DS_API_KEY" python3 /home/josh/Development/Projects/digitalmarketing/scripts/content_engine.py "{topic}"')
else:
    print(f"No post scheduled for today ({today})")
    print("Next posts:")
    for p in posts[:3]:
        print(f"  {p['id']}: {p['date']} - {p['topic']}")
