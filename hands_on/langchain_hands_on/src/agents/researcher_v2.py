"""Researcher agent with templates and parsers."""

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.config import get_settings
from src.models import ResearchResult, Source
from src.tools.scraper import WebScraper
from src.tools.web_search import WebSearchTool
from src.utils.router import router


class ResearcherAgent:
    """Agent with prompt templates and output parsers."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.search_tool = WebSearchTool()
        self.scraper = WebScraper()
        self.parser = StrOutputParser()

        # Prompt Template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um pesquisador especializado em {domain}. "
             "Forneça resumos concisos e objetivos."),
            ("human", "Pesquise sobre: {query}\n\n"
             "Fontes encontradas:\n{sources}\n\n"
             "Gere um resumo das principais descobertas."),
        ])

    async def research(self, query: str, max_sources: int = 5) -> ResearchResult:
        """Conduct research with template-based prompts.

        Args:
            query: Research query.
            max_sources: Maximum sources to collect.

        Returns:
            ResearchResult with findings.
        """
        import asyncio

        search_results = await self.search_tool.search(query, num_results=max_sources)

        sources = []
        for result in search_results:
            url = result.get("link", "")
            if url:
                source = self.scraper.scrape_url(url)
                if source:
                    sources.append(Source(
                        url=url,
                        title=source.title,
                        snippet=source.snippet,
                    ))
                else:
                    sources.append(Source(
                        url=url,
                        title=result.get("title", "Unknown"),
                        snippet=result.get("snippet", ""),
                    ))

        sources_text = "\n".join(
            f"- {s.title}: {s.snippet}" for s in sources[:5]
        )

        # Use router to select model
        llm = router.route(query, task_type="research")

        # Create chain with template + parser
        chain = self.prompt | llm | self.parser

        summary = await chain.ainvoke({
            "domain": "tecnologia e IA",
            "query": query,
            "sources": sources_text,
        })

        return ResearchResult(
            query=query,
            sources=sources,
            summary=summary,
        )

    def research_sync(self, query: str) -> ResearchResult:
        """Synchronous research wrapper."""
        import asyncio
        return asyncio.run(self.research(query))


__all__ = ["ResearcherAgent"]
