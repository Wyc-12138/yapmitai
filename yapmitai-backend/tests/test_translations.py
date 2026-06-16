from fastapi.testclient import TestClient

from app.main import app
from app.pages.system.translations import service

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_translate_batch(monkeypatch) -> None:
    service._translation_cache.clear()

    async def fake_complete_json(**_kwargs):
        return {"translations": {"0": "Switch Portal", "1": "AI Tools"}}

    monkeypatch.setattr(
        service.growth_llm_service, "complete_json", fake_complete_json
    )
    response = client.post(
        "/api/v1/translations/batch",
        headers=headers,
        json={"texts": ["切换入口", "AI工具中心"]},
    )

    assert response.status_code == 200
    assert response.json()["data"]["translations"] == {
        "切换入口": "Switch Portal",
        "AI工具中心": "AI Tools",
    }


def test_translate_batch_uses_cache(monkeypatch) -> None:
    service._translation_cache.clear()
    service._translation_cache["企业入口"] = "Enterprise Portal"

    async def fail_if_called(**_kwargs):
        raise AssertionError("cached translations should not call the model")

    monkeypatch.setattr(
        service.growth_llm_service, "complete_json", fail_if_called
    )
    response = client.post(
        "/api/v1/translations/batch",
        headers=headers,
        json={"texts": ["企业入口"]},
    )

    assert response.status_code == 200
    assert response.json()["data"]["translations"]["企业入口"] == "Enterprise Portal"
