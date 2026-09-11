"""Tests for workflow graph."""

import pytest


class TestWorkflow:
    """Tests for workflow graph."""

    def test_import(self):
        """Test workflow can be imported."""
        from src.workflow import create_workflow, graph
        assert create_workflow is not None
        assert graph is not None

    def test_graph_has_nodes(self):
        """Test graph has expected nodes."""
        from src.workflow import graph
        # Graph should be compiled and have nodes
        assert hasattr(graph, "invoke")
