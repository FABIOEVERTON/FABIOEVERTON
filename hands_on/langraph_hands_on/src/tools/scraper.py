"""Web scraper using Playwright and BeautifulSoup."""

import asyncio
from typing import Optional
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.async_api import async_playwright

from src.config import get_settings
from src.states import ResearchSource


class WebScraper:
    """Web scraper using Playwright and BeautifulSoup."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def scrape_url_async(self, url: str) -> Optional[ResearchSource]:
        """Scrape content from a URL asynchronously.

        Args:
            url: The URL to scrape.

        Returns:
            ResearchSource object with scraped content or None if failed.
        """
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.settings.scraper_headless)
                page = await browser.new_page()

                # Navigate to URL
                await page.goto(url, wait_until="domcontentloaded", timeout=self.settings.source_timeout * 1000)

                # Wait for content to load
                await page.wait_for_timeout(int(self.settings.scraper_delay * 1000))

                # Get page content
                html_content = await page.content()
                await browser.close()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract title
            title = soup.title.string if soup.title else urlparse(url).path

            # Extract main content (remove scripts, styles, nav, footer)
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()

            # Get text content
            text_content = soup.get_text(separator="\n", strip=True)

            # Convert to markdown for better readability
            markdown_content = md(text_content)

            # Clean up excessive whitespace
            lines = markdown_content.split("\n")
            cleaned_lines = [line.strip() for line in lines if line.strip()]
            markdown_content = "\n".join(cleaned_lines)

            return ResearchSource(
                url=url,
                title=title,
                snippet=markdown_content[:500] + "..." if len(markdown_content) > 500 else markdown_content,
                content=markdown_content,
            )

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None

    def scrape_url(self, url: str) -> Optional[ResearchSource]:
        """Scrape content from a URL (sync wrapper).

        Args:
            url: The URL to scrape.

        Returns:
            ResearchSource object with scraped content or None if failed.
        """
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    return pool.submit(asyncio.run, self.scrape_url_async(url)).result()
            else:
                return loop.run_until_complete(self.scrape_url_async(url))
        except RuntimeError:
            return asyncio.run(self.scrape_url_async(url))


__all__ = ["WebScraper"]
