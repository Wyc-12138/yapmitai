export default {
  path: "/",
  layout: "full",
  render() {
    const portals = [
      {
        path: "/enterprise/dashboard",
        label: "企业",
        title: "企业入口",
        en: "Enterprise",
        desc: "AI增长平台与超级员工",
        icon: "企",
        scope: "经营、工具、知识库、模型配置",
        pages: [
          ["/enterprise/dashboard", "企业控制台", "查看经营指标、任务队列与AI贡献。"],
          ["/enterprise/agents", "超级AI员工", "像管理团队一样管理AI员工。"],
          ["/enterprise/tools", "AI工具中心", "使用Prompt Skills完成业务任务。"],
          ["/enterprise/knowledge/agent", "企业智库", "管理本地知识库与RAG问答。"],
          ["/enterprise/model-configs", "模型配置", "配置Chat和Embedding模型。"],
          ["/enterprise/tools/agent-config", "Agent总配置", "管理网关、模块和连接测试。"],
          ["/enterprise/creation/agent", "AI创作配置", "配置图片、视频和内容生成能力。"],
          ["/enterprise/tools/agent-logs", "调用日志", "查看接口、模型调用和异常。"]
        ]
      },
      {
        path: "/talent/home",
        label: "员工",
        title: "员工入口",
        en: "Talent",
        desc: "个人AI工作台",
        icon: "人",
        scope: "任务、助手、个人效率",
        pages: [["/talent/home", "员工工作台", "处理日常任务并使用个人AI助手。"]]
      },
      {
        path: "/government/dashboard",
        label: "政府",
        title: "政府入口",
        en: "Government",
        desc: "产业AI决策驾驶舱",
        icon: "政",
        scope: "产业运行、政策问答、宏观指标",
        pages: [["/government/dashboard", "政府驾驶舱", "查看产业运行、企业分布和政策问答。"]]
      },
      {
        path: "/alliance/dashboard",
        label: "联盟",
        title: "联盟入口",
        en: "Alliance",
        desc: "品牌增长计划网络",
        icon: "盟",
        scope: "成员协同、增长计划、联盟看板",
        pages: [["/alliance/dashboard", "产业联盟", "管理联盟成员和品牌增长计划。"]]
      }
    ];
    return `
      <div class="landing-page">
        <header class="landing-nav">
          <button class="brand light-brand" data-go="/">
            <span class="yapmitai-wordmark">YAPMITAI</span>
          </button>
          <nav class="landing-menu">
            ${portals.map((portal) => `
              <div class="landing-menu-item">
                <button data-go="${portal.path}">${portal.label}</button>
                <div class="landing-mega">
                  ${portal.pages.map(([path, title, desc], pageIndex) => `
                    <button class="${pageIndex === 0 ? "featured" : ""}" data-go="${path}">
                      <strong>${title}</strong>
                      <span>${desc}</span>
                    </button>`).join("")}
                </div>
              </div>`).join("")}
          </nav>
          <button class="landing-login" data-go="/enterprise/dashboard">进入系统</button>
        </header>
        <section class="landing-hero">
          <div class="landing-copy">
            <span class="landing-kicker">YAPMITAI Demo v2.0</span>
            <h1>悦普AI产业超级操作系统</h1>
            <p>四个入口，四套边界。企业管理 AI 员工与工具，员工完成日常任务，政府查看产业态势，联盟推进品牌增长。</p>
            <div class="landing-actions">
              <button class="primary-btn" data-go="/enterprise/dashboard">开始使用</button>
              <button class="ghost-btn" data-go="/enterprise/tools">查看AI工具</button>
            </div>
          </div>
          <div class="landing-visual" aria-hidden="true">
            <div class="visual-window">
              <div class="visual-question">What should the team focus on this week?</div>
              <div class="visual-content">
                <section>
                  <span>Summary</span>
                  <strong>AI contribution is rising across tools and knowledge workflows.</strong>
                  <div class="visual-chart"><i></i><i></i><i></i><i></i><i></i></div>
                </section>
                <section>
                  <span>Recommendations</span>
                  <p>Prioritize customer reply automation.</p>
                  <p>Connect local knowledge bases.</p>
                  <p>Review model costs weekly.</p>
                </section>
              </div>
              <div class="visual-input">Ask a follow-up question <b>Ask</b></div>
            </div>
          </div>
        </section>
        <section class="portal-grid">
          ${portals.map((portal, index) => `
            <button class="portal-card" data-go="${portal.path}" style="animation-delay:${index * 70}ms">
              <span>${portal.icon}</span>
              <strong>${portal.title}</strong>
              <small>${portal.en}</small>
              <p>${portal.desc}</p>
              <em>${portal.scope}</em>
            </button>`).join("")}
        </section>
      </div>`;
  }
};
