#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTTP 请求与磁盘缓存工具。
"""
import os
import json
import time
import hashlib

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import CACHE_DIR, CACHE_TTL

# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
_session = requests.Session()
_retry = Retry(
    total=4,
    backoff_factor=1.2,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=['GET'],
)
_session.mount('https://', HTTPAdapter(max_retries=_retry))


def http_get(url, params, timeout=60, attempts=3):
    """带重试的 GET 请求，成功则返回 Response，全部失败则抛出最后一次异常。"""
    last_err = None
    for attempt in range(attempts):
        try:
            resp = _session.get(url, params=params, timeout=timeout)
            resp.raise_for_status()
            return resp
        except Exception as exc:  # noqa: BLE001 - 需要捕获所有网络异常
            last_err = exc
            time.sleep(1.5 * (attempt + 1))
    raise last_err


# ---------------------------------------------------------------------------
# 磁盘缓存
# ---------------------------------------------------------------------------
def _cache_path(key):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, hashlib.md5(key.encode('utf-8')).hexdigest() + '.json')


def cache_get(key):
    """读取未过期的缓存，未命中返回 None。"""
    path = _cache_path(key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            payload = json.load(fh)
        if time.time() - payload.get('_ts', 0) < CACHE_TTL:
            return payload.get('data')
    except Exception:  # noqa: BLE001 - 缓存损坏时视为未命中
        return None
    return None


def cache_set(key, data):
    """写入缓存（失败时静默忽略，不影响主流程）。"""
    path = _cache_path(key)
    try:
        with open(path, 'w', encoding='utf-8') as fh:
            json.dump({'_ts': time.time(), 'data': data}, fh, ensure_ascii=False)
    except Exception:  # noqa: BLE001
        pass
