from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.team.workflow.report import generate_workflow_report

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_workflow_crud_and_agent_order(monkeypatch) -> None:
    teams = client.get("/api/v1/teams", headers=headers)
    assert teams.status_code == 200
    team_items = [item for item in teams.json()["data"] if item["memberCount"]]
    if not team_items:
        return
    team = team_items[0]
    suffix = uuid4().hex[:8]

    created = client.post(
        "/api/v1/workflows",
        headers=headers,
        json={
            "team_id": team["id"],
            "name": f"workflow-{suffix}",
            "description": "workflow API test",
            "enabled": True,
        },
    )
    assert created.status_code == 200
    task = created.json()["data"]
    assert task["teamId"] == team["id"]
    assert len(task["agents"]) == team["memberCount"]

    reversed_ids = [item["id"] for item in reversed(task["agents"])]
    order = client.put(
        f"/api/v1/workflows/{task['id']}/agent-order",
        headers=headers,
        json={"agent_ids": reversed_ids},
    )
    assert order.status_code == 200
    assert [item["id"] for item in order.json()["data"]["agents"]] == reversed_ids

    async def skip_execution(_: str) -> None:
        return None

    monkeypatch.setattr(
        "app.team.workflow.service.execute_run",
        skip_execution,
    )
    run = client.post(
        f"/api/v1/workflows/{task['id']}/runs",
        headers=headers,
        json={"prompt": "生成一份完整市场方案"},
    )
    assert run.status_code == 200
    run_id = run.json()["data"]["runId"]
    status = client.get(
        f"/api/v1/workflows/{task['id']}/runs/{run_id}", headers=headers
    )
    assert status.status_code == 200
    assert status.json()["data"]["status"] == "running"

    deleted = client.delete(f"/api/v1/workflows/{task['id']}", headers=headers)
    assert deleted.status_code == 200


def test_generate_workflow_pdf(tmp_path: Path) -> None:
    output = tmp_path / "workflow.pdf"
    result = generate_workflow_report(
        task_name="品牌增长",
        team_name="增长团队",
        prompt="生成东南亚市场增长方案",
        sections=[
            {
                "title": "1. 市场分析 Agent",
                "content": {
                    "summary": "市场存在增长机会",
                    "analysis": "目标用户对健康饮品需求持续增长。",
                    "recommendations": ["优先测试短视频渠道", "建立月度复盘机制"],
                    "deliverables": ["市场分析报告", "渠道执行清单"],
                },
            }
        ],
        output_path=output,
    )

    assert result.exists()
    assert result.read_bytes().startswith(b"%PDF")
    assert result.stat().st_size > 5_000
