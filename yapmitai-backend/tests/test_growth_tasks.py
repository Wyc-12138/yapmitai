from datetime import UTC, datetime
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.growth import router as growth_router
from app.main import app

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


async def _noop_execute(task_id: str) -> None:
    return None


def test_start_growth_task(monkeypatch) -> None:
    created: dict = {}

    async def fake_create_growth_task_record(**kwargs):
        created.update(kwargs)
        return SimpleNamespace(id=kwargs["task_id"])

    monkeypatch.setattr(
        growth_router, "create_growth_task_record", fake_create_growth_task_record
    )
    monkeypatch.setattr(growth_router, "execute_growth_task", _noop_execute)

    response = client.post(
        "/api/v1/growth/tasks",
        headers=headers,
        json={
            "product": "海南椰子水",
            "market": "东南亚",
            "target_customer": "20-35 岁健康生活人群",
            "budget": "50 万元",
        },
    )

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["status"] == "running"
    assert payload["currentStep"] == "market_analyst"
    assert created["agent_input"].product == "海南椰子水"


def test_get_growth_task(monkeypatch) -> None:
    now = datetime.now(UTC)

    async def fake_get_growth_task(task_id: str):
        return SimpleNamespace(
            id=task_id,
            status="completed",
            current_step="completed",
            prompt="将海南椰子水推向东南亚",
            product="海南椰子水",
            market="东南亚",
            target_customer="健康生活人群",
            budget="50 万元",
            context={"market_report": {"summary": "市场具备增长空间"}},
            agent_outputs=[],
            pdf_path="storage/growth-reports/task-demo.pdf",
            error_message=None,
            created_at=now,
            completed_at=now,
        )

    monkeypatch.setattr(growth_router, "get_growth_task", fake_get_growth_task)

    response = client.get("/api/v1/growth/tasks/task-demo", headers=headers)

    assert response.status_code == 200
    payload = response.json()["data"]
    assert payload["taskId"] == "task-demo"
    assert payload["pdfReady"] is True
    assert payload["context"]["market_report"]["summary"] == "市场具备增长空间"
