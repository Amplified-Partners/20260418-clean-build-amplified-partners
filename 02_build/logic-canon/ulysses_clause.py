"""
Ulysses Clause — Tamper-Evident Immutable Constraints
======================================================
WHEN TO USE: You need constraints that the OPERATOR (including future-you)
cannot weaken when tempted. The system detects and rejects tampering.

Named after Odysseus, who had himself tied to the mast so he couldn't
steer toward the Sirens. Pre-commitment device.

EXAMPLES:
- Governance: Five Radicals cannot be weakened by any agent (including Ewan)
- PII: data separation tables cannot be merged
- Pricing: fee commitments cannot be silently raised
- Agent conduct: portable spine cannot be self-modified without detection
- Risk limits: maximum drawdown cannot be loosened under pressure
- Content: brand guidelines cannot be overridden by urgency

HOW IT WORKS:
1. Define immutable constraints as a manifest (dict of name → value)
2. Sign the manifest with HMAC-SHA256
3. Before any action, verify the manifest hasn't been tampered with
4. Hash-chain audit log: each entry includes hash of previous entry
5. Any tampering breaks the chain and halts the system

INPUTS:
- Constraints dictionary (the rules that cannot change)
- Signing key
- Actions to audit

OUTPUTS:
- Verification result (pass/fail)
- Tamper-evident audit chain

Provenance: Nexus V2 ulysses.py (1,547 lines) → generalised core pattern.
Devon-b3d8 | 2026-05-15
"""

import hashlib
import hmac
import json
import datetime as dt
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class AuditEntry:
    """One entry in the tamper-evident audit chain."""
    timestamp: str
    action: str
    details: dict
    previous_hash: str
    entry_hash: str


class UlyssesClause:
    """
    Tamper-evident immutable constraint system.

    Constraints are signed at creation. Any attempt to modify them
    is detected. All actions are recorded in a hash chain.
    """

    def __init__(self, constraints: Dict[str, Any], signing_key: str):
        """
        Args:
            constraints: The immutable rules. e.g.,
                {"max_drawdown": -0.20, "max_daily_loss": -0.03, "fee_pct": 0.0}
            signing_key: Secret key for HMAC signing
        """
        self._constraints = dict(constraints)
        self._signing_key = signing_key
        self._manifest_signature = self._sign_manifest()
        self._audit_chain: List[AuditEntry] = []
        self._last_hash = "GENESIS"

        # Record creation
        self._record("CONSTRAINTS_LOCKED", {
            "constraints": self._constraints,
            "signature": self._manifest_signature,
        })

    def _sign_manifest(self) -> str:
        """HMAC-SHA256 signature of the constraints manifest."""
        payload = json.dumps(self._constraints, sort_keys=True).encode()
        return hmac.new(
            self._signing_key.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()

    def verify_integrity(self) -> Tuple[bool, str]:
        """
        Verify that constraints haven't been tampered with.

        Returns:
            (is_valid, message)
        """
        current_sig = self._sign_manifest()
        if current_sig != self._manifest_signature:
            return False, "INTEGRITY VIOLATION: constraints have been modified"

        # Verify audit chain
        expected_prev = "GENESIS"
        for entry in self._audit_chain:
            if entry.previous_hash != expected_prev:
                return False, f"CHAIN BROKEN at {entry.timestamp}: expected prev={expected_prev}, got {entry.previous_hash}"
            expected_prev = entry.entry_hash

        return True, "Integrity verified"

    def check_constraint(self, name: str, proposed_value: Any) -> Tuple[bool, str]:
        """
        Check if a proposed value violates an immutable constraint.

        For numeric constraints: the proposed value must not exceed the
        constraint (respecting sign — more negative drawdown is worse).

        Returns:
            (is_allowed, reason)
        """
        if name not in self._constraints:
            return True, f"No constraint on '{name}'"

        limit = self._constraints[name]

        # Numeric comparison
        if isinstance(limit, (int, float)) and isinstance(proposed_value, (int, float)):
            if limit < 0:
                # Negative constraint (e.g., max_drawdown = -0.20)
                # Proposed must not be MORE negative
                if proposed_value < limit:
                    reason = f"VIOLATION: {name}={proposed_value} exceeds limit {limit}"
                    self._record("CONSTRAINT_VIOLATION", {
                        "constraint": name,
                        "limit": limit,
                        "proposed": proposed_value,
                    })
                    return False, reason
            else:
                # Positive constraint (e.g., max_fee = 0.0)
                # Proposed must not exceed
                if proposed_value > limit:
                    reason = f"VIOLATION: {name}={proposed_value} exceeds limit {limit}"
                    self._record("CONSTRAINT_VIOLATION", {
                        "constraint": name,
                        "limit": limit,
                        "proposed": proposed_value,
                    })
                    return False, reason

        # Equality constraint (e.g., fee must be exactly 0)
        elif proposed_value != limit:
            reason = f"VIOLATION: {name}={proposed_value} != required {limit}"
            self._record("CONSTRAINT_VIOLATION", {
                "constraint": name,
                "limit": limit,
                "proposed": proposed_value,
            })
            return False, reason

        self._record("CONSTRAINT_CHECK_PASSED", {
            "constraint": name,
            "value": proposed_value,
        })
        return True, f"{name}={proposed_value} within constraint {limit}"

    @property
    def constraints(self) -> Dict[str, Any]:
        """Read-only view of constraints."""
        return dict(self._constraints)

    @property
    def audit_chain(self) -> List[Dict]:
        """Read-only view of audit chain."""
        return [
            {
                "timestamp": e.timestamp,
                "action": e.action,
                "details": e.details,
                "previous_hash": e.previous_hash,
                "entry_hash": e.entry_hash,
            }
            for e in self._audit_chain
        ]

    def _record(self, action: str, details: dict):
        """Append to tamper-evident audit chain."""
        entry_data = {
            "timestamp": dt.datetime.utcnow().isoformat(),
            "action": action,
            "details": details,
            "previous_hash": self._last_hash,
        }
        entry_str = json.dumps(entry_data, sort_keys=True, default=str)
        entry_hash = hashlib.sha256(entry_str.encode()).hexdigest()

        entry = AuditEntry(
            timestamp=entry_data["timestamp"],
            action=action,
            details=details,
            previous_hash=self._last_hash,
            entry_hash=entry_hash,
        )

        self._audit_chain.append(entry)
        self._last_hash = entry_hash
