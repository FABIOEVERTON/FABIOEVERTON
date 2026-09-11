"""Reviewer node - validates report quality and accuracy."""

import json
from typing import Optional

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings
from src.states import AgentState


def reviewer_node(state: AgentState) -> dict:
    """Reviewer node that validates and improves report quality.

    Args:
        state: Current agent state.

    Returns:
        Updated state with review results.
    """
    settings = get_settings()
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model,
        google_api_key=settings.google_studio_api_key,
        temperature=0.2,
    )

    query = state.get("query", "")
    report_title = state.get("report_title", "")
    executive_summary = state.get("executive_summary", "")
    introduction = state.get("introduction", "")
    analysis = state.get("analysis", "")
    conclusions = state.get("conclusions", "")
    sources = state.get("sources", [])
    confidence_score = state.get("confidence_score", 0.6)

    # Prepare sources for review
    sources_text = "\n".join(
        f"- [{s.get('title', 'Unknown')}]({s.get('url', '')})" for s in sources
    )

    # Generate review
    review_prompt = f"""Review the following research report for quality, accuracy, and completeness.

REPORT TITLE: {report_title}

EXECUTIVE SUMMARY:
{executive_summary}

INTRODUCTION:
{introduction}

ANALYSIS:
{analysis}

CONCLUSIONS:
{conclusions}

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

3. IMPROVEMENTS:
   - Suggested edits for clarity
   - Additional points to include

4. VERDICT:
   - APPROVED: Report is ready
   - NEEDS REVISION: Requires changes

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

    response = llm.invoke(messages)

    # Parse response
    try:
        json_start = response.content.find("{")
        json_end = response.content.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            data = json.loads(response.content[json_start:json_end])

            updates = {}

            # Apply revisions if provided
            if data.get("revised_executive_summary"):
                updates["executive_summary"] = data["revised_executive_summary"]
            if data.get("revised_analysis"):
                updates["analysis"] = data["revised_analysis"]

            # Update confidence score
            quality = data.get("quality_assessment", {})
            if "overall_confidence" in quality:
                updates["confidence_score"] = quality["overall_confidence"]

            # Add review message
            verdict = data.get("verdict", "UNKNOWN")
            updates["messages"] = [
                AIMessage(content=f"Reviewer: {verdict} (Confidence: {updates.get('confidence_score', confidence_score):.0%})")
            ]

            return updates

    except (json.JSONDecodeError, KeyError):
        pass

    # If parsing fails, keep current state
    return {
        "messages": [AIMessage(content="Reviewer: Review completed (no changes)")],
    }


__all__ = ["reviewer_node"]
