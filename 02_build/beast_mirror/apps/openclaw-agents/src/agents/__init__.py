"""
Agent Registry
===============
One file per agent. This module discovers and registers them.
To add a new agent: create a .py file in this directory with:
  - AGENT_ID: str
  - AGENT_DESCRIPTION: str
  - AGENT_TOOLS: list[str]
  - def create_agent(model, checkpointer, store) -> CompiledGraph

The registry loads them all at startup. No hardcoded lists.
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Any

from langgraph.graph.state import CompiledStateGraph as CompiledGraph

_REGISTRY: dict[str, dict[str, Any]] = {}


def _discover_agents():
    """Walk this package and register anything with AGENT_ID."""
    package_path = Path(__file__).parent
    for importer, modname, ispkg in pkgutil.iter_modules([str(package_path)]):
        if modname.startswith("_"):
            continue
        module = importlib.import_module(f"agents.{modname}")
        if hasattr(module, "AGENT_ID"):
            _REGISTRY[module.AGENT_ID] = {
                "module": module,
                "description": getattr(module, "AGENT_DESCRIPTION", ""),
                "tools": getattr(module, "AGENT_TOOLS", []),
            }


def get_all_agent_info() -> list[dict[str, str]]:
    if not _REGISTRY:
        _discover_agents()
    return [
        {"agent_id": aid, "description": info["description"], "tools": info["tools"]}
        for aid, info in _REGISTRY.items()
    ]


def get_agent(agent_id: str, **kwargs) -> CompiledGraph:
    """Build and return a compiled agent graph."""
    if not _REGISTRY:
        _discover_agents()
    if agent_id not in _REGISTRY:
        raise ValueError(f"Unknown agent: {agent_id}. Available: {list(_REGISTRY.keys())}")
    return _REGISTRY[agent_id]["module"].create_agent(**kwargs)
