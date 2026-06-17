export const stats = [
  { label: "接入企业", value: 328, unit: "家" },
  { label: "AI员工总数", value: 1240, unit: "个" },
  { label: "品牌增长计划", value: 86, unit: "个" },
  { label: "累计服务GMV", value: "12.4", unit: "亿元" }
];

export const enterpriseKpis = [
  { title: "今日询盘线索", value: "47", unit: "条", trend: "↑ 12% 较昨日", color: "#10b981" },
  { title: "新增用户", value: "238", unit: "人", trend: "↑ 8% 较本月均值", color: "#3b82f6" },
  { title: "投流ROI", value: "3.8", unit: "x", trend: "↑ 0.4 较上周", color: "#f59e0b" },
  { title: "本月AI任务完成", value: "156", unit: "/ 180", trend: "完成率 86.7%", color: "#8b5cf6" },
  { title: "本月费用消耗", value: "¥2.4", unit: "万", trend: "↑ 预算余量 38%", color: "#ef4444" }
];

export const dashboardWorkflows = [
  { id: 1, name: "品牌内容矩阵生产", detail: "图文 × 8 · 短视频脚本 × 3 · 已分发至各平台", agent: "AI品牌营销经理", progress: 100, status: "done" },
  { id: 2, name: "海外投流策略执行", detail: "Meta Ads + TikTok · 预算 ¥8,000 · 投放中", agent: "AI广告投流专员", progress: 45, status: "running" },
  { id: 3, name: "客户满意度回访", detail: "已回访 28/45 位客户 · 满意度 4.7/5", agent: "AI客服主管", progress: 62, status: "running" }
];

export const dashboardTasks = [
  { id: 1, title: "生成品牌出海内容包（英文版）", agent: "AI品牌营销经理", tag: "营销", tagClass: "marketing", progress: 65, status: "running" },
  { id: 2, title: "分析上周亚马逊广告数据", agent: "AI数据分析师", tag: "数据", tagClass: "data", progress: 100, status: "done" },
  { id: 3, title: "回复30条海外用户询盘", agent: "AI客服主管", tag: "客服", tagClass: "service", progress: 40, status: "running" },
  { id: 4, title: "竞品定价分析报告", agent: "AI跨境运营经理", tag: "运营", tagClass: "ops", progress: 0, status: "pending" },
  { id: 5, title: "社媒内容排期（TikTok×7条）", agent: "AI内容创作官", tag: "营销", tagClass: "marketing", progress: 80, status: "running" }
];

export const dashboardAgents = [
  { id: 1, name: "AI品牌营销经理", role: "Brand Marketing Manager", score: 92, status: "running", todayDone: 5, monthTotal: 42, satisfaction: 4.8 },
  { id: 2, name: "AI广告投流专员", role: "Media Buying Specialist", score: 90, status: "running", todayDone: 5, monthTotal: 38, satisfaction: 4.6 },
  { id: 3, name: "AI客服主管", role: "Customer Service Lead", score: 96, status: "running", todayDone: 28, monthTotal: 156, satisfaction: 4.9 },
  { id: 4, name: "AI数据分析师", role: "Data Analyst", score: 94, status: "running", todayDone: 3, monthTotal: 28, satisfaction: 4.7 }
];

export const dashboardCosts = [
  { name: "广告投放", amt: "¥8,200", pct: "34%", color: "#3b82f6", width: 68 },
  { name: "AI算力", amt: "¥5,600", pct: "23%", color: "#8b5cf6", width: 46 },
  { name: "API调用", amt: "¥4,100", pct: "17%", color: "#06b6d4", width: 34 },
  { name: "内容审核", amt: "¥3,500", pct: "15%", color: "#10b981", width: 29 },
  { name: "数据存储", amt: "¥2,600", pct: "11%", color: "#f59e0b", width: 22 }
];

export const dashboardTools = [
  { name: "AI多语言文案", calls: 186, barWidth: 62, icon: "文", bg: "rgba(59,130,246,0.15)" },
  { name: "AI客服回复", calls: 145, barWidth: 48, icon: "客", bg: "rgba(6,182,212,0.15)" },
  { name: "AI短视频脚本", calls: 98, barWidth: 33, icon: "影", bg: "rgba(139,92,246,0.15)" },
  { name: "AI广告优化", calls: 72, barWidth: 24, icon: "投", bg: "rgba(245,158,11,0.15)" }
];

export const dashboardResults = [
  { title: "AI内容生成", big: "186", sub: "条 · 本周产出", rc: "rgba(59,130,246,0.12)", bars: [8,12,16,18,22,28,32], trend: "+24%", trendUp: true },
  { title: "广告投放优化", big: "¥60.8K", sub: "本周GMV · ROI 3.8x", rc: "rgba(16,185,129,0.12)", bars: [12,18,22,28,24,32,38], input: "¥16K", output: "¥60.8K" },
  { title: "客户服务统计", big: "4.9", sub: "平均满意度 · 本月", rc: "rgba(139,92,246,0.12)", bars: [28,32,30,38,40,44,48], trend: "+0.2", trendUp: true }
];

export const salesTrend = [
  { month: "1月", sales: 120, ai: 45 },
  { month: "2月", sales: 145, ai: 68 },
  { month: "3月", sales: 178, ai: 95 },
  { month: "4月", sales: 210, ai: 130 },
  { month: "5月", sales: 195, ai: 142 },
  { month: "6月", sales: 248, ai: 178 }
];

export const moduleDistribution = [
  { label: "内容生成", value: 32, color: "#4361EE" },
  { label: "客户管理", value: 24, color: "#00C9A7" },
  { label: "营销投放", value: 19, color: "#F72585" },
  { label: "数据分析", value: 15, color: "#FF9F1C" },
  { label: "知识库", value: 10, color: "#7B2FBE" }
];

export const trend7d = [
  { day: "周一", calls: 720, success: 690 },
  { day: "周二", calls: 810, success: 786 },
  { day: "周三", calls: 900, success: 875 },
  { day: "周四", calls: 1040, success: 1010 },
  { day: "周五", calls: 1180, success: 1155 },
  { day: "周六", calls: 1210, success: 1184 },
  { day: "周日", calls: 1248, success: 1230 }
];

export const tasks = [
  { id: 1, task: "生成品牌出海内容包（英文版）", agent: "AI品牌营销经理", status: "进行中", progress: 65 },
  { id: 2, task: "分析上周亚马逊广告数据", agent: "AI数据分析师", status: "已完成", progress: 100 },
  { id: 3, task: "回复30条海外用户询盘", agent: "AI客服主管", status: "进行中", progress: 40 },
  { id: 4, task: "竞品定价分析报告", agent: "AI跨境运营经理", status: "待处理", progress: 0 },
  { id: 5, task: "社媒内容排期（TikTok×7条）", agent: "AI内容创作官", status: "进行中", progress: 80 }
];

export const agents = [
  {
    id: 1,
    name: "AI品牌营销经理",
    nameEn: "AI Brand Marketing Manager",
    status: "working",
    category: "营销类",
    todayTasks: 5,
    completedTasks: 5,
    monthKPI: 92,
    description: "负责品牌内容生产、海外投放策略、社媒运营与增长方案。",
    todayLog: [
      { time: "09:15", action: "生成品牌英文介绍视频脚本" },
      { time: "10:30", action: "分析竞品社媒数据，产出报告" },
      { time: "13:00", action: "排期本周TikTok内容矩阵" },
      { time: "15:20", action: "优化亚马逊A+页面文案" },
      { time: "16:40", action: "正在生成品牌出海内容包（英文版）" }
    ]
  },
  {
    id: 2,
    name: "AI跨境运营经理",
    nameEn: "AI Cross-border Operations Manager",
    status: "working",
    category: "运营类",
    todayTasks: 4,
    completedTasks: 3,
    monthKPI: 88,
    description: "负责亚马逊、独立站店铺运营、选品分析和库存管理建议。",
    todayLog: [
      { time: "09:00", action: "整理Shopee热销品类" },
      { time: "11:20", action: "输出库存周转预警" },
      { time: "14:15", action: "分析独立站转化漏斗" }
    ]
  },
  {
    id: 3,
    name: "AI客服主管",
    nameEn: "AI Customer Service Lead",
    status: "standby",
    category: "客服类",
    todayTasks: 35,
    completedTasks: 28,
    monthKPI: 96,
    description: "负责多语言客户询盘回复、投诉处理、满意度提升和人工接管建议。",
    todayLog: [
      { time: "08:30", action: "回复英语询盘18条" },
      { time: "10:45", action: "升级2条售后工单" },
      { time: "15:00", action: "生成客服SOP优化建议" }
    ]
  },
  {
    id: 4,
    name: "AI数据分析师",
    nameEn: "AI Data Analyst",
    status: "working",
    category: "数据类",
    todayTasks: 3,
    completedTasks: 3,
    monthKPI: 94,
    description: "负责销售数据分析、市场趋势报告和ROI优化建议。",
    todayLog: [
      { time: "09:40", action: "同步广告与GMV数据" },
      { time: "12:10", action: "生成ROI分析报告" },
      { time: "16:00", action: "刷新经营驾驶舱指标" }
    ]
  },
  {
    id: 5,
    name: "AI广告投流专员",
    nameEn: "AI Media Buying Specialist",
    status: "working",
    category: "营销类",
    todayTasks: 6,
    completedTasks: 5,
    monthKPI: 90,
    description: "负责Google、Meta、亚马逊广告投放，预算分配和效果优化。",
    todayLog: [
      { time: "09:10", action: "完成Meta素材评分" },
      { time: "11:35", action: "调整TikTok预算分配" },
      { time: "15:50", action: "生成A/B测试方案" }
    ]
  },
  {
    id: 6,
    name: "AI财税助理",
    nameEn: "AI Finance & Tax Assistant",
    status: "standby",
    category: "管理类",
    todayTasks: 2,
    completedTasks: 2,
    monthKPI: 85,
    description: "负责财务报表分析、海南自贸港税筹建议和合规提醒。",
    todayLog: [
      { time: "10:00", action: "完成税收优惠匹配" },
      { time: "14:00", action: "生成本月费用摘要" }
    ]
  }
];

export const tools = [
  { id: 1, name: "AI多语言文案", nameEn: "AI Copywriting", icon: "文", category: "内容生成", desc: "一键生成中英日韩多语言品牌文案。", external: true },
  { id: 2, name: "AI短视频脚本", nameEn: "AI Video Script", icon: "影", category: "内容生成", desc: "TikTok、Reels、小红书脚本自动生成。", external: true },
  { id: 3, name: "AI销售数据分析", nameEn: "AI Sales Analytics", icon: "数", category: "数据分析", desc: "亚马逊、独立站销售数据一键分析。", external: false },
  { id: 4, name: "AI广告优化", nameEn: "AI Ad Optimizer", icon: "投", category: "营销投放", desc: "广告素材评分与投放建议自动生成。", external: true },
  { id: 5, name: "AI客服回复", nameEn: "AI Customer Reply", icon: "客", category: "客户管理", desc: "多语言询盘自动回复，响应时间小于30秒。", external: true },
  { id: 6, name: "AI竞品分析", nameEn: "AI Competitor Intel", icon: "竞", category: "数据分析", desc: "实时追踪竞品定价、评价和策略变化。", external: false },
  { id: 7, name: "AI选品助手", nameEn: "AI Product Selector", icon: "选", category: "运营工具", desc: "基于市场数据智能推荐选品方向。", external: true },
  { id: 8, name: "AI合同审查", nameEn: "AI Contract Review", icon: "审", category: "合规工具", desc: "跨境合同风险识别与条款建议。", external: false },
  { id: 9, name: "AI品牌报告", nameEn: "AI Brand Report", icon: "报", category: "数据分析", desc: "每周自动生成品牌增长分析报告。", external: true }
];

export const govKpis = [
  { title: "接入企业总数", value: "328", unit: "家", trend: "+26", color: "#00C9A7" },
  { title: "今日GMV", value: "1,240", unit: "万", trend: "+18%", color: "#4361EE" },
  { title: "新增就业人数", value: "156", unit: "人", trend: "+32", color: "#FF9F1C" },
  { title: "税收贡献", value: "86", unit: "万", trend: "+9%", color: "#F72585" },
  { title: "品牌出海数量", value: "64", unit: "个", trend: "+8", color: "#7B2FBE" },
  { title: "AI员工总数", value: "1,240", unit: "个", trend: "+120", color: "#00C9A7" }
];

export const alliancePlans = [
  { name: "海南臻选100品牌AI增长计划", status: "进行中", current: 86, target: 100 },
  { name: "中华老字号国际化AI计划", status: "筹备中", current: 12, target: 50 },
  { name: "跨境电商出海联盟2026", status: "进行中", current: 45, target: 200 }
];

export const allianceMembers = [
  { name: "海口椰源食品", type: "消费品牌", level: "L4", status: "活跃" },
  { name: "三亚跨境优选", type: "跨境电商", level: "L5", status: "活跃" },
  { name: "琼海智造工厂", type: "制造业", level: "L3", status: "活跃" },
  { name: "陵水文旅集团", type: "服务业", level: "L4", status: "活跃" }
];

export const callLogs = [
  { id: 1, time: "16:28:12", agent: "文生图Agent", module: "AI创作", status: "成功", latency: 1180, cost: "0.42" },
  { id: 2, time: "16:22:46", agent: "智能获客Agent", module: "AI拓客", status: "成功", latency: 920, cost: "0.18" },
  { id: 3, time: "16:18:31", agent: "企微客服Agent", module: "企微客服", status: "超时", latency: 30000, cost: "0.00" },
  { id: 4, time: "16:10:09", agent: "RAG知识库Agent", module: "企业智库", status: "成功", latency: 680, cost: "0.06" },
  { id: 5, time: "15:59:44", agent: "AI外呼Agent", module: "AI拓客", status: "失败", latency: 420, cost: "0.00" }
];
