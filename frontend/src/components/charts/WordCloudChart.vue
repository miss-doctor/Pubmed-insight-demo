<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import * as WordCloudModule from 'wordcloud'

import { WORDCLOUD_PALETTE } from '@/utils/constants'

// wordcloud2.js 是 UMD 包，兼容 default / 命名导出两种形态
const WordCloud = WordCloudModule.default || WordCloudModule

const props = defineProps({
  words: { type: Array, default: () => [] }
})

const containerRef = ref(null)
const hasWords = computed(() => Array.isArray(props.words) && props.words.length > 0)

function render() {
  const el = containerRef.value
  if (!el) return
  el.innerHTML = ''

  if (!hasWords.value || typeof WordCloud !== 'function') {
    el.innerHTML = '<p class="chart-empty">暂无词云数据</p>'
    return
  }

  const width = el.clientWidth || 520
  const height = el.clientHeight || 320
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height
  el.appendChild(canvas)

  const palette = WORDCLOUD_PALETTE
  const list = props.words.map((word, index) => [
    word.name,
    word.value,
    palette[index % palette.length]
  ])
  const colorMap = new Map(list.map((item) => [item[0], item[2]]))

  try {
    WordCloud(canvas, {
      list,
      gridSize: 10,
      weightFactor: (value) => Math.max(14, Math.sqrt(value) * 5),
      fontFamily: 'Segoe UI, PingFang SC, Microsoft YaHei, sans-serif',
      color: (word) => colorMap.get(word) || palette[0],
      rotateRatio: 0.25,
      rotationSteps: 2,
      backgroundColor: '#f7faff',
      drawOutOfBound: false
      // 注意：不要开启 shrinkToFit —— 它会递归缩小 weight，
      // 而 weightFactor 存在最小字号下限，会让递归无法收敛（栈溢出）。
    })
  } catch (err) {
    el.innerHTML = '<p class="chart-empty">词云渲染失败</p>'
  }
}

onMounted(() => nextTick(render))
watch(() => props.words, () => nextTick(render), { deep: true })
</script>

<template>
  <div ref="containerRef" class="wordcloud-canvas"></div>
</template>
