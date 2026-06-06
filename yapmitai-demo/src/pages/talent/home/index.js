import { miniStat, page, panel } from "../../../shared/ui.js";

export default {
  path: "/talent/home",
  layout: "shell",
  render() {
    return page("员工工作台", "Talent Workspace", "面向职工的AI协作入口。", `<div class="dashboard-grid">${panel("今日AI助手", "Assistants", `<div class="config-list flat">${["简历优化助手", "技能学习助手", "任务总结助手", "政策咨询助手"].map((item) => `<div class="config-row"><span>AI</span><span>${item}</span><button class="tiny-btn">打开</button></div>`).join("")}</div>`)}${panel("成长指数", "Growth Index", `${miniStat("本周完成任务", "18")}${miniStat("AI节省时间", "7.5h")}`)}</div>`);
  }
};
