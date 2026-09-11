"""Configuration management for the LangGraph system."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration
    google_studio_api_key: str = Field(..., env="GOOGLE_STUDIO_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash", env="GEMINI_MODEL")

    # Research Configuration
    max_sources: int = Field(default=10, env="MAX_SOURCES")
    source_timeout: int = Field(default=30, env="SOURCE_TIMEOUT")
    max_tokens_per_query: int = Field(default=8000, env="MAX_TOKENS_PER_QUERY")

    # Output Configuration
    output_dir: Path = Field(default=Path("output"), env="OUTPUT_DIR")

    # Scraper Configuration
    scraper_headless: bool = Field(default=True, env="SCRAPER_HEADLESS")
    scraper_delay: float = Field(default=1.0, env="SCRAPER_DELAY")

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()
