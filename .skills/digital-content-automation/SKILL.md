---
name: digital-content-automation
description: "Automated multi-platform content pipeline for a one-person business. Generate → Review → Approve → Post workflow across LinkedIn, YouTube, Facebook, WeChat."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Content, Automation, Digital-Marketing, LinkedIn, YouTube, Social-Media]
    related_skills: [overstory, notion, linkedin-profile-optimizer]
---

# Digital Content Automation Pipeline

## Overview

Automated content generation pipeline for a one-person AI-augmented advisory business. Three content pillars feed a multi-platform engine with a review-then-post approval workflow.

## Content Pillars

| Pillar | Focus | Frequency |
|--------|-------|-----------|
| **AI Strategy & Advisory** | Executive AI insights, decision frameworks | Mon, Wed |
| **Executive Coaching** | Leadership, cross-border wisdom | Fri |
| **Wisdom & Motivation** | Sun Tzu in business, Stoicism, quotes | Sat, Sun |

## Pipeline Architecture

```
Content Engine (DeepSeek API)
    │
    ├── Generates 4 formats per topic:
    │     LinkedIn (200 words, Hook→Explanation→Example→CTA)
    │     YouTube Shorts (60-sec script with [VISUAL] cues)
    │     Facebook (casual, emojis, question)
    │     WeChat (Chinese + English, professional)
    │
    ├── Saves to review/pending/
    │
    ├── Hermes presents for CEO approval
    │
    └── On approval → post to channel
```

## Workflow

1. **Content Engine** (cron Mon/Wed/Fri 9AM SGT) generates multi-format content
2. **Review Queue** — content lands in `review/pending/` folder
3. **CEO Review** — Hermes presents the post for approval in the conversation
4. **Approval** — CEO says yes → Hermes posts manually or provides copy-paste text
5. **Archive** — approved content moves to `review/approved/`

## Directory Structure

```
digitalmarketing/
├── scripts/
│   ├── content_engine.py      # Multi-format generator (DeepSeek API)
│   ├── market_intel.py         # Trend scanner (HN + Reddit)
│   ├── daily_brief.py          # CEO summary
│   ├── generate_by_schedule.py # Schedule-aware generator
│   └── linkedin_poster.py      # Auto-post via CDP (unreliable)
├── review/
│   ├── pending/                # Awaiting CEO approval
│   └── approved/               # Posted content archive
├── CONTENT-SCHEDULE.md         # 4-week content calendar
├── .overstory/agent-defs/      # Overstory agent definitions
└── .overstory/specs/           # Task specifications
```

## Cron Jobs

| Job | Schedule | Script |
|-----|----------|--------|
| Market Intel | Every 2h | `market_intel.py` |
| Content Engine | Mon/Wed/Fri 9AM | `content_engine.py` |
| Daily Brief | 8AM daily | `daily_brief.py` |

## Channels

| Channel | Format | Current Status |
|---------|--------|---------------|
| LinkedIn | Text + graphic | Manual post (auto-gen drafts) |
| YouTube | Shorts + long-form | Channel exists, needs setup |
| Facebook | Casual repurpose | Content generated, not posted |
| WeChat | Chinese + English | Content generated, not posted |

## Key Lessons

- **Short posts > long stories** — 3-5 sentence tips outperform essays
- **Review before post** — CEO must approve before anything goes live
- **Auto-post via CDP is unreliable** — LinkedIn's React UI resists automation
- **Content Engine generates all 4 formats** from one topic call
- **Create graphics alongside text** — visual posts get 3x engagement
- **Store in Git** — all content, scripts, and schedule are version-controlled
