"""VellumEvent — typed event model for system-wide witnessing.

Every meaningful action in the Amplified substrate emits a VellumEvent.
Vellum is permanent — once written, an event cannot be deleted or modified.

Standard fields cover: who did it, what changed, what evidence was used,
what should happen next. The idempotency_key prevents duplicate receipts.

Prior art: Porch-to-Brain bridge v3 JSONL receipts on Beast (live).

Signed-by: Devon-d493 | 2026-05-19 | devin-d49302e4179d43d0892997a7f3a9f57f
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from epistemic_core.tiers import EpistemicTier


class VellumEvent(BaseModel):
    """A single witnessed event in the Amplified substrate.

    Immutable once emitted. Idempotency enforced by idempotency_key.
    """

    # Identity
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
    )

    # Actor and component
    actor: str
    component: str

    # Subject and state transition
    subject_id: str = ""
    previous_state: str = ""
    new_state: str = ""

    # Epistemic provenance
    epistemic_tier: EpistemicTier = EpistemicTier.INTUITED
    provenance_refs: list[str] = Field(default_factory=list)
    evidence_refs: list[str] = Field(default_factory=list)

    # Correlation
    idempotency_key: str = ""
    correlation_id: str = ""
    workflow_id: str = ""

    # Permission and expectation
    permission_scope: str = ""
    expected_next_state: str = ""

    # Freeform metadata
    metadata: dict[str, Any] = Field(default_factory=dict)

    def model_post_init(self, __context: object) -> None:
        if not self.idempotency_key:
            payload = (
                f"{self.event_type}|{self.actor}|{self.component}"
                f"|{self.subject_id}|{self.new_state}"
                f"|{self.timestamp.isoformat()}"
            ).encode("utf-8")
            self.idempotency_key = hashlib.sha256(payload).hexdigest()[:16]

    def to_jsonl_dict(self) -> dict[str, Any]:
        """Serialise for JSONL buffer (fallback persistence)."""
        data = self.model_dump(mode="json")
        data["timestamp"] = self.timestamp.isoformat()
        return data
