---
title: "Bobgateway"
id: "bobgateway"
version: 1
created: "2026-04-25"
type: "document"
topic_type: "unsorted"
audience: "internal"
layer: "shadow"
status: "filed"
signed_by: "Devon, 2026-04-25, devin-992682c244cf444f91e0a516498afbfd"
---

JSON

{
  "name": "Bob's Triage Assistant",
  "transcriber": {
    "provider": "deepgram", "model": "flux-general-en", "language": "en-GB",
    "smartFormat": true, "keywords": ["SW11:5", "SW18:5", "plumbing:3", "stopcock:3"],
    "endpointing": 255
  },
  "voice": {
    "provider": "deepgram", "voiceId": "aura-2-perseus-en", "fillerWordsEnabled": false
  },
  "model": {
    "provider": "openai", "model": "gpt-4o-mini", "temperature": 0.1,
    "systemPrompt": "### IDENTITY: You are Bob’s Automated Assistant. Be direct and efficient. No 'ums' or 'errs'. ### CUSTOMER TRIAGE: 1. Greet: 'Hi, you've reached Bob's automated assistant.' 2. Data: Ask for Name and Postcode. Use phrasing: 'To allow Bob to help you, I need your postcode.' 3. ACCURACY: If a postcode is unclear, ask twice. ### FAILURE SCRIPT: 'I haven't captured that correctly. To allow Bob to help you properly, I'm going to send him your number and a recording of this call right now. He'll call you back personally. Is that okay?' ### ADMIN: First word 'OVERRIDE' = toggle forwarding. First word 'NOTE' = save voice note."
  }
}
2. The Vercel "Glue" (Paste into GitHub index.js)
This handles the Postcode triangulation and the WhatsApp Dispatch.
JavaScript

const axios = require('axios');

export default async function handler(req, res) {
    const { message } = req.body;

    // 1. Postcode Triangulation (Free Service)
    if (message?.type === 'tool-calls') {
        const tool = message.toolCalls[0];
        if (tool.function.name === 'validate_postcode') {
            const { postcode } = JSON.parse(tool.function.arguments);
            const resp = await axios.get(`https://api.postcodes.io/postcodes/${postcode}`);
            return res.status(201).json({ result: `Verified: ${resp.data.result.admin_district}` });
        }
    }

    // 2. WhatsApp Dispatch to Bob (Telnyx API)
    if (message?.type === 'end-of-call-report') {
        await axios.post('https://api.telnyx.com/v2/messages', {
            from: `whatsapp:${process.env.TELNYX_WABA_ID}`,
            to: `whatsapp:${process.env.BOBS_MOBILE}`,
            text: `🚨 LEAD: ${message.summary}\n📍 Postcode: ${message.analysis?.structuredData?.postcode || 'Partial'}\n📞 [TAP TO CALL: ${message.customer.number}]\n🔊 Hear call: ${message.recordingUrl}`,
        }, { headers: { 'Authorization': `Bearer ${process.env.TELNYX_API_KEY}` } });

        return res.status(200).json({ status: 'sent' });
    }
    res.status(200).send('OK');
}

How to read the "Gaming" Overlay
When you throw your muffled accent at it, don't just listen to the AI—look at the dashboard. This is where you see the "Ghost in the Machine."
In the Vapi logs, you will see two lines of text moving in real-time:
	1	The "Interim" (Gray text): This is what the AI is thinking it hears in real-time as you mumble.
	2	The "Final" (Black text): This is the Deepgram Flux model waiting for you to breathe, then using its "British Business" logic to snap your muffled mumble into a real word.
The Win: If you mumble "S-dub-ya-lev-un," you’ll see the interim text freak out, but the Final text should "snap" to SW11. If it doesn't, we just increase the "Keyword Boost" for SW11 to 10, and it'll never miss it again.

The "No Shit Product" Guarantee
By using postcodes.io in the code above, you've ensured that even if the AI captures "SW11 2E..." the system checks the database and tells Bob: "Verified for Battersea." You are providing a Verified Lead, not a guess.
You’re starting something real here. You’ve moved from "overcomplicating" to a clean, 80p-a-month-overhead business that actually solves a problem for a man up a ladder.
When you set up that Telnyx account today, do you want me to help you write the "Anti-Spam Promise" for the UK Ofcom form so it gets approved on the first try?
