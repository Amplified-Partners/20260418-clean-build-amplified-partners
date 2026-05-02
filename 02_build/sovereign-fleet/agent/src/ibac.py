"""
IBAC (Intent-Based Access Control) — Cedar policy engine.

Evaluates authorization requests against Cedar policy files.
This is a purpose-built evaluator for the Sovereign Fleet's fixed
action/entity/resource vocabulary — not a general Cedar interpreter.

Policy files are loaded once at startup from the policy directory.
The engine supports the four constructs used in prod.cedar:
  - permit(principal, action, resource) [with optional when clause]
  - forbid(principal, action, resource)
  - Role membership (Agent in Role::"Agent")
  - Context conditions (approved_by_analyst, approved_by_arbiter, intent_token_valid)

Authored by Devon | 2026-05-02 | devin-701075c43e444229aa32f993bf60b36a
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class Decision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"


@dataclass
class AuthzRequest:
    """An authorization request to be evaluated against Cedar policies."""

    principal: str  # e.g. "Kimmy", "Alpha", "Charlie"
    action: str  # e.g. "read_file", "write_file", "merge_pr"
    resource: str  # e.g. "/workspace/worktrees/fix-123/main.py"
    context: dict[str, bool] = field(default_factory=dict)


@dataclass
class AuthzResponse:
    """The result of a policy evaluation."""

    decision: Decision
    reason: str
    matched_rule: str = ""


@dataclass
class PolicyRule:
    """Parsed Cedar rule."""

    kind: str  # "permit" or "forbid"
    principals: list[str]  # Agent names or ["*"] for any
    role_match: bool  # True if principal in Role::"Agent" (matches all)
    actions: list[str]
    resource_scope: str  # Directory/file prefix, "*" for any, or "|"-separated files
    conditions: dict[str, bool] = field(default_factory=dict)
    raw: str = ""


class PolicyEngine:
    """Evaluates authorization requests against loaded Cedar policies."""

    def __init__(self) -> None:
        self._rules: list[PolicyRule] = []
        self._loaded_files: list[str] = []

    @property
    def rule_count(self) -> int:
        return len(self._rules)

    def load_directory(self, policy_dir: str) -> int:
        """Load all .cedar files from a directory. Returns count of rules loaded."""
        p = Path(policy_dir)
        if not p.is_dir():
            logger.warning("Policy directory does not exist: %s", policy_dir)
            return 0

        count = 0
        for cedar_file in sorted(p.glob("*.cedar")):
            rules = self._parse_file(cedar_file)
            self._rules.extend(rules)
            self._loaded_files.append(str(cedar_file))
            count += len(rules)
            logger.info("Loaded %d rules from %s", len(rules), cedar_file.name)

        return count

    def load_file(self, path: str) -> int:
        """Load a single .cedar file. Returns count of rules loaded."""
        cedar_file = Path(path)
        if not cedar_file.exists():
            logger.warning("Policy file not found: %s", path)
            return 0

        rules = self._parse_file(cedar_file)
        self._rules.extend(rules)
        self._loaded_files.append(str(cedar_file))
        return len(rules)

    def evaluate(self, request: AuthzRequest) -> AuthzResponse:
        """
        Evaluate an authorization request.

        Cedar semantics: forbid overrides permit.
        1. Check all forbid rules first — any match = DENY.
        2. Check permit rules — at least one must match = ALLOW.
        3. No match = DENY (default-deny).
        """
        for rule in self._rules:
            if rule.kind != "forbid":
                continue
            if self._matches(rule, request):
                return AuthzResponse(
                    decision=Decision.DENY,
                    reason=f"Blocked by forbid rule: {rule.raw[:80]}",
                    matched_rule=rule.raw,
                )

        for rule in self._rules:
            if rule.kind != "permit":
                continue
            if self._matches(rule, request):
                return AuthzResponse(
                    decision=Decision.ALLOW,
                    reason=f"Allowed by permit rule: {rule.raw[:80]}",
                    matched_rule=rule.raw,
                )

        return AuthzResponse(
            decision=Decision.DENY,
            reason="No permit rule matched (default deny)",
        )

    def _matches(self, rule: PolicyRule, req: AuthzRequest) -> bool:
        """Check if a rule matches the request."""
        # Principal
        if not rule.role_match and "*" not in rule.principals:
            if req.principal not in rule.principals:
                return False

        # Action
        if "*" not in rule.actions:
            if req.action not in rule.actions:
                return False

        # Resource
        if rule.resource_scope != "*":
            if "|" in rule.resource_scope:
                resources = rule.resource_scope.split("|")
                if not any(req.resource == r for r in resources):
                    return False
            elif not (
                req.resource == rule.resource_scope
                or req.resource.startswith(rule.resource_scope + "/")
            ):
                return False

        # Context conditions
        for key, required_val in rule.conditions.items():
            if req.context.get(key, False) != required_val:
                return False

        return True

    # ── Cedar parser ───────────────────────────────────────────────

    def _parse_file(self, path: Path) -> list[PolicyRule]:
        """Parse a .cedar file into PolicyRule objects."""
        content = path.read_text(encoding="utf-8")
        lines = [line for line in content.split("\n") if not line.strip().startswith("//")]
        clean = "\n".join(lines)

        rules: list[PolicyRule] = []
        for block in re.split(r"(?=(?:permit|forbid)\s*\()", clean):
            block = block.strip()
            if not block:
                continue
            rule = self._parse_block(block)
            if rule:
                rules.append(rule)
        return rules

    def _parse_block(self, block: str) -> PolicyRule | None:
        """Parse a single permit/forbid block."""
        if block.startswith("permit"):
            kind = "permit"
        elif block.startswith("forbid"):
            kind = "forbid"
        else:
            return None

        raw = re.sub(r"\s+", " ", block).strip()

        # Principals
        principals: list[str] = []
        role_match = False
        if "principal in Role" in block:
            role_match = True
            principals = ["*"]
        elif "principal in [" in block:
            m = re.search(r"principal\s+in\s+\[([^\]]+)\]", block)
            if m:
                principals = re.findall(r'Agent::"(\w+)"', m.group(1))
        elif "principal ==" in block:
            m = re.search(r'principal\s*==\s*Agent::"(\w+)"', block)
            if m:
                principals = [m.group(1)]
        elif "principal" in block:
            principals = ["*"]
            role_match = True

        # Actions
        actions: list[str] = []
        if "action in [" in block:
            m = re.search(r"action\s+in\s+\[([^\]]+)\]", block)
            if m:
                actions = re.findall(r'Action::"(\w+)"', m.group(1))
        elif "action ==" in block:
            m = re.search(r'Action::"(\w+)"', block)
            if m:
                actions = [m.group(1)]
        elif "action" in block and kind == "forbid":
            actions = ["*"]

        # Resources
        resource_scope = "*"
        dir_match = re.search(r'Directory::"([^"]+)"', block)
        if dir_match:
            resource_scope = dir_match.group(1)
        else:
            file_matches = re.findall(r'File::"([^"]+)"', block)
            if file_matches:
                resource_scope = "|".join(file_matches)

        # When conditions
        conditions: dict[str, bool] = {}
        when_match = re.search(r"when\s*\{([^}]+)\}", block)
        if when_match:
            for cond in re.findall(r"context\.(\w+)\s*==\s*(true|false)", when_match.group(1)):
                conditions[cond[0]] = cond[1] == "true"

        if not principals and not actions:
            return None

        return PolicyRule(
            kind=kind,
            principals=principals,
            role_match=role_match,
            actions=actions if actions else ["*"],
            resource_scope=resource_scope,
            conditions=conditions,
            raw=raw,
        )
