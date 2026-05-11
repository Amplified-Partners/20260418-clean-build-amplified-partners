# AMP-324 Brief Mode — Implementation Plan

**Devon-3397 | 2026-05-11 | Architect session**
**Ticket:** [AMP-324](https://linear.app/amplifiedpartners/issue/AMP-324/vellum-p3-brief-mode-daily-agent-populated-sheet-with-imessage)

## Architecture

Brief mode is the simplest Vellum mode: single-writer-agent, single-reader-human.
The engine primitives built here (canvas, hash chain, tenant isolation, token auth)
are reused by Council (AMP-322) and Correspondence (AMP-323) later.

### Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Runtime | Python 3.12 + FastAPI | Matches clean-build conventions |
| Real-time canvas | pycrdt (Yrs/Yjs Python bindings) | MIT, Rust-backed, no Node sidecar needed |
| Storage | PostgreSQL 16 + pgvector | Canonical data architecture (no FalkorDB/Qdrant) |
| Hash chain | SHA-256 (stdlib hashlib) | Tamper-detection per strategy v2 |
| Auth | Token-scoped share links (JWT) | Phone/email-bound, time-bound, role-scoped |
| Delivery | `pc imessage send` via Ewan's Mac | Per strategy v2 |
| Cron | APScheduler or system cron | 06:25 generate, 06:30 deliver |
| HTTP | Behind Traefik on Beast | TLS everywhere, `api.amplifiedpartners.ai` |

### File Layout

```
02_build/vellum/
├── PLAN.md              ← this file
├── README.md            ← module overview
├── requirements.txt     ← dependencies
├── models/              ← Pydantic v2 shared types
│   ├── __init__.py
│   ├── entry.py         ← SheetEntry, HashChainEntry
│   ├── sheet.py         ← Sheet, SheetMeta, Tenant
│   └── token.py         ← ShareToken, TokenRole
├── canvas/              ← shared engine primitives
│   ├── __init__.py
│   ├── yjs_bridge.py    ← Yjs document wrapper (pycrdt)
│   ├── hash_chain.py    ← SHA-256 chain enforcement
│   ├── additive.py      ← additive-only write enforcement
│   └── tenant.py        ← tenant isolation logic
├── auth/                ← token auth
│   ├── __init__.py
│   └── tokens.py        ← JWT creation, validation, scoping
├── sheets/brief/        ← Brief mode policy
│   ├── __init__.py
│   ├── policy.py        ← single-writer, single-reader rules
│   └── generator.py     ← orchestrates researchers → synthesiser → sheet
├── agents/              ← researcher agents (data fetchers)
│   ├── __init__.py
│   ├── researcher_stripe.py    ← Stripe: yesterday's transactions
│   ├── researcher_calendar.py  ← Google Calendar: today's jobs
│   ├── researcher_searxng.py   ← SearXNG: weather + demand signals
│   └── synthesiser.py          ← composes narrative from researcher data
├── render/              ← mobile-first templates
│   ├── __init__.py
│   ├── templates/
│   │   └── brief.html   ← mobile read view + emoji-tap composer
│   └── static/
│       └── brief.css    ← critical inline CSS
├── delivery/            ← iMessage delivery
│   ├── __init__.py
│   └── imessage.py      ← wraps `pc imessage send`
├── cron/                ← scheduled jobs
│   ├── __init__.py
│   └── morning_brief.py ← 06:25 cron: generate + 06:30 deliver
├── webhooks/            ← reply handling
│   ├── __init__.py
│   └── reply_to_loop.py ← customer reply → agent loop
├── routes/              ← FastAPI routes
│   ├── __init__.py
│   ├── brief.py         ← sheet read/write endpoints
│   └── webhook.py       ← incoming reply endpoints
└── tests/               ← test suite
    ├── __init__.py
    ├── conftest.py       ← shared fixtures, mocked services
    ├── test_brief_mode.py       ← end-to-end
    ├── test_canvas.py           ← hash chain, additive-only
    ├── test_researchers.py      ← mocked Stripe/Calendar/SearXNG
    ├── test_delivery.py         ← iMessage delivery
    └── test_reply_loop.py       ← webhook → agent loop
```

## Daughter Session Split

Six parallel streams. Each daughter works on a separate branch in `Amplified-Partners/clean-build`,
scoped to specific directories. Parent (this session) merges.

| # | Stream | Branch suffix | Directories owned | Dependencies |
|---|--------|---------------|-------------------|--------------|
| 1 | Canvas Engine | `amp-324-canvas` | `canvas/`, `models/`, `auth/` | None (foundation) |
| 2 | Researcher Agents | `amp-324-researchers` | `agents/` | Models from #1 (interface only) |
| 3 | Mobile Template | `amp-324-template` | `render/` | None (standalone HTML/CSS) |
| 4 | Delivery + Cron | `amp-324-delivery` | `delivery/`, `cron/` | Models from #1, auth from #1 |
| 5 | Webhook + Reply Loop | `amp-324-webhook` | `webhooks/`, `routes/` | Models from #1 |
| 6 | Tests | `amp-324-tests` | `tests/` | All interfaces (writes against stubs) |

### Interface contracts (daughters code against these)

**SheetEntry** (models/entry.py):
```python
class SheetEntry(BaseModel):
    id: str                    # uuid4
    sheet_id: str              # tenant-scoped sheet identifier
    author: str                # agent handle or human name
    content: str               # the line of text
    timestamp: datetime        # UTC
    prev_hash: str             # sha256 of previous entry
    entry_hash: str            # sha256(prev_hash || content)
    entry_type: Literal["agent_write", "human_comment", "emoji_reaction"]
```

**ShareToken** (models/token.py):
```python
class ShareToken(BaseModel):
    token_id: str
    sheet_id: str
    role: Literal["read", "comment", "write"]
    bound_to: str | None       # phone number or email
    expires_at: datetime | None
```

**ResearcherOutput** (agents interface):
```python
class ResearcherOutput(BaseModel):
    source: str                # "stripe" | "calendar" | "searxng"
    data: dict                 # structured payload
    summary: str               # one-line human-readable
    timestamp: datetime
```

## Decisions taken (reversible)

- Build in `clean-build/02_build/vellum/` — no org repo creation needed. OPINION 90%.
- Use `pycrdt` for Yjs (Rust-backed, no Node). OPINION 85%.
- JWT for token auth (PyJWT, HS256 initially). OPINION 88%.
- PostgreSQL for sheet storage (per canonical data architecture). OPINION 95%.
- Daughters branch from main, touch disjoint directories, parent merges. OPINION 90%.

## Acceptance scenarios (from ticket)

1. Daily generation — cron 06:25 creates fresh sheet for Jesmond
2. iMessage delivery at 06:30 — share link sent to Bob's phone
3. 30-second read — TTI < 1s on 4G, one page, no scroll for headline
4. One-tap reply — emoji (👍/⚠️/❓) or one-line comment, lands as sheet event
5. Reply-to-loop — Bob's comments fire webhook → Architect follow-up

---
*Devon-3397 | 2026-05-11 | session devin-3397942217f044f4942754d4fa76c72f*
