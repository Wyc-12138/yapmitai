import {
  agents,
  allianceMembers,
  alliancePlans,
  callLogs,
  enterpriseKpis,
  govKpis,
  moduleDistribution,
  salesTrend,
  stats,
  tasks,
  tools,
  trend7d
} from "./data/mock.js";
import { findRoute } from "./routes/index.js";

const app = document.getElementById("root");
let agentFilter = "全部";
let toolFilter = "全部";
let logFilter = "全部";
let selectedAgent = null;
let modalOpen = false;
let submitted = false;
let showKey = false;
let globalEnabled = readStore("agent-global-enabled", true);
let agentPackages = [
  { id: "creation-image", name: "文生图 Agent", type: "AI创作", version: "1.2.0", enabled: true },
  { id: "creation-video", name: "文生视频 Agent", type: "AI创作", version: "1.0.8", enabled: true },
  { id: "outreach-leads", name: "智能获客 Agent", type: "拓客", version: "2.1.1", enabled: true },
  { id: "cs-personalwx", name: "个微客服 Agent", type: "客服", version: "1.4.3", enabled: false },
  { id: "cs-corpwx", name: "企微客服 Agent", type: "客服", version: "1.5.0", enabled: true },
  { id: "knowledge-rag", name: "RAG知识库 Agent", type: "知识库", version: "0.9.7", enabled: true }
];

const navItems = [
  ["/enterprise/dashboard", "企业控制台", "Dashboard"],
  ["/enterprise/agents", "超级AI员工", "Agents"],
  ["/enterprise/tools", "AI工具中心", "Tools"],
  ["/enterprise/tools/agent-config", "Agent总配置", "Gateway"],
  ["/enterprise/creation/agent", "AI创作配置", "Creation"],
  ["/enterprise/outreach/agent", "AI拓客配置", "Outreach"],
  ["/enterprise/personalwx/agent", "个微Agent", "Personal WX"],
  ["/enterprise/corpwx/agent", "企微Agent", "Corp WX"],
  ["/enterprise/knowledge/agent", "企业智库", "Knowledge"],
  ["/enterprise/tools/agent-logs", "调用日志", "Logs"],
  ["/talent/home", "员工工作台", "Talent"],
  ["/government/dashboard", "政府驾驶舱", "Government"],
  ["/alliance/dashboard", "产业联盟", "Alliance"]
];

function render() {
  const path = window.location.pathname;
  selectedAgent = path === "/enterprise/agents" ? selectedAgent : null;
  modalOpen = path === "/enterprise/agents" ? modalOpen : false;

  const route = findRoute(path);
  const renderers = {
    loginPage,
    enterpriseDashboard,
    agentsCenter,
    toolsCenter,
    agentGlobalConfig,
    agentLogs,
    creationAgent: () => moduleConfig("creation"),
    outreachAgent: () => moduleConfig("outreach"),
    personalwxAgent: () => moduleConfig("personalwx"),
    corpwxAgent: () => moduleConfig("corpwx"),
    knowledgeConfig,
    talentHome,
    governmentDashboard,
    allianceDashboard
  };
  const pageRenderer = route ? renderers[route.renderer] : notFound;
  const content = pageRenderer();

  app.innerHTML = route?.layout === "full" ? content : shell(path, content);
}

function loginPage() {
  const entrances = [
    ["/talent/home", "员工入口", "Talent", "160万职工AI工作台", "人"],
    ["/enterprise/dashboard", "企业入口", "Enterprise", "AI增长平台与超级员工", "企"],
    ["/government/dashboard", "政府入口", "Government", "产业AI决策驾驶舱", "政"],
    ["/alliance/dashboard", "联盟入口", "Alliance", "品牌增长计划网络", "盟"]
  ];
  return `
    <div class="login-page">
      <div class="mesh-bg"></div>
      <header class="login-header">
        ${brand("on-hero")}
        <span class="pill">Public Demo Online</span>
      </header>
      <section class="login-hero">
        <div class="hero-copy">
          <span class="eyebrow">Demo v2.0 · AI产业基础设施</span>
          <h1>面向员工、企业、政府与产业联盟的 AI 产业超级操作系统</h1>
          <p>企业像管理团队一样雇佣AI员工，政府看到产业运行数据，联盟推动品牌增长计划。</p>
        </div>
        <div class="entrance-grid">
          ${entrances.map(([path, label, en, desc, icon], index) => `
            <button class="entrance-card" data-go="${path}" style="animation-delay:${index * 90}ms">
              <span class="tool-icon">${icon}</span>
              <strong>${label}</strong>
              <small>${en}</small>
              <span>${desc}</span>
              <span class="corner-icon">›</span>
            </button>`).join("")}
        </div>
      </section>
      <section class="stats-strip">${stats.map(metric).join("")}</section>
    </div>`;
}

function shell(path, content) {
  return `
    <div class="app-shell">
      <aside class="side-nav">
        ${brand("")}
        <nav>
          ${navItems.map(([href, label, en]) => `
            <button class="nav-item ${path === href ? "active" : ""}" data-go="${href}">
              <span class="nav-dot"></span>
              <span>${label}<small>${en}</small></span>
            </button>`).join("")}
        </nav>
      </aside>
      <main class="main-area">
        <header class="top-bar">
          <div><strong>YAPMITAI Demo v2.0</strong><span>Agent Gateway Ready · Mock Fallback Enabled</span></div>
          <div class="top-actions">
            <button class="ghost-btn" data-go="/enterprise/tools/agent-logs">调用日志</button>
            <button class="primary-btn" data-go="/enterprise/tools/agent-config">Agent配置</button>
          </div>
        </header>
        <div class="page-content">${content}</div>
      </main>
    </div>`;
}

function brand(extra) {
  return `
    <button class="brand ${extra}" data-go="/">
      <span class="brand-mark">Y</span>
      <span><strong>悦普AI产业超级操作系统</strong><small>YAPMITAI Industrial AI OS</small></span>
    </button>`;
}

function page(title, en, desc, body) {
  return `
    <section>
      <div class="page-title"><span class="eyebrow">${en}</span><h1>${title}</h1><p>${desc}</p></div>
      ${body}
    </section>`;
}

function enterpriseDashboard() {
  return page("企业AI控制台", "Enterprise AI Dashboard", "欢迎回来，李总。今日AI团队已完成 12 项任务。", `
    <div class="kpi-grid">${enterpriseKpis.map(kpi).join("")}</div>
    <div class="dashboard-grid">
      ${panel("销售趋势", "Sales vs AI Contribution", lineChart(salesTrend, "sales", "ai", "总销售额", "AI贡献"))}
      ${panel("AI员工任务分布", "Agent Workload", donutChart(moduleDistribution))}
    </div>
    <div class="dashboard-grid wide-left">
      ${panel("今日任务队列", "Today's Task Queue", taskList())}
      ${panel("第三方Agent调用统计", "Gateway Stats", `
        <div class="mini-stat-grid">
          ${miniStat("今日调用", "1,248")}${miniStat("成功率", "98.6%")}${miniStat("平均响应", "1.28s")}${miniStat("本月费用", "¥8,420")}
        </div>
        ${lineChart(trend7d, "calls", "success", "调用量", "成功数", true)}
        <button class="primary-btn full" data-go="/enterprise/tools/agent-logs">查看调用日志</button>`)}
    </div>`);
}

function agentsCenter() {
  const categories = ["全部", "营销类", "运营类", "客服类", "数据类", "管理类"];
  const visible = agentFilter === "全部" ? agents : agents.filter((item) => item.category === agentFilter);
  return page("超级AI员工中心", "Super AI Agent Center", "像管理团队一样管理AI。", `
    <div class="page-toolbar">
      <div class="tabs">${categories.map((item) => `<button class="${agentFilter === item ? "active" : ""}" data-agent-filter="${item}">${item}</button>`).join("")}</div>
      <button class="primary-btn">新增AI员工</button>
    </div>
    <div class="agent-grid">
      ${visible.map(agentCard).join("")}
      <button class="agent-card add-card">+ 添加新AI员工</button>
    </div>
    ${selectedAgent ? drawer(selectedAgent) : ""}
    ${modalOpen ? taskModal() : ""}`);
}

function toolsCenter() {
  const categories = ["全部", "内容生成", "数据分析", "营销投放", "客户管理", "运营工具", "合规工具"];
  const visible = toolFilter === "全部" ? tools : tools.filter((item) => item.category === toolFilter);
  return page("AI工具中心", "AI Skills Center", "一个账号，使用全部AI能力。", `
    <div class="tabs">${categories.map((item) => `<button class="${toolFilter === item ? "active" : ""}" data-tool-filter="${item}">${item}</button>`).join("")}</div>
    <div class="tool-grid">${visible.map(toolCard).join("")}</div>`);
}

function agentGlobalConfig() {
  return page("Agent网关全局配置", "Agent Gateway Config", "统一管理外部Agent包、全局开关与连接测试。", `
    <div class="settings-grid">
      ${panel("连接配置", "Connection", `
        <label class="field-label">API Key</label>
        <div class="input-row"><span>密</span><input value="${showKey ? "yap_sk_live_demo_2026" : "••••••••••••••••••••"}" readonly><button class="icon-btn" data-action="toggle-key">${showKey ? "隐" : "显"}</button></div>
        <label class="field-label">网关地址</label>
        <div class="input-row"><span>网</span><input value="https://gateway.yapmitai.com/api/v1" readonly></div>
        <label class="field-label">超时设置</label>
        <div class="input-row"><span>时</span><input value="30s" readonly></div>
        <div class="switch-row"><div><strong>全局 Agent 总开关</strong><small>${globalEnabled ? "外部Agent优先，异常自动fallback" : "全部接口直接使用Mock fallback"}</small></div>${toggle(globalEnabled, "global")}</div>
        <button class="primary-btn full" data-action="test-connection">连接测试</button>
        <div id="connection-result"></div>`)}
      ${panel("可用Agent包列表", "Available Agent Packages", `
        <div class="agent-package-list">
          ${agentPackages.map((item) => `
            <div class="agent-package">
              <div><strong>${item.name}</strong><span>${item.type} · v${item.version}</span></div>
              ${statusBadge(item.enabled ? "working" : "offline")}
              ${toggle(item.enabled, `pkg:${item.id}`)}
            </div>`).join("")}
        </div>`)}
    </div>`);
}

function moduleConfig(type) {
  const map = {
    creation: ["AI创作模块配置", "Creation Agent Config", ["文生图风格：商业摄影 / 3D渲染 / 国潮插画", "文生视频：15s / 30s / 60s", "多模态输入：图+文 / 文+表", "水印开关：开启"]],
    outreach: ["AI拓客模块配置", "Outreach Agent Config", ["目标行业：跨境电商 / 消费品牌 / 制造业", "地区：海南 / 东南亚 / 北美", "外呼频率上限：80通/日", "合规声明：已勾选"]],
    personalwx: ["AI个微Agent配置", "Personal WeChat Agent", ["接管模式：AI建议+人工确认", "关键词问答：合并检索", "SOP群发：限频开启", "客户标签：自动识别"]],
    corpwx: ["AI企微Agent配置", "Enterprise WeChat Agent", ["部门归属：海外销售部", "接管模式：全托管", "关键词问答：外部知识库优先", "工单升级：开启"]]
  };
  const [title, en, fields] = map[type];
  const source = readStore(`${type}-agent-source`, "外部Agent");
  return page(title, en, "模块级独立启停，支持外部Agent、原生模块和关闭三种模式。", `
    ${panel("Agent来源", "Source", `<div class="segmented">${["外部Agent", "原生模块", "关闭"].map((item) => `<button class="${source === item ? "active" : ""}" data-source="${type}:${item}">${item}</button>`).join("")}</div>`)}
    <div class="config-list">${fields.map((field) => `<article class="config-row"><span>设</span><span>${field}</span>${toggle(source !== "关闭", "noop")}</article>`).join("")}</div>`);
}

function knowledgeConfig() {
  return page("企业智库Agent配置", "Enterprise Knowledge Agent", "外部向量库与系统关键词库合并检索。", `
    <div class="settings-grid">
      ${panel("知识库来源", "Knowledge Sources", `<div class="config-list flat">${["外部Agent向量库", "系统原有关键词库", "品牌知识库", "跨境案例库"].map((item) => `<div class="config-row"><span>库</span><span>${item}</span>${toggle(true, "noop")}</div>`).join("")}</div>`)}
      ${panel("同步状态", "Sync Status", `${miniStat("知识条数", "1,284")}${miniStat("上次同步", "2分钟前")}${progress("同步进度", 100)}<button class="primary-btn full" data-action="sync-knowledge">立即同步</button><div id="sync-result"></div>`)}
    </div>`);
}

function agentLogs() {
  const statuses = ["全部", "成功", "失败", "超时"];
  const visible = logFilter === "全部" ? callLogs : callLogs.filter((item) => item.status === logFilter);
  return page("Agent调用日志", "Agent Call Logs", "记录每次Agent调用的模块、状态、耗时与费用。", `
    <div class="page-toolbar"><div class="tabs">${statuses.map((item) => `<button class="${logFilter === item ? "active" : ""}" data-log-filter="${item}">${item}</button>`).join("")}</div><button class="ghost-btn">导出</button></div>
    <div class="table-wrap"><table><thead><tr><th>时间</th><th>Agent名称</th><th>调用模块</th><th>状态</th><th>耗时</th><th>费用</th></tr></thead><tbody>
      ${visible.map((log) => `<tr><td>${log.time}</td><td>${log.agent}</td><td>${log.module}</td><td><span class="log-status ${log.status}">${log.status}</span></td><td>${log.latency}ms</td><td>¥${log.cost}</td></tr>`).join("")}
    </tbody></table></div>`);
}

function governmentDashboard() {
  return `
    <div class="gov-screen">
      <header class="gov-header">
        <button class="ghost-btn" data-go="/">返回首页</button>
        <div><h1>海南自贸港 · 产业AI驾驶舱</h1><span>Hainan FTP · Industrial AI Decision Dashboard</span></div>
        <time>${new Date().toLocaleString("zh-CN", { hour12: false })}</time>
      </header>
      <div class="gov-kpi-grid">${govKpis.map(kpi).join("")}</div>
      <div class="gov-grid">
        ${panel("产业活跃度", "30-Day Activity", lineChart(trend7d, "calls", "success", "产业活跃", "AI贡献"))}
        ${panel("企业类型分布", "Enterprise Distribution", donutChart(moduleDistribution))}
        ${panel("AI政策问答助手", "Policy Assistant", `<div class="assistant-box"><span class="tool-icon">策</span><strong>永不落幕消博会政策助手</strong><p>可查询自贸港税收政策、品牌出海补贴、企业入驻流程。</p><button class="primary-btn full">打开助手</button></div>`)}
      </div>
    </div>`;
}

function allianceDashboard() {
  return page("产业联盟管理中心", "Alliance Management Center", "展示联盟成员网络与100家品牌AI增长计划。", `
    <div class="kpi-grid three">${kpi({ title: "成员企业数", value: "128", unit: "家", trend: "+16", color: "#00C9A7" })}${kpi({ title: "活跃企业", value: "96", unit: "家", trend: "+12%", color: "#4361EE" })}${kpi({ title: "总GMV", value: "12.4", unit: "亿元", trend: "+18%", color: "#F72585" })}</div>
    <div class="dashboard-grid">
      ${panel("AI增长计划", "Growth Programs", `<div class="plan-list">${alliancePlans.map((plan) => `<article class="plan-card"><div><strong>${plan.name}</strong><span>${plan.status}</span></div>${progress(`${plan.current}/${plan.target}家`, Math.round(plan.current / plan.target * 100))}</article>`).join("")}</div>`)}
      ${panel("联盟成员列表", "Members", `<div class="member-list">${allianceMembers.map((member) => `<div class="member-row"><span>企</span><div><strong>${member.name}</strong><span>${member.type} · ${member.level}</span></div><span class="log-status 成功">${member.status}</span></div>`).join("")}</div>`)}
    </div>`);
}

function talentHome() {
  return page("员工工作台", "Talent Workspace", "面向职工的AI协作入口。", `
    <div class="dashboard-grid">
      ${panel("今日AI助手", "Assistants", `<div class="config-list flat">${["简历优化助手", "技能学习助手", "任务总结助手", "政策咨询助手"].map((item) => `<div class="config-row"><span>AI</span><span>${item}</span><button class="tiny-btn">打开</button></div>`).join("")}</div>`)}
      ${panel("成长指数", "Growth Index", `${miniStat("本周完成任务", "18")}${miniStat("AI节省时间", "7.5h")}`)}
    </div>`);
}

function notFound() {
  return page("页面未找到", "Not Found", "当前路由还没有对应页面。", `<button class="primary-btn" data-go="/">返回首页</button>`);
}

function panel(title, en, body) {
  return `<section class="panel"><div class="panel-head"><div><h2>${title}</h2><span>${en}</span></div></div>${body}</section>`;
}

function kpi(item) {
  return `<article class="kpi-card" style="--accent:${item.color}"><span>${item.title}</span><strong>${item.value}<small>${item.unit}</small></strong><em>${item.trend}</em></article>`;
}

function metric(item) {
  return `<article class="metric"><strong>${item.value}<small>${item.unit}</small></strong><span>${item.label}</span></article>`;
}

function miniStat(label, value) {
  return `<div class="mini-stat"><span>${label}</span><strong>${value}</strong></div>`;
}

function taskList() {
  return `<div class="task-list">${tasks.map((task) => `<article class="task-row"><div><strong>${task.task}</strong><span>${task.agent}</span></div><span class="task-status ${task.status}">${task.status}</span>${progress("", task.progress, true)}</article>`).join("")}</div>`;
}

function lineChart(data, aKey, bKey, aLabel, bLabel, compact = false) {
  const max = Math.max(...data.flatMap((item) => [item[aKey], item[bKey]]));
  const points = (key) => data.map((item, index) => `${index * (100 / (data.length - 1))},${100 - item[key] / max * 86}`).join(" ");
  return `<div class="chart-box ${compact ? "compact" : ""}"><svg viewBox="0 0 100 100" preserveAspectRatio="none"><line x1="0" x2="100" y1="20" y2="20"></line><line x1="0" x2="100" y1="40" y2="40"></line><line x1="0" x2="100" y1="60" y2="60"></line><line x1="0" x2="100" y1="80" y2="80"></line><polyline points="${points(aKey)}" class="line-a"></polyline><polyline points="${points(bKey)}" class="line-b"></polyline></svg><div class="chart-legend"><span class="dot a"></span>${aLabel}<span class="dot b"></span>${bLabel}</div></div>`;
}

function donutChart(data) {
  let start = 0;
  const total = data.reduce((sum, item) => sum + item.value, 0);
  const gradient = data.map((item) => {
    const end = start + item.value / total * 100;
    const segment = `${item.color} ${start}% ${end}%`;
    start = end;
    return segment;
  }).join(", ");
  return `<div class="donut-wrap"><div class="donut" style="background:conic-gradient(${gradient})"><span>${total}</span></div><div class="donut-list">${data.map((item) => `<span><i style="background:${item.color}"></i>${item.label} ${item.value}%</span>`).join("")}</div></div>`;
}

function progress(label, value, slim = false) {
  return `<div class="progress ${slim ? "slim" : ""}">${label ? `<div><span>${label}</span><b>${value}%</b></div>` : ""}<i><span style="width:${value}%"></span></i></div>`;
}

function agentCard(agent) {
  return `
    <button class="agent-card" data-agent="${agent.id}">
      <div class="avatar-ring ${agent.status}">AI</div>
      <strong>${agent.name}</strong>
      <small>${agent.nameEn}</small>
      ${statusBadge(agent.status)}
      <div class="agent-card-footer"><span>今日完成 <b>${agent.completedTasks}</b> 项</span><span>月KPI <b>${agent.monthKPI}</b></span></div>
      <div class="card-actions"><span>查看详情</span><span>分配任务</span></div>
    </button>`;
}

function statusBadge(status) {
  const text = { working: "工作中", standby: "待命中", offline: "离线" }[status] || status;
  return `<span class="status-badge ${status}">${text}</span>`;
}

function drawer(agent) {
  return `
    <div class="drawer-backdrop" data-action="close-drawer">
      <aside class="drawer" data-stop>
        <div class="drawer-head"><div><h2>${agent.name}</h2><span>${agent.nameEn}</span></div><button class="icon-btn" data-action="close-drawer">×</button></div>
        <p class="drawer-desc">${agent.description}</p>
        ${progress("本月完成率", agent.monthKPI)}
        ${progress("质量分", Math.min(99, agent.monthKPI + 3))}
        <h3>今日工作日志</h3>
        <div class="timeline">${agent.todayLog.map((item) => `<div><time>${item.time}</time><span>${item.action}</span></div>`).join("")}</div>
        <button class="primary-btn full" data-action="open-task">分配任务</button>
      </aside>
    </div>`;
}

function taskModal() {
  return `
    <div class="modal-backdrop" data-action="close-modal">
      <div class="modal" data-stop>
        <h2>分配任务</h2>
        ${submitted ? `<div class="success-state"><strong>任务已进入队列</strong><span>AI员工状态已更新为进行中</span></div>` : `
          <label class="field-label">任务描述</label><textarea placeholder="例如：生成品牌出海内容包（英文版）"></textarea>
          <label class="field-label">截止时间</label><input value="今天 18:00" readonly>
          <label class="field-label">优先级</label><select><option>高</option><option>中</option><option>低</option></select>
          <button class="primary-btn full" data-action="submit-task">提交任务</button>`}
      </div>
    </div>`;
}

function toolCard(tool) {
  return `<article class="tool-card"><div class="tool-icon">${tool.icon}</div><div><strong>${tool.name}</strong><small>${tool.nameEn}</small></div><p>${tool.desc}</p><div class="tool-meta"><span>${tool.category}</span>${tool.external ? `<span class="external-tag">External Agent</span>` : ""}</div><button class="ghost-btn full">立即使用</button></article>`;
}

function toggle(checked, id) {
  return `<button class="toggle ${checked ? "on" : ""}" data-toggle="${id}"><span></span></button>`;
}

function readStore(key, initialValue) {
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : initialValue;
}

function writeStore(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

document.addEventListener("click", (event) => {
  const stop = event.target.closest("[data-stop]");
  if (stop) return;

  const go = event.target.closest("[data-go]");
  if (go) {
    history.pushState({}, "", go.dataset.go);
    render();
    scrollTo({ top: 0, behavior: "smooth" });
    return;
  }

  const agentFilterButton = event.target.closest("[data-agent-filter]");
  if (agentFilterButton) {
    agentFilter = agentFilterButton.dataset.agentFilter;
    render();
    return;
  }

  const toolFilterButton = event.target.closest("[data-tool-filter]");
  if (toolFilterButton) {
    toolFilter = toolFilterButton.dataset.toolFilter;
    render();
    return;
  }

  const logFilterButton = event.target.closest("[data-log-filter]");
  if (logFilterButton) {
    logFilter = logFilterButton.dataset.logFilter;
    render();
    return;
  }

  const agentButton = event.target.closest("[data-agent]");
  if (agentButton) {
    selectedAgent = agents.find((item) => item.id === Number(agentButton.dataset.agent));
    render();
    return;
  }

  const sourceButton = event.target.closest("[data-source]");
  if (sourceButton) {
    const [type, value] = sourceButton.dataset.source.split(":");
    writeStore(`${type}-agent-source`, value);
    render();
    return;
  }

  const toggleButton = event.target.closest("[data-toggle]");
  if (toggleButton) {
    const id = toggleButton.dataset.toggle;
    if (id === "global") {
      globalEnabled = !globalEnabled;
      writeStore("agent-global-enabled", globalEnabled);
    } else if (id.startsWith("pkg:")) {
      const pkgId = id.slice(4);
      agentPackages = agentPackages.map((item) => item.id === pkgId ? { ...item, enabled: !item.enabled } : item);
    }
    render();
    return;
  }

  const action = event.target.closest("[data-action]")?.dataset.action;
  if (!action) return;

  if (action === "close-drawer") {
    selectedAgent = null;
    modalOpen = false;
    render();
  }
  if (action === "open-task") {
    modalOpen = true;
    submitted = false;
    render();
  }
  if (action === "close-modal") {
    modalOpen = false;
    render();
  }
  if (action === "submit-task") {
    submitted = true;
    render();
  }
  if (action === "toggle-key") {
    showKey = !showKey;
    render();
  }
  if (action === "test-connection") {
    const box = document.getElementById("connection-result");
    if (box) box.innerHTML = `<div class="success-line">连接成功，延迟 128ms</div>`;
  }
  if (action === "sync-knowledge") {
    const box = document.getElementById("sync-result");
    if (box) box.innerHTML = `<div class="success-line">同步完成，共 1,284 条知识</div>`;
  }
});

window.addEventListener("popstate", render);

render();
