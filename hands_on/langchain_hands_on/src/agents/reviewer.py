"""Reviewer agent - validates report quality and accuracy."""

from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.models import Report, ResearchResult


class ReviewerAgent:
    """Agent responsible for reviewing and validating report quality."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model=self.settings.gemini_model,
            google_api_key=self.settings.google_studio_api_key,
            temperature=0.2,
        )

    async def review(self, report: Report, research: ResearchResult) -> Report:
        """Review and improve a research report.

        Args:
            report: Report to review.
            research: Original research data for validation.

        Returns:
            Improved Report object.
        """
        # Prepare review context
        sources_text = "\n".join(
            f"- [{s.title}]({s.url})" for s in research.sources
        )

        review_prompt = f"""Review the following research report for quality, accuracy, and completeness.

REPORT TITLE: {report.title}

EXECUTIVE SUMMARY:
{report.executive_summary}

INTRODUCTION:
{report.introduction}

ANALYSIS:
{report.analysis}

CONCLUSIONS:
{report.conclusions}

AVAILABLE SOURCES:
{sources_text}

Please review and provide:

1. QUALITY ASSESSMENT:
   - Structure and flow (1-10)
   - Evidence support (1-10)
   - Clarity and readability (1-10)
   - Overall confidence (0-1)

2. ISSUES FOUND:
   - Any factual inconsistencies
   - Missing information or gaps
   - Areas needing more detail
   - Citations that need verification

3. IMPROVEMENTS:
   - Suggested edits for clarity
   - Additional points to include
   - Better ways to present findings

4. VERDICT:
   - APPROVED: Report is ready
   - NEEDS REVISION: Requires changes (specify what)
   - REJECTED: Major issues (specify why)

Format your response as JSON:
{{
    "quality_assessment": {{
        "structure_score": 8,
        "evidence_score": 7,
        "clarity_score": 9,
        "overall_confidence": 0.85
    }},
    "issues_found": ["issue 1", "issue 2"],
    "improvements": ["improvement 1", "improvement 2"],
    "verdict": "APPROVED",
    "revised_executive_summary": "If changes needed, provide revised version",
    "revised_analysis": "If changes needed, provide revised version"
}}"""

        messages = [
            SystemMessage(
                content="You are a quality reviewer. Evaluate research reports for accuracy, completeness, and quality."
            ),
            HumanMessage(content=review_prompt),
        ]

        response = await self.llm.ainvoke(messages)

        # Parse and apply review
        return self._parse_review_response(response.content, report, research)

    def _parse_review_response(
        self,
        response: str,
        report: Report,
        research: ResearchResult,
    ) -> Report:
        """Parse review response and update report.

        Args:
            response: LLM review response.
            report: Original report.
            research: Research data.

        Returns:
            Updated Report object.
        """
        import json

        try:
            json_start = response.find("{")
            json_end = response.rfind("}") + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                # Update report with revisions if provided
                if data.get("revised_executive_summary"):
                    report.executive_summary = data["revised_executive_summary"]
                if data.get("revised_analysis"):
                    report.analysis = data["revised_analysis"]

                # Update confidence score
                quality = data.get("quality_assessment", {})
                if "overall_confidence" in quality:
                    report.confidence_score = quality["overall_confidence"]

                # Recalculate word count
                report.calculate_word_count()

                return report

        except (json.JSONDecodeError, KeyError):
            pass

        # If parsing fails, return original report
        return report

    def review_sync(self, report: Report, research: ResearchResult) -> Report:
        """Synchronous version of review.

        Args:
            report: Report to review.
            research: Research data.

        Returns:
            Updated Report object.
        """
        import asyncio

        return asyncio.run(self.review(report, research))


__all__ = ["ReviewerAgent"]
