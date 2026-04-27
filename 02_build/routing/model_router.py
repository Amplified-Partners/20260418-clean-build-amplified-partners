"""
Model Router — classify prompts and route to the right model tier.

Usage:
    from app.core.model_router import ModelRouter
    router = ModelRouter()
    model = router.route(prompt="Extract the business name from: ...", task_type="extraction")
    response = client.messages.create(model=model, ...)

Tiers:
    Haiku  ($0.25/1M input)  — classification, extraction, yes/no, reformatting
    Sonnet ($3.00/1M input)  — reasoning, generation, interview responses, analysis
    Opus                     — not used (overkill, cost prohibitive)

Price ratio: Sonnet is 12x more expensive than Haiku.
Goal: route >70% of calls by volume to Haiku.

Config file: app/core/model_router_config.json (auto-created if missing)
Override via env: MODEL_ROUTER_FORCE=haiku / sonnet (disables routing, forces model)
"""

import os
import json
import re
from typing import Optional
from pathlib import Path


# ---- Models ----------------------------------------------------------------

HAIKU = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"

# Env override — set to "haiku" or "sonnet" to force all calls to one model
_FORCE = os.getenv("MODEL_ROUTER_FORCE", "").lower().strip()

# ---- Default Config --------------------------------------------------------

DEFAULT_CONFIG = {
    # Task type → model mapping (explicit, highest priority)
    "task_type_routing": {
        "classification": HAIKU,
        "extraction": HAIKU,
        "reformatting": HAIKU,
        "yes_no": HAIKU,
        "confidence_score": HAIKU,
        "entity_extraction": HAIKU,
        "sentiment": HAIKU,
        "summarise": HAIKU,
        "summary": HAIKU,
        "interview": SONNET,
        "generation": SONNET,
        "reasoning": SONNET,
        "analysis": SONNET,
        "strategy": SONNET,
        "insight": SONNET,
        "question": SONNET,
        "options": SONNET,
        "completion_check": SONNET,
    },
    # Keyword patterns in prompt → model (lower priority than task_type)
    "keyword_routing": {
        HAIKU: [
            r"\bextract\b",
            r"\bclassif",
            r"\byes or no\b",
            r"\breturn only (a )?(number|json|true|false)",
            r"\breturn ONLY",
            r"\bformat (this|the following)\b",
            r"\bconvert\b",
            r"\bnormalise\b",
            r"\bnormalize\b",
            r"\bparse\b",
            r"\bscore\b.*\b0\.0.*1\.0\b",
        ],
        SONNET: [
            r"\binterview\b",
            r"\bask\b.*\bquestion\b",
            r"\bnext question\b",
            r"\bgenerate\b.*\binsight",
            r"\banalyse\b",
            r"\banalyze\b",
            r"\bstrateg",
            r"\brecommend\b",
            r"\badvice\b",
        ],
    },
    # Token count thresholds — long prompts stay on Sonnet regardless
    "long_prompt_threshold_tokens": 800,
    "default_model": SONNET,
}

CONFIG_PATH = Path(__file__).parent / "model_router_config.json"


def _load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    # Write default config so it's visible/editable
    with open(CONFIG_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    return DEFAULT_CONFIG


# ---- Router ----------------------------------------------------------------

class ModelRouter:
    """
    Routes prompts to the most cost-effective model.

    Priority order:
    1. ENV override (MODEL_ROUTER_FORCE)
    2. Explicit task_type argument
    3. Keyword matching on prompt text
    4. Token count (long → Sonnet)
    5. Default (Sonnet)
    """

    def __init__(self):
        self.config = _load_config()
        self._task_map = self.config.get("task_type_routing", {})
        self._keyword_map = self.config.get("keyword_routing", {})
        self._long_threshold = self.config.get("long_prompt_threshold_tokens", 800)
        self._default = self.config.get("default_model", SONNET)
        self.stats = {"haiku": 0, "sonnet": 0, "total": 0}

        # Pre-compile regexes
        self._haiku_patterns = [
            re.compile(p, re.IGNORECASE)
            for p in self._keyword_map.get(HAIKU, [])
        ]
        self._sonnet_patterns = [
            re.compile(p, re.IGNORECASE)
            for p in self._keyword_map.get(SONNET, [])
        ]

    def route(
        self,
        prompt: str = "",
        task_type: Optional[str] = None,
        system: Optional[str] = None,
    ) -> str:
        """
        Return the model string to use for this call.

        Args:
            prompt: The user-facing prompt text (used for keyword matching)
            task_type: Explicit task type (extraction, interview, classification, etc.)
            system: System prompt (checked for keywords if prompt is short)

        Returns:
            Model string: HAIKU or SONNET
        """
        self.stats["total"] += 1

        # 1. ENV override
        if _FORCE in ("haiku",):
            model = HAIKU
        elif _FORCE in ("sonnet",):
            model = SONNET
        # 2. Explicit task type
        elif task_type and task_type.lower() in self._task_map:
            model = self._task_map[task_type.lower()]
        else:
            # 3. Keyword matching
            text = (prompt or "") + " " + (system or "")
            model = self._keyword_match(text)

        # Track stats
        if model == HAIKU:
            self.stats["haiku"] += 1
        else:
            self.stats["sonnet"] += 1

        return model

    def _keyword_match(self, text: str) -> str:
        """Check text against keyword patterns. Sonnet patterns take priority."""
        # Sonnet first — if it looks like reasoning/generation, don't downgrade
        for pattern in self._sonnet_patterns:
            if pattern.search(text):
                return SONNET
        for pattern in self._haiku_patterns:
            if pattern.search(text):
                return HAIKU
        # Rough token estimate: ~1 token per 4 chars
        estimated_tokens = len(text) // 4
        if estimated_tokens > self._long_threshold:
            return SONNET
        return self._default

    def haiku_rate(self) -> float:
        total = self.stats["total"]
        return self.stats["haiku"] / total if total > 0 else 0.0

    def log_stats(self):
        print(
            f"[ModelRouter] total={self.stats['total']} "
            f"haiku={self.stats['haiku']} ({self.haiku_rate():.1%}) "
            f"sonnet={self.stats['sonnet']}"
        )
