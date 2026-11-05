#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""期刊指标查询：影响因子（IF）、JCR 分区（Q1–Q4）、中科院大类分区（1–4 区）。

数据源
------
``data/journal_metrics.json``，由 ``tools/build_journal_metrics.py`` 从两份公开
数据表构建：

* Clarivate **JCR 2025**：影响因子 + 每个所属学科的 JCR 分区与排名；
* 中国科学院文献情报中心 **分区表升级版 2025**：大类分区（1–4 区）、Top 标记、
  各小类分区。

匹配策略（重要）
----------------
旧版实现使用「子串包含匹配」（``known in key or key in known``），导致只要期刊名里
含 ``science`` / ``cell`` / ``nature`` 等子串，就被赋予顶刊的影响因子，例如
``Life sciences`` 被赋成 56.9、``Journal of cellular and molecular medicine`` 被赋成
64.5。这正是笔试反馈「影响因子数据存在缺失 / 分区未完整实现」的根因之一。

本实现的每一条规则都是**精确查表**，不包含任何包含匹配：

1. **ISSN / EISSN**：PubMed esummary 每篇文献都返回 ISSN 与 EISSN，是权威主键，
   100% 无歧义；
2. **期刊名归一化后精确相等**；
3. **去掉副标题**（``Molecular therapy : the journal of ...`` → ``moleculartherapy``）；
4. **去掉括号限定符**（``Science (New York, N.Y.)`` → ``science``）；
5. **去掉前导 ``the``**（``The Lancet`` → ``lancet``）。

任何一步命中不了就返回「未收录」，**绝不猜测**。宁可显示未收录，也不给出错误数字。
"""

import re

from config import JOURNAL_METRICS_PATH
from services.storage import load_json

_DB = load_json(JOURNAL_METRICS_PATH)

JOURNALS = _DB.get('journals', [])
ISSN_INDEX = _DB.get('issn_index', {})
NAME_INDEX = _DB.get('name_index', {})
META = _DB.get('meta', {})

UNKNOWN_QUARTILE = '未收录'
UNKNOWN_ZONE = '未收录'


def metrics_meta():
    """返回期刊指标库的版本信息（用于前端标注数据来源与版本）。"""
    return META


def normalize_journal(name):
    """统一期刊名格式（小写、仅保留字母数字），用于匹配。"""
    return re.sub(r'[^a-z0-9]', '', (name or '').lower())


def normalize_issn(raw):
    """归一化 ISSN：去掉连字符与空格并转大写；不足 8 位视为无效。"""
    if not raw:
        return ''
    value = re.sub(r'[^0-9A-Za-z]', '', str(raw)).upper()
    return value if len(value) == 8 else ''


def _name_variants(name):
    """按优先级产出期刊名的候选写法，全部供精确查表使用。

    所有候选都只是「原名的规范化裁剪」，命中即代表同名，不会跨刊误匹配。
    """
    full = (name or '').strip()
    if not full:
        return

    yield 'name', normalize_journal(full)

    # 去副标题：Molecular therapy : the journal of ... -> Molecular therapy
    head = re.split(r'\s*[:;]\s*', full)[0].strip()
    if head and head != full:
        yield 'name:nosubtitle', normalize_journal(head)

    # 去括号限定符：Science (New York, N.Y.) -> Science
    no_paren = re.sub(r'\([^)]*\)', ' ', full).strip()
    if no_paren and no_paren != full:
        yield 'name:noparenthesis', normalize_journal(no_paren)

    # 去前导 the：The Lancet -> Lancet
    if full.lower().startswith('the '):
        stripped = full[4:].strip()
        if stripped:
            yield 'name:nothe', normalize_journal(stripped)

    # 去方括号前缀：[Rinsho ketsueki] The Japanese journal ... -> The Japanese journal ...
    no_bracket = re.sub(r'^\[[^\]]*\]\s*', '', full).strip()
    if no_bracket and no_bracket != full:
        yield 'name:nobracket', normalize_journal(no_bracket)
        if no_bracket.lower().startswith('the '):
            yield 'name:nobracket+nothe', normalize_journal(no_bracket[4:].strip())


def _lookup(index, key):
    """从索引查下标，返回期刊记录或 None。"""
    if not key:
        return None
    idx = index.get(key)
    return JOURNALS[idx] if isinstance(idx, int) and 0 <= idx < len(JOURNALS) else None


def _empty_result():
    """未收录时的结果结构。"""
    return {
        'matched': False,
        'match_by': None,
        'journal': '',
        'impact_factor': None,
        'quartile': UNKNOWN_QUARTILE,
        'jcr_rank': '',
        'categories': [],
        'zone': None,
        'zone_label': UNKNOWN_ZONE,
        'zone_name': '',
        'zone_rank': '',
        'is_top': False,
        'source': '',
    }


def get_journal_metrics(journal_name=None, issn=None, essn=None):
    """查询期刊的影响因子与分区。

    Args:
        journal_name (str): PubMed 返回的期刊全称（fulljournalname）。
        issn (str): 印刷版 ISSN。
        essn (str): 电子版 ISSN。

    Returns:
        dict: 见模块顶部说明；``matched`` 为 False 表示未被 JCR / 中科院分区表收录。
    """
    # 1) ISSN 是最权威的主键，优先使用
    for raw in (issn, essn):
        record = _lookup(ISSN_INDEX, normalize_issn(raw))
        if record:
            return _build_result(record, 'issn')

    # 2) 期刊名的各种规范化写法，全部为精确查表
    for how, key in _name_variants(journal_name):
        record = _lookup(NAME_INDEX, key)
        if record:
            return _build_result(record, how)

    return _empty_result()


def _build_result(record, match_by):
    """把原始记录整理成对外输出结构。"""
    zone = record.get('zone')
    cats = record.get('cats') or []
    return {
        'matched': True,
        'match_by': match_by,
        'journal': record.get('name', ''),
        'impact_factor': record.get('if'),
        'quartile': record.get('q') or UNKNOWN_QUARTILE,
        'jcr_rank': cats[0][2] if cats and len(cats[0]) > 2 else '',
        'categories': [
            {'name': c[0], 'quartile': c[1], 'rank': c[2]}
            for c in cats if c and c[0]
        ],
        'zone': zone,
        'zone_label': f'{zone}区' if zone else UNKNOWN_ZONE,
        'zone_name': record.get('zone_name', ''),
        'zone_rank': record.get('zone_rank', ''),
        'is_top': bool(record.get('top')),
        'source': record.get('source', ''),
    }
