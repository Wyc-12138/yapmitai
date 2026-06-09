from datetime import UTC, datetime
import json

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import AgentUnavailableError, InvalidParameterError
from app.models import AiTool, ModelConfig, SkillRunRecord
from app.shared.external_ai import external_ai_service


def _record_dict(item: SkillRunRecord) -> dict:
    return {
        "id": item.id,
        "skillId": item.skill_id,
        "title": item.title,
        "target": item.target,
        "suggestedAction": item.suggested_action,
        "deliverables": item.deliverables,
        "createdAt": item.created_at.strftime("%Y/%m/%d %H:%M:%S") if item.created_at else "",
    }


def _tool_dict(item: AiTool, records: list[SkillRunRecord] | None = None) -> dict:
    model = item.model_config
    return {
        "id": item.id,
        "name": item.name,
        "nameEn": item.name_en,
        "code": item.code,
        "category": item.category,
        "description": item.description,
        "icon": item.icon,
        "modelConfigId": item.model_config_id,
        "modelDisplayName": model.display_name if model else None,
        "modelCode": model.model_code if model else None,
        "promptTemplate": item.prompt_template,
        "inputSchema": item.input_schema,
        "outputSchema": item.output_schema,
        "enabled": item.enabled,
        "isSystem": item.is_system,
        "callCount": item.call_count,
        "sortOrder": item.sort_order,
        "createdAt": item.created_at.strftime("%Y/%m/%d %H:%M:%S") if item.created_at else "",
        "updatedAt": item.updated_at.strftime("%Y/%m/%d %H:%M:%S") if item.updated_at else "",
        "recentRecords": [_record_dict(record) for record in (records or [])],
    }


async def _chat_model(db: AsyncSession, model_config_id: int | None) -> ModelConfig | None:
    if model_config_id:
        model = await db.get(ModelConfig, model_config_id)
        if not model or model.model_type != "chat" or not model.enabled:
            raise InvalidParameterError("只能选择已启用的 Chat 模型")
        return model
    return await db.scalar(
        select(ModelConfig)
        .where(ModelConfig.model_type == "chat", ModelConfig.enabled.is_(True))
        .order_by(ModelConfig.is_default.desc(), ModelConfig.id)
    )


async def list_chat_models(db: AsyncSession) -> list[dict]:
    models = (
        await db.scalars(
            select(ModelConfig)
            .where(ModelConfig.model_type == "chat", ModelConfig.enabled.is_(True))
            .order_by(ModelConfig.is_default.desc(), ModelConfig.id)
        )
    ).all()
    return [
        {
            "id": item.id,
            "displayName": item.display_name,
            "modelCode": item.model_code,
            "providerName": item.provider_name,
            "isDefault": item.is_default,
        }
        for item in models
    ]


async def list_tools(
    db: AsyncSession, category: str | None = None, enabled: bool | None = None
) -> list[dict]:
    statement = (
        select(AiTool)
        .options(selectinload(AiTool.model_config))
        .order_by(AiTool.sort_order, AiTool.id)
    )
    if category:
        statement = statement.where(AiTool.category == category)
    if enabled is not None:
        statement = statement.where(AiTool.enabled.is_(enabled))
    tools = (await db.scalars(statement)).all()
    result = []
    for tool in tools:
        records = (
            await db.scalars(
                select(SkillRunRecord)
                .where(SkillRunRecord.skill_id == tool.id)
                .order_by(SkillRunRecord.created_at.desc(), SkillRunRecord.id.desc())
                .limit(3)
            )
        ).all()
        result.append(_tool_dict(tool, records))
    return result


async def get_tool(db: AsyncSession, tool_id: int) -> dict | None:
    item = await db.scalar(
        select(AiTool)
        .options(selectinload(AiTool.model_config))
        .where(AiTool.id == tool_id)
    )
    if not item:
        return None
    records = (
        await db.scalars(
            select(SkillRunRecord)
            .where(SkillRunRecord.skill_id == item.id)
            .order_by(SkillRunRecord.created_at.desc(), SkillRunRecord.id.desc())
            .limit(3)
        )
    ).all()
    return _tool_dict(item, records)


async def _ensure_unique_code(
    db: AsyncSession, code: str, except_id: int | None = None
) -> None:
    statement = select(AiTool.id).where(AiTool.code == code)
    if except_id:
        statement = statement.where(AiTool.id != except_id)
    if await db.scalar(statement):
        raise ValueError("工具编码已存在")


async def create_tool(db: AsyncSession, payload: dict) -> dict:
    await _ensure_unique_code(db, payload["code"])
    if payload.get("model_config_id"):
        await _chat_model(db, payload["model_config_id"])
    elif default_model := await _chat_model(db, None):
        payload["model_config_id"] = default_model.id
    item = AiTool(**payload)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return await get_tool(db, item.id)


async def update_tool(db: AsyncSession, tool_id: int, payload: dict) -> dict | None:
    item = await db.get(AiTool, tool_id)
    if not item:
        return None
    if "code" in payload:
        await _ensure_unique_code(db, payload["code"], tool_id)
    if payload.get("model_config_id"):
        await _chat_model(db, payload["model_config_id"])
    for key, value in payload.items():
        setattr(item, key, value)
    item.updated_at = datetime.now(UTC)
    await db.commit()
    return await get_tool(db, tool_id)


async def delete_tool(db: AsyncSession, tool_id: int) -> bool:
    item = await db.get(AiTool, tool_id)
    if not item:
        return False
    await db.delete(item)
    await db.commit()
    return True


async def toggle_tool(db: AsyncSession, tool_id: int, enabled: bool) -> dict | None:
    item = await db.get(AiTool, tool_id)
    if not item:
        return None
    item.enabled = enabled
    item.updated_at = datetime.now(UTC)
    await db.commit()
    return await get_tool(db, tool_id)


def _render_prompt(template: str, task: str) -> str:
    return template.replace("{{task}}", task).replace("{task}", task)


def _fallback_result(tool: AiTool, task: str) -> dict:
    return {
        "title": f"{tool.name} · 结果包",
        "target": task,
        "suggested_action": f"由{tool.name}生成首版材料，交给AI员工复核后发布。",
        "deliverables": "执行清单、渠道建议、风险提醒、下一步审批项。",
    }


def _parse_result(tool: AiTool, task: str, answer: str) -> dict:
    try:
        data = json.loads(answer)
    except json.JSONDecodeError:
        return {
            "title": f"{tool.name} · 结果包",
            "target": task,
            "suggested_action": answer[:1000],
            "deliverables": "请查看模型返回正文，并按业务需要拆解为交付清单。",
        }
    return {
        "title": data.get("title") or f"{tool.name} · 结果包",
        "target": data.get("target") or task,
        "suggested_action": data.get("suggested_action") or data.get("suggestedAction"),
        "deliverables": data.get("deliverables"),
    }


async def run_tool(
    db: AsyncSession, tool_id: int, task: str, model_config_id: int | None = None
) -> dict | None:
    tool = await db.get(AiTool, tool_id)
    if not tool:
        return None
    if not tool.enabled:
        raise InvalidParameterError("工具已停用")
    model = await _chat_model(db, model_config_id or tool.model_config_id)
    if not model:
        raise AgentUnavailableError("没有可用的 Chat 模型配置")
    system_prompt = (
        "你是企业AI工具中心的 Prompt Skill 执行器。"
        "请严格输出 JSON，字段为 title、target、suggested_action、deliverables。"
    )
    user_prompt = _render_prompt(tool.prompt_template, task)
    try:
        generated = await external_ai_service.generate_with_config(
            system_prompt, user_prompt, model
        )
        result = _parse_result(tool, task, generated["answer"])
    except AgentUnavailableError:
        result = _fallback_result(tool, task)
    record = SkillRunRecord(skill_id=tool.id, **result)
    db.add(record)
    await db.execute(
        update(AiTool)
        .where(AiTool.id == tool.id)
        .values(call_count=AiTool.call_count + 1, updated_at=datetime.now(UTC))
    )
    await db.commit()
    await db.refresh(record)
    return _record_dict(record)
