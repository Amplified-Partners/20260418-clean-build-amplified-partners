"""
Voice AI API Server
====================
FastAPI backend serving the voice pipeline with TickTick integration.

Endpoints:
- POST /api/voice - Accept audio or text, return audio response
- GET /api/notifications - Get pending notifications
- POST /api/notifications/dismiss - Dismiss a notification

Built: December 6th, 2025
Updated: December 11th, 2025 - Added TickTick integration
"""

import os
import io
import base64
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from voice_pipeline import VoicePipeline

import soundfile as sf
import numpy as np


from fastapi.middleware.cors import CORSMiddleware

# Initialize app
app = FastAPI(title="Voice AI", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
pipeline: Optional[VoicePipeline] = None

# In-memory notification queue
notifications = []


class TextInput(BaseModel):
    text: str


class Notification(BaseModel):
    id: str
    text: str
    type: str = "info"
    created_at: datetime


@app.on_event("startup")
async def startup():
    """Initialize pipeline on startup."""
    global pipeline
    
    pipeline = VoicePipeline(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
        cartesia_api_key=os.environ.get("CARTESIA_API_KEY"),
        ticktick_api_key=os.environ.get("TICKTICK_API_KEY"),
        voice_id=os.environ.get("CARTESIA_VOICE_ID")
    )
    
    ticktick_status = "✅ enabled" if os.environ.get("TICKTICK_API_KEY") else "❌ disabled"
    print(f"✅ Voice pipeline initialized (TickTick: {ticktick_status})")


@app.post("/api/voice")
async def process_voice(
    audio: Optional[UploadFile] = File(None),
    text_input: Optional[TextInput] = None
):
    """
    Process voice or text input, return audio response.
    Creates tasks in TickTick if detected.
    """
    global pipeline, notifications
    
    if not pipeline:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    user_text = None
    
    # Handle audio input
    if audio:
        with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as f:
            content = await audio.read()
            f.write(content)
            temp_path = f.name
        
        try:
            audio_data, sample_rate = sf.read(temp_path)
            if len(audio_data.shape) > 1:
                audio_data = audio_data.mean(axis=1)
            
            user_text = pipeline.transcribe(audio_data.astype(np.float32))
        finally:
            os.unlink(temp_path)
    
    # Handle text input
    elif text_input:
        user_text = text_input.text
    
    else:
        raise HTTPException(status_code=400, detail="No input provided")
    
    if not user_text or not user_text.strip():
        raise HTTPException(status_code=400, detail="Empty input")
    
    # Get Claude response (may include task data)
    response_text, task_data = pipeline.get_claude_response(user_text)
    
    # Create task if detected
    task_created = None
    if task_data and pipeline.ticktick:
        try:
            task_created = await pipeline.create_task(task_data)
            # Add notification for created task
            add_notification(
                f"✅ Task added: {task_data.get('title', 'Untitled')}",
                "success"
            )
        except Exception as e:
            print(f"Task creation failed: {e}")
            add_notification(f"⚠️ Couldn't create task: {str(e)}", "warning")
    
    # Generate audio
    audio_bytes = pipeline.text_to_speech(response_text)
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    
    # Save transcript
    pipeline.save_transcript(user_text, response_text)
    
    # Get pending notifications
    pending = [{"id": n.id, "text": n.text, "type": n.type} for n in notifications[:5]]
    
    return {
        "transcript": user_text,
        "response": response_text,
        "audio": audio_base64,
        "task_created": task_created,
        "notifications": pending
    }


@app.get("/api/notifications")
async def get_notifications():
    """Get all pending notifications."""
    return [
        {"id": n.id, "text": n.text, "type": n.type, "created_at": n.created_at}
        for n in notifications
    ]


@app.post("/api/notifications/{notification_id}/dismiss")
async def dismiss_notification(notification_id: str):
    """Dismiss a notification."""
    global notifications
    notifications = [n for n in notifications if n.id != notification_id]
    return {"status": "dismissed"}


def add_notification(text: str, type: str = "info"):
    """Add a notification to the queue."""
    global notifications
    notifications.append(Notification(
        id=str(uuid.uuid4()),
        text=text,
        type=type,
        created_at=datetime.now()
    ))
    # Keep only last 20 notifications
    notifications = notifications[-20:]


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint for Railway."""
    return {"status": "healthy", "ticktick": bool(os.environ.get("TICKTICK_API_KEY"))}


# Serve static files (the PWA)
app.mount("/", StaticFiles(directory="app", html=True), name="static")


def main():
    """Run the server."""
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )


if __name__ == "__main__":
    main()
