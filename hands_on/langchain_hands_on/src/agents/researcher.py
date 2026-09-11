"""Researcher agent - collects information from web sources."""

from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.models import ResearchResult, Source
from src.tools.scraper import WebScraper
from src.tools.web_search import WebSearchTool


class ResearcherAgent:
    """Agent responsible for collecting research data from web sources."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model=self.settings.gemini_model,
            google_api_key=self.settings.google_studio_api_key,
            temperature=0.3,
        )
        self.search_tool = WebSearchTool()
        self.scraper = WebScraper()

    async def research(self, query: str, max_sources: Optional[int] = None) -> ResearchResult:
        """Conduct research on a topic.

        Args:
            query: Research query.
            max_sources: Maximum number of sources to collect.

        Returns:
            ResearchResult with collected sources and summary.
        """
        max_sources = max_sources or self.settings.max_sources

        # Step 1: Search for relevant sources
        search_results = await self.search_tool.search(query, num_results=max_sources)

        sources = []
        for result in search_results:
            url = result.get("link", "")
            if url:
                # Step 2: Scrape each source for detailed content
                source = self.scraper.scrape_url(url)
                if source:
                    sources.append(source)
                else:
                    # Fallback to search snippet
                    sources.append(
                        Source(
                            url=url,
                            title=result.get("title", "Unknown"),
                            snippet=result.get("snippet", ""),
                        )
                    )

        # Step 3: Generate summary using LLM
        summary = await self._generate_summary(query, sources)

        return ResearchResult(
            query=query,
            sources=sources,
            summary=summary,
        )

    async def _generate_summary(self, query: str, sources: list[Source]) -> str:
        """Generate a summary of research findings.

        Args:
            query: Original research query.
            sources: List of collected sources.

        Returns:
            Summary string.
        """
        sources_text = "\n\n".join(
            f"Source {i + 1}: {s.title}\n{s.snippet}"
            for i, s in enumerate(sources[:5])
        )

        messages = [
            SystemMessage(
                content="You are a research assistant. Summarize the key findings from the provided sources."
            ),
            HumanMessage(
                content=f"""Research Query: {query}

Sources:
{sources_text}

Provide a concise summary of the key findings, highlighting main points, trends, and important data points.
Focus on factual information and cite sources where possible."""
            ),
        ]

        response = await self.llm.ainvoke(messages)
        return response.content

    def research_sync(self, query: str, max_sources: Optional[int] = None) -> ResearchResult:
        """Synchronous version of research for simpler usage.

        Args:
            query: Research query.
            max_sources: Maximum number of sources to collect.

        Returns:
            ResearchResult with collected sources and summary.
        """
        import asyncio

        return asyncio.run(self.research(query, max_sources))


__all__ = ["ResearcherAgent"]
