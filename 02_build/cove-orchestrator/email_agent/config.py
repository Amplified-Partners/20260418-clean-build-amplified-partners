"""Email Agent configuration — accounts, triage thresholds, models."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from enum import Enum


class EmailPriority(str, Enum):
    CRITICAL = "critical"   # Needs response within 1 hour
    URGENT = "urgent"       # Needs response today
    NORMAL = "normal"       # Needs response within 48 hours
    LOW = "low"             # FYI / newsletter / no response needed

    @classmethod
    def from_score(cls, score: float) -> "EmailPriority":
        if score >= 9.0:
            return cls.CRITICAL
        if score >= 7.0:
            return cls.URGENT
        if score >= 4.0:
            return cls.NORMAL
        return cls.LOW


class EmailAction(str, Enum):
    RESPOND = "respond"     # Generate draft response
    DELEGATE = "delegate"   # Forward to appropriate person/agent
    ARCHIVE = "archive"     # No action needed, archive
    DEFER = "defer"         # Mark for later review
    ESCALATE = "escalate"   # Needs Ewan's direct attention


class DraftStatus(str, Enum):
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    SENT = "sent"
    REJECTED = "rejected"


@dataclass(frozen=True)
class TriageResult:
    """Output from the triage classifier."""

    priority: EmailPriority
    action: EmailAction
    confidence: float
    reasoning: str


@dataclass(frozen=True)
class EmailAccountConfig:
    """IMAP/SMTP account config loaded from env."""

    email_address: str
    display_name: str
    imap_host: str = "imap.gmail.com"
    imap_port: int = 993
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    auth_method: str = "app_password"
    app_password: str = ""


# ─── Environment ─────────────────────────────────────────────────────

POSTGRES_DSN = os.environ.get(
    "POSTGRES_DSN",
    "postgresql://cove:cove_dev_2026@localhost:5432/cove",
)

LITELLM_URL = os.environ.get("LITELLM_URL", "http://localhost:4000")

# Triage uses cheap model; drafts use medium
TRIAGE_MODEL = os.environ.get("EMAIL_TRIAGE_MODEL", "deepseek/deepseek-chat")
DRAFT_MODEL = os.environ.get("EMAIL_DRAFT_MODEL", "anthropic/claude-sonnet-4-20250514")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

# Gmail app password (for initial build; OAuth2 later)
GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
GMAIL_DISPLAY_NAME = os.environ.get("GMAIL_DISPLAY_NAME", "Ewan Bramley")

# How many emails to fetch per sync
FETCH_BATCH_SIZE = int(os.environ.get("EMAIL_FETCH_BATCH_SIZE", "50"))

# Confidence threshold below which we escalate to human
CONFIDENCE_THRESHOLD = float(os.environ.get("EMAIL_CONFIDENCE_THRESHOLD", "0.7"))

# Auto-handle domains (newsletters, notifications)
AUTO_ARCHIVE_DOMAINS: list[str] = [
    "noreply@",
    "no-reply@",
    "notifications@",
    "mailer-daemon@",
    "updates@",
    "digest@",
]
