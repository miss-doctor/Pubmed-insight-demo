#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地数据文件读取工具。"""

import os
import json


def load_json(path):
    """读取 JSON 文件，不存在或解析失败时返回空字典。"""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:  # noqa: BLE001
        return {}


def load_text_lines(path):
    """读取文本文件为小写字符串集合（用于停用词表，支持 ``#`` 注释行）。"""
    if not os.path.exists(path):
        return set()
    with open(path, 'r', encoding='utf-8') as fh:
        return {
            line.strip().lower()
            for line in fh
            if line.strip() and not line.lstrip().startswith('#')
        }
