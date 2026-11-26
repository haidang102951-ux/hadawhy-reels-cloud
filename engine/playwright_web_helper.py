# -*- coding: utf-8 -*-
r"""
playwright_web_helper.py - Đọc trang web JS & chụp ảnh bằng chứng báo chí siêu nét bằng Playwright
Cách dùng:
  python playwright_web_helper.py read --url "https://..." --max-chars 6000
  python playwright_web_helper.py capture --url "https://..." --out "D:\DuAn_DangLam\...\evidence.png"
"""
import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")


def _open_page(pw, url: str, width: int = 1280, height: int = 900, timeout_ms: int = 25000):
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": width, "height": height},
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        ),
        locale="vi-VN",
    )
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
    try:
        page.wait_for_load_state("networkidle", timeout=6000)
    except Exception:
        page.wait_for_timeout(1500)
    return browser, page


def cmd_read(url: str, max_chars: int) -> dict:
    with sync_playwright() as pw:
        browser, page = _open_page(pw, url)
        try:
            title = page.title()
            text = page.evaluate(
                """() => {
                    const drop = document.querySelectorAll('script, style, noscript, nav, footer, aside, iframe');
                    drop.forEach(el => el.remove());
                    const main = document.querySelector('article, main, [role="main"]') || document.body;
                    return (main ? main.innerText : '').replace(/\\n{3,}/g, '\\n\\n').trim();
                }"""
            )
            return {
                "ok": True,
                "url": page.url,
                "title": title,
                "chars": len(text),
                "text": text[:max_chars],
            }
        finally:
            browser.close()


def cmd_capture(url: str, out_path: Path, width: int, height: int, full_page: bool) -> dict:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser, page = _open_page(pw, url, width=width, height=height)
        try:
            page.screenshot(path=str(out_path), full_page=full_page)
            return {
                "ok": True,
                "url": page.url,
                "title": page.title(),
                "saved": str(out_path),
                "bytes": out_path.stat().st_size,
            }
        finally:
            browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description="Playwright helper cho Biên kịch & Trinh sát FB Reels")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_read = sub.add_parser("read", help="Đọc nội dung trang web nặng JS")
    p_read.add_argument("--url", required=True)
    p_read.add_argument("--max-chars", type=int, default=6000)

    p_cap = sub.add_parser("capture", help="Chụp ảnh màn hình bài báo / số liệu thật")
    p_cap.add_argument("--url", required=True)
    p_cap.add_argument("--out", required=True)
    p_cap.add_argument("--width", type=int, default=1280)
    p_cap.add_argument("--height", type=int, default=900)
    p_cap.add_argument("--full-page", action="store_true")

    args = ap.parse_args()
    if args.cmd == "read":
        res = cmd_read(args.url, args.max_chars)
    else:
        res = cmd_capture(args.url, Path(args.out), args.width, args.height, args.full_page)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
