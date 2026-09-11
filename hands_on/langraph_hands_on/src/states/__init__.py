"""State definitions for LangGraph workflows."""

from enum import Enum
from typing import Annotated, Any, Literal, Optional, TypedDict

from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class AgentState(TypedDict):
    """Main state for the multi-agent system."""

    # Messages history (automatically accumulated)
    messages: Annotated[list[Any], add_messages]

    # Current agent
    current_agent: str

    # Research data
    query: str
    sources: list[dict]
    research_summary: str

    # Analysis data
    insights: list[dict]
    comparisons: list[dict]
    trends: list[str]
    recommendations: list[str]

    # Report data
    report_title: str
    executive_summary: str
    introduction: str
    analysis: str
    conclusions: str
    confidence_score: float

    # Control flow
    iteration: int
    max_iterations: int
    should_continue: bool
    error: Optional[str]


class WorkflowPhase(str, Enum):
    """Phases of the research workflow."""

    INIT = "init"
    RESEARCH = "research"
    ANALYSIS = "analysis"
    REVIEW = "review"
    WRITING = "writing"
    COMPLETE = "complete"


class ResearchSource(BaseModel):
    """A research source."""

    url: str
    title: str
    snippet: str
    content: Optional[str] = None
    credibility_score: float = Field(ge=0, le=1, default=0.5)


class Insight(BaseModel):
    """An analysis insight."""

    topic: str
    finding: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class WorkflowConfig(BaseModel):
    """Configuration for the workflow."""

    max_sources: int = 10
    max_iterations: int = 5
    confidence_threshold: float = 0.7
    gemini_model: str = "gemini-2.0-flash"


def create_initial_state(query: str) -> AgentState:
    """Create initial state for a new workflow.

    Args:
        query: Research query.

    Returns:
        Initial AgentState.
    """
    return {
        "messages": [],
        "current_agent": "orchestrator",
        "query": query,
        "sources": [],
        "research_summary": "",
        "insights": [],
        "comparisons": [],
        "trends": [],
        "recommendations": [],
        "report_title": "",
        "executive_summary": "",
        "introduction": "",
        "analysis": "",
        "conclusions": "",
        "confidence_score": 0.0,
        "iteration": 0,
        "max_iterations": 5,
        "should_continue": True,
        "error": None,
    }


__all__ = [
    "AgentState",
    "Insight",
    "ResearchSource",
    "WorkflowConfig",
    "WorkflowPhase",
    "create_initial_state",
]
