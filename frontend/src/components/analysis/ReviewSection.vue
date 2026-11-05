<script setup>
import { computed } from 'vue'

import PanelSection from '@/components/common/PanelSection.vue'
import { parseReport } from '@/utils/format'

const props = defineProps({
  report: { type: String, default: '' },
  keyword: { type: String, default: '' }
})

const blocks = computed(() => parseReport(props.report))
</script>

<template>
  <PanelSection
    id="section-review"
    index="④"
    title="领域简要综述报告（中文）"
    :subtitle="`基于「${keyword}」相关文献的题录与摘要自动生成，约 500 字`"
  >
    <div class="report-box">
      <template v-for="(block, index) in blocks" :key="index">
        <h2 v-if="block.type === 'heading'" v-html="block.html" />
        <p v-else :class="{ 'report-point': block.type === 'point' }" v-html="block.html" />
      </template>
    </div>
  </PanelSection>
</template>
