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
        <span>设置</span><span>{{ field }}</span><AppToggle v-model="enabled" />
      </article>
    </div>
  </section>
</template>
<script setup>
import { ref, computed } from "vue";
import AppPanel from "./AppPanel.vue";
import AppToggle from "./AppToggle.vue";
import PageHeader from "./PageHeader.vue";
const props = defineProps({ config: { type: Object, required: true } });
const sources = ["外部Agent", "原生模块", "关闭"];
const key = `${props.config.type}-agent-source`;
const source = ref(JSON.parse(localStorage.getItem(key) || '"外部Agent"'));
const enabled = computed({
  get: () => source.value !== "关闭",
  set: (val) => {
    source.value = val ? sources[0] : sources[2];
    localStorage.setItem(key, JSON.stringify(source.value));
  }
});
function setSource(value) {
  source.value = value;
  localStorage.setItem(key, JSON.stringify(value));
}
</script>
<style scoped></style>
