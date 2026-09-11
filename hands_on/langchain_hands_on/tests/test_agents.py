"""Tests for agent modules."""

import pytest
from unittest.mock import MagicMock, patch

from src.models import ResearchResult, Source


class TestResearcherAgent:
    """Tests for ResearcherAgent."""

    def test_import(self):
        """Test researcher agent can be imported."""
        from src.agents.researcher import ResearcherAgent
        assert ResearcherAgent is not None


class TestAnalystAgent:
    """Tests for AnalystAgent."""

    def test_import(self):
        """Test analyst agent can be imported."""
        from src.agents.analyst import AnalystAgent
        assert AnalystAgent is not None


class TestWriterAgent:
    """Tests for WriterAgent."""

    def test_import(self):
        """Test writer agent can be imported."""
        from src.agents.writer import WriterAgent
        assert WriterAgent is not None


class TestReviewerAgent:
    """Tests for ReviewerAgent."""

    def test_import(self):
        """Test reviewer agent can be imported."""
        from src.agents.reviewer import ReviewerAgent
        assert ReviewerAgent is not None
