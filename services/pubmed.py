#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PubMed E-utilities 客户端：检索、摘要元数据、文摘与文献类型。"""

import time
import xml.etree.ElementTree as ET

from config import (
    PUBMED_ESEARCH,
    PUBMED_ESUMMARY,
    PUBMED_EFETCH,
    SUMMARY_BATCH_SIZE,
    ABSTRACT_BATCH_SIZE,
    SLEEP_BETWEEN_REQUESTS,
    FIVE_YEARS_AGO,
    CURRENT_YEAR,
)
from services.http_utils import http_get


def _sleep(seconds=None):
    """按 NCBI 公共速率限制休眠，避免被限流。"""
    time.sleep(seconds if seconds is not None else SLEEP_BETWEEN_REQUESTS)


def build_query(keyword, year_from=FIVE_YEARS_AGO, year_to=CURRENT_YEAR):
    """构造带近五年时间过滤的 PubMed 查询语句。"""
    return f"({keyword.strip()}) AND ({year_from}/1/1:{year_to}/12/31[dp])"


def search(keyword, retmax=200):
    """检索 PubMed，返回 (pmid 列表, 命中总数)。"""
    params = {
        'db': 'pubmed',
        'term': build_query(keyword),
        'retmode': 'json',
        'retmax': retmax,
        'sort': 'relevance',
    }

    data = http_get(PUBMED_ESEARCH, params).json()
    result = data.get('esearchresult', {})
    return result.get('idlist', []), int(result.get('count', 0))


def summaries(pmids, batch_size=SUMMARY_BATCH_SIZE):
    """批量获取文献元数据（标题、期刊、年份、作者等）。"""
    if not pmids:
        return []

    out = []
    for start in range(0, len(pmids), batch_size):
        batch = pmids[start:start + batch_size]
        params = {'db': 'pubmed', 'id': ','.join(batch), 'retmode': 'json'}

        result = http_get(PUBMED_ESUMMARY, params).json().get('result', {})
        out.extend(result.get(uid, {}) for uid in result.get('uids', []))

        if start + batch_size < len(pmids):
            _sleep()
    return out


def details(pmids, batch_size=ABSTRACT_BATCH_SIZE):
    """批量获取文摘与文献类型。

    返回 ``{pmid: {'abstract': str, 'types': [str]}}``。
    单批失败会跳过，不影响整体流程。
    """
    if not pmids:
        return {}

    out = {}
    for start in range(0, len(pmids), batch_size):
        batch = pmids[start:start + batch_size]
        params = {
            'db': 'pubmed',
            'id': ','.join(batch),
            'retmode': 'xml',
            'rettype': 'abstract',
        }

        try:
            root = ET.fromstring(http_get(PUBMED_EFETCH, params, timeout=90).content)
        except Exception:  # noqa: BLE001 - 单批失败不影响其它批次
            _sleep()
            continue

        out.update(_parse_articles(root))
        _sleep()
    return out


def _parse_articles(root):
    """从 efetch 的 XML 根节点中解析出文摘与文献类型。"""
    parsed = {}
    for article in root.findall('.//PubmedArticle'):
        pmid_el = article.find('.//PMID')
        pmid = pmid_el.text if pmid_el is not None else None
        if not pmid:
            continue

        chunks = [
            ''.join(ab.itertext()).strip()
            for ab in article.findall('.//Abstract/AbstractText')
        ]
        parsed[pmid] = {
            'abstract': ' '.join(chunk for chunk in chunks if chunk),
            'types': [t.text for t in article.findall('.//PublicationType') if t.text],
        }
    return parsed
