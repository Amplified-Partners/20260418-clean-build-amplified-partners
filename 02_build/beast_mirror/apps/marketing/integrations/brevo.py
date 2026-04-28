"""
Brevo (formerly Sendinblue) email integration.
Handles transactional and marketing emails with DISC personalisation.
"""
import os
import logging
from dataclasses import dataclass
from typing import Optional
import httpx

logger = logging.getLogger("marketing.brevo")

BREVO_API = "https://api.brevo.com/v3"


@dataclass
class EmailMessage:
    to_email: str
    to_name: str
    subject: str
    html_content: str
    text_content: str
    tag: str = "marketing-engine"
    disc_type: str = ""
    sequence_step: int = 1


class BrevoClient:
    """Brevo email client. Uses httpx directly — no SDK needed."""

    def __init__(self):
        self.api_key = os.environ.get("BREVO_API_KEY", "")
        if not self.api_key:
            logger.warning("BREVO_API_KEY not set — email will be logged only")
        self._client = httpx.AsyncClient(
            base_url=BREVO_API,
            headers={"api-key": self.api_key, "Content-Type": "application/json"},
            timeout=30.0,
        )

    async def send(self, msg: EmailMessage) -> dict:
        """Send a transactional email."""
        if not self.api_key:
            logger.info(f"[DRY RUN] Email to {msg.to_email}: {msg.subject}")
            return {"messageId": "dry-run", "status": "logged"}

        payload = {
            "sender": {"name": "Ewan @ Amplified Partners", "email": "hello@amplifiedpartners.ai"},
            "to": [{"email": msg.to_email, "name": msg.to_name}],
            "subject": msg.subject,
            "htmlContent": msg.html_content,
            "textContent": msg.text_content,
            "tags": [msg.tag],
            "headers": {
                "X-DISC-Type": msg.disc_type,
                "X-Sequence-Step": str(msg.sequence_step),
            },
        }

        try:
            resp = await self._client.post("/smtp/email", json=payload)
            resp.raise_for_status()
            data = resp.json()
            logger.info(f"Email sent to {msg.to_email}: messageId={data.get('messageId')}")
            return data
        except httpx.HTTPStatusError as e:
            logger.error(f"Brevo API error {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            raise

    async def send_sequence_email(
        self,
        to_email: str,
        to_name: str,
        step: str,
        disc_type: str,
        context: dict,
    ) -> dict:
        """Send one step of the 4-email Amplified sequence."""
        templates = {
            "here_is_the_problem": {
                "subject": "The real reason your {pain_point} is harder than it needs to be",
                "html": """<p>Hi {name},</p>
<p>{problem_description}</p>
<p>You're not doing anything wrong. The system just wasn't built for businesses like yours.</p>
<p>I'll share more on this shortly.</p>
<p>— Ewan</p>
<p><small>Amplified Partners · <a href="{{unsubscribe}}">Unsubscribe</a></small></p>""",
            },
            "here_is_the_solution": {
                "subject": "Here's how to actually fix {pain_point}",
                "html": """<p>Hi {name},</p>
<p>Yesterday I talked about {pain_point}.</p>
<p>Here's the complete fix — no strings:</p>
<p>{solution_steps}</p>
<p>Try it. If it helps, brilliant. If you need a hand implementing it, you know where I am.</p>
<p>— Ewan</p>
<p><small>Amplified Partners · <a href="{{unsubscribe}}">Unsubscribe</a></small></p>""",
            },
            "do_you_need_help": {
                "subject": "Quick check-in",
                "html": """<p>Hi {name},</p>
<p>Hope the {pain_point} tip was useful.</p>
<p>If you want to take it further — pick four words you'll remember and reply with them.</p>
<p>That's it. No forms, no calls, no commitment. Just four words.</p>
<p>I'll follow up and we'll figure out what actually helps you.</p>
<p>— Ewan</p>
<p><small>Amplified Partners · <a href="{{unsubscribe}}">Unsubscribe</a></small></p>""",
            },
            "here_is_help": {
                "subject": "Re: your four words",
                "html": """<p>Hi {name},</p>
<p>Got your four words.</p>
<p>{personalised_response}</p>
<p>— Ewan</p>
<p><small>Amplified Partners · <a href="{{unsubscribe}}">Unsubscribe</a></small></p>""",
            },
        }

        template = templates.get(step, templates["here_is_the_problem"])
        subject = template["subject"].format(**context, name=to_name)
        html = template["html"].format(**context, name=to_name)
        text = html.replace("<p>", "").replace("</p>", "\n").replace("<small>", "").replace("</small>", "")

        return await self.send(EmailMessage(
            to_email=to_email,
            to_name=to_name,
            subject=subject,
            html_content=html,
            text_content=text,
            tag=f"sequence-{step}",
            disc_type=disc_type,
            sequence_step=["here_is_the_problem", "here_is_the_solution", "do_you_need_help", "here_is_help"].index(step) + 1,
        ))

    async def close(self):
        await self._client.aclose()
