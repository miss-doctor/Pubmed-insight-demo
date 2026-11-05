<script setup>
defineProps({
  directions: { type: Array, default: () => [] }
})
</script>

<template>
  <ul class="direction-list">
    <li v-for="(item, index) in directions" :key="item.theme">
      <span class="direction-name">
        <span class="rank">{{ index + 1 }}</span>{{ item.theme }}
      </span>
      <span class="dc">{{ item.count }} 次</span>
    </li>
    <li v-if="!directions.length" class="direction-empty">暂无研究方向数据</li>
  </ul>
</template>
