from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Agent
from app.team.models import AiTeam, AiTeamAgent


def _agent_dict(agent: Agent) -> dict:
    return {
        "id": agent.id,
        "code": agent.code,
        "name": agent.name,
        "nameEn": agent.name_en or "",
        "category": agent.category,
        "status": agent.status,
        "enabled": agent.enabled,
    }


async def _team_agents(db: AsyncSession, team_id: int) -> list[dict]:
    agents = (
        await db.scalars(
            select(Agent)
            .join(AiTeamAgent, AiTeamAgent.agent_id == Agent.id)
            .where(AiTeamAgent.team_id == team_id)
            .order_by(Agent.id)
        )
    ).all()
    return [_agent_dict(agent) for agent in agents]


async def _team_dict(db: AsyncSession, team: AiTeam) -> dict:
    agents = await _team_agents(db, team.id)
    return {
        "id": team.id,
        "name": team.name,
        "description": team.description or "",
        "enabled": team.enabled,
        "memberCount": len(agents),
        "agents": agents,
        "agentIds": [agent["id"] for agent in agents],
        "createdAt": team.created_at.isoformat() if team.created_at else None,
        "updatedAt": team.updated_at.isoformat() if team.updated_at else None,
    }


async def list_teams(db: AsyncSession) -> list[dict]:
    teams = (await db.scalars(select(AiTeam).order_by(AiTeam.id.desc()))).all()
    return [await _team_dict(db, team) for team in teams]


async def get_team(db: AsyncSession, team_id: int) -> dict | None:
    team = await db.get(AiTeam, team_id)
    return await _team_dict(db, team) if team else None


async def list_agent_options(db: AsyncSession) -> list[dict]:
    agents = (await db.scalars(select(Agent).order_by(Agent.category, Agent.id))).all()
    return [_agent_dict(agent) for agent in agents]


async def _validate_agent_ids(db: AsyncSession, agent_ids: list[int]) -> list[int]:
    unique_ids = list(dict.fromkeys(agent_ids))
    if not unique_ids:
        return []
    valid_ids = set(
        (await db.scalars(select(Agent.id).where(Agent.id.in_(unique_ids)))).all()
    )
    missing = [agent_id for agent_id in unique_ids if agent_id not in valid_ids]
    if missing:
        raise ValueError(f"AI员工不存在：{', '.join(map(str, missing))}")
    return unique_ids


async def _replace_members(
    db: AsyncSession, team_id: int, agent_ids: list[int]
) -> None:
    valid_ids = await _validate_agent_ids(db, agent_ids)
    await db.execute(delete(AiTeamAgent).where(AiTeamAgent.team_id == team_id))
    db.add_all(
        AiTeamAgent(team_id=team_id, agent_id=agent_id) for agent_id in valid_ids
    )


async def create_team(db: AsyncSession, payload: dict) -> dict:
    if await db.scalar(select(AiTeam.id).where(AiTeam.name == payload["name"])):
        raise ValueError("团队名称已存在")
    agent_ids = payload.pop("agent_ids", [])
    team = AiTeam(**payload)
    db.add(team)
    await db.flush()
    await _replace_members(db, team.id, agent_ids)
    await db.commit()
    await db.refresh(team)
    return await _team_dict(db, team)


async def update_team(
    db: AsyncSession, team_id: int, payload: dict
) -> dict | None:
    team = await db.get(AiTeam, team_id)
    if not team:
        return None
    if "name" in payload and payload["name"] != team.name:
        if await db.scalar(select(AiTeam.id).where(AiTeam.name == payload["name"])):
            raise ValueError("团队名称已存在")
    agent_ids = payload.pop("agent_ids", None)
    for field, value in payload.items():
        setattr(team, field, value)
    if agent_ids is not None:
        await _replace_members(db, team.id, agent_ids)
    await db.commit()
    await db.refresh(team)
    return await _team_dict(db, team)


async def delete_team(db: AsyncSession, team_id: int) -> bool:
    team = await db.get(AiTeam, team_id)
    if not team:
        return False
    await db.delete(team)
    await db.commit()
    return True


async def team_summary(db: AsyncSession) -> dict:
    return {
        "teamCount": await db.scalar(select(func.count()).select_from(AiTeam)) or 0,
        "enabledCount": await db.scalar(
            select(func.count()).select_from(AiTeam).where(AiTeam.enabled.is_(True))
        )
        or 0,
        "memberLinks": await db.scalar(
            select(func.count()).select_from(AiTeamAgent)
        )
        or 0,
    }
