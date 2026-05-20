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
    out_dir = "/home/josh/Development/Projects/digitalmarketing/review/pending"
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
        linkedin_text = content[linkedin_start+13:linkedin_end].strip()
        print("\n📱 LINKEDIN POST:")
        print(linkedin_text)
        
        # Update Notion coordination board with the new post
        try:
            notion_key = os.environ.get("NOTION_API_KEY", "")
            if notion_key:
                board_id = "366da819-df10-81dd-b0a7-f00857365477"
                notion_headers = {
                    "Authorization": f"Bearer {notion_key}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json"
                }
                # Read current board content
                read_req = urllib.request.Request(
                    f"https://api.notion.com/v1/pages/{board_id}/markdown",
                    headers=notion_headers
                )
                read_resp = json.loads(urllib.request.urlopen(read_req, timeout=10).read())
                current_md = read_resp.get("markdown", "")
                
                # Replace the pending section with new content
                from datetime import datetime
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                new_section = f"""\n## ⏳ Pending Approval\n\n### W1P2 — {now} — \"{TOPIC}\"\n\n**LinkedIn post draft:**\n\n{linkedin_text}\n\n**To approve:** Send `approve W1P2` on Telegram\n**To edit:** Edit the text above and send `check board` on Telegram\n---"""
                
                # Find and replace the pending section
                if "## ⏳ Pending Approval" in current_md:
                    parts = current_md.split("## ⏳ Pending Approval")
                    rest = parts[1].split("## ✅ Recently Posted") if "## ✅ Recently Posted" in parts[1] else [parts[1], ""]
                    updated = parts[0] + "## ⏳ Pending Approval" + new_section + "\n\n## ✅ Recently Posted" + rest[1]
                else:
                    updated = current_md + "\n\n" + new_section
                
                # Patch the page
                patch_data = json.dumps({"type": "replace_content", "replace_content": {"new_str": updated}})
                patch_req = urllib.request.Request(
                    f"https://api.notion.com/v1/pages/{board_id}/markdown",
                    data=patch_data.encode(), headers=notion_headers, method="PATCH"
                )
                urllib.request.urlopen(patch_req, timeout=10)
                print("📋 Coordination board updated on Notion")
        except Exception as e:
            print(f"⚠️ Board update skipped: {e}")
    else:
        print(content[:200])
except Exception as e:
    print(f"❌ Error: {e}")