"""
Secrets Manager — Amplified Partners CRM

Two-layer secrets model:
  Layer 1 (now):   keys.env → loaded into in-memory cache → os.environ populated
  Layer 2 (after): macOS Keychain → OP_SERVICE_ACCOUNT_TOKEN → 1Password 'op' CLI → cache

The 1Password path activates automatically once:
  1. Ewan creates the "Eli" Service Account and stores the token in Keychain:
       security add-generic-password -a eli -s "1password-service-account" -w "ops_TOKEN"
  2. The 'op' CLI is installed (brew install 1password-cli)

Until then: graceful fallback to keys.env. No code changes needed at activation.

Usage (CRM internal):
    from app.core.secrets import secrets

    # Get a single value (lazy — fetches from 1Password if configured)
    key = secrets.get("ANTHROPIC_API_KEY")

    # Populate os.environ for code that uses os.getenv() (backward compat)
    secrets.load_into_environ()

Status:
    DONE — keys.env loading, in-memory cache, os.environ population, access logging
    DONE — 1Password integration stub (activates when op CLI + Keychain token present)
    UNFINISHED — 1Password item mapping (needs vault item names once Ewan creates them)
"""

import os
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ── 1Password vault/item mapping ────────────────────────────────────────────
# Maps env var name → 1Password op:// reference.
# Populate after Ewan creates items in the "Amplified Secrets" vault.
# Format: "op://Vault Name/Item Name/field"
_OP_MAPPING: dict[str, str] = {
    # "ANTHROPIC_API_KEY": "op://Amplified Secrets/Anthropic/credential",
    # "BRAVE_API_KEY":     "op://Amplified Secrets/Brave Search/credential",
    # "LINEAR_API_KEY":    "op://Amplified Secrets/Linear/credential",
    # etc. — uncomment as items are created in 1Password
}

_KEYS_ENV = Path.home() / ".amplified/keys.env"
_KEYCHAIN_SERVICE = "1password-service-account"
_KEYCHAIN_ACCOUNT = "eli"


# ── SecretsManager ───────────────────────────────────────────────────────────

class SecretsManager:
    """
    Unified secrets access for the Amplified CRM.

    Priority (highest to lowest):
      1. 1Password via op CLI (when configured)
      2. os.environ (manually set, or from previous load_into_environ())
      3. ~/.amplified/keys.env (transition period)
    """

    def __init__(self):
        self._cache: dict[str, str] = {}
        self._op_available: Optional[bool] = None  # None = not yet checked
        self._op_token: Optional[str] = None
        self._access_log: list[dict] = []

        self._load_keys_env()

    # ── Baseline loading ─────────────────────────────────────────────────────

    def _load_keys_env(self):
        """Load keys.env into cache as the baseline (lowest priority)."""
        if not _KEYS_ENV.exists():
            return
        try:
            for line in _KEYS_ENV.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                k = k.strip()
                v = v.strip()
                if k and v and k not in self._cache:
                    self._cache[k] = v
        except Exception as e:
            logger.warning(f"[Secrets] Failed to load keys.env: {e}")

    # ── 1Password integration ────────────────────────────────────────────────

    def _check_op_available(self) -> bool:
        """Check once if op CLI is installed and Keychain token is present."""
        if self._op_available is not None:
            return self._op_available

        # Check op CLI is installed
        try:
            result = subprocess.run(
                ["which", "op"], capture_output=True, timeout=2
            )
            if result.returncode != 0:
                self._op_available = False
                return False
        except Exception:
            self._op_available = False
            return False

        # Try to get service account token from macOS Keychain
        try:
            result = subprocess.run(
                [
                    "security", "find-generic-password",
                    "-a", _KEYCHAIN_ACCOUNT,
                    "-s", _KEYCHAIN_SERVICE,
                    "-w",
                ],
                capture_output=True,
                text=True,
                timeout=3,
            )
            if result.returncode == 0 and result.stdout.strip():
                self._op_token = result.stdout.strip()
                self._op_available = True
                logger.info("[Secrets] 1Password service account token found in Keychain")
                return True
        except Exception:
            pass

        self._op_available = False
        return False

    def _fetch_from_1password(self, key: str) -> Optional[str]:
        """Fetch a secret from 1Password using op CLI."""
        op_ref = _OP_MAPPING.get(key)
        if not op_ref or not self._op_token:
            return None

        try:
            env = {**os.environ, "OP_SERVICE_ACCOUNT_TOKEN": self._op_token}
            result = subprocess.run(
                ["op", "read", op_ref],
                capture_output=True,
                text=True,
                env=env,
                timeout=5,
            )
            if result.returncode == 0:
                value = result.stdout.strip()
                if value:
                    self._cache[key] = value  # cache in memory
                    return value
        except Exception as e:
            logger.warning(f"[Secrets] 1Password fetch failed for {key}: {e}")

        return None

    # ── Public API ───────────────────────────────────────────────────────────

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get a secret by environment variable name.

        Checks (in order): 1Password → os.environ → keys.env cache → default.
        Every access is logged for audit trail.
        """
        # Try 1Password first (if configured)
        if self._check_op_available() and key in _OP_MAPPING:
            value = self._fetch_from_1password(key)
            if value:
                self._log_access(key, source="1password")
                return value

        # Check os.environ (may have been set externally)
        value = os.environ.get(key)
        if value:
            self._log_access(key, source="environ")
            return value

        # Fall back to keys.env cache
        value = self._cache.get(key)
        if value:
            self._log_access(key, source="keys_env")
            return value

        self._log_access(key, source="not_found")
        if default is not None:
            return default

        logger.warning(f"[Secrets] {key} not found in any source")
        return None

    def load_into_environ(self):
        """
        Populate os.environ from the cache.

        Backward-compat drop-in for the old keys.env loading block.
        Call once at app startup. Does not override already-set env vars.
        """
        for k, v in self._cache.items():
            if k not in os.environ:
                os.environ[k] = v

    def get_all_keys(self) -> list[str]:
        """Return list of known key names (not values)."""
        return list(self._cache.keys())

    def _log_access(self, key: str, source: str):
        entry = {
            "ts": datetime.utcnow().isoformat(),
            "key": key,
            "source": source,
        }
        self._access_log.append(entry)
        # Keep log bounded
        if len(self._access_log) > 1000:
            self._access_log = self._access_log[-500:]

    def access_log(self) -> list[dict]:
        """Return copy of access log for audit/debugging."""
        return list(self._access_log)


# ── Singleton ────────────────────────────────────────────────────────────────

secrets = SecretsManager()

# Auto-populate os.environ on import so existing os.getenv() calls work.
# This is the zero-friction migration path — existing code needs no changes.
secrets.load_into_environ()
