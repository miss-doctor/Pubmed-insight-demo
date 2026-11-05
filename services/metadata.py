#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文献元数据解析：年份提取、文献类型归一化。"""

import re

# PubMed 文献类型 -> 中文短标签（按优先级排列）
_PUBLICATION_TYPE_MAP = [
    ('randomized controlled trial', 'RCT'),
    ('meta-analysis', 'Meta分析'),
    ('systematic review', '系统综述'),
    ('review', '综述'),
    ('clinical trial', '临床试验'),
    ('editorial', '社论'),
    ('comment', '评论'),
    ('letter', '通讯'),
    ('practice guideline', '指南'),
    ('retracted', '撤稿'),
    ('published erratum', '勘误'),
    ('journal article', '研究论文'),
]

DEFAULT_PUB_TYPE = '研究论文'


def parse_year(date_str):
    """从 PubMed 日期字符串中提取四位年份，失败返回 None。"""
    if not date_str:
        return None
    match = re.search(r'(19|20)\d{2}', str(date_str))
    return int(match.group(0)) if match else None


def simplify_ptype(types):
    """将 PubMed 的 PublicationType 列表映射为中文短标签。"""
    if not types:
        return DEFAULT_PUB_TYPE

    lowered = [t.lower() for t in types]
    for keyword, label in _PUBLICATION_TYPE_MAP:
        if any(keyword in t for t in lowered):
            return label
    return DEFAULT_PUB_TYPE
