"""Pydantic-based routers for structured decisions."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EmailAction(str, Enum):
    """Email action types."""
    IGNORE = "ignorar"
    NOTIFY = "notificar"
    RESPONDER = "responder"
    ENCAMINHAR = "encaminhar"


class EmailDecision(BaseModel):
    """Structured email routing decision."""
    action: EmailAction = Field(description="Ação a tomar no email")
    reasoning: str = Field(description="Justificativa da decisão")
    priority: int = Field(ge=1, le=5, description="Prioridade 1-5")
    response_suggestion: Optional[str] = Field(None, description="Sugestão de resposta")
    category: str = Field(description="Categoria: trabalho, pessoal, spam, newsletter")


class TaskDecision(BaseModel):
    """Structured task routing decision."""
    task_type: str = Field(description="Tipo: pesquisa, análise, escrita, revisão")
    complexity: str = Field(description="Complexidade: simples, média, complexa")
    estimated_time: str = Field(description="Tempo estimado")
    requires_human: bool = Field(description="Precisa de intervenção humana")


class ReportDecision(BaseModel):
    """Structured report quality decision."""
    quality_score: int = Field(ge=1, le=10, description="Score de qualidade 1-10")
    needs_revision: bool = Field(description="Precisa de revisão")
    missing_elements: list[str] = Field(default_factory=list, description="Elementos faltantes")
    suggested_improvements: list[str] = Field(default_factory=list, description="Melhorias sugeridas")


def create_router(llm, schema):
    """Create a structured router from LLM and Pydantic schema.

    Args:
        llm: Language model.
        schema: Pydantic model for output.

    Returns:
        Router that outputs structured decisions.
    """
    return llm.with_structured_output(schema)
