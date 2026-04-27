"""
Voice Pipeline for Ewan's Voice-First AI System
================================================
Whisper (transcription) → Claude (intelligence) → Cartesia (voice output)
+ TickTick task creation

Built: December 6th, 2025
Updated: December 11th, 2025 - Added TickTick integration
"""

import os
import io
import re
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# API imports
import anthropic
import openai
from cartesia import Cartesia

# Audio handling
import soundfile as sf
import numpy as np

# Task management
from ticktick_client import TickTickClient, parse_due_date, parse_priority


class VoicePipeline:
    """
    Two-way voice conversation with Claude + task management.
    
    Flow:
    1. Record user audio
    2. Transcribe with Whisper
    3. Send to Claude, get response
    4. If task detected, create in TickTick
    5. Convert response to speech with Cartesia
    6. Play audio back
    """
    
    def __init__(
        self,
        openai_api_key: str,
        anthropic_api_key: str,
        cartesia_api_key: str,
        ticktick_api_key: str = None,
        voice_id: str = None,
        sample_rate: int = 44100
    ):
        # Initialize clients
        self.openai_client = openai.OpenAI(api_key=openai_api_key)
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key)
        self.cartesia_client = Cartesia(api_key=cartesia_api_key)
        
        # TickTick (optional)
        self.ticktick = TickTickClient(ticktick_api_key) if ticktick_api_key else None
        
        # Audio settings
        self.sample_rate = sample_rate
        self.voice_id = voice_id or "a0e99841-438c-4a64-b679-ae501e7d6091"
        
        # Conversation history
        self.conversation_history = []
        
        # Storage paths
        self.transcript_dir = Path("transcripts/raw")
        self.transcript_dir.mkdir(parents=True, exist_ok=True)
        
        # Tasks created this session (for notifications)
        self.created_tasks = []
    
    def transcribe(self, audio: np.ndarray) -> str:
        """Transcribe audio using Whisper API."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            sf.write(f.name, audio, self.sample_rate)
            temp_path = f.name
        
        try:
            with open(temp_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )
            return transcript.strip()
        finally:
            os.unlink(temp_path)
    
    def get_claude_response(self, user_message: str) -> Tuple[str, Optional[dict]]:
        """
        Send message to Claude and get response.
        Returns (response_text, task_data) where task_data is None or a dict.
        """
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # System prompt with task creation capability
        system_prompt = """You are Ewan's AI assistant, speaking through voice.

Your tone:
- Direct, no waffle
- Warm but not sycophantic  
- You're a collaborator, not a servant
- You have initiative within the frame Ewan sets

Keep responses conversational and concise - this is spoken, not written.
No bullet points, no headers, no formatting. Just speak naturally.

TASK CREATION:
You can create tasks in TickTick. When Ewan asks you to add a task, remind him of something, or schedule something, include a JSON block at the END of your response like this:

```task
{"title": "Task title here", "due": "tomorrow", "priority": "normal"}
```

Due can be: "today", "tomorrow", "monday", "tuesday", etc., "in 3 days", "next week", or omit for no due date.
Priority can be: "low", "normal", "high", or "urgent".

Only include the task block when Ewan explicitly wants to create/add a task or reminder. Don't create tasks for casual mentions.

Examples of when to create tasks:
- "Add a task to follow up with John"
- "Remind me to call the dentist tomorrow"  
- "I need to finish the proposal by Friday, add that"
- "Put on my list: review the contracts"

Examples of when NOT to create tasks:
- "I should probably call John sometime" (too vague, no explicit request)
- "What do I have to do today?" (asking, not creating)

Your spoken response should confirm the task naturally, like "Done, I've added that for tomorrow" or "Got it, that's on your list now."
"""

        response = self.anthropic_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=system_prompt,
            messages=self.conversation_history
        )
        
        full_response = response.content[0].text
        
        # Parse task if present
        task_data = None
        spoken_response = full_response
        
        task_match = re.search(r'```task\s*\n?(.+?)\n?```', full_response, re.DOTALL)
        if task_match:
            try:
                task_data = json.loads(task_match.group(1))
                # Remove task block from spoken response
                spoken_response = re.sub(r'```task\s*\n?.+?\n?```', '', full_response, flags=re.DOTALL).strip()
            except json.JSONDecodeError:
                pass
        
        # Add to history (without task block)
        self.conversation_history.append({
            "role": "assistant", 
            "content": spoken_response
        })
        
        return spoken_response, task_data
    
    async def create_task(self, task_data: dict) -> dict:
        """Create a task in TickTick."""
        if not self.ticktick:
            return None
        
        title = task_data.get("title", "Untitled task")
        due_str = task_data.get("due", "")
        priority_str = task_data.get("priority", "normal")
        
        # Parse due date
        due_date = parse_due_date(due_str) if due_str else None
        
        # Parse priority
        priority_map = {"low": 1, "normal": 0, "high": 3, "urgent": 5}
        priority = priority_map.get(priority_str.lower(), 0)
        
        # Create task
        created = await self.ticktick.create_task(
            title=title,
            due_date=due_date,
            priority=priority
        )
        
        self.created_tasks.append(created)
        return created
    
    def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using Cartesia."""
        audio_bytes = b""
        
        for chunk in self.cartesia_client.tts.bytes(
            model_id="sonic-2",
            transcript=text,
            voice={"mode": "id", "id": self.voice_id},
            language="en",
            output_format={
                "container": "wav",
                "sample_rate": self.sample_rate,
                "encoding": "pcm_f32le"
            }
        ):
            audio_bytes += chunk
        
        return audio_bytes
    
    def save_transcript(self, user_text: str, assistant_text: str):
        """Save conversation turn to transcript file."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        daily_file = self.transcript_dir / f"{date_str}.md"
        
        with open(daily_file, "a") as f:
            f.write(f"\n## {timestamp}\n\n")
            f.write(f"**Ewan:** {user_text}\n\n")
            f.write(f"**Claude:** {assistant_text}\n\n")
            f.write("---\n")


def main():
    """Run the voice pipeline."""
    pipeline = VoicePipeline(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
        cartesia_api_key=os.environ.get("CARTESIA_API_KEY"),
        ticktick_api_key=os.environ.get("TICKTICK_API_KEY"),
        voice_id=os.environ.get("CARTESIA_VOICE_ID")
    )
    
    print("Voice Pipeline initialized with TickTick integration")


if __name__ == "__main__":
    main()
