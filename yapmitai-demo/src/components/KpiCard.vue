<template>
  <article class="kpi-card" :style="{ '--accent': item.color }">
    <span>{{ item.title }}</span>
    <strong>{{ item.value }}<small>{{ item.unit }}</small></strong>
    <em>{{ item.trend }}</em>
  </article>
</template>
<script setup>
defineProps({ item: { type: Object, required: true } });
</script>
<style scoped></style>
