"""Orchestrator node - coordinates the workflow."""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.states import AgentState, WorkflowPhase


def orchestrator_node(state: AgentState) -> dict:
    """Orchestrator node that coordinates the workflow.

    Args:
        state: Current agent state.

    Returns:
        Updated state with next agent decision.
    """
    settings = get_settings()
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_studio_api_key,
        temperature=0.3,
    )

    # Get current phase based on state
    query = state.get("query", "")
    iteration = state.get("iteration", 0)
    sources = state.get("sources", [])
    insights = state.get("insights", [])
    report_title = state.get("report_title", "")

    # Determine next phase
    if not sources:
        next_phase = WorkflowPhase.RESEARCH
    elif not insights:
        next_phase = WorkflowPhase.ANALYSIS
    elif not report_title:
        next_phase = WorkflowPhase.WRITING
    elif state.get("confidence_score", 0) < 0.7 and iteration < state.get("max_iterations", 5):
        next_phase = WorkflowPhase.REVIEW
    else:
        next_phase = WorkflowPhase.COMPLETE

    # Create orchestrator message
    messages = [
        SystemMessage(
            content="You are the orchestrator of a research system. "
            "Determine the next step based on the current state."
        ),
        HumanMessage(
            content=f"Current state: Query='{query}', Sources={len(sources)}, "
            f"Insights={len(insights)}, Report='{report_title}', "
            f"Iteration={iteration}, Next phase={next_phase.value}"
        ),
    ]

    response = llm.invoke(messages)

    # Update state
    updates = {
        "current_agent": next_phase.value,
        "iteration": iteration + 1,
        "messages": [AIMessage(content=f"Orchestrator: Moving to {next_phase.value}")],
    }

    # Set continuation flag
    if next_phase == WorkflowPhase.COMPLETE:
        updates["should_continue"] = False

    return updates


__all__ = ["orchestrator_node"]
