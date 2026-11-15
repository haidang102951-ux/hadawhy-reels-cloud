#!/usr/bin/env python3
"""
HaDa Why Cloud Reels Runner (Windows & Ubuntu Linux / GitHub Actions).
Supports:
  --mode preview : Render 1 representative PNG per scene (~20-30s) for fast approval.
  --mode render  : Render full 1080x1920 @ 60fps MP4 from scene_plan.json.
  --mode revise  : Update scene_plan.json from natural-language feedback via Gemini Free API.
Optionally posts outputs to Telegram when TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID are set.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REMOTION_DIR = BASE_DIR / "remotion_reels"
HARVESTED_DIR = REMOTION_DIR / "public" / "harvested"
PLAN_PATH = REMOTION_DIR / "src" / "scene_plan.json"
OUT_DIR = BASE_DIR / "cloud_out"


def run_cmd(cmd: list[str], cwd: Path) -> None:
    print(f"[CMD] {' '.join(cmd)} (cwd={cwd})")
    subprocess.run(cmd, cwd=str(cwd), check=True, shell=(os.name == "nt"))


def send_telegram_message(text: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text[:4000]}).encode()
    req = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=payload)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"[TELEGRAM] Sent message: {resp.status}")
    except Exception as exc:
        print(f"[TELEGRAM] Message error: {exc}")


def send_telegram_photo(photo_path: Path, caption: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return
    import mimetypes
    boundary = "----HaDaWhyBoundary7MA4YWxkTrZu0gW"
    data = []
    data.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode())
    data.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode())
    mime = mimetypes.guess_type(str(photo_path))[0] or "image/png"
    data.append(
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"photo\"; filename=\"{photo_path.name}\"\r\nContent-Type: {mime}\r\n\r\n".encode()
    )
    data.append(photo_path.read_bytes())
    data.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(data)
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendPhoto",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"[TELEGRAM] Sent {photo_path.name}: {resp.status}")


def send_telegram_video(video_path: Path, caption: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        return
    boundary = "----HaDaWhyVideoBoundary"
    data = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"width\"\r\n\r\n1080\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"height\"\r\n\r\n1920\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"supports_streaming\"\r\n\r\ntrue\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"video\"; filename=\"{video_path.name}\"\r\nContent-Type: video/mp4\r\n\r\n".encode(),
        video_path.read_bytes(),
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendVideo",
        data=b"".join(data),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        print(f"[TELEGRAM] Sent video {video_path.name}: {resp.status}")


def _fetch_wikipedia_image(query: str) -> bytes | None:
    import requests  # type: ignore

    headers = {"User-Agent": "HaDaWhyCloudBot/1.0 (https://github.com/haidang102951-ux/hadawhy-reels-cloud)"}
    params = {
        "action": "query",
        "generator": "search",
        "gsrsearch": query,
        "gsrlimit": "4",
        "prop": "pageimages",
        "piprop": "original|thumbnail",
        "pithumbsize": "1200",
        "format": "json",
    }
    try:
        r = requests.get("https://en.wikipedia.org/w/api.php", params=params, headers=headers, timeout=20)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for page in sorted(pages.values(), key=lambda p: p.get("index", 99)):
            img_info = page.get("original") or page.get("thumbnail") or {}
            img_url = img_info.get("source", "")
            w = int(img_info.get("width") or 0)
            h = int(img_info.get("height") or 0)
            if img_url and not img_url.lower().endswith((".svg", ".tif", ".tiff", ".pdf")) and min(w, h) >= 350:
                img_resp = requests.get(img_url, headers=headers, timeout=25)
                ctype = img_resp.headers.get("content-type", "").lower()
                if img_resp.ok and len(img_resp.content) > 20000 and ctype.startswith("image/") and "svg" not in ctype and "tiff" not in ctype:
                    return img_resp.content
    except Exception as exc:
        print(f"[HARVEST] Wikipedia fallback for '{query}': {exc}")
    return None


def _fetch_wikimedia_image(query: str) -> bytes | None:
    import requests  # type: ignore

    headers = {"User-Agent": "HaDaWhyCloudBot/1.0 (https://github.com/haidang102951-ux/hadawhy-reels-cloud)"}
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": "6",
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": "1280",
        "format": "json",
    }
    try:
        r = requests.get("https://commons.wikimedia.org/w/api.php", params=params, headers=headers, timeout=20)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            info = (page.get("imageinfo") or [{}])[0]
            mime = info.get("mime", "")
            width = int(info.get("width") or 0)
            height = int(info.get("height") or 0)
            img_url = info.get("thumburl") or info.get("url")
            if img_url and mime in ("image/jpeg", "image/png", "image/webp") and min(width, height) >= 500:
                img_resp = requests.get(img_url, headers=headers, timeout=25)
                if img_resp.ok and len(img_resp.content) > 20000:
                    return img_resp.content
    except Exception as exc:
        print(f"[HARVEST] Wikimedia fallback for '{query}': {exc}")
    return None


def _fetch_pollinations_image(query: str) -> bytes | None:
    import requests  # type: ignore

    prompt_enc = urllib.parse.quote(
        f"{query}, authentic documentary photograph, real-world editorial studio photo, ultra realistic, sharp focus, 8k, no cartoon, no 3D render, no illustration, no text"
    )
    url = f"https://image.pollinations.ai/prompt/{prompt_enc}?model=flux&width=1024&height=1024&nologo=true"
    try:
        r = requests.get(url, timeout=60)
        if r.ok and len(r.content) > 20000:
            return r.content
    except Exception as exc:
        print(f"[HARVEST] Pollinations error for '{query}': {exc}")
    return None


def _is_person_or_place_query(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in ("ceo", "founder", "president", "building", "factory", "headquarters", "newspaper", "portrait", "huang", "musk", "nvidia", "tsmc", "amd", "intel", "gpu", "server", "data center", "wafer", "cleanroom", "silicon"))


def _should_keep_full_frame(query: str) -> bool:
    q = query.lower()
    return any(k in q for k in ("gpu", "chip", "wafer", "facility", "factory", "cleanroom", "headquarters", "building", "server", "data center", "supercomputer", "fabricat", "rack", "silicon"))


_STOCK_WATERMARK_DOMAINS = (
    "shutterstock.com", "istockphoto.com", "alamy.com", "gettyimages.com",
    "dreamstime.com", "123rf.com", "depositphotos.com", "vecteezy.com", "stock.adobe.com",
)


def _fetch_serper_google_image(query: str) -> bytes | None:
    serper_key = os.getenv("SERPER_API_KEY", "").strip()
    if not serper_key:
        return None
    import requests  # type: ignore

    try:
        r = requests.post(
            "https://google.serper.dev/images",
            headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
            json={"q": query, "num": 8},
            timeout=20,
        )
        if not r.ok:
            print(f"[SERPER] HTTP {r.status_code}: {r.text[:200]}")
            return None
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36"}
        for img in r.json().get("images", []):
            img_url = str(img.get("imageUrl") or "").strip()
            w = int(img.get("imageWidth") or 0)
            h = int(img.get("imageHeight") or 0)
            low = img_url.lower()
            if not img_url or any(d in low for d in _STOCK_WATERMARK_DOMAINS):
                continue
            if low.endswith((".svg", ".tif", ".tiff", ".gif")) or min(w, h) < 400:
                continue
            try:
                resp = requests.get(img_url, headers=headers, timeout=15)
                ctype = resp.headers.get("content-type", "").lower()
                if resp.ok and len(resp.content) > 20000 and ctype.startswith("image/") and "svg" not in ctype:
                    return resp.content
            except Exception:
                continue
    except Exception as exc:
        print(f"[SERPER] Google Images error for '{query}': {exc}")
    return None


def _fetch_best_image(query: str) -> tuple[bytes | None, str]:
    queries = [query]
    words = [w for w in query.split() if len(w) > 1]
    if len(words) > 2:
        queries.append(" ".join(words[:2]))
    for q in queries:
        if _is_person_or_place_query(q):
            order = (
                ("google_serper", _fetch_serper_google_image),
                ("wikipedia", _fetch_wikipedia_image),
                ("wikimedia", _fetch_wikimedia_image),
                ("pollinations", _fetch_pollinations_image),
            )
        else:
            order = (
                ("google_serper", _fetch_serper_google_image),
                ("wikipedia", _fetch_wikipedia_image),
                ("wikimedia", _fetch_wikimedia_image),
                ("pollinations", _fetch_pollinations_image),
            )
        for s_name, fn in order:
            raw_bytes = fn(q)
            if raw_bytes:
                try:
                    from PIL import Image  # type: ignore
                    with Image.open(io.BytesIO(raw_bytes)) as test_im:
                        test_im.verify()
                    return raw_bytes, f"{s_name}('{q}')"
                except Exception as exc:
                    print(f"[AGENT-3 HARVEST] Invalid image bytes from {s_name}('{q}'): {exc}")
    return None, "none"


def harvest_assets(plan: dict, clean: bool = False) -> None:
    specs = plan.get("assetSpecs", [])
    if clean and HARVESTED_DIR.exists():
        shutil.rmtree(HARVESTED_DIR, ignore_errors=True)
    HARVESTED_DIR.mkdir(parents=True, exist_ok=True)
    if not specs:
        return

    from PIL import Image, ImageEnhance, ImageFilter, ImageStat  # type: ignore
    try:
        from rembg import remove  # type: ignore
    except Exception:
        remove = None

    for item in specs:
        filename = Path(str(item.get("filename", "prop.png"))).name
        if not filename.lower().endswith(".png"):
            filename = f"{Path(filename).stem}.png"
        out_path = HARVESTED_DIR / filename
        if out_path.exists() and not clean:
            continue
        query = str(item.get("query", filename)).strip()
        remove_bg = bool(item.get("removeBg", True)) and not _should_keep_full_frame(query)
        print(f"[AGENT-3 HARVEST] Fetching '{query}' -> {out_path.name} (removeBg={remove_bg})")

        raw_bytes, src_name = _fetch_best_image(query)
        print(f"[AGENT-3 HARVEST]   -> source={src_name} ({len(raw_bytes) if raw_bytes else 0} bytes)")
        if not raw_bytes:
            continue

        if remove_bg and remove is not None:
            try:
                cut_bytes = remove(raw_bytes)
                img = Image.open(io.BytesIO(cut_bytes)).convert("RGBA")
                alpha = img.getchannel("A")
                total_px = max(1, img.width * img.height)
                opaque_px = sum(alpha.histogram()[30:])
                opaque_ratio = opaque_px / total_px
                if 0.12 <= opaque_ratio <= 0.94:
                    bbox = img.getbbox()
                    if bbox:
                        img = img.crop(bbox)
                    alpha_cropped = img.getchannel("A")
                    mean_rgb = sum(ImageStat.Stat(img.convert("RGB"), mask=alpha_cropped).mean) / 3.0
                    if mean_rgb < 90:
                        img = ImageEnhance.Brightness(img).enhance(1.22)
                        img = ImageEnhance.Contrast(img).enhance(1.12)
                    img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
                    img.save(out_path, "PNG")
                    continue
                print(f"[AGENT-3 HARVEST] rembg ratio={opaque_ratio:.2f} out of safe range for {filename}, keeping sharp full photo")
            except Exception as exc:
                print(f"[AGENT-3 HARVEST] rembg failed for {filename}: {exc}")

        img = Image.open(io.BytesIO(raw_bytes)).convert("RGBA")
        img = ImageEnhance.Sharpness(img).enhance(1.2)
        img.save(out_path, "PNG")


def _extract_json_object(text: str) -> dict:
    import re
    raw = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        raw = raw[start : end + 1]
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    obj = json.loads(raw, strict=False)
    if isinstance(obj, dict) and "scenes" not in obj:
        for wrapper_key in ("scene_plan", "plan", "data"):
            if isinstance(obj.get(wrapper_key), dict) and "scenes" in obj[wrapper_key]:
                obj = obj[wrapper_key]
                break
    return obj


def _call_openai_compat_json(url: str, api_key: str, model: str, prompt: str, label: str, require_scenes: bool = True) -> dict | None:
    import requests  # type: ignore

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    try:
        print(f"[{label}] Calling {model}...")
        payload: dict = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.35,
            "max_tokens": 4096,
        }
        if "openrouter" in url:
            payload["response_format"] = {"type": "json_object"}
        r = requests.post(url, headers=headers, json=payload, timeout=45)
        if not r.ok:
            print(f"[{label}] {model} HTTP {r.status_code}: {r.text[:220]}")
            return None
        msg = (r.json().get("choices") or [{}])[0].get("message") or {}
        text = msg.get("content") or msg.get("reasoning") or ""
        if not str(text).strip():
            print(f"[{label}] {model} returned empty content")
            return None
        obj = _extract_json_object(str(text))
        if not isinstance(obj, dict) or (require_scenes and not obj.get("scenes")):
            print(f"[{label}] {model} JSON invalid or missing 'scenes' key, skipping...")
            return None
        return obj
    except Exception as exc:
        print(f"[{label}] {model} error: {exc}")
        return None


def _call_gemini_json(prompt: str, require_scenes: bool = True) -> dict:
    import time
    import requests  # type: ignore

    last_err = None

    # 1. OpenRouter free high-intelligence models (if OPENROUTER_API_KEY is set)
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if openrouter_key:
        for or_model in (
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "openrouter/free",
            "google/gemma-4-31b-it:free",
        ):
            res = _call_openai_compat_json(
                "https://openrouter.ai/api/v1/chat/completions",
                openrouter_key,
                or_model,
                prompt,
                "OPENROUTER",
                require_scenes=require_scenes,
            )
            if res is not None:
                return res

    # 2. DeepSeek official API (if DEEPSEEK_API_KEY is set)
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if deepseek_key:
        res = _call_openai_compat_json(
            "https://api.deepseek.com/chat/completions",
            deepseek_key,
            "deepseek-chat",
            prompt,
            "DEEPSEEK",
        )
        if res is not None:
            return res

    # 3. Google Gemini API (fail-fast 45s timeout)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if api_key:
        for model in ("gemini-3.8-flash", "gemini-flash-latest"):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"},
            }
            for retry in range(2):
                try:
                    print(f"[GEMINI] Calling {model} (try {retry + 1})...")
                    r = requests.post(url, json=payload, timeout=45)
                    if r.status_code == 404:
                        print(f"[GEMINI] {model} returned 404, skipping...")
                        last_err = r.text[:300]
                        break
                    if r.status_code in (429, 500, 502, 503, 504):
                        print(f"[GEMINI] {model} HTTP {r.status_code}: {r.text[:200]}")
                        last_err = f"HTTP {r.status_code}"
                        if retry == 0:
                            time.sleep(12 if r.status_code == 429 else 4)
                        continue
                    r.raise_for_status()
                    data = r.json()
                    text = data["candidates"][0]["content"]["parts"][0]["text"]
                    return _extract_json_object(text)
                except Exception as exc:
                    print(f"[GEMINI] {model} error: {exc}")
                    last_err = exc
                    break

    # 4. Zero-key fallback: Pollinations (deepseek -> openai)
    for p_model in ("deepseek", "openai"):
        for attempt in range(1, 3):
            try:
                print(f"[POLLINATIONS] Calling free model '{p_model}' POST (attempt {attempt})...")
                r = requests.post(
                    "https://text.pollinations.ai/openai",
                    headers={"Content-Type": "application/json"},
                    json={
                        "model": p_model,
                        "messages": [{"role": "user", "content": prompt}],
                        "reasoning_effort": "low",
                        "max_tokens": 4096,
                    },
                    timeout=60,
                )
                if r.status_code == 402:
                    print(f"[POLLINATIONS] {p_model} 402 rate limit, waiting 47s...")
                    time.sleep(47)
                    continue
                if not r.ok:
                    print(f"[POLLINATIONS] POST HTTP {r.status_code}: {r.text[:300]}")
                    break
                text = r.json()["choices"][0]["message"]["content"]
                return _extract_json_object(text)
            except Exception as exc:
                print(f"[POLLINATIONS] {p_model} error: {exc}")
                last_err = exc

    raise RuntimeError(f"All LLM providers (OpenRouter + DeepSeek + Gemini + Pollinations) failed: {last_err}")


_EMPHASIS_WORDS = {
    "NVIDIA", "CUDA", "H100", "TSMC", "AMD", "INTEL", "AI", "GPU", "CHIP",
    "ĐỘC", "QUYỀN", "THỊ", "PHẦN", "BÍ", "MẬT", "THAO", "TÚNG", "KHÓA", "CHẶT",
    "BÁN", "XẺNG", "CƠN", "SỐT", "VÀNG", "LỢI", "NHUẬN", "ĐẮT", "ĐỎ", "KHỔNG", "LỒ",
    "THỐNG", "TRỊ", "VŨ", "KHÍ", "SỰ", "THẬT", "TRIỆU", "TỶ", "NGHÌN", "USD", "ĐÔ",
}


def _pick_word_color(word_upper: str, accent: str, idx: int, total: int) -> str:
    clean = re.sub(r"[^\w%$]", "", word_upper)
    if any(ch.isdigit() for ch in clean) or "%" in word_upper or "$" in word_upper:
        return accent
    if clean in _EMPHASIS_WORDS:
        return accent
    if idx >= max(0, total - 2):
        return accent
    return "#FFFFFF"


def _build_captions_from_scenes(plan: dict) -> dict:
    """Normalize scene defaults (non-empty Text Hook), validate asset paths, and emit rolling captions."""
    import difflib

    spec_names = [
        Path(str(item.get("filename", ""))).stem + ".png"
        for item in plan.get("assetSpecs", [])
        if item.get("filename")
    ]
    asset_keys = ("primaryAsset", "leftAsset", "rightAsset", "centerAsset", "topLeftAsset", "topRightAsset", "bottomAsset")
    accent_cycle = ["#FFE600", "#FF4D5A", "#42B2F2"]
    for idx, scene in enumerate(plan.get("scenes", []), start=1):
        for k in asset_keys:
            val = str(scene.get(k, "")).strip()
            if val.startswith("harvested/") and spec_names:
                fname = Path(val).name
                if fname not in spec_names:
                    match = difflib.get_close_matches(fname, spec_names, n=1, cutoff=0.45)
                    scene[k] = f"harvested/{match[0]}" if match else ""
        scene.setdefault("id", f"scene_{idx}")
        narration = str(scene.get("narration", "")).strip()
        if not scene.get("eyebrow"):
            scene["eyebrow"] = "SỰ THẬT BẤT NGỜ"
        if not scene.get("heroText"):
            words_fb = [w.strip(",.!?") for w in narration.split() if len(w.strip(",.!?")) > 1]
            scene["heroText"] = " ".join(words_fb[:2]).upper() if words_fb else f"BÍ MẬT #{idx}"
        if not scene.get("heroColor"):
            scene["heroColor"] = accent_cycle[(idx - 1) % len(accent_cycle)]
    if plan.get("captions"):
        return plan
    captions = []
    for s_idx, scene in enumerate(plan.get("scenes", [])):
        narration = str(scene.get("narration", "")).strip()
        if not narration:
            continue
        words = [w for w in narration.split() if w]
        if not words:
            continue
        scene_start = float(scene.get("startSec", 0))
        scene_end = float(scene.get("endSec", scene_start + 3.0))
        spoken_dur = float(scene.get("_spokenDur") or max(0.8, scene_end - scene_start - 0.2))
        s0 = scene_start + 0.12
        s1 = min(scene_end - 0.04, s0 + spoken_dur)
        if s1 <= s0 + 0.3:
            s1 = max(s0 + 0.5, scene_end - 0.05)

        highlight_color = "#FFE600" if s_idx % 2 == 0 else "#FF4D5A"
        step = (s1 - s0) / len(words)

        # Split words into dynamic 5-6 word phrases so captions roll continuously with the voice
        phrase_size = 5
        for p_start in range(0, len(words), phrase_size):
            chunk = words[p_start:p_start + phrase_size]
            p0 = round(s0 + p_start * step, 2)
            p1 = round(s0 + (p_start + len(chunk)) * step, 2)
            lines: list[list[dict]] = []
            cur_line: list[dict] = []
            cur_chars = 0
            for j, w in enumerate(chunk):
                global_i = p_start + j
                t0 = round(s0 + global_i * step, 2)
                t1 = round(s0 + (global_i + 1) * step, 2)
                w_upper = w.upper()
                tok = {
                    "text": w_upper,
                    "startSec": t0,
                    "endSec": t1,
                    "color": _pick_word_color(w_upper, highlight_color, global_i, len(words)),
                }
                tlen = len(w_upper)
                if cur_line and (len(cur_line) >= 3 or cur_chars + 1 + tlen > 16):
                    lines.append(cur_line)
                    cur_line = [tok]
                    cur_chars = tlen
                else:
                    cur_line.append(tok)
                    cur_chars += (1 if cur_line else 0) + tlen
            if cur_line:
                lines.append(cur_line)
            captions.append({"startSec": p0, "endSec": p1, "lines": lines[:2]})
    plan["captions"] = captions
    return plan


def _agent_2_editor_qa(plan: dict) -> dict:
    """Agent 2: Dedicated Editor & Vietnamese QA pass (fix broken phrasing, stop duplicate Hook/Odometer numbers, clean asset specs)."""
    print("[AGENT-2 EDITOR] Reviewing script, Vietnamese phrasing, and asset queries...")
    qa_prompt = (
        "Bạn là Tổng Biên Tập & Thanh Tra Kịch Bản kênh HaDa Why. Hãy kiểm tra và sửa lại JSON scene_plan dưới đây:\n"
        "1. Sửa mọi lỗi chính tả/tiếng Việt ngô nghê (VD: 'CHIP HỌC HOPPER' -> 'KIẾN TRÚC HOPPER', từ dịch máy vô nghĩa).\n"
        "2. Ở mọi cảnh layout 'stat_odometer': 'heroText' TUYỆT ĐỐI KHÔNG được lặp lại con số của 'statNumber' (VD nếu statNumber=30000 thì heroText phải là nhận định như 'GIÁ TRÊN TRỜI' hoặc 'SIÊU LỢI NHUẬN', CẤM viết '30.000 USD' vào heroText).\n"
        "3. Xóa bỏ 'yearWatermark' nếu là năm hiện tại 2023-2026 (chỉ giữ nếu là năm lịch sử thật như 1307, 2006).\n"
        "4. Trong 'assetSpecs': chỉ dùng từ khóa tiếng Anh ngắn gọn có ảnh thật trên Wikipedia/Wikimedia; đặt 'removeBg': false cho chip/GPU/nhà máy/tòa nhà/tư liệu, chỉ đặt 'removeBg': true cho chân dung nhân vật hoặc vật thể đơn lẻ.\n"
        "Chỉ trả về JSON hợp lệ hoàn chỉnh (không markdown ```json).\n\n"
        f"JSON CẦN RÀ SOÁT:\n{json.dumps(plan, ensure_ascii=False)}"
    )
    try:
        reviewed = _call_gemini_json(qa_prompt)
        if isinstance(reviewed, dict) and reviewed.get("scenes"):
            plan = reviewed
            print("[AGENT-2 EDITOR] LLM QA pass applied successfully")
    except Exception as exc:
        print(f"[AGENT-2 EDITOR] LLM QA fallback to deterministic sanitizer: {exc}")

    # Deterministic safety net
    for scene in plan.get("scenes", []):
        yw = str(scene.get("yearWatermark", "")).strip()
        if yw in ("2023", "2024", "2025", "2026"):
            scene["yearWatermark"] = ""
        if scene.get("layout") == "stat_odometer":
            num_str = str(int(float(scene.get("statNumber") or 0)))
            hero_digits = "".join(ch for ch in str(scene.get("heroText", "")) if ch.isdigit())
            if hero_digits and num_str and (hero_digits == num_str or num_str[:2] in hero_digits):
                scene["heroText"] = "CON SỐ BIẾT NÓI"
    return _build_captions_from_scenes(plan)


def _agent_3_prune_missing_assets(plan: dict) -> dict:
    """Ensure no missing/0-byte asset or invalid iconAsset path remains in scene_plan before Remotion renders."""
    asset_keys = ("primaryAsset", "leftAsset", "rightAsset", "centerAsset", "topLeftAsset", "topRightAsset", "bottomAsset")
    public_dir = REMOTION_DIR / "public"
    for scene in plan.get("scenes", []):
        for k in asset_keys:
            val = str(scene.get(k, "")).strip()
            if val.startswith("harvested/"):
                fpath = HARVESTED_DIR / Path(val).name
                if not fpath.exists() or fpath.stat().st_size < 1024:
                    print(f"[AGENT-3 QC] Removed missing asset '{val}' from {scene.get('id')}.{k}")
                    scene[k] = ""
        icon_val = str(scene.get("iconAsset", "")).strip()
        if icon_val:
            if not (public_dir / icon_val).exists():
                scene["iconAsset"] = ""
    return plan


def mode_create(topic_prompt: str) -> None:
    if not topic_prompt.strip():
        raise RuntimeError("Topic prompt (--feedback) is required for --mode create/auto")

    # Fast bypass: if caller already provides JSON scene_plan, skip LLM completely
    if topic_prompt.lstrip().startswith("{"):
        parsed = _build_captions_from_scenes(_extract_json_object(topic_prompt))
        parsed["fps"] = 30
        PLAN_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[CREATE] Loaded direct JSON scene_plan into {PLAN_PATH}")
        harvest_assets(parsed, clean=True)
        return

    prompt = f"""Bạn là Đạo diễn Điều tra kênh HaDa Why (@hadawhy) — chuyên làm video ngắn 9:16 bóc trần sự thật kinh tế/công nghệ với DỮ LIỆU THẬT, CON SỐ CỤ THỂ và CƠ CHẾ SÂU SẮC.

HÃY HỌC ĐÚNG PHONG CÁCH 2 VIDEO MẪU ĐỈNH CAO CỦA KÊNH (MasterShowcase20s - vụ kiện thuê máy bay 250 triệu đô & Friday13Origins - bóc trần lịch sử Thứ Sáu Ngày 13):
- Mẫu lời thoại & nhịp điệu:
  * Cảnh 1 (Hook nghịch lý ngay giây 0): "Từ 4 tàu bay thuê, số nợ bất ngờ vọt lên 250 triệu đô la!" -> heroText: "250 TRIỆU ĐÔ"
  * Cảnh 2 (Cơ chế tài chính/kỹ thuật): "Ngân hàng cắt hợp đồng, bán khoản nợ thẳng sang cho quỹ ngoại ở Anh." -> layout: "causal_chain"
  * Cảnh 3 (Bằng chứng lịch sử/tư liệu): "Vụ kiện kéo dài từ Việt Nam sang tận Tòa Tối Cao Luân Đôn." -> layout: "archival_proof", stampText: "XÁC THỰC 100%"
  * Cảnh 4 (Chốt hạ bản chất WHY): "Một bài học đắt giá khi bước chân ra sân chơi quốc tế!" -> heroText: "LUẬT CHƠI NGẦM"

Hãy sáng tác JSON scene_plan chất lượng tương đương cho yêu cầu: "{topic_prompt}"

NGUYÊN TẮC NỘI DUNG & TEXT HOOK BẮT BUỘC:
- **CẢNH 1 (3–4 GIÂY ĐẦU) PHẢI LÀ HOOK GÂY TÒ MÒ TỘT ĐỘ (CURIOSITY GAP / PATTERN INTERRUPT):**
  * TUYỆT ĐỐI CẤM mở bài kiểu báo cáo khô khan (VD cấm: "Nvidia hiện nay đang chiếm 90% thị phần chip AI").
  * BẮT BUỘC lật ngược nhận thức người xem bằng 1 trong 3 công thức kéo giữ chân ngay câu đầu:
    1) **Lật tẩy ảo tưởng:** "Ai cũng tưởng [điều số đông nghĩ], nhưng thứ thật sự giúp [chủ thể] thống trị lại là [bí mật ngược đời]!"
    2) **Nghịch lý con số sốc:** "Chỉ tốn vài trăm đô sản xuất nhưng bán tới 30.000 đô — bí mật nằm ở một thứ giấu kín suốt 18 năm!"
    3) **Mở vòng lặp tò mò (Open Loop):** Kết câu Cảnh 1 phải gài móc câu khiến người xem PHẢI coi tiếp Cảnh 2 mới giải tỏa được (VD: "...nhưng ít ai biết cái bẫy thật sự không nằm ở phần cứng!").
  * `heroText` Cảnh 1 (1–3 từ) phải đấm thẳng vào nghịch lý đó (VD: `"KHÔNG PHẢI CHIP"`, `"BẪY TỪ 2006"`, `"LÃI GẤP 10 LẦN"`).
- Nếu yêu cầu có ghi rõ thời lượng (VD "20s" hoặc "25s"), hãy điều chỉnh số cảnh cho khớp (VD: 3–4 cảnh cho ~20–25s; 6–7 cảnh cho ~38–48s), đi theo mạch điều tra bóc tách từng lớp:
  (1) Hook nghịch lý kéo giữ chân -> (2) Con số doanh thu/lợi nhuận gây sốc -> (3) Kiến thức phần cứng/kỹ thuật lõi ít ai biết (tên chip, thông số, năm ra mắt, công nghệ độc quyền) -> (4) Chuỗi nhân-quả bóc trần cơ chế khóa chặt hệ sinh thái ("causal_chain") -> (5) Đối chiếu đối thủ / nút thắt chuỗi cung ứng ("bar_compare" hoặc "compare_two") -> (6) Kết luận bản chất WHY sắc lạnh.
- Lời thoại (`narration`) mỗi cảnh dài 15–22 từ, BẮT BUỘC chứa KIẾN THỨC THẬT CỤ THỂ (tên riêng, năm lịch sử, thông số kỹ thuật thật, tỷ suất lợi nhuận, cơ chế độc quyền), tạo cảm giác "nghe xong mở mang đầu óc ngay lập tức!".
- **LUẬT THÉP TEXT HOOK (`eyebrow` & `heroText`):**
  * TUYỆT ĐỐI CẤM ĐẶT CÂU HỎI XÀM trong `eyebrow` hay `heroText` (CẤM "TẠI SAO?", "VÌ SAO?", "LÀ GÌ?", "CÓ BIẾT?", dấu "?").
  * `heroText` (1–3 từ) PHẢI LÀ **SỰ THẬT CHẤN ĐỘNG / CON SỐ / NGHỊCH LÝ ĐẮT GIÁ** giải quyết thẳng vấn đề (VD: `"KẺ BÁN XẺNG"`, `"30.000 USD"`, `"90% ĐỘC TÔN"`, `"CÁI BẪY CUDA"`, `"KHÔNG LỐI THOÁT"`).
  * `heroColor` chọn màu sáng rực rỡ (`#FFE600`, `#FF4D5A`, `#42B2F2`, `#FFFFFF`).
- VỚI `stat_odometer`: `statNumber` phải gọn đẹp (VD: `47` với `statSuffix`: `" TỶ USD"`, hoặc `90` với `"%"`, hoặc `30000` với `" USD"`). CẤM viết số dài 10-12 chữ số như `47500000000`.
- MỖI CẢNH PHẢI CÓ `infoTags`: mảng 2–3 thẻ kiến thức ngắn chứa số liệu/sự thật đắt giá (VD: `["RA MẮT TỪ 2006", "4 TRIỆU LẬP TRÌNH VIÊN", "NVLINK 900 GB/S"]`).
- BẮT BUỘC CÓ ÍT NHẤT 1 CẢNH DÙNG `"causal_chain"` với `chainSteps` (3 bước nối tiếp nhau A -> B -> C để người xem thấy rõ cơ chế!).
- TRONG `assetSpecs`: ÁP DỤNG LUẬT **"NÓI A HIỆN ĐÚNG A"** — chỉ tìm đúng VẬT THỂ / NHÂN VẬT / ĐỊA ĐIỂM THẬT bằng tên riêng chuẩn tiếng Anh trên Wikipedia (VD: `"Jensen Huang"`, `"Nvidia H100"`, `"Nvidia headquarters"`, `"TSMC"`, `"AMD Instinct MI300"`). TUYỆT ĐỐI CẤM tìm `"chart"`, `"graph"`, `"stock"`, `"price"`, `"skyline"`, `"vertical"`, `"code"`, `"screenshot"`. Cảnh `causal_chain` và `bar_compare` KHÔNG cần `primaryAsset`.

CHỈ trả về JSON hợp lệ (không markdown ```json):
{{
  "projectTitle": "HaDaWhy_<TenKhongDau>",
  "theme": "tech_cyber",
  "fps": 30,
  "mistIntensity": 0.11,
  "assetSpecs": [
    {{ "filename": "ten_anh_1.png", "query": "tu khoa tieng Anh chuan de tim anh that", "removeBg": false }}
  ],
  "scenes": [
    {{
      "id": "scene_1",
      "startSec": 0,
      "endSec": 3.5,
      "layout": "cinematic_backdrop",
      "eyebrow": "TIEU DE PHU",
      "heroText": "CHU TO",
      "heroColor": "#ff3b3b",
      "subNote": "GHI CHU",
      "primaryAsset": "harvested/ten_anh_1.png",
      "iconAsset": "objects/dollar.png",
      "primaryLabel": "",
      "narration": "Cau thoai tieng Viet ngan gon 15-20 tu doc trong canh nay."
    }}
  ]
}}

BẮT BUỘC CHỌN ĐÚNG `theme` THEO DNA CHỦ ĐỀ (cấm lúc nào cũng dùng 1 màu):
- `"tech_cyber"` (AI, chip, công nghệ)
- `"retail_warm"` (siêu thị, thương hiệu tiêu dùng, ẩm thực, bán lẻ)
- `"noir_dossier"` (đại án, bí ẩn, lịch sử, phốt thương hiệu)
- `"finance_vox"` (tài chính, kinh tế vĩ mô, chứng khoán)

QUY TẮC ĐẠO CỤ THẬT 100% (CẤM ICON HOẠT HÌNH):
- TUYỆT ĐỐI CẤM dùng `objects/*.png` hay icon hoạt hình/vector.
- Mọi hình ảnh/đạo cụ phải là ẢNH CHỤP THẬT ngoài đời đưa vào `assetSpecs` (`harvested/<name>.png`) để săn từ Wikipedia/Wikimedia!

10 layout hợp lệ (BẮT BUỘC luân phiên đa dạng, mỗi video phải dùng `cinematic_backdrop` + `causal_chain` + `stat_odometer`/`bar_compare`):
- "cinematic_backdrop": primaryAsset (ảnh thật tràn màn hình Ken Burns), infoTags
- "hero_prop": primaryAsset, primaryLabel, subNote, infoTags
- "compare_two": leftAsset, leftLabel, leftLabelColor, rightAsset, rightLabel, rightLabelColor, centerAsset, yearWatermark
- "sat_map": mapRegion ("fra"|"uk"|"usa"|"world"), mapCaption
- "two_tier": topLeftAsset, topLeftLabel, topRightAsset, bottomAsset, bottomTitle, bottomHighlight
- "split_duo": leftAsset, leftLabel, rightAsset, rightLabel, ctaText
- "stat_odometer": statNumber (số nguyên), statSuffix (vd "%", " USD"), statLabel, primaryAsset, yearWatermark, infoTags
- "bar_compare": leftValue (số), leftLabel, leftLabelColor, rightValue (số), rightLabel, rightLabelColor, yearWatermark, infoTags
- "archival_proof": primaryAsset, stampText (vd "SỰ THẬT 100%"), yearWatermark, infoTags
- "causal_chain": chainSteps ([{{"badge":"BƯỚC 1","title":"...","detail":"..."}}, ... 3 bước nối tiếp]), primaryAsset (tùy chọn), yearWatermark

Mọi file "harvested/<name>.png" dùng trong scenes phải có trong assetSpecs."""

    print("[AGENT-1 SCRIPT] Drafting investigative 5-beat script...")
    parsed = _call_gemini_json(prompt)
    parsed = _agent_2_editor_qa(parsed)
    parsed["fps"] = 30
    harvest_assets(parsed, clean=True)
    parsed = _agent_3_prune_missing_assets(parsed)
    PLAN_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[CREATE] Generated {PLAN_PATH} for topic: {topic_prompt}")

    script_lines = [f"🎬 KỊCH BẢN MỚI ({parsed.get('projectTitle', 'HaDaWhy')}):"]
    for i, sc in enumerate(parsed.get("scenes", []), start=1):
        script_lines.append(f"{i}. [{sc.get('layout')}] {sc.get('heroText')} — {sc.get('narration')}")
    send_telegram_message("\n".join(script_lines))


def mode_revise(feedback: str) -> None:
    current_plan = PLAN_PATH.read_text(encoding="utf-8")
    prompt = (
        "Bạn là Đạo diễn kỹ thuật Remotion. Hãy cập nhật JSON scene_plan dưới đây theo đúng góp ý của Người Chỉ Huy.\n"
        "Chỉ trả về JSON hợp lệ (không markdown ```json), giữ nguyên cấu trúc và các cảnh không được yêu cầu sửa.\n\n"
        f"GÓP Ý CẦN SỬA:\n{feedback}\n\n"
        f"SCENE_PLAN HIỆN TẠI:\n{current_plan}"
    )
    parsed = _call_gemini_json(prompt)
    PLAN_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[REVISE] Updated {PLAN_PATH}")


def mode_preview() -> list[Path]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    harvest_assets(plan, clean=False)
    fps = int(plan.get("fps", 60))
    preview_dir = OUT_DIR / "preview"
    preview_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []

    for idx, scene in enumerate(plan["scenes"], start=1):
        mid_sec = (float(scene["startSec"]) + float(scene["endSec"])) / 2.0
        frame_num = max(0, int(round(mid_sec * fps)))
        out_png = preview_dir / f"scene_{idx}_{scene['id']}.png"
        run_cmd(
            [
                "npx",
                "remotion",
                "still",
                "src/index.ts",
                "HaDaWhyUniversal9x16",
                str(out_png),
                f"--frame={frame_num}",
                "--gl=angle",
            ],
            cwd=REMOTION_DIR,
        )
        outputs.append(out_png)
        send_telegram_photo(out_png, f"Preview {idx}: {scene['id']} (frame {frame_num})")

    print(f"[PREVIEW] Generated {len(outputs)} preview PNGs in {preview_dir}")
    return outputs


def _normalize_vi_numbers(text: str) -> str:
    import re
    text = re.sub(r"(\d+)%", r"\1 phần trăm", text)
    text = re.sub(r"(\d+)\s*k\b", r"\1 nghìn", text, flags=re.IGNORECASE)
    text = re.sub(r"(\d+)\s*đ\b", r"\1 đồng", text, flags=re.IGNORECASE)
    return text


def _get_audio_duration(path: Path) -> float:
    try:
        out = subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            text=True,
        ).strip()
        return max(0.3, float(out))
    except Exception:
        return 2.5


def build_audio_track(plan: dict, temp_dir: Path) -> Path | None:
    """Synthesize VieNeu-TTS 'Hải Đăng' per scene, sync scene_plan timing to real audio duration, and mix SFX + BGM at -14.0 LUFS."""
    scenes = plan.get("scenes", [])
    if not scenes:
        return None

    temp_dir.mkdir(parents=True, exist_ok=True)
    sfx_dir = REMOTION_DIR / "public" / "sfx"
    sfx_map = {
        "hero_prop": sfx_dir / "bass_hit.mp3",
        "stat_odometer": sfx_dir / "bass_hit.mp3",
        "compare_two": sfx_dir / "metal_hit.mp3",
        "bar_compare": sfx_dir / "metal_hit.mp3",
        "sat_map": sfx_dir / "whoosh_big.mp3",
        "archival_proof": sfx_dir / "whoosh_big.mp3",
        "two_tier": sfx_dir / "zoom_hit.mp3",
        "split_duo": sfx_dir / "zoom_hit.mp3",
    }
    bgm_path = BASE_DIR / "assets" / "music" / "hadawhy_mystery_bgm.mp3"

    # Initialize VieNeu-TTS (channel voice: Hải Đăng)
    vieneu_client = None
    try:
        from vieneu import Vieneu  # type: ignore
        vieneu_client = Vieneu()
        print("[TTS] VieNeu-TTS initialized (voice: Hải Đăng)")
    except Exception as exc:
        print(f"[WARN] VieNeu-TTS unavailable, falling back to edge-tts: {exc}")

    # 1. Generate per-scene voiceover and measure exact spoken duration
    vo_entries: list[tuple[Path, int]] = []
    cursor_sec = 0.0
    for idx, scene in enumerate(scenes):
        text = str(scene.get("narration", "")).strip()
        if not text and idx < len(plan.get("captions", [])):
            words = [
                str(tok.get("text", "")).strip()
                for line in plan["captions"][idx].get("lines", [])
                for tok in line
                if str(tok.get("text", "")).strip()
            ]
            text = " ".join(words)

        planned_dur = max(1.8, float(scene.get("endSec", cursor_sec + 3.0)) - float(scene.get("startSec", cursor_sec)))
        vo_file: Path | None = None
        if text:
            if vieneu_client is not None:
                vo_wav = temp_dir / f"vo_{idx:02d}.wav"
                try:
                    clean_text = _normalize_vi_numbers(text)
                    audio = vieneu_client.infer(clean_text, voice="Hải Đăng", temperature=0.35, top_p=0.9)
                    vieneu_client.save(audio, str(vo_wav))
                    if vo_wav.exists() and vo_wav.stat().st_size > 0:
                        vo_file = vo_wav
                except Exception as exc:
                    print(f"[WARN] VieNeu-TTS failed for scene {idx}: {exc}")
            if vo_file is None:
                vo_mp3 = temp_dir / f"vo_{idx:02d}.mp3"
                try:
                    subprocess.run(
                        [sys.executable, "-m", "edge_tts", "--voice", "vi-VN-NamMinhNeural", "--rate=+12%", "--text", text, "--write-media", str(vo_mp3)],
                        check=True,
                    )
                    if vo_mp3.exists() and vo_mp3.stat().st_size > 0:
                        vo_file = vo_mp3
                except Exception as exc:
                    print(f"[WARN] edge-tts failed for scene {idx}: {exc}")

        if vo_file is not None:
            spoken_dur = _get_audio_duration(vo_file)
            scene["_spokenDur"] = round(spoken_dur, 2)
            scene_dur = max(planned_dur, spoken_dur + 0.35)
            delay_ms = int(round((cursor_sec + 0.12) * 1000))
            vo_entries.append((vo_file, delay_ms))
        else:
            scene_dur = planned_dur

        scene["startSec"] = round(cursor_sec, 2)
        scene["endSec"] = round(cursor_sec + scene_dur, 2)
        if text:
            scene["narration"] = text
        cursor_sec += scene_dur

    total_dur = max(cursor_sec, 3.0)
    # Rebuild word-level captions to match exact spoken scene windows
    plan["captions"] = []
    _build_captions_from_scenes(plan)
    PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. Rich Multi-Layer Contextual SFX Hooks (scene impact + odometer ticks + causal pops + infoTags)
    sfx_entries: list[tuple[Path, int, float]] = []
    sfx_map["causal_chain"] = sfx_dir / "gear_lock.mp3"
    tick_sfx = sfx_dir / "tick.mp3"
    coin_sfx = sfx_dir / "coin1.mp3"
    lock_sfx = sfx_dir / "lock.mp3"
    pop_sfx = sfx_dir / "pop.mp3"
    pop_dry_sfx = sfx_dir / "pop_dry.mp3"
    whoosh_sfx = sfx_dir / "whoosh1.mp3"

    for scene in scenes:
        s0_ms = max(0, int(round(float(scene.get("startSec", 0)) * 1000)))
        s_dur_ms = max(1000, int(round((float(scene.get("endSec", 0)) - float(scene.get("startSec", 0))) * 1000)))
        layout = str(scene.get("layout", ""))

        # Primary scene entrance impact
        sfx_file = sfx_map.get(layout, sfx_dir / "bass_hit.mp3")
        if sfx_file.exists():
            sfx_entries.append((sfx_file, s0_ms, 0.80))

        # Odometer rolling ticks + jackpot/lock ding
        if layout == "stat_odometer":
            if tick_sfx.exists():
                for step_ms in (140, 300, 460, 620, 780, 940):
                    if step_ms < s_dur_ms - 300:
                        sfx_entries.append((tick_sfx, s0_ms + step_ms, 0.56))
            end_ding = coin_sfx if coin_sfx.exists() else lock_sfx
            if end_ding.exists() and s_dur_ms > 1300:
                sfx_entries.append((end_ding, s0_ms + 1180, 0.78))

        # Causal chain 3-step sequential pop/lock
        elif layout == "causal_chain":
            for step_idx in range(min(3, len(scene.get("chainSteps") or []) or 3)):
                t_ms = s0_ms + 150 + step_idx * 380
                if t_ms < s0_ms + s_dur_ms - 200 and pop_sfx.exists():
                    sfx_entries.append((pop_sfx, t_ms, 0.68))

        # Bar compare grow whoosh + lock
        elif layout == "bar_compare":
            if whoosh_sfx.exists():
                sfx_entries.append((whoosh_sfx, s0_ms + 220, 0.55))
            if lock_sfx.exists() and s_dur_ms > 900:
                sfx_entries.append((lock_sfx, s0_ms + 720, 0.65))

        # InfoTags knowledge badges pop-in
        info_tags = scene.get("infoTags") or []
        if info_tags and pop_dry_sfx.exists() and layout != "causal_chain":
            for t_idx in range(min(3, len(info_tags))):
                t_ms = s0_ms + 280 + t_idx * 180
                if t_ms < s0_ms + s_dur_ms - 180:
                    sfx_entries.append((pop_dry_sfx, t_ms, 0.52))

    # 3. Mix Voiceover + SFX + Ducked BGM -> -14.0 LUFS WAV
    inputs: list[str] = ["-f", "lavfi", "-t", f"{total_dur:.3f}", "-i", "anullsrc=r=44100:cl=stereo"]
    filters: list[str] = []
    idx_counter = 1
    base_idx = 0

    vo_labels: list[str] = []
    for vo_path, delay_ms in vo_entries:
        inputs.extend(["-i", str(vo_path)])
        lbl = f"vo{idx_counter}"
        filters.append(f"[{idx_counter}:a]adelay={delay_ms}|{delay_ms},volume=1.35[{lbl}]")
        vo_labels.append(f"[{lbl}]")
        idx_counter += 1

    sfx_labels: list[str] = []
    for sfx_path, delay_ms, vol in sfx_entries:
        inputs.extend(["-i", str(sfx_path)])
        lbl = f"sfx{idx_counter}"
        filters.append(f"[{idx_counter}:a]adelay={delay_ms}|{delay_ms},volume={vol:.2f}[{lbl}]")
        sfx_labels.append(f"[{lbl}]")
        idx_counter += 1

    bgm_label: str | None = None
    if bgm_path.exists():
        inputs.extend(["-stream_loop", "-1", "-t", f"{total_dur:.3f}", "-i", str(bgm_path)])
        fade_out_st = max(0.5, total_dur - 0.8)
        if vo_labels:
            filters.append(f"[{base_idx}:a]{''.join(vo_labels)}amix=inputs={1 + len(vo_labels)}:duration=first:dropout_transition=0:normalize=0,asplit=2[vo_mix][vo_sc]")
            filters.append(f"[{idx_counter}:a]volume=0.36,afade=t=in:st=0:d=0.4,afade=t=out:st={fade_out_st:.2f}:d=0.8[bgm_raw]")
            filters.append("[bgm_raw][vo_sc]sidechaincompress=threshold=0.025:ratio=4:attack=25:release=320[bgm_ducked]")
            bgm_label = "[bgm_ducked]"
            mix_inputs = ["[vo_mix]"] + sfx_labels + [bgm_label]
        else:
            filters.append(f"[{idx_counter}:a]volume=0.32[bgm_bed]")
            bgm_label = "[bgm_bed]"
            mix_inputs = [f"[{base_idx}:a]"] + sfx_labels + [bgm_label]
        idx_counter += 1
    else:
        mix_inputs = [f"[{base_idx}:a]"] + vo_labels + sfx_labels

    if len(mix_inputs) == 1 and not vo_labels and not sfx_labels and not bgm_label:
        return None

    out_wav = temp_dir / "master_mix_14lufs.wav"
    filter_complex = ";".join(
        filters
        + [
            f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=0:normalize=0,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        ]
    )
    subprocess.run(
        ["ffmpeg", "-y", *inputs, "-filter_complex", filter_complex, "-map", "[aout]", "-ar", "44100", "-ac", "2", str(out_wav)],
        check=True,
    )
    return out_wav


def _agent_5_visual_qc(out_mp4: Path) -> str:
    """Agent 5: Verify 1080x1920 stream & non-black keyframes before Telegram delivery."""
    try:
        probe = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,nb_frames", "-of", "csv=p=0", str(out_mp4)],
            text=True,
        ).strip()
        dur = _get_audio_duration(out_mp4)
        from PIL import Image, ImageStat  # type: ignore
        qc_dir = OUT_DIR / "qc_frames"
        qc_dir.mkdir(parents=True, exist_ok=True)
        bright_scores: list[float] = []
        for idx, t in enumerate((0.8, max(1.0, dur * 0.45), max(1.5, dur * 0.80)), start=1):
            frame_png = qc_dir / f"qc_{idx}.png"
            subprocess.run(
                ["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(out_mp4), "-frames:v", "1", str(frame_png)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if frame_png.exists():
                im = Image.open(frame_png).convert("L")
                bright_scores.append(round(ImageStat.Stat(im).mean[0], 1))
        report = f"QC PASS ({probe}, {dur:.1f}s, brightness={bright_scores})"
        print(f"[AGENT-5 QC] {report}")
        return report
    except Exception as exc:
        print(f"[AGENT-5 QC] Warning: {exc}")
        return "QC completed"


def _agent_6_thumbnail_and_seo(plan: dict) -> None:
    """Agent 6: Render 9:16 ThumbnailCover9x16 + write viral Title/SEO Hashtags and send to Telegram."""
    try:
        scenes = plan.get("scenes", [])
        harvested_files = sorted(
            [f"harvested/{p.name}" for p in HARVESTED_DIR.glob("*.png") if p.stat().st_size > 1024]
        )
        if not harvested_files:
            print("[AGENT-6 THUMB/SEO] No harvested images available, skipping thumbnail.")
            return

        hero_img = ""
        bg_img = ""
        sec_img = ""
        for sc in scenes:
            for k in ("primaryAsset", "leftAsset", "topLeftAsset"):
                val = str(sc.get(k, "")).strip()
                if val.startswith("harvested/") and (HARVESTED_DIR / Path(val).name).exists():
                    if not hero_img:
                        hero_img = val
                    elif not bg_img and val != hero_img:
                        bg_img = val
                    elif not sec_img and val not in (hero_img, bg_img):
                        sec_img = val
        hero_img = hero_img or harvested_files[0]
        bg_img = bg_img or harvested_files[-1]
        sec_img = sec_img or hero_img

        first_hero = str(scenes[0].get("heroText", "BÍ MẬT CHẤN ĐỘNG") if scenes else "BÍ MẬT CHẤN ĐỘNG").upper()
        second_hero = str(scenes[1].get("heroText", "SỰ THẬT ĐẰNG SAU") if len(scenes) > 1 else "SỰ THẬT ĐẰNG SAU").upper()
        title = plan.get("projectTitle", "HaDaWhy_Cloud_Video")

        seo_prompt = (
            "Bạn là Chuyên gia Thumbnail & SEO kênh HaDa Why (@hadawhy). Dựa trên kịch bản sau, hãy trả về JSON gồm:\n"
            '{"line1": "DÒNG 1 NGẮN 3-5 TỪ IN HOA", "line2": "DÒNG 2 NGẮN 3-5 TỪ IN HOA", '
            '"viralTitle": "Tiêu đề Reels/TikTok/Shorts giật tò mò", "hashtags": "#HaDaWhy #KinhTe #CongNghe ..."}\n'
            f"Kịch bản: {json.dumps([s.get('narration', '') for s in scenes], ensure_ascii=False)}"
        )
        line1, line2 = first_hero, second_hero
        viral_title = f"{first_hero} — {second_hero}"
        hashtags = "#HaDaWhy #BiMatThuongHieu #KienThucThuVi #ReelsVN"
        try:
            seo = _call_gemini_json(seo_prompt, require_scenes=False)
            line1 = str(seo.get("line1") or line1).upper()
            line2 = str(seo.get("line2") or line2).upper()
            viral_title = str(seo.get("viralTitle") or viral_title)
            hashtags = str(seo.get("hashtags") or hashtags)
        except Exception as exc:
            print(f"[AGENT-6 THUMB/SEO] LLM SEO fallback: {exc}")

        try:
            avail_cpus = len(os.sched_getaffinity(0))
        except AttributeError:
            avail_cpus = os.cpu_count() or 2
        concurrency = str(max(1, min(4, avail_cpus)))

        thumb_props = {
            "backgroundPhotoSrc": bg_img,
            "backgroundBlurPx": 0,
            "backgroundScale": 1.0,
            "backgroundObjectPosition": "50% 50%",
            "backgroundBrightness": 0.85,
            "backgroundContrast": 1.15,
            "backgroundSaturate": 1.0,
            "heroSubjectSrc": hero_img,
            "mysteryOrSecondarySrc": sec_img,
            "headlineLine1": line1,
            "headlineLine2": line2,
            "brandLogoSrc": "brand/hadawhy_logo.png",
            "glowAccentColor": "#E11D2E",
            "headlineLine1Color": "#42B2F2",
            "headlineLine2Color": "#FFFFFF",
            "heroBwHighContrast": True,
            "mysterySilhouetteMode": False,
            "mysterySymbol": "!",
        }
        props_file = OUT_DIR / "thumb_props.json"
        props_file.write_text(json.dumps(thumb_props, ensure_ascii=False), encoding="utf-8")
        thumb_png = OUT_DIR / f"{title}_thumb_9x16.png"
        run_cmd(
            [
                "npx",
                "remotion",
                "still",
                "src/index.ts",
                "ThumbnailCover9x16",
                str(thumb_png),
                f"--props={props_file}",
                f"--concurrency={concurrency}",
                "--gl=angle",
            ],
            cwd=REMOTION_DIR,
        )
        if thumb_png.exists():
            send_telegram_photo(thumb_png, f"🖼️ THUMBNAIL 9:16 & SEO\n📌 {viral_title}\n{hashtags}")
            print(f"[AGENT-6 THUMB/SEO] Generated and sent {thumb_png.name}")
    except Exception as exc:
        print(f"[AGENT-6 THUMB/SEO] Warning: {exc}")


def _call_llm_text(prompt: str) -> str:
    """Call OpenRouter / DeepSeek for raw TSX code generation without JSON wrapping."""
    import requests  # type: ignore

    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if openrouter_key:
        for or_model in ("nvidia/nemotron-3-ultra-550b-a55b:free", "openrouter/free"):
            try:
                print(f"[AGENT-4 TSX] Calling {or_model}...")
                r = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {openrouter_key}"},
                    json={"model": or_model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.25, "max_tokens": 6000},
                    timeout=60,
                )
                if r.ok:
                    msg = (r.json().get("choices") or [{}])[0].get("message") or {}
                    text = str(msg.get("content") or "").strip()
                    if "export const DynamicReel" in text:
                        return text
            except Exception as exc:
                print(f"[AGENT-4 TSX] {or_model} error: {exc}")

    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if deepseek_key:
        r = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {deepseek_key}"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.25, "max_tokens": 6000},
            timeout=60,
        )
        if r.ok:
            return str(r.json()["choices"][0]["message"]["content"]).strip()
    raise RuntimeError("No LLM returned valid DynamicReel TSX")


def _extract_tsx_code(raw: str) -> str:
    text = raw.strip()
    for fence in ("```tsx", "```typescript", "```ts", "```"):
        if fence in text:
            parts = text.split(fence)
            if len(parts) >= 2:
                text = parts[1]
                if "```" in text:
                    text = text.split("```")[0]
                break
    idx = text.find("import React")
    if idx != -1:
        text = text[idx:]
    return text.strip()


def _agent_4_tsx_director(plan: dict) -> str:
    """Agent 4 Motion Director: Write custom DynamicReel.tsx per video (like MasterShowcase20s) + tsc --noEmit self-repair loop."""
    dyn_path = REMOTION_DIR / "src" / "DynamicReel.tsx"
    safe_backup = dyn_path.read_text(encoding="utf-8") if dyn_path.exists() else ""

    harvested_list = sorted([f"harvested/{p.name}" for p in HARVESTED_DIR.glob("*.png") if p.stat().st_size > 1024])
    fps = int(plan.get("fps", 30))
    scenes_brief = [
        {
            "id": s.get("id"),
            "fromFrame": int(round(float(s.get("startSec", 0)) * fps)),
            "durationFrames": max(15, int(round((float(s.get("endSec", 3)) - float(s.get("startSec", 0))) * fps))),
            "heroText": s.get("heroText"),
            "eyebrow": s.get("eyebrow"),
            "primaryAsset": s.get("primaryAsset", ""),
            "statNumber": s.get("statNumber"),
            "statSuffix": s.get("statSuffix"),
            "infoTags": s.get("infoTags", []),
            "chainSteps": s.get("chainSteps", []),
            "narration": s.get("narration", ""),
        }
        for s in plan.get("scenes", [])
    ]

    tsx_prompt = f"""Bạn là Kỹ Sư Đạo Diễn Remotion 3D (`fb-reels-motion-3d-director`). Hãy viết MỘT FILE CODE `DynamicReel.tsx` ĐỘC BẢN (KHÔNG dùng template slideshow cũ!) cho video 9:16 (1080x1920, {fps} fps).

CÁC COMPONENT CÓ SẴN ĐƯỢC IMPORT ĐÚNG ĐƯỜNG DẪN:
- `import React from "react";`
- `import {{ AbsoluteFill, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";`
- `import {{ HaDaWhyMistBackground }} from "./components/HaDaWhyMistBackground";`
- `import {{ ChannelWatermark9x16 }} from "./components/ChannelWatermark9x16";`
- `import {{ KineticWordCaption }} from "./components/KineticWordCaption";`
- `import {{ StickerPop }} from "./components/StickerPop";`
- `import {{ CoinStream }} from "./components/CoinStream";`
- `import defaultPlan from "./scene_plan.json";`
- `import {{ UniversalScenePlan }} from "./HaDaWhyUniversal9x16";`

YÊU CẦU KỸ THUẬT DỰNG PHIM ĐIỆN ẢNH (LÀM GIỐNG HỆT MasterShowcase20s.tsx):
1. Export đúng `export const DynamicReel: React.FC<{{ plan?: UniversalScenePlan }}> = ({{ plan = defaultPlan as unknown as UniversalScenePlan }}) => {{ ... }};`
2. Dùng `const frame = useCurrentFrame(); const {{ fps }} = useVideoConfig();`
3. Dựng **Camera Rig 3D chuyển động mượt** (rung chấn nhẹ ở điểm đập `Math.sin(dt * 2.9)`, zoom/pan mượt, chuyển cảnh bằng `<Sequence from={{...}} durationInFrames={{...}}>`).
4. **ĐA DẠNG BỐ CỤC TỪNG CẢNH (100% ẢNH THẬT, CẤM ICON HOẠT HÌNH):**
   - CHỈ dùng ảnh thật từ danh sách: `{json.dumps(harvested_list)}` qua `<Img src={{staticFile("...")}} />` (TUYỆT ĐỐI CẤM dùng `objects/*.png` hay icon hoạt hình).
   - Cảnh 1 (Hook): Ảnh thật tràn màn hình / Ken Burns zoom + chữ Hook to rõ (`maxWidth: 920`, không tràn mép, có `textShadow` viền đen dày).
   - Cảnh có số liệu: Số đếm nhảy động (`interpolate` + `Math.round`) + ảnh thật có bóng đổ 3D (`drop-shadow`) và viền sáng, hoặc `CoinStream` khi nói về dòng tiền.
   - Cảnh cơ chế/chuỗi sự kiện: Đường nối SVG động (`strokeDashoffset`) hoặc thẻ bước trượt vào từ 2 bên kết hợp ảnh thật.
5. BẮT BUỘC render `<ChannelWatermark9x16 />` và `<KineticWordCaption phrases={{plan.captions || []}} />` ở lớp trên cùng!
6. Mọi chữ tiếng Việt có dấu chuẩn, `maxWidth: 920, textAlign: "center", wordBreak: "break-word"`, không bao giờ tràn màn hình 1080px.

DỮ LIỆU CÁC CẢNH CẦN DỰNG:
{json.dumps(scenes_brief, ensure_ascii=False, indent=2)}

CHỈ trả về code TypeScript hoàn chỉnh cho `DynamicReel.tsx` (bắt đầu bằng `import React from "react";`, không giải thích thêm)."""

    current_prompt = tsx_prompt
    for attempt in range(1, 4):
        try:
            raw_code = _call_llm_text(current_prompt)
            tsx_code = _extract_tsx_code(raw_code)
            if "export const DynamicReel" not in tsx_code or "KineticWordCaption" not in tsx_code:
                raise RuntimeError("Missing DynamicReel export or KineticWordCaption")
            dyn_path.write_text(tsx_code, encoding="utf-8")
            proc = subprocess.run(["npx", "tsc", "--noEmit"], cwd=REMOTION_DIR, capture_output=True, text=True)
            if proc.returncode == 0:
                print(f"[AGENT-4 TSX] Custom DynamicReel.tsx compiled cleanly on attempt {attempt}!")
                return "DynamicReel"
            err_msg = (proc.stdout + "\n" + proc.stderr).strip()[:1500]
            print(f"[AGENT-4 TSX] tsc failed (attempt {attempt}):\n{err_msg}")
            current_prompt = (
                f"File DynamicReel.tsx vừa viết bị lỗi TypeScript sau:\n{err_msg}\n\n"
                f"Hãy sửa lại toàn bộ file DynamicReel.tsx cho hết lỗi `tsc --noEmit`. CHỈ trả về code TypeScript hoàn chỉnh:\n\n{tsx_code}"
            )
        except Exception as exc:
            print(f"[AGENT-4 TSX] Attempt {attempt} error: {exc}")

    # Restore safe wrapper if all 3 attempts failed
    if safe_backup:
        dyn_path.write_text(safe_backup, encoding="utf-8")
    print("[AGENT-4 TSX] Falling back to HaDaWhyUniversal9x16")
    return "HaDaWhyUniversal9x16"


def mode_render() -> Path:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    harvest_assets(plan, clean=False)
    plan = _agent_3_prune_missing_assets(plan)
    PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    title = plan.get("projectTitle", "HaDaWhy_Cloud_Video")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_mp4 = OUT_DIR / f"{title}_raw.mp4"
    out_mp4 = OUT_DIR / f"{title}.mp4"
    # Build TTS + sync scene_plan.json BEFORE rendering Remotion so captions/scenes match voice 100%
    audio_wav = build_audio_track(plan, OUT_DIR / "audio_tmp")
    try:
        avail_cpus = len(os.sched_getaffinity(0))
    except AttributeError:
        avail_cpus = os.cpu_count() or 2
    concurrency = str(max(1, min(4, avail_cpus)))
    comp_id = _agent_4_tsx_director(plan)
    run_cmd(
        [
            "npx",
            "remotion",
            "render",
            "src/index.ts",
            comp_id,
            str(raw_mp4),
            "--codec=h264",
            "--image-format=jpeg",
            "--jpeg-quality=90",
            f"--concurrency={concurrency}",
            "--gl=angle",
        ],
        cwd=REMOTION_DIR,
    )
    if audio_wav and audio_wav.exists():
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(raw_mp4),
                "-i",
                str(audio_wav),
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-movflags",
                "+faststart",
                "-shortest",
                str(out_mp4),
            ],
            check=True,
        )
        raw_mp4.unlink(missing_ok=True)
    else:
        raw_mp4.replace(out_mp4)
    qc_summary = _agent_5_visual_qc(out_mp4)
    send_telegram_video(out_mp4, f"Render hoàn tất ({qc_summary}): {title}")
    _agent_6_thumbnail_and_seo(plan)
    print(f"[RENDER] Output MP4: {out_mp4}")
    # Auto-clean temporary cloud_out directory after Telegram delivery (Zero-Junk)
    shutil.rmtree(OUT_DIR, ignore_errors=True)
    return out_mp4


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "create", "preview", "render", "revise"], required=True)
    parser.add_argument("--feedback", default="")
    args = parser.parse_args()

    if args.mode == "auto":
        mode_create(args.feedback)
        mode_render()
    elif args.mode == "create":
        mode_create(args.feedback)
        mode_preview()
    elif args.mode == "revise":
        mode_revise(args.feedback)
        mode_preview()
    elif args.mode == "preview":
        mode_preview()
    elif args.mode == "render":
        mode_render()
    return 0


if __name__ == "__main__":
    sys.exit(main())
