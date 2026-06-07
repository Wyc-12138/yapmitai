from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_model_config_crud() -> None:
    created = client.post(
        "/api/v1/model-configs",
        headers=headers,
        json={
            "provider_code": "test-provider",
            "provider_name": "Test Provider",
            "model_code": "test-chat-model",
            "display_name": "测试 Chat 模型",
            "model_type": "chat",
            "api_base_url": "https://example.com/v1",
            "api_key": "test-secret-1234",
            "context_window_tokens": 32000,
            "max_output_tokens": 2048,
            "default_temperature": 0.3,
            "enabled": True,
            "is_default": False,
            "remark": "CRUD test",
        },
    )
    assert created.status_code == 200
    item = created.json()["data"]
    config_id = item["id"]
    assert item["contextWindowTokens"] == 32000
    assert item["maxOutputTokens"] == 2048
    assert item["apiKeyLast4"] == "1234"
    assert "apiKey" not in item

    listed = client.get("/api/v1/model-configs?model_type=chat", headers=headers)
    assert listed.status_code == 200
    assert any(config["id"] == config_id for config in listed.json()["data"])

    updated = client.patch(
        f"/api/v1/model-configs/{config_id}",
        headers=headers,
        json={
            "display_name": "修改后的 Chat 模型",
            "context_window_tokens": 64000,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["displayName"] == "修改后的 Chat 模型"
    assert updated.json()["data"]["contextWindowTokens"] == 64000

    deleted = client.delete(f"/api/v1/model-configs/{config_id}", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["data"]["deleted"] is True
