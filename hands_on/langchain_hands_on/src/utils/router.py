"""Intelligent router for model selection."""

from langchain_google_genai import ChatGoogleGenerativeAI

from src.config import get_settings


class IntelligentRouter:
    """Routes queries to optimal model based on complexity."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.models = {
            "flash": ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=self.settings.google_studio_api_key,
                temperature=0.3,
            ),
            "flash_lite": ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-lite",
                google_api_key=self.settings.google_studio_api_key,
                temperature=0.3,
            ),
            "pro": ChatGoogleGenerativeAI(
                model="gemini-2.5-pro-preview",
                google_api_key=self.settings.google_studio_api_key,
                temperature=0.3,
            ),
        }

    def route(self, query: str, task_type: str = "general") -> ChatGoogleGenerativeAI:
        """Route to optimal model based on query complexity.

        Args:
            query: Input query.
            task_type: Type of task (simple, general, complex).

        Returns:
            Selected LLM model.
        """
        complexity = self._assess_complexity(query, task_type)

        if complexity == "simple":
            return self.models["flash_lite"]
        elif complexity == "complex":
            return self.models["pro"]
        return self.models["flash"]

    def _assess_complexity(self, query: str, task_type: str) -> str:
        """Assess query complexity."""
        if task_type in ("math", "translate", "summarize") or len(query) < 100:
            return "simple"
        elif task_type in ("analyze", "research", "compare") or len(query) > 500:
            return "complex"
        return "medium"


router = IntelligentRouter()
