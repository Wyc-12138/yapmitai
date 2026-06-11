import json
import logging
import re
from typing import Any

import anthropic
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.core.exceptions import AgentUnavailableError

logger = logging.getLogger(__name__)


class GrowthLLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def openai_api_key(self) -> str:
        return self.settings.openai_api_key or self.settings.external_ai_api_key

    @property
    def openai_base_url(self) -> str:
        return self.settings.external_ai_base_url.rstrip("/")

    @property
    def configured(self) -> bool:
        return bool(self.openai_api_key or self.settings.anthropic_api_key)

    async def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        if not self.configured:
            raise AgentUnavailableError(
                "Growth Team LLM is not configured. Set EXTERNAL_AI_API_KEY, "
                "OPENAI_API_KEY, or ANTHROPIC_API_KEY."
            )

        if self.openai_api_key:
            try:
                return await self._openai_json(system_prompt, user_prompt, temperature)
            except Exception as exc:
                logger.warning("GPT request failed: %s", exc)
                if self.settings.anthropic_api_key:
                    return await self._anthropic_json(system_prompt, user_prompt, temperature)
                raise AgentUnavailableError(f"GPT-4o request failed: {exc}") from exc

        return await self._anthropic_json(system_prompt, user_prompt, temperature)

    async def _openai_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
    ) -> dict[str, Any]:
        client = AsyncOpenAI(
            api_key=self.openai_api_key,
            base_url=self.openai_base_url,
            timeout=120.0,
        )
        response = await client.chat.completions.create(
            model=self.settings.openai_model,
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content or "{}"
        return self._parse_json(content)

    async def _anthropic_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float,
    ) -> dict[str, Any]:
        client = anthropic.AsyncAnthropic(api_key=self.settings.anthropic_api_key)
        response = await client.messages.create(
            model=self.settings.anthropic_model,
            max_tokens=8192,
            temperature=temperature,
            system=f"{system_prompt}\n\n只返回合法 JSON，不要 markdown 代码块。",
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        return self._parse_json(text)

    @staticmethod
    def _parse_json(content: str) -> dict[str, Any]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError:
            start = cleaned.find("{")
            end = cleaned.rfind("}")
            if start == -1 or end <= start:
                raise
            data = json.loads(cleaned[start : end + 1])
        if not isinstance(data, dict):
            raise ValueError("LLM response is not a JSON object")
        return data


growth_llm_service = GrowthLLMService()
