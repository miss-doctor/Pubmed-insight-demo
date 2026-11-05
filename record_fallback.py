#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fallback demo-video generator (no Playwright ffmpeg needed).

Drives the app with Playwright, captures a continuous sequence of frames while
performing the demo actions, then assembles them into an MP4 with imageio-ffmpeg.

Output: artifacts/demo_video.mp4
"""

import os
import io
import time
import glob
import shutil

import imageio.v2 as imageio
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:5000"
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "artifacts")
FRAMES = os.path.join(OUT, "frames")
FPS = 8

os.makedirs(OUT, exist_ok=True)
if os.path.exists(FRAMES):
    shutil.rmtree(FRAMES)
os.makedirs(FRAMES, exist_ok=True)

counter = {"n": 0}


def grab(page):
    """Capture one frame."""
    counter["n"] += 1
    path = os.path.join(FRAMES, f"f{counter['n']:05d}.png")
    try:
        page.screenshot(path=path)
    except Exception:
        pass


def hold(page, seconds):
    """Hold the current view while grabbing frames at FPS."""
    n = max(1, int(seconds * FPS))
    for _ in range(n):
        grab(page)
        time.sleep(1.0 / FPS)


def scroll_through(page, seconds=8):
    steps = max(1, int(seconds * FPS))
    height = page.evaluate("document.body.scrollHeight")
    viewport = page.evaluate("window.innerHeight")
    max_scroll = max(1, height - viewport)
    for i in range(steps):
        pos = int(max_scroll * i / steps)
        page.evaluate(f"window.scrollTo(0,{pos})")
        grab(page)
        time.sleep(1.0 / FPS)


def launch_browser(p):
    for channel in ("chrome", "msedge", None):
        try:
            return p.chromium.launch(headless=True, channel=channel) if channel else p.chromium.launch(headless=True)
        except Exception:
            continue
    raise RuntimeError("no browser")


def run():
    with sync_playwright() as p:
        browser = launch_browser(p)
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
        page = ctx.new_page()

        page.goto(BASE, wait_until="networkidle")
        hold(page, 2.0)

        # search
        page.fill("#keyword", "")
        page.click("#keyword")
        for ch in "CAR-T therapy":
            page.type("#keyword", ch, delay=30)
        hold(page, 1.0)
        page.click("#searchBtn")
        page.wait_for_selector("#results:not(.hidden)", timeout=180_000)
        hold(page, 2.5)

        scroll_through(page, 10)
        page.evaluate("window.scrollTo(0,0)")
        hold(page, 1.2)
        scroll_through(page, 10)

        ctx.close()
        browser.close()

    # assemble
    files = sorted(glob.glob(os.path.join(FRAMES, "*.png")))
    print("frames:", len(files))
    out_mp4 = os.path.join(OUT, "demo_video.mp4")
    writer = imageio.get_writer(out_mp4, fps=FPS, codec="libx264", quality=8,
                                macro_block_size=None)
    target = (1440, 900)
    for f in files:
        img = Image.open(f).convert("RGB")
        if img.size != target:
            img = img.resize(target, Image.LANCZOS)
        writer.append_data(bytearray(img.tobytes()) and __import__("numpy").array(img))
    writer.close()
    shutil.rmtree(FRAMES, ignore_errors=True)
    print("VIDEO ->", out_mp4)


if __name__ == "__main__":
    run()
