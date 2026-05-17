"""Council engine — parallel dispatch to heterogeneous frontier models.

Protocol (Structured Adversarial Critique, from §1 BRAIN_ARCHITECTURE):
1. Phase 1 — Independent: each model produces recommendation + top 3 reasons
   + top 2 self-objections. No inter-agent context.
2. Phase 2 — Adversarial Exchange (max 2 rounds): only if disagreement.
   Each agent sees others' outputs labelled Model A/B/C (no brand reveal).
3. Phase 3 — Brief to Human: aggregator compiles vote tally, strongest for/against,
   constitutional clauses invoked, dissent summary.

Key evidence constraints:
- Self-reported confidence is near-random (R² = 0.02) — never weight by it
- Inter-model disagreement is the reliable uncertainty signal
- Sycophancy compounds after round 3-4 — max 2 debate rounds
- Same-family councils earn ~half the benefit — heterogeneity non-negotiable
- Council on routine queries is net-negative — selective routing mandatory

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

import httpx

from vellum.council.context import CouncilContext, build_council_prompt

log = logging.getLogger("vellum.council")

# LiteLLM endpoint on Beast (or local dev)
LITELLM_BASE = os.environ.get("LITELLM_BASE_URL", "http://localhost:4000")
LITELLM_KEY = os.environ.get("LITELLM_API_KEY", "")


class Verdict(str, Enum):
    UNANIMOUS = "unanimous"
    MAJORITY = "majority"
    SPLIT = "split"


@dataclass
class CouncilMember:
    """A single frontier model in the council."""

    label: str  # "A", "B", "C" — no brand reveal in debate
    model_id: str  # LiteLLM model routing key
    family: str  # For diversity audit


@dataclass
class MemberResponse:
    """One council member's independent answer."""

    label: str
    model_id: str
    recommendation: str
    raw_response: str
    latency_ms: float = 0.0
    error: str | None = None


@dataclass
class CouncilResult:
    """The aggregated council output."""

    question: str
    verdict: Verdict
    responses: list[MemberResponse] = field(default_factory=list)
    majority_position: str = ""
    minority_report: str = ""
    agreement_score: float = 0.0
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    round_2_needed: bool = False
    round_2_responses: list[MemberResponse] = field(default_factory=list)
    escalate: bool = False
    escalation_reason: str = ""


# Default council composition (May 2026, from §4.2 of the science paper)
DEFAULT_COUNCIL: list[CouncilMember] = [
    CouncilMember(label="A", model_id="gpt-5.5", family="openai"),
    CouncilMember(label="B", model_id="claude-opus-4.7", family="anthropic"),
    CouncilMember(label="C", model_id="gemini-3.1-pro", family="google"),
]


async def _call_model(
    member: CouncilMember,
    prompt: str,
    system_prompt: str = "",
) -> MemberResponse:
    """Call a single council member via LiteLLM."""
    start = asyncio.get_event_loop().time()

    messages: list[dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    headers: dict[str, str] = {"Content-Type": "application/json"}
    if LITELLM_KEY:
        headers["Authorization"] = f"Bearer {LITELLM_KEY}"

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            resp = await client.post(
                f"{LITELLM_BASE}/v1/chat/completions",
                json={
                    "model": member.model_id,
                    "messages": messages,
                    "temperature": 0.3,
                    "max_tokens": 2000,
                },
                headers=headers,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            elapsed = (asyncio.get_event_loop().time() - start) * 1000

            return MemberResponse(
                label=member.label,
                model_id=member.model_id,
                recommendation=content,
                raw_response=content,
                latency_ms=elapsed,
            )
    except Exception as e:
        elapsed = (asyncio.get_event_loop().time() - start) * 1000
        log.error("Council member %s (%s) failed: %s", member.label, member.model_id, e)
        return MemberResponse(
            label=member.label,
            model_id=member.model_id,
            recommendation="",
            raw_response="",
            latency_ms=elapsed,
            error=str(e),
        )


def _classify_agreement(responses: list[MemberResponse]) -> tuple[Verdict, float]:
    """Classify the level of agreement between council members.

    Uses a simple heuristic for v1: check if responses converge on
    the same action/recommendation direction. Full semantic comparison
    would use embeddings (future upgrade).

    Returns (verdict, agreement_score 0.0-1.0).
    """
    valid = [r for r in responses if not r.error]
    if len(valid) < 2:
        return Verdict.SPLIT, 0.0

    # For v1: we look at the first sentence of each recommendation
    # to detect if they converge on the same direction.
    # This is a placeholder for semantic comparison.
    # In production, use embedding cosine similarity.
    first_lines = [r.recommendation.split("\n")[0].lower().strip() for r in valid]

    # Simple keyword overlap heuristic
    if len(valid) == 3:
        # Check pairwise overlap
        overlaps = 0
        for i in range(len(valid)):
            for j in range(i + 1, len(valid)):
                words_i = set(first_lines[i].split())
                words_j = set(first_lines[j].split())
                shared = words_i & words_j
                # If they share >30% of words in opening line, count as agreement
                min_len = min(len(words_i), len(words_j))
                if min_len > 0 and len(shared) / min_len > 0.3:
                    overlaps += 1

        if overlaps == 3:
            return Verdict.UNANIMOUS, 1.0
        elif overlaps >= 1:
            return Verdict.MAJORITY, 0.67
        else:
            return Verdict.SPLIT, 0.33
    elif len(valid) == 2:
        words_0 = set(first_lines[0].split())
        words_1 = set(first_lines[1].split())
        shared = words_0 & words_1
        min_len = min(len(words_0), len(words_1))
        if min_len > 0 and len(shared) / min_len > 0.3:
            return Verdict.MAJORITY, 0.67
        return Verdict.SPLIT, 0.33

    return Verdict.SPLIT, 0.0


def _build_debate_prompt(
    original_question: str,
    responses: list[MemberResponse],
    current_label: str,
) -> str:
    """Build the Round 2 debate prompt for a council member.

    Each agent sees others' outputs labelled Model A/B/C (no brand reveal).
    Instruction: maintain, modify, or reverse — must explicitly rebut
    at least one peer objection or cite the argument that changed their view.
    """
    parts = [f"## Original Question\n{original_question}\n"]
    parts.append("## Other Council Members' Positions (Round 1)\n")

    for r in responses:
        if r.label == current_label:
            continue
        parts.append(f"### Model {r.label}\n{r.recommendation}\n")

    parts.append("""## Your Task (Round 2)

You previously gave your independent recommendation in Round 1.
Now you have seen the other council members' positions.

Instructions:
- Unless convinced by a SPECIFIC argument you had not previously considered, MAINTAIN your initial position.
- You MUST explicitly rebut at least one peer objection OR cite the specific argument that changed your view.
- State clearly: MAINTAIN, MODIFY, or REVERSE your Round 1 position.
- If modifying or reversing, explain exactly which argument convinced you and why.
- Do NOT capitulate to consensus pressure. Disagreement is more valuable than false agreement.""")

    return "\n\n".join(parts)


async def run_council(
    question: str,
    ctx: CouncilContext,
    council: list[CouncilMember] | None = None,
    system_prompt: str = "",
) -> CouncilResult:
    """Run the full council protocol.

    1. Dispatch question to all members in parallel (Round 1, blind)
    2. Assess agreement
    3. If split → Run Round 2 (adversarial debate, max 1 round)
    4. Return aggregated result with verdict + minority report
    """
    members = council or DEFAULT_COUNCIL
    prompt = build_council_prompt(ctx)
    full_prompt = f"{prompt}\n\n## The Question\n{question}"

    # Phase 1 — Independent (parallel dispatch)
    log.info("Council Phase 1: dispatching to %d members", len(members))
    tasks = [_call_model(m, full_prompt, system_prompt) for m in members]
    responses = await asyncio.gather(*tasks)

    # Check for failures
    valid_responses = [r for r in responses if not r.error]
    if len(valid_responses) < 2:
        return CouncilResult(
            question=question,
            verdict=Verdict.SPLIT,
            responses=list(responses),
            escalate=True,
            escalation_reason=f"Only {len(valid_responses)} of {len(members)} members responded",
        )

    # Phase 2 — Agreement classification
    verdict, agreement_score = _classify_agreement(list(responses))
    log.info("Council agreement: %s (score=%.2f)", verdict.value, agreement_score)

    result = CouncilResult(
        question=question,
        verdict=verdict,
        responses=list(responses),
        agreement_score=agreement_score,
    )

    # Determine majority position and minority report
    if verdict == Verdict.UNANIMOUS:
        result.majority_position = valid_responses[0].recommendation
        result.minority_report = ""
    elif verdict == Verdict.MAJORITY:
        # First two that agree form majority (simplified for v1)
        result.majority_position = valid_responses[0].recommendation
        if len(valid_responses) >= 3:
            result.minority_report = valid_responses[2].recommendation
        result.round_2_needed = True
    else:
        # Split — all positions are minority
        result.majority_position = ""
        result.minority_report = "No majority — all positions diverge"
        result.round_2_needed = True
        result.escalate = True
        result.escalation_reason = "Full split after Round 1 — escalate to Ewan"

    # Phase 2 — Adversarial debate (only if needed, max 1 round)
    if result.round_2_needed and not result.escalate:
        log.info("Council Phase 2: adversarial debate round")
        debate_tasks = [
            _call_model(
                m,
                _build_debate_prompt(question, list(responses), m.label),
                system_prompt,
            )
            for m in members
        ]
        round_2 = await asyncio.gather(*debate_tasks)
        result.round_2_responses = list(round_2)

        # Re-assess after debate
        valid_r2 = [r for r in round_2 if not r.error]
        if valid_r2:
            new_verdict, new_score = _classify_agreement(list(round_2))
            if new_score > agreement_score:
                result.verdict = new_verdict
                result.agreement_score = new_score
                log.info(
                    "Council after debate: %s (score=%.2f → %.2f)",
                    new_verdict.value, agreement_score, new_score,
                )
            else:
                # Debate didn't help — escalate
                result.escalate = True
                result.escalation_reason = (
                    "Disagreement persists after debate — escalate to Ewan"
                )

    return result
