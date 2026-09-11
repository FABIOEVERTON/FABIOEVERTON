"""Cache system for LLM responses."""

from langchain_core.globals import set_llm_cache
from langchain_community.caches import SQLiteCache

_cache_initialized = False


def init_cache(db_path: str = ".langchain_cache.db") -> None:
    """Initialize SQLite cache for LLM responses.

    Args:
        db_path: Path to SQLite database.
    """
    global _cache_initialized
    if not _cache_initialized:
        set_llm_cache(SQLiteCache(database_path=db_path))
        _cache_initialized = True


def get_cache_status() -> str:
    """Get cache initialization status."""
    return "initialized" if _cache_initialized else "not initialized"
