from app.services.mock_data import GOVERNMENT_KPIS


def get_dashboard() -> dict:
    return {
        "kpis": GOVERNMENT_KPIS,
        "activityTrend": [72, 78, 81, 85, 89, 92, 96],
        "enterpriseDistribution": {
            "跨境电商": 36,
            "制造": 24,
            "服务": 22,
            "贸易": 18,
        },
    }


def answer_policy(question: str) -> dict:
    return {
        "question": question,
        "answer": "根据当前Demo知识库，符合条件的鼓励类产业企业可申请海南自贸港相关优惠政策。",
        "sources": ["海南自贸港政策知识库"],
    }
