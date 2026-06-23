<template>
  <section class="panel">
    <div class="panel-head"><div><h2>{{ title }}</h2><span>{{ subtitle }}</span></div></div>
    <div class="panel-body"><slot /></div>
  </section>
</template>
<script setup>
defineProps({ title: String, subtitle: String });
</script>
<style scoped></style>
