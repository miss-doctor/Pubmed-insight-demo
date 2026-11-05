<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const visible = ref(false)

function onScroll() {
  visible.value = window.scrollY > 600
}

function toTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onBeforeUnmount(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <transition name="fade-up">
    <button v-show="visible" type="button" class="back-to-top" title="回到顶部" @click="toTop">
      ↑
    </button>
  </transition>
</template>
