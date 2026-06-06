import { allianceMembers, alliancePlans } from "../../../data/mock.js";
import { kpi, page, panel, progress } from "../../../shared/ui.js";

export default {
  path: "/alliance/dashboard",
  layout: "shell",
  render() {
    return page("产业联盟管理中心", "Alliance Management Center", "展示联盟成员网络与100家品牌AI增长计划。", `<div class="kpi-grid three">${kpi({ title: "成员企业数", value: "128", unit: "家", trend: "+16", color: "#00C9A7" })}${kpi({ title: "活跃企业", value: "96", unit: "家", trend: "+12%", color: "#4361EE" })}${kpi({ title: "总GMV", value: "12.4", unit: "亿元", trend: "+18%", color: "#F72585" })}</div><div class="dashboard-grid">${panel("AI增长计划", "Growth Programs", `<div class="plan-list">${alliancePlans.map((plan) => `<article class="plan-card"><div><strong>${plan.name}</strong><span>${plan.status}</span></div>${progress(`${plan.current}/${plan.target}家`, Math.round(plan.current / plan.target * 100))}</article>`).join("")}</div>`)}${panel("联盟成员列表", "Members", `<div class="member-list">${allianceMembers.map((member) => `<div class="member-row"><span>企</span><div><strong>${member.name}</strong><span>${member.type} · ${member.level}</span></div><span class="log-status 成功">${member.status}</span></div>`).join("")}</div>`)}</div>`);
  }
};
