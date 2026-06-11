import asyncio
from typing import Any

from tavily import TavilyClient

from app.core.config import get_settings


class TavilySearchService:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return bool(self.settings.tavily_api_key)

    async def search(self, query: str, max_results: int = 8) -> list[dict[str, Any]]:
        if not self.configured:
            return []
        client = TavilyClient(api_key=self.settings.tavily_api_key)
        response = await asyncio.to_thread(
            client.search,
            query,
            search_depth="advanced",
            max_results=max_results,
        )
        return response.get("results", [])


tavily_search_service = TavilySearchService()
