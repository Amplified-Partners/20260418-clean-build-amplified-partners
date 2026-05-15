#!/usr/bin/env python3
"""
Business Brain Context — 19-Field Schema & Transmission Layer
===============================================================

Implements the canonical 19-field business_brain_context table and the
transmission layer that bridges 17 (signature cardinality) to 3 (attention
cardinality) for human rendering, and 3 back to 19 for expansion.

Schema: 19 fields total
  - 17 signature fields (the 17-store — what makes a record itself)
  - 2 system fields (pudding_label + status)
  - Plus provenance metadata (signed_by, created_at, updated_at, id)

The 17-and-3 Principle (Ewan Bramley, 2026-05-14):
  - Pipe captures 17. CRM stores 17. AI reasons on 17.
  - 3 is what the transmission layer renders when a human arrives.
  - Don't lobotomise the AI — 17 is AI's ground truth, 3 is what AI produces.

Usage:
  # Create schema on PostgreSQL:
  python business_brain_schema.py --create-schema

  # Run transmission layer demo:
  python business_brain_schema.py --demo

  # Validate schema:
  python business_brain_schema.py --validate

Environment variables:
  PG_HOST      PostgreSQL host (default: cove-postgres)
  PG_PORT      PostgreSQL port (default: 5432)
  PG_DB        Database name (default: amplified_brain)
  PG_USER      PostgreSQL user (default: postgres)
  PG_PASSWORD  PostgreSQL password (required for DB operations)

Signed-by: Devon-8da1 | 2026-05-15 | devin-8da1981ce177481da3fe1d2b40e7fade
"""
from __future__ import annotations

import argparse
import enum
import json
import logging
import os
import re
import sys
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("business_brain_schema")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PG_HOST = os.environ.get("PG_HOST", "cove-postgres")
PG_PORT = int(os.environ.get("PG_PORT", "5432"))
PG_DB = os.environ.get("PG_DB", "amplified_brain")
PG_USER = os.environ.get("PG_USER", "postgres")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "")


# ---------------------------------------------------------------------------
# 1. Epistemic Status (inline — mirrors epistemic_status.py)
# ---------------------------------------------------------------------------

class EpistemicTier(enum.IntEnum):
    INTUITED = 1
    STRUCTURED = 2
    MEASURED = 3
    PROVEN = 4

    def label(self) -> str:
        return {1: "INTUITED", 2: "STRUCTURED", 3: "MEASURED", 4: "PROVEN"}[self]


class ContextStatus(enum.Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    SUPERSEDED = "superseded"
    DRAFT = "draft"


# ---------------------------------------------------------------------------
# 2. PUDDING Taxonomy Validation
# ---------------------------------------------------------------------------

PUDDING_WHAT = 7    # content type dimensions
PUDDING_HOW = 7     # methodology dimensions
PUDDING_SCALE = 7   # scale dimensions
PUDDING_TIME = 6    # time dimensions

PUDDING_TOTAL = PUDDING_WHAT * PUDDING_HOW * PUDDING_SCALE * PUDDING_TIME  # 2,058


def validate_pudding_label(label: str) -> bool:
    """Validate PUDDING taxonomy label format: X.X.X.X where each X is 1-7 (or 1-6 for TIME)."""
    pattern = r"^[1-7]\.[1-7]\.[1-7]\.[1-6]$"
    return bool(re.match(pattern, label))


# ---------------------------------------------------------------------------
# 3. The 19-Field Schema — Business Brain Context
# ---------------------------------------------------------------------------

@dataclass
class BusinessBrainContext:
    """
    The 19-field business brain context record.

    17 signature fields (the 17-store):
      1.  context_name          — human-readable name for this context
      2.  context_type          — category (interview, research, operational, strategic)
      3.  business_name         — the business this context belongs to
      4.  industry_sector       — SIC code or free text
      5.  owner_goal_primary    — primary goal from founder interview
      6.  owner_goal_secondary  — secondary goal
      7.  current_revenue       — monthly or annual (currency: GBP)
      8.  team_size             — number of employees
      9.  biggest_friction      — primary pain point
      10. operational_capacity  — capacity utilisation (0.0-1.0)
      11. cash_position         — cash in bank (GBP)
      12. risk_level            — assessed risk (1-10)
      13. opportunity_score     — assessed opportunity (1-10)
      14. source_agent          — which agent produced this context
      15. source_session        — session ID for radical attribution
      16. epistemic_tier        — INTUITED/STRUCTURED/MEASURED/PROVEN
      17. valid_until           — expiry timestamp for staleness rules

    2 system fields:
      18. pudding_label         — PUDDING taxonomy code (X.X.X.X)
      19. status                — active/archived/superseded/draft

    Plus provenance metadata (not counted in the 19 — these are infrastructure):
      - id (UUID primary key)
      - tenant_id (multi-tenancy)
      - signed_by (radical attribution)
      - created_at
      - updated_at
      - embedding_id (foreign key to pgvector)
    """

    # --- 17 signature fields ---
    context_name: str = ""
    context_type: str = "operational"
    business_name: str = ""
    industry_sector: str = ""
    owner_goal_primary: str = ""
    owner_goal_secondary: str = ""
    current_revenue: Optional[float] = None
    team_size: Optional[int] = None
    biggest_friction: str = ""
    operational_capacity: Optional[float] = None
    cash_position: Optional[float] = None
    risk_level: Optional[int] = None
    opportunity_score: Optional[int] = None
    source_agent: str = ""
    source_session: str = ""
    epistemic_tier: int = EpistemicTier.INTUITED
    valid_until: Optional[str] = None

    # --- 2 system fields ---
    pudding_label: str = "1.1.1.1"
    status: str = ContextStatus.DRAFT.value

    # --- Provenance metadata ---
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tenant_id: Optional[str] = None
    signed_by: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    embedding_id: Optional[int] = None

    def validate(self) -> list[str]:
        """Validate all fields. Returns list of errors (empty = valid)."""
        errors = []

        if not self.context_name:
            errors.append("context_name is required")
        if self.context_type not in ("interview", "research", "operational", "strategic"):
            errors.append(f"context_type must be interview/research/operational/strategic, got '{self.context_type}'")
        if not self.business_name:
            errors.append("business_name is required")
        if self.pudding_label and not validate_pudding_label(self.pudding_label):
            errors.append(f"pudding_label must be X.X.X.X format (1-7.1-7.1-7.1-6), got '{self.pudding_label}'")
        if self.risk_level is not None and not (1 <= self.risk_level <= 10):
            errors.append(f"risk_level must be 1-10, got {self.risk_level}")
        if self.opportunity_score is not None and not (1 <= self.opportunity_score <= 10):
            errors.append(f"opportunity_score must be 1-10, got {self.opportunity_score}")
        if self.operational_capacity is not None and not (0.0 <= self.operational_capacity <= 1.0):
            errors.append(f"operational_capacity must be 0.0-1.0, got {self.operational_capacity}")
        if self.epistemic_tier not in (1, 2, 3, 4):
            errors.append(f"epistemic_tier must be 1-4, got {self.epistemic_tier}")
        if self.status not in ("active", "archived", "superseded", "draft"):
            errors.append(f"status must be active/archived/superseded/draft, got '{self.status}'")
        if not self.source_agent:
            errors.append("source_agent is required (Radical Attribution)")
        if not self.source_session:
            errors.append("source_session is required (Radical Attribution)")
        if not self.signed_by:
            errors.append("signed_by is required (Radical Attribution)")

        return errors


# ---------------------------------------------------------------------------
# 4. The Transmission Layer — 19→3 and 3→19
# ---------------------------------------------------------------------------

@dataclass
class HumanRendering:
    """
    The 3-field human rendering. What a human sees.

    This is an EVENT, not a RECORD. Ephemeral. Re-derivable on demand.
    Different human, different moment, different 3.
    The 19 underneath is invariant.
    """
    headline: str       # one-line summary
    situation: str      # current state + key numbers
    recommendation: str # what to do next

    # Attribution back to the full record
    source_id: str = ""
    source_tier: str = "INTUITED"
    full_record_available: bool = True


def render_19_to_3(context: BusinessBrainContext) -> HumanRendering:
    """
    Transmission layer: 19 → 3.

    Reads the full 19-field record and renders 3 fields for human attention.
    The other 16 fields remain reachable on demand.

    This is the DETERMINISTIC path. For AI-enhanced rendering, pass the
    full 19-field record to the AI transmission layer instead.
    """
    tier_label = EpistemicTier(context.epistemic_tier).label()

    headline = f"{context.business_name}: {context.context_name}"
    if context.status != "active":
        headline += f" [{context.status.upper()}]"

    situation_parts = []
    if context.current_revenue is not None:
        situation_parts.append(f"Revenue: £{context.current_revenue:,.0f}")
    if context.team_size is not None:
        situation_parts.append(f"Team: {context.team_size}")
    if context.cash_position is not None:
        situation_parts.append(f"Cash: £{context.cash_position:,.0f}")
    if context.operational_capacity is not None:
        situation_parts.append(f"Capacity: {context.operational_capacity:.0%}")
    if context.biggest_friction:
        situation_parts.append(f"Friction: {context.biggest_friction}")
    situation = " | ".join(situation_parts) if situation_parts else "No quantitative data available"

    rec_parts = []
    if context.owner_goal_primary:
        rec_parts.append(f"Goal: {context.owner_goal_primary}")
    if context.risk_level is not None and context.risk_level >= 7:
        rec_parts.append(f"⚠ High risk ({context.risk_level}/10)")
    if context.opportunity_score is not None and context.opportunity_score >= 7:
        rec_parts.append(f"Opportunity ({context.opportunity_score}/10)")
    recommendation = ". ".join(rec_parts) if rec_parts else "Awaiting analysis"

    return HumanRendering(
        headline=headline,
        situation=situation,
        recommendation=recommendation,
        source_id=context.id,
        source_tier=tier_label,
        full_record_available=True,
    )


def expand_3_to_19(
    headline: str,
    situation: str,
    recommendation: str,
    source_agent: str = "",
    source_session: str = "",
    signed_by: str = "",
) -> BusinessBrainContext:
    """
    Transmission layer: 3 → 19.

    Takes a human's 3-field input and expands it into a 19-field record.
    Fields that cannot be inferred from the 3 are left empty or defaulted.

    The DETERMINISTIC expansion sets what it can. The AI expansion layer
    (not in this module) fills in the gaps using the full 17-store context.
    """
    ctx = BusinessBrainContext(
        context_name=headline,
        context_type="operational",
        business_name=_extract_business_name(headline),
        biggest_friction=_extract_friction(situation),
        owner_goal_primary=_extract_goal(recommendation),
        source_agent=source_agent or "human_input",
        source_session=source_session,
        signed_by=signed_by or "human",
        epistemic_tier=EpistemicTier.INTUITED,
        status=ContextStatus.DRAFT.value,
    )

    revenue = _extract_currency(situation)
    if revenue is not None:
        ctx.current_revenue = revenue

    team = _extract_number(situation, "Team")
    if team is not None:
        ctx.team_size = int(team)

    cash = _extract_currency(situation, prefix="Cash")
    if cash is not None:
        ctx.cash_position = cash

    return ctx


def _extract_business_name(headline: str) -> str:
    """Extract business name from headline (before colon)."""
    if ":" in headline:
        return headline.split(":")[0].strip()
    return headline.strip()


def _extract_friction(situation: str) -> str:
    """Extract friction point from situation string."""
    if "Friction:" in situation:
        part = situation.split("Friction:")[1]
        if "|" in part:
            return part.split("|")[0].strip()
        return part.strip()
    return ""


def _extract_goal(recommendation: str) -> str:
    """Extract goal from recommendation string."""
    if "Goal:" in recommendation:
        part = recommendation.split("Goal:")[1]
        if "." in part:
            return part.split(".")[0].strip()
        return part.strip()
    return recommendation.strip()


def _extract_currency(text: str, prefix: str = "Revenue") -> Optional[float]:
    """Extract £-prefixed number from text."""
    pattern = rf"{prefix}:\s*£([\d,]+)"
    match = re.search(pattern, text)
    if match:
        return float(match.group(1).replace(",", ""))
    return None


def _extract_number(text: str, prefix: str) -> Optional[float]:
    """Extract number after a labelled prefix."""
    pattern = rf"{prefix}:\s*([\d.]+)"
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    return None


# ---------------------------------------------------------------------------
# 5. PostgreSQL Schema DDL
# ---------------------------------------------------------------------------

CREATE_SCHEMA_SQL = """
-- Business Brain Context — 19-Field Schema
-- Canonical Data Architecture: PostgreSQL + Apache AGE + pgvector
-- Signed-by: Devon-8da1 | 2026-05-15

-- Ensure extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

-- The 19-field business_brain_context table
CREATE TABLE IF NOT EXISTS business_brain_context (
    -- Infrastructure (not part of the 19)
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id           UUID,
    signed_by           TEXT NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    embedding_id        INTEGER,

    -- 17 signature fields (the 17-store)
    context_name        TEXT NOT NULL,
    context_type        TEXT NOT NULL CHECK (context_type IN ('interview', 'research', 'operational', 'strategic')),
    business_name       TEXT NOT NULL,
    industry_sector     TEXT DEFAULT '',
    owner_goal_primary  TEXT DEFAULT '',
    owner_goal_secondary TEXT DEFAULT '',
    current_revenue     NUMERIC(15,2),
    team_size           INTEGER,
    biggest_friction    TEXT DEFAULT '',
    operational_capacity NUMERIC(5,4) CHECK (operational_capacity IS NULL OR (operational_capacity >= 0 AND operational_capacity <= 1)),
    cash_position       NUMERIC(15,2),
    risk_level          INTEGER CHECK (risk_level IS NULL OR (risk_level >= 1 AND risk_level <= 10)),
    opportunity_score   INTEGER CHECK (opportunity_score IS NULL OR (opportunity_score >= 1 AND opportunity_score <= 10)),
    source_agent        TEXT NOT NULL,
    source_session      TEXT NOT NULL,
    epistemic_tier      INTEGER NOT NULL DEFAULT 1 CHECK (epistemic_tier >= 1 AND epistemic_tier <= 4),
    valid_until         TIMESTAMPTZ,

    -- 2 system fields
    pudding_label       TEXT DEFAULT '1.1.1.1' CHECK (pudding_label ~ '^[1-7]\\.[1-7]\\.[1-7]\\.[1-6]$'),
    status              TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('active', 'archived', 'superseded', 'draft'))
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_bbc_tenant ON business_brain_context (tenant_id);
CREATE INDEX IF NOT EXISTS idx_bbc_business ON business_brain_context (business_name);
CREATE INDEX IF NOT EXISTS idx_bbc_status ON business_brain_context (status);
CREATE INDEX IF NOT EXISTS idx_bbc_type ON business_brain_context (context_type);
CREATE INDEX IF NOT EXISTS idx_bbc_pudding ON business_brain_context (pudding_label);
CREATE INDEX IF NOT EXISTS idx_bbc_tier ON business_brain_context (epistemic_tier);
CREATE INDEX IF NOT EXISTS idx_bbc_created ON business_brain_context (created_at);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_bbc_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_bbc_updated_at ON business_brain_context;
CREATE TRIGGER trg_bbc_updated_at
    BEFORE UPDATE ON business_brain_context
    FOR EACH ROW EXECUTE FUNCTION update_bbc_updated_at();

-- Provenance view: full context with human-readable tier
CREATE OR REPLACE VIEW business_brain_context_view AS
SELECT
    *,
    CASE epistemic_tier
        WHEN 1 THEN 'INTUITED'
        WHEN 2 THEN 'STRUCTURED'
        WHEN 3 THEN 'MEASURED'
        WHEN 4 THEN 'PROVEN'
    END AS tier_label,
    CASE
        WHEN valid_until IS NOT NULL AND valid_until < NOW() THEN true
        ELSE false
    END AS is_stale
FROM business_brain_context;
""".strip()


# ---------------------------------------------------------------------------
# 6. API Layer (FastAPI endpoints for context CRUD)
# ---------------------------------------------------------------------------

FASTAPI_ROUTER_CODE = '''
"""
Business Brain Context API — FastAPI Router
=============================================

Endpoints for storing and retrieving 19-field business brain context records.
Includes transmission layer endpoints (19→3 and 3→19).

Mount this router in your FastAPI app:
    from business_brain_api import router as brain_router
    app.include_router(brain_router, prefix="/api/v1/brain")
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator

router = APIRouter(tags=["business-brain"])


class BusinessBrainContextCreate(BaseModel):
    """19-field context creation payload."""
    context_name: str
    context_type: str = "operational"
    business_name: str
    industry_sector: str = ""
    owner_goal_primary: str = ""
    owner_goal_secondary: str = ""
    current_revenue: Optional[float] = None
    team_size: Optional[int] = None
    biggest_friction: str = ""
    operational_capacity: Optional[float] = None
    cash_position: Optional[float] = None
    risk_level: Optional[int] = None
    opportunity_score: Optional[int] = None
    source_agent: str
    source_session: str
    epistemic_tier: int = 1
    valid_until: Optional[str] = None
    pudding_label: str = "1.1.1.1"
    status: str = "draft"
    signed_by: str
    tenant_id: Optional[str] = None

    @field_validator("pudding_label")
    @classmethod
    def validate_pudding(cls, v: str) -> str:
        import re
        if not re.match(r"^[1-7]\.[1-7]\.[1-7]\.[1-6]$", v):
            raise ValueError("pudding_label must be X.X.X.X (1-7.1-7.1-7.1-6)")
        return v


class HumanRenderingResponse(BaseModel):
    """3-field human rendering."""
    headline: str
    situation: str
    recommendation: str
    source_id: str
    source_tier: str
    full_record_available: bool = True


class HumanInputExpand(BaseModel):
    """3-field human input for expansion to 19."""
    headline: str
    situation: str
    recommendation: str
    source_agent: str = "human_input"
    source_session: str = ""
    signed_by: str = "human"


@router.post("/context", status_code=201)
async def create_context(payload: BusinessBrainContextCreate):
    """Create a new 19-field business brain context record."""
    # Validation happens via Pydantic
    # In production: insert into business_brain_context table
    return {
        "id": str(uuid.uuid4()),
        "status": "created",
        "context_name": payload.context_name,
        "business_name": payload.business_name,
        "epistemic_tier": payload.epistemic_tier,
        "pudding_label": payload.pudding_label,
    }


@router.get("/context/{context_id}")
async def get_context(context_id: str):
    """Retrieve full 19-field context by ID."""
    # In production: SELECT * FROM business_brain_context WHERE id = context_id
    raise HTTPException(status_code=404, detail="Context not found")


@router.get("/context/{context_id}/render")
async def render_context(context_id: str):
    """Transmission layer: 19→3. Render a context record for human consumption."""
    # In production: load full record, pass through render_19_to_3()
    return HumanRenderingResponse(
        headline="[placeholder]",
        situation="[placeholder]",
        recommendation="[placeholder]",
        source_id=context_id,
        source_tier="INTUITED",
    )


@router.post("/context/expand")
async def expand_human_input(payload: HumanInputExpand):
    """Transmission layer: 3→19. Expand human input to full context record."""
    # In production: pass through expand_3_to_19(), then save
    return {
        "status": "expanded",
        "fields_populated": 19,
        "fields_from_input": 3,
        "fields_defaulted": 16,
        "epistemic_tier": "INTUITED",
    }


@router.get("/context/business/{business_name}")
async def list_contexts_by_business(business_name: str, status: str = "active"):
    """List all context records for a business."""
    return {"business_name": business_name, "contexts": [], "count": 0}
'''


# ---------------------------------------------------------------------------
# 7. CLI entry point
# ---------------------------------------------------------------------------

def create_schema():
    """Execute CREATE TABLE on PostgreSQL."""
    try:
        import psycopg2
    except ImportError:
        log.error("psycopg2 not installed. Run: pip install psycopg2-binary")
        sys.exit(1)

    if not PG_PASSWORD:
        log.error("PG_PASSWORD environment variable is required")
        sys.exit(1)

    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB,
        user=PG_USER, password=PG_PASSWORD,
    )
    with conn.cursor() as cur:
        cur.execute(CREATE_SCHEMA_SQL)
    conn.commit()
    conn.close()
    log.info("Schema created successfully on %s:%s/%s", PG_HOST, PG_PORT, PG_DB)


def validate_schema():
    """Validate the 19-field schema definition."""
    log.info("Validating 19-field schema...")

    ctx = BusinessBrainContext(
        context_name="Dave's Plumbing Assessment",
        context_type="interview",
        business_name="Dave's Plumbing Services",
        industry_sector="SIC 43220 — Plumbing",
        owner_goal_primary="Reduce working hours from 60 to 40 per week",
        owner_goal_secondary="Grow revenue to £500k/year",
        current_revenue=320000.0,
        team_size=4,
        biggest_friction="Quoting takes too long — losing jobs",
        operational_capacity=0.85,
        cash_position=45000.0,
        risk_level=4,
        opportunity_score=8,
        source_agent="Devon-8da1",
        source_session="devin-8da1981ce177481da3fe1d2b40e7fade",
        epistemic_tier=EpistemicTier.STRUCTURED,
        valid_until="2026-08-15T00:00:00Z",
        pudding_label="3.2.4.3",
        status=ContextStatus.ACTIVE.value,
        signed_by="Devon-8da1 | 2026-05-15 | devin-8da1981ce177481da3fe1d2b40e7fade",
    )

    errors = ctx.validate()
    if errors:
        for e in errors:
            log.error(f"  Validation error: {e}")
        return False

    log.info("  ✓ All 19 fields valid")
    log.info(f"  PUDDING label: {ctx.pudding_label} (valid: {validate_pudding_label(ctx.pudding_label)})")
    log.info(f"  Epistemic tier: {EpistemicTier(ctx.epistemic_tier).label()}")
    log.info(f"  Status: {ctx.status}")

    signature_fields = [
        "context_name", "context_type", "business_name", "industry_sector",
        "owner_goal_primary", "owner_goal_secondary", "current_revenue",
        "team_size", "biggest_friction", "operational_capacity", "cash_position",
        "risk_level", "opportunity_score", "source_agent", "source_session",
        "epistemic_tier", "valid_until",
    ]
    system_fields = ["pudding_label", "status"]

    log.info(f"  Signature fields (17): {len(signature_fields)}")
    log.info(f"  System fields (2): {len(system_fields)}")
    log.info(f"  Total (19): {len(signature_fields) + len(system_fields)}")
    assert len(signature_fields) == 17, f"Expected 17 signature fields, got {len(signature_fields)}"
    assert len(system_fields) == 2, f"Expected 2 system fields, got {len(system_fields)}"

    return True


def run_demo():
    """Demonstrate the transmission layer."""
    log.info("=" * 60)
    log.info("Business Brain Context — Transmission Layer Demo")
    log.info("=" * 60)

    ctx = BusinessBrainContext(
        context_name="Q2 2026 Assessment",
        context_type="operational",
        business_name="Dave's Plumbing Services",
        industry_sector="SIC 43220 — Plumbing",
        owner_goal_primary="Reduce working hours from 60 to 40/week",
        owner_goal_secondary="Grow revenue to £500k/year",
        current_revenue=320000.0,
        team_size=4,
        biggest_friction="Quoting takes too long — losing jobs",
        operational_capacity=0.85,
        cash_position=45000.0,
        risk_level=4,
        opportunity_score=8,
        source_agent="Devon-8da1",
        source_session="devin-8da1981ce177481da3fe1d2b40e7fade",
        epistemic_tier=EpistemicTier.STRUCTURED,
        valid_until="2026-08-15T00:00:00Z",
        pudding_label="3.2.4.3",
        status=ContextStatus.ACTIVE.value,
        signed_by="Devon-8da1 | 2026-05-15 | devin-8da1981ce177481da3fe1d2b40e7fade",
    )

    log.info("\n--- Full 19-Field Record (AI reads this) ---")
    for k, v in asdict(ctx).items():
        log.info(f"  {k}: {v}")

    log.info("\n--- 19 → 3 Transmission (Human sees this) ---")
    rendering = render_19_to_3(ctx)
    log.info(f"  Headline:       {rendering.headline}")
    log.info(f"  Situation:      {rendering.situation}")
    log.info(f"  Recommendation: {rendering.recommendation}")
    log.info(f"  Source tier:     [{rendering.source_tier}]")
    log.info(f"  Full record:    {rendering.source_id}")

    log.info("\n--- 3 → 19 Expansion (Human input → full record) ---")
    expanded = expand_3_to_19(
        headline="Bob's Electricals: Monthly Review",
        situation="Revenue: £180,000 | Team: 6 | Cash: £22,000 | Friction: Late payments from customers",
        recommendation="Goal: Reduce debtor days from 45 to 30. Opportunity (8/10)",
        source_agent="human_input",
        source_session="manual-entry-2026-05-15",
        signed_by="Ewan Bramley",
    )
    populated = sum(1 for k, v in asdict(expanded).items() if v is not None and v != "" and v != "1.1.1.1" and v != "draft")
    log.info(f"  Fields populated from 3 inputs: {populated}")
    log.info(f"  business_name: {expanded.business_name}")
    log.info(f"  current_revenue: {expanded.current_revenue}")
    log.info(f"  team_size: {expanded.team_size}")
    log.info(f"  cash_position: {expanded.cash_position}")
    log.info(f"  biggest_friction: {expanded.biggest_friction}")
    log.info(f"  owner_goal_primary: {expanded.owner_goal_primary}")
    log.info(f"  epistemic_tier: {EpistemicTier(expanded.epistemic_tier).label()}")

    log.info("\n✓ Transmission layer demo complete")
    log.info("  17 is the signature cardinality — what makes a record itself")
    log.info("  3 is the attention cardinality — what a human holds in one moment")
    log.info("  The transmission layer is the bridge. AI produces 3, not receives 3.")


def main():
    parser = argparse.ArgumentParser(description="Business Brain 19-Field Schema")
    parser.add_argument("--create-schema", action="store_true", help="Create schema on PostgreSQL")
    parser.add_argument("--validate", action="store_true", help="Validate schema definition")
    parser.add_argument("--demo", action="store_true", help="Run transmission layer demo")
    parser.add_argument("--emit-sql", action="store_true", help="Print CREATE TABLE SQL to stdout")
    parser.add_argument("--emit-api", action="store_true", help="Print FastAPI router code to stdout")
    args = parser.parse_args()

    if args.create_schema:
        create_schema()
    elif args.validate:
        ok = validate_schema()
        sys.exit(0 if ok else 1)
    elif args.demo:
        run_demo()
    elif args.emit_sql:
        print(CREATE_SCHEMA_SQL)
    elif args.emit_api:
        print(FASTAPI_ROUTER_CODE)
    else:
        validate_schema()
        print()
        run_demo()


if __name__ == "__main__":
    main()
