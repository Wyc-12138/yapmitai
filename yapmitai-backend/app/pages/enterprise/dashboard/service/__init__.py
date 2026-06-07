from app.shared.mock_data import ENTERPRISE_KPIS, SALES_TREND, TASKS


async def get_overview(_db) -> dict:
    return {
        "kpis": ENTERPRISE_KPIS,
        "salesTrend": SALES_TREND,
        "taskDistribution": [
            {"label": "内容生成", "value": 32},
            {"label": "客户管理", "value": 24},
            {"label": "营销投放", "value": 19},
            {"label": "数据分析", "value": 15},
            {"label": "知识库", "value": 10},
        ],
        "tasks": TASKS,
        "gatewayStats": {
            "calls": 1248,
            "successRate": 98.6,
            "averageLatencyMs": 1280,
            "monthlyCost": 8420,
        },
    }
