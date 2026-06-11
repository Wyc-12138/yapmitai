<template>
  <section>
    <PageHeader eyebrow="Enterprise AI Dashboard" title="企业AI控制台" description="欢迎回来，李总。今日AI团队已完成 12 项任务。" />
    <div class="enterprise-dashboard-screen">
      <div class="kpi-grid"><KpiCard v-for="item in enterpriseKpis" :key="item.title" :item="item" /></div>
      <div class="dashboard-grid">
        <AppPanel title="销售趋势" subtitle="Sales vs AI Contribution"><LineChart :data="salesTrend" a-key="sales" b-key="ai" a-label="总销售额" b-label="AI贡献" /></AppPanel>
        <AppPanel title="AI员工任务分布" subtitle="Agent Workload"><DonutChart :data="moduleDistribution" /></AppPanel>
      </div>
      <div class="dashboard-grid wide-left">
        <AppPanel title="今日任务队列" subtitle="Today's Task Queue">
          <div class="task-list">
            <article v-for="task in tasks" :key="task.id" class="task-row">
              <div><strong>{{ task.task }}</strong><span>{{ task.agent }}</span></div>
              <span class="task-status" :class="task.status">{{ task.status }}</span>
              <ProgressBar :value="task.progress" slim />
            </article>
          </div>
        </AppPanel>
        <AppPanel title="第三方Agent调用统计" subtitle="Gateway Stats">
          <div class="mini-stat-grid"><div v-for="item in stats" :key="item.label" class="mini-stat"><span>{{ item.label }}</span><strong>{{ item.value }}</strong></div></div>
          <LineChart :data="trend7d" a-key="calls" b-key="success" a-label="调用量" b-label="成功数" compact />
          <button class="primary-btn full" @click="router.push('/enterprise/tools/agent-logs')">查看调用日志</button>
        </AppPanel>
      </div>
    </div>
  </section>
</template>
<script setup>
import { useRouter } from "vue-router";
import AppPanel from "../../../components/AppPanel.vue";
import DonutChart from "../../../components/DonutChart.vue";
import KpiCard from "../../../components/KpiCard.vue";
import LineChart from "../../../components/LineChart.vue";
import PageHeader from "../../../components/PageHeader.vue";
import ProgressBar from "../../../components/ProgressBar.vue";
import { enterpriseKpis, moduleDistribution, salesTrend, tasks, trend7d } from "../../../data/mock.js";
const router = useRouter();
const stats = [{ label: "今日调用", value: "1,248" }, { label: "成功率", value: "98.6%" }, { label: "平均响应", value: "1.28s" }, { label: "本月费用", value: "¥8,420" }];
</script>
<style scoped></style>
