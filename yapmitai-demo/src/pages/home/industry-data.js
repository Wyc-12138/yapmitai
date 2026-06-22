export const industries = {
  brand: {
    slug: "brand",
    cardClass: "card-brand",
    color: "var(--brand)",
    tagBg: "rgba(255,107,53,0.12)",
    tagBorder: "rgba(255,107,53,0.25)",
    tag: "品牌增长",
    en: "AI for Marketing · Brand Growth",
    title: "让每个品牌决策<br>都由数据驱动",
    subtitle: "从一句 Prompt 到跨平台发布，YAPMIT 品牌增长 AI 团队替你完成内容生产、受众洞察和效果优化的完整闭环。",
    primaryLabel: "免费体验 Demo",
    kpis: [
      { value: "73%", label: "内容生产效率<br>平均提升" },
      { value: "5×", label: "社媒发布频次<br>提升倍数" },
      { value: "38%", label: "广告 ROI<br>平均提升" },
      { value: "24h", label: "品牌舆情<br>响应时效" }
    ],
    useCases: [
      { icon: "✍️", title: "多平台内容生成", desc: "输入品牌信息与目标，AI 自动生成小红书、微博、微信、抖音、LinkedIn 的差异化内容，风格一键适配。" },
      { icon: "🎯", title: "受众洞察与分层", desc: "基于行为数据和语义分析，自动识别高价值受众群体，输出精准用户画像与触达策略。" },
      { icon: "📊", title: "广告素材智能优化", desc: "AI 对比测试多版本创意，实时分析 CTR、CVR 数据，自动推荐最优素材组合。" },
      { icon: "🔍", title: "品牌舆情监控与响应", desc: "7×24 全网品牌声量监控，发现负面舆情立即预警，并生成应对话术草案供审核。" },
      { icon: "📧", title: "个性化私域运营", desc: "基于用户行为链路，动态生成个性化推送内容，提升私域开信率与复购转化。" },
      { icon: "📈", title: "营销报告自动化", desc: "自动拉取多渠道数据，生成结构化营销周报、月报，附带 AI 解读与下一步建议。" }
    ],
    workflowTitle: "品牌增长 AI 流水线",
    steps: [
      { title: "品牌素材接入", desc: "上传品牌指南、产品信息、历史内容，AI 构建专属品牌知识库，确保所有输出风格一致。", tools: ["Skills: Brand Memory", "Tool: File Ingestion"] },
      { title: "策略 Agent 规划", desc: "策略 Agent 分析目标受众、竞品动态和当前热点，输出内容日历与话题规划。", tools: ["Agent: Strategist", "Tool: Web Search"] },
      { title: "内容 Agent 批量生产", desc: "写作 Agent 根据规划批量生成多平台差异化内容，视觉 Agent 同步输出配图提示词。", tools: ["Agent: Copywriter", "Agent: Visual Director"] },
      { title: "审核与多平台发布", desc: "内容进入人工审核队列，一键审批后自动按计划发布至各平台，完整留存发布记录。", tools: ["Workflow Studio", "Tool: Social APIs"] },
      { title: "效果追踪与自我进化", desc: "分析 Agent 持续监测内容表现，将高效内容模式反哺策略库，实现自我迭代的品牌增长系统。", tools: ["Agent: Analyst", "Skills: Performance Loop"] }
    ],
    ctaTitle: "准备好让 AI 接管品牌增长了吗？",
    ctaDesc: "加入已在使用 YAPMIT 品牌增长空间的企业，预约一次 30 分钟产品演示。",
    ctaLabel: "预约演示 →"
  },
  cross: {
    slug: "cross",
    cardClass: "card-cross",
    color: "var(--cross)",
    tagBg: "rgba(168,85,247,0.12)",
    tagBorder: "rgba(168,85,247,0.25)",
    tag: "跨境出海",
    en: "AI for Cross-border · Global Expansion",
    title: "跨越边境<br>不该有那么多摩擦",
    subtitle: "合规审查、选品决策、本地化内容、物流追踪——YAPMIT 跨境出海 AI 把最复杂的出海环节全部自动化，助力中国品牌走向全球。",
    primaryLabel: "免费合规检测",
    kpis: [
      { value: "85%", label: "合规审查时间<br>缩短" },
      { value: "50+", label: "覆盖目标市场<br>国家与地区" },
      { value: "3×", label: "选品决策效率<br>提升倍数" },
      { value: "40%", label: "本地化内容<br>成本降低" }
    ],
    useCases: [
      { icon: "📋", title: "多国合规智能审查", desc: "上传产品信息，AI 自动对照目标国海关法规、认证要求和禁限商品清单，输出合规风险报告。" },
      { icon: "🛍️", title: "跨境选品决策", desc: "分析目标市场消费趋势、竞品售价和平台算法，AI 给出高潜力选品建议和定价区间。" },
      { icon: "🌍", title: "本地化内容批量生产", desc: "产品描述、营销文案、客服话术的多语言本地化，深度适配目标市场文化语境和平台规范。" },
      { icon: "📦", title: "物流与清关智能协同", desc: "智能推荐最优物流方案，自动生成报关文件草稿，实时追踪货物状态并预警异常。" },
      { icon: "💱", title: "汇率与定价动态优化", desc: "监控实时汇率波动，结合竞品价格动态，AI 推荐最优定价策略，保护利润空间。" },
      { icon: "⭐", title: "海外评论与口碑运营", desc: "自动生成多语言回评模板，分析差评关键词并反馈产品改进建议，提升全球店铺评分。" }
    ],
    workflowTitle: "跨境出海 AI 全链路",
    steps: [
      { title: "目标市场分析", desc: "市场 Agent 扫描目标国消费数据、竞争格局和平台政策，生成市场进入评估报告。", tools: ["Agent: Market Intel", "Tool: Web Search"] },
      { title: "合规自动审查", desc: "合规 Agent 对照海关 HS Code、目标国认证数据库，自动生成合规 Checklist 和风险提示。", tools: ["Agent: Compliance", "Skills: Regulation KB"] },
      { title: "本地化内容生产", desc: "内容 Agent 将产品资料本地化，适配亚马逊、Shopee、TikTok Shop 等各平台 Listing 规范。", tools: ["Agent: Localizer", "Skills: Platform Rules"] },
      { title: "上架与自运转运营", desc: "运营 Agent 监控销售数据，自动调价、补货预警、响应客诉，形成自运转的跨境运营系统。", tools: ["Agent: Operator", "Tool: Marketplace APIs"] }
    ],
    ctaTitle: "打开下一个市场，用 AI 开路",
    ctaDesc: "已有数十家跨境卖家使用 YAPMIT 进入新市场，平均上线时间缩短 60%。",
    ctaLabel: "预约演示 →"
  },
  commerce: {
    slug: "commerce",
    cardClass: "card-commerce",
    color: "var(--commerce)",
    tagBg: "rgba(0,196,140,0.12)",
    tagBorder: "rgba(0,196,140,0.25)",
    tag: "导购文旅",
    en: "AI for Commerce · Smart Retail & Cultural Tourism",
    title: "旅行的每一刻<br>购物的每一步<br>都值得被 AI 照顾",
    subtitle: "YAPMIT 导购文旅 AI 融合智能导购与文旅服务——为消费者提供个性化推荐与全旅程陪伴，为商家与景区降本增效。",
    primaryLabel: "体验 AI 导购",
    kpis: [
      { value: "90s", label: "生成完整行程<br>平均耗时" },
      { value: "40+", label: "支持语言数量" },
      { value: "62%", label: "客服人工咨询<br>量减少" },
      { value: "35%", label: "AI 推荐带来<br>转化率提升" }
    ],
    useCases: [
      { icon: "🛒", title: "AI 智能导购助手", desc: "嵌入购物平台或商场 App，AI 基于用户偏好、预算与场景实时推荐最适合的商品，驱动转化。" },
      { icon: "🗺️", title: "个性化行程规划", desc: "根据旅行者偏好、预算和时间，AI 在 90 秒内生成完整文旅行程，支持实时调整与深度定制。" },
      { icon: "🎙️", title: "多语言 AI 导览", desc: "到达景点或商圈后，AI 即时提供深度文化解说与购物攻略，支持 40+ 语言，随时问、随时答。" },
      { icon: "🏨", title: "一站式智能预订", desc: "基于用户实时偏好和本地库存，推荐最匹配的酒店、餐厅、门票和活动，直连预订完成闭环。" },
      { icon: "📸", title: "文旅内容自动生产", desc: "为景区、OTA 和商业综合体自动生成目的地攻略、景点介绍、商品文案和用户评论回复。" },
      { icon: "🌤️", title: "实时场景播报", desc: "整合天气、客流、促销活动等实时数据，主动推送贴心提醒与个性化场景建议。" }
    ],
    workflowTitle: "导购文旅 AI 服务链路",
    steps: [
      { title: "用户偏好采集", desc: "通过对话式交互收集用户的目的地、消费偏好、预算与时间，构建实时个人画像。", tools: ["Agent: Concierge", "Skills: Preference Model"] },
      { title: "方案 Agent 规划", desc: "规划 Agent 调用景区知识库、商品库和实时数据，生成最优行程或导购推荐方案。", tools: ["Agent: Planner", "Tool: Maps API", "Skills: Destination KB"] },
      { title: "预订与消费转化", desc: "预订 Agent 一键完成门票、住宿、餐饮和商品的比价与预订，引导完成消费转化闭环。", tools: ["Agent: Booking", "Tool: Commerce APIs"] },
      { title: "全程 AI 陪伴", desc: "旅途与购物过程中，导览 Agent 随时响应问询，并主动推送基于位置的内容与优惠。", tools: ["Agent: Guide", "Skills: Real-time Context"] }
    ],
    ctaTitle: "为你的文旅与零售业务接入 AI 能力",
    ctaDesc: "景区、OTA、商业综合体、免税店——YAPMIT 导购文旅空间提供定制化 AI 解决方案。",
    ctaLabel: "预约演示 →"
  },
  invest: {
    slug: "invest",
    cardClass: "card-invest",
    color: "var(--invest)",
    tagBg: "rgba(255,184,0,0.12)",
    tagBorder: "rgba(255,184,0,0.25)",
    tag: "招商引资",
    en: "AI for Investment · Smart Investment Promotion",
    title: "政府招商的<br>AI 大脑",
    subtitle: "YAPMIT 招商引资 AI 帮助政府机构和产业园区精准匹配企业资源、自动化招商材料生产、全流程追踪项目落地进展。",
    primaryLabel: "体验招商 AI",
    primaryDarkText: true,
    kpis: [
      { value: "80%", label: "招商材料生产<br>时间缩短" },
      { value: "3×", label: "企业精准匹配<br>效率提升" },
      { value: "100%", label: "项目进度<br>可视化追踪" },
      { value: "60%", label: "招商人员重复<br>工作量减少" }
    ],
    useCases: [
      { icon: "🔍", title: "企业资源智能匹配", desc: "AI 分析园区产业定位，从企业数据库中精准筛选符合落地条件的目标企业，并生成定向触达策略。" },
      { icon: "📄", title: "招商材料自动生成", desc: "根据目标企业类型，AI 自动定制化生成招商手册、政策摘要、园区介绍等材料，一键导出多格式。" },
      { icon: "📊", title: "政策解读与对比", desc: "AI 实时解读最新优惠政策，与周边区域横向对比，帮助招商人员快速掌握差异化竞争优势。" },
      { icon: "🗓️", title: "项目全流程追踪", desc: "从企业意向到签约落地，全流程数字化追踪，自动推送节点提醒与待办事项，防止线索流失。" },
      { icon: "🤝", title: "AI 招商谈判助手", desc: "会前自动整理企业背景、行业动态和谈判要点；会后生成纪要与跟进行动清单。" },
      { icon: "🏗️", title: "产业生态图谱", desc: "AI 构建区域产业链图谱，识别缺失环节，为招商方向提供数据依据，实现精准补链强链。" }
    ],
    workflowTitle: "招商引资 AI 工作链路",
    steps: [
      { title: "园区产业定位分析", desc: "产业 Agent 分析园区现有产业结构与发展规划，识别重点招商行业方向和关键缺口。", tools: ["Agent: Industry Analyst", "Skills: Industrial KB"] },
      { title: "目标企业精准筛选", desc: "匹配 Agent 从企业数据库中按行业、规模、注册地、财务状况等多维条件筛选目标企业清单。", tools: ["Agent: Matcher", "Tool: Enterprise DB"] },
      { title: "定制招商材料生产", desc: "内容 Agent 针对不同目标企业，自动生成个性化招商 PPT、政策对照表、园区优势简报。", tools: ["Agent: Content", "Skills: Policy Library"] },
      { title: "项目追踪与闭环管理", desc: "CRM Agent 全程追踪企业从接触到落地的每个节点，自动提醒跟进、汇总进展、预警风险项目。", tools: ["Agent: CRM Manager", "Workflow Studio"] }
    ],
    ctaTitle: "让招商工作变得更智能、更高效",
    ctaDesc: "政府机构、产业园区、经济开发区——YAPMIT 招商引资空间支持定制化部署与数据安全方案。",
    ctaLabel: "预约政府专属演示 →",
    ctaDarkText: true
  }
};

export const industryCards = [
  {
    slug: "brand",
    cardClass: "card-brand",
    icon: "📣",
    title: "品牌增长",
    tag: "AI for Marketing",
    subtitle: "Brand Growth · AI-Powered Marketing",
    desc: "从内容生产到投放优化，AI 驱动全链路品牌增长，让品牌声量与转化率同步提升。",
    features: ["多平台内容自动生成与发布", "智能受众分析与广告优化", "品牌声量与舆情实时监控"]
  },
  {
    slug: "cross",
    cardClass: "card-cross",
    icon: "🌐",
    title: "跨境出海",
    tag: "AI for Cross-border",
    subtitle: "Global Expansion · AI-Powered",
    desc: "合规审查、选品决策、本地化内容、物流追踪——AI 把跨境贸易最复杂的环节全部自动化。",
    features: ["多国合规与报关智能审查", "跨境选品定价与竞品分析", "多语言本地化内容批量生产"]
  },
  {
    slug: "commerce",
    cardClass: "card-commerce",
    icon: "🗺️",
    title: "导购文旅",
    tag: "AI for Commerce",
    subtitle: "Smart Retail & Cultural Tourism · AI-Powered",
    desc: "重塑文旅消费体验，AI 导购助手与智能行程规划让每位用户享受个性化的旅行与购物体验。",
    features: ["AI 导购助手与个性化推荐", "智能行程规划与多语言导览", "文旅目的地内容自动生产"]
  },
  {
    slug: "invest",
    cardClass: "card-invest",
    icon: "🏛️",
    title: "招商引资",
    tag: "AI for Investment",
    subtitle: "Investment Promotion · AI-Powered",
    desc: "政府与园区的 AI 招商大脑——精准匹配企业资源、自动生成招商材料、实时追踪项目进展。",
    features: ["企业资源库智能匹配与推送", "招商政策与材料自动生成", "项目落地进度全流程追踪"]
  }
];

export const osStackLayers = [
  { icon: "🏢", bg: "rgba(30,111,255,0.12)", name: "Industry Space", desc: "品牌增长 · 跨境出海 · 导购文旅 · 招商引资 — 四个垂直行业入口", tag: "TOP" },
  { icon: "⚙️", bg: "rgba(0,194,255,0.12)", name: "Workflow Studio", desc: "可视化流程编排，拖拽式搭建行业场景工作流", tag: "STUDIO" },
  { icon: "🤖", bg: "rgba(168,85,247,0.12)", name: "Agent Team", desc: "多智能体协同，分角色执行复杂任务", tag: "AGENT" },
  { icon: "🧩", bg: "rgba(0,196,140,0.12)", name: "Skills", desc: "行业知识库、技能模块，可插拔式组合", tag: "SKILL" },
  { icon: "🔧", bg: "rgba(255,184,0,0.12)", name: "Tools", desc: "搜索、代码执行、API 调用、数据连接器", tag: "TOOL" },
  { icon: "🧠", bg: "rgba(255,107,53,0.12)", name: "Models + Compute Center", desc: "多模型路由，弹性算力调度，支持 GPU 资源统一管理", tag: "INFRA" }
];

export const stats = [
  { value: "4", label: "垂直行业空间" },
  { value: "6", label: "OS 技术层" },
  { value: "4", label: "登录主体类型" },
  { value: "∞", label: "可组合工作流" }
];
