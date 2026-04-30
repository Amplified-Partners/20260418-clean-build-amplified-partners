"""Email fetcher — IMAP connection, incremental fetch, parsing."""

from __future__ import annotations

import email
import email.header
import email.utils
import imaplib
import logging
import re
import ssl
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .config import EmailAccountConfig, FETCH_BATCH_SIZE

logger = logging.getLogger("email_agent.fetcher")


@dataclass
class FetchedEmail:
    """Parsed email ready for triage."""

    message_id: str
    imap_uid: int
    from_address: str
    from_name: str
    to_addresses: list[str]
    cc_addresses: list[str]
    subject: str
    body_text: str
    body_html: str
    received_at: datetime
    thread_id: str | None
    has_attachments: bool
    attachment_names: list[str]
    raw_headers: dict[str, str]


def _decode_header(raw: str | None) -> str:
    """Decode RFC 2047 encoded header value."""
    if not raw:
        return ""
    parts = email.header.decode_header(raw)
    decoded: list[str] = []
    for data, charset in parts:
        if isinstance(data, bytes):
            decoded.append(data.decode(charset or "utf-8", errors="replace"))
        else:
            decoded.append(data)
    return " ".join(decoded)


def _extract_addresses(header_val: str | None) -> list[str]:
    """Extract email addresses from a header like To or Cc."""
    if not header_val:
        return []
    # email.utils.getaddresses handles groups and multiple addresses
    pairs = email.utils.getaddresses([header_val])
    return [addr for _, addr in pairs if addr]


def _extract_body(msg: email.message.Message) -> tuple[str, str]:
    """Extract plain text and HTML body from a MIME message."""
    text_body = ""
    html_body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition:
                continue
            try:
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                charset = part.get_content_charset() or "utf-8"
                decoded = payload.decode(charset, errors="replace")
            except Exception:
                continue

            if content_type == "text/plain" and not text_body:
                text_body = decoded
            elif content_type == "text/html" and not html_body:
                html_body = decoded
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or "utf-8"
                decoded = payload.decode(charset, errors="replace")
                if msg.get_content_type() == "text/html":
                    html_body = decoded
                else:
                    text_body = decoded
        except Exception:
            pass

    return text_body, html_body


def _extract_attachments(msg: email.message.Message) -> list[str]:
    """Get attachment filenames."""
    names: list[str] = []
    if not msg.is_multipart():
        return names
    for part in msg.walk():
        disposition = str(part.get("Content-Disposition", ""))
        if "attachment" in disposition:
            filename = part.get_filename()
            if filename:
                names.append(_decode_header(filename))
    return names


def _parse_date(date_str: str | None) -> datetime:
    """Parse email date header to UTC datetime."""
    if not date_str:
        return datetime.now(timezone.utc)
    try:
        parsed = email.utils.parsedate_to_datetime(date_str)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except Exception:
        return datetime.now(timezone.utc)


def _extract_gmail_thread_id(msg: email.message.Message) -> str | None:
    """Extract Gmail thread ID from X-GM-THRID if available."""
    # This requires IMAP extension; we get it from raw_headers if fetched
    return None  # Will be populated from IMAP FETCH response


def fetch_emails(
    account: EmailAccountConfig,
    last_uid: int | None = None,
    batch_size: int = FETCH_BATCH_SIZE,
) -> list[FetchedEmail]:
    """
    Connect to IMAP, fetch emails newer than last_uid.

    Uses UID SEARCH to do incremental fetch. Returns parsed emails
    sorted by received_at ascending (oldest first).
    """
    logger.info(
        "Connecting to %s:%d for %s",
        account.imap_host,
        account.imap_port,
        account.email_address,
    )

    ctx = ssl.create_default_context()
    imap = imaplib.IMAP4_SSL(account.imap_host, account.imap_port, ssl_context=ctx)

    try:
        imap.login(account.email_address, account.app_password)
        imap.select("INBOX", readonly=True)

        # Incremental fetch: UIDs greater than watermark
        if last_uid:
            search_criteria = f"UID {last_uid + 1}:*"
        else:
            # First sync: fetch last N
            search_criteria = "ALL"

        status, uid_data = imap.uid("SEARCH", None, search_criteria)
        if status != "OK" or not uid_data[0]:
            logger.info("No new emails found")
            return []

        uid_list = uid_data[0].split()

        # If first sync (no watermark), take only most recent batch_size
        if not last_uid and len(uid_list) > batch_size:
            uid_list = uid_list[-batch_size:]

        # Cap at batch_size
        uid_list = uid_list[:batch_size]

        logger.info("Fetching %d emails (UIDs: %s...)", len(uid_list), uid_list[0])

        emails: list[FetchedEmail] = []

        for uid_bytes in uid_list:
            uid = int(uid_bytes)

            status, msg_data = imap.uid(
                "FETCH", str(uid), "(RFC822 X-GM-THRID)"
            )
            if status != "OK" or not msg_data or not msg_data[0]:
                continue

            # Parse the response
            raw_email = None
            thread_id = None

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    header_line = response_part[0]
                    if isinstance(header_line, bytes):
                        header_str = header_line.decode("utf-8", errors="replace")
                        # Extract X-GM-THRID from FETCH response
                        thrid_match = re.search(r"X-GM-THRID (\d+)", header_str)
                        if thrid_match:
                            thread_id = thrid_match.group(1)
                    raw_email = response_part[1]

            if raw_email is None:
                continue

            msg = email.message_from_bytes(raw_email)

            # Extract components
            from_name, from_addr = email.utils.parseaddr(
                _decode_header(msg.get("From", ""))
            )
            text_body, html_body = _extract_body(msg)
            attachment_names = _extract_attachments(msg)

            fetched = FetchedEmail(
                message_id=msg.get("Message-ID", f"<uid-{uid}@{account.imap_host}>"),
                imap_uid=uid,
                from_address=from_addr,
                from_name=from_name,
                to_addresses=_extract_addresses(msg.get("To")),
                cc_addresses=_extract_addresses(msg.get("Cc")),
                subject=_decode_header(msg.get("Subject")),
                body_text=text_body,
                body_html=html_body,
                received_at=_parse_date(msg.get("Date")),
                thread_id=thread_id,
                has_attachments=len(attachment_names) > 0,
                attachment_names=attachment_names,
                raw_headers={
                    "Reply-To": msg.get("Reply-To", ""),
                    "List-Unsubscribe": msg.get("List-Unsubscribe", ""),
                    "X-Mailer": msg.get("X-Mailer", ""),
                    "Precedence": msg.get("Precedence", ""),
                },
            )
            emails.append(fetched)

        # Sort oldest first
        emails.sort(key=lambda e: e.received_at)
        logger.info("Fetched and parsed %d emails", len(emails))
        return emails

    finally:
        try:
            imap.logout()
        except Exception:
            pass
