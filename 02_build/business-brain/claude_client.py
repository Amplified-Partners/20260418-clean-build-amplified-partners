"""
Claude API Client - Interview Integration

Integrates with Anthropic Claude API for interview conversations.
Uses prompt caching (cache_control: ephemeral) on system prompts to reduce
input token costs by ~90% on repeated calls with the same system prompt.
"""

import os
import json
from typing import List, Dict, Any, Optional
import anthropic
from anthropic import Anthropic


class ClaudeClient:
    """
    Client for Claude API interactions during interviews.

    Design principle: Ask, listen, pick next question.
    NOT therapy - we're gathering business intelligence.

    Prompt caching: system prompts are marked with cache_control so Anthropic
    caches them for up to 5 minutes (ephemeral). Cached tokens cost 10% of
    normal input price. The interview system prompt is ~2000 tokens — at 50
    calls per interview session, caching saves ~90% of those tokens.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found. Set environment variable or pass api_key parameter."
            )

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-6"
        self.max_tokens = 4096

    def _make_system_with_cache(self, system_prompt: str) -> List[Dict]:
        """
        Wrap a system prompt string as a cacheable content block.

        Anthropic requires minimum 1024 tokens to cache. Interview system prompts
        are typically 1500-3000 tokens so this always qualifies.
        Returns a list of content blocks as required by the beta API.
        """
        return [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ]

    def ask_question(
        self,
        conversation_history: List[Dict[str, str]],
        system_prompt: str,
        temperature: float = 0.7,
    ) -> Dict[str, Any]:
        """
        Ask Claude to generate the next question.

        Args:
            conversation_history: List of {role: str, content: str} messages
            system_prompt: System instructions for Claude
            temperature: Randomness (0.0-1.0)

        Returns:
            Dict with question and metadata, including cache usage stats
        """
        formatted_messages = []
        for msg in conversation_history:
            content = msg["content"]
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            formatted_messages.append({"role": msg["role"], "content": content})

        import sys
        print(f"[DEBUG] Sending {len(formatted_messages)} messages to Claude:", file=sys.stderr)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=temperature,
            system=self._make_system_with_cache(system_prompt),
            messages=formatted_messages,
            betas=["prompt-caching-2024-07-31"],
        )

        content = response.content[0].text if response.content else ""

        # Cache stats — log them so we can verify cache hit rate
        cache_creation = getattr(response.usage, "cache_creation_input_tokens", 0)
        cache_read = getattr(response.usage, "cache_read_input_tokens", 0)
        if cache_creation or cache_read:
            print(
                f"[CACHE] created={cache_creation} read={cache_read} "
                f"input={response.usage.input_tokens}",
                file=sys.stderr,
            )

        return {
            "content": content,
            "model": response.model,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "cache_creation_tokens": cache_creation,
                "cache_read_tokens": cache_read,
            },
        }

    def extract_insights(
        self,
        conversation_history: List[Dict[str, str]],
        extraction_prompt: str,
    ) -> List[Dict[str, Any]]:
        """
        Extract structured insights from conversation.

        Returns list of extractions with confidence scores.
        """
        formatted_messages = []
        for msg in conversation_history:
            content = msg["content"]
            if isinstance(content, str):
                content = [{"type": "text", "text": content}]
            formatted_messages.append({"role": msg["role"], "content": content})

        import sys
        print(f"[DEBUG extract_insights] Sending {len(formatted_messages)} messages:", file=sys.stderr)

        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=0.3,
            system=self._make_system_with_cache(extraction_prompt),
            messages=formatted_messages,
            betas=["prompt-caching-2024-07-31"],
        )

        content = response.content[0].text if response.content else ""

        try:
            extractions = json.loads(content)
            return extractions if isinstance(extractions, list) else [extractions]
        except json.JSONDecodeError:
            return [
                {
                    "category": "unknown",
                    "key": "raw_extraction",
                    "value": content,
                    "confidence": 0.5,
                    "reasoning": "Failed to parse structured extraction",
                }
            ]

    def generate_options(
        self,
        context: str,
        question_type: str,
        count: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Generate Rule of Three options for a question.

        Args:
            context: Current conversation context
            question_type: Type of question needing options
            count: Number of options (default 3)

        Returns:
            List of {label, value, confidence} options
        """
        prompt = f"""Generate {count} distinct options for the following context.

Context: {context}
Question type: {question_type}

Return a JSON array of options with this structure:
[
  {{"label": "Short label", "value": "Full value", "confidence": 0.8}},
  ...
]

Options should be:
1. Distinct and mutually exclusive
2. Cover the likely range
3. Ordered by confidence (most likely first)

Return ONLY the JSON array, no other text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            temperature=0.5,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.content[0].text if response.content else "[]"

        try:
            options = json.loads(content)
            return options if isinstance(options, list) else []
        except json.JSONDecodeError:
            return []

    def assess_confidence(
        self,
        statement: str,
        context: str,
    ) -> float:
        """
        Assess confidence level (0.0-1.0) for a statement.

        Used for extraction confidence scoring.
        """
        prompt = f"""Assess confidence level (0.0-1.0) for this statement given the context.

Context: {context}

Statement: {statement}

Consider:
- How explicitly was this stated?
- Is there ambiguity?
- Could it be interpreted differently?

Return ONLY a number between 0.0 and 1.0, nothing else."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=128,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}],
        )

        content = response.content[0].text.strip() if response.content else "0.5"

        try:
            confidence = float(content)
            return max(0.0, min(1.0, confidence))
        except ValueError:
            return 0.5

    def check_completion_readiness(
        self,
        conversation_history: List[Dict[str, str]],
        required_topics: List[str],
    ) -> Dict[str, Any]:
        """
        Check if interview has covered enough ground to complete.

        Returns:
            Dict with {ready: bool, covered: list, missing: list, confidence: float}
        """
        topics_str = ", ".join(required_topics)

        system = "You are assessing interview completeness. Be thorough but not perfectionist."

        prompt = f"""Analyze this interview conversation to determine if it's ready to complete.

Required topics: {topics_str}

For each topic, determine if it was adequately covered.

Return JSON:
{{
  "ready": true/false,
  "covered": ["topic1", "topic2"],
  "missing": ["topic3"],
  "confidence": 0.85,
  "reasoning": "Brief explanation"
}}

Return ONLY the JSON object, no other text."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=0.3,
            system=self._make_system_with_cache(system),
            messages=conversation_history
            + [{"role": "user", "content": prompt}],
            betas=["prompt-caching-2024-07-31"],
        )

        content = response.content[0].text if response.content else "{}"

        try:
            result = json.loads(content)
            return result
        except json.JSONDecodeError:
            return {
                "ready": False,
                "covered": [],
                "missing": required_topics,
                "confidence": 0.0,
                "reasoning": "Failed to parse completion check",
            }
