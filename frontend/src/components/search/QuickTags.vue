<script setup>
import { QUICK_TAGS } from '@/utils/constants'

defineProps({
  loading: { type: Boolean, default: false }
})
const emit = defineEmits(['pick'])
</script>

<template>
  <div class="quick-tags">
    <span class="quick-label">热门示例：</span>
    <button
      v-for="tag in QUICK_TAGS"
      :key="tag.keyword"
      type="button"
      class="tag"
      :disabled="loading"
      @click="emit('pick', tag.keyword)"
    >
      {{ tag.label }}
    </button>
  </div>
</template>
