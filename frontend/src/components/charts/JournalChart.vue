<script setup>
import { onMounted, watch } from 'vue'

import { useChart } from '@/composables/useChart'

const props = defineProps({
  journals: { type: Array, default: () => [] }
})

const { canvasRef, draw } = useChart()

function render() {
  const list = props.journals || []
  const labels = list.map((item) =>
    item.journal.length > 34 ? `${item.journal.slice(0, 32)}…` : item.journal
  )
  draw({
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: '发文量（篇）',
          data: list.map((item) => item.count),
          backgroundColor: 'rgba(0, 168, 168, .78)',
          hoverBackgroundColor: 'rgba(0, 140, 140, .95)',
          borderRadius: 6,
          maxBarThickness: 24
        }
      ]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: false,
      animation: { duration: 600 },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            title: (items) => list[items[0].dataIndex]?.journal || items[0].label
          }
        }
      },
      scales: {
        x: { beginAtZero: true, ticks: { precision: 0 }, grid: { color: '#eef2f8' } },
        y: { grid: { display: false }, ticks: { font: { size: 11 } } }
      }
    }
  })
}

onMounted(render)
watch(() => props.journals, render, { deep: true })
</script>

<template>
  <div class="chart-canvas-wrap chart-canvas-tall">
    <canvas ref="canvasRef"></canvas>
  </div>
</template>
