from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_list_agents() -> None:
    response = client.get("/api/v1/agents", headers=headers)
    assert response.status_code == 200
    agents = response.json()["data"]
    assert len(agents) >= 10
    assert {
        "growth-market-analyst",
        "growth-brand-manager",
        "growth-content-creator",
        "growth-media-buying",
    }.issubset({item["code"] for item in agents})


def test_agent_crud() -> None:
    created = client.post(
        "/api/v1/agents",
        headers=headers,
        json={
            "code": "test-agent-crud",
            "name": "测试 Agent",
            "name_en": "Test Agent",
            "description": "接口测试临时数据",
            "system_prompt": "你是测试智能体。",
            "category": "测试",
            "status": "standby",
            "enabled": True,
            "today_done": 0,
            "month_kpi": 10,
        },
    )
    assert created.status_code == 200
    agent_id = created.json()["data"]["id"]

    updated = client.patch(
        f"/api/v1/agents/{agent_id}",
        headers=headers,
        json={"description": "已修改", "month_kpi": 20},
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["description"] == "已修改"
    assert updated.json()["data"]["monthKPI"] == 20

    deleted = client.delete(f"/api/v1/agents/{agent_id}", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["data"]["deleted"] is True


def test_assign_task() -> None:
    response = client.post(
        "/api/v1/agents/1/tasks",
        headers=headers,
        json={"description": "Generate an export plan", "priority": "high"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["status"] == "running"


def test_creation_falls_back_without_gateway_token() -> None:
    response = client.post(
        "/api/v1/creation/image",
        headers=headers,
        json={"prompt": "Hainan coconut water campaign"},
    )
    assert response.status_code == 200
    assert response.json()["data"]["fallback"] is True
