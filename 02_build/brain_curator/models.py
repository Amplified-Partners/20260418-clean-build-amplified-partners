"""Pydantic models for all brain_curator entities.

These mirror the database tables from migration 008 and provide
validation at the application layer.

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_uuid() -> uuid.UUID:
    return uuid.uuid4()


class Document(BaseModel):
    document_id: uuid.UUID = Field(default_factory=_new_uuid)
    source_path: str
    source_system: str = "amplified-pipeline-v0.3"
    source_id: str | None = None
    file_hash_sha256: str
    raw_frontmatter: dict[str, Any] = Field(default_factory=dict)
    fm_metadata: dict[str, Any] = Field(default_factory=dict)
    title: str | None = None
    document_type: str | None = None
    created_at: datetime = Field(default_factory=_utcnow)
    ingested_at: datetime = Field(default_factory=_utcnow)
    pipeline_version: str = "amplified-pipeline-v0.3"
    chunk_count: int = 0
    status: str = "inventoried"


class DedupeCluster(BaseModel):
    cluster_id: uuid.UUID = Field(default_factory=_new_uuid)
    cluster_type: str  # 'exact' | 'metadata_family'
    method: str  # 'sha256' | 'title_path' | 'source_timestamp'
    canonical_member_id: uuid.UUID | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)


class DedupeMember(BaseModel):
    member_id: uuid.UUID = Field(default_factory=_new_uuid)
    cluster_id: uuid.UUID
    chunk_id: uuid.UUID
    member_role: str = "member"  # 'canonical' | 'member'
    confidence: float = 1.0
    created_at: datetime = Field(default_factory=_utcnow)


class Packet(BaseModel):
    packet_id: uuid.UUID = Field(default_factory=_new_uuid)
    packet_type: str
    title: str | None = None
    summary: str | None = None
    status: str = "draft"
    route: str | None = None
    epistemic_tier: str | None = None
    claim_status: str | None = None
    decision_state: str | None = None
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    last_verified_at: datetime | None = None
    source_document_id: uuid.UUID | None = None
    canonical_packet_id: uuid.UUID | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)
    updated_at: datetime = Field(default_factory=_utcnow)


class Evidence(BaseModel):
    evidence_id: uuid.UUID = Field(default_factory=_new_uuid)
    packet_id: uuid.UUID
    chunk_id: uuid.UUID
    evidence_role: str = "supports"
    confidence: float = 1.0
    created_at: datetime = Field(default_factory=_utcnow)


class Relationship(BaseModel):
    relationship_id: uuid.UUID = Field(default_factory=_new_uuid)
    source_packet_id: uuid.UUID
    target_packet_id: uuid.UUID
    predicate: str
    evidence_count: int = 0
    confidence: float = 1.0
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=_utcnow)


class CurationRun(BaseModel):
    run_id: str
    stage: str
    started_at: datetime = Field(default_factory=_utcnow)
    completed_at: datetime | None = None
    code_version: str = "brain-curator-v0.1"
    config_hash: str | None = None
    input_scope: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)
    status: str = "running"
    error: str | None = None


class ValidationSample(BaseModel):
    sample_id: uuid.UUID = Field(default_factory=_new_uuid)
    packet_id: uuid.UUID
    verdict: str | None = None
    reviewed_by: str | None = None
    reviewed_at: datetime | None = None
    notes: str | None = None
    metrics: dict[str, Any] = Field(default_factory=dict)
