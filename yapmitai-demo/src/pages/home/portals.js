export const portals = [
  {
    key: "enterprise",
    path: "/enterprise/dashboard",
    label: "企业",
    title: "企业入口",
    en: "Enterprise",
    desc: "AI增长平台与超级员工",
    icon: "企",
    emoji: "🏢",
    scope: "经营、工具、知识库、模型配置",
    pages: [
      { path: "/enterprise/dashboard", title: "企业控制台", description: "查看经营指标、任务队列与AI贡献。" },
      { path: "/enterprise/agents", title: "超级AI员工", description: "像管理团队一样管理AI员工。" },
      { path: "/enterprise/tools", title: "AI工具中心", description: "使用Prompt Skills完成业务任务。" },
      { path: "/enterprise/knowledge/agent", title: "企业智库", description: "管理本地知识库与RAG问答。" },
      { path: "/enterprise/model-configs", title: "模型配置", description: "配置Chat和Embedding模型。" },
      { path: "/enterprise/tools/agent-config", title: "Agent总配置", description: "管理网关、模块和连接测试。" },
      { path: "/enterprise/creation/agent", title: "AI创作配置", description: "配置图片、视频和内容生成能力。" },
      { path: "/enterprise/inquiry", title: "询盘转化AI", description: "三大 Agent 处理询盘：分析、回复、跟进。" },
      { path: "/enterprise/tools/agent-logs", title: "调用日志", description: "查看接口、模型调用和异常。" }
    ]
  },
  {
    key: "talent",
    path: "/talent/home",
    label: "员工",
    title: "员工入口",
    en: "Talent",
    desc: "个人AI工作台",
    icon: "人",
    emoji: "👤",
    scope: "任务、助手、个人效率",
    pages: [{ path: "/talent/home", title: "员工工作台", description: "处理日常任务并使用个人AI助手。" }]
  },
  {
    key: "government",
    path: "/government/dashboard",
    label: "政府",
    title: "政府入口",
    en: "Government",
    desc: "产业AI决策驾驶舱",
    icon: "政",
    emoji: "🏛️",
    scope: "产业运行、政策问答、宏观指标",
    pages: [{ path: "/government/dashboard", title: "政府驾驶舱", description: "查看产业运行、企业分布和政策问答。" }]
  },
  {
    key: "alliance",
    path: "/alliance/dashboard",
    label: "联盟",
    title: "联盟入口",
    en: "Alliance",
    desc: "品牌增长计划网络",
    icon: "盟",
    emoji: "🤝",
    scope: "成员协同、增长计划、联盟看板",
    pages: [{ path: "/alliance/dashboard", title: "产业联盟", description: "管理联盟成员和品牌增长计划。" }]
  }
];
