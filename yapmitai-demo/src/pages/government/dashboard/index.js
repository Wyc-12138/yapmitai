import { govKpis, moduleDistribution, trend7d } from "../../../data/mock.js";
import { donutChart, kpi, lineChart, panel } from "../../../shared/ui.js";

export default {
  path: "/government/dashboard",
  layout: "full",
  render() {
    return `<div class="gov-screen"><header class="gov-header"><button class="ghost-btn" data-go="/">返回首页</button><div><h1>海南自贸港 · 产业AI驾驶舱</h1><span>Hainan FTP · Industrial AI Decision Dashboard</span></div><time>${new Date().toLocaleString("zh-CN", { hour12: false })}</time></header><div class="gov-kpi-grid">${govKpis.map(kpi).join("")}</div><div class="gov-grid">${panel("产业活跃度", "30-Day Activity", lineChart(trend7d, "calls", "success", "产业活跃", "AI贡献"))}${panel("企业类型分布", "Enterprise Distribution", donutChart(moduleDistribution))}${panel("AI政策问答助手", "Policy Assistant", `<div class="assistant-box"><span class="tool-icon">策</span><strong>永不落幕消博会政策助手</strong><p>可查询自贸港税收政策、品牌出海补贴、企业入驻流程。</p><button class="primary-btn full">打开助手</button></div>`)}</div></div>`;
  }
};
