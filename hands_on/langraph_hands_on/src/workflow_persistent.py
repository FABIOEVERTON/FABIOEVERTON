"""Persistent workflow with SqliteSaver."""

from langgraph.checkpoint.sqlite import SqliteSaver

from src.agents import (
    analyst_node,
    orchestrator_node,
    researcher_node,
    reviewer_node,
    writer_node,
)
from src.states import AgentState, WorkflowPhase
from langgraph.graph import END, StateGraph


def route_after_orchestrator(state: AgentState) -> str:
    """Route based on current phase."""
    current_agent = state.get("current_agent", "")
    phases = {
        WorkflowPhase.RESEARCH.value: "researcher",
        WorkflowPhase.ANALYSIS.value: "analyst",
        WorkflowPhase.WRITING.value: "writer",
        WorkflowPhase.REVIEW.value: "reviewer",
        WorkflowPhase.COMPLETE.value: END,
    }
    return phases.get(current_agent, "orchestrator")


def create_persistent_workflow(db_path: str = "checkpoints.db"):
    """Create workflow with SQLite persistence.

    Args:
        db_path: Path to SQLite database.

    Returns:
        Compiled graph with checkpointer.
    """
    memory = SqliteSaver.from_conn_string(db_path)

    workflow = StateGraph(AgentState)
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("reviewer", reviewer_node)
    workflow.set_entry_point("orchestrator")

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

    workflow.add_edge("researcher", "orchestrator")
    workflow.add_edge("analyst", "orchestrator")
    workflow.add_edge("writer", "orchestrator")
    workflow.add_edge("reviewer", "orchestrator")

    return workflow.compile(checkpointer=memory)


persistent_graph = create_persistent_workflow()
