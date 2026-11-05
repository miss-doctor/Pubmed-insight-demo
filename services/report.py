#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""中文综述报告生成。

采用「结构化模板 + 真实统计量注入」策略：所有数字（文献量、年份区间、
期刊、影响因子）均来自真实检索结果，避免大模型幻觉。
"""

# 各章节的固定结语
_DIRECTION_DESCRIPTIONS = [
    ("**方向一 · {theme}**：出现频次最高，是当前该领域最核心的研究焦点，"
     "相关成果集中探讨其作用机制与临床可行性。"),
    ("**方向二 · {theme}**：紧随其后，反映学界对相关靶点与信号通路的持续关注，"
     "基础研究积累较为扎实。"),
    ("**方向三 · {theme}**：相关成果不断涌现，提示该方向正处于快速成长阶段，"
     "具备较大的发展潜力。"),
]

_NO_DATA_REPORT = "未检索到相关文献，无法生成综述。"


def _year_trend(year_counts, years):
    """根据首尾年份发文量给出趋势描述。"""
    if len(years) < 2:
        return "较为集中"
    first, last = year_counts[years[0]], year_counts[years[-1]]
    if last > first:
        return "呈上升态势，研究热度持续攀升"
    if last < first:
        return "稳中有变，逐步进入沉淀与深化阶段"
    return "总体保持稳定"


def _direction_points(direction_names):
    """生成「研究热点方向」的分点描述。"""
    points = [
        template.format(theme=theme)
        for template, theme in zip(_DIRECTION_DESCRIPTIONS, direction_names)
    ]
    return points or ["相关研究集中在机制探索与临床应用两个层面，整体呈现稳步推进的态势。"]


def _top_journals_by_if(papers, limit=3):
    """按影响因子降序去重，取高影响力期刊。"""
    ranked = sorted(
        (p for p in papers if p.get('impact_factor')),
        key=lambda p: p['impact_factor'],
        reverse=True,
    )
    seen, picked = set(), []
    for paper in ranked:
        if paper['journal'] in seen:
            continue
        seen.add(paper['journal'])
        picked.append(paper)
        if len(picked) >= limit:
            break
    return picked


def generate_review(keyword, papers, directions, year_counts, journal_counts, pubmed_total=None):
    """生成约 500 字、分点呈现的中文综述。"""
    total = len(papers)
    if total == 0:
        return _NO_DATA_REPORT

    years = sorted(year_counts)
    span = f"{years[0]}–{years[-1]}" if years else "近五年"
    trend = _year_trend(year_counts, years)

    top_journals = journal_counts.most_common(3)
    journal_text = '、'.join(name for name, _ in top_journals) or "暂无"

    direction_names = [d['theme'] for d in directions[:3]]
    direction_text = '、'.join(d['theme'] for d in directions[:5]) or "相关机制与临床研究"
    points_text = '\n'.join(
        f"{i + 1}. {point}" for i, point in enumerate(_direction_points(direction_names))
    )

    def journal_label(paper):
        parts = [f"IF≈{paper['impact_factor']}"]
        if paper.get('zone'):
            parts.append(f"中科院{paper['zone']}区")
        return f"{paper['journal']}（{'，'.join(parts)}）"

    high_if = _top_journals_by_if(papers, limit=3)
    high_if_text = '、'.join(journal_label(p) for p in high_if) or "暂无可比影响因子数据"

    sample_titles = '；'.join(p['title'] for p in papers[:2] if p.get('title'))
    hit_text = f"，PubMed 原始命中 {pubmed_total} 篇" if pubmed_total else ""

    return f"""## {keyword} 领域研究进展综述（自动生成）

**一、研究概况**
以“{keyword}”为关键词检索 PubMed{hit_text}，并按近五年（{span} 年）时间窗口纳入 {total} 篇文献进行分析。从发文趋势看，该领域近五年发文量{trend}，说明其仍是国际科研关注的热点方向之一。相关成果主要发表在 {journal_text} 等高影响力期刊，研究力量分布较为集中，整体呈现基础研究与临床应用并进的格局。

**二、研究热点方向**
{points_text}
综合高频主题词可知，当前研究整体围绕 {direction_text} 等方向展开，研究链条正由作用机制的解析，逐步向新型治疗策略的临床验证与转化延伸。

**三、高影响力成果**
在影响因子维度上，本领域的代表性期刊包括 {high_if_text} 等。其中较具代表性的文献有：{sample_titles}。这些工作分别从机制、疗效与安全性等角度，推动了该领域认识的深化，也为后续研究提供了重要参考。

**四、研究趋势与展望**
总体而言，{keyword} 领域仍处于活跃发展阶段，且呈现出多学科交叉、从实验室走向临床的鲜明特征。未来研究可重点关注以下三点：1）整合多组学与真实世界数据，提升研究结论的外部效度与可重复性；2）开展多中心、大样本的前瞻性研究，系统评估新型干预策略的安全性与有效性；3）关注人工智能辅助设计、基因编辑等交叉技术的应用潜力，加速基础成果向临床转化落地。"""
