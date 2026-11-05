<script setup>
defineProps({
  message: { type: String, default: '' }
})
const emit = defineEmits(['retry'])
</script>

<template>
  <div class="container state-wrap">
    <div class="alert-error">
      <div class="alert-body">
        <strong>检索失败</strong>
        <p>{{ message }}</p>
      </div>
      <button type="button" class="btn-ghost" @click="emit('retry')">重试</button>
    </div>
  </div>
</template>
