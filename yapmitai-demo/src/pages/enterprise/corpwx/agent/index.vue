<template><ModuleConfigPage :config="config" /></template>
<script setup>
import ModuleConfigPage from "../../../../components/ModuleConfigPage.vue";
const config = { type: "corpwx", title: "AI企微Agent配置", en: "Enterprise WeChat Agent", fields: ["部门归属：海外销售部", "接管模式：全托管", "关键词问答：外部知识库优先", "工单升级：开启"] };
</script>
<style scoped></style>
