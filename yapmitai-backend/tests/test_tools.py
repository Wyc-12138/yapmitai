from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.main import app
from app.pages.enterprise.tools import service

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_tools_crud_and_run(monkeypatch) -> None:
    models = client.get("/api/v1/tools/chat-models", headers=headers)
    assert models.status_code == 200
    chat_models = models.json()["data"]
    assert chat_models

    created = client.post(
        "/api/v1/tools",
        headers=headers,
        json={
            "name": "测试Prompt技能",
            "name_en": "Test Prompt Skill",
            "code": "test-prompt-skill",
            "category": "运营工具",
            "description": "用于验证工具CRUD",
            "icon": "测",
            "model_config_id": chat_models[0]["id"],
            "prompt_template": "请处理任务：{{task}}",
            "input_schema": {"fields": [{"name": "task", "type": "textarea"}]},
            "output_schema": {"type": "object"},
            "enabled": True,
            "is_system": False,
            "sort_order": 999,
        },
    )
    assert created.status_code == 200
    tool = created.json()["data"]
    tool_id = tool["id"]

    updated = client.patch(
        f"/api/v1/tools/{tool_id}",
        headers=headers,
        json={"description": "修改后的说明"},
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["description"] == "修改后的说明"

    monkeypatch.setattr(
        service.external_ai_service,
        "generate_with_config",
        AsyncMock(
            return_value={
                "answer": (
                    '{"title":"测试结果包","target":"测试目标",'
                    '"suggested_action":"测试动作","deliverables":"测试交付物"}'
                ),
                "model": "test",
                "usage": {},
            }
        ),
    )
    for index in range(4):
        run = client.post(
            f"/api/v1/tools/{tool_id}/run",
            headers=headers,
            json={"task": f"测试任务{index}", "model_config_id": chat_models[0]["id"]},
        )
        assert run.status_code == 200

    detail = client.get(f"/api/v1/tools/{tool_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["callCount"] == 4
    assert len(detail.json()["data"]["recentRecords"]) == 3

    deleted = client.delete(f"/api/v1/tools/{tool_id}", headers=headers)
    assert deleted.status_code == 200
