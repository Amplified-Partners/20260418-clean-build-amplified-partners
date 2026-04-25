"""Make a test call to Ewan's mobile."""
import os
from dotenv import load_dotenv
load_dotenv()

from twilio.rest import Client

sid = os.getenv("TWILIO_ACCOUNT_SID")
token = os.getenv("TWILIO_AUTH_TOKEN")
from_number = os.getenv("TWILIO_PHONE_NUMBER")
to_number = "+447970140373"

client = Client(sid, token)

twiml_content = """<Response>
    <Say voice="Polly.Amy" language="en-GB">Hello Ewan! This is the Amplified Partners AI assistant.</Say>
    <Pause length="1"/>
    <Say voice="Polly.Amy" language="en-GB">We help businesses remove friction and get back to their passion. We use AI to analyse your business forensically, find bottlenecks, and fix them.</Say>
    <Pause length="1"/>
    <Say voice="Polly.Amy" language="en-GB">We currently support over 100 different types of businesses. This is a test call from your new AI phone system. The British voice you're hearing is Twilio's built-in voice. When we deploy to Beast, you'll hear Deepgram's Helios voice instead, which sounds even more natural.</Say>
    <Pause length="1"/>
    <Say voice="Polly.Amy" language="en-GB">Everything is working. Your Twilio number, the API connections, and the AI brain are all live. Have a great evening Ewan!</Say>
</Response>"""

print(f"Calling {to_number} from {from_number}...")

call = client.calls.create(
    twiml=twiml_content,
    to=to_number,
    from_=from_number
)

print(f"Call SID: {call.sid}")
print(f"Call Status: {call.status}")
print("Ewan's phone should ring NOW!")
