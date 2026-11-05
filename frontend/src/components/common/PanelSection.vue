<script setup>
defineProps({
  id: { type: String, default: undefined },
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  index: { type: String, default: '' },
  collapsible: { type: Boolean, default: false }
})
</script>

<template>
  <section :id="id" class="panel">
    <div class="panel-head">
      <div>
        <h3>
          <span v-if="index" class="panel-index">{{ index }}</span>
          {{ title }}
        </h3>
        <p v-if="subtitle" class="panel-sub">{{ subtitle }}</p>
      </div>
      <div v-if="$slots.actions" class="panel-actions">
        <slot name="actions" />
      </div>
    </div>
    <slot />
  </section>
</template>
