"""Tests for agent nodes."""

import pytest


class TestOrchestratorNode:
    """Tests for orchestrator_node."""

    def test_import(self):
        """Test orchestrator node can be imported."""
        from src.agents.orchestrator import orchestrator_node
        assert orchestrator_node is not None


class TestResearcherNode:
    """Tests for researcher_node."""

    def test_import(self):
        """Test researcher node can be imported."""
        from src.agents.researcher import researcher_node
        assert researcher_node is not None


class TestAnalystNode:
    """Tests for analyst_node."""

    def test_import(self):
        """Test analyst node can be imported."""
        from src.agents.analyst import analyst_node
        assert analyst_node is not None


class TestWriterNode:
    """Tests for writer_node."""

    def test_import(self):
        """Test writer node can be imported."""
        from src.agents.writer import writer_node
        assert writer_node is not None


class TestReviewerNode:
    """Tests for reviewer_node."""

    def test_import(self):
        """Test reviewer node can be imported."""
        from src.agents.reviewer import reviewer_node
        assert reviewer_node is not None
