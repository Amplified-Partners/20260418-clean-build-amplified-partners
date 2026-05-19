"""Brevo adapter — real email path, dry-run by default.

Connects to Brevo (formerly Sendinblue) transactional email API.
Dry-run mode simulates the send and records what would happen.
Live mode requires an explicit API key AND the artifact must be in
'sent' state (i.e. it passed guardrails, dry-run, and got approval).

The adapter never forks the marketing_consumer schema — it reads from
MarketingArtifact and emits VellumEvents for every action.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

import requests

from marketing_consumer.models import MarketingArtifact

log = logging.getLogger("amplified.marketing.brevo")


# ---------------------------------------------------------------------------
# Brevo configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BrevoConfig:
    """Configuration for Brevo transactional email.

    api_key: Brevo API key. Empty string = dry-run only.
    sender_email: From address for transactional emails.
    sender_name: Display name for sender.
    dry_run: If True (default), never actually send.
    api_url: Brevo API endpoint.
    """

    api_key: str = ""
    sender_email: str = "noreply@amplifiedpartners.ai"
    sender_name: str = "Amplified Partners"
    dry_run: bool = True
    api_url: str = "https://api.brevo.com/v3/smtp/email"

    @property
    def is_live(self) -> bool:
        return bool(self.api_key.strip()) and not self.dry_run


# ---------------------------------------------------------------------------
# Send result
# ---------------------------------------------------------------------------


@dataclass
class BrevoSendResult:
    """Result of a Brevo send attempt."""

    sent: bool
    dry_run: bool
    message_id: str
    status_code: int
    detail: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc),
    )
    request_payload: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Payload builder
# ---------------------------------------------------------------------------


def build_payload(
    artifact: MarketingArtifact,
    *,
    config: BrevoConfig,
    to_email: str,
    to_name: str = "",
) -> dict[str, Any]:
    """Build the Brevo transactional email payload from a MarketingArtifact.

    The payload shape follows Brevo's v3 SMTP API:
    https://developers.brevo.com/reference/sendtransacemail
    """
    return {
        "sender": {
            "email": config.sender_email,
            "name": config.sender_name,
        },
        "to": [
            {
                "email": to_email,
                "name": to_name,
            },
        ],
        "subject": artifact.title,
        "htmlContent": artifact.content,
        "tags": [
            f"artifact:{artifact.artifact_id}",
            f"channel:{artifact.channel}",
            f"brain_packet:{artifact.brain_packet_id}",
        ],
    }


# ---------------------------------------------------------------------------
# Send (dry-run or live)
# ---------------------------------------------------------------------------


def send_email(
    artifact: MarketingArtifact,
    *,
    config: BrevoConfig,
    to_email: str,
    to_name: str = "",
) -> BrevoSendResult:
    """Send a marketing artifact as a transactional email via Brevo.

    In dry-run mode (default), builds the payload but does not call the API.
    In live mode, calls Brevo's transactional email endpoint.

    Requires the artifact to be in 'sent' state (post-approval).
    """
    payload = build_payload(
        artifact, config=config, to_email=to_email, to_name=to_name,
    )

    if artifact.state != "sent":
        return BrevoSendResult(
            sent=False,
            dry_run=False,
            message_id="",
            status_code=0,
            detail=f"Cannot send: artifact state is '{artifact.state}', must be 'sent'.",
            request_payload=payload,
        )

    if not config.is_live:
        log.info(
            "DRY-RUN: would send email to %s (artifact %s)",
            to_email,
            artifact.artifact_id,
        )
        return BrevoSendResult(
            sent=False,
            dry_run=True,
            message_id="dry-run",
            status_code=200,
            detail="Dry-run: payload built, API not called.",
            request_payload=payload,
        )

    # Live send path
    try:
        response = requests.post(
            config.api_url,
            headers={
                "api-key": config.api_key,
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            json=payload,
            timeout=30,
        )
        body = response.json() if response.content else {}
        message_id = body.get("messageId", "")

        if response.status_code in (200, 201):
            log.info(
                "SENT: email to %s (artifact %s, messageId %s)",
                to_email,
                artifact.artifact_id,
                message_id,
            )
            return BrevoSendResult(
                sent=True,
                dry_run=False,
                message_id=message_id,
                status_code=response.status_code,
                detail="Sent successfully via Brevo.",
                request_payload=payload,
            )

        log.warning(
            "BREVO ERROR: %s %s (artifact %s)",
            response.status_code,
            body,
            artifact.artifact_id,
        )
        return BrevoSendResult(
            sent=False,
            dry_run=False,
            message_id=message_id,
            status_code=response.status_code,
            detail=f"Brevo API error: {response.status_code} — {body}",
            request_payload=payload,
        )

    except requests.RequestException as exc:
        log.error("Brevo request failed: %s", exc)
        return BrevoSendResult(
            sent=False,
            dry_run=False,
            message_id="",
            status_code=0,
            detail=f"Brevo request failed: {exc}",
            request_payload=payload,
        )
    except Exception as exc:
        log.error("Brevo send failed: %s", exc)
        return BrevoSendResult(
            sent=False,
            dry_run=False,
            message_id="",
            status_code=0,
            detail=f"Send failed: {exc}",
            request_payload=payload,
        )
