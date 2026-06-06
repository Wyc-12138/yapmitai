from app.services.mock_data import ALLIANCE_MEMBERS, ALLIANCE_PLANS


def get_dashboard() -> dict:
    return {
        "overview": {"members": 128, "active": 96, "gmv": 12.4},
        "plans": ALLIANCE_PLANS,
        "members": ALLIANCE_MEMBERS,
    }


def create_member(payload: dict) -> dict:
    member = {
        "name": payload["name"],
        "type": payload["enterprise_type"],
        "level": payload["ai_level"],
        "status": "active",
    }
    ALLIANCE_MEMBERS.append(member)
    return member
