from app.shared.mock_data import ALLIANCE_MEMBERS, ALLIANCE_PLANS


async def get_dashboard(_db) -> dict:
    return {
        "overview": {"members": 128, "active": 96, "gmv": 12.4},
        "plans": ALLIANCE_PLANS,
        "members": ALLIANCE_MEMBERS,
    }


async def create_member(_db, payload: dict) -> dict:
    return {
        "name": payload["name"],
        "type": payload["enterprise_type"],
        "level": payload["ai_level"],
        "status": "active",
    }
