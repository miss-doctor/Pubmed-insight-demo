<script setup>
const props = defineProps({
  modelValue: { type: String, default: '' },
  loading: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue', 'submit'])

function onInput(event) {
  emit('update:modelValue', event.target.value)
}

function onSubmit() {
  if (!props.loading) emit('submit')
}
</script>

<template>
  <form class="search-box" autocomplete="off" @submit.prevent="onSubmit">
    <div class="search-input-wrap">
      <svg class="search-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true">
        <path
          fill="currentColor"
          d="M15.5 14h-.79l-.28-.27A6.47 6.47 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
        />
      </svg>
      <input
        type="text"
        :value="modelValue"
        placeholder="请输入研究关键词，例如：CAR-T therapy、diabetes、lung cancer …"
        aria-label="研究关键词"
        required
        @input="onInput"
      >
    </div>
    <button type="submit" class="btn-primary" :disabled="loading">
      <span v-if="loading" class="btn-spinner" aria-hidden="true"></span>
      {{ loading ? '检索中…' : '开始检索' }}
    </button>
  </form>
</template>
