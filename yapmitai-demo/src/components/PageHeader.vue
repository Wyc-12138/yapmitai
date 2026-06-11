<template>
  <div class="page-title">
    <span class="eyebrow">{{ eyebrow }}</span>
    <h1>{{ title }}</h1>
    <p>{{ description }}</p>
  </div>
</template>
<script setup>
defineProps({ eyebrow: String, title: String, description: String });
</script>
<style scoped></style>
