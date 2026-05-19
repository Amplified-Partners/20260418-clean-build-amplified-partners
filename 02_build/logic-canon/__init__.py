"""
Logic Canon — Amplified Partners
=================================
Domain-agnostic algorithmic patterns extracted from production systems.
Each module solves one problem. Import what you need.

Design principle: Python holds the safety net. AI holds the intelligence.
These modules are deterministic guards — thresholds, constraints, detection.
They do not think. They protect.

Provenance: Extracted from Nexus V2 (trading engine), generalised by
removing domain-specific language. The maths is identical; the framing
is universal.

Dependencies: numpy, pandas (both already in every Amplified system).

Discovery: See REGISTRY.md for "I have problem X → use module Y" routing.

Devon-b3d8 | 2026-05-15
"""

from . import circuit_breaker
from . import shadow_tester
from . import regime_detector
from . import correlation_monitor
from . import signal_normaliser
from . import ulysses_clause
