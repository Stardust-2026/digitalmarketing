#!/usr/bin/env python3
"""Canva integration — auto-generate carousel slides from Content Engine output.
Uses Canva API to create branded slides from DeepSeek-generated content.

Setup: 
1. Get Canva API key from https://www.canva.com/developers/
2. Set CANVA_API_KEY env var
3. Create a branded template in Canva, note the template_id
"""
import json, os, sys, urllib.request, urllib.error, re
from datetime import datetime

CANVA_KEY = os.environ.get("CANVA_API_KEY", "")

def generate_slides_via_canva(topic, slides_data, brand_template_id=None):
    """Generate slides using Canva API.
    Falls back to HTML/Playwright if Canva API is not available."""
    
    if not CANVA_KEY:
        print("⚠️ No CANVA_API_KEY. Falling back to HTML/Playwright carousel builder.")
        return _fallback_html_carousel(topic, slides_data)
    
    headers = {
        "Authorization": f"Bearer {CANVA_KEY}",
        "Content-Type": "application/json"
    }
    
    # Canva API: Create design from template
    payload = {
        "template_id": brand_template_id or "your_template_id",
        "title": f"Carousel: {topic}",
        "pages": []
    }
    
    for i, slide in enumerate(slides_data):
        page = {
            "elements": [
                {"type": "text", "content": slide.get("headline", ""), 
                 "position": {"x": 100, "y": 100}, "size": {"width": 880, "height": 200},
                 "style": {"fontSize": 44, "fontWeight": "bold", "color": "#f0ece4"}}
            ]
        }
        for j, pt in enumerate(slide.get("points", [])):
            page["elements"].append({
                "type": "text", "content": pt,
                "position": {"x": 100, "y": 350 + j * 80}, "size": {"width": 880, "height": 60},
                "style": {"fontSize": 20, "color": "rgba(240,236,228,0.8)"}
            })
        payload["pages"].append(page)
    
    try:
        req = urllib.request.Request(
            "https://api.canva.com/rest/v1/designs",
            data=json.dumps(payload).encode(),
            headers=headers, method="POST"
        )
        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read())
        design_id = result.get("id", "")
        print(f"✅ Canva design created: {design_id}")
        return design_id
    except urllib.error.HTTPError as e:
        print(f"❌ Canva API error: {e.code} {e.read().decode()[:200]}")
        return _fallback_html_carousel(topic, slides_data)

def _fallback_html_carousel(topic, slides_data):
    """Fallback: use Playwright HTML→PNG rendering."""
    print("Using HTML/Playwright fallback...")
    sys.path.insert(0, "/home/josh/Development/Projects/digitalmarketing/scripts")
    from build_carousel import build_from_slides
    return build_from_slides(topic, slides_data)

if __name__ == "__main__":
    # Test with sample data
    test_slides = [
        {"headline": "The AI Strategy Gap", "points": ["Most companies have AI vision decks", "Few have actually deployed anything", "The gap is execution, not strategy"]},
        {"headline": "Three Lenses to Apply AI", "points": ["What can I ship this week?", "Where is my bottleneck?", "Does this replace or augment?"]},
    ]
    generate_slides_via_canva("Test: AI Strategy", test_slides)
