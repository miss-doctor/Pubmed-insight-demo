#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全局配置：路径、外部 API 地址、缓存与时间窗口参数。"""

import os
from datetime import datetime

# ---------------------------------------------------------------------------
# 路径
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# Vue 3 前端构建产物目录（由 frontend/ 执行 npm run build 生成）
DIST_DIR = os.path.join(STATIC_DIR, 'dist')

JOURNAL_METRICS_PATH = os.path.join(DATA_DIR, 'journal_metrics.json')
STOPWORDS_PATH = os.path.join(DATA_DIR, 'stopwords.txt')

# ---------------------------------------------------------------------------
# PubMed E-utilities
# ---------------------------------------------------------------------------
PUBMED_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

PUBMED_WEB = "https://pubmed.ncbi.nlm.nih.gov/"

# 单次检索请求的批量大小
SUMMARY_BATCH_SIZE = 100
ABSTRACT_BATCH_SIZE = 50

# NCBI 公共速率限制：匿名访问约 3 次/秒
SLEEP_BETWEEN_REQUESTS = 0.4

# ---------------------------------------------------------------------------
# 检索与分析参数
# ---------------------------------------------------------------------------
DEFAULT_RETMAX = 150      # 默认分析文献数
MAX_RETMAX = 400          # 上限，防止请求过大
TOP_PAPERS_LIMIT = 100    # 影响力排序取前 N 篇
TOP_JOURNAL_LIMIT = 10    # 期刊分布图表取前 N 本
WORDCLOUD_SIZE = 60       # 词云词条数
DIRECTION_SIZE = 8        # 研究方向条数

CURRENT_YEAR = datetime.now().year
FIVE_YEARS_AGO = CURRENT_YEAR - 4     # 含当年，共 5 年

# ---------------------------------------------------------------------------
# 缓存
# ---------------------------------------------------------------------------
CACHE_TTL = 6 * 3600      # 缓存有效期（秒）
CACHE_VERSION = "v7"      # 分析逻辑变更时递增，用于失效旧缓存

# ---------------------------------------------------------------------------
# 服务器
# ---------------------------------------------------------------------------
HOST = '0.0.0.0'
PORT = 5000
