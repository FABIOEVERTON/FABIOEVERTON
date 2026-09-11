"""Tests for the LangGraph multi-agent system."""

import pytest

from src.states import (
    AgentState,
    Insight,
    ResearchSource,
    WorkflowConfig,
    WorkflowPhase,
    create_initial_state,
)


def test_create_initial_state():
    """Test initial state creation."""
    state = create_initial_state("test query")
    assert state["query"] == "test query"
    assert state["sources"] == []
    assert state["iteration"] == 0
    assert state["should_continue"] is True


def test_workflow_phase_enum():
    """Test WorkflowPhase enum."""
    assert WorkflowPhase.INIT.value == "init"
    assert WorkflowPhase.RESEARCH.value == "research"
    assert WorkflowPhase.COMPLETE.value == "complete"


def test_research_source_creation():
    """Test ResearchSource model creation."""
    source = ResearchSource(
        url="https://example.com",
        title="Test Source",
        snippet="Test snippet",
    )
    assert source.url == "https://example.com"
    assert source.credibility_score == 0.5


def test_insight_creation():
    """Test Insight model creation."""
    insight = Insight(
        topic="Test Topic",
        finding="Test finding",
        confidence=0.85,
    )
    assert insight.topic == "Test Topic"
    assert insight.confidence == 0.85


def test_workflow_config():
    """Test WorkflowConfig model creation."""
    config = WorkflowConfig(max_sources=5, confidence_threshold=0.8)
    assert config.max_sources == 5
    assert config.confidence_threshold == 0.8
