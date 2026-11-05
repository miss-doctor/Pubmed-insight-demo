/** 与 Flask 后端约定的默认分析文献数。 */
export const DEFAULT_RETMAX = 200

/**
 * 调用后端 /search 接口，返回结构化分析结果。
 * @param {{ keyword: string, retmax?: number, cache?: boolean }} params
 */
export async function fetchAnalysis({ keyword, retmax = DEFAULT_RETMAX, cache = true }) {
  const query = new URLSearchParams({
    keyword,
    retmax: String(retmax)
  })
  if (!cache) query.set('cache', '0')

  let response
  try {
    response = await fetch(`/search?${query.toString()}`)
  } catch (err) {
    throw new Error('无法连接分析服务，请确认后端已启动（python app.py）')
  }

  let data
  try {
    data = await response.json()
  } catch (err) {
    throw new Error(`服务返回异常（HTTP ${response.status}）`)
  }

  if (!response.ok || data.error) {
    throw new Error(data.error || `检索失败（HTTP ${response.status}）`)
  }
  return data
}