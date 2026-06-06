import { callLogs } from "../../../../data/mock.js";
import { page } from "../../../../shared/ui.js";

export default {
  path: "/enterprise/tools/agent-logs",
  layout: "shell",
  render(context) {
    const statuses = ["全部", "成功", "失败", "超时"];
    const visible = context.logFilter === "全部" ? callLogs : callLogs.filter((item) => item.status === context.logFilter);
    return page("Agent调用日志", "Agent Call Logs", "记录每次Agent调用的模块、状态、耗时与费用。", `<div class="page-toolbar"><div class="tabs">${statuses.map((item) => `<button class="${context.logFilter === item ? "active" : ""}" data-log-filter="${item}">${item}</button>`).join("")}</div><button class="ghost-btn">导出</button></div><div class="table-wrap"><table><thead><tr><th>时间</th><th>Agent名称</th><th>调用模块</th><th>状态</th><th>耗时</th><th>费用</th></tr></thead><tbody>${visible.map((log) => `<tr><td>${log.time}</td><td>${log.agent}</td><td>${log.module}</td><td><span class="log-status ${log.status}">${log.status}</span></td><td>${log.latency}ms</td><td>¥${log.cost}</td></tr>`).join("")}</tbody></table></div>`);
  }
};
