import { miniStat, page, panel, progress, toggle } from "../../../../shared/ui.js";

export default {
  path: "/enterprise/knowledge/agent",
  layout: "shell",
  render() {
    return page("企业智库Agent配置", "Enterprise Knowledge Agent", "外部向量库与系统关键词库合并检索。", `<div class="settings-grid">${panel("知识库来源", "Knowledge Sources", `<div class="config-list flat">${["外部Agent向量库", "系统原有关键词库", "品牌知识库", "跨境案例库"].map((item) => `<div class="config-row"><span>库</span><span>${item}</span>${toggle(true, "noop")}</div>`).join("")}</div>`)}${panel("同步状态", "Sync Status", `${miniStat("知识条数", "1,284")}${miniStat("上次同步", "2分钟前")}${progress("同步进度", 100)}<button class="primary-btn full" data-action="sync-knowledge">立即同步</button><div id="sync-result"></div>`)}</div>`);
  }
};
