<template>
  <section>
    <PageHeader :eyebrow="config.en" :title="config.title" description="模块级独立启停，支持外部Agent、原生模块和关闭三种模式。" />
    <AppPanel title="Agent来源" subtitle="Source">
      <div class="segmented">
        <button v-for="item in sources" :key="item" :class="{ active: source === item }" @click="setSource(item)">{{ item }}</button>
      </div>
    </AppPanel>
    <div class="config-list">
      <article v-for="field in config.fields" :key="field" class="config-row">
        <span>设</span><span>{{ field }}</span><AppToggle :model-value="source !== '关闭'" />
      </article>
    </div>
  </section>
</template>
<script setup>
import { ref } from "vue";
import AppPanel from "./AppPanel.vue";
import AppToggle from "./AppToggle.vue";
import PageHeader from "./PageHeader.vue";
const props = defineProps({ config: { type: Object, required: true } });
const sources = ["外部Agent", "原生模块", "关闭"];
const key = `${props.config.type}-agent-source`;
const source = ref(JSON.parse(localStorage.getItem(key) || '"外部Agent"'));
function setSource(value) {
  source.value = value;
  localStorage.setItem(key, JSON.stringify(value));
}
</script>
<style scoped></style>
