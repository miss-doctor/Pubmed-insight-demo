<script setup>
import { computed } from 'vue'

import ChartCard from '@/components/charts/ChartCard.vue'
import JournalChart from '@/components/charts/JournalChart.vue'
import QuartileChart from '@/components/charts/QuartileChart.vue'
import YearChart from '@/components/charts/YearChart.vue'
import PanelSection from '@/components/common/PanelSection.vue'
import { ZONE_COLORS, ZONE_ORDER } from '@/utils/constants'
import { formatCoverage } from '@/utils/format'

const props = defineProps({
  years: { type: Object, default: () => ({}) },
  quartileCounts: { type: Object, default: () => ({}) },
  zoneCounts: { type: Object, default: () => ({}) },
  journals: { type: Array, default: () => [] },
  stats: { type: Object, default: () => ({}) },
  retrieved: { type: Number, default: 0 },
  metricsMeta: { type: Object, default: () => ({}) }
})

const ifEdition = computed(() => props.metricsMeta.if_edition || 'JCR')
const zoneEdition = computed(() => props.metricsMeta.zone_edition || '中科院分区表')
const matched = computed(() => props.stats.if_matched || 0)
const coverage = computed(() => formatCoverage(props.stats.if_coverage))
</script>

<template>
  <PanelSection
    id="section-stats"
    index="①"
    title="研究数量与年份分布统计"
    subtitle="近5年相关文献的发文量趋势、JCR 分区与中科院分区占比、高产出期刊"
  >
    <div class="chart-grid">
      <ChartCard title="逐年发文量趋势" hint="单位：篇">
        <YearChart :years="years" />
      </ChartCard>
      <ChartCard title="JCR 分区（Q1–Q4）占比" hint="按本次分析文献统计">
        <QuartileChart :counts="quartileCounts" />
      </ChartCard>
      <ChartCard title="中科院大类分区（1–4 区）占比" hint="按本次分析文献统计">
        <QuartileChart
          :counts="zoneCounts"
          :order="ZONE_ORDER"
          :colors="ZONE_COLORS"
        />
      </ChartCard>
      <ChartCard title="高产出期刊 TOP 10" hint="单位：篇">
        <JournalChart :journals="journals" />
      </ChartCard>
    </div>

    <p class="metrics-note">
      影响因子与分区来源：<strong>{{ ifEdition }}</strong> +
      <strong>{{ zoneEdition }}</strong>。
      匹配方式为「PubMed ISSN/EISSN 精确查表」，本次
      {{ retrieved }} 篇文献命中 {{ matched }} 篇（覆盖率
      <strong>{{ coverage }}</strong>）；未收录文献在图中单独计入「未收录」，
      不参与影响因子均值与 TOP100 排序。
    </p>
  </PanelSection>
</template>
