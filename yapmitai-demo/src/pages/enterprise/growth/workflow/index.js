import { page, panel } from "../../../../shared/ui.js";

const STEPS = [
  { id: "market_analyst", label: "AI 市场分析师" },
  { id: "brand_manager", label: "AI 品牌营销经理" },
  { id: "content_creator", label: "AI 内容创作官" },
  { id: "media_buying", label: "AI 投流专家" },
  { id: "completed", label: "生成 PDF 报告" }
];

const STEP_STATUS = {
  pending: { label: "等待中", className: "pending" },
  running: { label: "执行中", className: "running" },
  done: { label: "已完成", className: "done" },
  failed: { label: "失败", className: "failed" }
};

const TABS = [
  { id: "market", label: "市场分析", key: "market_report" },
  { id: "brand", label: "品牌战略", key: "brand_strategy" },
  { id: "content", label: "内容资产", key: "content_assets" },
  { id: "media", label: "广告方案", key: "media_plan" }
];

function stepIndex(stepId) {
  const index = STEPS.findIndex((item) => item.id === stepId);
  return index === -1 ? 0 : index;
}

function resolveStepState(index, context) {
  const status = context.growthStatus || "idle";
  const current = stepIndex(context.growthStep || "market_analyst");

  if (status === "idle") return "pending";
  if (status === "completed") return "done";
  if (status === "failed") {
    if (index < current) return "done";
    if (index === current) return "failed";
    return "pending";
  }
  if (index < current) return "done";
  if (index === current) return "running";
  return "pending";
}

function workflowList(context) {
  return `
    <div class="growth-workflow-list">
      ${STEPS.map((step, index) => {
        const state = resolveStepState(index, context);
        const meta = STEP_STATUS[state];
        return `<article class="growth-workflow-row ${meta.className}">
          <div class="growth-workflow-row-left">
            <span class="growth-step-index">${index + 1}</span>
            <strong>${step.label}</strong>
          </div>
          <span class="growth-workflow-status ${meta.className}">${meta.label}</span>
        </article>`;
      }).join("")}
    </div>`;
}

function renderJsonBlock(data) {
  if (!data || !Object.keys(data).length) {
    return `<div class="empty-state">等待 Agent 输出…</div>`;
  }
  return `<pre class="growth-json">${JSON.stringify(data, null, 2)}</pre>`;
}

function failureBanner(context) {
  if (context.growthStatus !== "failed") return "";
  const message =
    context.growthError ||
    "任务已失败，但后端未返回具体原因。请查看运行 uvicorn 的后端终端日志。";
  return `
    <div class="growth-error-banner">
      <strong>失败原因</strong>
      <p>${message}</p>
      ${context.growthTaskId ? `<small>任务 ID：${context.growthTaskId} · 可在浏览器 F12 → Network → GET /api/task/${context.growthTaskId} 查看 error_message</small>` : ""}
    </div>`;
}

function resultTabs(context) {
  const active = context.growthResultTab || "market";
  const tab = TABS.find((item) => item.id === active) || TABS[0];
  const payload = context.growthContext?.[tab.key] || {};
  return `
    <div class="page-toolbar">
      <div class="tabs">
        ${TABS.map((item) => `<button class="${active === item.id ? "active" : ""}" data-growth-tab="${item.id}">${item.label}</button>`).join("")}
      </div>
      ${context.growthStatus === "completed" ? `<button class="primary-btn" data-action="download-growth-report">下载 PDF 报告</button>` : ""}
    </div>
    ${renderJsonBlock(payload)}`;
}

export default {
  path: "/enterprise/growth/workflow",
  layout: "shell",
  render(context) {
    const busy = context.growthBusy;
    const status = context.growthStatus || "idle";
    const statusText = {
      idle: "输入一句增长需求，系统将自动串联四个 Agent 并生成 PDF。",
      running: "方案生成中，请稍候（目标 2–5 分钟）…",
      completed: "增长方案已生成，可预览结果并下载 PDF 报告。"
    }[status] || "";

    return page(
      "品牌增长方案",
      "Growth Strategy",
      statusText,
      `
      <div class="growth-layout">
        <section class="panel">
          <div class="growth-brief">
            <label class="field-label">描述你的品牌增长需求</label>
            <textarea id="growth-prompt" placeholder="例如：我要把海南椰子水卖到马来西亚市场" ${busy ? "disabled" : ""}>${context.growthPrompt || ""}</textarea>
            <div class="growth-actions">
              <button class="primary-btn" data-action="start-growth-task" ${busy ? "disabled" : ""}>
                ${busy ? "生成中…" : "生成增长方案 PDF"}
              </button>
              ${context.growthTaskId ? `<span class="growth-task-id">任务 ID：${context.growthTaskId}</span>` : ""}
            </div>
          </div>
        </section>
        ${panel(
          "执行进度",
          "Agent Pipeline",
          `${failureBanner(context)}
          ${workflowList(context)}`
        )}
        ${panel("增长方案结果", "Strategy Output", resultTabs(context))}
      </div>`
    );
  }
};
