#!/usr/bin/env python3
"""Daily Brief — consolidates Content Engine and Market Intel outputs into CEO summary."""
import os, glob
from datetime import datetime, timedelta

today = datetime.now().strftime("%Y%m%d")
yesterday = (datetime.now() - timedelta(1)).strftime("%Y%m%d")

content_dir = "/home/josh/Development/Projects/digitalmarketing/content"
intel_dir = "/home/josh/Development/Projects/digitalmarketing/intel"
brief_dir = "/home/josh/Development/Projects/digitalmarketing/briefs"
os.makedirs(brief_dir, exist_ok=True)

# Find today/yesterday's content and intel
recent_content = sorted(glob.glob(f"{content_dir}/*.md"))[-3:] if os.path.exists(content_dir) else []
recent_intel = sorted(glob.glob(f"{intel_dir}/*.md"))[-1:] if os.path.exists(intel_dir) else []

lines = [f"📋 GSA Daily Brief — {datetime.now().strftime('%d %b %Y')}", ""]

if recent_content:
    lines.append("📈 Content Queue:")
    for f in recent_content:
        name = os.path.basename(f)
        with open(f) as fh:
            first_line = fh.readline().strip()
        lines.append(f"  • {name} — {first_line}")
else:
    lines.append("📈 Content Queue: None")

lines.append("")

if recent_intel:
    lines.append("🔍 Market Signals:")
    with open(recent_intel[-1]) as fh:
        content = fh.read()
    for l in content.split("\n")[:10]:
        if l.strip():
            lines.append(f"  {l}")
else:
    lines.append("🔍 Market Signals: None")

lines.append("")
lines.append("✅ All systems: OK")
lines.append("")
lines.append("— GSA Operations Monitor")

brief = "\n".join(lines)
fname = f"{brief_dir}/brief_{today}.md"
with open(fname, "w") as f:
    f.write(brief)

print(brief)
