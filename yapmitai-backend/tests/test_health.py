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


def test_cors_preflight_does_not_require_api_key() -> None:
    response = client.options(
        "/api/v1/model-configs",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type,x-api-key",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_dashboard_with_key() -> None:
    response = client.get(
        "/api/v1/dashboard/overview",
        headers={"X-API-Key": "yap_demo_key_2026"},
    )
    assert response.status_code == 200
    assert len(response.json()["data"]["kpis"]) == 4
