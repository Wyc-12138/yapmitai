import { page } from "../../../shared/ui.js";

const emptyToolForm = {
  name: "",
  nameEn: "",
  code: "",
  category: "内容生成",
  description: "",
  icon: "技",
  modelConfigId: "",
  promptTemplate: "请基于任务简报完成该AI工具任务：{{task}}",
  enabled: true,
  isSystem: false,
  sortOrder: 100
};

function esc(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    "\"": "&quot;",
    "'": "&#39;"
  })[char]);
}

function toolCard(tool) {
  return `
    <article class="tool-card skill-card">
      <div class="tool-icon">${esc(tool.icon || tool.name?.slice(0, 1) || "技")}</div>
      <div>
        <strong>${esc(tool.name)}</strong>
        <small>${esc(tool.nameEn || tool.code)}</small>
      </div>
      <p>${esc(tool.description || "")}</p>
      <div class="tool-meta">
        <span>${esc(tool.category)}</span>
        <span>${tool.callCount || 0} 次调用</span>
      </div>
      <div class="skill-card-actions">
        <button class="ghost-btn" data-tool-edit="${tool.id}">编辑</button>
        <button class="danger-btn" data-tool-delete="${tool.id}">删除</button>
        <button class="primary-btn" data-tool-run="${tool.id}">立即使用</button>
      </div>
    </article>`;
}

function runModal(context) {
  const tool = context.activeTool;
  if (!tool) return "";
  return `
    <div class="modal-backdrop skill-modal-backdrop">
      <div class="skill-run-modal" data-stop>
        <button class="icon-btn skill-close" data-action="close-tool-run">×</button>
        <h2>${esc(tool.name)}</h2>
        <p>${esc(tool.nameEn || tool.code)} · ${esc(tool.description || "")}</p>
        <label>使用模型
          <select id="tool-run-model">
            ${(context.toolChatModels || []).map((model) => `
              <option value="${model.id}" ${Number(tool.modelConfigId) === Number(model.id) ? "selected" : ""}>
                ${esc(model.displayName)} · ${esc(model.providerName)}
              </option>`).join("")}
          </select>
        </label>
        <label>任务简报
          <textarea id="tool-run-task" required placeholder="例如：为海南椰子零食生成TikTok短视频脚本和英文Listing"></textarea>
        </label>
        ${context.toolRunError ? `<div class="form-error">${esc(context.toolRunError)}</div>` : ""}
        <button class="primary-btn full" data-action="run-active-tool">${context.toolRunBusy ? "Running..." : "Run tool"}</button>
        <h3>RECENT OUTPUTS</h3>
        <div class="skill-record-list">
          ${(tool.recentRecords || []).length ? tool.recentRecords.map(recordCard).join("") : `<div class="empty-state">暂无历史输出</div>`}
        </div>
      </div>
    </div>`;
}

function recordCard(record) {
  return `
    <article class="skill-record">
      <h4>${esc(record.title)}</h4>
      <time>${esc(record.createdAt)}</time>
      <p>目标：${esc(record.target || "-")}</p>
      <p>建议动作：${esc(record.suggestedAction || "-")}</p>
      <p>交付物：${esc(record.deliverables || "-")}</p>
    </article>`;
}

function toolDrawer(context) {
  if (!context.toolDrawerOpen) return "";
  const form = context.toolForm || emptyToolForm;
  const editing = Boolean(form.id);
  return `
    <div class="drawer-backdrop model-config-backdrop">
      <aside class="drawer model-config-drawer" data-stop>
        <div class="drawer-head">
          <div><h2>${editing ? "编辑AI工具" : "新增AI工具"}</h2><span>Prompt Skill</span></div>
          <button class="icon-btn" data-action="close-tool-drawer">×</button>
        </div>
        <div class="drawer-form">
          <label>技能名称<input id="tool-name" value="${esc(form.name)}"></label>
          <label>英文名称<input id="tool-name-en" value="${esc(form.nameEn)}"></label>
          <label>唯一编码<input id="tool-code" value="${esc(form.code)}"></label>
          <label>分类<input id="tool-category" value="${esc(form.category)}"></label>
          <label>图标<input id="tool-icon" value="${esc(form.icon)}" maxlength="10"></label>
          <label>使用 Chat 模型
            <select id="tool-model-config">
              ${(context.toolChatModels || []).map((model) => `
                <option value="${model.id}" ${Number(form.modelConfigId) === Number(model.id) ? "selected" : ""}>
                  ${esc(model.displayName)} · ${esc(model.providerName)}
                </option>`).join("")}
            </select>
          </label>
          <label>技能说明<textarea id="tool-description">${esc(form.description)}</textarea></label>
          <label>Prompt 模板<textarea id="tool-prompt-template">${esc(form.promptTemplate)}</textarea></label>
          <label>排序<input id="tool-sort-order" type="number" value="${form.sortOrder ?? 0}"></label>
          <label class="drawer-check"><input id="tool-enabled" type="checkbox" ${form.enabled ? "checked" : ""}> 启用</label>
          <label class="drawer-check"><input id="tool-is-system" type="checkbox" ${form.isSystem ? "checked" : ""}> 系统内置</label>
          ${context.toolFormError ? `<div class="form-error">${esc(context.toolFormError)}</div>` : ""}
        </div>
        <button class="primary-btn full" data-action="save-tool">${editing ? "确认保存" : "确认新增"}</button>
      </aside>
    </div>`;
}

export default {
  path: "/enterprise/tools",
  layout: "shell",
  render(context) {
    const categories = ["全部", "内容生成", "数据分析", "营销投放", "客户管理", "运营工具", "合规工具"];
    const items = context.tools || [];
    const visible = context.toolFilter === "全部" ? items : items.filter((item) => item.category === context.toolFilter);
    return page(
      "AI工具中心",
      "AI Skills Center",
      "一个账号，使用全部AI能力。",
      `
      <div class="page-toolbar">
        <div class="tabs">${categories.map((item) => `<button class="${context.toolFilter === item ? "active" : ""}" data-tool-filter="${item}">${item}</button>`).join("")}</div>
        <button class="primary-btn" data-action="open-tool-create">新增AI工具</button>
      </div>
      ${context.toolError ? `<div class="form-error">${esc(context.toolError)}</div>` : ""}
      <div class="tool-grid">${visible.length ? visible.map(toolCard).join("") : `<div class="empty-state">暂无AI工具</div>`}</div>
      ${runModal(context)}
      ${toolDrawer(context)}
      `
    );
  }
};
