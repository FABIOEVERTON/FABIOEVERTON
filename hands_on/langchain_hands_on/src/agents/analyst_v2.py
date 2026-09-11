"""Analyst agent with structured output."""

import json

from langchain_core.messages import AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.config import get_settings
from src.models.structured import AnalysisOutput
from src.utils.router import router


class AnalystAgent:
    """Agent with structured output using Pydantic."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.parser = JsonOutputParser()

        # Prompt Template com instruções de formato
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Você é um analista de dados. {format_instructions}"),
            ("human", "Analise os dados da pesquisa:\n\n"
             "Query: {query}\n"
             "Resumo: {summary}\n\n"
             "Forneça insights estruturados."),
        ])

    def analyze(self, query: str, summary: str, sources: list) -> dict:
        """Analyze research data with structured output.

        Args:
            query: Research query.
            summary: Research summary.
            sources: List of sources.

        Returns:
            Structured analysis dictionary.
        """
        llm = router.route(query, task_type="analyze")

        # Create chain
        chain = self.prompt | llm | self.parser

        try:
            result = chain.invoke({
                "format_instructions": "Retorne um JSON com: insights (lista), trends (lista), recommendations (lista), overall_confidence (float 0-1)",
                "query": query,
                "summary": summary,
            })
            return result
        except Exception:
            return {
                "insights": [{"topic": "General", "finding": summary[:200], "confidence": 0.6}],
                "trends": [],
                "recommendations": [],
                "overall_confidence": 0.6,
            }


__all__ = ["AnalystAgent"]
