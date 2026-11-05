<script setup>
import ChartCard from '@/components/charts/ChartCard.vue'
import WordCloudChart from '@/components/charts/WordCloudChart.vue'
import PanelSection from '@/components/common/PanelSection.vue'
import DirectionList from './DirectionList.vue'

defineProps({
  wordcloud: { type: Array, default: () => [] },
  directions: { type: Array, default: () => [] }
})
</script>

<template>
  <PanelSection
    id="section-topics"
    index="②"
    title="研究词云与方向总结"
    subtitle="基于标题与摘要的高频主题词挖掘，字号越大代表出现频次越高"
  >
    <div class="wordcloud-grid">
      <ChartCard title="关键词词云" :hint="`共 ${wordcloud.length} 个高频词`">
        <WordCloudChart :words="wordcloud" />
      </ChartCard>
      <ChartCard title="主要研究方向概括" hint="按出现频次排序">
        <DirectionList :directions="directions" />
      </ChartCard>
    </div>
  </PanelSection>
</template>
