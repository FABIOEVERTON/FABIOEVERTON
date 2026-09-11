"""Real web search tools."""

import asyncio
from typing import Optional

from langchain_core.tools import tool

try:
    from langchain_community.tools import DuckDuckGoSearchRun
    from langchain_community.tools.tavily_search import TavilySearchResults
    HAS_SEARCH_TOOLS = True
except ImportError:
    HAS_SEARCH_TOOLS = False


class RealWebSearch:
    """Real web search using DuckDuckGo."""

    def __init__(self) -> None:
        if HAS_SEARCH_TOOLS:
            self.ddg = DuckDuckGoSearchRun()
        else:
            self.ddg = None

    def search(self, query: str, max_results: int = 5) -> str:
        """Search using DuckDuckGo.

        Args:
            query: Search query.
            max_results: Maximum results.

        Returns:
            Search results as string.
        """
        if self.ddg:
            return self.ddg.invoke(query)
        return f"Search results for: {query} (DuckDuckGo not installed)"


@tool
def duckduckgo_search(query: str) -> str:
    """Busca informações na web usando DuckDuckGo.

    Args:
        query: Termo de busca.

    Returns:
        Resultados da busca.
    """
    searcher = RealWebSearch()
    return searcher.search(query)


@tool
def tavily_search(query: str) -> str:
    """Busca inteligente usando Tavily com consciência de contexto.

    Args:
        query: Termo de busca.

    Returns:
        Resultados enriquecidos da busca.
    """
    if HAS_SEARCH_TOOLS:
        try:
            search = TavilySearchResults(max_results=5)
            results = search.invoke({"query": query, "search_depth": "advanced"})
            return str(results)
        except Exception as e:
            return f"Tavily error: {e}"
    return "Tavily not installed. Install with: pip install langchain-community tavily-python"


@tool
def scrape_url(url: str) -> str:
    """Faz scraping de uma URL usando Playwright.

    Args:
        url: URL para fazer scraping.

    Returns:
        Conteúdo extraído da página.
    """
    from src.tools.scraper import WebScraper
    scraper = WebScraper()
    source = scraper.scrape_url(url)
    if source:
        return f"Title: {source.title}\n\nContent:\n{source.content[:2000]}"
    return f"Failed to scrape: {url}"


ALL_SEARCH_TOOLS = [duckduckgo_search, tavily_search, scrape_url]
