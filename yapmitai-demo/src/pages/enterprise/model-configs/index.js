import { page } from "../../../shared/ui.js";

const emptyForm = {
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

function badge(type) {
  return `<span class="model-type-badge ${type}">${type}</span>`;
}

function row(item) {
  return `
    <tr>
      <td><strong>${item.displayName}</strong><small>${item.modelCode}</small></td>
      <td>${item.providerName}<small>${item.providerCode}</small></td>
      <td>${badge(item.modelType)}</td>
      <td>${item.apiBaseUrl}</td>
      <td>${item.apiKeyLast4 ? `****${item.apiKeyLast4}` : "未配置"}</td>
      <td>${item.modelType === "embedding"
        ? `${item.maxInputTokens || "-"} tokens${item.dimension ? `<small>${item.dimension} 维</small>` : ""}`
        : `${item.contextWindowTokens || "-"} tokens${item.maxOutputTokens ? `<small>最大输出 ${item.maxOutputTokens}</small>` : ""}`}</td>
      <td>${item.enabled ? "启用" : "停用"}${item.isDefault ? " · 默认" : ""}</td>
      <td><div class="row-actions">
        <button class="tiny-btn" data-model-edit="${item.id}">编辑</button>
        <button class="danger-btn" data-model-delete="${item.id}">删除</button>
      </div></td>
    </tr>`;
}

function drawer(context) {
  if (!context.modelConfigDrawerOpen) return "";
  const form = context.modelConfigForm || emptyForm;
  const editing = Boolean(form.id);
  return `
    <div class="drawer-backdrop model-config-backdrop">
      <aside class="drawer model-config-drawer" data-stop>
        <div class="drawer-head">
          <div><h2>${editing ? "编辑模型配置" : "新增模型配置"}</h2><span>${editing ? form.displayName : "Model Provider"}</span></div>
          <button class="icon-btn" data-action="close-model-config-drawer">×</button>
        </div>
        <div class="drawer-form">
          <label>供应商编码<input id="mc-provider-code" value="${form.providerCode || ""}"></label>
          <label>供应商名称<input id="mc-provider-name" value="${form.providerName || ""}"></label>
          <label>API 模型名<input id="mc-model-code" value="${form.modelCode || ""}"></label>
          <label>页面展示名<input id="mc-display-name" value="${form.displayName || ""}"></label>
          <label>模型类型<select id="mc-model-type">
            <option value="chat" ${form.modelType === "chat" ? "selected" : ""}>chat</option>
            <option value="embedding" ${form.modelType === "embedding" ? "selected" : ""}>embedding</option>
          </select></label>
          <label>API 地址<input id="mc-api-base-url" value="${form.apiBaseUrl || ""}"></label>
          <label>API Key<input id="mc-api-key" type="password" placeholder="${editing && form.apiKeyLast4 ? `留空保持 ****${form.apiKeyLast4}` : "请输入 API Key"}"></label>
          <div class="model-specific-fields" data-model-fields="embedding" ${form.modelType !== "embedding" ? "hidden" : ""}>
            <label>输出向量维度<input id="mc-dimension" type="number" min="1" value="${form.dimension ?? ""}" placeholder="例如 1536"></label>
            <label>单段文本最大输入 Token<input id="mc-max-input-tokens" type="number" min="1" value="${form.maxInputTokens ?? ""}" placeholder="例如 8191"></label>
          </div>
          <div class="model-specific-fields" data-model-fields="chat" ${form.modelType !== "chat" ? "hidden" : ""}>
            <label>上下文窗口 Token<input id="mc-context-window-tokens" type="number" min="1" value="${form.contextWindowTokens ?? ""}" placeholder="输入与输出合计，例如 128000"></label>
            <label>单次最大输出 Token<input id="mc-max-output-tokens" type="number" min="1" value="${form.maxOutputTokens ?? ""}" placeholder="例如 4096"></label>
            <label>默认生成温度<input id="mc-default-temperature" type="number" min="0" max="2" step="0.1" value="${form.defaultTemperature ?? ""}"></label>
          </div>
          <label>备注<textarea id="mc-remark">${form.remark || ""}</textarea></label>
          <label class="drawer-check"><input id="mc-enabled" type="checkbox" ${form.enabled ? "checked" : ""}> 启用</label>
          <label class="drawer-check"><input id="mc-is-default" type="checkbox" ${form.isDefault ? "checked" : ""}> 设为该类型默认模型</label>
          ${context.modelConfigError ? `<div class="form-error">${context.modelConfigError}</div>` : ""}
        </div>
        <button class="primary-btn full model-config-submit" data-action="save-model-config">${editing ? "确认保存" : "确认新增"}</button>
      </aside>
    </div>`;
}

export default {
  path: "/enterprise/model-configs",
  layout: "shell",
  render(context) {
    const items = context.modelConfigs || [];
    return page(
      "模型配置中心",
      "Model Configurations",
      "统一管理 chat 与 embedding 模型，供智能体和本地 RAG 选择使用。",
      `
      <div class="page-toolbar">
        <div class="tabs">
          ${["全部", "chat", "embedding"].map((item) => `<button class="${context.modelConfigFilter === item ? "active" : ""}" data-model-filter="${item}">${item}</button>`).join("")}
        </div>
        <button class="primary-btn" data-action="open-model-config-create">新增模型配置</button>
      </div>
      <div class="table-wrap model-config-table">
        <table>
          <thead><tr><th>模型</th><th>供应商</th><th>类型</th><th>API地址</th><th>Key</th><th>能力</th><th>状态</th><th>操作</th></tr></thead>
          <tbody>${items.length ? items.map(row).join("") : `<tr><td colspan="8"><div class="empty-state">暂无模型配置</div></td></tr>`}</tbody>
        </table>
      </div>
      ${drawer(context)}
      `
    );
  }
};
