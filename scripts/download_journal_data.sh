#!/usr/bin/env bash
# 下载 tools/build_journal_metrics.py 所需的原始 CSV。
# 数据来源：hitfyd/ShowJCR（公开发布）经 jsDelivr CDN 拉取。
set -euo pipefail

VERSION="${VERSION:-2026-1.2}"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/data/source"
mkdir -p "$DIR"

# "中科院分区表及JCR原始数据文件" 目录名的 URL 编码
CN="$(printf '中科院分区表及JCR原始数据文件' | jq -sRr @uri)"
BASE="https://cdn.jsdelivr.net/gh/hitfyd/ShowJCR@${VERSION}/${CN}"

echo "[1/2] JCR 2025 (影响因子 + JCR 分区) ..."
curl -fL -o "${DIR}/JCR2025-UTF8.csv" "${BASE}/JCR2025-UTF8.csv"

echo "[2/2] 中科院分区表升级版 2025 (大类分区 / Top) ..."
curl -fL -o "${DIR}/FQBJCR2025-UTF8.csv" "${BASE}/FQBJCR2025-UTF8.csv"

echo
echo "Done. 下一步： python tools/build_journal_metrics.py"
