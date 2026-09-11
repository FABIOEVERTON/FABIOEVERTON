"""Analyst node - processes and analyzes research data."""

import json
from typing import Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.states import AgentState, Insight


def analyst_node(state: AgentState) -> dict:
    """Analyst node that processes research data and generates insights.

    Args:
        state: Current agent state.

    Returns:
        Updated state with analysis results.
    """
    settings = get_settings()
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_studio_api_key,
        temperature=0.4,
    )

    query = state.get("query", "")
    sources = state.get("sources", [])
    research_summary = state.get("research_summary", "")

    # Prepare sources for analysis
    sources_text = "\n\n".join(
        f"Source {i + 1}: {s.get('title', 'Unknown')}\n"
        f"URL: {s.get('url', '')}\n"
        f"{s.get('snippet', '')}"
        for i, s in enumerate(sources[:5])
    )

    # Generate analysis
    analysis_prompt = f"""Analyze the following research data and provide comprehensive insights.

Research Query: {query}

Sources:
{sources_text}

Research Summary:
{research_summary}

Please provide:
1. KEY INSIGHTS: 3-5 main findings with evidence and confidence levels (0-1)
2. COMPARISONS: If applicable, compare different options/approaches mentioned
3. TRENDS: Identify patterns or trends in the data
4. RECOMMENDATIONS: Actionable recommendations based on the analysis

Format your response as JSON:
{{
    "insights": [
        {{
            "topic": "topic name",
            "finding": "detailed finding",
            "evidence": ["evidence 1", "evidence 2"],
            "confidence": 0.85
        }}
    ],
    "comparisons": [
        {{
            "option_a": "name",
            "option_b": "name",
            "comparison": "detailed comparison",
            "winner": "recommended option"
        }}
    ],
    "trends": ["trend 1", "trend 2"],
    "recommendations": ["recommendation 1", "recommendation 2"]
}}"""

    messages = [
        SystemMessage(
            content="You are a data analyst. Analyze research data and provide structured insights in JSON format."
        ),
        HumanMessage(content=analysis_prompt),
    ]

    response = llm.invoke(messages)

    # Parse response
    try:
        json_start = response.content.find("{")
        json_end = response.content.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            data = json.loads(response.content[json_start:json_end])

            insights = [
                {
                    "topic": i.get("topic", "Unknown"),
                    "finding": i.get("finding", ""),
                    "evidence": i.get("evidence", []),
                    "confidence": i.get("confidence", 0.5),
                }
                for i in data.get("insights", [])
            ]

            return {
                "insights": insights,
                "comparisons": data.get("comparisons", []),
                "trends": data.get("trends", []),
                "recommendations": data.get("recommendations", []),
                "messages": [AIMessage(content=f"Analyst: Generated {len(insights)} insights")],
            }

    except (json.JSONDecodeError, KeyError):
        pass

    # Fallback
    return {
        "insights": [
            {
                "topic": "General Analysis",
                "finding": response.content[:500],
                "confidence": 0.6,
            }
        ],
        "trends": ["Analysis completed"],
        "recommendations": ["Review the full analysis for details"],
        "messages": [AIMessage(content="Analyst: Analysis completed (fallback)")],
    }


__all__ = ["analyst_node"]
