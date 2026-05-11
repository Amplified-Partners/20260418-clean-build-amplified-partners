"""Reply-to-loop webhook — handles Bob's replies (emoji taps or text comments).

Flow:
1. Receives reply content + entry_type
2. Validates the share token (valid, not expired, role >= 'comment')
3. Appends the reply to the sheet's hash chain
4. Fires a webhook/event to OpenClaw to schedule an Architect follow-up

Devon-598da8fc | 2026-05-11
"""

from __future__ import annotations

import os
from typing import Literal

import httpx

from vellum.models.entry import SheetEntry
from vellum.models.sheet import Sheet
from vellum.models.token import ShareToken, TokenRole

OPENCLAW_WEBHOOK_URL = os.environ.get("OPENCLAW_WEBHOOK_URL", "")

ROLE_HIERARCHY: dict[TokenRole, int] = {"read": 0, "comment": 1, "write": 2}


class TokenValidationError(Exception):
    """Raised when a share token is invalid, expired, or lacks permission."""


class SheetNotFoundError(Exception):
    """Raised when the target sheet does not exist."""


# ---------------------------------------------------------------------------
# In-memory store (replaced by PostgreSQL in production)
# ---------------------------------------------------------------------------
_sheets: dict[str, Sheet] = {}
_tokens: dict[str, ShareToken] = {}


def register_sheet(sheet: Sheet) -> None:
    """Register a sheet in the in-memory store."""
    _sheets[sheet.meta.id] = sheet


def register_token(token: ShareToken) -> None:
    """Register a token in the in-memory store."""
    _tokens[token.token_id] = token


def get_sheet(sheet_id: str) -> Sheet | None:
    """Look up a sheet by ID."""
    return _sheets.get(sheet_id)


def get_tokens_for_sheet(sheet_id: str) -> list[ShareToken]:
    """Return all tokens scoped to a given sheet."""
    return [t for t in _tokens.values() if t.sheet_id == sheet_id]


def clear_stores() -> None:
    """Reset in-memory stores (used by tests)."""
    _sheets.clear()
    _tokens.clear()


# ---------------------------------------------------------------------------
# Token validation
# ---------------------------------------------------------------------------

def validate_token(
    sheet_id: str,
    token_id: str,
    min_role: TokenRole = "comment",
) -> ShareToken:
    """Validate a share token against a sheet.

    Raises TokenValidationError if the token is invalid, expired, revoked,
    does not match the sheet, or lacks the required role.
    """
    token = _tokens.get(token_id)
    if token is None:
        raise TokenValidationError("Token not found")
    if token.sheet_id != sheet_id:
        raise TokenValidationError("Token does not match sheet")
    if not token.is_valid:
        raise TokenValidationError("Token is revoked or expired")
    if ROLE_HIERARCHY.get(token.role, 0) < ROLE_HIERARCHY.get(min_role, 0):
        raise TokenValidationError(
            f"Token role '{token.role}' is below required '{min_role}'"
        )
    return token


# ---------------------------------------------------------------------------
# Core reply processor
# ---------------------------------------------------------------------------

async def process_reply(
    sheet_id: str,
    token: str,
    content: str,
    entry_type: Literal["emoji_reaction", "human_comment"],
) -> SheetEntry:
    """Process a reply from a human reader.

    Args:
        sheet_id: The target sheet.
        token: Share token ID for authentication.
        content: The reply content (emoji character or text comment).
        entry_type: 'emoji_reaction' or 'human_comment'.

    Returns:
        The newly created SheetEntry appended to the chain.

    Raises:
        SheetNotFoundError: If the sheet does not exist.
        TokenValidationError: If the token is invalid/expired/insufficient.
    """
    sheet = get_sheet(sheet_id)
    if sheet is None:
        raise SheetNotFoundError(f"Sheet '{sheet_id}' not found")

    validate_token(sheet_id, token, min_role="comment")

    prev_hash = sheet.latest_hash
    entry = SheetEntry(
        sheet_id=sheet_id,
        author="human",
        content=content,
        prev_hash=prev_hash,
        entry_type=entry_type,
    )

    sheet.entries.append(entry)
    sheet.latest_hash = entry.entry_hash

    await _fire_openclaw_webhook(sheet_id, entry)

    return entry


async def _fire_openclaw_webhook(sheet_id: str, entry: SheetEntry) -> None:
    """Notify OpenClaw that a reply was received so it can schedule follow-up."""
    url = OPENCLAW_WEBHOOK_URL
    if not url:
        return

    payload = {
        "event": "brief.reply_received",
        "sheet_id": sheet_id,
        "entry_id": entry.id,
        "entry_type": entry.entry_type,
        "content": entry.content,
        "timestamp": entry.timestamp.isoformat(),
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        await client.post(url, json=payload)
