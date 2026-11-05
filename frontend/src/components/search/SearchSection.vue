<script setup>
import QuickTags from './QuickTags.vue'
import SearchBar from './SearchBar.vue'

defineProps({
  keyword: { type: String, default: '' },
  loading: { type: Boolean, default: false }
})
const emit = defineEmits(['update:keyword', 'submit'])
</script>

<template>
  <section class="search-section">
    <div class="container">
      <div class="search-hero">
        <SearchBar
          :model-value="keyword"
          :loading="loading"
          @update:model-value="emit('update:keyword', $event)"
          @submit="emit('submit')"
        />
        <QuickTags :loading="loading" @pick="emit('submit', $event)" />
      </div>
    </div>
  </section>
</template>