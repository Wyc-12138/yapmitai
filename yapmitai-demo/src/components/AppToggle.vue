<template><button class="toggle" :class="{ on: modelValue }" @click="$emit('update:modelValue', !modelValue)"><span></span></button></template>
<script setup>
defineProps({ modelValue: Boolean });
defineEmits(["update:modelValue"]);
</script>
<style scoped></style>
