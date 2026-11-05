<script setup>
defineProps({
  title: { type: String, required: true },
  hint: { type: String, default: '' },
  wide: { type: Boolean, default: false }
})
</script>

<template>
  <div class="chart-card" :class="{ wide }">
    <div class="chart-card-head">
      <h4>{{ title }}</h4>
      <span v-if="hint" class="chart-hint">{{ hint }}</span>
    </div>
    <slot />
  </div>
</template>
