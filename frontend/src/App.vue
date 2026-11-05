<script setup>
import { computed } from 'vue'

import SearchSection from '@/components/search/SearchSection.vue'
import SiteHeader from '@/components/layout/SiteHeader.vue'
import PageFooter from '@/components/layout/PageFooter.vue'
import SectionNav from '@/components/layout/SectionNav.vue'
import BackToTop from '@/components/layout/BackToTop.vue'
import LoadingState from '@/components/common/LoadingState.vue'
import ErrorAlert from '@/components/common/ErrorAlert.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import ResultHeader from '@/components/analysis/ResultHeader.vue'
import StatGrid from '@/components/analysis/StatGrid.vue'
import StatsSection from '@/components/analysis/StatsSection.vue'
import TopicsSection from '@/components/analysis/TopicsSection.vue'
import TopPapersSection from '@/components/analysis/TopPapersSection.vue'
import ReviewSection from '@/components/analysis/ReviewSection.vue'
import { useSearch } from '@/composables/useSearch'

const {
  keyword,
  status,
  errorMessage,
  result,
  elapsedSeconds,
  isLoading,
  hasResult,
  search
} = useSearch()

const NAV_SECTIONS = [
  { id: 'section-stats', label: '① 统计与图表' },
  { id: 'section-topics', label: '② 词云与方向' },
  { id: 'section-papers', label: '③ 影响力 TOP100' },
  { id: 'section-review', label: '④ 中文综述' }
]

const quartileCounts = computed(() => result.value?.stats?.q_counts || {})
const zoneCounts = computed(() => result.value?.stats?.zone_counts || {})
const stats = computed(() => result.value?.stats || {})
const metricsMeta = computed(() => result.value?.metrics_meta || {})
const retrieved = computed(() => result.value?.retrieved || 0)
</script>

<template>
  <SiteHeader />

  <SearchSection
    v-model:keyword="keyword"
    :loading="isLoading"
    @submit="search"
  />

  <LoadingState :visible="isLoading" :keyword="keyword" />

  <ErrorAlert
    v-if="status === 'error'"
    :message="errorMessage"
    @retry="search()"
  />

  <EmptyState v-if="status === 'empty'" :keyword="keyword" />

  <template v-if="hasResult">
    <SectionNav :sections="NAV_SECTIONS" />

    <main class="container results">
      <ResultHeader
        :keyword="result.keyword"
        :source-url="result.source_url"
        :from-cache="!!result.from_cache"
        :elapsed-seconds="elapsedSeconds"
      />

      <StatGrid :result="result" />

      <StatsSection
        :years="result.years"
        :quartile-counts="quartileCounts"
        :zone-counts="zoneCounts"
        :journals="result.journals"
        :stats="stats"
        :retrieved="retrieved"
        :metrics-meta="metricsMeta"
      />

      <TopicsSection :wordcloud="result.wordcloud" :directions="result.directions" />

      <TopPapersSection :papers="result.top_papers" />

      <ReviewSection :report="result.report" :keyword="result.keyword" />

      <PageFooter />
    </main>
  </template>

  <BackToTop />
</template>
