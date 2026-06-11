<template>
  <RouterView v-if="route.meta.layout === 'full'" />
  <AppShell v-else>
    <RouterView />
  </AppShell>
</template>

<script setup>
import { RouterView, useRoute } from "vue-router";
import AppShell from "./layouts/AppShell.vue";

const route = useRoute();
</script>

<style scoped>
</style>
