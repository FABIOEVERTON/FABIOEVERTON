"""Web search tool using Google Custom Search API."""

from typing import Optional

import httpx
from langchain_core.tools import tool

from src.config import get_settings


class WebSearchTool:
    """Web search tool using Google Custom Search API."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    async def search(self, query: str, num_results: int = 5) -> list[dict]:
        """Search the web using Google Custom Search API.

        Args:
            query: Search query string.
            num_results: Number of results to return (max 10).

        Returns:
            List of search results with title, link, and snippet.
        """
        # For demo purposes, we'll use a simulated search
        # In production, you'd use the actual Google API
        results = []
        async with httpx.AsyncClient(timeout=self.settings.source_timeout) as client:
            # Simulated search results for demo
            # Replace with actual Google Custom Search API call
            simulated_results = [
                {
                    "title": f"Result for: {query} - Part 1",
                    "link": "https://example.com/result1",
                    "snippet": f"This is a comprehensive analysis of {query} covering key aspects and findings.",
                },
                {
                    "title": f"Result for: {query} - Part 2",
                    "link": "https://example.com/result2",
                    "snippet": f"Detailed comparison and review of {query} with expert opinions.",
                },
                {
                    "title": f"Result for: {query} - Part 3",
                    "link": "https://example.com/result3",
                    "snippet": f"Latest trends and developments in {query} for 2024.",
                },
            ]
            results = simulated_results[:num_results]

        return results


@tool
def web_search(query: str, num_results: int = 5) -> str:
    """Search the web for information on a topic.

    Args:
        query: The search query.
        num_results: Number of results to return.

    Returns:
        Formatted search results.
    """
    import asyncio

    search_tool = WebSearchTool()
    results = asyncio.run(search_tool.search(query, num_results))

    formatted = []
    for i, result in enumerate(results, 1):
        formatted.append(
            f"{i}. **{result['title']}**\n"
            f"   URL: {result['link']}\n"
            f"   {result['snippet']}\n"
        )

    return "\n".join(formatted)
