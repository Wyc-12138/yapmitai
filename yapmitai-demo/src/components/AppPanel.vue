<template>
  <section class="panel">
    <div class="panel-head"><div><h2>{{ title }}</h2><span>{{ subtitle }}</span></div></div>
    <slot />
  </section>
</template>
<script setup>
defineProps({ title: String, subtitle: String });
</script>
<style scoped></style>
