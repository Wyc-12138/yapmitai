from uuid import uuid4

from app.shared.gateway import gateway_service


async def search_leads(payload: dict) -> dict:
    limit = payload.get("limit", 20)
    leads = [
        {"company": f"海南品牌企业{i + 1}", "contact": f"contact{i + 1}@example.com", "score": 96 - i, "source": "public"}
        for i in range(min(limit, 10))
    ]
    return await gateway_service.call("outreach-leads", payload, {"leads": leads})


async def create_call_task(payload: dict) -> dict:
    return await gateway_service.call(
        "outreach-call",
        payload,
        {"taskId": str(uuid4()), "status": "queued", "consentFlag": payload["consentFlag"]},
    )
