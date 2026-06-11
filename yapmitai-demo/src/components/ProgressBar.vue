<template>
  <div class="progress" :class="{ slim }">
    <div v-if="label"><span>{{ label }}</span><b>{{ value }}%</b></div>
    <i><span :style="{ width: `${value}%` }"></span></i>
  </div>
</template>
<script setup>
defineProps({ label: { type: String, default: "" }, value: { type: Number, required: true }, slim: Boolean });
</script>
<style scoped></style>
