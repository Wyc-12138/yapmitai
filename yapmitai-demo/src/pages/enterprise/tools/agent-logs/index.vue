<template>
  <section>
    <PageHeader eyebrow="Agent Call Logs" title="Agent调用日志" description="记录每次Agent调用的模块、状态、耗时与费用。" />
    <div class="page-toolbar"><div class="tabs"><button v-for="item in statuses" :key="item" :class="{ active: filter === item }" @click="filter = item">{{ item }}</button></div><button class="ghost-btn">导出</button></div>
    <div class="table-wrap"><table><thead><tr><th>时间</th><th>Agent名称</th><th>调用模块</th><th>状态</th><th>耗时</th><th>费用</th></tr></thead><tbody><tr v-for="log in visible" :key="log.id"><td>{{ log.time }}</td><td>{{ log.agent }}</td><td>{{ log.module }}</td><td><span class="log-status" :class="log.status">{{ log.status }}</span></td><td>{{ log.latency }}ms</td><td>¥{{ log.cost }}</td></tr></tbody></table></div>
  </section>
</template>
<script setup>
import { computed, ref } from "vue";
import PageHeader from "../../../../components/PageHeader.vue";
import { callLogs } from "../../../../data/mock.js";
const statuses = ["全部", "成功", "失败", "超时"];
const filter = ref("全部");
const visible = computed(() => filter.value === "全部" ? callLogs : callLogs.filter((item) => item.status === filter.value));
</script>
<style scoped></style>
