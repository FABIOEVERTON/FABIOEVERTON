"""Tests for the research analyst system."""

import pytest

from src.models import (
    AnalysisResult,
    Insight,
    Report,
    ResearchResult,
    Source,
)


def test_source_creation():
    """Test Source model creation."""
    source = Source(
        url="https://example.com",
        title="Test Source",
        snippet="Test snippet",
    )
    assert source.url == "https://example.com"
    assert source.title == "Test Source"
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


def test_research_result_creation():
    """Test ResearchResult model creation."""
    result = ResearchResult(
        query="test query",
        sources=[],
        summary="test summary",
    )
    assert result.query == "test query"
    assert len(result.sources) == 0


def test_analysis_result_creation():
    """Test AnalysisResult model creation."""
    result = AnalysisResult(
        insights=[],
        comparisons=[],
        trends=["trend1"],
        recommendations=["rec1"],
    )
    assert len(result.trends) == 1
    assert len(result.recommendations) == 1


def test_report_word_count():
    """Test Report word count calculation."""
    report = Report(
        title="Test Report",
        query="test query",
        executive_summary="This is a test summary with five words here.",
        introduction="Introduction text.",
        analysis="Analysis text.",
        conclusions="Conclusions.",
        confidence_score=0.8,
    )
    report.calculate_word_count()
    assert report.word_count > 0
