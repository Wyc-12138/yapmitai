from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_list_agents() -> None:
    response = client.get("/api/v1/agents", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["data"]) == 6


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
