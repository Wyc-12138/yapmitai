import { tools } from "../../../data/mock.js";
import { page } from "../../../shared/ui.js";

function toolCard(tool) {
  return `<article class="tool-card"><div class="tool-icon">${tool.icon}</div><div><strong>${tool.name}</strong><small>${tool.nameEn}</small></div><p>${tool.desc}</p><div class="tool-meta"><span>${tool.category}</span>${tool.external ? `<span class="external-tag">External Agent</span>` : ""}</div><button class="ghost-btn full">立即使用</button></article>`;
}

export default {
  path: "/enterprise/tools",
  layout: "shell",
  render(context) {
    const categories = ["全部", "内容生成", "数据分析", "营销投放", "客户管理", "运营工具", "合规工具"];
    const visible = context.toolFilter === "全部" ? tools : tools.filter((item) => item.category === context.toolFilter);
    return page("AI工具中心", "AI Skills Center", "一个账号，使用全部AI能力。", `<div class="tabs">${categories.map((item) => `<button class="${context.toolFilter === item ? "active" : ""}" data-tool-filter="${item}">${item}</button>`).join("")}</div><div class="tool-grid">${visible.map(toolCard).join("")}</div>`);
  }
};
