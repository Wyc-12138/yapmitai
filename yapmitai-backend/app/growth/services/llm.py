import json
import re
from typing import Any

import httpx
from sqlalchemy import select

from app.core.config import get_settings
from app.core.exceptions import AgentUnavailableError
from app.db.database import AsyncSessionLocal
from app.models import ModelConfig
from app.shared.crypto import decrypt_api_key


class GrowthLLMService:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def model(self) -> str:
        models = self.settings.answer_model_list
        return models[0] if models else "gpt-4o-mini"

    async def complete_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3,
        model_config: ModelConfig | None = None,
    ) -> dict[str, Any]:
        config = model_config or await self._get_default_chat_config()
        api_key = (
            decrypt_api_key(config.api_key_encrypted)
            if config
            else self.settings.external_ai_api_key
        )
        if not api_key:
            raise AgentUnavailableError(
                "请先在模型配置页面为默认 Chat 模型填写 API Key"
            )

        api_base_url = config.api_base_url if config else self.settings.external_ai_base_url
        payload = {
            "model": config.model_code if config else self.model,
            "temperature": (
                config.default_temperature
                if config and config.default_temperature is not None
                else temperature
            ),
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if config and config.max_output_tokens:
            payload["max_tokens"] = config.max_output_tokens

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        url = f"{api_base_url.rstrip('/')}/chat/completions"
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"] or "{}"
        return self._parse_json(content)

    async def _get_default_chat_config(self) -> ModelConfig | None:
        async with AsyncSessionLocal() as session:
            result = await session.scalars(
                select(ModelConfig)
                .where(
                    ModelConfig.model_type == "chat",
                    ModelConfig.enabled.is_(True),
                )
                .order_by(ModelConfig.is_default.desc(), ModelConfig.id.asc())
                .limit(1)
            )
            return result.first()

    @staticmethod
    def _parse_json(content: str) -> dict[str, Any]:
        cleaned = content.strip()
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
        cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            start, end = cleaned.find("{"), cleaned.rfind("}")
            if start < 0 or end <= start:
                raise
            result = json.loads(cleaned[start : end + 1])
        if not isinstance(result, dict):
            raise ValueError("模型返回内容不是 JSON 对象")
        return result


growth_llm_service = GrowthLLMService()
