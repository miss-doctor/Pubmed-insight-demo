import { onBeforeUnmount, ref, watch } from 'vue'

import { PROGRESS_STEPS } from '@/utils/constants'

/**
 * 检索耗时较长（首次实时抓取约 10~60 秒），用轮播文案让等待过程可感知。
 */
export function useElapsedProgress(isLoading) {
  const stepIndex = ref(0)
  const elapsed = ref(0)
  let timer = null

  function stop() {
    if (timer) {
      clearInterval(timer)
      timer = null
    }
  }

  watch(
    isLoading,
    (loading) => {
      stop()
      if (!loading) {
        stepIndex.value = 0
        elapsed.value = 0
        return
      }
      const startedAt = Date.now()
      timer = setInterval(() => {
        elapsed.value = Math.floor((Date.now() - startedAt) / 1000)
        const next = Math.floor(elapsed.value / 5)
        if (next < PROGRESS_STEPS.length) stepIndex.value = next
      }, 500)
    },
    { immediate: true }
  )

  onBeforeUnmount(stop)

  return { stepIndex, elapsed }
}
