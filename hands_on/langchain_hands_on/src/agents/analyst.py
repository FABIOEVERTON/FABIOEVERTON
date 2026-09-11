"""Analyst agent - processes and analyzes research data."""

from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.models import AnalysisResult, Insight, ResearchResult


class AnalystAgent:
    """Agent responsible for analyzing research data and generating insights."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model=self.settings.gemini_model,
            google_api_key=self.settings.google_studio_api_key,
            temperature=0.4,
        )

    async def analyze(self, research: ResearchResult) -> AnalysisResult:
        """Analyze research results and generate insights.

        Args:
            research: ResearchResult from the researcher agent.

        Returns:
            AnalysisResult with insights, comparisons, and recommendations.
        """
        # Prepare research data for analysis
        sources_text = "\n\n".join(
            f"Source {i + 1}: {s.title}\nURL: {s.url}\n{s.snippet}"
            for i, s in enumerate(research.sources)
        )

        # Generate analysis using LLM
        analysis_prompt = f"""Analyze the following research data and provide comprehensive insights.

Research Query: {research.query}

Sources:
{sources_text}

Research Summary:
{research.summary}

Please provide:
1. KEY INSIGHTS: 3-5 main findings with evidence and confidence levels (0-1)
2. COMPARISONS: If applicable, compare different options/approaches mentioned
3. TRENDS: Identify patterns or trends in the data
4. RECOMMENDATIONS: Actionable recommendations based on the analysis

Format your response as JSON with the following structure:
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

        response = await self.llm.ainvoke(messages)

        # Parse response into AnalysisResult
        return self._parse_analysis_response(response.content, research)

    def _parse_analysis_response(self, response: str, research: ResearchResult) -> AnalysisResult:
        """Parse LLM response into AnalysisResult.

        Args:
            response: LLM response string.
            research: Original research data.

        Returns:
            Parsed AnalysisResult.
        """
        import json

        try:
            # Try to extract JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                insights = [
                    Insight(
                        topic=insight.get("topic", "Unknown"),
                        finding=insight.get("finding", ""),
                        evidence=insight.get("evidence", []),
                        confidence=insight.get("confidence", 0.5),
                    )
                    for insight in data.get("insights", [])
                ]

                return AnalysisResult(
                    insights=insights,
                    comparisons=data.get("comparisons", []),
                    trends=data.get("trends", []),
                    recommendations=data.get("recommendations", []),
                )

        except (json.JSONDecodeError, KeyError):
            pass

        # Fallback: create basic analysis from response
        return AnalysisResult(
            insights=[
                Insight(
                    topic="General Analysis",
                    finding=response[:500],
                    confidence=0.6,
                )
            ],
            trends=["Analysis completed"],
            recommendations=["Review the full analysis for details"],
        )

    def analyze_sync(self, research: ResearchResult) -> AnalysisResult:
        """Synchronous version of analyze.

        Args:
            research: ResearchResult from the researcher agent.

        Returns:
            AnalysisResult with insights.
        """
        import asyncio

        return asyncio.run(self.analyze(research))


__all__ = ["AnalystAgent"]
