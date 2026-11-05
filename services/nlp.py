#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""文本挖掘：分词、高频短语（词云）、研究方向归纳。"""

import re
import html
from collections import Counter

from config import STOPWORDS_PATH
from services.storage import load_text_lines

STOPWORDS = load_text_lines(STOPWORDS_PATH)

# 研究主题去重时需要归一化的同义词
_THEME_ALIASES = re.compile(r'\b(car|cell|cells|therapy|therapies)\b')


def tokenize(text):
    """英文文本分词并过滤停用词、数字与过短词。"""
    if not text:
        return []
    text = html.unescape(text)
    text = re.sub(r'[^\w\s]', ' ', text)
    tokens = [t.lower() for t in text.split() if len(t) > 2]
    return [t for t in tokens if t not in STOPWORDS and not t.isdigit()]


def extract_phrases(texts, top_n=50):
    """统计高频词与二元短语，用于生成词云。

    二元短语权重 ×2，使其在词云中更突出、语义更完整。
    返回 ``[(短语, 频次), ...]``，按频次降序。
    """
    unigrams, bigrams = Counter(), Counter()
    for text in texts:
        tokens = tokenize(text)
        unigrams.update(tokens)
        bigrams.update(zip(tokens, tokens[1:]))

    combined = Counter()
    for word, count in unigrams.most_common(top_n * 2):
        combined[word] = count
    for (w1, w2), count in bigrams.most_common(top_n):
        combined[f"{w1} {w2}"] = count * 2

    return combined.most_common(top_n)


def _normalize_theme(text):
    """归一化主题词以便去重（如 car cells / cell therapy）。"""
    text = re.sub(r'[^a-z0-9 ]', '', text.lower())
    text = _THEME_ALIASES.sub(lambda m: m.group(1).rstrip('s'), text)
    return ' '.join(sorted(text.split()))


def extract_research_directions(texts, top_n=6):
    """归纳主要研究方向：优先多词短语，并剔除语义重复项。"""
    phrases = extract_phrases(texts, top_n=top_n * 15)
    seen = set()
    directions = []

    def try_add(theme, count):
        key = _normalize_theme(theme)
        if not key or key in seen:
            return
        if any(key in other or other in key for other in seen):
            return
        seen.add(key)
        directions.append({'theme': theme, 'count': count})

    # 第一轮：多词短语（信息量更大）
    for phrase, count in phrases:
        if len(directions) >= top_n:
            break
        if ' ' in phrase and len(phrase) < 50:
            try_add(phrase.title(), count)

    # 第二轮：不足时用单词补齐
    if len(directions) < top_n:
        for phrase, count in phrases:
            if len(directions) >= top_n:
                break
            if ' ' not in phrase:
                try_add(phrase.title(), count)

    return directions
