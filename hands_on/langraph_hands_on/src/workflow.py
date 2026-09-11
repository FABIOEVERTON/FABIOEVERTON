"""Main workflow graph for the multi-agent system."""

from typing import Literal

from langgraph.graph import END, StateGraph

from src.agents import (
    analyst_node,
    orchestrator_node,
    researcher_node,
    reviewer_node,
    writer_node,
)
from src.states import AgentState, WorkflowPhase


def should_continue(state: AgentState) -> Literal["orchestrator", "__end__"]:
    """Determine if the workflow should continue.

    Args:
        state: Current agent state.

    Returns:
        Next node to execute or END.
    """
    if state.get("should_continue", True) and state.get("iteration", 0) < state.get("max_iterations", 5):
        return "orchestrator"
    return END


def route_after_orchestrator(state: AgentState) -> str:
    """Route to the appropriate agent after orchestrator.

    Args:
        state: Current agent state.

    Returns:
        Next node to execute.
    """
    current_agent = state.get("current_agent", "")

    if current_agent == WorkflowPhase.RESEARCH.value:
        return "researcher"
    elif current_agent == WorkflowPhase.ANALYSIS.value:
        return "analyst"
    elif current_agent == WorkflowPhase.WRITING.value:
        return "writer"
    elif current_agent == WorkflowPhase.REVIEW.value:
        return "reviewer"
    elif current_agent == WorkflowPhase.COMPLETE.value:
        return END
    else:
        return "orchestrator"


def create_workflow() -> StateGraph:
    """Create the LangGraph workflow.

    Returns:
        Compiled StateGraph.
    """
    # Create the graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("reviewer", reviewer_node)

    # Set entry point
    workflow.set_entry_point("orchestrator")

    # Add conditional edges from orchestrator
    workflow.add_conditional_edges(
        "orchestrator",
        route_after_orchestrator,
        {
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer",
            "reviewer": "reviewer",
            END: END,
        },
    )

    # All agents go back to orchestrator for next decision
    workflow.add_edge("researcher", "orchestrator")
    workflow.add_edge("analyst", "orchestrator")
    workflow.add_edge("writer", "orchestrator")
    workflow.add_edge("reviewer", "orchestrator")

    # Compile the graph
    return workflow.compile()


# Create the compiled graph
graph = create_workflow()


__all__ = ["create_workflow", "graph"]
