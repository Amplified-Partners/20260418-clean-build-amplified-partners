"""
AG2 Executive GroupChat Runner
===============================
The actual conversation engine. Takes a question or directive,
routes it through the executive team using believability-weighted
speaker selection, and returns a synthesised decision.

This is the "brain" — the sovereign core that runs on Beast.
Third-party models execute inference, but the logic lives here.

Usage:
    runner = ExecutiveRunner()
    result = await runner.discuss("What should our Q2 priorities be?")
    result = await runner.ask_executive(ExecRole.CFO, "What's our burn rate?")
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .team import (
    EXECUTIVE_REGISTRY,
    ExecConfig,
    ExecRole,
    extract_topics,
    get_all_executives,
    get_executive,
    select_speaker,
)


# ─── Configuration ─────────────────────────────────────────────────


@dataclass
class RunnerConfig:
    """Configuration for the executive runner."""
    max_rounds: int = 8            # Max turns in a group discussion
    max_tokens_per_turn: int = 4096
    model_map: dict[str, str] = field(default_factory=lambda: {
        "premium": os.environ.get("COVE_PREMIUM_MODEL", "anthropic/claude-sonnet-4-20250514"),
        "medium": os.environ.get("COVE_MEDIUM_MODEL", "deepseek/deepseek-chat"),
    })
    litellm_base: str = field(
        default_factory=lambda: os.environ.get("LITELLM_API_BASE", "http://localhost:4000")
    )
    litellm_key: str = field(
        default_factory=lambda: os.environ.get("LITELLM_MASTER_KEY", "")
    )
    langfuse_enabled: bool = True
    temperature: float = 0.3


# ─── Message Types ─────────────────────────────────────────────────


@dataclass
class ExecMessage:
    """A single message in the executive conversation."""
    role: ExecRole
    display_name: str
    title: str
    content: str
    timestamp: float = field(default_factory=time.time)
    tokens_used: int = 0
    model: str = ""
    latency_ms: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role.value,
            "speaker": f"{self.display_name} ({self.title})",
            "content": self.content,
            "timestamp": self.timestamp,
            "tokens_used": self.tokens_used,
            "model": self.model,
            "latency_ms": self.latency_ms,
        }


@dataclass
class DiscussionResult:
    """The output of a group discussion."""
    question: str
    messages: list[ExecMessage]
    synthesis: str               # Final summary from CoS
    topics_detected: list[str]
    total_tokens: int = 0
    total_cost_usd: float = 0.0
    total_latency_ms: float = 0.0
    rounds: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "topics": self.topics_detected,
            "rounds": self.rounds,
            "total_tokens": self.total_tokens,
            "total_latency_ms": round(self.total_latency_ms, 1),
            "synthesis": self.synthesis,
            "messages": [m.to_dict() for m in self.messages],
        }


# ─── System Prompt Loader ──────────────────────────────────────────


_prompt_cache: dict[str, str] = {}


def _load_system_prompt(config: ExecConfig) -> str:
    """Load and cache the system prompt for an executive."""
    if config.role.value in _prompt_cache:
        return _prompt_cache[config.role.value]

    prompt_path = Path(config.system_prompt_file)
    if not prompt_path.exists():
        # Try relative to project root
        alt_path = Path(__file__).parent.parent.parent / config.system_prompt_file
        if alt_path.exists():
            prompt_path = alt_path

    if prompt_path.exists():
        content = prompt_path.read_text(encoding="utf-8")
    else:
        # Fallback — use description as prompt
        content = (
            f"You are {config.display_name}, {config.title} at Amplified Partners.\n\n"
            f"{config.description}\n\n"
            "Respond concisely. Be direct. No corporate fluff."
        )

    _prompt_cache[config.role.value] = content
    return content


# ─── LLM Call Layer ────────────────────────────────────────────────


async def _call_llm(
    model: str,
    system_prompt: str,
    messages: list[dict[str, str]],
    config: RunnerConfig,
) -> dict[str, Any]:
    """
    Call LLM through LiteLLM proxy.
    Returns dict with content, tokens, model, latency_ms.
    """
    import httpx

    headers: dict[str, str] = {"Content-Type": "application/json"}
    if config.litellm_key:
        headers["Authorization"] = f"Bearer {config.litellm_key}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            *messages,
        ],
        "max_tokens": config.max_tokens_per_turn,
        "temperature": config.temperature,
    }

    # Add Langfuse tracing metadata if enabled
    if config.langfuse_enabled:
        payload["metadata"] = {
            "trace_name": "executive-discussion",
            "tags": ["cove", "executive-team"],
        }

    start = time.monotonic()

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            f"{config.litellm_base}/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

    latency = (time.monotonic() - start) * 1000

    choice = data.get("choices", [{}])[0]
    usage = data.get("usage", {})

    return {
        "content": choice.get("message", {}).get("content", ""),
        "tokens": usage.get("total_tokens", 0),
        "model": data.get("model", model),
        "latency_ms": round(latency, 1),
    }


# ─── Executive Runner ──────────────────────────────────────────────


class ExecutiveRunner:
    """
    Runs executive team discussions.

    The runner manages the conversation loop:
    1. Detect topics from the input question
    2. Select speakers using believability weights
    3. Each speaker gets the full conversation history
    4. CoS synthesises the final answer
    """

    def __init__(self, config: RunnerConfig | None = None):
        self.config = config or RunnerConfig()

    def _resolve_model(self, exec_config: ExecConfig) -> str:
        """Resolve the actual model ID from the tier."""
        return self.config.model_map.get(
            exec_config.model_tier,
            self.config.model_map["medium"],  # Default to cheaper model
        )

    async def discuss(
        self,
        question: str,
        max_rounds: int | None = None,
        required_speakers: list[ExecRole] | None = None,
    ) -> DiscussionResult:
        """
        Run a full executive team discussion.

        Args:
            question: The question or directive to discuss
            max_rounds: Override max conversation rounds
            required_speakers: Ensure these executives speak at least once
        """
        rounds = max_rounds or self.config.max_rounds
        topics = extract_topics(question)
        messages: list[ExecMessage] = []
        chat_history: list[dict[str, str]] = [
            {"role": "user", "content": question}
        ]

        # Track who has spoken
        speakers_heard: set[ExecRole] = set()
        last_speaker: ExecRole | None = None
        total_tokens = 0
        total_latency = 0.0

        for round_num in range(rounds):
            # Select next speaker
            if required_speakers:
                # Prioritise required speakers who haven't spoken yet
                unheard = [r for r in required_speakers if r not in speakers_heard]
                if unheard:
                    speaker_role = unheard[0]
                else:
                    speaker_role = select_speaker(topics, last_speaker)
            else:
                speaker_role = select_speaker(topics, last_speaker)

            exec_config = get_executive(speaker_role)
            model = self._resolve_model(exec_config)
            system_prompt = _load_system_prompt(exec_config)

            # Add context about the discussion
            discussion_context = (
                f"\n\n---\n"
                f"You are in a group discussion with the executive team.\n"
                f"Topics being discussed: {', '.join(topics)}\n"
                f"This is round {round_num + 1} of {rounds}.\n"
                f"Be concise. Add value or pass. Don't repeat what others said."
            )

            try:
                result = await _call_llm(
                    model=model,
                    system_prompt=system_prompt + discussion_context,
                    messages=chat_history,
                    config=self.config,
                )

                msg = ExecMessage(
                    role=speaker_role,
                    display_name=exec_config.display_name,
                    title=exec_config.title,
                    content=result["content"],
                    tokens_used=result["tokens"],
                    model=result["model"],
                    latency_ms=result["latency_ms"],
                )
                messages.append(msg)
                total_tokens += result["tokens"]
                total_latency += result["latency_ms"]

                # Add to chat history
                chat_history.append({
                    "role": "assistant",
                    "content": f"[{exec_config.display_name} — {exec_config.title}]: {result['content']}",
                })

                speakers_heard.add(speaker_role)
                last_speaker = speaker_role

            except Exception as e:
                # Log error but continue discussion
                msg = ExecMessage(
                    role=speaker_role,
                    display_name=exec_config.display_name,
                    title=exec_config.title,
                    content=f"[Error: {str(e)[:200]}]",
                )
                messages.append(msg)
                last_speaker = speaker_role

        # ─── Synthesis by CoS ──────────────────────────────────────
        cos_config = get_executive(ExecRole.CHIEF_OF_STAFF)
        cos_model = self._resolve_model(cos_config)
        cos_prompt = _load_system_prompt(cos_config)

        synthesis_instruction = (
            "\n\n---\n"
            "The discussion is complete. Synthesise the key points into a clear, "
            "actionable summary for Ewan. Include:\n"
            "1. The decision or recommendation\n"
            "2. Key points of agreement\n"
            "3. Any dissent or risks flagged\n"
            "4. Recommended next actions\n"
            "Be direct. No fluff."
        )

        try:
            synthesis_result = await _call_llm(
                model=cos_model,
                system_prompt=cos_prompt + synthesis_instruction,
                messages=chat_history,
                config=self.config,
            )
            synthesis = synthesis_result["content"]
            total_tokens += synthesis_result["tokens"]
            total_latency += synthesis_result["latency_ms"]
        except Exception as e:
            synthesis = f"[Synthesis failed: {str(e)[:200]}]"

        return DiscussionResult(
            question=question,
            messages=messages,
            synthesis=synthesis,
            topics_detected=topics,
            total_tokens=total_tokens,
            total_latency_ms=total_latency,
            rounds=len(messages),
        )

    async def ask_executive(
        self,
        role: ExecRole,
        question: str,
    ) -> ExecMessage:
        """
        Ask a specific executive a direct question (no group discussion).
        Useful for targeted queries like "Morgan, what's the burn rate?"
        """
        exec_config = get_executive(role)
        model = self._resolve_model(exec_config)
        system_prompt = _load_system_prompt(exec_config)

        direct_context = (
            "\n\n---\n"
            "Ewan is asking you directly. Respond concisely and specifically. "
            "If you need input from another executive, say so."
        )

        result = await _call_llm(
            model=model,
            system_prompt=system_prompt + direct_context,
            messages=[{"role": "user", "content": question}],
            config=self.config,
        )

        return ExecMessage(
            role=role,
            display_name=exec_config.display_name,
            title=exec_config.title,
            content=result["content"],
            tokens_used=result["tokens"],
            model=result["model"],
            latency_ms=result["latency_ms"],
        )

    async def broadcast(
        self,
        message: str,
    ) -> list[ExecMessage]:
        """
        Send a message to all executives and collect their responses.
        Useful for announcements or when you need everyone's perspective.
        """
        import asyncio

        async def _ask_one(role: ExecRole) -> ExecMessage:
            return await self.ask_executive(role, message)

        tasks = [_ask_one(role) for role in ExecRole]
        return await asyncio.gather(*tasks)
