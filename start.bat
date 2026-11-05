@echo off
chcp 65001 >nul
cd /d %~dp0

echo ============================================
echo   PubMed 科研情报分析平台 - Demo 启动脚本
echo ============================================
echo.

echo [1/3] 安装 / 校验 Python 依赖...
python -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo [X] 依赖安装失败，请检查 Python 与网络后重试。
    pause
    exit /b 1
)

echo [2/3] 校验期刊指标库（JCR 2025 + 中科院分区表 2025）...
if not exist "data\journal_metrics.json" (
    python tools\build_journal_metrics.py
    if errorlevel 1 (
        echo [X] 期刊指标库构建失败，请先执行 scripts\download_journal_data.bat 下载原始数据。
        pause
        exit /b 1
    )
)

echo [3/3] 启动服务 http://127.0.0.1:5000
echo.
echo 浏览器将自动打开，如未打开请手动访问 http://127.0.0.1:5000
start "" http://127.0.0.1:5000
python app.py
pause
