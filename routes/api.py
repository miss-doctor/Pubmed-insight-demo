#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""页面与数据接口。"""

import os

from flask import Blueprint, jsonify, request, send_from_directory

from config import CACHE_VERSION, DEFAULT_RETMAX, DIST_DIR, MAX_RETMAX
from services.analysis import build_analysis
from services.http_utils import cache_get, cache_set

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    """首页：托管 Vue 3 构建产物（static/dist/index.html）。"""
    if os.path.exists(os.path.join(DIST_DIR, 'index.html')):
        return send_from_directory(DIST_DIR, 'index.html')
    return (
        '<h3>前端尚未构建</h3>'
        '<p>请在 frontend 目录执行 <code>npm install &amp;&amp; npm run build</code>，'
        '构建产物会输出到 static/dist。</p>',
        503,
    )


@bp.route('/search')
def search():
    """关键词检索接口：命中缓存则直接返回，否则实时抓取并写入缓存。"""
    keyword = request.args.get('keyword', '').strip()
    retmax = min(int(request.args.get('retmax', DEFAULT_RETMAX)), MAX_RETMAX)
    use_cache = request.args.get('cache', '1') != '0'

    if not keyword:
        return jsonify({'error': '请输入关键词'}), 400

    cache_key = f"{CACHE_VERSION}|{keyword.lower()}|{retmax}"

    if use_cache:
        cached = cache_get(cache_key)
        if cached is not None:
            cached['from_cache'] = True
            return jsonify(cached)

    try:
        result = build_analysis(keyword, retmax=retmax)
    except Exception as exc:  # noqa: BLE001 - 统一转成 JSON 错误
        return jsonify({'error': f'PubMed 检索失败：{exc}'}), 500

    if use_cache:
        cache_set(cache_key, result)

    result['from_cache'] = False
    return jsonify(result)
