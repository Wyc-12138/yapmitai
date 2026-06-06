from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"]["status"] == "healthy"


def test_api_requires_key() -> None:
    response = client.get("/api/v1/dashboard/overview")
    assert response.status_code == 401


def test_dashboard_with_key() -> None:
    response = client.get(
        "/api/v1/dashboard/overview",
        headers={"X-API-Key": "yap_demo_key_2026"},
    )
    assert response.status_code == 200
    assert len(response.json()["data"]["kpis"]) == 4
