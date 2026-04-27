import os
import httpx
from fastapi import FastAPI, Form, HTTPException, Request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

app = FastAPI(title="WhatsApp Gateway")

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.environ.get("TWILIO_WHATSAPP_NUMBER")

VOICE_API_URL = "http://voice-ai:8000/api/voice"

if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    twilio_client = None
    print("Warning: Twilio credentials not found.")

@app.post("/webhook")
async def twilio_webhook(request: Request):
    """
    Receives incoming messages from Twilio WhatsApp.
    """
    form_data = await request.form()
    incoming_msg = form_data.get('Body', '').strip()
    sender = form_data.get('From', '')

    print(f"Received WhatsApp message from {sender}: {incoming_msg}")

    # Forward the message to the internal Voice/Text AI pipeline
    ai_response = "I couldn't process that right now."
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(VOICE_API_URL, json={"text": incoming_msg})
            if resp.status_code == 200:
                data = resp.json()
                ai_response = data.get("response", "No response generated.")
            else:
                ai_response = f"Central Ops Error: {resp.status_code}"
    except Exception as e:
        print(f"Error reaching internal AI: {e}")
        ai_response = "Central Ops is currently offline."

    # Build the Twilio XML response
    resp = MessagingResponse()
    resp.message(ai_response)

    # Note: We return XML because Twilio webhooks expect TwiML format.
    from fastapi.responses import Response
    return Response(content=str(resp), media_type="application/xml")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "twilio_configured": twilio_client is not None}
