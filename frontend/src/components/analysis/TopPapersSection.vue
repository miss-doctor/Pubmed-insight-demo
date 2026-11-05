<script setup>
import { computed, ref, watch } from 'vue'

import PanelSection from '@/components/common/PanelSection.vue'
import { EXCLUDE_TYPES } from '@/utils/constants'
import { escapeHtml, formatImpactFactor, quartileClass } from '@/utils/format'

const props = defineProps({
  papers: { type: Array, default: () => [] }
})

const query = ref('')
const onlyResearch = ref(true)
const sortKey = ref('default') // default | impact_factor | year
const sortDesc = ref(true)

/* 换关键词后重置筛选条件 */
watch(
  () => props.papers,
  () => {
    query.value = ''
    sortKey.value = 'default'
    sortDesc.value = true
  }
)

const filtered = computed(() => {
  const keyword = query.value.trim().toLowerCase()
  let list = props.papers || []

  if (onlyResearch.value) {
    list = list.filter((paper) => !EXCLUDE_TYPES.includes(paper.pub_type))
  }
  if (keyword) {
    list = list.filter(
      (paper) =>
        (paper.title || '').toLowerCase().includes(keyword) ||
        (paper.journal || '').toLowerCase().includes(keyword) ||
        (paper.authors || []).join(' ').toLowerCase().includes(keyword)
    )
  }

  if (sortKey.value !== 'default') {
    const key = sortKey.value
    list = [...list].sort((a, b) => {
      const diff = (a[key] || 0) - (b[key] || 0)
      return sortDesc.value ? -diff : diff
    })
  }
  return list
})

/* 原始排名（影响力降序）作为 # 列，排序后仍可看出原始位次 */
const rankMap = computed(() => {
  const map = new Map()
  ;(props.papers || []).forEach((paper, index) => map.set(paper.pmid, index + 1))
  return map
})

function toggleSort(key) {
  if (sortKey.value === key) {
    sortDesc.value = !sortDesc.value
  } else {
    sortKey.value = key
    sortDesc.value = true
  }
}

function sortIndicator(key) {
  if (sortKey.value !== key) return '↕'
  return sortDesc.value ? '↓' : '↑'
}
</script>

<template>
  <PanelSection
    id="section-papers"
    index="③"
    title="影响力排序（近5年影响因子 TOP 100）"
    subtitle="按 JCR 影响因子降序排列，同时给出 JCR 分区与中科院大类分区"
  >
    <div class="table-tools">
      <input v-model="query" type="text" placeholder="在结果中筛选标题 / 期刊 / 作者…">
      <label class="filter-check">
        <input v-model="onlyResearch" type="checkbox">
        仅研究论文 / 综述
      </label>
      <span class="table-count">共 {{ filtered.length }} 篇</span>
    </div>

    <div class="table-scroll">
      <table class="paper-table">
        <thead>
          <tr>
            <th style="width:56px">#</th>
            <th>标题</th>
            <th style="width:200px">期刊</th>
            <th style="width:72px">JCR</th>
            <th style="width:76px">中科院</th>
            <th style="width:100px">
              <button type="button" class="th-sort" @click="toggleSort('impact_factor')">
                影响因子 <span class="sort-ind">{{ sortIndicator('impact_factor') }}</span>
              </button>
            </th>
            <th style="width:80px">
              <button type="button" class="th-sort" @click="toggleSort('year')">
                年份 <span class="sort-ind">{{ sortIndicator('year') }}</span>
              </button>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="paper in filtered" :key="paper.pmid">
            <td class="rank-cell">{{ rankMap.get(paper.pmid) }}</td>
            <td>
              <a class="paper-title" :href="paper.url" target="_blank" rel="noopener">
                {{ paper.title || '(无标题)' }}
              </a>
              <div class="paper-meta">
                <span class="ptype-tag">{{ paper.pub_type || '研究论文' }}</span>
                <span v-html="escapeHtml((paper.authors || []).join(', '))" />
                <template v-if="paper.authors && paper.authors.length"> 等</template>
              </div>
            </td>
            <td>{{ paper.journal || '-' }}</td>
            <td>
              <span class="q-pill" :class="quartileClass(paper.quartile)">
                {{ paper.quartile || '未收录' }}
              </span>
            </td>
            <td>
              <span
                class="q-pill"
                :class="quartileClass(paper.zone_label)"
                :title="paper.zone_name ? `${paper.zone_name} ${paper.zone_label || ''}` : ''"
              >
                {{ paper.zone_label || '未收录' }}
              </span>
            </td>
            <td><span class="if-badge">{{ formatImpactFactor(paper.impact_factor) }}</span></td>
            <td>{{ paper.year || '-' }}</td>
          </tr>
        </tbody>
      </table>

      <p v-if="!filtered.length" class="table-empty">
        没有符合当前筛选条件的文献，试试清空搜索框或取消「仅研究论文 / 综述」。
      </p>
    </div>
  </PanelSection>
</template>
