import { onBeforeUnmount, ref } from 'vue'
import Chart from 'chart.js/auto'

/**
 * 统一管理单个 Chart 实例的生命周期：
 * 重复绘制时先销毁旧实例，组件卸载时自动清理，避免内存泄漏。
 */
export function useChart() {
  const canvasRef = ref(null)
  let instance = null

  function draw(config) {
    if (instance) {
      instance.destroy()
      instance = null
    }
    if (!canvasRef.value) return
    instance = new Chart(canvasRef.value, config)
    return instance
  }

  onBeforeUnmount(() => {
    if (instance) {
      instance.destroy()
      instance = null
    }
  })

  return { canvasRef, draw }
}
