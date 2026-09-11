"""Tests for tool modules."""

import pytest


class TestWebSearchTool:
    """Tests for WebSearchTool."""

    def test_import(self):
        """Test web search tool can be imported."""
        from src.tools.web_search import WebSearchTool
        assert WebSearchTool is not None


class TestWebScraper:
    """Tests for WebScraper."""

    def test_import(self):
        """Test web scraper can be imported."""
        from src.tools.scraper import WebScraper
        assert WebScraper is not None


class TestPDFExporter:
    """Tests for PDFExporter."""

    def test_import(self):
        """Test PDF exporter can be imported."""
        from src.tools.pdf_export import PDFExporter
        assert PDFExporter is not None
