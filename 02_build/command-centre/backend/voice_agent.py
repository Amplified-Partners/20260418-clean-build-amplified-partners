"""
Amplified Partners — AI Telephone Assistant
TwiML Gather + Say + Claude Haiku 3.5 (optimised for speed)

Architecture:
  Call → Twilio → /incoming-call → TwiML <Say> greeting + <Gather> input
  Caller speaks → Twilio STT → /respond → Claude → TwiML <Say> response + <Gather>
  Loop until caller hangs up or says goodbye.

This uses Twilio's native TwiML — no WebSockets needed.
Works with any Twilio account. Battle-tested approach.

Run: uvicorn voice_agent:app --host 0.0.0.0 --port 8080
"""

import os
import json
import logging
import hashlib
import time
from typing import Optional

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import Response
from dotenv import load_dotenv
import httpx

load_dotenv()

# ============================================================
# Configuration
# ============================================================

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

CLAUDE_MODEL = "claude-3-haiku-20240307"

# Twilio TTS settings
# Google Neural2-B = British male, warm and natural
TTS_VOICE = "Google.en-GB-Neural2-B"
TTS_LANGUAGE = "en-GB"

# Speech recognition hints — guide STT toward expected words
SPEECH_HINTS = "Ewan, Amplified, Partners, callback, plumber, booking, emergency, message, appointment, quote, leak, boiler, heating"

# ============================================================
# System Prompt
# ============================================================

SYSTEM_PROMPT = """You are the telephone assistant for Amplified Partners.
You answer calls, help callers, and take messages.

TONE:
- Warm, interested, and professional — the way a good colleague would speak to a client
- NOT robotic or corporate. NOT overly casual like "alright mate"
- Think: friendly business conversation. Helpful and human, but still professional
- You genuinely want to help the caller

CRITICAL FORMATTING RULES:
- Keep responses SHORT: one to two sentences maximum. Be concise
- Do NOT use asterisks, bullet points, numbered lists, or any markdown
- Do NOT use colons followed by lists
- Write in plain conversational English only
- Spell out all numbers: say "twenty" not "20"
- No special characters at all, just plain text
- This text will be read aloud, so write the way people actually talk
- Always end with a brief question to keep the conversation going

CONVERSATION RULES:
- If someone asks what Amplified Partners does, say "The best way to find out about us is to visit our website at www.amplifiedpartners.ai. All the information is there. Is there anything else I can help with?"
- Never pretend to be human. If asked, say "I am the AI telephone assistant for Amplified Partners"
- If the caller asks to speak to Ewan or a real person, say "Ewan is busy right now, but I can take a message and make sure he gets back to you. Can I take your name and number?"
- If you cannot help, offer to take a message for Ewan
- For emergencies, say "If this is an emergency, please hang up and call nine nine nine"
- Take the caller's name, number, and a brief description of what they need
- If the caller says goodbye, respond warmly and include the EXACT phrase "END_CALL" at the very end

{brain_context}
"""


# ============================================================
# FalkorDB Business Brain
# ============================================================

def get_brain_context() -> str:
    """Query FalkorDB for business context."""
    try:
        from falkordb import FalkorDB
        host = os.getenv("FALKORDB_HOST", "falkordb")
        port = int(os.getenv("FALKORDB_PORT", "6379"))
        db = FalkorDB(host=host, port=port)
        graph = db.select_graph('amplified_brain')

        parts = []

        try:
            result = graph.query("MATCH (m:AIMemory) RETURN m.key, m.value LIMIT 10")
            if result.result_set:
                memories = [f"{row[0]}: {row[1]}" for row in result.result_set]
                parts.append("Key Principles: " + ". ".join(memories))
        except Exception:
            pass

        try:
            result = graph.query("MATCH (f:FrictionPoint) RETURN f.name LIMIT 5")
            if result.result_set:
                frictions = [row[0] for row in result.result_set]
                parts.append(f"Common friction points we fix: {', '.join(frictions)}")
        except Exception:
            pass

        if parts:
            return "BUSINESS CONTEXT: " + " | ".join(parts)
        return ""

    except Exception as e:
        logger.warning(f"FalkorDB: {e}")
        return ""


# ============================================================
# FastAPI App
# ============================================================

app = FastAPI(title="Amplified Voice Agent")
logger = logging.getLogger("voice_agent")
logging.basicConfig(level=logging.INFO)

brain_context = ""
# In-memory conversation store: CallSid → list of messages
conversations: dict = {}


@app.on_event("startup")
async def startup():
    global brain_context
    brain_context = get_brain_context()
    logger.info(f"Brain context loaded: {len(brain_context)} chars")


# ============================================================
# Claude LLM
# ============================================================

async def get_claude_response(messages: list) -> str:
    """Get a response from Claude for the conversation."""
    system = SYSTEM_PROMPT.format(brain_context=brain_context)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": CLAUDE_MODEL,
                    "max_tokens": 150,
                    "system": system,
                    "messages": messages,
                },
                timeout=15,
            )

            if response.status_code == 200:
                result = response.json()
                text = result["content"][0]["text"]
                # Strip any markdown that might slip through
                text = text.replace("*", "").replace("#", "").replace("`", "")
                return text
            else:
                logger.error(f"Claude {response.status_code}: {response.text[:200]}")
                return "I'm sorry, I'm having a little trouble at the moment. Can I take your name and number and get someone to call you back?"

        except Exception as e:
            logger.error(f"Claude error: {e}")
            return "I'm sorry, I'm having a little trouble at the moment. Can I take your name and number and get someone to call you back?"


def escape_xml(text: str) -> str:
    """Escape text for use in XML/TwiML."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


# ============================================================
# Twilio: Incoming call → Greeting
# ============================================================

@app.post("/incoming-call")
async def handle_incoming_call(request: Request):
    """
    Twilio webhook for incoming calls.
    Returns TwiML that greets the caller and listens for speech.
    """
    form_data = await request.form()
    caller = form_data.get("From", "Unknown")
    called = form_data.get("To", "Unknown")
    call_sid = form_data.get("CallSid", "unknown")

    logger.info(f"📞 Incoming call: {caller} → {called} (SID: {call_sid})")

    # Initialize conversation
    conversations[call_sid] = []

    # Build respond URL using the same host
    host = request.headers.get("host", "voice.beast.amplifiedpartners.ai")
    scheme = "https" if "443" in str(request.url) or "https" in str(request.url) else request.url.scheme
    respond_url = f"https://{host}/respond"

    greeting = "Hi, I am the telephone assistant for Amplified Partners. How can I help you today?"

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}">{greeting}</Say>
    <Gather input="speech" 
            action="{respond_url}" 
            method="POST" 
            speechTimeout="3" 
            timeout="10"
            language="{TTS_LANGUAGE}"
            enhanced="true"
            hints="{SPEECH_HINTS}"
            speechModel="phone_call">
        <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}"></Say>
    </Gather>
    <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}">Are you still there? Take your time, I'm listening.</Say>
    <Gather input="speech" 
            action="{respond_url}" 
            method="POST" 
            speechTimeout="3" 
            timeout="15"
            language="{TTS_LANGUAGE}"
            enhanced="true"
            hints="{SPEECH_HINTS}"
            speechModel="phone_call">
        <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}"></Say>
    </Gather>
    <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}">I haven't heard from you, so I'll let you go. Feel free to call back anytime on oh one nine one, seven four three, three five five eight. Goodbye!</Say>
</Response>"""

    logger.info(f"Greeting sent, respond URL: {respond_url}")
    return Response(content=twiml, media_type="application/xml")


# ============================================================
# Twilio: Handle speech input → Claude → Response
# ============================================================

@app.post("/respond")
async def handle_response(request: Request):
    """
    Twilio calls this after <Gather> captures speech.
    We send it to Claude and return a TwiML response.
    """
    form_data = await request.form()
    speech = form_data.get("SpeechResult", "")
    call_sid = form_data.get("CallSid", "unknown")
    caller = form_data.get("From", "Unknown")

    logger.info(f"🎤 Caller said: '{speech}' (SID: {call_sid})")

    # Get or create conversation history
    if call_sid not in conversations:
        conversations[call_sid] = []

    history = conversations[call_sid]

    # Add the user's speech
    history.append({"role": "user", "content": speech})

    # Keep history manageable (last 20 turns)
    if len(history) > 20:
        history[:] = history[-20:]

    # Get Claude's response
    ai_response = await get_claude_response(history)

    logger.info(f"🤖 AI responds: '{ai_response[:100]}'")

    # Add to history
    history.append({"role": "assistant", "content": ai_response})

    # Check if call should end
    should_end = "END_CALL" in ai_response
    ai_response = ai_response.replace("END_CALL", "").strip()

    # Build respond URL
    host = request.headers.get("host", "voice.beast.amplifiedpartners.ai")
    respond_url = f"https://{host}/respond"

    escaped = escape_xml(ai_response)

    if should_end:
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}">{escaped}</Say>
    <Hangup/>
</Response>"""
    else:
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}">{escaped}</Say>
    <Gather input="speech" 
            action="{respond_url}" 
            method="POST" 
            speechTimeout="3" 
            timeout="15"
            language="{TTS_LANGUAGE}"
            enhanced="true"
            hints="{SPEECH_HINTS}"
            speechModel="phone_call">
        <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}"></Say>
    </Gather>
    <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}">Are you still there? Take your time, I'm listening.</Say>
    <Gather input="speech" 
            action="{respond_url}" 
            method="POST" 
            speechTimeout="3" 
            timeout="15"
            language="{TTS_LANGUAGE}"
            enhanced="true"
            hints="{SPEECH_HINTS}"
            speechModel="phone_call">
        <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}"></Say>
    </Gather>
    <Say voice="{TTS_VOICE}" language="{TTS_LANGUAGE}">I haven't heard from you, so I'll let you go. Feel free to call back anytime on oh one nine one, seven four three, three five five eight. Goodbye!</Say>
</Response>"""

    return Response(content=twiml, media_type="application/xml")


# ============================================================
# Health check
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "architecture": "twiml-gather-say",
        "anthropic": bool(ANTHROPIC_API_KEY),
        "twilio": bool(TWILIO_ACCOUNT_SID),
        "llm": CLAUDE_MODEL,
        "tts_voice": TTS_VOICE,
        "brain_context_loaded": len(brain_context) > 0,
        "active_calls": len(conversations),
    }


# ============================================================
# Test endpoint
# ============================================================

@app.post("/test-claude")
async def test_claude(request: Request):
    """Test Claude response."""
    body = await request.json()
    text = body.get("text", "What services do you offer?")
    response = await get_claude_response([{"role": "user", "content": text}])
    return {"response": response}


# ============================================================
# Cleanup old conversations (prevent memory leak)
# ============================================================

@app.on_event("startup")
async def cleanup_task():
    """Periodically clean up old conversations."""
    async def cleanup():
        while True:
            await asyncio.sleep(3600)  # Every hour
            old = list(conversations.keys())
            for sid in old:
                conversations.pop(sid, None)
            logger.info(f"Cleaned up {len(old)} old conversations")
    import asyncio
    asyncio.create_task(cleanup())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
