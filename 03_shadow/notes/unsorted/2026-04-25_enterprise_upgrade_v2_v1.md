---
title: "Enterprise Upgrade v2.0 - Summary"
id: "enterprise_upgrade_v2"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

# Enterprise Upgrade v2.0 - Summary

## Changes Applied

### 1. Vapi Assistant (Live on Vapi)
✅ **Updated Gemma v2 System Prompt**
- AI disclosure: Gemma confirms she's an AI when asked
- Word limit: 25 words max per response
- Emergency protocol: Gas → route to 0800 111 999
- GDPR compliance: Data notice when asked

### 2. Webhook Handler (Local - needs deploy)
✅ **Updated `/src/api/routes/webhooks.py`**
- Latency tracking (TTFA < 500ms target)
- Priority SMS templates (🚨 Emergency / ⚡ Urgent / 📞 Routine)
- Emergency keyword detection fallback
- Full metrics logging for compliance
- New endpoints: `/vapi/call-start`, `/vapi/speech-update`

### 3. SMS Templates
| Urgency | Emoji | Response Time |
|---------|-------|---------------|
| Emergency | 🚨 | IMMEDIATE |
| Urgent | ⚡ | 2 hours |
| Routine | 📞 | Convenience |

## To Deploy

```bash
cd ~/Documents/Baselayer/covered-ai-v2

# Check changes
git status
git diff src/api/routes/webhooks.py

# Commit
git add -A
git commit -m "Enterprise v2.0: latency tracking, priority SMS, compliance"

# Push (Railway auto-deploys)
git push origin main
```

## Verify Deployment

```bash
# Check health
curl https://covered-ai-production.up.railway.app/health

# Should return:
# {"status":"healthy","version":"2.0.0"}

# Check webhook health
curl https://covered-ai-production.up.railway.app/api/v1/webhooks/health

# Should return:
# {"status":"healthy","service":"webhooks","version":"2.0.0",...}
```

## Test Call

1. Call the Titan Plumbing number
2. Talk to Gemma
3. Check Railway logs for:
   - `📞 Vapi call complete webhook received`
   - `TTFA: XXXms`
   - `Urgency: routine/urgent/emergency`
4. Check Ralph receives SMS with correct priority emoji

## Metrics to Monitor

| Metric | Target | Alert |
|--------|--------|-------|
| TTFA | < 500ms | > 800ms |
| Lead capture | > 80% | < 60% |
| Emergency detection | 100% | Any miss |

## Files Changed

```
Modified:
- src/api/routes/webhooks.py (enterprise upgrade)

New (specs only, not deployed):
- /Documents/businessfactory/covered-ai-specs/
  ├── 01-gemma-system-prompt-v2.md
  ├── 02-webhook-handler-enterprise.md
  ├── 03-sms-notifications.md
  ├── 04-transcript-storage-compliance.md
  ├── 05-latency-monitoring.md
  └── src/ (standalone deployment option)
```

## Vapi Configuration (Applied)

- Assistant ID: `0630abf5-9bc3-4b54-b362-e212f1c133a0`
- Voice: Cartesia female (`79a125e8-cd45-4c13-8a67-188112f4dd22`)
- Model: GPT-4o-mini, temp 0.7, max 80 tokens
- First message: "Titan Plumbing, Gemma speaking. How can I help?"
- Server URL: `https://covered-ai-production.up.railway.app/api/v1/webhooks/vapi/call-complete`
