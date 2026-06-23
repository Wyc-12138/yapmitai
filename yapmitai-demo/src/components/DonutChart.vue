<template>
  <div class="donut-wrap">
    <div class="donut" :style="{ background: gradient }"><span>{{ total }}</span></div>
    <div class="donut-list">
      <span v-for="item in data" :key="item.label"><i :style="{ background: item.color }"></i>{{ item.label }} {{ item.value }}%</span>
    </div>
  </div>
</template>
<script setup>
import { computed } from "vue";
const props = defineProps({ data: { type: Array, required: true } });
const total = computed(() => props.data.reduce((sum, item) => sum + item.value, 0));
const gradient = computed(() => {
  if (!props.data?.length || !total.value) return 'conic-gradient(#333 0% 100%)';
  let start = 0;
  return `conic-gradient(${props.data.map((item) => {
    const end = start + item.value / total.value * 100;
    const segment = `${item.color} ${start}% ${end}%`;
    start = end;
    return segment;
  }).join(", ")})`;
});
</script>
<style scoped></style>
