"""iMessage delivery via SSH to Ewan's Mac (`pc` CLI tool).

Environment variables:
    IMESSAGE_HOST  — SSH hostname for the Mac (e.g. ewans-mac.local)
    IMESSAGE_USER  — SSH user on the Mac
    IMESSAGE_KEY_PATH — path to SSH private key for the Mac
"""

from __future__ import annotations

import asyncio
import logging
import os
import shlex

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration — all from environment, never hardcoded
# ---------------------------------------------------------------------------

_IMESSAGE_HOST: str | None = None
_IMESSAGE_USER: str | None = None
_IMESSAGE_KEY_PATH: str | None = None
_SSH_TIMEOUT_SECONDS = 15


def _load_config() -> tuple[str, str, str]:
    """Read iMessage SSH config from environment.

    Returns (host, user, key_path). Raises ``RuntimeError`` if any
    required variable is missing.
    """
    global _IMESSAGE_HOST, _IMESSAGE_USER, _IMESSAGE_KEY_PATH  # noqa: PLW0603

    _IMESSAGE_HOST = os.environ.get("IMESSAGE_HOST", _IMESSAGE_HOST)
    _IMESSAGE_USER = os.environ.get("IMESSAGE_USER", _IMESSAGE_USER)
    _IMESSAGE_KEY_PATH = os.environ.get("IMESSAGE_KEY_PATH", _IMESSAGE_KEY_PATH)

    missing = []
    if not _IMESSAGE_HOST:
        missing.append("IMESSAGE_HOST")
    if not _IMESSAGE_USER:
        missing.append("IMESSAGE_USER")
    if not _IMESSAGE_KEY_PATH:
        missing.append("IMESSAGE_KEY_PATH")

    if missing:
        raise RuntimeError(
            f"iMessage delivery not configured — missing env vars: {', '.join(missing)}"
        )

    return _IMESSAGE_HOST, _IMESSAGE_USER, _IMESSAGE_KEY_PATH  # type: ignore[return-value]


def _build_ssh_command(
    host: str,
    user: str,
    key_path: str,
    phone_number: str,
    message_body: str,
) -> list[str]:
    """Build the SSH + pc iMessage send command list."""
    remote_cmd = (
        f"pc imessage send"
        f" --to {shlex.quote(phone_number)}"
        f" --text {shlex.quote(message_body)}"
    )
    return [
        "ssh",
        "-i", key_path,
        "-o", "StrictHostKeyChecking=accept-new",
        "-o", f"ConnectTimeout={_SSH_TIMEOUT_SECONDS}",
        f"{user}@{host}",
        remote_cmd,
    ]


async def send_brief_link(
    phone_number: str,
    sheet_url: str,
    message: str,
) -> bool:
    """Send an iMessage containing the brief share link.

    Parameters
    ----------
    phone_number:
        Recipient phone number (E.164 format, e.g. ``+447700900000``).
    sheet_url:
        The share URL for the brief sheet.
    message:
        Human-readable message text (the URL is appended on a new line).

    Returns
    -------
    bool
        ``True`` if the message was sent successfully, ``False`` otherwise.
        Failures are logged but never raise — the caller decides how to
        handle a delivery failure.
    """
    try:
        host, user, key_path = _load_config()
    except RuntimeError:
        logger.exception("iMessage config missing — cannot send")
        return False

    message_body = f"{message}\n{sheet_url}"
    cmd = _build_ssh_command(host, user, key_path, phone_number, message_body)

    try:
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(),
            timeout=_SSH_TIMEOUT_SECONDS + 10,
        )

        if proc.returncode == 0:
            logger.info(
                "iMessage sent to %s (sheet_url=%s)",
                phone_number,
                sheet_url,
            )
            return True

        logger.error(
            "iMessage send failed (rc=%d) to %s: %s",
            proc.returncode,
            phone_number,
            stderr.decode(errors="replace").strip(),
        )
        return False

    except TimeoutError:
        logger.error(
            "iMessage send timed out for %s (host=%s)",
            phone_number,
            host,
        )
        return False
    except OSError:
        logger.exception("iMessage send OS error for %s", phone_number)
        return False
