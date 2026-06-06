from app.services.gateway import gateway_service


async def reply(payload: dict) -> dict:
    return await gateway_service.call(
        "cs-personalwx",
        payload,
        {"reply": f"已收到：{payload['content']}", "takeoverMode": payload["takeover_mode"]},
    )
