from app.shared.gateway import gateway_service


async def reply(payload: dict) -> dict:
    return await gateway_service.call(
        "cs-corpwx",
        payload,
        {"reply": f"企微助手已处理：{payload['content']}", "department": payload["department"]},
    )
