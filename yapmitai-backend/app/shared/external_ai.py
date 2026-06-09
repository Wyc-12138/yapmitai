import base64
import time
from datetime import UTC, datetime
from typing import Any

import httpx

from app.core.config import get_settings
from app.core.exceptions import AgentUnavailableError, InvalidParameterError
from app.models import ModelConfig
from app.shared.crypto import decrypt_api_key


class ExternalAIService:
    def __init__(self) -> None:
        self.settings = get_settings()

    @property
    def configured(self) -> bool:
        return bool(self.settings.external_ai_api_key)

    def available_models(self) -> dict[str, Any]:
        return {
            "configured": self.configured,
            "baseUrl": self.settings.external_ai_base_url,
            "embeddingModels": self.settings.embedding_model_list,
            "answerModels": self.settings.answer_model_list,
        }

    async def embed(self, texts: list[str], model: str) -> list[list[float]]:
        if model not in self.settings.embedding_model_list:
            raise InvalidParameterError(f"Unsupported embedding model: {model}")
        if not self.configured:
            raise AgentUnavailableError("External AI API key is not configured")

        payload = {"model": model, "input": texts}
        data = await self._post("/embeddings", payload)
        return [item["embedding"] for item in data["data"]]

    async def embed_with_config(
        self, texts: list[str], config: ModelConfig
    ) -> list[list[float]]:
        if config.model_type != "embedding":
            raise InvalidParameterError("Model config is not an embedding model")
        if not config.enabled:
            raise InvalidParameterError("Model config is disabled")
        api_key = decrypt_api_key(config.api_key_encrypted)
        if not api_key:
            raise AgentUnavailableError(
                f"Embedding model '{config.display_name}' API key is not configured"
            )
        payload = {"model": config.model_code, "input": texts}
        data = await self._post(
            "/embeddings",
            payload,
            api_base_url=config.api_base_url,
            api_key=api_key,
        )
        return [item["embedding"] for item in data["data"]]

    async def answer(
        self,
        question: str,
        contexts: list[str],
        model: str,
    ) -> dict[str, Any]:
        if model not in self.settings.answer_model_list:
            raise InvalidParameterError(f"Unsupported answer model: {model}")
        if not self.configured:
            raise AgentUnavailableError("External AI API key is not configured")

        context_text = "\n\n".join(contexts) if contexts else "暂无检索上下文。"
        payload = {
            "model": model,
            "temperature": 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": "你是企业知识库助手。仅根据提供的知识上下文回答；无法确定时明确说明。",
                },
                {
                    "role": "user",
                    "content": f"知识上下文：\n{context_text}\n\n用户问题：{question}",
                },
            ],
        }
        data = await self._post("/chat/completions", payload)
        return {
            "answer": data["choices"][0]["message"]["content"],
            "model": model,
            "usage": data.get("usage", {}),
        }

    async def answer_with_config(
        self,
        question: str,
        contexts: list[str],
        config: ModelConfig,
    ) -> dict[str, Any]:
        if config.model_type != "chat":
            raise InvalidParameterError("Model config is not a chat model")
        if not config.enabled:
            raise InvalidParameterError("Model config is disabled")
        api_key = decrypt_api_key(config.api_key_encrypted)
        if not api_key:
            raise AgentUnavailableError(
                f"Chat model '{config.display_name}' API key is not configured"
            )
        context_text = "\n\n".join(contexts) if contexts else "暂无检索上下文。"
        payload = {
            "model": config.model_code,
            "temperature": config.default_temperature if config.default_temperature is not None else 0.2,
            "messages": [
                {
                    "role": "system",
                    "content": "你是企业知识库助手。仅根据提供的知识上下文回答；无法确定时明确说明。",
                },
                {
                    "role": "user",
                    "content": f"知识上下文：\n{context_text}\n\n用户问题：{question}",
                },
            ],
        }
        if config.max_output_tokens:
            payload["max_tokens"] = config.max_output_tokens
        data = await self._post(
            "/chat/completions",
            payload,
            api_base_url=config.api_base_url,
            api_key=api_key,
        )
        return {
            "answer": data["choices"][0]["message"]["content"],
            "model": config.model_code,
            "usage": data.get("usage", {}),
        }

    async def generate_with_config(
        self,
        system_prompt: str,
        user_prompt: str,
        config: ModelConfig,
    ) -> dict[str, Any]:
        if config.model_type != "chat":
            raise InvalidParameterError("Model config is not a chat model")
        if not config.enabled:
            raise InvalidParameterError("Model config is disabled")
        api_key = decrypt_api_key(config.api_key_encrypted)
        if not api_key:
            raise AgentUnavailableError(
                f"Chat model '{config.display_name}' API key is not configured"
            )
        payload = {
            "model": config.model_code,
            "temperature": config.default_temperature if config.default_temperature is not None else 0.2,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }
        if config.max_output_tokens:
            payload["max_tokens"] = config.max_output_tokens
        data = await self._post(
            "/chat/completions",
            payload,
            api_base_url=config.api_base_url,
            api_key=api_key,
        )
        return {
            "answer": data["choices"][0]["message"]["content"],
            "model": config.model_code,
            "usage": data.get("usage", {}),
        }

    async def describe_image(
        self,
        content: bytes,
        content_type: str,
        model: str,
    ) -> str:
        if model not in self.settings.answer_model_list:
            raise InvalidParameterError(f"Unsupported vision model: {model}")
        if not self.configured:
            raise AgentUnavailableError("External AI API key is not configured")

        encoded = base64.b64encode(content).decode("ascii")
        payload = {
            "model": model,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "请详细描述图片中的主体、文字、场景、品牌元素和可检索信息。",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{content_type};base64,{encoded}"
                            },
                        },
                    ],
                }
            ],
        }
        data = await self._post("/chat/completions", payload)
        return data["choices"][0]["message"]["content"]

    async def describe_image_with_config(
        self,
        content: bytes,
        content_type: str,
        config: ModelConfig,
    ) -> str:
        if config.model_type != "chat":
            raise InvalidParameterError("Model config is not a chat model")
        api_key = decrypt_api_key(config.api_key_encrypted)
        if not api_key:
            raise AgentUnavailableError(
                f"Chat model '{config.display_name}' API key is not configured"
            )
        encoded = base64.b64encode(content).decode("ascii")
        payload = {
            "model": config.model_code,
            "temperature": config.default_temperature if config.default_temperature is not None else 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "请详细描述图片中的主体、文字、场景、品牌元素和可检索信息。"},
                        {"type": "image_url", "image_url": {"url": f"data:{content_type};base64,{encoded}"}},
                    ],
                }
            ],
        }
        data = await self._post(
            "/chat/completions",
            payload,
            api_base_url=config.api_base_url,
            api_key=api_key,
        )
        return data["choices"][0]["message"]["content"]

    async def _post(
        self,
        path: str,
        payload: dict[str, Any],
        api_base_url: str | None = None,
        api_key: str | None = None,
    ) -> dict[str, Any]:
        from app.db.postgres import AsyncSessionLocal
        from app.models import AgentCallLog

        url = f"{(api_base_url or self.settings.external_ai_base_url).rstrip('/')}{path}"
        headers = {
            "Authorization": f"Bearer {api_key or self.settings.external_ai_api_key}",
            "Content-Type": "application/json",
        }
        started_at = datetime.now(UTC)
        started = time.perf_counter()
        try:
            async with httpx.AsyncClient(
                timeout=self.settings.agent_timeout_seconds
            ) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
            usage = data.get("usage", {})
            async with AsyncSessionLocal() as session:
                session.add(
                    AgentCallLog(
                        agent_id=None,
                        module="embedding" if path == "/embeddings" else "answer",
                        path=path,
                        method="POST",
                        request_at=started_at,
                        response_at=datetime.now(UTC),
                        status="success",
                        latency_ms=round((time.perf_counter() - started) * 1000),
                        cost=0,
                        prompt_tokens=usage.get("prompt_tokens", 0),
                        completion_tokens=usage.get("completion_tokens", 0),
                        total_tokens=usage.get("total_tokens", 0),
                    )
                )
                await session.commit()
            return data
        except httpx.HTTPError as exc:
            async with AsyncSessionLocal() as session:
                session.add(
                    AgentCallLog(
                        agent_id=None,
                        module="embedding" if path == "/embeddings" else "answer",
                        path=path,
                        method="POST",
                        request_at=started_at,
                        response_at=datetime.now(UTC),
                        status="failed",
                        latency_ms=round((time.perf_counter() - started) * 1000),
                        cost=0,
                        error_msg=str(exc),
                    )
                )
                await session.commit()
            raise AgentUnavailableError(f"External AI API request failed: {exc}") from exc


external_ai_service = ExternalAIService()
