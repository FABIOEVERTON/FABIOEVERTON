"""Structured output schemas using Pydantic."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class InsightSeverity(str, Enum):
    """Severity level for insights."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class StructuredInsight(BaseModel):
    """Structured insight output."""
    topic: str = Field(description="Tópico do insight")
    finding: str = Field(description="Descoberta principal")
    evidence: list[str] = Field(default_factory=list, description="Evidências")
    confidence: float = Field(ge=0, le=1, description="Nível de confiança")
    severity: InsightSeverity = Field(description="Severidade do insight")


class AnalysisOutput(BaseModel):
    """Structured analysis output."""
    insights: list[StructuredInsight] = Field(description="Lista de insights")
    trends: list[str] = Field(default_factory=list, description="Tendências")
    recommendations: list[str] = Field(default_factory=list, description="Recomendações")
    overall_confidence: float = Field(ge=0, le=1, description="Confiança geral")


class EmailDecision(BaseModel):
    """Structured email routing decision."""
    action: str = Field(description="Ação: ignorar, notificar, ou responder")
    reasoning: str = Field(description="Justificativa da decisão")
    priority: int = Field(ge=1, le=5, description="Prioridade 1-5")
    response_suggestion: Optional[str] = Field(None, description="Sugestão de resposta")


class ReportStructure(BaseModel):
    """Structured report output."""
    title: str = Field(description="Título do relatório")
    executive_summary: str = Field(description="Resumo executivo")
    key_findings: list[str] = Field(description="Principais descobertas")
    conclusions: list[str] = Field(description="Conclusões")
    word_count: int = Field(description="Contagem de palavras")
