<template><ModuleConfigPage :config="config" /></template>
<script setup>
import ModuleConfigPage from "../../../../components/ModuleConfigPage.vue";
const config = { type: "personalwx", title: "AI个微Agent配置", en: "Personal WeChat Agent", fields: ["接管模式：AI建议+人工确认", "关键词问答：合并检索", "SOP群发：限频开启", "客户标签：自动识别"] };
</script>
<style scoped></style>
