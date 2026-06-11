<template>
  <div class="gov-screen gov-dashboard-screen">
    <header class="gov-header"><button class="ghost-btn" @click="router.push('/')">返回首页</button><div><h1>海南自贸港 · 产业AI驾驶舱</h1><span>Hainan FTP · Industrial AI Decision Dashboard</span></div><time>{{ now }}</time></header>
    <div class="gov-kpi-grid"><KpiCard v-for="item in govKpis" :key="item.title" :item="item" /></div>
    <div class="gov-grid">
      <AppPanel title="产业活跃度" subtitle="30-Day Activity"><LineChart :data="trend7d" a-key="calls" b-key="success" a-label="产业活跃" b-label="AI贡献" /></AppPanel>
      <AppPanel title="企业类型分布" subtitle="Enterprise Distribution"><DonutChart :data="moduleDistribution" /></AppPanel>
      <AppPanel title="AI政策问答助手" subtitle="Policy Assistant"><div class="assistant-box"><span class="tool-icon">策</span><strong>永不落幕消博会政策助手</strong><p>可查询自贸港税收政策、品牌出海补贴、企业入驻流程。</p><button class="primary-btn full">打开助手</button></div></AppPanel>
    </div>
  </div>
</template>
<script setup>
import { useRouter } from "vue-router";
import AppPanel from "../../../components/AppPanel.vue";
import DonutChart from "../../../components/DonutChart.vue";
import KpiCard from "../../../components/KpiCard.vue";
import LineChart from "../../../components/LineChart.vue";
import { govKpis, moduleDistribution, trend7d } from "../../../data/mock.js";
const router = useRouter();
const now = new Date().toLocaleString("zh-CN", { hour12: false });
</script>
<style scoped></style>
