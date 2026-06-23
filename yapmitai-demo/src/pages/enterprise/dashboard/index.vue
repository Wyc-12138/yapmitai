<template>
  <section>
    <PageHeader eyebrow="Dashboard · Overview" title="今日企业全景" description="海南澄迈品牌有限公司 · 所有AI员工运行中 · 上次更新 2分钟前" />
    <div class="enterprise-dashboard-screen">
      <!-- Alert strip -->
      <div class="alert-strip">
        <span class="alert-icon">⚠️</span>
        <span class="alert-text">AI跨境运营经理 有 <strong>2</strong> 项任务待确认分配，投流预算剩余不足72小时</span>
        <span class="alert-action" @click="router.push('/enterprise/agents')">立即处理 →</span>
      </div>

      <!-- KPI row: 5 cards -->
      <div class="kpi-row">
        <KpiCard v-for="item in enterpriseKpis" :key="item.title" :item="item" />
      </div>

      <!-- TWO COL: Workflow + Tasks -->
      <div class="two-col">

        <!-- WORKFLOW -->
        <div class="section-card">
          <div class="section-head">
            <span style="font-size:14px">🔀</span>
            <h3>工作流进展</h3>
            <span class="sub">今日活跃 {{ dashboardWorkflows.length }} 条</span>
            <span class="view-all">查看全部</span>
          </div>
          <div class="section-body">
            <div class="workflow-steps">
              <div v-for="wf in dashboardWorkflows" :key="wf.id" class="wf-step">
                <div class="wf-num" :class="wf.status">{{ wf.id }}</div>
                <div class="wf-info">
                  <div class="wf-name">{{ wf.name }}</div>
                  <div class="wf-detail">{{ wf.detail }}</div>
                  <div class="wf-agent">→ {{ wf.agent }}</div>
                </div>
                <div class="wf-progress">
                  <div class="progress-bar">
                    <div class="progress-fill" :class="wf.status" :style="{ width: wf.progress + '%' }"></div>
                  </div>
                  <div class="progress-pct" :class="wf.status">{{ wf.progress }}%</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- TODAY TASKS -->
        <div class="section-card">
          <div class="section-head">
            <span style="font-size:14px">📋</span>
            <h3>今日任务</h3>
            <span class="sub">{{ dashboardTasks.filter(t => t.status === 'running').length }} 项进行中</span>
            <span class="view-all">全部任务</span>
          </div>
          <div class="section-body">
            <div class="task-list">
              <div v-for="task in dashboardTasks" :key="task.id" class="task-item">
                <div>
                  <div class="task-title">{{ task.title }}</div>
                  <div class="task-meta">
                    <span class="task-tag" :class="task.tagClass">{{ task.tag }}</span>
                    <span><span class="status-dot" :class="task.statusClass"></span>{{ task.statusText }}</span>
                    <span>{{ task.time }}</span>
                  </div>
                </div>
                <div class="task-right">
                  <div class="task-pct" :class="task.statusClass">{{ task.progressText }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- THREE COL: AI AGENTS + Cost + Results -->
      <div class="three-col">

        <!-- AI AGENTS -->
        <div class="section-card">
          <div class="section-head">
            <span style="font-size:14px">🤖</span>
            <h3>AI员工状态</h3>
            <span class="sub">{{ dashboardAgents.length }} 在线</span>
            <span class="view-all">员工详情</span>
          </div>
          <div class="section-body">
            <div class="agent-grid">
              <div v-for="agent in dashboardAgents" :key="agent.id" class="agent-card" @click="router.push('/enterprise/agents')">
                <div class="agent-head">
                  <div class="agent-avatar" :style="{ background: agent.avatarGradient }">{{ agent.avatarChar }}</div>
                  <div class="agent-info">
                    <div class="agent-name">{{ agent.name }}</div>
                    <div class="agent-role">{{ agent.role }}</div>
                  </div>
                  <div class="agent-score" :style="{ color: agent.scoreColor }">{{ agent.score }}</div>
                </div>
                <div class="agent-status">
                  <span class="status-dot" :class="agent.statusClass"></span>
                  <span :style="{ color: agent.statusTextColor }">{{ agent.statusText }}</span>
                </div>
                <div class="agent-stats">
                  <div class="agent-stat">完成 <span>{{ agent.todayDone }}</span></div>
                  <div class="agent-stat">KPI <span :style="{ color: agent.kpiColor }">{{ agent.kpiGrade }}</span></div>
                  <div class="agent-stat">费用 <span>{{ agent.cost }}</span></div>
                  <div class="agent-stat">工具 <span>{{ agent.tools }}</span></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- COST CENTER -->
        <div class="section-card">
          <div class="section-head">
            <span style="font-size:14px">💰</span>
            <h3>费用消耗</h3>
            <span class="sub">本月 ¥{{ totalCost }}</span>
            <span class="view-all">费用详情</span>
          </div>
          <div class="section-body">
            <div style="margin-bottom:14px">
              <div style="display:flex;justify-content:space-between;font-size:11px;color:var(--text3);margin-bottom:6px">
                <span>预算使用率</span>
                <span style="color:var(--text)">{{ budgetUsage }} · 余 ¥{{ budgetRemain }}</span>
              </div>
              <div style="height:6px;background:rgba(255,255,255,0.06);border-radius:3px;overflow:hidden">
                <div :style="{ width: budgetUsage + '%', height: '6px', background: 'linear-gradient(90deg,#3b82f6,#8b5cf6)', borderRadius: '3px' }"></div>
              </div>
            </div>
            <div class="cost-table">
              <div v-for="item in dashboardCosts" :key="item.name" class="cost-row">
                <span class="cost-name">{{ item.icon }} {{ item.name }}</span>
                <div class="cost-bar-wrap">
                  <div class="cost-bar-bg"><div class="cost-bar-fill" :style="{ width: item.width + '%', background: item.color }"></div></div>
                </div>
                <span class="cost-amt">{{ item.amt }}</span>
                <span class="cost-pct">{{ item.pct }}</span>
              </div>
            </div>
            <div style="margin-top:16px;border-top:1px solid var(--border2);padding-top:14px">
              <div style="font-size:11px;color:var(--text3);margin-bottom:10px">🛠 AI工具调用频次（今日）</div>
              <div class="tool-list">
                <div v-for="tool in dashboardTools" :key="tool.name" class="tool-item">
                  <div class="tool-icon" :style="{ background: tool.bg }">{{ tool.icon }}</div>
                  <span class="tool-label">{{ tool.name }}</span>
                  <div class="tool-bar-wrap">
                    <div class="tool-bar-bg"><div class="tool-bar-fill" :style="{ width: tool.barWidth + '%' }"></div></div>
                  </div>
                  <span class="tool-calls">{{ tool.calls }}次</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- BUSINESS RESULTS -->
        <div class="section-card">
          <div class="section-head">
            <span style="font-size:14px">📈</span>
            <h3>业务结果</h3>
            <div class="tabs" style="margin:0;margin-left:4px">
              <div class="tab active">本周</div>
              <div class="tab">本月</div>
            </div>
            <span class="view-all">详细报告</span>
          </div>
          <div class="section-body">
            <div style="display:flex;flex-direction:column;gap:14px">
              <div v-for="(item, i) in dashboardResults" :key="i" class="result-card" :style="{ '--rc': item.rc }">
                <div class="result-title">{{ item.title }}</div>
                <div class="result-big" :style="{ color: item.bigColor }">{{ item.big }}<span v-if="item.unit" class="result-unit">{{ item.unit }}</span></div>
                <div class="result-sub">{{ item.sub }}</div>
                <template v-if="item.showInputOutput">
                  <div class="roi-input-output">
                    <div class="roi-block">
                      <span class="roi-label">投入</span>
                      <span class="roi-amt roi-amount-negative">{{ item.input }}</span>
                    </div>
                    <div class="roi-block">
                      <span class="roi-label">产出</span>
                      <span class="roi-amt roi-amount-positive">{{ item.output }}</span>
                    </div>
                  </div>
                </template>
                <template v-else>
                  <div class="result-chart">
                    <div class="mini-bars">
                      <span v-for="(h, j) in item.bars" :key="j" class="mini-bar" :class="{ active: j >= item.bars.length - 3 }" :style="{ height: h + '%', background: i === 0 ? '#3b82f6' : i === 1 ? '#10b981' : '#8b5cf6' }"></span>
                    </div>
                  </div>
                </template>
                <div class="result-trend">
                  <span v-if="item.trendUp" class="trend-up">↑ {{ item.trend }}</span>
                  <span v-else class="trend-down">↓ {{ item.trend }}</span>
                  <template v-if="item.input">
                    <span style="margin-left:8px;font-size:10px;color:var(--text3)">
                      投入 {{ item.input }} → 产出 {{ item.output }}
                    </span>
                  </template>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

    </div>
  </section>
</template>
<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import KpiCard from "../../../components/KpiCard.vue";
import PageHeader from "../../../components/PageHeader.vue";
import { enterpriseKpis, dashboardWorkflows, dashboardTasks, dashboardAgents, dashboardCosts, dashboardTools, dashboardResults } from "../../../data/mock.js";

const router = useRouter();

const totalCost = computed(() => {
  return dashboardCosts.reduce((sum, c) => sum + parseInt(c.amt.replace(/[¥,]/g, '')), 0).toLocaleString();
});

const budgetUsage = 62;
const budgetRemain = "14,860";
</script>
<style scoped></style>
