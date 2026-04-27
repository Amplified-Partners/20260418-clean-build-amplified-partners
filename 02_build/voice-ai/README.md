# Voice AI System

Voice-first AI assistant. Talk button. Text fallback. That's it.

## What This Does

1. You speak → Whisper transcribes
2. Transcript → Claude thinks
3. Response → Cartesia speaks back
4. Everything saved to Google Drive

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
CARTESIA_API_KEY=sk_car_...
CARTESIA_VOICE_ID=  # Optional - leave blank for default
```

### 3. Google Drive Setup (Optional)

For Drive sync, you need OAuth credentials:

1. Go to Google Cloud Console
2. Create project, enable Drive API
3. Create OAuth credentials (Desktop app)
4. Download as `credentials.json`
5. Run `python drive_sync.py` to authenticate

### 4. Run

```bash
# Start the server
python api_server.py
```

Open http://localhost:8000 in your browser.

On phone: Add to Home Screen for app-like experience.

## Files

```
voice_pipeline.py   - Core voice processing (Whisper → Claude → Cartesia)
daily_processor.py  - Extract insights from transcripts
drive_sync.py       - Sync to Google Drive
api_server.py       - FastAPI backend
app/                - PWA frontend
  index.html        - The UI (one button, one text box)
  manifest.json     - PWA manifest
  sw.js             - Service worker
```

## Usage

**Voice:** Hold the Talk button, speak, release.

**Text:** Type in the box, press Send.

**Notifications:** Completed tasks float up from bottom. Tap to dismiss.

## Daily Processing

Run at end of day to extract insights:

```bash
python daily_processor.py
```

This reads the day's transcripts and outputs:
- Tasks identified
- Ideas captured
- Decisions made
- Sentiment patterns
- Tomorrow's brief

## Sync to Drive

```bash
python drive_sync.py
```

Creates structure:
```
VoiceAI/
  transcripts/raw/
  transcripts/processed/
  insights/daily/
  insights/weekly/
```

---

Built: December 6th, 2025
