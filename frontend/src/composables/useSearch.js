import { computed, ref } from 'vue'

import { DEFAULT_RETMAX, fetchAnalysis } from '@/api/pubmed'

/**
 * 检索状态机：把「输入 → 请求 → 成功/空/失败」全部收敛在一处，
 * 组件只负责展示，不关心请求细节。
 *
 * status: idle | loading | success | empty | error
 */
export function useSearch() {
  const keyword = ref('')
  const retmax = ref(DEFAULT_RETMAX)

  const status = ref('idle')
  const errorMessage = ref('')
  const result = ref(null)
  const elapsedSeconds = ref(0)

  const isLoading = computed(() => status.value === 'loading')
  const hasResult = computed(() => status.value === 'success' && !!result.value)

  async function search(rawKeyword) {
    const nextKeyword = String(rawKeyword ?? keyword.value).trim()
    if (!nextKeyword || isLoading.value) return

    keyword.value = nextKeyword
    status.value = 'loading'
    errorMessage.value = ''
    const startedAt = performance.now()

    try {
      const data = await fetchAnalysis({
        keyword: nextKeyword,
        retmax: retmax.value
      })
      elapsedSeconds.value = (performance.now() - startedAt) / 1000
      result.value = data
      status.value = data.retrieved === 0 ? 'empty' : 'success'
    } catch (err) {
      errorMessage.value = err?.message || '检索失败，请稍后重试'
      result.value = null
      status.value = 'error'
    }
  }

  function reset() {
    status.value = 'idle'
    result.value = null
    errorMessage.value = ''
    elapsedSeconds.value = 0
  }

  return {
    keyword,
    retmax,
    status,
    errorMessage,
    result,
    elapsedSeconds,
    isLoading,
    hasResult,
    search,
    reset
  }
}