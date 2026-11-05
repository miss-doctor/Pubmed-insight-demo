#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析流水线：把 PubMed 原始数据加工成前端可直接渲染的结果结构。"""

import time
from collections import Counter
from urllib.parse import quote

from config import (
    PUBMED_WEB,
    SLEEP_BETWEEN_REQUESTS,
    TOP_PAPERS_LIMIT,
    TOP_JOURNAL_LIMIT,
    WORDCLOUD_SIZE,
    DIRECTION_SIZE,
)
from services import pubmed
from services.metadata import parse_year, simplify_ptype
from services.metrics import get_journal_metrics, metrics_meta
from services.nlp import extract_phrases, extract_research_directions
from services.report import generate_review


def source_url(keyword):
    """返回 PubMed 官网对应的检索链接。"""
    return f"{PUBMED_WEB}?term={quote(keyword)}"


def _empty_result(keyword):
    """无命中时的空结果结构。"""
    empty_stats = {
        'avg_if': 0,
        'max_if': 0,
        'q_counts': {},
        'zone_counts': {},
        'with_abstract': 0,
        'if_matched': 0,
        'zone_matched': 0,
        'if_coverage': 0,
        'zone_coverage': 0,
        'top_journal_papers': 0,
    }
    return {
        'keyword': keyword,
        'total': 0,
        'retrieved': 0,
        'years': {},
        'journals': [],
        'wordcloud': [],
        'directions': [],
        'top_papers': [],
        'stats': empty_stats,
        'metrics_meta': metrics_meta(),
        'report': generate_review(keyword, [], [], {}, Counter()),
        'source_url': source_url(keyword),
    }


def _build_paper(summary, detail):
    """把 esummary + efetch 的数据合并成单篇文献记录。"""
    pmid = summary.get('uid')
    journal = summary.get('fulljournalname') or summary.get('source') or 'Unknown'
    abstract = detail.get('abstract', '')

    # 以 ISSN 为主键做精确匹配，避免期刊名子串误判
    metrics = get_journal_metrics(journal, summary.get('issn'), summary.get('essn'))

    return {
        'pmid': pmid,
        'title': summary.get('title', ''),
        'authors': [a.get('name') for a in summary.get('authors', [])[:3] if a.get('name')],
        'journal': journal,
        'year': parse_year(summary.get('pubdate') or summary.get('sortpubdate')),
        'doi': summary.get('elocationid', ''),
        'abstract': abstract,
        'abstract_preview': abstract[:300] + ('…' if len(abstract) > 300 else ''),
        'issn': summary.get('issn') or summary.get('essn') or '',
        'impact_factor': metrics['impact_factor'],
        'quartile': metrics['quartile'],
        'zone': metrics['zone'],
        'zone_label': metrics['zone_label'],
        'zone_name': metrics['zone_name'],
        'is_top': metrics['is_top'],
        'has_abstract': bool(abstract),
        'pub_type': simplify_ptype(detail.get('types', [])),
        'url': f"{PUBMED_WEB}{pmid}/",
    }


def _summarize(papers, quartile_counts, zone_counts):
    """汇总统计指标：影响因子均值/最高值、JCR 与中科院分区计数、覆盖率。"""
    total = len(papers)
    factors = [p['impact_factor'] for p in papers if p['impact_factor']]
    if_matched = sum(1 for p in papers if p['impact_factor'] is not None)
    zone_matched = sum(1 for p in papers if p['zone'])

    def coverage(n):
        return round(n / total, 3) if total else 0

    return {
        'avg_if': round(sum(factors) / len(factors), 2) if factors else 0,
        'max_if': round(max(factors), 1) if factors else 0,
        'q_counts': dict(quartile_counts),
        'zone_counts': dict(zone_counts),
        'with_abstract': sum(1 for p in papers if p['abstract']),
        'if_matched': if_matched,
        'zone_matched': zone_matched,
        'if_coverage': coverage(if_matched),
        'zone_coverage': coverage(zone_matched),
        'top_journal_papers': sum(1 for p in papers if p['is_top']),
    }


def build_analysis(keyword, retmax=150):
    """执行「检索 -> 抓取 -> 清洗 -> 统计 -> 词云 -> 综述」全流程。"""
    if not keyword:
        raise ValueError('关键词不能为空')

    pmids, total = pubmed.search(keyword, retmax=retmax)
    if not pmids:
        return _empty_result(keyword)

    # 遵守 NCBI 公共速率限制，避免被限流
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    summaries = pubmed.summaries(pmids)
    time.sleep(SLEEP_BETWEEN_REQUESTS)
    details = pubmed.details(pmids)

    papers = []
    year_counts, journal_counts = Counter(), Counter()
    quartile_counts, zone_counts = Counter(), Counter()
    texts = []

    for summary in summaries:
        paper = _build_paper(summary, details.get(summary.get('uid'), {}))
        papers.append(paper)
        texts.append(f"{paper['title']} {paper['abstract']}")

        if paper['year']:
            year_counts[paper['year']] += 1
        journal_counts[paper['journal']] += 1
        quartile_counts[paper['quartile']] += 1
        zone_counts[paper['zone_label']] += 1

    # ③ 影响力排序：影响因子优先，同年按年份（越新越前）；未收录的排在最后
    top_papers = sorted(
        papers,
        key=lambda p: (p['impact_factor'] is not None, p['impact_factor'] or 0,
                       p['year'] or 0),
        reverse=True,
    )[:TOP_PAPERS_LIMIT]

    wordcloud = [
        {'name': name, 'value': int(count)}
        for name, count in extract_phrases(texts, top_n=WORDCLOUD_SIZE)
    ]
    directions = extract_research_directions(texts, top_n=DIRECTION_SIZE)

    return {
        'keyword': keyword,
        'total': total,
        'retrieved': len(papers),
        'years': dict(sorted(year_counts.items())),
        'journals': [
            {'journal': name, 'count': count}
            for name, count in journal_counts.most_common(TOP_JOURNAL_LIMIT)
        ],
        'wordcloud': wordcloud,
        'directions': directions,
        'top_papers': top_papers,
        'stats': _summarize(papers, quartile_counts, zone_counts),
        'metrics_meta': metrics_meta(),
        'report': generate_review(
            keyword, papers, directions, year_counts, journal_counts, pubmed_total=total
        ),
        'source_url': source_url(keyword),
    }
