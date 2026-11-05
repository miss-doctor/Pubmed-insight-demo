<script setup>
defineProps({
  keyword: { type: String, default: '' }
})
</script>

<template>
  <div class="container state-wrap">
    <div class="empty-inner">
      <div class="empty-icon">🔍</div>
      <h3>未检索到「{{ keyword }}」的相关文献</h3>
      <p>请尝试更换关键词，或放宽检索条件（例如使用更通用的主题词）。</p>
    </div>
  </div>
</template>
