"""Pydantic models for data schemas."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class AgentRole(str, Enum):
    """Agent roles in the system."""

    ORCHESTRATOR = "orchestrator"
    RESEARCHER = "researcher"
    ANALYST = "analyst"
    WRITER = "writer"
    REVIEWER = "reviewer"


class Source(BaseModel):
    """A research source."""

    url: HttpUrl
    title: str
    snippet: str
    content: Optional[str] = None
    credibility_score: float = Field(ge=0, le=1, default=0.5)
    scraped_at: datetime = Field(default_factory=datetime.now)


class Insight(BaseModel):
    """An analysis insight."""

    topic: str
    finding: str
    evidence: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    sources: list[HttpUrl] = Field(default_factory=list)


class ResearchResult(BaseModel):
    """Result from the researcher agent."""

    query: str
    sources: list[Source] = Field(default_factory=list)
    summary: str = ""
    collected_at: datetime = Field(default_factory=datetime.now)


class AnalysisResult(BaseModel):
    """Result from the analyst agent."""

    insights: list[Insight] = Field(default_factory=list)
    comparisons: list[dict] = Field(default_factory=list)
    trends: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class Report(BaseModel):
    """Final research report."""

    title: str
    query: str
    executive_summary: str
    introduction: str
    analysis: str
    conclusions: str
    sources: list[Source] = Field(default_factory=list)
    confidence_score: float = Field(ge=0, le=1)
    generated_at: datetime = Field(default_factory=datetime.now)
    word_count: int = 0

    def calculate_word_count(self) -> None:
        """Calculate total word count."""
        text = f"{self.executive_summary} {self.introduction} {self.analysis} {self.conclusions}"
        self.word_count = len(text.split())


class AgentMessage(BaseModel):
    """Message passed between agents."""

    sender: AgentRole
    receiver: AgentRole
    content: str
    metadata: dict = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)
