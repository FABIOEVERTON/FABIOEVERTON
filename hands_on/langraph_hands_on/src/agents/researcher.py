"""Researcher node - collects information from web sources."""

import asyncio
from typing import Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.states import AgentState
from src.tools.scraper import WebScraper
from src.tools.web_search import WebSearchTool


def researcher_node(state: AgentState) -> dict:
    """Researcher node that collects information from web sources.

    Args:
        state: Current agent state.

    Returns:
        Updated state with research data.
    """
    settings = get_settings()
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_studio_api_key,
        temperature=0.3,
    )

    query = state.get("query", "")
    existing_sources = state.get("sources", [])

    # Initialize tools
    search_tool = WebSearchTool()
    scraper = WebScraper()

    # Search for sources
    try:
        search_results = asyncio.run(search_tool.search(query, num_results=5))
    except Exception:
        search_results = []

    # Process sources
    sources = list(existing_sources)
    for result in search_results:
        url = result.get("link", "")
        if url and not any(s.get("url") == url for s in sources):
            # Try to scrape the source
            source_data = scraper.scrape_url(url)
            if source_data:
                sources.append({
                    "url": url,
                    "title": source_data.title,
                    "snippet": source_data.snippet,
                    "content": source_data.content[:2000] if source_data.content else "",
                    "credibility_score": 0.6,
                })
            else:
                # Fallback to search snippet
                sources.append({
                    "url": url,
                    "title": result.get("title", "Unknown"),
                    "snippet": result.get("snippet", ""),
                    "content": "",
                    "credibility_score": 0.5,
                })

    # Generate summary using LLM
    sources_text = "\n\n".join(
        f"Source {i + 1}: {s.get('title', 'Unknown')}\n{s.get('snippet', '')}"
        for i, s in enumerate(sources[:5])
    )

    messages = [
        SystemMessage(
            content="You are a research assistant. Summarize the key findings from the provided sources."
        ),
        HumanMessage(
            content=f"Research Query: {query}\n\nSources:\n{sources_text}\n\n"
            "Provide a concise summary of the key findings."
        ),
    ]

    response = llm.invoke(messages)

    return {
        "sources": sources,
        "research_summary": response.content,
        "messages": [AIMessage(content=f"Researcher: Found {len(sources)} sources")],
    }


__all__ = ["researcher_node"]
