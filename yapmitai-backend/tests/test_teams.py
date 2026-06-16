from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.team.schema import TeamCreate

client = TestClient(app)
headers = {"X-API-Key": "yap_demo_key_2026"}


def test_team_name_accepts_single_character() -> None:
    payload = TeamCreate(name="1")

    assert payload.name == "1"


def test_create_team_with_single_character_name() -> None:
    name = chr(0x4E00 + int(uuid4().hex[:4], 16) % 0x4FFF)
    created = client.post(
        "/api/v1/teams",
        headers=headers,
        json={"name": name, "description": "2", "enabled": True, "agent_ids": []},
    )

    assert created.status_code == 200
    team_id = created.json()["data"]["id"]

    deleted = client.delete(f"/api/v1/teams/{team_id}", headers=headers)
    assert deleted.status_code == 200


def test_team_crud_and_members() -> None:
    suffix = uuid4().hex[:8]
    agent_count_before = len(
        client.get("/api/v1/teams/agent-options", headers=headers).json()["data"]
    )
    agents = client.get("/api/v1/teams/agent-options", headers=headers)
    assert agents.status_code == 200
    agent_ids = [item["id"] for item in agents.json()["data"][:3]]
    assert agent_ids

    created = client.post(
        "/api/v1/teams",
        headers=headers,
        json={
            "name": f"测试AI团队-{suffix}",
            "description": "团队接口测试",
            "enabled": True,
            "agent_ids": agent_ids[:2],
        },
    )
    assert created.status_code == 200
    team = created.json()["data"]
    team_id = team["id"]
    assert team["memberCount"] == len(agent_ids[:2])

    updated = client.patch(
        f"/api/v1/teams/{team_id}",
        headers=headers,
        json={
            "name": f"测试AI团队-已修改-{suffix}",
            "agent_ids": agent_ids,
        },
    )
    assert updated.status_code == 200
    assert updated.json()["data"]["memberCount"] == len(agent_ids)

    detail = client.get(f"/api/v1/teams/{team_id}", headers=headers)
    assert detail.status_code == 200
    assert detail.json()["data"]["agentIds"] == agent_ids

    deleted = client.delete(f"/api/v1/teams/{team_id}", headers=headers)
    assert deleted.status_code == 200
    assert deleted.json()["data"]["deleted"] is True
    agent_count_after = len(
        client.get("/api/v1/teams/agent-options", headers=headers).json()["data"]
    )
    assert agent_count_after == agent_count_before
