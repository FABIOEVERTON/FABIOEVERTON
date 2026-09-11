"""Writer node - generates research reports."""

import json
from typing import Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.states import AgentState


def writer_node(state: AgentState) -> dict:
    """Writer node that generates research reports.

    Args:
        state: Current agent state.

    Returns:
        Updated state with generated report.
    """
    settings = get_settings()
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_studio_api_key,
        temperature=0.5,
    )

    query = state.get("query", "")
    sources = state.get("sources", [])
    research_summary = state.get("research_summary", "")
    insights = state.get("insights", [])
    comparisons = state.get("comparisons", [])
    trends = state.get("trends", [])
    recommendations = state.get("recommendations", [])

    # Prepare data for report generation
    insights_text = "\n".join(
        f"- **{i.get('topic', 'Unknown')}**: {i.get('finding', '')} "
        f"(Confidence: {i.get('confidence', 0.5):.0%})"
        for i in insights
    )

    trends_text = "\n".join(f"- {t}" for t in trends)
    recommendations_text = "\n".join(f"- {r}" for r in recommendations)
    sources_text = "\n".join(
        f"- [{s.get('title', 'Unknown')}]({s.get('url', '')})" for s in sources
    )

    # Generate report
    report_prompt = f"""Generate a comprehensive research report based on the following data.

RESEARCH QUERY: {query}

RESEARCH SUMMARY:
{research_summary}

KEY INSIGHTS:
{insights_text}

TRENDS:
{trends_text}

RECOMMENDATIONS:
{recommendations_text}

SOURCES:
{sources_text}

Please generate a professional research report with the following sections:

1. TITLE: A clear, descriptive title for the report
2. EXECUTIVE SUMMARY: A 2-3 paragraph overview of key findings (max 300 words)
3. INTRODUCTION: Context and background for the research (1-2 paragraphs)
4. ANALYSIS: Detailed analysis with insights, comparisons, and evidence (3-5 paragraphs)
5. CONCLUSIONS: Key takeaways and final thoughts (1-2 paragraphs)

Make the report:
- Professional and well-structured
- Evidence-based with citations to sources
- Clear and concise
- Actionable where possible

Format your response as JSON:
{{
    "title": "Report Title",
    "executive_summary": "Executive summary text...",
    "introduction": "Introduction text...",
    "analysis": "Analysis text...",
    "conclusions": "Conclusions text..."
}}"""

    messages = [
        SystemMessage(
            content="You are a professional report writer. Generate well-structured, evidence-based research reports."
        ),
        HumanMessage(content=report_prompt),
    ]

    response = llm.invoke(messages)

    # Parse response
    try:
        json_start = response.content.find("{")
        json_end = response.content.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            data = json.loads(response.content[json_start:json_end])

            # Calculate confidence score
            avg_confidence = 0.6
            if insights:
                avg_confidence = sum(i.get("confidence", 0.5) for i in insights) / len(insights)

            # Calculate word count
            text = f"{data.get('executive_summary', '')} {data.get('introduction', '')} "
            text += f"{data.get('analysis', '')} {data.get('conclusions', '')}"
            word_count = len(text.split())

            return {
                "report_title": data.get("title", "Research Report"),
                "executive_summary": data.get("executive_summary", ""),
                "introduction": data.get("introduction", ""),
                "analysis": data.get("analysis", ""),
                "conclusions": data.get("conclusions", ""),
                "confidence_score": avg_confidence,
                "messages": [AIMessage(content=f"Writer: Generated report ({word_count} words)")],
            }

    except (json.JSONDecodeError, KeyError):
        pass

    # Fallback
    return {
        "report_title": "Research Report",
        "executive_summary": response.content[:500],
        "introduction": research_summary,
        "analysis": str(insights),
        "conclusions": "See analysis for conclusions.",
        "confidence_score": 0.6,
        "messages": [AIMessage(content="Writer: Report generated (fallback)")],
    }


__all__ = ["writer_node"]
