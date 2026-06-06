import { agents } from "../../../data/mock.js";
import { page, progress, statusBadge } from "../../../shared/ui.js";

function agentCard(agent) {
  return `<button class="agent-card" data-agent="${agent.id}"><div class="avatar-ring ${agent.status}">AI</div><strong>${agent.name}</strong><small>${agent.nameEn}</small>${statusBadge(agent.status)}<div class="agent-card-footer"><span>今日完成 <b>${agent.completedTasks}</b> 项</span><span>月KPI <b>${agent.monthKPI}</b></span></div><div class="card-actions"><span>查看详情</span><span>分配任务</span></div></button>`;
}

function drawer(agent) {
  return `<div class="drawer-backdrop" data-action="close-drawer"><aside class="drawer" data-stop><div class="drawer-head"><div><h2>${agent.name}</h2><span>${agent.nameEn}</span></div><button class="icon-btn" data-action="close-drawer">×</button></div><p class="drawer-desc">${agent.description}</p>${progress("本月完成率", agent.monthKPI)}${progress("质量分", Math.min(99, agent.monthKPI + 3))}<h3>今日工作日志</h3><div class="timeline">${agent.todayLog.map((item) => `<div><time>${item.time}</time><span>${item.action}</span></div>`).join("")}</div><button class="primary-btn full" data-action="open-task">分配任务</button></aside></div>`;
}

function taskModal(submitted) {
  return `<div class="modal-backdrop" data-action="close-modal"><div class="modal" data-stop><h2>分配任务</h2>${submitted ? `<div class="success-state"><strong>任务已进入队列</strong><span>AI员工状态已更新为进行中</span></div>` : `<label class="field-label">任务描述</label><textarea placeholder="例如：生成品牌出海内容包（英文版）"></textarea><label class="field-label">截止时间</label><input value="今天 18:00" readonly><label class="field-label">优先级</label><select><option>高</option><option>中</option><option>低</option></select><button class="primary-btn full" data-action="submit-task">提交任务</button>`}</div></div>`;
}

export default {
  path: "/enterprise/agents",
  layout: "shell",
  render(context) {
    const categories = ["全部", "营销类", "运营类", "客服类", "数据类", "管理类"];
    const visible = context.agentFilter === "全部" ? agents : agents.filter((item) => item.category === context.agentFilter);
    return page("超级AI员工中心", "Super AI Agent Center", "像管理团队一样管理AI。", `<div class="page-toolbar"><div class="tabs">${categories.map((item) => `<button class="${context.agentFilter === item ? "active" : ""}" data-agent-filter="${item}">${item}</button>`).join("")}</div><button class="primary-btn">新增AI员工</button></div><div class="agent-grid">${visible.map(agentCard).join("")}<button class="agent-card add-card">+ 添加新AI员工</button></div>${context.selectedAgent ? drawer(context.selectedAgent) : ""}${context.modalOpen ? taskModal(context.submitted) : ""}`);
  }
};
