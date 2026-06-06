ENTERPRISE_KPIS = [
    {"title": "AI贡献指数", "value": 89, "unit": "分", "trend": "+5"},
    {"title": "本月GMV", "value": 248, "unit": "万元", "trend": "+18%"},
    {"title": "新增客户", "value": 127, "unit": "位", "trend": "+23%"},
    {"title": "任务完成率", "value": 94, "unit": "%", "trend": "+2%"},
]

SALES_TREND = [
    {"month": "1月", "sales": 120, "ai": 45},
    {"month": "2月", "sales": 145, "ai": 68},
    {"month": "3月", "sales": 178, "ai": 95},
    {"month": "4月", "sales": 210, "ai": 130},
    {"month": "5月", "sales": 195, "ai": 142},
    {"month": "6月", "sales": 248, "ai": 178},
]

TASKS = [
    {"id": 1, "task": "生成品牌出海内容包（英文版）", "agent": "AI品牌营销经理", "status": "running", "progress": 65},
    {"id": 2, "task": "分析上周亚马逊广告数据", "agent": "AI数据分析师", "status": "completed", "progress": 100},
    {"id": 3, "task": "回复30条海外用户询盘", "agent": "AI客服主管", "status": "running", "progress": 40},
]

AGENTS = [
    {"id": 1, "name": "AI品牌营销经理", "nameEn": "AI Brand Marketing Manager", "status": "working", "category": "营销类", "todayDone": 5, "monthKPI": 92, "enabled": True},
    {"id": 2, "name": "AI跨境运营经理", "nameEn": "AI Cross-border Operations Manager", "status": "working", "category": "运营类", "todayDone": 3, "monthKPI": 88, "enabled": True},
    {"id": 3, "name": "AI客服主管", "nameEn": "AI Customer Service Lead", "status": "standby", "category": "客服类", "todayDone": 28, "monthKPI": 96, "enabled": True},
    {"id": 4, "name": "AI数据分析师", "nameEn": "AI Data Analyst", "status": "working", "category": "数据类", "todayDone": 4, "monthKPI": 94, "enabled": True},
    {"id": 5, "name": "AI广告投流专员", "nameEn": "AI Media Buying Specialist", "status": "working", "category": "营销类", "todayDone": 6, "monthKPI": 90, "enabled": True},
    {"id": 6, "name": "AI财税助理", "nameEn": "AI Finance & Tax Assistant", "status": "standby", "category": "管理类", "todayDone": 2, "monthKPI": 85, "enabled": True},
]

TOOLS = [
    {"id": 1, "name": "AI多语言文案", "category": "内容生成", "external": True, "enabled": True},
    {"id": 2, "name": "AI短视频脚本", "category": "内容生成", "external": True, "enabled": True},
    {"id": 3, "name": "AI销售数据分析", "category": "数据分析", "external": False, "enabled": True},
    {"id": 4, "name": "AI广告优化", "category": "营销投放", "external": True, "enabled": True},
]

GOVERNMENT_KPIS = [
    {"title": "接入企业总数", "value": 328, "unit": "家"},
    {"title": "今日GMV", "value": 1240, "unit": "万"},
    {"title": "新增就业人数", "value": 156, "unit": "人"},
    {"title": "税收贡献", "value": 86, "unit": "万"},
    {"title": "品牌出海数量", "value": 64, "unit": "个"},
    {"title": "AI员工总数", "value": 1240, "unit": "个"},
]

ALLIANCE_PLANS = [
    {"name": "海南臻选100品牌AI增长计划", "status": "running", "current": 86, "target": 100},
    {"name": "中华老字号国际化AI计划", "status": "preparing", "current": 12, "target": 50},
]

ALLIANCE_MEMBERS = [
    {"name": "海口椰源食品", "type": "消费品牌", "level": "L4", "status": "active"},
    {"name": "三亚跨境优选", "type": "跨境电商", "level": "L5", "status": "active"},
]
