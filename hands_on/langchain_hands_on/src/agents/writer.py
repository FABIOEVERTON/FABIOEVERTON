"""Writer agent - generates research reports."""

from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.models import AnalysisResult, Report, ResearchResult


class WriterAgent:
    """Agent responsible for generating well-structured research reports."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model=self.settings.gemini_model,
            google_api_key=self.settings.google_studio_api_key,
            temperature=0.5,
        )

    async def write_report(
        self,
        research: ResearchResult,
        analysis: AnalysisResult,
    ) -> Report:
        """Generate a research report from analysis results.

        Args:
            research: Original research data.
            analysis: Analysis results.

        Returns:
            Complete Report object.
        """
        # Prepare context for report generation
        insights_text = "\n".join(
            f"- **{insight.topic}**: {insight.finding} (Confidence: {insight.confidence:.0%})"
            for insight in analysis.insights
        )

        trends_text = "\n".join(f"- {trend}" for trend in analysis.trends)
        recommendations_text = "\n".join(f"- {rec}" for rec in analysis.recommendations)

        sources_text = "\n".join(
            f"- [{source.title}]({source.url})" for source in research.sources
        )

        # Generate report sections
        report_prompt = f"""Generate a comprehensive research report based on the following data.

RESEARCH QUERY: {research.query}

RESEARCH SUMMARY:
{research.summary}

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

        response = await self.llm.ainvoke(messages)

        # Parse response into Report
        return self._parse_report_response(response.content, research, analysis)

    def _parse_report_response(
        self,
        response: str,
        research: ResearchResult,
        analysis: AnalysisResult,
    ) -> Report:
        """Parse LLM response into Report object.

        Args:
            response: LLM response string.
            research: Original research data.
            analysis: Analysis results.

        Returns:
            Parsed Report object.
        """
        import json

        try:
            # Try to extract JSON from response
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                report = Report(
                    title=data.get("title", "Research Report"),
                    query=research.query,
                    executive_summary=data.get("executive_summary", ""),
                    introduction=data.get("introduction", ""),
                    analysis=data.get("analysis", ""),
                    conclusions=data.get("conclusions", ""),
                    sources=research.sources,
                    confidence_score=sum(i.confidence for i in analysis.insights) / max(len(analysis.insights), 1),
                )
                report.calculate_word_count()
                return report

        except (json.JSONDecodeError, KeyError):
            pass

        # Fallback: create basic report
        report = Report(
            title="Research Report",
            query=research.query,
            executive_summary=response[:500],
            introduction=research.summary,
            analysis=str(analysis.insights),
            conclusions="See analysis for conclusions.",
            sources=research.sources,
            confidence_score=0.6,
        )
        report.calculate_word_count()
        return report

    def write_report_sync(
        self,
        research: ResearchResult,
        analysis: AnalysisResult,
    ) -> Report:
        """Synchronous version of write_report.

        Args:
            research: Original research data.
            analysis: Analysis results.

        Returns:
            Complete Report object.
        """
        import asyncio

        return asyncio.run(self.write_report(research, analysis))


__all__ = ["WriterAgent"]
