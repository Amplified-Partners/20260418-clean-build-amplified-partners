"""Council context builder — assembles the context packet per query.

From the science (§9, §10.2):
Every council query must attach:
- Decision statement (one sentence, deadline, decision-maker)
- Explicit options under consideration (including "do nothing" and "defer")
- Binding constraints (what cannot change)
- Success criteria (what "worked" means)
- Top 2-3 failure modes to avoid
- 2-4 prior analogous decisions with outcomes
- No stated preference from questioner (avoids 50pp sycophancy premium)
- Reasoning instructions (plan, steelman, flag uncertainty)

Devon-b5dc | 2026-05-14
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CouncilContext:
    """The structured context packet sent to each council member."""

    decision_statement: str
    options: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    success_criteria: str = ""
    failure_modes: list[str] = field(default_factory=list)
    prior_decisions: list[str] = field(default_factory=list)
    additional_context: str = ""


_REASONING_INSTRUCTIONS = """Instructions for your response:
1. Plan before answering — identify sub-questions, answer each, then synthesise.
2. Show reasoning step by step. No conclusion without steps.
3. Steelman the opposition — argue against your recommendation before giving it.
4. Flag explicit uncertainty — note where reasoning depends on missing information.
5. Provide your top 3 reasons for your recommendation.
6. Provide your top 2 self-objections (strongest arguments against your own position).
7. Reference any constitutional principles (Five Rods) that apply.
Do NOT ask the questioner what they prefer. Give your independent judgment."""


def build_council_prompt(ctx: CouncilContext) -> str:
    """Build the full prompt sent to each council member.

    Context placement discipline (§9.4, MEASURED):
    - Decision statement and binding constraints at the START
    - Most critical context immediately before the question
    - 3-5 most relevant documents, not 20
    """
    parts: list[str] = []

    parts.append(f"## Decision\n{ctx.decision_statement}")

    if ctx.constraints:
        parts.append("## Binding Constraints (cannot change)")
        for c in ctx.constraints:
            parts.append(f"- {c}")

    if ctx.options:
        parts.append("## Options Under Consideration")
        for i, opt in enumerate(ctx.options, 1):
            parts.append(f"{i}. {opt}")
        parts.append(f"{len(ctx.options) + 1}. Do nothing")
        parts.append(f"{len(ctx.options) + 2}. Defer (gather more information first)")
        parts.append("\nAre there important options not listed above? If so, name them.")

    if ctx.success_criteria:
        parts.append(f"## Success Criteria\n{ctx.success_criteria}")

    if ctx.failure_modes:
        parts.append("## Priority Failure Modes to Avoid")
        for fm in ctx.failure_modes:
            parts.append(f"- {fm}")

    if ctx.prior_decisions:
        parts.append("## Prior Analogous Decisions")
        for pd in ctx.prior_decisions:
            parts.append(f"- {pd}")

    if ctx.additional_context:
        parts.append(f"## Additional Context\n{ctx.additional_context}")

    parts.append(f"\n{_REASONING_INSTRUCTIONS}")

    return "\n\n".join(parts)
