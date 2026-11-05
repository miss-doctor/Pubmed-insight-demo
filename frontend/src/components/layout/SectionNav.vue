<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'

const props = defineProps({
  sections: { type: Array, required: true } // [{ id, label }]
})

const activeId = ref(props.sections[0]?.id || '')
let observer = null

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

onMounted(() => {
  observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0]
      if (visible) activeId.value = visible.target.id
    },
    { rootMargin: '-120px 0px -60% 0px', threshold: [0.1, 0.4, 0.8] }
  )
  props.sections.forEach(({ id }) => {
    const el = document.getElementById(id)
    if (el) observer.observe(el)
  })
})

onBeforeUnmount(() => observer?.disconnect())
</script>

<template>
  <nav class="section-nav" aria-label="结果分区导航">
    <div class="container section-nav-inner">
      <button
        v-for="item in sections"
        :key="item.id"
        type="button"
        class="nav-pill"
        :class="{ active: activeId === item.id }"
        @click="scrollTo(item.id)"
      >
        {{ item.label }}
      </button>
    </div>
  </nav>
</template>
