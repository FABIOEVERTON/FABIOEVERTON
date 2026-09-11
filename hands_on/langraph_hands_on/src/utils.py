"""Utility functions for LangGraph workflow management."""

import json
from typing import Any


def get_snapshot(graph, config: dict) -> dict:
    """Get a state snapshot from a compiled graph.

    Args:
        graph: Compiled LangGraph graph.
        config: Thread config with configurable.thread_id.

    Returns:
        Dict with values, next, config, metadata, tasks.
    """
    snapshot = graph.get_state(config)
    return {
        "values": snapshot.values,
        "next": snapshot.next,
        "config": snapshot.config,
        "metadata": snapshot.metadata,
        "created_at": str(snapshot.created_at) if snapshot.created_at else None,
        "tasks": [str(t) for t in snapshot.tasks],
    }


def format_snapshot(snapshot: dict) -> str:
    """Format a snapshot dict as readable JSON string."""
    return json.dumps(snapshot, indent=2, default=str)
