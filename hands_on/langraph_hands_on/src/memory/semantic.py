"""Semantic memory with langmem and embeddings."""

try:
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    from langgraph.store.memory import InMemoryStore
    from langmem import create_manage_memory_tool, create_search_memory_tool
    HAS_LANGMEM = True
except ImportError:
    HAS_LANGMEM = False

from src.config import get_settings


class SemanticMemory:
    """Semantic memory system using embeddings."""

    def __init__(self, thread_id: str = "default") -> None:
        self.settings = get_settings()
        self.thread_id = thread_id
        self.store = None
        self.manage_memory = None
        self.search_memory = None

        if HAS_LANGMEM:
            self._init_memory()

    def _init_memory(self) -> None:
        """Initialize memory store and tools."""
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=self.settings.google_studio_api_key,
        )

        self.store = InMemoryStore(
            index={
                "dims": 768,
                "embed": embeddings,
            }
        )

        namespace = ("memories", self.thread_id)
        self.manage_memory = create_manage_memory_tool(namespace=namespace)
        self.search_memory = create_search_memory_tool(namespace=namespace)

    def get_tools(self) -> list:
        """Get memory tools for agent.

        Returns:
            List of memory tools.
        """
        if self.manage_memory and self.search_memory:
            return [self.manage_memory, self.search_memory]
        return []

    def save(self, key: str, value: str) -> str:
        """Save a memory.

        Args:
            key: Memory key.
            value: Memory value.

        Returns:
            Status message.
        """
        if self.store:
            self.store.put(("memories", self.thread_id), key, {"value": value})
            return f"Saved: {key}"
        return "Memory store not initialized"

    def search(self, query: str, limit: int = 3) -> list:
        """Search memories.

        Args:
            query: Search query.
            limit: Maximum results.

        Returns:
            List of matching memories.
        """
        if self.store:
            results = self.store.search(
                ("memories", self.thread_id),
                query=query,
                limit=limit,
            )
            return [r.value.get("value", "") for r in results]
        return []


def get_memory_store(thread_id: str = "default") -> SemanticMemory:
    """Get or create memory store.

    Args:
        thread_id: Thread identifier.

    Returns:
        SemanticMemory instance.
    """
    return SemanticMemory(thread_id)
