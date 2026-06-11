from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "yap_demo_key_2026"}


def test_growth_start_requires_api_key() -> None:
    response = client.post("/api/task/start", json={"prompt": "测试需求"})
    assert response.status_code == 401


def test_growth_start_requires_prompt_or_fields() -> None:
    response = client.post("/api/task/start", json={}, headers=HEADERS)
    assert response.status_code == 422


@patch("app.growth.router.execute_growth_task", new_callable=AsyncMock)
@patch("app.growth.router.create_growth_task_record", new_callable=AsyncMock)
@patch("app.growth.router.parse_prompt_to_input", new_callable=AsyncMock)
def test_growth_start_accepts_prompt(
    mock_parse,
    mock_create,
    mock_execute,
) -> None:
    from app.growth.schemas import AgentInput

    mock_parse.return_value = AgentInput(
        task_id="task-test123456",
        product="海南椰子水",
        market="马来西亚",
        target_customer="健康饮品消费者",
        budget="待评估",
    )
    mock_create.return_value = object()

    response = client.post(
        "/api/task/start",
        json={"prompt": "我要把海南椰子水卖到马来西亚市场"},
        headers=HEADERS,
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"]["status"] == "running"
    assert payload["data"]["current_step"] == "market_analyst"
    assert payload["data"]["input"]["product"] == "海南椰子水"
    mock_execute.assert_called_once()
