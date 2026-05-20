# Content Automation Pipeline — Tool Integration Status

## Current Pipeline

```
DeepSeek API (Content Engine)
    │
    ├── Text content → review/pending/ → CEO approves → manual post
    │
    ├── Carousel slides → HTML/Playwright → PNG slides → LinkedIn
    │                     (Canva API - pending key setup)
    │
    ├── Avatar videos → HeyGen API → MP4 → YouTube/Short
    │                   (waiting for Instant Avatar creation)
    │
    └── Image gen → Canva API → thumbnails/carousel backgrounds
                    (pending key setup)
```

## Tool Status

| Tool | Status | API Key? | Next Step |
|------|--------|----------|-----------|
| **Content Engine** | ✅ Live on cron | DeepSeek ✅ | Auto-generates Mon/Wed/Fri |
| **Carousel builder** | ✅ Live (Playwright) | None needed | HTML→PNG fallback works |
| **Canva API** | ⏳ Script ready | Not set | Boss needs to create Canva API key |
| **HeyGen API** | ⏳ Script ready | Not set | Record avatar video first |
| **LinkedIn poster** | ⏳ Script ready | N/A (CDP) | Unreliable, manual for now |
| **Opus Clip** | ❌ Not needed yet | N/A | Wait for long-form video |
| **Higgsfield** | ❌ Not needed yet | N/A | Evaluate if Canva isn't enough |

## API Keys Needed

1. **Canva** — https://www.canva.com/developers/ → Create app → API key
2. **HeyGen** — https://app.heygen.com → Settings → API → Generate key
3. After recording Instant Avatar: note avatar_id from dashboard

## Quick Start

```bash
# Generate carousel from topic (works now)
DS_API_KEY="$DS_API_KEY" python3 ~/.hermes/scripts/build_carousel.py "Topic" 3

# Generate text content (works now)
DS_API_KEY="$DS_API_KEY" python3 ~/.hermes/scripts/content_engine.py "Topic"

# Generate avatar video (after keys + avatar setup)
HEYGEN_API_KEY="$HEYGEN_API_KEY" python3 ~/.hermes/scripts/heygen_integration.py "Script text"

# Generate Canva slides (after API key)
CANVA_API_KEY="$CANVA_API_KEY" python3 ~/.hermes/scripts/canva_integration.py "Topic"
```
