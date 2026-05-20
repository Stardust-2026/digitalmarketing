#!/usr/bin/env python3
"""Master carousel builder. Usage: python3 build_carousel.py "Topic" [3]
Generates HTML carousel, renders to PNG slides + attempts PDF.

Args:
  topic: The carousel topic (required)
  slides: Number of slides (default: 3, max: 5)

Dependencies: playwright, Pillow
Paths: uses templates from ./prototypes/
Output: saves to ./prototypes/{topic_slug}_slide_XX.png
"""
import sys, os, json, urllib.request, re, textwrap
from datetime import datetime

TOPIC = sys.argv[1] if len(sys.argv) > 1 else "AI Strategy"
SLIDE_COUNT = int(sys.argv[2]) if len(sys.argv) > 2 else 3
OUTPUT_DIR = "/home/josh/Development/Projects/digitalmarketing/prototypes"
DS_KEY = os.environ.get("DS_API_KEY", "")

# 1. Generate slide content using DeepSeek
if not DS_KEY:
    print("NO DS_API_KEY")
    sys.exit(1)

prompt = f"""Create a LinkedIn carousel about: {TOPIC}

Generate {SLIDE_COUNT} slides. Each slide has:
- A short headline (max 8 words)
- 2-3 supporting bullet points (max 15 words each)

Output format:
SLIDE 1|Headline|Point 1|Point 2|Point 3
SLIDE 2|Headline|Point 1|Point 2
...etc

Make it actionable, business-focused. No fluff."""

req = urllib.request.Request(
    "https://api.deepseek.com/v1/chat/completions",
    data=json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You generate LinkedIn carousel content. Output in pipe-delimited format only."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }).encode(),
    headers={"Authorization": f"Bearer {DS_KEY}", "Content-Type": "application/json"}
)
resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
content = resp["choices"][0]["message"]["content"].strip()

# Parse slides
slides_data = []
for line in content.split("\n"):
    line = line.strip()
    if line.startswith("SLIDE "):
        parts = line.split("|")
        if len(parts) >= 2:
            slides_data.append({
                "headline": parts[1].strip() if len(parts) > 1 else "",
                "points": [p.strip() for p in parts[2:] if p.strip()]
            })

print(f"Generated {len(slides_data)} slides for: {TOPIC}")

# 2. Generate HTML
topic_slug = re.sub(r'[^a-z0-9]+', '-', TOPIC.lower())[:30]
colors = ["#c8a050", "#4FC3F7", "#64FFDA", "#D4A843", "#FF8A65"]
icons = ["🎯", "⚡", "🧠", "🚀", "💡"]

html_parts = ["""<!DOCTYPE html><html><head><style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Playfair+Display:ital,wght@0,700;1,400&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0f;display:flex;flex-wrap:wrap;gap:20px;padding:40px;font-family:'Inter',sans-serif}
.slide{width:1080px;height:1080px;background:linear-gradient(145deg,#0f0f1a 0%,#1a1a2e 100%);border-radius:32px;position:relative;overflow:hidden;padding:60px 70px;box-shadow:0 20px 60px rgba(0,0,0,0.5);flex-shrink:0}
.slide::before{content:'';position:absolute;top:-200px;right:-200px;width:500px;height:500px;background:radial-gradient(circle,rgba(180,120,60,0.08) 0%,transparent 70%);border-radius:50%}
.brand-bar{position:absolute;top:0;left:0;right:0;height:6px;background:linear-gradient(90deg,#c8a050,#e8c060,#c8a050)}
h1{font-family:'Playfair Display',serif;font-weight:700;color:#f0ece4;line-height:1.15;font-size:44px;margin-top:40px}
.sub{font-size:18px;color:rgba(240,236,228,0.75);font-weight:300;line-height:1.6;margin-top:20px}
.point{margin-top:24px;padding:18px 24px;background:rgba(255,255,255,0.02);border-left:3px solid COLOR;border-radius:0 8px 8px 0}
.point-num{font-size:11px;letter-spacing:2px;color:COLOR;font-weight:600}
.point-text{font-size:18px;color:#f0ece4;margin-top:4px;font-weight:300;line-height:1.5}
.pn{position:absolute;bottom:40px;left:70px;font-size:14px;color:rgba(255,255,255,0.15);letter-spacing:1px}
.cover-center{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;width:85%}
.label{font-size:14px;letter-spacing:3px;text-transform:uppercase;color:rgba(200,160,80,0.7);font-weight:600;margin-bottom:20px}
.sigil{position:absolute;bottom:60px;right:70px;opacity:0.06;font-family:'Playfair Display',serif;font-size:120px;font-style:italic;color:#c8a050}
</style></head><body>"""]

# Cover slide
html_parts.append(f"""<div class="slide"><div class="brand-bar"></div><div class="cover-center">
<div class="label">AI Strategy · Application</div>
<h1 style="font-size:52px;">{TOPIC}</h1>
<div style="margin-top:50px;"><span style="font-size:16px;color:rgba(255,255,255,0.3);letter-spacing:2px;">by Josh Lai · AI-Augmented Strategy</span></div>
</div><div class="sigil">应用</div><div class="pn">01 / {len(slides_data)+1}</div></div>""")

for i, slide in enumerate(slides_data):
    color = colors[i % len(colors)]
    icon = icons[i % len(icons)]
    points_html = ""
    for j, pt in enumerate(slide["points"]):
        points_html += f"""<div class="point" style="border-left-color:{color}">
<div class="point-num" style="color:{color}">{chr(65+j)}</div>
<div class="point-text">{pt}</div>
</div>"""
    
    html_parts.append(f"""<div class="slide"><div class="brand-bar"></div>
<h1>{icon} {slide['headline']}</h1>
{points_html}
<div class="sigil">应用</div>
<div class="pn">{i+2:02d} / {len(slides_data)+1}</div></div>""")

html_parts.append("</body></html>")
html_content = "\n".join(html_parts)

# 3. Save HTML
html_path = os.path.join(OUTPUT_DIR, f"carousel_{topic_slug}.html")
with open(html_path, "w") as f:
    f.write(html_content)
print(f"HTML saved: {html_path}")

# 4. Render to PNGs using Playwright
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1080})
    page.goto(f"file://{html_path}")
    page.wait_for_timeout(1000)
    
    slides = page.locator(".slide")
    count = slides.count()
    print(f"Rendering {count} slides...")
    
    for i in range(count):
        path = os.path.join(OUTPUT_DIR, f"carousel_{topic_slug}_slide_{i+1:02d}.png")
        slides.nth(i).screenshot(path=path)
        print(f"  Slide {i+1}: {os.path.basename(path)}")
    
    browser.close()

print(f"\n✅ Carousel '{TOPIC}' ready! {count} slides in {OUTPUT_DIR}")
