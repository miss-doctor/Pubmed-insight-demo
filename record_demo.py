#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright automation: record a demo video + capture all required screenshots.

针对 Vue 3 版前端（构建产物位于 static/dist，由 Flask 托管）。

Outputs -> attachment/
  demo_video.webm                 screen recording of the working demo
  screenshot_demo_full.png        full-page screenshot of the demo
  screenshot_01_home.png          landing page
  screenshot_02_stats.png         statistics + charts
  screenshot_02b_partition.png    JCR quartile + CAS zone charts & source note
  screenshot_03_top100.png        impact-factor TOP 100 table
  screenshot_04_report.png        auto-generated Chinese review
  screenshot_05_second_query.png  second keyword result
  screenshot_source_pubmed.png    DATA SOURCE: PubMed search result page
  screenshot_source_api.png       DATA SOURCE: raw PubMed E-utilities JSON
"""

import os
import time

import requests
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5000"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "attachment")
VIDEO_RAW = os.path.join(OUT, "video_raw")
os.makedirs(VIDEO_RAW, exist_ok=True)

KEYWORD = "CAR-T therapy"
KEYWORD2 = "Alzheimer disease"

# Vue 3 版选择器
SEL_INPUT = ".search-input-wrap input"
SEL_SUBMIT = ".btn-primary"
SEL_DONE = "#section-papers"


def launch_browser(p):
    """Prefer the system Chrome/Edge; fall back to bundled Chromium."""
    last_err = None
    for channel in ("chrome", "msedge", None):
        try:
            if channel:
                return p.chromium.launch(headless=True, channel=channel,
                                         args=["--hide-scrollbars", "--force-device-scale-factor=1"])
            return p.chromium.launch(headless=True, args=["--hide-scrollbars"])
        except Exception as e:
            last_err = e
            continue
    raise last_err


def smooth_scroll(page, steps=16, delay=0.55):
    height = page.evaluate("document.body.scrollHeight")
    viewport = page.evaluate("window.innerHeight")
    max_scroll = max(1, height - viewport)
    step = max(1, max_scroll // steps)
    pos = 0
    for _ in range(steps):
        pos = min(pos + step, max_scroll)
        page.evaluate(f"window.scrollTo({{top:{pos}, behavior:'smooth'}})")
        time.sleep(delay)
    page.evaluate("window.scrollTo({top:0, behavior:'smooth'})")
    time.sleep(delay)


def do_search(page, keyword):
    page.fill(SEL_INPUT, "")
    page.click(SEL_INPUT)
    for ch in keyword:
        page.type(SEL_INPUT, ch, delay=40)
    time.sleep(0.6)
    page.click(SEL_SUBMIT)
    page.wait_for_selector(SEL_DONE, timeout=180_000)
    time.sleep(2.2)


def run():
    with sync_playwright() as p:
        browser = launch_browser(p)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1,
            record_video_dir=VIDEO_RAW,
            record_video_size={"width": 1440, "height": 900},
        )
        page = context.new_page()

        # ---------- 1) Landing ----------
        page.goto(BASE, wait_until="networkidle")
        time.sleep(2.0)
        page.screenshot(path=os.path.join(OUT, "screenshot_01_home.png"))

        # ---------- 2) First search: CAR-T therapy ----------
        do_search(page, KEYWORD)

        # section: statistics + charts（题面 ①）
        page.evaluate("document.querySelector('#section-stats').scrollIntoView({block:'start'})")
        time.sleep(1.4)
        page.screenshot(path=os.path.join(OUT, "screenshot_02_stats.png"))

        # 分区详细截图：JCR Q1–Q4 + 中科院 1–4 区 + 数据来源说明
        # 这是笔试反馈中被重点指出的部分，单独出一张图便于评审查看
        page.evaluate("document.querySelector('.metrics-note').scrollIntoView({block:'center'})")
        time.sleep(1.4)
        page.screenshot(path=os.path.join(OUT, "screenshot_02b_partition.png"))

        # 分区导航跳转（Vue 版新增交互）
        page.evaluate("document.querySelector('.section-nav').scrollIntoView({block:'start'})")
        time.sleep(1.0)
        page.click(".nav-pill:nth-child(2)")          # ② 词云与方向
        time.sleep(1.6)
        page.click(".nav-pill:nth-child(1)")          # ① 统计与图表
        time.sleep(1.4)

        # full walkthrough scroll (captured in video)
        smooth_scroll(page, steps=16, delay=0.5)

        # full-page screenshot of the entire demo
        page.evaluate("window.scrollTo(0,0)")
        time.sleep(1.0)
        page.screenshot(path=os.path.join(OUT, "screenshot_demo_full.png"), full_page=True)

        # TOP 100 table + 表格筛选交互
        page.eval_on_selector(".paper-table", "el => el.closest('.panel').scrollIntoView({block:'start'})")
        time.sleep(1.4)
        page.screenshot(path=os.path.join(OUT, "screenshot_03_top100.png"))

        page.fill(".table-tools input[type='text']", "CD19")
        time.sleep(1.2)
        page.fill(".table-tools input[type='text']", "")
        time.sleep(0.8)

        # report
        page.eval_on_selector("#section-review", "el => el.scrollIntoView({block:'start'})")
        time.sleep(1.4)
        page.screenshot(path=os.path.join(OUT, "screenshot_04_report.png"))

        # back to top（Vue 版新增交互）
        page.click(".back-to-top")
        time.sleep(1.5)

        # ---------- 3) Second search: Alzheimer disease ----------
        do_search(page, KEYWORD2)
        smooth_scroll(page, steps=8, delay=0.45)

        page.screenshot(path=os.path.join(OUT, "screenshot_05_second_query.png"))

        # ---------- 4) Data source: PubMed website ----------
        #  PubMed 前端对 headless browser 会弹出 Cloudflare 挑战页，
        #  因此用 requests 抓取原始 HTML，再本地渲染截图，确保显示真实结果。
        pubmed_url = "https://pubmed.ncbi.nlm.nih.gov/?term=" + KEYWORD.replace(" ", "+")
        resp = requests.get(
            pubmed_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/129.0.0.0 Safari/537.36"
                )
            },
            timeout=30,
        )
        resp.raise_for_status()
        pubmed_html_path = os.path.join(VIDEO_RAW, "pubmed_source.html")
        with open(pubmed_html_path, "w", encoding="utf-8") as f:
            f.write(resp.text)

        src = context.new_page()
        src.goto("file:///" + pubmed_html_path.replace("\\", "/"),
                 wait_until="networkidle", timeout=60_000)
        time.sleep(2.0)
        src.screenshot(path=os.path.join(OUT, "screenshot_source_pubmed.png"))
        time.sleep(0.5)
        src.close()

        # ---------- 5) Data source: raw API ----------
        #  把原始 JSON 包成一份简洁的说明页，避免浏览器自带 JSON 视图里的
        #  中文「美观输出」控件干扰，同时清晰展示请求 URL 与返回结构。
        api_url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
            "?db=pubmed&term=CAR-T+therapy&retmode=json&retmax=5"
        )
        api_resp = requests.get(api_url, timeout=30)
        api_resp.raise_for_status()
        api_json = api_resp.text
        api_html_path = os.path.join(VIDEO_RAW, "api_source.html")
        with open(api_html_path, "w", encoding="utf-8") as f:
            f.write(
                "<!DOCTYPE html><html><head>"
                "<meta charset='utf-8'>"
                "<title>PubMed E-utilities API 原始返回</title>"
                "<style>"
                "body{font-family:system-ui,-apple-system,sans-serif;margin:0;padding:40px;background:#f6f8fa;color:#24292f;}"
                ".wrap{max-width:1100px;margin:0 auto;background:#fff;border:1px solid #d0d7de;border-radius:8px;padding:28px;box-shadow:0 2px 8px rgba(0,0,0,.04);}"
                "h1{font-size:22px;margin:0 0 12px;color:#0969da;}"
                ".url{font-family:monospace;font-size:13px;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:10px 12px;word-break:break-all;margin-bottom:18px;color:#24292f;}"
                "pre{font-family:'SFMono-Regular',Consolas,monospace;font-size:13px;background:#f6f8fa;border:1px solid #d0d7de;border-radius:6px;padding:16px;overflow:auto;max-height:640px;line-height:1.5;}"
                ".badge{display:inline-block;font-size:12px;font-weight:600;padding:3px 10px;border-radius:12px;background:#ddf4ff;color:#0969da;margin-bottom:14px;}"
                "</style></head><body>"
                "<div class='wrap'>"
                "<div class='badge'>PubMed E-utilities / esearch.fcgi</div>"
                "<h1>原始 API 请求与返回示例</h1>"
                "<div class='url'>" + api_url + "</div>"
                "<pre>" + api_json.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + "</pre>"
                "</div></body></html>"
            )

        api = context.new_page()
        api.goto("file:///" + api_html_path.replace("\\", "/"),
                 wait_until="networkidle", timeout=60_000)
        time.sleep(1.2)
        api.screenshot(path=os.path.join(OUT, "screenshot_source_api.png"))
        api.close()

        # ---------- close -> video flushed ----------
        context.close()
        browser.close()

    # move produced video to artifacts/
    vids = [os.path.join(VIDEO_RAW, f) for f in os.listdir(VIDEO_RAW) if f.endswith(".webm")]
    if vids:
        vids.sort(key=os.path.getmtime)
        dst = os.path.join(OUT, "demo_video.webm")
        if os.path.exists(dst):
            os.remove(dst)
        os.rename(vids[-1], dst)
        print("VIDEO ->", dst)
    print("ALL DONE")


if __name__ == "__main__":
    run()
