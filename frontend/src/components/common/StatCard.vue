<script setup>
defineProps({
  value: { type: [String, Number], required: true },
  label: { type: String, required: true },
  icon: { type: String, default: '📄' },
  tone: { type: String, default: 'ic-blue' },
  delay: { type: Number, default: 0 }
})
</script>

<template>
  <div class="stat-card" :style="{ animationDelay: `${delay}ms` }">
    <div class="stat-icon" :class="tone">{{ icon }}</div>
    <div class="stat-meta">
      <span class="stat-value">{{ value }}</span>
      <span class="stat-label" :title="label">{{ label }}</span>
    </div>
  </div>
</template>
