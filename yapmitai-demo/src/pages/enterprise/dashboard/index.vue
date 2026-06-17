<template>
  <section>
    <PageHeader eyebrow="Dashboard · Overview" title="今日企业全景" description="海南澄迈品牌有限公司 · 所有AI员工运行中 · 上次更新 2分钟前" />
    <div class="enterprise-dashboard-screen">
      <!-- Alert strip -->
      <div class="dashboard-alert">
        <span>⚠️</span>
        <span>AI跨境运营经理 有 <strong>2</strong> 项任务待确认分配，投流预算剩余不足72小时</span>
        <button class="ghost-btn tiny-btn" @click="router.push('/enterprise/agents')">立即处理 →</button>
      </div>

      <!-- KPI row: 5 cards -->
      <div class="kpi-grid"><KpiCard v-for="item in enterpriseKpis" :key="item.title" :item="item" /></div>

      <!-- TWO COL: Workflow + Tasks -->
      <div class="dashboard-grid wide-left">
        <AppPanel title="工作流进展" subtitle="今日活跃 {{ dashboardWorkflows.length }} 条">
          <div class="workflow-steps">
            <div v-for="wf in dashboardWorkflows" :key="wf.id" class="wf-step">
              <span class="wf-num" :class="wf.status">{{ wf.id }}</span>
              <div class="wf-info">
                <div class="wf-name">{{ wf.name }}</div>
                <div class="wf-detail">{{ wf.detail }}</div>
                <div class="wf-agent">→ {{ wf.agent }}</div>
              </div>
              <div class="wf-progress-col">
                <ProgressBar :value="wf.progress" slim />
                <span class="wf-pct" :class="wf.status">{{ wf.progress }}%</span>
              </div>
            </div>
          </div>
        </AppPanel>

        <AppPanel title="今日任务队列" subtitle="Today's Task Queue">
          <div class="task-list">
            <article v-for="task in dashboardTasks" :key="task.id" class="task-row">
              <div>
                <strong>{{ task.title }}</strong>
                <span>{{ task.agent }}</span>
                <span class="task-tag" :class="task.tagClass">{{ task.tag }}</span>
              </div>
              <span class="task-status" :class="task.status">{{ task.status === 'done' ? '已完成' : task.status === 'running' ? '进行中' : '待处理' }}</span>
              <ProgressBar :value="task.progress" slim />
            </article>
          </div>
        </AppPanel>
      </div>

      <!-- THREE COL: AI agent scorecards -->
      <div class="three-col">
        <div v-for="agent in dashboardAgents" :key="agent.id" class="agent-card">
          <div class="agent-head">
            <div class="agent-avatar">{{ agent.name.slice(2, 3) }}</div>
            <div class="agent-info">
              <div class="agent-name">{{ agent.name }}</div>
              <div class="agent-role">{{ agent.role }}</div>
            </div>
            <div class="agent-score">{{ agent.score }}</div>
          </div>
          <div class="agent-status">
            <span class="status-dot running"></span> 运行中
          </div>
          <div class="agent-stats">
            <div class="agent-stat">今日完成 <span>{{ agent.todayDone }}</span></div>
            <div class="agent-stat">本月总计 <span>{{ agent.monthTotal }}</span></div>
            <div class="agent-stat">满意度 <span>{{ agent.satisfaction }}</span></div>
          </div>
        </div>
      </div>

      <!-- TWO COL: Cost + Results -->
      <div class="dashboard-grid wide-left">
        <AppPanel title="本月费用分布" subtitle="Cost Breakdown">
          <div class="cost-table">
            <div v-for="item in dashboardCosts" :key="item.name" class="cost-row">
              <span class="cost-name">{{ item.name }}</span>
              <span class="cost-bar-wrap"><span class="cost-bar-bg"><span class="cost-bar-fill" :style="{ width: item.width + '%', background: item.color }"></span></span></span>
              <span class="cost-amt">{{ item.amt }}</span>
              <span class="cost-pct">{{ item.pct }}</span>
            </div>
          </div>
        </AppPanel>

        <AppPanel title="AI生成结果概览" subtitle="本周产出">
          <div class="result-grid">
            <div v-for="(item, i) in dashboardResults" :key="i" class="result-card">
              <div class="result-title">{{ item.title }}</div>
              <div class="result-big">{{ item.big }}</div>
              <div class="result-sub">{{ item.sub }}</div>
              <div class="result-chart">
                <div class="mini-bars">
                  <span v-for="(h, j) in item.bars" :key="j" class="mini-bar" :class="{ active: j >= item.bars.length - 3 }" :style="{ height: h + '%', background: i === 0 ? '#3b82f6' : i === 1 ? '#10b981' : '#8b5cf6' }"></span>
                </div>
              </div>
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
        </AppPanel>
      </div>

      <!-- Tool usage -->
      <AppPanel title="AI工具使用排行" subtitle="本月调用">
        <div class="tool-list">
          <div v-for="tool in dashboardTools" :key="tool.name" class="tool-item">
            <span class="tool-icon-dash" :style="{ background: tool.bg }">{{ tool.icon }}</span>
            <span class="tool-label">{{ tool.name }}</span>
            <span class="tool-calls">{{ tool.calls }} 次</span>
            <span class="tool-bar-wrap"><span class="tool-bar-bg"><span class="tool-bar-fill" :style="{ width: tool.barWidth + '%' }"></span></span></span>
          </div>
        </div>
      </AppPanel>
    </div>
  </section>
</template>
<script setup>
import { useRouter } from "vue-router";
import AppPanel from "../../../components/AppPanel.vue";
import KpiCard from "../../../components/KpiCard.vue";
import PageHeader from "../../../components/PageHeader.vue";
import ProgressBar from "../../../components/ProgressBar.vue";
import { enterpriseKpis, dashboardWorkflows, dashboardTasks, dashboardAgents, dashboardCosts, dashboardTools, dashboardResults } from "../../../data/mock.js";
const router = useRouter();
</script>
<style scoped></style>
