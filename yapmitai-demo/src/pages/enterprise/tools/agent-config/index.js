import { page, panel, statusBadge, toggle } from "../../../../shared/ui.js";

export default {
  path: "/enterprise/tools/agent-config",
  layout: "shell",
  render(context) {
    return page("Agent网关全局配置", "Agent Gateway Config", "统一管理外部Agent包、全局开关与连接测试。", `<div class="settings-grid">${panel("连接配置", "Connection", `<label class="field-label">API Key</label><div class="input-row"><span>密</span><input value="${context.showKey ? "yap_sk_live_demo_2026" : "••••••••••••••••••••"}" readonly><button class="icon-btn" data-action="toggle-key">${context.showKey ? "隐" : "显"}</button></div><label class="field-label">网关地址</label><div class="input-row"><span>网</span><input value="https://gateway.yapmitai.com/api/v1" readonly></div><label class="field-label">超时设置</label><div class="input-row"><span>时</span><input value="30s" readonly></div><div class="switch-row"><div><strong>全局 Agent 总开关</strong><small>${context.globalEnabled ? "外部Agent优先，异常自动fallback" : "全部接口直接使用Mock fallback"}</small></div>${toggle(context.globalEnabled, "global")}</div><button class="primary-btn full" data-action="test-connection">连接测试</button><div id="connection-result"></div>`)}${panel("可用Agent包列表", "Available Agent Packages", `<div class="agent-package-list">${context.agentPackages.map((item) => `<div class="agent-package"><div><strong>${item.name}</strong><span>${item.type} · v${item.version}</span></div>${statusBadge(item.enabled ? "working" : "offline")}${toggle(item.enabled, `pkg:${item.id}`)}</div>`).join("")}</div>`)}</div>`);
  }
};
