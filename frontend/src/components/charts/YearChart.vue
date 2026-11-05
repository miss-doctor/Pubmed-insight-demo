<script setup>
import { onMounted, watch } from 'vue'

import { useChart } from '@/composables/useChart'

const props = defineProps({
  years: { type: Object, default: () => ({}) }
})

const { canvasRef, draw } = useChart()

function render() {
  const labels = Object.keys(props.years || {})
  const values = labels.map((year) => props.years[year])
  draw({
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: '发文量（篇）',
          data: values,
          backgroundColor: 'rgba(31, 111, 235, .78)',
          hoverBackgroundColor: 'rgba(21, 88, 192, .95)',
          borderRadius: 6,
          maxBarThickness: 46
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 600 },
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#eef2f8' } },
        x: { grid: { display: false } }
      }
    }
  })
}

onMounted(render)
watch(() => props.years, render, { deep: true })
</script>

<template>
  <div class="chart-canvas-wrap">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>
