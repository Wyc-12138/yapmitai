from unittest.mock import AsyncMock

import httpx
import pytest
from sqlalchemy import select

from app.core.exceptions import AgentUnavailableError
from app.db.database import AsyncSessionLocal
from app.models import KnowledgeBase, ModelConfig
from app.pages.enterprise.knowledge.agent import service
from app.shared.external_ai import external_ai_service


@pytest.mark.asyncio
async def test_missing_library_embedding_config_uses_enabled_default() -> None:
    async with AsyncSessionLocal() as db:
        library = await db.scalar(select(KnowledgeBase).limit(1))
        embedding = await db.scalar(
            select(ModelConfig).where(
                ModelConfig.model_type == "embedding",
                ModelConfig.enabled.is_(True),
            )
        )
        if not library or not embedding:
            pytest.skip("Knowledge base or embedding config is unavailable")
        library.embedding_model_config_id = None
        await db.commit()

        resolved = await service._embedding_config_for_library(db, library)

        assert resolved.id == embedding.id
        assert library.embedding_model_config_id == embedding.id


@pytest.mark.asyncio
async def test_upstream_error_body_is_exposed(monkeypatch) -> None:
    request = httpx.Request("POST", "https://example.com/v1/embeddings")
    response = httpx.Response(
        503,
        request=request,
        json={"error": {"message": "模型无可用渠道"}},
    )
    mocked_post = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "503 Service Unavailable",
            request=request,
            response=response,
        )
    )
    monkeypatch.setattr(httpx.AsyncClient, "post", mocked_post)

    with pytest.raises(AgentUnavailableError, match="模型无可用渠道"):
        await external_ai_service._post(
            "/embeddings",
            {"model": "embedding-model", "input": ["test"]},
            api_base_url="https://example.com/v1",
            api_key="test-key",
        )


@pytest.mark.asyncio
async def test_upstream_non_json_body_is_reported(monkeypatch) -> None:
    response = httpx.Response(
        200,
        request=httpx.Request("POST", "https://example.com/v1/embeddings"),
        text="",
    )
    mocked_post = AsyncMock(return_value=response)
    monkeypatch.setattr(httpx.AsyncClient, "post", mocked_post)

    with pytest.raises(
        AgentUnavailableError,
        match="External AI API returned non-JSON response: empty response body",
    ):
        await external_ai_service._post(
            "/embeddings",
            {"model": "embedding-model", "input": ["test"]},
            api_base_url="https://example.com/v1",
            api_key="test-key",
        )


@pytest.mark.asyncio
async def test_embedding_requests_are_batched_to_provider_limit(monkeypatch) -> None:
    calls: list[list[str]] = []

    async def fake_post(_path, payload, **_kwargs):
        batch = payload["input"]
        calls.append(batch)
        return {
            "data": [
                {"embedding": [float(len(calls)), float(index)]}
                for index, _text in enumerate(batch)
            ]
        }

    monkeypatch.setattr(external_ai_service, "_post", fake_post)

    embeddings = await external_ai_service._embed_batches(
        [f"chunk-{index}" for index in range(25)],
        model="embedding-model",
        api_base_url="https://example.com/v1",
        api_key="test-key",
    )

    assert [len(batch) for batch in calls] == [10, 10, 5]
    assert len(embeddings) == 25
