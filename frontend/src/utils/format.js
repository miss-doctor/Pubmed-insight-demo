/** HTML 转义，防止题录内容注入。 */
export function escapeHtml(str) {
  return String(str ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

/** 把 `**加粗**` 转成 <strong>，其余内容先转义。 */
export function formatInline(text) {
  return escapeHtml(text).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
}

/** 千分位数字。 */
export function formatNumber(value) {
  return Number(value || 0).toLocaleString()
}

/** 影响因子保留 1 位小数。 */
export function formatImpactFactor(value) {
  const num = Number(value)
  return Number.isFinite(num) && num > 0 ? num.toFixed(1) : '-'
}

/** 分区徽标 -> 样式类。支持 JCR（Q1–Q4）与中科院（1区–4区）两种写法。 */
export function quartileClass(label) {
  if (!label || label === '未知' || label === '未收录') return 'q-unknown'
  if (/^Q[1-4]$/.test(label)) return `q${label.slice(1)}`
  const zone = String(label).match(/^([1-4])区$/)
  return zone ? `z${zone[1]}` : 'q-unknown'
}

/** 覆盖率小数 -> 百分比字符串。 */
export function formatCoverage(value) {
  const num = Number(value)
  if (!Number.isFinite(num) || num <= 0) return '0%'
  return `${(num * 100).toFixed(1)}%`
}

/** 解析后端返回的类 Markdown 综述为结构化段落。 */
export function parseReport(markdown) {
  const lines = String(markdown || '').split('\n').filter((line) => line.trim())
  return lines.map((line) => {
    if (line.startsWith('## ')) {
      return { type: 'heading', html: escapeHtml(line.replace('## ', '')) }
    }
    if (/^\d+\.\s/.test(line)) {
      return { type: 'point', html: formatInline(line) }
    }
    return { type: 'paragraph', html: formatInline(line) }
  })
}
