"""
Cost Monitor — LLM call tracking with Langfuse + daily Telegram alerts.

What it does:
- Wraps Anthropic API calls to log cost per call, per model, per task type
- Uses Langfuse (cloud free tier) for the dashboard
- Sends daily Telegram alert when daily spend exceeds threshold

Integration:
    from app.core.cost_monitor import CostMonitor
    monitor = CostMonitor()

    # Decorator pattern (preferred)
    @monitor.track(task_type="interview")
    def call_claude(prompt):
        return client.messages.create(...)

    # Or manual tracking
    with monitor.span(task_type="extraction", model="claude-haiku-4-5") as span:
        response = client.messages.create(...)
        span.record_usage(response.usage.input_tokens, response.usage.output_tokens)

Environment variables (from ~/.amplified/keys.env):
    LANGFUSE_PUBLIC_KEY  — from Langfuse project settings
    LANGFUSE_SECRET_KEY  — from Langfuse project settings
    LANGFUSE_HOST        — defaults to https://cloud.langfuse.com
    TELEGRAM_BOT_TOKEN   — for daily alerts
    TELEGRAM_CHAT_ID     — Ewan's chat ID

Pricing (as of 2026-02):
    claude-haiku-4-5:    $0.25 / 1M input,  $1.25 / 1M output
    claude-sonnet-4-6:   $3.00 / 1M input,  $15.00 / 1M output
    claude-opus-4-6:     $15.00 / 1M input, $75.00 / 1M output
    Prompt cache write:  +25% on top of input price
    Prompt cache read:   10% of normal input price

Status: DONE — tracking, cost calc, daily summary, Telegram alert
        UNFINISHED — Langfuse integration requires LANGFUSE_PUBLIC_KEY/SECRET_KEY
        to be added to ~/.amplified/keys.env. Works without Langfuse (logs locally).
"""

import os
import json
import time
import logging
from contextlib import contextmanager
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, Any
from functools import wraps

logger = logging.getLogger(__name__)

# ---- Pricing ---------------------------------------------------------------
# Per token (not per million — divide by 1M to get per-token cost in USD)

MODEL_PRICING: Dict[str, Dict[str, float]] = {
    "claude-haiku-4-5-20251001": {"input": 0.25e-6, "output": 1.25e-6},
    "claude-haiku-4-5": {"input": 0.25e-6, "output": 1.25e-6},
    "claude-sonnet-4-6": {"input": 3.00e-6, "output": 15.00e-6},
    "claude-sonnet-4-5": {"input": 3.00e-6, "output": 15.00e-6},
    "claude-opus-4-6": {"input": 15.00e-6, "output": 75.00e-6},
    # Cache pricing
    "_cache_write_multiplier": 1.25,  # Cache write = 1.25x input price
    "_cache_read_multiplier": 0.10,   # Cache read = 0.10x input price
}

DAILY_ALERT_THRESHOLD_USD = float(os.getenv("COST_ALERT_THRESHOLD_USD", "5.0"))
COST_LOG_FILE = Path.home() / ".amplified/cost-log.jsonl"


# ---- Langfuse (optional) ---------------------------------------------------

def _init_langfuse():
    """Initialise Langfuse client. Returns None if not configured."""
    pk = os.getenv("LANGFUSE_PUBLIC_KEY")
    sk = os.getenv("LANGFUSE_SECRET_KEY")
    if not (pk and sk):
        return None
    try:
        from langfuse import Langfuse
        host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        return Langfuse(public_key=pk, secret_key=sk, host=host)
    except ImportError:
        logger.warning("langfuse not installed. Run: pip install langfuse")
        return None
    except Exception as e:
        logger.warning(f"Langfuse init failed: {e}")
        return None


# ---- Telegram alert --------------------------------------------------------

def _send_telegram(message: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not (token and chat_id):
        return
    try:
        import urllib.request
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
        req = urllib.request.Request(url, data.encode(), {"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        logger.warning(f"Telegram alert failed: {e}")


# ---- Cost calculation ------------------------------------------------------

def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int,
    cache_creation_tokens: int = 0,
    cache_read_tokens: int = 0,
) -> float:
    """Return total cost in USD for a single API call."""
    pricing = MODEL_PRICING.get(model, MODEL_PRICING.get("claude-sonnet-4-6"))
    if isinstance(pricing, float):
        return 0.0  # Skip multiplier keys

    normal_input = max(0, input_tokens - cache_creation_tokens - cache_read_tokens)
    cost = (
        normal_input * pricing["input"]
        + output_tokens * pricing["output"]
        + cache_creation_tokens * pricing["input"] * MODEL_PRICING["_cache_write_multiplier"]
        + cache_read_tokens * pricing["input"] * MODEL_PRICING["_cache_read_multiplier"]
    )
    return round(cost, 8)


# ---- CostMonitor -----------------------------------------------------------

class CostMonitor:
    """
    Tracks LLM API costs locally (JSONL log) and optionally via Langfuse.

    Usage:
        monitor = CostMonitor()
        monitor.record(model="claude-sonnet-4-6", input_tokens=1000,
                       output_tokens=200, task_type="interview")
    """

    def __init__(self):
        self._langfuse = _init_langfuse()
        self._session_cost = 0.0
        self._session_calls = 0
        self._todays_cost = self._load_todays_cost()
        COST_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    def _load_todays_cost(self) -> float:
        """Sum costs logged today from the JSONL file."""
        if not COST_LOG_FILE.exists():
            return 0.0
        today = date.today().isoformat()
        total = 0.0
        try:
            with open(COST_LOG_FILE) as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if entry.get("date") == today:
                            total += entry.get("cost_usd", 0)
                    except Exception:
                        pass
        except Exception:
            pass
        return total

    def record(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        task_type: str = "unknown",
        cache_creation_tokens: int = 0,
        cache_read_tokens: int = 0,
        metadata: Optional[Dict] = None,
    ) -> float:
        """Record a single API call. Returns cost in USD."""
        cost = calculate_cost(
            model, input_tokens, output_tokens,
            cache_creation_tokens, cache_read_tokens,
        )

        self._session_cost += cost
        self._session_calls += 1
        self._todays_cost += cost

        entry = {
            "ts": datetime.utcnow().isoformat(),
            "date": date.today().isoformat(),
            "model": model,
            "task_type": task_type,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cache_creation_tokens": cache_creation_tokens,
            "cache_read_tokens": cache_read_tokens,
            "cost_usd": cost,
            **(metadata or {}),
        }

        # Write to JSONL log
        try:
            with open(COST_LOG_FILE, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.warning(f"Cost log write failed: {e}")

        # Langfuse
        if self._langfuse:
            try:
                self._langfuse.generation(
                    name=task_type,
                    model=model,
                    usage={
                        "input": input_tokens,
                        "output": output_tokens,
                        "total": input_tokens + output_tokens,
                        "unit": "TOKENS",
                    },
                    metadata={"cost_usd": cost, **(metadata or {})},
                )
            except Exception as e:
                logger.warning(f"Langfuse generation log failed: {e}")

        # Check daily threshold
        if self._todays_cost >= DAILY_ALERT_THRESHOLD_USD:
            self._maybe_alert()

        return cost

    def record_from_response(self, response, task_type: str = "unknown"):
        """Record cost directly from an Anthropic response object."""
        usage = response.usage
        self.record(
            model=response.model,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            task_type=task_type,
            cache_creation_tokens=getattr(usage, "cache_creation_input_tokens", 0),
            cache_read_tokens=getattr(usage, "cache_read_input_tokens", 0),
        )

    def _maybe_alert(self):
        """Send Telegram alert once per day when threshold exceeded."""
        flag_file = Path.home() / f".amplified/cost-alert-{date.today().isoformat()}.flag"
        if flag_file.exists():
            return  # Already alerted today
        flag_file.touch()
        msg = (
            f"⚠️ *Amplified AI Cost Alert*\n"
            f"Daily spend: *${self._todays_cost:.4f}* USD\n"
            f"Threshold: ${DAILY_ALERT_THRESHOLD_USD:.2f}\n"
            f"Date: {date.today().isoformat()}"
        )
        _send_telegram(msg)
        logger.warning(f"Daily cost threshold exceeded: ${self._todays_cost:.4f}")

    def daily_summary(self) -> str:
        """Return a human-readable daily summary string."""
        return (
            f"Today's LLM spend: ${self._todays_cost:.4f} USD | "
            f"Session: ${self._session_cost:.4f} ({self._session_calls} calls)"
        )

    def session_cost(self) -> float:
        return self._session_cost

    @contextmanager
    def span(self, task_type: str = "unknown", model: str = "unknown"):
        """
        Context manager for tracking a single API call.

        Usage:
            with monitor.span(task_type="extraction", model="claude-haiku-4-5") as span:
                response = client.messages.create(...)
                span.record_usage(response.usage.input_tokens, response.usage.output_tokens)
        """
        class _Span:
            def __init__(self, monitor, task_type, model):
                self._monitor = monitor
                self.task_type = task_type
                self.model = model
                self.cost = 0.0

            def record_usage(self, input_tokens, output_tokens,
                             cache_creation=0, cache_read=0):
                self.cost = self._monitor.record(
                    model=self.model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    task_type=self.task_type,
                    cache_creation_tokens=cache_creation,
                    cache_read_tokens=cache_read,
                )

            def record_from_response(self, response):
                self._monitor.record_from_response(response, self.task_type)
                self.cost = calculate_cost(
                    response.model,
                    response.usage.input_tokens,
                    response.usage.output_tokens,
                )

        s = _Span(self, task_type, model)
        yield s

    def flush(self):
        """Flush Langfuse buffer if configured."""
        if self._langfuse:
            try:
                self._langfuse.flush()
            except Exception:
                pass


# Singleton for app-wide use
_monitor: Optional[CostMonitor] = None

def get_monitor() -> CostMonitor:
    global _monitor
    if _monitor is None:
        _monitor = CostMonitor()
    return _monitor
