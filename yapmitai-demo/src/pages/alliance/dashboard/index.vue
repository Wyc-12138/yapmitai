<template>
  <section>
    <PageHeader eyebrow="Alliance Management Center" title="产业联盟管理中心" description="展示联盟成员网络与100家品牌AI增长计划。" />
    <div class="kpi-grid three"><KpiCard v-for="item in kpis" :key="item.title" :item="item" /></div>
    <div class="dashboard-grid">
      <AppPanel title="AI增长计划" subtitle="Growth Programs">
        <div class="plan-list"><article v-for="plan in alliancePlans" :key="plan.name" class="plan-card"><div><strong>{{ plan.name }}</strong><span>{{ plan.status }}</span></div><ProgressBar :label="`${plan.current}/${plan.target}家`" :value="Math.round(plan.current / plan.target * 100)" /></article></div>
      </AppPanel>
      <AppPanel title="联盟成员列表" subtitle="Members">
        <div class="member-list"><div v-for="member in allianceMembers" :key="member.name" class="member-row"><span>企</span><div><strong>{{ member.name }}</strong><span>{{ member.type }} · {{ member.level }}</span></div><span class="log-status 成功">{{ member.status }}</span></div></div>
      </AppPanel>
    </div>
  </section>
</template>
<script setup>
import AppPanel from "../../../components/AppPanel.vue";
import KpiCard from "../../../components/KpiCard.vue";
import PageHeader from "../../../components/PageHeader.vue";
import ProgressBar from "../../../components/ProgressBar.vue";
import { allianceMembers, alliancePlans } from "../../../data/mock.js";
const kpis = [{ title: "成员企业数", value: "128", unit: "家", trend: "+16", color: "#00C9A7" }, { title: "活跃企业", value: "96", unit: "家", trend: "+12%", color: "#4361EE" }, { title: "总GMV", value: "12.4", unit: "亿元", trend: "+18%", color: "#F72585" }];
</script>
<style scoped></style>
