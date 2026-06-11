<template>
  <section>
    <PageHeader eyebrow="Talent Workspace" title="员工工作台" description="面向职工的AI协作入口。" />
    <div class="dashboard-grid">
      <AppPanel title="今日AI助手" subtitle="Assistants">
        <div class="config-list flat"><div v-for="item in assistants" :key="item" class="config-row"><span>AI</span><span>{{ item }}</span><button class="tiny-btn">打开</button></div></div>
      </AppPanel>
      <AppPanel title="成长指数" subtitle="Growth Index">
        <div class="mini-stat"><span>本周完成任务</span><strong>18</strong></div>
        <div class="mini-stat"><span>AI节省时间</span><strong>7.5h</strong></div>
      </AppPanel>
    </div>
  </section>
</template>
<script setup>
import AppPanel from "../../../components/AppPanel.vue";
import PageHeader from "../../../components/PageHeader.vue";
const assistants = ["简历优化助手", "技能学习助手", "任务总结助手", "政策咨询助手"];
</script>
<style scoped></style>
