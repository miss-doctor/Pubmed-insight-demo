<script setup>
import { onMounted, watch } from 'vue'

import { useChart } from '@/composables/useChart'
import { QUARTILE_COLORS, QUARTILE_ORDER, UNKNOWN_LABEL } from '@/utils/constants'

const props = defineProps({
  /* 分区计数，形如 { Q1: 133, Q2: 23, ... } 或 { '1区': 88, ... } */
  counts: { type: Object, default: () => ({}) },
  /* 图例顺序；不在该集合内的取值一律归入「未收录」 */
  order: { type: Array, default: () => QUARTILE_ORDER },
  /* 分区配色表 */
  colors: { type: Object, default: () => QUARTILE_COLORS },
  /* 悬浮提示中的计数单位 */
  unit: { type: String, default: '篇' }
})

const { canvasRef, draw } = useChart()

function normalize(raw) {
  const counts = { [UNKNOWN_LABEL]: 0 }
  props.order.forEach((key) => {
    counts[key] = 0
  })
  Object.entries(raw || {}).forEach(([key, value]) => {
    if (key in counts) counts[key] += value
    else counts[UNKNOWN_LABEL] += value
  })
  return [...props.order, UNKNOWN_LABEL]
    .filter((key) => counts[key] > 0)
    .map((key) => ({ key, value: counts[key] }))
}

function render() {
  const items = normalize(props.counts)
  draw({
    type: 'doughnut',
    data: {
      labels: items.map((item) => item.key),
      datasets: [
        {
          data: items.map((item) => item.value),
          backgroundColor: items.map((item) => props.colors[item.key] || '#c7d0da'),
          borderWidth: 2,
          borderColor: '#fff',
          hoverOffset: 6
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '58%',
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, padding: 14, font: { size: 12 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const total = ctx.dataset.data.reduce((a, b) => a + b, 0) || 1
              const percent = ((ctx.parsed / total) * 100).toFixed(1)
              return `${ctx.label}: ${ctx.parsed} ${props.unit} (${percent}%)`
            }
          }
        }
      }
    }
  })
}

onMounted(render)
watch(() => props.counts, render, { deep: true })
</script>

<template>
  <div class="chart-canvas-wrap">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>
