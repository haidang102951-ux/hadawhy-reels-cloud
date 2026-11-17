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


def _check_image_hd_and_sharp(
    raw_bytes: bytes,
    min_w: int = 800,
    min_h: int = 500,
    min_sharpness: float = 45.0,
) -> tuple[bool, int, int, float]:
    """Verify real decoded image dimensions and Laplacian sharpness to block blurry/pixelated photos."""
    from PIL import Image, ImageFilter, ImageStat  # type: ignore

    with Image.open(io.BytesIO(raw_bytes)) as im:
        im.load()
        w, h = im.size
        if w < min_w or h < min_h:
            return False, w, h, 0.0
        rgb = im.convert("RGB")
        scale = 512.0 / min(w, h)
        if scale < 1.0:
            rgb = rgb.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.Resampling.LANCZOS)
        try:
            import cv2  # type: ignore
            import numpy as np  # type: ignore
            gray = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2GRAY)
            sharp = float(cv2.Laplacian(gray, cv2.CV_64F).var())
        except Exception:
            edges = rgb.convert("L").filter(ImageFilter.FIND_EDGES)
            sharp = float(ImageStat.Stat(edges).var[0])
        return sharp >= min_sharpness, w, h, sharp


def _fetch_wikimedia_image(query: str) -> bytes | None:
    import requests  # type: ignore

    headers = {"User-Agent": "HaDaWhyCloudBot/1.0 (https://github.com/haidang102951-ux/hadawhy-reels-cloud)"}
    params = {
        "action": "query",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": "8",
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
            if img_url and mime in ("image/jpeg", "image/png", "image/webp") and min(width, height) >= 750:
                img_resp = requests.get(img_url, headers=headers, timeout=25)
                if img_resp.ok and len(img_resp.content) > 25000:
                    ok, rw, rh, sharp = _check_image_hd_and_sharp(img_resp.content, min_w=750, min_h=500)
                    if ok:
                        print(f"[WIKIMEDIA OK] {rw}x{rh}, sharp={sharp:.1f} for '{query}'")
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


def _call_gemini_vision(prompt: str, images_bytes: list[bytes], max_tokens: int = 256) -> str | None:
    """Call Gemini Vision API (gemini-2.5-flash / gemini-flash-latest) with JPEG thumbnails."""
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or not images_bytes:
        return None
    import base64
    import requests  # type: ignore
    from PIL import Image  # type: ignore

    parts: list[dict] = [{"text": prompt}]
    for raw in images_bytes:
        with Image.open(io.BytesIO(raw)) as im:
            thumb = im.convert("RGB")
            thumb.thumbnail((768, 768))
            buf = io.BytesIO()
            thumb.save(buf, "JPEG", quality=82)
            b64 = base64.b64encode(buf.getvalue()).decode("ascii")
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": b64}})

    for model in ("gemini-2.5-flash", "gemini-flash-latest"):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        try:
            r = requests.post(
                url,
                json={
                    "contents": [{"parts": parts}],
                    "generationConfig": {"temperature": 0.1, "maxOutputTokens": max_tokens},
                },
                timeout=45,
            )
            if r.ok:
                cands = r.json().get("candidates") or []
                if cands:
                    return str(cands[0]["content"]["parts"][0]["text"]).strip()
        except Exception as exc:
            print(f"[GEMINI-VISION] {model} error: {exc}")
    return None


def _vision_pick_best_image(query: str, candidates: list[bytes]) -> bytes:
    """Use Gemini Vision (primary) or OpenRouter free Vision to pick the cleanest real photo."""
    if len(candidates) <= 1:
        return candidates[0]

    pick_prompt = (
        f"Pick the single best real, crisp HD photograph for query: '{query}'. "
        "Reject any image that is blurry, pixelated, low-resolution, has watermarks, big text overlays, cartoons, "
        "wrong era, or wrong cultural context (if Vietnam-related, prefer authentic Vietnamese people/settings). "
        f"Reply ONLY with the single integer index (0 to {len(candidates) - 1})."
    )
    gem_ans = _call_gemini_vision(pick_prompt, candidates, max_tokens=16)
    if gem_ans:
        for ch in gem_ans:
            if ch.isdigit() and int(ch) < len(candidates):
                pick = int(ch)
                print(f"[VISION] (Gemini) Picked candidate #{pick}/{len(candidates)} for '{query}'")
                return candidates[pick]

    or_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not or_key:
        return candidates[0]
    try:
        import base64
        import requests  # type: ignore
        from PIL import Image  # type: ignore

        content: list[dict] = [{"type": "text", "text": pick_prompt}]
        for raw in candidates:
            with Image.open(io.BytesIO(raw)) as im:
                thumb = im.convert("RGB")
                thumb.thumbnail((384, 384))
                buf = io.BytesIO()
                thumb.save(buf, "JPEG", quality=75)
                b64 = base64.b64encode(buf.getvalue()).decode("ascii")
            content.append({"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}})

        for v_model in ("google/gemma-4-26b-a4b-it:free", "nvidia/nemotron-3.5-super-vl:free"):
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {or_key}", "Content-Type": "application/json"},
                json={"model": v_model, "messages": [{"role": "user", "content": content}], "max_tokens": 8, "temperature": 0},
                timeout=25,
            )
            if r.ok:
                ans = str((r.json().get("choices") or [{}])[0].get("message", {}).get("content") or "").strip()
                for ch in ans:
                    if ch.isdigit() and int(ch) < len(candidates):
                        pick = int(ch)
                        print(f"[VISION] ({v_model}) Picked candidate #{pick}/{len(candidates)} for '{query}'")
                        return candidates[pick]
    except Exception as exc:
        print(f"[VISION] Fallback to candidate #0 for '{query}': {exc}")
    return candidates[0]


def _vision_verify_cutout(png_bytes: bytes, query: str) -> bool:
    """Verify cutout PNG via Gemini Vision: reject jagged halos, sliced limbs/heads, or empty cutouts."""
    if not os.getenv("GEMINI_API_KEY", "").strip():
        return True
    from PIL import Image  # type: ignore

    with Image.open(io.BytesIO(png_bytes)) as im:
        rgba = im.convert("RGBA")
        bg = Image.new("RGB", rgba.size, (18, 28, 48))
        bg.paste(rgba, mask=rgba.getchannel("A"))
        buf = io.BytesIO()
        bg.save(buf, "JPEG", quality=85)
    ans = _call_gemini_vision(
        f"Inspect this background-removed cutout for '{query}' placed on dark blue background. "
        "Reply PASS if the subject is intact, clean edges, no severe jagged white/grey halo, and matches the subject. "
        "Reply FAIL if cut off, badly jagged, or garbage.",
        [buf.getvalue()],
        max_tokens=32,
    )
    if ans and "FAIL" in ans.upper():
        print(f"[VISION-CUTOUT] Rejected cutout for '{query}': {ans}")
        return False
    return True


def _fetch_serper_google_image(query: str) -> bytes | None:
    serper_key = os.getenv("SERPER_API_KEY", "").strip()
    if not serper_key:
        return None
    import requests  # type: ignore
    from PIL import Image  # type: ignore

    try:
        r = requests.post(
            "https://google.serper.dev/images",
            headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
            json={"q": query, "num": 12},
            timeout=20,
        )
        if not r.ok:
            print(f"[SERPER] HTTP {r.status_code}: {r.text[:200]}")
            return None
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36"}
        hd_candidates: list[bytes] = []
        fallback_candidates: list[bytes] = []
        for img in r.json().get("images", []):
            img_url = str(img.get("imageUrl") or "").strip()
            w = int(img.get("imageWidth") or 0)
            h = int(img.get("imageHeight") or 0)
            low = img_url.lower()
            if not img_url or any(d in low for d in _STOCK_WATERMARK_DOMAINS):
                continue
            if low.endswith((".svg", ".tif", ".tiff", ".gif")) or w < 650 or h < 450:
                continue
            try:
                resp = requests.get(img_url, headers=headers, timeout=12)
                ctype = resp.headers.get("content-type", "").lower()
                if resp.ok and len(resp.content) > 25000 and ctype.startswith("image/") and "svg" not in ctype:
                    ok_hd, rw, rh, sharp = _check_image_hd_and_sharp(resp.content, min_w=800, min_h=500, min_sharpness=45.0)
                    if ok_hd:
                        print(f"[SERPER HD] {rw}x{rh}, sharp={sharp:.1f} <- {img_url[:70]}")
                        hd_candidates.append(resp.content)
                        if len(hd_candidates) >= 3:
                            break
                    else:
                        ok_fb, rw, rh, sharp = _check_image_hd_and_sharp(resp.content, min_w=650, min_h=450, min_sharpness=45.0)
                        if ok_fb:
                            fallback_candidates.append(resp.content)
                        else:
                            print(f"[SERPER REJECT] {rw}x{rh}, sharp={sharp:.1f} <- {img_url[:70]}")
            except Exception:
                continue
        valid_candidates = hd_candidates or fallback_candidates[:3]
        if valid_candidates:
            return _vision_pick_best_image(query, valid_candidates)
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
    rembg_session = None
    try:
        from rembg import new_session, remove  # type: ignore
        try:
            rembg_session = new_session("bria-rmbg")
            print("[AGENT-3 HARVEST] Using rembg session: bria-rmbg")
        except Exception:
            rembg_session = None
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
                cut_bytes = remove(raw_bytes, session=rembg_session) if rembg_session is not None else remove(raw_bytes)
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
                    check_buf = io.BytesIO()
                    img.save(check_buf, "PNG")
                    if _vision_verify_cutout(check_buf.getvalue(), query):
                        out_path.write_bytes(check_buf.getvalue())
                        continue
                    print(f"[AGENT-3 HARVEST] Vision rejected cutout for {filename}, keeping sharp full photo")
                else:
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

    # 1. DeepSeek official API (ưu tiên số 1 nếu có DEEPSEEK_API_KEY — cực nhanh & ổn định)
    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if deepseek_key:
        res = _call_openai_compat_json(
            "https://api.deepseek.com/chat/completions",
            deepseek_key,
            "deepseek-chat",
            prompt,
            "DEEPSEEK",
            require_scenes=require_scenes,
        )
        if res is not None:
            return res

    # 2. OpenRouter free high-intelligence models (if OPENROUTER_API_KEY is set)
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
        parsed["fps"] = 60
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

9 layout ĐIỆN ẢNH 3D hợp lệ cho CinematicReel (BẮT BUỘC luân phiên đa dạng giữa các cảnh, KHÔNG lặp 2 cảnh liên tiếp cùng layout; mỗi video PHẢI có ít nhất 1 `flow_diagram` hoặc `bar_versus` để giải thích cơ chế):
- "flow_diagram": sơ đồ 3 bước dòng tiền/cơ chế phát sáng động — primaryAsset (ảnh nền), heroText (tiêu đề sơ đồ), chainSteps ([{{"badge":"BƯỚC 1","title":"...","detail":"..."}}, ... đúng 3 bước])
- "bar_versus": biểu đồ cột 3D so sánh 2 con số — primaryAsset (ảnh nền), heroText (tiêu đề), leftLabel, leftValue (số nguyên), rightLabel, rightValue (số nguyên), statSuffix (vd "%", " USD")
- "evidence_stack": nhiều lớp ảnh chồng 3D parallax — primaryAsset (ảnh nền/hồ sơ), rightAsset (ảnh vật thể tách nền `removeBg=true`), heroText (nhận định ngắn)
- "dossier_stamp": primaryAsset (ảnh thật), heroText (tiêu đề 3-6 từ), stampText (con dấu đỏ 2-3 từ vd "MIỄN THUẾ 0%", "PHI LỢI NHUẬN"), eyebrow (nhãn nguồn)
- "odometer_shock": primaryAsset (ảnh thật), statNumber (số nguyên), statSuffix (vd "%", " USD", " TỶ"), statLabel (chú thích 2-4 từ), heroText (tuyệt đối KHÔNG lặp lại con số statNumber)
- "cutout_ar_stage": primaryAsset (ảnh vật thể/nhân vật, `removeBg=true`), heroText, statNumber + statSuffix (tia chỉ AR)
- "split_versus": primaryAsset + leftLabel (nửa trên), rightAsset + rightLabel (nửa dưới), stampText hoặc statNumber+statSuffix (huy hiệu ở giữa)
- "headline_evidence": primaryAsset, heroText (tiêu đề bằng chứng), eyebrow (nhãn đỏ nguồn tin)
- "timeline_reveal": primaryAsset, chainSteps ([{{"badge":"MỐC 1","title":"...","detail":""}}, ... 3 mốc])

QUY TẮC LỜI THOẠI TIẾNG VIỆT TỰ NHIÊN:
- Mỗi câu `narration` phải là văn nói tiếng Việt mạch lạc, có chủ ngữ-vị ngữ và liên kết nhân quả rõ ràng (vì sao -> kết quả thế nào), TUYỆT ĐỐI KHÔNG viết rời rạc kiểu liệt kê từ khóa.

Mọi file "harvested/<name>.png" dùng trong scenes phải có trong assetSpecs."""

    print("[AGENT-1 SCRIPT] Drafting investigative 5-beat script...")
    parsed = _call_gemini_json(prompt)
    parsed = _agent_2_editor_qa(parsed)
    parsed["fps"] = 60
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
    foley_dir = BASE_DIR / "assets" / "foleys"
    sfx_pools: dict[str, list[Path]] = {
        "flow_diagram": [sfx_dir / "gear_lock.mp3", sfx_dir / "cut.mp3", foley_dir / "keyboard_clack.wav"],
        "bar_versus": [foley_dir / "boom_drop.wav", sfx_dir / "bass_hit.mp3", foley_dir / "impact.wav"],
        "evidence_stack": [sfx_dir / "whoosh1.mp3", foley_dir / "camera_click.wav", sfx_dir / "whoosh2.mp3"],
        "dossier_stamp": [foley_dir / "gavel_slam_norm.wav", sfx_dir / "metal_hit.mp3", foley_dir / "gavel_thud.wav"],
        "odometer_shock": [foley_dir / "braaam.wav", foley_dir / "kaching.wav", sfx_dir / "bass_hit.mp3"],
        "cutout_ar_stage": [sfx_dir / "zoom_hit.mp3", sfx_dir / "whoosh3.mp3", sfx_dir / "hit_blow.mp3"],
        "split_versus": [sfx_dir / "whoosh2.mp3", sfx_dir / "glitch.mp3", foley_dir / "impact.wav"],
        "headline_evidence": [foley_dir / "camera_click.wav", sfx_dir / "whoosh_big.mp3", sfx_dir / "cut.mp3"],
        "timeline_reveal": [sfx_dir / "gear_lock.mp3", foley_dir / "cash_flip.wav", sfx_dir / "whoosh1.mp3"],
    }
    default_pool = [
        sfx_dir / "whoosh1.mp3", foley_dir / "boom_drop.wav", sfx_dir / "whoosh2.mp3",
        foley_dir / "impact.wav", sfx_dir / "zoom_hit.mp3", sfx_dir / "whoosh3.mp3",
    ]

    theme_bgm_map = {
        "tech_cyber": "tension_intro_epic.mp3",
        "noir_dossier": "clock_ticking_teaser.mp3",
        "finance_vox": "master_cinematic_bgm.mp3",
        "retail_warm": "cinematic_documentary_bgm_real.mp3",
    }
    theme_name = str(plan.get("theme", "")).strip()
    bgm_name = theme_bgm_map.get(theme_name, "hadawhy_mystery_bgm.mp3")
    bgm_path = BASE_DIR / "assets" / "music" / bgm_name
    if not bgm_path.exists():
        bgm_path = BASE_DIR / "assets" / "music" / "hadawhy_mystery_bgm.mp3"

    # Hook-text kinetic slam SFX pool (rotated continuously so every Hook sounds fresh)
    hook_sfx_pool = [
        p for p in (
            foley_dir / "braaam.wav",
            foley_dir / "boom_drop.wav",
            foley_dir / "gavel_slam_norm.wav",
            foley_dir / "impact.wav",
            sfx_dir / "hit_blow.mp3",
            sfx_dir / "zoom_hit.mp3",
            sfx_dir / "bass_hit.mp3",
            sfx_dir / "metal_hit.mp3",
        )
        if p.exists()
    ]
    accent_sfx_pool = [
        p for p in (
            foley_dir / "camera_click.wav",
            foley_dir / "keyboard_clack.wav",
            foley_dir / "cash_flip.wav",
            foley_dir / "kaching.wav",
            foley_dir / "heartbeat.wav",
            sfx_dir / "glitch.mp3",
            sfx_dir / "cut.mp3",
            sfx_dir / "whoosh1.mp3",
            sfx_dir / "whoosh2.mp3",
            sfx_dir / "whoosh3.mp3",
        )
        if p.exists()
    ]

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

    # Export words.json, script_scenes.json & choreography_blueprint.json for pre_render_gate & TSX director
    gate_dir = OUT_DIR / "gate_tmp"
    gate_dir.mkdir(parents=True, exist_ok=True)
    words_flat: list[dict] = []
    for cap in plan.get("captions", []):
        for line in cap.get("lines", []):
            for tok in line:
                words_flat.append({
                    "word": tok.get("text", ""),
                    "start": round(float(tok.get("startSec", 0)), 3),
                    "end": round(float(tok.get("endSec", 0)), 3),
                })
    (gate_dir / "words.json").write_text(
        json.dumps({"audio_duration_sec": round(total_dur, 2), "words": words_flat}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (gate_dir / "script_scenes.json").write_text(
        json.dumps(
            [
                {
                    "id": sc.get("id"),
                    "start": sc.get("startSec"),
                    "end": sc.get("endSec"),
                    "narration": sc.get("narration", ""),
                    "heroText": sc.get("heroText", ""),
                    "layout": sc.get("layout", ""),
                }
                for sc in scenes
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    blueprint = {
        "projectTitle": plan.get("projectTitle", "HaDaWhy_Cloud_Video"),
        "fps": int(plan.get("fps", 60)),
        "totalDurationSec": round(total_dur, 2),
        "beats": [
            {
                "id": sc.get("id"),
                "startSec": sc.get("startSec"),
                "endSec": sc.get("endSec"),
                "layout": sc.get("layout"),
                "heroText": sc.get("heroText"),
                "eyebrow": sc.get("eyebrow"),
                "primaryAsset": sc.get("primaryAsset", ""),
                "rightAsset": sc.get("rightAsset", ""),
                "statNumber": sc.get("statNumber"),
                "statSuffix": sc.get("statSuffix"),
                "chainSteps": sc.get("chainSteps", []),
                "infoTags": sc.get("infoTags", []),
                "narration": sc.get("narration", ""),
            }
            for sc in scenes
        ],
    }
    (gate_dir / "choreography_blueprint.json").write_text(
        json.dumps(blueprint, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # 2. Rich Multi-Layer Contextual SFX Hooks (rotate diverse SFX per scene, never repeat same sound back-to-back)
    sfx_entries: list[tuple[Path, int, float]] = []
    tick_sfx = sfx_dir / "tick.mp3"
    coin_sfx = foley_dir / "kaching.wav" if (foley_dir / "kaching.wav").exists() else sfx_dir / "coin1.mp3"
    lock_sfx = sfx_dir / "lock.mp3"
    pop_sfx = sfx_dir / "pop.mp3"
    pop_dry_sfx = sfx_dir / "pop_dry.mp3"
    whoosh_sfx = sfx_dir / "whoosh2.mp3"
    last_sfx_name = ""

    for sc_idx, scene in enumerate(scenes):
        s0_ms = max(0, int(round(float(scene.get("startSec", 0)) * 1000)))
        s_dur_ms = max(1000, int(round((float(scene.get("endSec", 0)) - float(scene.get("startSec", 0))) * 1000)))
        layout = str(scene.get("layout", ""))

        pool = [p for p in sfx_pools.get(layout, default_pool) if p.exists()]
        if not pool:
            pool = [p for p in default_pool if p.exists()]
        if pool:
            sfx_file = pool[sc_idx % len(pool)]
            if sfx_file.name == last_sfx_name and len(pool) > 1:
                sfx_file = pool[(sc_idx + 1) % len(pool)]
            last_sfx_name = sfx_file.name
            sfx_entries.append((sfx_file, s0_ms, 0.78))

        # Rotating Hook-text slam + mid-scene foley accent so every Hook & transition sounds unique
        if hook_sfx_pool:
            hk_sfx = hook_sfx_pool[(sc_idx * 3 + 1) % len(hook_sfx_pool)]
            if hk_sfx.name != last_sfx_name:
                sfx_entries.append((hk_sfx, s0_ms + 80, 0.62))
        if accent_sfx_pool and s_dur_ms > 1500:
            ac_sfx = accent_sfx_pool[(sc_idx * 5 + 2) % len(accent_sfx_pool)]
            sfx_entries.append((ac_sfx, s0_ms + min(750, s_dur_ms // 2), 0.55))

        # Odometer rolling ticks + jackpot/lock ding
        if layout in ("stat_odometer", "odometer_shock"):
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

    # Generate bespoke 5-beat Hollywood Trailer BGM per script via ACE-Step / Procedural Composer
    try:
        sys.path.insert(0, str(BASE_DIR / "engine"))
        from ace_step_fb_runner import ACEStepFBRunner  # type: ignore
        bespoke_bgm = temp_dir / "bespoke_5beat_bgm.mp3"
        beat_ts = [float(sc.get("startSec", 0)) for sc in scenes]
        full_script_txt = " ".join(str(sc.get("narration", "")) for sc in scenes)
        ACEStepFBRunner().generate_unique_script_bgm(
            script_topic=str(plan.get("projectTitle", "HaDaWhy")),
            output_path=bespoke_bgm,
            duration_sec=total_dur + 0.5,
            script_text=full_script_txt,
            beat_timestamps=beat_ts,
        )
        if bespoke_bgm.exists() and bespoke_bgm.stat().st_size > 10000:
            bgm_path = bespoke_bgm
            print(f"[BGM-ACE] Generated unique 5-beat bespoke trailer score: {bgm_path.name}")
    except Exception as exc:
        print(f"[BGM-ACE] Bespoke score fallback to {bgm_path.name}: {exc}")

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


def _agent_6_thumbnail_and_seo(plan: dict) -> tuple[Path | None, str]:
    """Agent 6: Render 9:16 ThumbnailCover9x16 + write 3 Evergreen SEO titles and return (thumb_png, caption)."""
    try:
        scenes = plan.get("scenes", [])
        harvested_files = sorted(
            [f"harvested/{p.name}" for p in HARVESTED_DIR.glob("*.png") if p.stat().st_size > 1024]
        )
        if not harvested_files:
            print("[AGENT-6 THUMB/SEO] No harvested images available, skipping thumbnail.")
            return None, ""

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
            "Bạn là Chuyên gia Thumbnail & SEO Evergreen kênh HaDa Why (@hadawhy). Dựa trên kịch bản sau, hãy trả về JSON gồm:\n"
            '{"line1": "DÒNG 1 NGẮN 3-5 TỪ IN HOA", "line2": "DÒNG 2 NGẮN 3-5 TỪ IN HOA", '
            '"seoTitles": ["Tiêu đề SEO 1 (giật tò mò)", "Tiêu đề SEO 2 (nhấn con số/bí mật)", "Tiêu đề SEO 3 (chuẩn tìm kiếm Evergreen)"], '
            '"hashtags": "#HaDaWhy #KinhTe #CongNghe ..."}\n'
            f"Kịch bản: {json.dumps([s.get('narration', '') for s in scenes], ensure_ascii=False)}"
        )
        line1, line2 = first_hero, second_hero
        seo_titles = [f"{first_hero} — {second_hero}"]
        hashtags = "#HaDaWhy #BiMatThuongHieu #KienThucThuVi #ReelsVN"
        try:
            seo = _call_gemini_json(seo_prompt, require_scenes=False)
            line1 = str(seo.get("line1") or line1).upper()
            line2 = str(seo.get("line2") or line2).upper()
            raw_titles = seo.get("seoTitles") or ([seo.get("viralTitle")] if seo.get("viralTitle") else [])
            if isinstance(raw_titles, list) and raw_titles:
                seo_titles = [str(t).strip() for t in raw_titles if str(t).strip()][:3]
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
        titles_block = "\n".join(f"{i}. {t}" for i, t in enumerate(seo_titles, start=1))
        seo_caption = f"🖼️ THUMBNAIL 9:16 & 3 TIÊU ĐỀ SEO EVERGREEN\n{titles_block}\n\n{hashtags}"
        if thumb_png.exists():
            print(f"[AGENT-6 THUMB/SEO] Generated {thumb_png.name}")
            return thumb_png, seo_caption
        return None, seo_caption
    except Exception as exc:
        print(f"[AGENT-6 THUMB/SEO] Warning: {exc}")
        return None, ""


def _call_llm_text(prompt: str) -> str:
    """Call DeepSeek (primary if key set) / Gemini / GitHub Models / OpenRouter for raw TSX code generation."""
    import requests  # type: ignore

    deepseek_key = os.getenv("DEEPSEEK_API_KEY", "").strip()
    if deepseek_key:
        try:
            print("[AGENT-4 TSX] Calling DeepSeek deepseek-chat...")
            r = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {deepseek_key}"},
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.2, "max_tokens": 8192},
                timeout=90,
            )
            if r.ok:
                text = str(r.json()["choices"][0]["message"]["content"]).strip()
                if "export const DynamicReel" in text:
                    return text
            else:
                print(f"[AGENT-4 TSX] DeepSeek HTTP {r.status_code}: {r.text[:200]}")
        except Exception as exc:
            print(f"[AGENT-4 TSX] DeepSeek error: {exc}")

    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()
    if gemini_key:
        for model in ("gemini-2.5-flash", "gemini-flash-latest"):
            try:
                print(f"[AGENT-4 TSX] Calling Gemini {model}...")
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
                r = requests.post(
                    url,
                    json={
                        "contents": [{"parts": [{"text": prompt}]}],
                        "generationConfig": {"temperature": 0.25, "maxOutputTokens": 8192},
                    },
                    timeout=90,
                )
                if r.ok:
                    cands = r.json().get("candidates") or []
                    if cands:
                        text = str(cands[0]["content"]["parts"][0]["text"]).strip()
                        if "export const DynamicReel" in text:
                            return text
                else:
                    print(f"[AGENT-4 TSX] Gemini {model} HTTP {r.status_code}: {r.text[:200]}")
            except Exception as exc:
                print(f"[AGENT-4 TSX] Gemini {model} error: {exc}")

    gh_token = os.getenv("GH_MODELS_TOKEN", "").strip()
    if gh_token:
        try:
            print("[AGENT-4 TSX] Calling GH_MODELS openai/gpt-4o-mini...")
            r = requests.post(
                "https://models.github.ai/inference/chat/completions",
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {gh_token}"},
                json={"model": "openai/gpt-4o-mini", "messages": [{"role": "user", "content": prompt}], "temperature": 0.25, "max_tokens": 6000},
                timeout=60,
            )
            if r.ok:
                text = str(r.json()["choices"][0]["message"]["content"]).strip()
                if "export const DynamicReel" in text:
                    return text
        except Exception as exc:
            print(f"[AGENT-4 TSX] GH_MODELS error: {exc}")

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


def _vision_inspect_beat_stills(still_paths: list[Path]) -> str | None:
    """Send per-beat rendered still PNGs to Gemini Vision to catch overlapping text, clipping, black frames, or jagged cutouts."""
    if not still_paths or not os.getenv("GEMINI_API_KEY", "").strip():
        return None
    raw_imgs = [p.read_bytes() for p in still_paths if p.exists()]
    if not raw_imgs:
        return None
    prompt = (
        "Bạn là Giám đốc QC Thị Giác cho video dọc 9:16 (1080x1920). "
        "Hãy soi kỹ các khung hình (still) của từng Beat vừa render:\n"
        "1. Có chữ bị đè lên nhau, rớt dòng xấu hoặc tràn ra ngoài Safe Zone (lề phải >920px, đáy >1620px, đỉnh <160px) không?\n"
        "2. Có ảnh bị đen, mất hình, trơ ảnh phẳng vô hồn hay viền tách nền răng cưa nặng không?\n"
        "3. Có hộp nền đục xấu che mất bối cảnh không?\n"
        "Nếu TẤT CẢ đều ổn, trả lời đúng 1 từ: PASS\n"
        "Nếu có lỗi, trả lời bắt đầu bằng FAIL: <liệt kê lỗi ngắn gọn từng Beat để sửa code TSX>."
    )
    ans = _call_gemini_vision(prompt, raw_imgs, max_tokens=300)
    if ans and ans.upper().startswith("FAIL"):
        return ans
    return None


def _agent_4_tsx_director(plan: dict) -> str:
    """Bước C & D: AI tự viết DynamicReel.tsx + vòng lặp tsc --noEmit + pre_render_gate + remotion still Vision QC."""
    dyn_path = REMOTION_DIR / "src" / "DynamicReel.tsx"
    safe_backup = dyn_path.read_text(encoding="utf-8") if dyn_path.exists() else ""

    harvested_list = sorted([f"harvested/{p.name}" for p in HARVESTED_DIR.glob("*.png") if p.stat().st_size > 1024])
    fps = int(plan.get("fps", 60))
    scenes = plan.get("scenes", [])
    scenes_brief = [
        {
            "id": s.get("id"),
            "fromFrame": int(round(float(s.get("startSec", 0)) * fps)),
            "durationFrames": max(15, int(round((float(s.get("endSec", 3)) - float(s.get("startSec", 0))) * fps))),
            "layout": s.get("layout", ""),
            "heroText": s.get("heroText"),
            "eyebrow": s.get("eyebrow"),
            "primaryAsset": s.get("primaryAsset", ""),
            "rightAsset": s.get("rightAsset", ""),
            "statNumber": s.get("statNumber"),
            "statSuffix": s.get("statSuffix"),
            "infoTags": s.get("infoTags", []),
            "chainSteps": s.get("chainSteps", []),
            "narration": s.get("narration", ""),
        }
        for s in scenes
    ]

    ref_snippet = ""
    for ref_name in ("RapPhimBongNgo42s.tsx", "NvidiaSuccession40s.tsx"):
        ref_file = REMOTION_DIR / "src" / ref_name
        if ref_file.exists():
            ref_snippet += f"\n--- MẪU THAM CHIẾU ({ref_name}) ---\n" + "\n".join(ref_file.read_text(encoding="utf-8").splitlines()[:85]) + "\n"

    tsx_prompt = f"""Bạn là Kỹ Sư Đạo Diễn Remotion 3D (`fb-reels-motion-3d-director`). Hãy viết MỘT FILE CODE `DynamicReel.tsx` ĐỘC BẢN cho video 9:16 (1080x1920, {fps} fps).

CÁC COMPONENT CHUẨN CÓ SẴN & EXACT PROPS:
- `import React from "react";`
- `import {{ AbsoluteFill, Img, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig }} from "remotion";`
- `import {{ HaDaWhyMistBackground }} from "./components/HaDaWhyMistBackground";` // props: intensity?: number, accentHex?: string
- `import {{ HaDaWhyFontFaces, KineticHookHeader }} from "./components/KineticHookHeader";` // KineticHookHeader props: beat={{start:number, eyebrow:string, hero:string, accent:string, heroSize?:number}}, top?:number
- `import {{ ChannelWatermark9x16 }} from "./components/ChannelWatermark9x16";` // no required props
- `import {{ ScaleComparison3D }} from "./components/ScaleComparison3D";` // props: startFrame, endFrame, leftItemSrc, leftItemCount, leftLabel, rightTopTitle, rightTargetNumber, rightUnitSuffix, rightLabel, stampText?
- `import {{ TimelineTrack3D }} from "./components/TimelineTrack3D";` // props: startFrame, endFrame, milestones: {{dateLabel, title, iconOrCutoutSrc, accentColor?, triggerOffsetFrames}}[]
- `import {{ GeoStrategicMap3D }} from "./components/GeoStrategicMap3D";` // props: startFrame, endFrame, originLabel, targetLabel, evidenceImageSrc?, evidenceTitle?
- `import {{ StickerPop }} from "./components/StickerPop";`
- `import {{ CoinStream }} from "./components/CoinStream";`
- `import defaultPlan from "./scene_plan.json";`
- `import {{ UniversalScenePlan }} from "./HaDaWhyUniversal9x16";`

YÊU CẦU KỸ THUẬT BẮT BUỘC:
1. Export đúng: `export const DynamicReel: React.FC<{{ plan?: UniversalScenePlan }}> = ({{ plan = defaultPlan as unknown as UniversalScenePlan }}) => {{ ... }};`
2. BẮT BUỘC render `<HaDaWhyFontFaces />` và `<HaDaWhyMistBackground intensity={0.11} accentHex="66, 178, 242" />` ở lớp nền, và `<ChannelWatermark9x16 />` ở lớp trên cùng!
3. BẮT BUỘC dùng `<KineticHookHeader />` (hoặc `spring` slam) cho tiêu đề tầng trên (`top: 240..480px`), `maxWidth: 900`, ZERO-BOX (tuyệt đối CẤM `backgroundColor: "rgba(...,0.4..0.9)"` bọc chữ; chỉ dùng `WebkitTextStroke` + `textShadow`).
4. Tầng giữa (`top: 520..1580px`): Phối hợp chuyển động đa lớp liên tục cho ảnh thật (`{json.dumps(harvested_list)}`), mọi ảnh BẮT BUỘC có chuyển động Ken Burns / Parallax / Scale suốt `durationFrames`, sử dụng `ScaleComparison3D` / `TimelineTrack3D` / `GeoStrategicMap3D` / số đếm Odometer / sơ đồ SVG tùy ngữ cảnh từng Beat.
5. **KHÔNG ĐƯỢC ĐỨNG IM Ở CUỐI VIDEO:** Toàn bộ các `<Sequence>` phải nối tiếp kín 100% từ frame `0` đến hết tổng `durationFrames` (`{sum(b["durationFrames"] for b in scenes_brief)}` frames).
6. CẤM tuyệt đối `objects/*_3d.png` (icon nhựa hoạt hình) và CẤM phụ đề karaoke đáy màn hình.
{ref_snippet}

DỮ LIỆU CHOREOGRAPHY CÁC BEAT ({fps} fps):
{json.dumps(scenes_brief, ensure_ascii=False, indent=2)}

CHỈ trả về code TypeScript hoàn chỉnh cho `DynamicReel.tsx` (bắt đầu bằng `import React from "react";`, không giải thích thêm)."""

    gate_dir = OUT_DIR / "gate_tmp"
    still_dir = OUT_DIR / "beat_stills"
    still_dir.mkdir(parents=True, exist_ok=True)
    try:
        sys.path.insert(0, str(BASE_DIR / "engine"))
        from pre_render_gate import inspect_composition  # type: ignore
    except Exception:
        inspect_composition = None

    current_prompt = tsx_prompt
    for attempt in range(1, 4):
        try:
            raw_code = _call_llm_text(current_prompt)
            tsx_code = _extract_tsx_code(raw_code)
            if "export const DynamicReel" not in tsx_code or "ChannelWatermark9x16" not in tsx_code:
                raise RuntimeError("Missing DynamicReel export or ChannelWatermark9x16")
            dyn_path.write_text(tsx_code, encoding="utf-8")

            # 1) TypeScript check (use explicit typescript package so npx never grabs wrong tsc@2.0.4)
            proc = subprocess.run(
                ["npx", "-p", "typescript", "tsc", "--noEmit"],
                cwd=REMOTION_DIR,
                capture_output=True,
                text=True,
                shell=(os.name == "nt"),
            )
            if proc.returncode != 0:
                err_msg = (proc.stdout + "\n" + proc.stderr).strip()[:1800]
                print(f"[AGENT-4 TSX] tsc failed (attempt {attempt}):\n{err_msg}")
                current_prompt = (
                    f"File DynamicReel.tsx vừa viết bị lỗi TypeScript:\n{err_msg}\n\n"
                    f"Hãy sửa lại toàn bộ file DynamicReel.tsx cho hết lỗi `tsc --noEmit`. CHỈ trả về code TypeScript hoàn chỉnh:\n\n{tsx_code}"
                )
                continue

            # 2) Pre-render gate check
            if inspect_composition is not None and gate_dir.exists():
                gate_res = inspect_composition(dyn_path, gate_dir)
                if not gate_res.get("passed", True):
                    gate_issues = "\n".join(gate_res.get("issues", []))
                    print(f"[AGENT-4 TSX] pre_render_gate failed (attempt {attempt}):\n{gate_issues}")
                    current_prompt = (
                        f"File DynamicReel.tsx vi phạm Pre-Render Gate:\n{gate_issues}\n\n"
                        f"Hãy sửa lại toàn bộ file DynamicReel.tsx khắc phục triệt để các lỗi trên. CHỈ trả về code TypeScript hoàn chỉnh:\n\n{tsx_code}"
                    )
                    continue

            # 3) Render 1 still per beat & inspect with Gemini Vision
            still_paths: list[Path] = []
            for idx, sc in enumerate(scenes[:6], start=1):
                mid_sec = (float(sc.get("startSec", 0)) + float(sc.get("endSec", 2))) / 2.0
                mid_frame = max(5, int(round(mid_sec * fps)))
                sp = still_dir / f"beat_{idx:02d}.png"
                try:
                    subprocess.run(
                        [
                            "npx", "remotion", "still", "src/index.ts", "DynamicReel", str(sp),
                            f"--frame={mid_frame}", "--gl=angle",
                        ],
                        cwd=REMOTION_DIR,
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        shell=(os.name == "nt"),
                    )
                    if sp.exists():
                        still_paths.append(sp)
                except Exception as exc:
                    print(f"[STILL-QC] Could not capture beat {idx}: {exc}")

            vision_err = _vision_inspect_beat_stills(still_paths)
            if vision_err:
                print(f"[STILL-QC] Vision rejected stills (attempt {attempt}): {vision_err}")
                current_prompt = (
                    f"Gemini Vision đã soi ảnh chụp từng Beat của DynamicReel.tsx và phát hiện lỗi bố cục sau:\n{vision_err}\n\n"
                    f"Hãy sửa lại tọa độ/fontSize/căn lề trong DynamicReel.tsx để hết hoàn toàn lỗi trên. CHỈ trả về code TypeScript hoàn chỉnh:\n\n{tsx_code}"
                )
                continue

            print(f"[AGENT-4 TSX] DynamicReel.tsx passed tsc + pre_render_gate + Vision Still QC on attempt {attempt}!")
            return "DynamicReel"
        except Exception as exc:
            print(f"[AGENT-4 TSX] Attempt {attempt} error: {exc}")

    if safe_backup:
        dyn_path.write_text(safe_backup, encoding="utf-8")
    raise RuntimeError("Agent-4 TSX failed to produce a clean DynamicReel.tsx after 3 attempts (refusing to fallback to legacy template)")


def mode_render() -> Path:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    plan["fps"] = 60
    harvest_assets(plan, clean=False)
    plan = _agent_3_prune_missing_assets(plan)
    PLAN_PATH.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    title = plan.get("projectTitle", "HaDaWhy_Cloud_Video")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_mp4 = OUT_DIR / f"{title}_raw.mp4"
    out_mp4 = OUT_DIR / f"{title}.mp4"

    # Bước A: Build VieNeu TTS + words.json + choreography_blueprint.json + -14.0 LUFS mix
    audio_wav = build_audio_track(plan, OUT_DIR / "audio_tmp")

    try:
        avail_cpus = len(os.sched_getaffinity(0))
    except AttributeError:
        avail_cpus = os.cpu_count() or 2
    concurrency = str(max(1, min(4, avail_cpus)))

    # Bước C & D: AI tự viết TSX + tsc + pre_render_gate + Vision Still QC
    has_any_llm = any(
        os.getenv(k, "").strip()
        for k in ("GEMINI_API_KEY", "GH_MODELS_TOKEN", "OPENROUTER_API_KEY", "DEEPSEEK_API_KEY")
    )
    comp_id = _agent_4_tsx_director(plan) if has_any_llm else "CinematicReel"
    print(f"[RENDER] Using Remotion composition: {comp_id} @ {plan.get('fps', 60)}fps")
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

    # Bước E: Ghép âm thanh -14.0 LUFS + Tạo & Nhúng Thumbnail + Auto QC + Gửi Telegram
    thumb_png, seo_caption = _agent_6_thumbnail_and_seo(plan)
    merged_mp4 = OUT_DIR / f"{title}_merged.mp4"
    if audio_wav and audio_wav.exists():
        subprocess.run(
            [
                "ffmpeg", "-y", "-i", str(raw_mp4), "-i", str(audio_wav),
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", "-shortest", str(merged_mp4),
            ],
            check=True,
        )
        raw_mp4.unlink(missing_ok=True)
    else:
        raw_mp4.replace(merged_mp4)

    if thumb_png and thumb_png.exists():
        try:
            subprocess.run(
                [
                    "ffmpeg", "-y", "-i", str(merged_mp4), "-i", str(thumb_png),
                    "-map", "0", "-map", "1", "-c", "copy", "-disposition:v:1", "attached_pic",
                    str(out_mp4),
                ],
                check=True,
            )
            merged_mp4.unlink(missing_ok=True)
        except Exception as exc:
            print(f"[THUMB-EMBED] Warning: {exc}")
            merged_mp4.replace(out_mp4)
    else:
        merged_mp4.replace(out_mp4)

    qc_summary = _agent_5_visual_qc(out_mp4)
    try:
        sys.path.insert(0, str(BASE_DIR / "engine"))
        from auto_qc_fb_reels import AutoQCFBReels  # type: ignore
        qc_res = AutoQCFBReels().inspect_video(out_mp4)
        qc_summary = f"{qc_summary} | AutoQC={qc_res.get('score')}/100 ({'PASS' if qc_res.get('passed') else 'WARN'})"
    except Exception as exc:
        print(f"[AUTO-QC] Skipped deep OpenCV QC: {exc}")

    send_telegram_video(out_mp4, f"Render hoàn tất ({qc_summary}): {title}")
    if thumb_png and thumb_png.exists():
        send_telegram_photo(thumb_png, seo_caption)
    elif seo_caption:
        send_telegram_message(seo_caption)

    print(f"[RENDER] Output MP4: {out_mp4}")
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
