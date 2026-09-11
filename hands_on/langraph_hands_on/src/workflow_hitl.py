"""HITL workflow with interrupt and state management."""

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, StateGraph

from src.agents import (
    analyst_node,
    orchestrator_node,
    researcher_node,
    reviewer_node,
    writer_node,
)
from src.states import AgentState, WorkflowPhase


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


def create_hitl_workflow(db_path: str = "hitl_checkpoints.db"):
    """Create workflow with Human-in-the-Loop.

    Uses interrupt_before to pause at reviewer for human approval.

    Args:
        db_path: Path to SQLite database.

    Returns:
        Compiled graph with HITL support.
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

    # Compile with interrupt before reviewer (HITL)
    return workflow.compile(
        checkpointer=memory,
        interrupt_before=["reviewer"],
    )


hitl_graph = create_hitl_workflow()


def run_with_approval(query: str, thread_id: str = "default"):
    """Run workflow with human approval at reviewer step.

    Args:
        query: Research query.
        thread_id: Unique thread identifier.

    Returns:
        Final state after human approval.
    """
    from src.states import create_initial_state

    config = {"configurable": {"thread_id": thread_id}}
    initial_state = create_initial_state(query)

    # Run until interrupt (before reviewer)
    for step in hitl_graph.stream(initial_state, config):
        pass

    # Get state snapshot
    snapshot = hitl_graph.get_state(config)
    print(f"Paused at: {snapshot.next}")

    # Human approves and provides feedback
    hitl_graph.update_state(config, {
        "messages": [("human", "Aprovado. Prosseguir com a revisão.")]
    })

    # Continue execution
    for step in hitl_graph.stream(None, config):
        pass

    return hitl_graph.get_state(config)
