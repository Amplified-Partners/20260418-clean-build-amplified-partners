# AG2 Executive Team — Amplified Partners C-Suite
#
# The "brain" of Cove. Five AI executives that collaborate on decisions,
# planning, and operational oversight.
#
# Usage:
#     from agents.executive import ExecutiveRunner, ExecRole
#
#     runner = ExecutiveRunner()
#     result = await runner.discuss("What should our Q2 priorities be?")
#     answer = await runner.ask_executive(ExecRole.CFO, "What's our burn rate?")

from .runner import DiscussionResult, ExecMessage, ExecutiveRunner, RunnerConfig
from .team import (
    EXECUTIVE_REGISTRY,
    ExecConfig,
    ExecRole,
    compute_speaker_weights,
    extract_topics,
    get_all_executives,
    get_executive,
    select_speaker,
)

__all__ = [
    "ExecutiveRunner",
    "RunnerConfig",
    "DiscussionResult",
    "ExecMessage",
    "ExecRole",
    "ExecConfig",
    "EXECUTIVE_REGISTRY",
    "get_executive",
    "get_all_executives",
    "select_speaker",
    "compute_speaker_weights",
    "extract_topics",
]
