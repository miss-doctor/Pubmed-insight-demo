<script setup>
import { computed } from 'vue'

import { PROGRESS_STEPS } from '@/utils/constants'
import { useElapsedProgress } from '@/composables/useElapsedProgress'

const props = defineProps({
  visible: { type: Boolean, default: false },
  keyword: { type: String, default: '' }
})

const { stepIndex, elapsed } = useElapsedProgress(computed(() => props.visible))
</script>

<template>
  <transition name="fade">
    <div v-if="visible" class="container state-wrap">
      <div class="loading-card">
        <div class="spinner"></div>
        <p class="loading-title">
          正在检索并分析「{{ keyword }}」
        </p>
        <ul class="progress-steps">
          <li
            v-for="(step, index) in PROGRESS_STEPS"
            :key="step"
            :class="{ done: index < stepIndex, active: index === stepIndex }"
          >
            <span class="dot"></span>{{ step }}
          </li>
        </ul>
        <p class="loading-hint">
          首次检索需实时抓取 PubMed 数据，通常 10~60 秒；已检索过的关键词会命中本地缓存，秒级返回。
          <strong v-if="elapsed > 3">已等待 {{ elapsed }} 秒</strong>
        </p>
      </div>
    </div>
  </transition>
</template>
