@echo off
rem Download the raw JCR / CAS journal-rank CSVs used by tools\build_journal_metrics.py
chcp 65001 >nul
cd /d %~dp0..

set VERSION=2026-1.2
set BASE=https://cdn.jsdelivr.net/gh/hitfyd/ShowJCR@%VERSION%/%%E4%%B8%%AD%%E7%%A7%%91%%E9%%99%%A2%%E5%%88%%86%%E5%%8C%%BA%%E8%%A1%%A8%%E5%%8F%%8AJCR%%E5%%8E%%9F%%E5%%A7%%8B%%E6%%95%%B0%%E6%%8D%%AE%%E6%%96%%87%%E4%%BB%%B6

if not exist "data\source" mkdir "data\source"

echo [1/2] JCR 2025 (impact factor + JCR quartile) ...
curl -L -o "data\source\JCR2025-UTF8.csv" "%BASE%/JCR2025-UTF8.csv"

echo [2/2] CAS journal rank 2025 (zone) ...
curl -L -o "data\source\FQBJCR2025-UTF8.csv" "%BASE%/FQBJCR2025-UTF8.csv"

echo.
echo Done. Now run:  python tools\build_journal_metrics.py
pause
