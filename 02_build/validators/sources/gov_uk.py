"""GOV.UK content / statutory pages — open, no key.

GOV.UK serves statutory guidance, regulations, and consultations under OGL.
We use it to assert availability of authoritative pages cited in the catalogue
(Tipping Act, Licensing Act, HMRC rates relief, etc.).

Used by:
- INS-042 (Licence Renewal — Licensing Act 2003 statutory guidance)
- INS-043 (Business Rates — HMRC reliefs schedule)
- INS-052 (Deposit / No-Show Policy ROI — Consumer Contracts Regs 2013)
- INS-053 (Corkage and Tip Pool — Tipping Act 2023 statutory code)

Authored by Devon (Devin session 4234e1c8afbe42f2aff84a29ce139809), 2026-05-03.
"""

from __future__ import annotations

from ._http import CachedResponse, HttpClient


def fetch_url(client: HttpClient, url: str) -> CachedResponse:
    return client.get(url)
