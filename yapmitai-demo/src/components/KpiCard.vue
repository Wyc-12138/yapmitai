<template>
  <div class="kpi-card" :style="{ '--kpi-color': item.color }">
    <span class="kpi-bar"></span>
    <span class="kpi-label">{{ item.title }}</span>
    <div class="kpi-value">
      <strong>{{ item.value }}</strong><span class="kpi-unit">{{ item.unit }}</span>
    </div>
    <div class="kpi-delta" :class="item.deltaClass">{{ item.delta }}</div>
    <span class="kpi-icon">{{ item.icon }}</span>
  </div>
</template>
<script setup>
defineProps({ item: { type: Object, required: true } });
</script>
<style scoped>
.kpi-card {
  position: relative;
}
.kpi-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--kpi-color, var(--accent)), transparent);
}
</style>
