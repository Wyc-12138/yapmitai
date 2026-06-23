import base64
import time
from datetime import UTC, datetime
from json import JSONDecodeError
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

        return await self._embed_batches(
            texts,
            model=model,
            api_base_url=None,
            api_key=None,
        )

    async def embed_with_config(
        self, texts: list[str], config: ModelConfig | None
    ) -> list[list[float]]:
        if config is None:
            raise InvalidParameterError(
                "知识库未关联可用的 Embedding 模型，请先在模型配置中启用 Embedding 模型"
            )
        if config.model_type != "embedding":
            raise InvalidParameterError("Model config is not an embedding model")
        if not config.enabled:
            raise InvalidParameterError("Model config is disabled")
        api_key = decrypt_api_key(config.api_key_encrypted)
        if not api_key:
            raise AgentUnavailableError(
                f"Embedding model '{config.display_name}' API key is not configured"
            )
        return await self._embed_batches(
            texts,
            model=config.model_code,
            api_base_url=config.api_base_url,
            api_key=api_key,
        )

    async def _embed_batches(
        self,
        texts: list[str],
        *,
        model: str,
        api_base_url: str | None,
        api_key: str | None,
        batch_size: int = 10,
    ) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for index in range(0, len(texts), batch_size):
            batch = texts[index : index + batch_size]
            payload = {"model": model, "input": batch}
            data = await self._post(
                "/embeddings",
                payload,
                api_base_url=api_base_url,
                api_key=api_key,
            )
            embeddings.extend(item["embedding"] for item in data["data"])
        return embeddings

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
        config: ModelConfig | None,
    ) -> dict[str, Any]:
        if config is None:
            raise InvalidParameterError(
                "没有可用的回答生成模型，请先在模型配置中启用 Chat 模型"
            )
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
        config: ModelConfig | None,
    ) -> dict[str, Any]:
        if config is None:
            raise InvalidParameterError(
                "没有可用的 Chat 模型，请先完成模型配置"
            )
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
        config: ModelConfig | None,
    ) -> str:
        if config is None:
            raise InvalidParameterError(
                "没有可用的图片理解模型，请先在模型配置中启用 Chat 模型"
            )
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
                try:
                    data = response.json()
                except JSONDecodeError as exc:
                    body = response.text.strip()
                    detail = body[:300] if body else "empty response body"
                    raise AgentUnavailableError(
                        f"External AI API returned non-JSON response: {detail}"
                    ) from exc
            usage = data.get("usage", {})
            await self._write_call_log(
                path=path,
                started_at=started_at,
                started=started,
                status="success",
                usage=usage,
            )
            return data
        except httpx.HTTPError as exc:
            upstream_detail = ""
            if isinstance(exc, httpx.HTTPStatusError):
                try:
                    payload = exc.response.json()
                    upstream_detail = (
                        payload.get("error", {}).get("message")
                        or payload.get("message")
                        or exc.response.text
                    )
                except (ValueError, AttributeError):
                    upstream_detail = exc.response.text
            upstream_detail = str(upstream_detail).strip()[:1000]
            error_message = (
                f"External AI API request failed: {upstream_detail}"
                if upstream_detail
                else f"External AI API request failed: {exc}"
            )
            await self._write_call_log(
                path=path,
                started_at=started_at,
                started=started,
                status="failed",
                error_msg=error_message,
            )
            raise AgentUnavailableError(error_message) from exc

    async def _write_call_log(
        self,
        *,
        path: str,
        started_at: datetime,
        started: float,
        status: str,
        usage: dict[str, Any] | None = None,
        error_msg: str | None = None,
    ) -> None:
        from app.db.database import AsyncSessionLocal
        from app.models import AgentCallLog

        usage = usage or {}
        try:
            async with AsyncSessionLocal() as session:
                session.add(
                    AgentCallLog(
                        agent_id=None,
                        module="embedding" if path == "/embeddings" else "answer",
                        path=path,
                        method="POST",
                        request_at=started_at,
                        response_at=datetime.now(UTC),
                        status=status,
                        latency_ms=round((time.perf_counter() - started) * 1000),
                        cost=0,
                        prompt_tokens=usage.get("prompt_tokens", 0),
                        completion_tokens=usage.get("completion_tokens", 0),
                        total_tokens=usage.get("total_tokens", 0),
                        error_msg=error_msg,
                    )
                )
                await session.commit()
        except Exception:
            return


external_ai_service = ExternalAIService()
