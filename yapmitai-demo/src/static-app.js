import { agents } from "./data/mock.js";
import { findRoute } from "./routes/index.js";

const app = document.getElementById("root");

const state = {
  agentFilter: "全部",
  toolFilter: "全部",
  logFilter: "全部",
  selectedAgent: null,
  modalOpen: false,
  submitted: false,
  showKey: false,
  globalEnabled: readStore("agent-global-enabled", true),
  agentPackages: [
    { id: "creation-image", name: "文生图 Agent", type: "AI创作", version: "1.2.0", enabled: true },
    { id: "creation-video", name: "文生视频 Agent", type: "AI创作", version: "1.0.8", enabled: true },
    { id: "outreach-leads", name: "智能获客 Agent", type: "拓客", version: "2.1.1", enabled: true },
    { id: "cs-personalwx", name: "个微客服 Agent", type: "客服", version: "1.4.3", enabled: false },
    { id: "cs-corpwx", name: "企微客服 Agent", type: "客服", version: "1.5.0", enabled: true },
    { id: "knowledge-rag", name: "RAG知识库 Agent", type: "知识库", version: "0.9.7", enabled: true }
  ]
};

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
  if (path !== "/enterprise/agents") {
    state.selectedAgent = null;
    state.modalOpen = false;
  }

  const route = findRoute(path);
  const context = { ...state, readStore };
  const content = route
    ? route.render(context)
    : `<section><div class="page-title"><span class="eyebrow">Not Found</span><h1>页面未找到</h1><p>当前路由还没有对应页面。</p></div><button class="primary-btn" data-go="/">返回首页</button></section>`;

  app.innerHTML = route?.layout === "full" ? content : shell(path, content);
}

function shell(path, content) {
  return `
    <div class="app-shell">
      <aside class="side-nav">
        ${brand()}
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

function brand() {
  return `<button class="brand" data-go="/"><span class="brand-mark">Y</span><span><strong>悦普AI产业超级操作系统</strong><small>YAPMITAI Industrial AI OS</small></span></button>`;
}

function readStore(key, initialValue) {
  const raw = localStorage.getItem(key);
  return raw ? JSON.parse(raw) : initialValue;
}

function writeStore(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

document.addEventListener("click", (event) => {
  const go = event.target.closest("[data-go]");
  if (go) {
    history.pushState({}, "", go.dataset.go);
    render();
    scrollTo({ top: 0, behavior: "smooth" });
    return;
  }

  const agentFilterButton = event.target.closest("[data-agent-filter]");
  if (agentFilterButton) {
    state.agentFilter = agentFilterButton.dataset.agentFilter;
    render();
    return;
  }

  const toolFilterButton = event.target.closest("[data-tool-filter]");
  if (toolFilterButton) {
    state.toolFilter = toolFilterButton.dataset.toolFilter;
    render();
    return;
  }

  const logFilterButton = event.target.closest("[data-log-filter]");
  if (logFilterButton) {
    state.logFilter = logFilterButton.dataset.logFilter;
    render();
    return;
  }

  const agentButton = event.target.closest("[data-agent]");
  if (agentButton) {
    state.selectedAgent = agents.find((item) => item.id === Number(agentButton.dataset.agent));
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
      state.globalEnabled = !state.globalEnabled;
      writeStore("agent-global-enabled", state.globalEnabled);
    } else if (id.startsWith("pkg:")) {
      const packageId = id.slice(4);
      state.agentPackages = state.agentPackages.map((item) =>
        item.id === packageId ? { ...item, enabled: !item.enabled } : item
      );
    }
    render();
    return;
  }

  const action = event.target.closest("[data-action]")?.dataset.action;
  if (!action) return;

  if (action === "close-drawer") {
    state.selectedAgent = null;
    state.modalOpen = false;
    render();
  } else if (action === "open-task") {
    state.modalOpen = true;
    state.submitted = false;
    render();
  } else if (action === "close-modal") {
    state.modalOpen = false;
    render();
  } else if (action === "submit-task") {
    state.submitted = true;
    render();
  } else if (action === "toggle-key") {
    state.showKey = !state.showKey;
    render();
  } else if (action === "test-connection") {
    const box = document.getElementById("connection-result");
    if (box) box.innerHTML = `<div class="success-line">连接成功，延迟 128ms</div>`;
  } else if (action === "sync-knowledge") {
    const box = document.getElementById("sync-result");
    if (box) box.innerHTML = `<div class="success-line">同步完成，共 1,284 条知识</div>`;
  }
});

window.addEventListener("popstate", render);
render();
