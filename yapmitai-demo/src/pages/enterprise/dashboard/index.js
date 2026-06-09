import { enterpriseKpis, moduleDistribution, salesTrend, tasks, trend7d } from "../../../data/mock.js";
import { donutChart, kpi, lineChart, miniStat, page, panel, progress } from "../../../shared/ui.js";

function taskList() {
  return `<div class="task-list">${tasks.map((task) => `<article class="task-row"><div><strong>${task.task}</strong><span>${task.agent}</span></div><span class="task-status ${task.status}">${task.status}</span>${progress("", task.progress, true)}</article>`).join("")}</div>`;
}

export default {
  path: "/enterprise/dashboard",
  layout: "shell",
  render() {
    return page("企业AI控制台", "Enterprise AI Dashboard", "欢迎回来，李总。今日AI团队已完成 12 项任务。", `<div class="enterprise-dashboard-screen">
      <div class="kpi-grid">${enterpriseKpis.map(kpi).join("")}</div>
      <div class="dashboard-grid">${panel("销售趋势", "Sales vs AI Contribution", lineChart(salesTrend, "sales", "ai", "总销售额", "AI贡献"))}${panel("AI员工任务分布", "Agent Workload", donutChart(moduleDistribution))}</div>
      <div class="dashboard-grid wide-left">${panel("今日任务队列", "Today's Task Queue", taskList())}${panel("第三方Agent调用统计", "Gateway Stats", `<div class="mini-stat-grid">${miniStat("今日调用", "1,248")}${miniStat("成功率", "98.6%")}${miniStat("平均响应", "1.28s")}${miniStat("本月费用", "¥8,420")}</div>${lineChart(trend7d, "calls", "success", "调用量", "成功数", true)}<button class="primary-btn full" data-go="/enterprise/tools/agent-logs">查看调用日志</button>`)}</div></div>`);
  }
};
