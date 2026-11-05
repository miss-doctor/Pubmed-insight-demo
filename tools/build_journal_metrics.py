#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把 JCR 与中科院分区表的原始 CSV 合并成前端/后端可直接使用的期刊指标库。

数据源（均为公开发布的数据集，随 ShowJCR 项目分发）：
  1. JCR2025-UTF8.csv
     Clarivate JCR 2025 版：期刊名、ISSN、eISSN、影响因子、
     以及每个所属学科的 JCR 分区（Q1–Q4）与分区内排名。
  2. FQBJCR2025-UTF8.csv
     中国科学院文献情报中心分区表升级版 2025：大类分区（1–4 区）、
     是否 Top 期刊、以及各小类分区。

产出 data/journal_metrics.json，结构：
  {
    "meta":       { 版本、构建时间、条目统计、数据来源 },
    "journals":   [ 期刊记录数组 ],
    "issn_index": { 归一化 ISSN -> journals 下标 },
    "name_index": { 归一化期刊名 -> journals 下标 }
  }

设计要点：
  - **以 ISSN 为主键**。PubMed esummary 每篇文献都会返回 ISSN / EISSN，
    用 ISSN 匹配可以从根上消除「期刊名子串误匹配」（例如 Life sciences
    被当成 Science）这类问题。
  - 名称索引只用于**精确匹配**，不存储任何模糊/包含规则。

用法：
    python tools/build_journal_metrics.py
"""

import csv
import json
import os
import re
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)

SOURCE_DIR = os.path.join(ROOT, "data", "source")
JCR_CSV = os.path.join(SOURCE_DIR, "JCR2025-UTF8.csv")
CAS_CSV = os.path.join(SOURCE_DIR, "FQBJCR2025-UTF8.csv")
OUTPUT = os.path.join(ROOT, "data", "journal_metrics.json")

JCR_EDITION = "JCR 2025"
CAS_EDITION = "中科院分区表升级版 2025"

Q_ORDER = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}


def norm_issn(raw):
    """归一化 ISSN：去掉连字符、转大写；非 8 位视为无效。"""
    if not raw:
        return ""
    v = re.sub(r"[^0-9A-Za-z]", "", raw).upper()
    return v if len(v) == 8 else ""


def norm_name(raw):
    """归一化期刊名：小写、只保留字母与数字（与运行时的匹配函数保持一致）。"""
    return re.sub(r"[^a-z0-9]", "", (raw or "").lower())


def to_float(raw):
    """解析影响因子；缺失或非数值返回 None。"""
    try:
        return float(str(raw).strip())
    except (TypeError, ValueError):
        return None


def best_quartile(values):
    """一门期刊可能属于多个学科、各学科分区不同，取最好的那个（Q1 最优）。"""
    best = None
    for v in values:
        v = (v or "").strip()
        if v in Q_ORDER and (best is None or Q_ORDER[v] < Q_ORDER[best]):
            best = v
    return best


def parse_zone(cell):
    """解析中科院分区单元格，形如 '4 [625/778]' -> (4, '625/778')。"""
    if not cell:
        return None, ""
    m = re.search(r"(\d)", str(cell))
    zone = int(m.group(1)) if m else None
    rank = re.search(r"\[(.*?)\]", str(cell))
    return zone, (rank.group(1) if rank else "")


def read_csv(path):
    """读取 UTF-8(BOM) CSV，返回 DictReader。"""
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def load_jcr(path):
    """读取 JCR CSV，返回 issn -> 指标 的映射。"""
    if not os.path.exists(path):
        raise SystemExit(f"[!] 缺少 JCR 数据文件：{path}\n    请先运行 scripts/download_journal_data.bat / .sh")

    rows = read_csv(path)
    issn_map, name_map = {}, {}

    for row in rows:
        name = (row.get("Journal") or "").strip()
        if_value = to_float(row.get("IF(2025)"))

        # 每门期刊最多 6 个学科，逐个取出（学科, 分区, 排名）
        cats = []
        for i in range(1, 7):
            cat = (row.get(f"Category_{i}") or "").strip()
            if not cat:
                continue
            cats.append([
                cat,
                (row.get(f"IF Quartile(2025)_{i}") or "").strip(),
                (row.get(f"IF Rank(2025)_{i}") or "").strip(),
            ])

        record = {
            "name": name,
            "wos": (row.get("Web of Science") or "").strip(),
            "if": if_value,
            "q": best_quartile([c[1] for c in cats]) or "",
            "cats": cats,
        }

        issns = [norm_issn(row.get("ISSN")), norm_issn(row.get("EISSN"))]
        for issn in issns:
            if not issn:
                continue
            prev = issn_map.get(issn)
            # 同一 ISSN 重复出现时保留影响因子更高的那条
            if prev is None or (if_value or -1) > (prev["if"] if prev["if"] is not None else -1):
                issn_map[issn] = record

        key = norm_name(name)
        if key:
            prev = name_map.get(key)
            if prev is None or (if_value or -1) > (prev["if"] if prev["if"] is not None else -1):
                name_map[key] = record

    print(f"[JCR ] 读取 {len(rows)} 行 -> {len(issn_map)} 个 ISSN / {len(name_map)} 个期刊名")
    return issn_map, name_map


def load_cas(path):
    """读取中科院分区表，返回 issn -> (大类, 大类分区, 排名, Top, 小类列表)。"""
    if not os.path.exists(path):
        raise SystemExit(f"[!] 缺少中科院分区表文件：{path}\n    请先运行 scripts/download_journal_data.bat / .sh")

    rows = read_csv(path)
    issn_map, name_map = {}, {}

    for row in rows:
        name = (row.get("Journal") or "").strip()
        zone, zone_rank = parse_zone(row.get("大类分区"))
        raw_issn = row.get("ISSN/EISSN") or ""

        record = {
            "zone": zone,
            "zone_rank": zone_rank,
            "zone_name": (row.get("大类") or "").strip(),
            "top": (row.get("Top") or "").strip() == "是",
            "review": (row.get("Review") or "").strip() == "是",
            "subs": [],
        }

        for i in range(1, 7):
            cat = (row.get(f"小类{i}") or "").strip()
            if not cat:
                continue
            sub_zone, sub_rank = parse_zone(row.get(f"小类{i}分区"))
            record["subs"].append([cat, sub_zone, sub_rank])

        # ISSN/EISSN 形如 "2649-664X/2649-6100"
        for part in re.split(r"[/,;]|\\", raw_issn):
            issn = norm_issn(part)
            if issn:
                issn_map.setdefault(issn, record)

        key = norm_name(name)
        if key:
            name_map.setdefault(key, record)

    print(f"[CAS ] 读取 {len(rows)} 行 -> {len(issn_map)} 个 ISSN / {len(name_map)} 个期刊名")
    return issn_map, name_map


def main():
    jcr_issn, jcr_name = load_jcr(JCR_CSV)
    cas_issn, cas_name = load_cas(CAS_CSV)

    # 以 JCR 期刊为骨架，补上中科院分区
    from collections import defaultdict

    issns_by_rec, names_by_rec = defaultdict(list), defaultdict(list)
    for issn, rec in jcr_issn.items():
        issns_by_rec[id(rec)].append(issn)
    for key, rec in jcr_name.items():
        names_by_rec[id(rec)].append(key)
    cas_issns_by_rec, cas_names_by_rec = defaultdict(list), defaultdict(list)
    for issn, rec in cas_issn.items():
        cas_issns_by_rec[id(rec)].append(issn)
    for key, rec in cas_name.items():
        cas_names_by_rec[id(rec)].append(key)

    journals, issn_index, name_index = [], {}, {}

    def push(record, issns, names):
        idx = len(journals)
        journals.append(record)
        for issn in issns:
            if issn:
                issn_index.setdefault(issn, idx)
        for n in names:
            if n:
                name_index.setdefault(n, idx)

    seen_ids = set()
    for rec in jcr_issn.values():
        key = id(rec)
        if key in seen_ids:
            continue
        seen_ids.add(key)

        issns = sorted(set(issns_by_rec.get(key, [])))
        names = sorted(set(names_by_rec.get(key, [])))

        cas = {}
        for probe in issns:
            if probe in cas_issn:
                cas = cas_issn[probe]
                break
        else:
            cas = cas_name.get(norm_name(rec["name"]), {})

        push({
            "name": rec["name"],
            "issn": issns,
            "if": rec["if"],
            "q": rec["q"],
            "cats": rec["cats"],
            "zone": cas.get("zone"),
            "zone_name": cas.get("zone_name", ""),
            "zone_rank": cas.get("zone_rank", ""),
            "top": cas.get("top", False),
            "review": cas.get("review", False),
            "subs": cas.get("subs", []),
            "source": "JCR" + ("/CAS" if cas else ""),
        }, issns, names)

    # 只在中科院表出现、JCR 未收录的期刊（多为暂无 IF 的新刊）
    for rec in cas_issn.values():
        key = id(rec)
        issns = sorted(set(cas_issns_by_rec.get(key, [])))
        if not issns or any(i in issn_index for i in issns):
            continue
        names = sorted(set(cas_names_by_rec.get(key, [])))
        push({
            "name": names[0].upper() if names else "",
            "issn": issns,
            "if": None,
            "q": "",
            "cats": [],
            "zone": rec.get("zone"),
            "zone_name": rec.get("zone_name", ""),
            "zone_rank": rec.get("zone_rank", ""),
            "top": rec.get("top", False),
            "review": rec.get("review", False),
            "subs": rec.get("subs", []),
            "source": "CAS",
        }, issns, names)

    with_if = sum(1 for j in journals if j["if"] is not None)
    with_zone = sum(1 for j in journals if j["zone"])

    payload = {
        "meta": {
            "if_edition": JCR_EDITION,
            "zone_edition": CAS_EDITION,
            "built_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "journal_count": len(journals),
            "with_impact_factor": with_if,
            "with_cas_zone": with_zone,
            "issn_count": len(issn_index),
            "name_count": len(name_index),
            "sources": [
                "Clarivate JCR 2025（影响因子与 JCR 分区 Q1–Q4）",
                "中国科学院文献情报中心《国际期刊预警名单》配套分区表升级版 2025（大类分区 / Top）",
                "原始 CSV 随 hitfyd/ShowJCR 项目公开发布",
            ],
        },
        "journals": journals,
        "issn_index": issn_index,
        "name_index": name_index,
    }

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))

    size = os.path.getsize(OUTPUT) / 1024 / 1024
    print(f"\n[OK ] 已写出 {OUTPUT}")
    print(f"     期刊 {len(journals)} 条（有 IF {with_if}、有中科院分区 {with_zone}）")
    print(f"     ISSN 索引 {len(issn_index)}、期刊名索引 {len(name_index)}")
    print(f"     文件大小 {size:.2f} MB")


if __name__ == "__main__":
    main()
