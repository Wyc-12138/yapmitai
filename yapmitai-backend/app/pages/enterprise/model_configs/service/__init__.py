from datetime import UTC, datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ModelConfig
from app.shared.crypto import api_key_last4, encrypt_api_key


def _dict(item: ModelConfig) -> dict:
    return {
        "id": item.id,
        "providerCode": item.provider_code,
        "providerName": item.provider_name,
        "modelCode": item.model_code,
        "displayName": item.display_name,
        "modelType": item.model_type,
        "apiBaseUrl": item.api_base_url,
        "apiKeyLast4": item.api_key_last4,
        "dimension": item.dimension,
        "maxInputTokens": item.max_input_tokens,
        "contextWindowTokens": item.context_window_tokens,
        "maxOutputTokens": item.max_output_tokens,
        "defaultTemperature": item.default_temperature,
        "enabled": item.enabled,
        "isDefault": item.is_default,
        "remark": item.remark,
    }


async def list_configs(
    db: AsyncSession, model_type: str | None = None, enabled: bool | None = None
) -> list[dict]:
    statement = select(ModelConfig).order_by(ModelConfig.model_type, ModelConfig.provider_code, ModelConfig.id)
    if model_type:
        statement = statement.where(ModelConfig.model_type == model_type)
    if enabled is not None:
        statement = statement.where(ModelConfig.enabled.is_(enabled))
    return [_dict(item) for item in (await db.scalars(statement)).all()]


async def get_config(db: AsyncSession, config_id: int) -> dict | None:
    item = await db.get(ModelConfig, config_id)
    return _dict(item) if item else None


async def _clear_default(db: AsyncSession, model_type: str, except_id: int | None = None) -> None:
    statement = update(ModelConfig).where(ModelConfig.model_type == model_type).values(is_default=False)
    if except_id:
        statement = statement.where(ModelConfig.id != except_id)
    await db.execute(statement)


async def create_config(db: AsyncSession, payload: dict) -> dict:
    api_key = payload.pop("api_key", "")
    model_type = payload["model_type"]
    duplicate = await db.scalar(
        select(ModelConfig.id).where(
            ModelConfig.provider_code == payload["provider_code"],
            ModelConfig.model_code == payload["model_code"],
            ModelConfig.model_type == model_type,
        )
    )
    if duplicate:
        raise ValueError("同一供应商下已存在相同类型和模型编码的配置")
    item = ModelConfig(
        provider_code=payload["provider_code"],
        provider_name=payload["provider_name"],
        model_code=payload["model_code"],
        display_name=payload["display_name"],
        model_type=model_type,
        api_base_url=str(payload["api_base_url"]),
        api_key_encrypted=encrypt_api_key(api_key),
        api_key_last4=api_key_last4(api_key),
        dimension=payload.get("dimension") if model_type == "embedding" else None,
        max_input_tokens=payload.get("max_input_tokens") if model_type == "embedding" else None,
        context_window_tokens=payload.get("context_window_tokens") if model_type == "chat" else None,
        max_output_tokens=payload.get("max_output_tokens") if model_type == "chat" else None,
        default_temperature=payload.get("default_temperature") if model_type == "chat" else None,
        enabled=payload.get("enabled", True),
        is_default=payload.get("is_default", False),
        remark=payload.get("remark"),
    )
    if item.is_default:
        await _clear_default(db, item.model_type)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return _dict(item)


async def update_config(db: AsyncSession, config_id: int, payload: dict) -> dict | None:
    item = await db.get(ModelConfig, config_id)
    if not item:
        return None
    target_provider = payload.get("provider_code", item.provider_code)
    target_model = payload.get("model_code", item.model_code)
    target_type = payload.get("model_type", item.model_type)
    duplicate = await db.scalar(
        select(ModelConfig.id).where(
            ModelConfig.provider_code == target_provider,
            ModelConfig.model_code == target_model,
            ModelConfig.model_type == target_type,
            ModelConfig.id != config_id,
        )
    )
    if duplicate:
        raise ValueError("同一供应商下已存在相同类型和模型编码的配置")
    api_key = payload.pop("api_key", None)
    for incoming, attr in (
        ("provider_code", "provider_code"),
        ("provider_name", "provider_name"),
        ("model_code", "model_code"),
        ("display_name", "display_name"),
        ("model_type", "model_type"),
        ("dimension", "dimension"),
        ("max_input_tokens", "max_input_tokens"),
        ("context_window_tokens", "context_window_tokens"),
        ("max_output_tokens", "max_output_tokens"),
        ("default_temperature", "default_temperature"),
        ("enabled", "enabled"),
        ("is_default", "is_default"),
        ("remark", "remark"),
    ):
        if incoming in payload:
            setattr(item, attr, payload[incoming])
    if item.model_type == "chat":
        item.dimension = None
        item.max_input_tokens = None
        if item.context_window_tokens is None or item.max_output_tokens is None:
            raise ValueError("Chat 模型必须填写上下文窗口和最大输出 Token")
    else:
        item.context_window_tokens = None
        item.max_output_tokens = None
        item.default_temperature = None
        if item.dimension is None or item.max_input_tokens is None:
            raise ValueError("Embedding 模型必须填写向量维度和最大输入 Token")
    if "api_base_url" in payload:
        item.api_base_url = str(payload["api_base_url"])
    if api_key is not None:
        item.api_key_encrypted = encrypt_api_key(api_key)
        item.api_key_last4 = api_key_last4(api_key)
    if item.is_default:
        await _clear_default(db, item.model_type, item.id)
    item.updated_at = datetime.now(UTC)
    await db.commit()
    await db.refresh(item)
    return _dict(item)


async def delete_config(db: AsyncSession, config_id: int) -> bool:
    item = await db.get(ModelConfig, config_id)
    if not item:
        return False
    await db.delete(item)
    await db.commit()
    return True
