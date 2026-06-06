import asyncio
from typing import Any
from uuid import uuid4

import httpx

from app.core.config import get_settings


class AgentGatewayService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def call(
        self,
        agent: str,
        payload: dict[str, Any],
        fallback_data: dict[str, Any],
    ) -> dict[str, Any]:
        if not self.settings.agent_gateway_token:
            return self._fallback(agent, fallback_data, "gateway token is not configured")

        try:
            async with httpx.AsyncClient(timeout=self.settings.agent_timeout_seconds) as client:
                response = await client.post(
                    f"{self.settings.agent_gateway_url}/agents/{agent}/invoke",
                    headers={"Authorization": f"Bearer {self.settings.agent_gateway_token}"},
                    json=payload,
                )
                response.raise_for_status()
                return {"fallback": False, "agent": agent, "result": response.json()}
        except (httpx.HTTPError, asyncio.TimeoutError) as exc:
            if not self.settings.enable_mock_fallback:
                raise
            return self._fallback(agent, fallback_data, str(exc))

    @staticmethod
    def _fallback(agent: str, data: dict[str, Any], reason: str) -> dict[str, Any]:
        return {
            "fallback": True,
            "agent": agent,
            "taskId": str(uuid4()),
            "reason": reason,
            "data": data,
        }


gateway_service = AgentGatewayService()
