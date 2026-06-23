<template>
  <div class="chart-box" :class="{ compact }">
    <svg viewBox="0 0 100 100" preserveAspectRatio="none">
      <line v-for="y in [20, 40, 60, 80]" :key="y" x1="0" x2="100" :y1="y" :y2="y" />
      <polyline :points="points(aKey)" class="line-a" />
      <polyline :points="points(bKey)" class="line-b" />
    </svg>
    <div class="chart-legend"><span class="dot a"></span>{{ aLabel }}<span class="dot b"></span>{{ bLabel }}</div>
  </div>
</template>
<script setup>
import { computed } from "vue";
const props = defineProps({
  data: { type: Array, required: true }, aKey: String, bKey: String,
  aLabel: String, bLabel: String, compact: Boolean
});
const max = computed(() => {
  const values = props.data.flatMap((item) => [item[props.aKey], item[props.bKey]]).filter(v => v != null);
  return values.length ? Math.max(...values) : 1;
});
function points(key) {
  if (props.data.length < 2) return "0,100 100,100";
  return props.data.map((item, index) =>
    `${index * (100 / (props.data.length - 1))},${100 - item[key] / max.value * 86}`
  ).join(" ");
}
</script>
<style scoped></style>
