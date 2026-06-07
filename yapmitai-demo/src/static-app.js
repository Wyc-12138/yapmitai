import { agents } from "./data/mock.js";
import { findRoute } from "./routes/index.js";
import { knowledgeApi } from "./services/knowledgeApi.js";
import { modelConfigsApi } from "./services/modelConfigsApi.js";

const app = document.getElementById("root");

const state = {
  agentFilter: "全部",
  toolFilter: "全部",
  logFilter: "全部",
  selectedAgent: null,
  modalOpen: false,
  submitted: false,
  knowledgeCreateOpen: false,
  selectedKnowledge: null,
  knowledgeKeyword: "",
  knowledgePage: 1,
  embeddingModels: ["text-embedding-3-small", "text-embedding-3-large"],
  answerModels: ["gpt-4o-mini", "gpt-4.1-mini"],
  embeddingModel: "text-embedding-3-small",
  answerModel: "gpt-4o-mini",
  externalAiConfigured: false,
  selectedKnowledgeBaseId: "",
  modelActionStatus: "",
  modelTestResult: null,
  modelBusy: false,
  ragQuestion: "",
  ragResult: null,
  ragBusy: false,
  ragError: "",
  modelConfigs: [],
  modelConfigFilter: "全部",
  modelConfigDrawerOpen: false,
  modelConfigForm: null,
  modelConfigError: "",
  localLibraries: [
    { id: "kb-brand", name: "品牌营销知识库", description: "品牌定位、营销案例与消费品牌增长方法", knowledgeType: "text", collectionCount: 28, createdAt: "2026-05-15 18:05:06", updatedAt: "2026-06-06 10:20:00" },
    { id: "kb-cross-border", name: "跨境电商知识库", description: "亚马逊、Shopee、Lazada运营与出海案例", knowledgeType: "text", collectionCount: 46, createdAt: "2026-05-15 12:10:45", updatedAt: "2026-06-05 16:42:00" },
    { id: "kb-policy", name: "海南自贸港政策库", description: "税收优惠、人才政策与企业入驻指引", knowledgeType: "text", collectionCount: 35, createdAt: "2026-04-30 15:39:33", updatedAt: "2026-06-04 09:12:00" },
    { id: "kb-finance", name: "财税合规知识库", description: "企业财税制度、申报流程与合规案例", knowledgeType: "text", collectionCount: 19, createdAt: "2026-04-25 11:05:02", updatedAt: "2026-06-02 15:20:00" },
    { id: "kb-product-images", name: "商品图片素材库", description: "商品主图、场景图与品牌视觉素材", knowledgeType: "image", collectionCount: 16, createdAt: "2026-04-22 17:26:20", updatedAt: "2026-06-03 14:30:00" }
  ],
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
  ["/enterprise/model-configs", "模型配置", "Models"],
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
  if (path !== "/enterprise/knowledge/agent") {
    state.knowledgeCreateOpen = false;
    state.selectedKnowledge = null;
  }
  if (path !== "/enterprise/model-configs") {
    state.modelConfigDrawerOpen = false;
    state.modelConfigForm = null;
    state.modelConfigError = "";
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

  const modelFilterButton = event.target.closest("[data-model-filter]");
  if (modelFilterButton) {
    state.modelConfigFilter = modelFilterButton.dataset.modelFilter;
    loadModelConfigs();
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

  const actionElement = event.target.closest("[data-action]");
  const stopContainer = event.target.closest("[data-stop]");
  if (stopContainer && actionElement && !stopContainer.contains(actionElement)) return;
  const action = actionElement?.dataset.action;
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
  } else if (action === "open-knowledge-create") {
    state.knowledgeCreateOpen = true;
    render();
  } else if (action === "close-knowledge-create") {
    state.knowledgeCreateOpen = false;
    render();
  } else if (action === "create-knowledge") {
    createKnowledgeLibrary();
  } else if (action === "search-knowledge") {
    state.knowledgeKeyword = document.getElementById("knowledge-search")?.value || "";
    state.knowledgePage = 1;
    render();
  } else if (action === "close-knowledge-detail") {
    state.selectedKnowledge = null;
    render();
  } else if (action === "open-model-config-create") {
    state.modelConfigDrawerOpen = true;
    state.modelConfigForm = {
      providerCode: "openai",
      providerName: "OpenAI",
      modelCode: "",
      displayName: "",
      modelType: "chat",
      apiBaseUrl: "https://api.openai.com/v1",
      apiKey: "",
      dimension: "",
      maxInputTokens: "",
      contextWindowTokens: "",
      maxOutputTokens: "",
      defaultTemperature: "0.2",
      enabled: true,
      isDefault: false,
      remark: ""
    };
    state.modelConfigError = "";
    render();
  } else if (action === "close-model-config-drawer") {
    closeModelConfigDrawer();
  } else if (action === "save-model-config") {
    saveModelConfig();
  }
});

document.addEventListener("click", (event) => {
  const detailButton = event.target.closest("[data-knowledge-detail]");
  if (detailButton) {
    openKnowledgeDetail(detailButton.dataset.knowledgeDetail);
    return;
  }

  const deleteButton = event.target.closest("[data-knowledge-delete]");
  if (deleteButton) {
    deleteKnowledgeLibrary(deleteButton.dataset.knowledgeDelete);
    return;
  }

  const pageButton = event.target.closest("[data-knowledge-page]");
  if (pageButton && !pageButton.disabled) {
    state.knowledgePage = Number(pageButton.dataset.knowledgePage);
    render();
    return;
  }

  const embeddingButton = event.target.closest("[data-embedding-model]");
  if (embeddingButton) {
    state.embeddingModel = embeddingButton.dataset.embeddingModel;
    saveKnowledgeModelConfig();
    render();
    return;
  }

  const answerButton = event.target.closest("[data-answer-model]");
  if (answerButton) {
    state.answerModel = answerButton.dataset.answerModel;
    saveKnowledgeModelConfig();
    render();
    return;
  }

  if (event.target.closest("[data-action='test-local-models']")) {
    testLocalModels();
    return;
  }

  if (event.target.closest("[data-action='ask-local-knowledge']")) {
    askLocalKnowledge();
    return;
  }

  const editModelButton = event.target.closest("[data-model-edit]");
  if (editModelButton) {
    const item = state.modelConfigs.find((model) => String(model.id) === editModelButton.dataset.modelEdit);
    state.modelConfigDrawerOpen = true;
    state.modelConfigForm = { ...item, apiKey: "" };
    state.modelConfigError = "";
    render();
    return;
  }

  const deleteModelButton = event.target.closest("[data-model-delete]");
  if (deleteModelButton) {
    deleteModelConfig(deleteModelButton.dataset.modelDelete);
  }
});

document.addEventListener("change", (event) => {
  if (event.target.id === "mc-model-type") {
    toggleModelSpecificFields(event.target.value);
    return;
  }
  if (event.target.id === "local-model-knowledge-base") {
    selectModelKnowledgeBase(event.target.value);
    return;
  }
  const input = event.target.closest("[data-knowledge-upload]");
  if (!input || !input.files?.length) return;
  const libraryId = input.dataset.knowledgeUpload;
  const file = input.files[0];
  uploadKnowledgeDocument(libraryId, file);
});

async function createKnowledgeLibrary() {
  const name = document.getElementById("knowledge-name")?.value.trim();
  const knowledgeType = document.getElementById("knowledge-type")?.value;
  const description = document.getElementById("knowledge-description")?.value.trim();
  const error = document.getElementById("knowledge-form-error");

  if (!name || !description) {
    if (error) error.textContent = "请完整填写知识库名称和描述。";
    return;
  }

  const payload = { name, knowledge_type: knowledgeType, description };
  try {
    const response = await knowledgeApi.createLibrary(payload);
    const library = response.data;
    state.localLibraries = [library, ...state.localLibraries];
    state.selectedKnowledgeBaseId = library.id;
    state.embeddingModel = library.embeddingModel;
    state.answerModel = library.answerModel;
    state.knowledgeCreateOpen = false;
    state.knowledgePage = 1;
    render();
  } catch (requestError) {
    if (error) error.textContent = requestError.message;
  }
}

window.addEventListener("popstate", render);
render();
initializeKnowledge();
loadModelConfigs();

async function initializeKnowledge() {
  await loadKnowledgeLibraries();
  await loadKnowledgeModelConfig();
}

async function loadKnowledgeLibraries() {
  try {
    const response = await knowledgeApi.listLibraries({ page_size: 100 });
    state.localLibraries = response.data?.items || [];
    if (
      !state.selectedKnowledgeBaseId ||
      !state.localLibraries.some((item) => item.id === state.selectedKnowledgeBaseId)
    ) {
      state.selectedKnowledgeBaseId = state.localLibraries[0]?.id || "";
    }
    if (window.location.pathname === "/enterprise/knowledge/agent") render();
  } catch {
    // The static Demo keeps its local fallback data when the API is offline.
  }
}

async function loadKnowledgeModelConfig() {
  try {
    const response = await knowledgeApi.getModelConfig(state.selectedKnowledgeBaseId);
    const config = response.data;
    state.embeddingModels = config.embeddingModels;
    state.answerModels = config.answerModels;
    state.embeddingModel = config.embeddingModel;
    state.answerModel = config.answerModel;
    state.externalAiConfigured = config.configured;
    if (window.location.pathname === "/enterprise/knowledge/agent") render();
  } catch {
    // Keep defaults when the backend is offline.
  }
}

async function saveKnowledgeModelConfig() {
  if (!state.selectedKnowledgeBaseId) {
    state.modelActionStatus = "请先创建并选择一个本地知识库。";
    render();
    return;
  }
  state.modelActionStatus = "正在保存模型配置…";
  render();
  try {
    const response = await knowledgeApi.updateModelConfig({
      knowledge_base_id: state.selectedKnowledgeBaseId,
      embedding_model: state.embeddingModel,
      answer_model: state.answerModel
    });
    state.modelActionStatus = "模型配置已保存到该知识库。";
    state.localLibraries = state.localLibraries.map((item) =>
      item.id === state.selectedKnowledgeBaseId
        ? { ...item, embeddingModel: response.data.embeddingModel, answerModel: response.data.answerModel }
        : item
    );
  } catch (error) {
    state.modelActionStatus = error.message;
  }
  render();
}

async function selectModelKnowledgeBase(libraryId) {
  state.selectedKnowledgeBaseId = libraryId;
  state.modelTestResult = null;
  state.ragResult = null;
  state.modelActionStatus = "";
  const library = state.localLibraries.find((item) => item.id === libraryId);
  if (library?.embeddingModel) state.embeddingModel = library.embeddingModel;
  if (library?.answerModel) state.answerModel = library.answerModel;
  render();
  await loadKnowledgeModelConfig();
}

async function testLocalModels() {
  if (!state.selectedKnowledgeBaseId || state.modelBusy) return;
  state.modelBusy = true;
  state.modelTestResult = null;
  state.modelActionStatus = "正在真实调用 Embedding 和回答模型…";
  render();
  try {
    const response = await knowledgeApi.testModels({
      knowledge_base_id: state.selectedKnowledgeBaseId,
      text: "请确认本地知识库模型连接正常"
    });
    state.modelTestResult = response.data;
    state.modelActionStatus = "真实模型调用成功。";
  } catch (error) {
    state.modelActionStatus = error.message;
  } finally {
    state.modelBusy = false;
    render();
  }
}

async function askLocalKnowledge() {
  const question = document.getElementById("local-rag-question")?.value.trim();
  if (!question || !state.selectedKnowledgeBaseId || state.ragBusy) return;
  state.ragQuestion = question;
  state.ragBusy = true;
  state.ragError = "";
  state.ragResult = null;
  render();
  try {
    const response = await knowledgeApi.query({
      query: question,
      limit: 5,
      knowledge_base_id: state.selectedKnowledgeBaseId
    });
    state.ragResult = response.data;
  } catch (error) {
    state.ragError = error.message;
  } finally {
    state.ragBusy = false;
    render();
  }
}

async function uploadKnowledgeDocument(libraryId, file) {
  state.modelActionStatus = `正在使用真实 Embedding API 处理 ${file.name}…`;
  render();
  try {
    await knowledgeApi.uploadCollection(libraryId, file);
    state.modelActionStatus = `${file.name} 已完成切片和向量化。`;
    await loadKnowledgeLibraries();
  } catch (error) {
    state.modelActionStatus = error.message;
    render();
  }
}

async function deleteKnowledgeLibrary(libraryId) {
  const library = state.localLibraries.find((item) => item.id === libraryId);
  const name = library?.name || "该知识库";
  if (!window.confirm(`确定删除知识库“${name}”吗？关联文档和向量数据也会被删除，此操作无法撤销。`)) {
    return;
  }
  try {
    await knowledgeApi.deleteLibrary(libraryId);
    state.localLibraries = state.localLibraries.filter((item) => item.id !== libraryId);
    if (state.selectedKnowledgeBaseId === libraryId) {
      state.selectedKnowledgeBaseId = state.localLibraries[0]?.id || "";
      await loadKnowledgeModelConfig();
    }
    state.modelActionStatus = "知识库及其 Chroma 向量已删除。";
  } catch (error) {
    state.modelActionStatus = error.message;
  }
  render();
}

async function loadModelConfigs() {
  try {
    const params = state.modelConfigFilter === "全部" ? {} : { model_type: state.modelConfigFilter };
    const response = await modelConfigsApi.list(params);
    state.modelConfigs = response.data || [];
    if (window.location.pathname === "/enterprise/model-configs") render();
  } catch (error) {
    state.modelConfigError = error.message;
    if (window.location.pathname === "/enterprise/model-configs") render();
  }
}

function readModelConfigForm() {
  const numberValue = (id) => {
    const value = document.getElementById(id)?.value;
    return value ? Number(value) : null;
  };
  const modelType = document.getElementById("mc-model-type")?.value;
  const payload = {
    provider_code: document.getElementById("mc-provider-code")?.value.trim(),
    provider_name: document.getElementById("mc-provider-name")?.value.trim(),
    model_code: document.getElementById("mc-model-code")?.value.trim(),
    display_name: document.getElementById("mc-display-name")?.value.trim(),
    model_type: modelType,
    api_base_url: document.getElementById("mc-api-base-url")?.value.trim(),
    api_key: document.getElementById("mc-api-key")?.value,
    enabled: document.getElementById("mc-enabled")?.checked,
    is_default: document.getElementById("mc-is-default")?.checked,
    remark: document.getElementById("mc-remark")?.value.trim() || null
  };
  if (modelType === "embedding") {
    payload.dimension = numberValue("mc-dimension");
    payload.max_input_tokens = numberValue("mc-max-input-tokens");
  } else {
    payload.context_window_tokens = numberValue("mc-context-window-tokens");
    payload.max_output_tokens = numberValue("mc-max-output-tokens");
    payload.default_temperature = numberValue("mc-default-temperature");
  }
  return payload;
}

function toggleModelSpecificFields(modelType) {
  document.querySelectorAll("[data-model-fields]").forEach((section) => {
    section.hidden = section.dataset.modelFields !== modelType;
  });
}

function closeModelConfigDrawer() {
  if (!state.modelConfigDrawerOpen) return;
  if (!window.confirm("退出后当前内容不会保存，确定退出吗？")) {
    return;
  }
  state.modelConfigDrawerOpen = false;
  state.modelConfigForm = null;
  state.modelConfigError = "";
  render();
}

async function saveModelConfig() {
  const payload = readModelConfigForm();
  const editingId = state.modelConfigForm?.id;
  if (!payload.provider_code || !payload.provider_name || !payload.model_code || !payload.display_name || !payload.api_base_url) {
    state.modelConfigError = "请填写供应商、模型名、展示名和 API 地址。";
    render();
    return;
  }
  if (payload.model_type === "embedding" && (!payload.dimension || !payload.max_input_tokens)) {
    state.modelConfigError = "Embedding 模型必须填写输出向量维度和最大输入 Token。";
    render();
    return;
  }
  if (payload.model_type === "chat" && (!payload.context_window_tokens || !payload.max_output_tokens)) {
    state.modelConfigError = "Chat 模型必须填写上下文窗口和单次最大输出 Token。";
    render();
    return;
  }
  if (editingId && !payload.api_key) {
    delete payload.api_key;
  }
  try {
    if (editingId) {
      await modelConfigsApi.update(editingId, payload);
    } else {
      await modelConfigsApi.create(payload);
    }
    state.modelConfigDrawerOpen = false;
    state.modelConfigForm = null;
    state.modelConfigError = "";
    await loadModelConfigs();
    await loadKnowledgeModelConfig();
  } catch (error) {
    state.modelConfigError = error.message;
    render();
  }
}

async function deleteModelConfig(id) {
  const model = state.modelConfigs.find((item) => String(item.id) === String(id));
  const name = model?.displayName || model?.modelCode || "该模型配置";
  if (!window.confirm(`确定删除模型配置“${name}”吗？此操作无法撤销。`)) {
    return;
  }
  try {
    await modelConfigsApi.delete(id);
    await loadModelConfigs();
    await loadKnowledgeModelConfig();
  } catch (error) {
    state.modelConfigError = error.message;
    render();
  }
}

async function openKnowledgeDetail(libraryId) {
  state.selectedKnowledge = state.localLibraries.find((item) => item.id === libraryId);
  render();
  try {
    const response = await knowledgeApi.getLibrary(libraryId);
    state.selectedKnowledge = response.data;
    render();
  } catch {
    // Keep the list summary when the backend is offline.
  }
}
