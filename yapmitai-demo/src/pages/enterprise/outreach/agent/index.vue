<template><ModuleConfigPage :config="config" /></template>
<script setup>
import ModuleConfigPage from "../../../../components/ModuleConfigPage.vue";
const config = { type: "outreach", title: "AI拓客模块配置", en: "Outreach Agent Config", fields: ["目标行业：跨境电商 / 消费品牌 / 制造业", "地区：海南 / 东南亚 / 北美", "外呼频率上限：80通/日", "合规声明：已勾选"] };
</script>
<style scoped></style>
