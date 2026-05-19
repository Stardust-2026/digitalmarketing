#!/usr/bin/env python3
"""Content Engine — generates multi-platform posts from a topic using DeepSeek."""
import json, os, urllib.request, sys, textwrap

DS_KEY = os.environ.get("DS_API_KEY", "")
if not DS_KEY:
    print("NO DS_API_KEY")
    sys.exit(1)

TOPIC = sys.argv[1] if len(sys.argv) > 1 else "AI agents for business beginners"

SYSTEM_PROMPT = """You are the Content Engine for Global South Advisory, an AI-Augmented advisory firm. Your audience is business professionals, not developers.

For the topic given, produce 4 pieces of content:

1. LINKEDIN POST: Hook (1-2 sentences) → Explanation (2-3 sentences) → Example (1-2 sentences) → CTA (1 sentence) → Hashtags (3-4). Max 200 words. Short paragraphs.

2. YOUTUBE SHORTS SCRIPT: 60 seconds. Timed with [VISUAL] cues. Hook 0-5s, Explanation 5-30s, Example 30-50s, CTA 50-60s.

3. FACEBOOK POST: Casual, conversational. 100-150 words. 2-3 emojis. Question at end.

4. WECHAT ARTICLE: Chinese + English mix. 200-300 words. Professional tone for Chinese business audience.

Output in this exact format:
===LINKEDIN===
[linkedin post text]
===YOUTUBE===
[script with timestamps]
===FACEBOOK===
[facebook post text]
===WECHAT===
[wechat article text]"""

req = urllib.request.Request(
    "https://api.deepseek.com/v1/chat/completions",
    data=json.dumps({
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Topic: {TOPIC}\n\nGenerate all 4 content formats."}
        ],
        "max_tokens": 2000,
        "temperature": 0.7
    }).encode(),
    headers={"Authorization": f"Bearer {DS_KEY}", "Content-Type": "application/json"}
)

try:
    resp = urllib.request.urlopen(req, timeout=60)
    data = json.loads(resp.read())
    content = data["choices"][0]["message"]["content"]
    
    # Save to file
    out_dir = "/home/josh/Development/Projects/digitalmarketing/content"
    os.makedirs(out_dir, exist_ok=True)
    from datetime import datetime
    fname = f"{out_dir}/content_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(fname, "w") as f:
        f.write(f"# Content Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Topic: {TOPIC}\n\n")
        f.write(content)
    
    print(f"✅ Content saved to {fname}")
    # Print LinkedIn post for quick use
    linkedin_start = content.find("===LINKEDIN===")
    linkedin_end = content.find("===YOUTUBE===")
    if linkedin_start >= 0 and linkedin_end >= 0:
        print("\n📱 LINKEDIN POST:")
        print(content[linkedin_start+13:linkedin_end].strip())
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
