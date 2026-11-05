<script setup>
import { computed } from 'vue'

import StatCard from '@/components/common/StatCard.vue'
import { formatNumber } from '@/utils/format'

const props = defineProps({
  result: { type: Object, required: true }
})

/** 兼容后端返回的 stats 字段，缺失时按 top_papers 兜底计算。 */
const impactFactors = computed(() => {
  const stats = props.result.stats
  if (stats && (stats.avg_if !== undefined || stats.max_if !== undefined)) {
    return { avg: Number(stats.avg_if || 0), max: Number(stats.max_if || 0) }
  }
  const values = (props.result.top_papers || [])
    .map((paper) => paper.impact_factor)
    .filter((value) => value > 0)
  if (!values.length) return { avg: 0, max: 0 }
  return {
    avg: values.reduce((a, b) => a + b, 0) / values.length,
    max: Math.max(...values)
  }
})

const cards = computed(() => [
  {
    key: 'total',
    icon: '📚',
    tone: 'ic-blue',
    value: formatNumber(props.result.total),
    label: 'PubMed 命中总数'
  },
  {
    key: 'retrieved',
    icon: '📊',
    tone: 'ic-green',
    value: formatNumber(props.result.retrieved),
    label: '本次分析文献数（近5年）'
  },
  {
    key: 'avgIf',
    icon: '📈',
    tone: 'ic-purple',
    value: impactFactors.value.avg.toFixed(1),
    label: '平均影响因子'
  },
  {
    key: 'maxIf',
    icon: '🏆',
    tone: 'ic-orange',
    value: impactFactors.value.max.toFixed(1),
    label: '最高影响因子'
  }
])
</script>

<template>
  <section class="stat-grid">
    <StatCard
      v-for="(card, index) in cards"
      :key="card.key"
      :icon="card.icon"
      :tone="card.tone"
      :value="card.value"
      :label="card.label"
      :delay="index * 70"
    />
  </section>
</template>
