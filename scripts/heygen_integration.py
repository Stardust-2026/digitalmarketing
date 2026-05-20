#!/usr/bin/env python3
"""HeyGen video API integration — auto-generate avatar videos from Content Engine scripts.
Requires HeyGen API key and an existing Instant Avatar.

Setup:
1. Create Instant Avatar at https://app.heygen.com (see heygen-production-plan.md)
2. Get API key from HeyGen dashboard → API
3. Set HEYGEN_API_KEY env var
"""
import json, os, sys, urllib.request, urllib.error, time

HEYGEN_KEY = os.environ.get("HEYGEN_API_KEY", "")

def generate_avatar_video(script_text, avatar_id=None, title="AI Tip"):
    """Generate an avatar video from script text using HeyGen API.
    
    Args:
        script_text: The text the avatar will speak
        avatar_id: Your Instant Avatar ID (from dashboard)
        title: Video title
    
    Returns:
        Video URL when rendering is complete
    """
    if not HEYGEN_KEY:
        print("⚠️ No HEYGEN_API_KEY. Save script for manual HeyGen upload.")
        return None
    
    headers = {
        "Authorization": f"Bearer {HEYGEN_KEY}",
        "Content-Type": "application/json"
    }
    
    # Step 1: Create video task
    payload = {
        "video_inputs": [{
            "character": {
                "type": "avatar",
                "avatar_id": avatar_id or "your_avatar_id",
                "avatar_style": "normal"
            },
            "voice": {
                "type": "text",
                "input_text": script_text,
                "voice_id": "your_voice_id"  # or use HeyGen's default
            },
            "background": {
                "type": "color",
                "value": "#0a0a0f"
            }
        }],
        "title": title,
        "caption": False
    }
    
    try:
        req = urllib.request.Request(
            "https://api.heygen.com/v2/video/generate",
            data=json.dumps(payload).encode(),
            headers=headers, method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        video_id = result.get("data", {}).get("video_id", "")
        print(f"✅ HeyGen video queued: {video_id}")
        
        # Step 2: Poll until complete (up to 5 min)
        for _ in range(30):
            time.sleep(10)
            status_req = urllib.request.Request(
                f"https://api.heygen.com/v1/video_status.get?video_id={video_id}",
                headers=headers
            )
            status_resp = json.loads(urllib.request.urlopen(status_req).read())
            status = status_resp.get("data", {}).get("status", "")
            if status == "completed":
                video_url = status_resp["data"]["video_url"]
                print(f"✅ Video ready: {video_url}")
                return video_url
            elif status == "failed":
                print(f"❌ Video generation failed")
                return None
        
        print(f"⏳ Video still rendering. Check later. ID: {video_id}")
        return video_id
        
    except urllib.error.HTTPError as e:
        print(f"❌ HeyGen API error: {e.code} {e.read().decode()[:200]}")
        return None

if __name__ == "__main__":
    # Test with sample script
    test_script = "How to evaluate if an AI output is actually good. Run these three checks: relevance, specificity, actionability."
    generate_avatar_video(test_script, title="Test: AI Tip")
