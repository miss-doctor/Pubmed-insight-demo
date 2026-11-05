/** 结果表格中默认被过滤掉的文献类型（非研究性文献）。 */
export const EXCLUDE_TYPES = ['社论', '评论', '通讯', '勘误', '撤稿']

/** 首页热门示例关键词。 */
export const QUICK_TAGS = [
  { label: 'CAR-T therapy', keyword: 'CAR-T therapy' },
  { label: 'gut microbiota', keyword: 'gut microbiota' },
  { label: 'Alzheimer disease', keyword: 'Alzheimer disease' },
  { label: 'CRISPR', keyword: 'CRISPR gene editing' },
  { label: 'PD-1 免疫治疗', keyword: 'PD-1 immunotherapy' }
]

/** 未被 JCR / 中科院分区表收录时的统一文案。 */
export const UNKNOWN_LABEL = '未收录'

/** JCR 分区配色（与图表、表格徽标保持一致）。 */
export const QUARTILE_ORDER = ['Q1', 'Q2', 'Q3', 'Q4']

export const QUARTILE_COLORS = {
  Q1: '#1f9d55',
  Q2: '#1f6feb',
  Q3: '#e8850c',
  Q4: '#d64545',
  未收录: '#c7d0da'
}

/** 中科院大类分区配色。 */
export const ZONE_ORDER = ['1区', '2区', '3区', '4区']

export const ZONE_COLORS = {
  '1区': '#8b5cf6',
  '2区': '#1f6feb',
  '3区': '#e8850c',
  '4区': '#8a99aa',
  未收录: '#c7d0da'
}

/** 词云配色。 */
export const WORDCLOUD_PALETTE = [
  '#1f6feb', '#00a8a8', '#7a5af8', '#e8850c',
  '#1f9d55', '#d64545', '#1558c0'
]

/** 检索进度提示（纯展示，按时间推进）。 */
export const PROGRESS_STEPS = [
  '正在检索 PubMed 命中文献…',
  '正在拉取标题与期刊元数据…',
  '正在解析摘要并计算影响因子…',
  '正在生成词云、研究方向与综述…'
]
