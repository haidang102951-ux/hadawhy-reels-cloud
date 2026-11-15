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
            if img_url and not img_url.lower().endswith(".svg") and min(w, h) >= 350:
                img_resp = requests.get(img_url, headers=headers, timeout=25)
                if img_resp.ok and len(img_resp.content) > 20000:
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
        f"{query}, ultra sharp 3D isometric studio product render, vibrant bright rim lighting, high contrast, isolated on pure solid white background, no text, 8k"
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
    return any(k in q for k in ("ceo", "founder", "president", "building", "factory", "headquarters", "newspaper", "portrait", "huang", "musk", "nvidia", "tsmc", "amd", "intel", "gpu", "server", "data center", "wafer"))


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
        remove_bg = bool(item.get("removeBg", True))
        print(f"[HARVEST] Fetching '{query}' -> {out_path.name} (removeBg={remove_bg})")

        # Prefer canonical Wikipedia real photos for real entities; Pollinations 3D render for isolated props
        raw_bytes = None
        src_name = "none"
        if _is_person_or_place_query(query):
            for s_name, fn in (("wikipedia", _fetch_wikipedia_image), ("wikimedia", _fetch_wikimedia_image), ("pollinations", _fetch_pollinations_image)):
                raw_bytes = fn(query)
                if raw_bytes:
                    src_name = s_name
                    break
        else:
            for s_name, fn in (("pollinations", _fetch_pollinations_image), ("wikipedia", _fetch_wikipedia_image), ("wikimedia", _fetch_wikimedia_image)):
                raw_bytes = fn(query)
                if raw_bytes:
                    src_name = s_name
                    break
        print(f"[HARVEST]   -> source={src_name} ({len(raw_bytes) if raw_bytes else 0} bytes)")
        if not raw_bytes:
            Image.new("RGBA", (512, 512), (66, 178, 242, 40)).save(out_path, "PNG")
            continue

        if remove_bg and remove is not None:
            try:
                cut_bytes = remove(raw_bytes)
                img = Image.open(io.BytesIO(cut_bytes)).convert("RGBA")
                bbox = img.getbbox()
                if bbox:
                    img = img.crop(bbox)
                # Boost brightness slightly if cutout is too dark against #04060a canvas
                alpha = img.getchannel("A")
                mean_rgb = sum(ImageStat.Stat(img.convert("RGB"), mask=alpha).mean) / 3.0
                if mean_rgb < 90:
                    img = ImageEnhance.Brightness(img).enhance(1.22)
                    img = ImageEnhance.Contrast(img).enhance(1.12)
                img = img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=2))
                img.save(out_path, "PNG")
                continue
            except Exception as exc:
                print(f"[HARVEST] rembg failed for {filename}: {exc}")

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
    return json.loads(raw, strict=False)


def _call_openai_compat_json(url: str, api_key: str, model: str, prompt: str, label: str) -> dict | None:
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
        return _extract_json_object(str(text))
    except Exception as exc:
        print(f"[{label}] {model} error: {exc}")
        return None


def _call_gemini_json(prompt: str) -> dict:
    import time
    import requests  # type: ignore

    last_err = None

    # 1. OpenRouter free high-intelligence models (if OPENROUTER_API_KEY is set)
    openrouter_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if openrouter_key:
        for or_model in (
            "nvidia/nemotron-3.5-lightning:free",
            "google/gemma-4-31b-it:free",
            "nvidia/nemotron-3-ultra-550b-a55b:free",
            "openrouter/free",
        ):
            res = _call_openai_compat_json(
                "https://openrouter.ai/api/v1/chat/completions",
                openrouter_key,
                or_model,
                prompt,
                "OPENROUTER",
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
- Viết đủ 5 cảnh giàu thông tin (hoặc theo đúng thời lượng yêu cầu), theo 5 nhịp điều tra gây tò mò tột độ:
  (1) Hook nghịch lý thực tế (cấm mở bài sáo rỗng) -> (2) Bằng chứng số liệu sốc -> (3) So sánh đối lập áp đảo -> (4) Chuỗi nhân-quả bóc trần cơ chế "WHY" ít ai biết -> (5) Kết luận sắc lạnh.
- Lời thoại (`narration`) mỗi cảnh dài 13–19 từ, chứa KIẾN THỨC THẬT, tên riêng thật, con số thật, giải thích rõ CƠ CHẾ TẠI SAO (tạo cảm giác "à hóa ra là vậy!").
- **LUẬT THÉP TEXT HOOK (`eyebrow` & `heroText`):**
  * TUYỆT ĐỐI CẤM ĐẶT CÂU HỎI XÀM trong `eyebrow` hay `heroText` (CẤM "TẠI SAO?", "VÌ SAO?", "LÀ GÌ?", "CÓ BIẾT?", dấu "?").
  * `heroText` (1–3 từ) PHẢI LÀ **SỰ THẬT CHẤN ĐỘNG / CON SỐ / NGHỊCH LÝ ĐẮT GIÁ** giải quyết thẳng vấn đề (VD: `"KẺ BÁN XẺNG"`, `"30.000 USD"`, `"90% ĐỘC TÔN"`, `"CÁI BẪY CUDA"`, `"KHÔNG LỐI THOÁT"`).
  * `heroColor` chọn màu sáng rực rỡ (`#FFE600`, `#FF4D5A`, `#42B2F2`, `#FFFFFF`).
- MỖI CẢNH PHẢI CÓ `infoTags`: mảng 2–3 thẻ thông tin ngắn chứa số liệu/kiến thức thật (VD: `["30.000 USD / CHIP", "80GB HBM3", "LỢI NHUẬN 75%"]`).
- BẮT BUỘC CÓ ÍT NHẤT 1 CẢNH DÙNG `"causal_chain"` với `chainSteps` (3 bước nối tiếp nhau A -> B -> C để người xem thấy sự việc này kéo theo sự việc kia!).
- TRONG `assetSpecs`: ÁP DỤNG LUẬT **"NÓI A HIỆN ĐÚNG A"** — chỉ tìm đúng VẬT THỂ / NHÂN VẬT THẬT được nhắc tới trong lời thoại bằng tên chuẩn ngắn gọn tiếng Anh (VD: `"Jensen Huang"`, `"Nvidia H100 GPU"`, `"gold shovel"`, `"AMD Instinct MI300"`). TUYỆT ĐỐI CẤM bịa hình ẩn dụ lạc đề (như lâu đài, hào nước, cờ vua) và CẤM tìm `"chart"`, `"pie"`, `"code"`, `"price"`, `"screenshot"`. Cảnh `causal_chain` và `bar_compare` KHÔNG cần `primaryAsset`.

CHỈ trả về JSON hợp lệ (không markdown ```json):
{{
  "projectTitle": "HaDaWhy_<TenKhongDau>",
  "fps": 30,
  "mistIntensity": 0.11,
  "assetSpecs": [
    {{ "filename": "ten_anh_1.png", "query": "tu khoa tieng Anh chuan de tim anh that", "removeBg": true }}
  ],
  "scenes": [
    {{
      "id": "scene_1",
      "startSec": 0,
      "endSec": 3.5,
      "layout": "hero_prop",
      "eyebrow": "TIEU DE PHU",
      "heroText": "CHU TO",
      "heroColor": "#ff3b3b",
      "subNote": "GHI CHU",
      "yearWatermark": "2026",
      "primaryAsset": "harvested/ten_anh_1.png",
      "primaryLabel": "",
      "narration": "Cau thoai tieng Viet ngan gon 8-12 tu doc trong canh nay."
    }}
  ]
}}

9 layout hợp lệ (luân phiên đa dạng, bắt buộc dùng causal_chain + bar_compare/stat_odometer):
- "hero_prop": primaryAsset, primaryLabel, subNote, yearWatermark, infoTags
- "compare_two": leftAsset, leftLabel, leftLabelColor, rightAsset, rightLabel, rightLabelColor, centerAsset, yearWatermark
- "sat_map": mapRegion ("fra"|"uk"|"usa"|"world"), mapCaption
- "two_tier": topLeftAsset, topLeftLabel, topRightAsset, bottomAsset, bottomTitle, bottomHighlight
- "split_duo": leftAsset, leftLabel, rightAsset, rightLabel, ctaText
- "stat_odometer": statNumber (số nguyên), statSuffix (vd "%", " USD"), statLabel, primaryAsset, yearWatermark, infoTags
- "bar_compare": leftValue (số), leftLabel, leftLabelColor, rightValue (số), rightLabel, rightLabelColor, yearWatermark, infoTags
- "archival_proof": primaryAsset, stampText (vd "SỰ THẬT 100%"), yearWatermark, infoTags
- "causal_chain": chainSteps ([{{"badge":"BƯỚC 1","title":"...","detail":"..."}}, ... 3 bước nối tiếp]), primaryAsset (tùy chọn), yearWatermark

Mọi file "harvested/<name>.png" dùng trong scenes phải có trong assetSpecs."""

    parsed = _build_captions_from_scenes(_call_gemini_json(prompt))
    parsed["fps"] = 30
    PLAN_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[CREATE] Generated {PLAN_PATH} for topic: {topic_prompt}")
    harvest_assets(parsed, clean=True)


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

    # 2. Contextual Text Hook SFX aligned to each synced scene startSec
    sfx_entries: list[tuple[Path, int]] = []
    for scene in scenes:
        sfx_file = sfx_map.get(str(scene.get("layout", "")), sfx_dir / "bass_hit.mp3")
        if sfx_file.exists():
            delay_ms = max(0, int(round(float(scene.get("startSec", 0)) * 1000)))
            sfx_entries.append((sfx_file, delay_ms))

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
    for sfx_path, delay_ms in sfx_entries:
        inputs.extend(["-i", str(sfx_path)])
        lbl = f"sfx{idx_counter}"
        filters.append(f"[{idx_counter}:a]adelay={delay_ms}|{delay_ms},volume=0.55[{lbl}]")
        sfx_labels.append(f"[{lbl}]")
        idx_counter += 1

    bgm_label: str | None = None
    if bgm_path.exists():
        inputs.extend(["-stream_loop", "-1", "-t", f"{total_dur:.3f}", "-i", str(bgm_path)])
        filters.append(f"[{idx_counter}:a]volume=0.14[bgm_bed]")
        bgm_label = "[bgm_bed]"
        idx_counter += 1

    mix_inputs = [f"[{base_idx}:a]"] + vo_labels + sfx_labels + ([bgm_label] if bgm_label else [])
    if len(mix_inputs) == 1:
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


def mode_render() -> Path:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
    harvest_assets(plan, clean=False)
    title = plan.get("projectTitle", "HaDaWhy_Cloud_Video")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw_mp4 = OUT_DIR / f"{title}_raw.mp4"
    out_mp4 = OUT_DIR / f"{title}.mp4"
    # Build TTS + sync scene_plan.json BEFORE rendering Remotion so captions/scenes match voice 100%
    audio_wav = build_audio_track(plan, OUT_DIR / "audio_tmp")
    concurrency = str(max(1, min(4, os.cpu_count() or 2)))
    run_cmd(
        [
            "npx",
            "remotion",
            "render",
            "src/index.ts",
            "HaDaWhyUniversal9x16",
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
                "-shortest",
                str(out_mp4),
            ],
            check=True,
        )
        raw_mp4.unlink(missing_ok=True)
    else:
        raw_mp4.replace(out_mp4)
    send_telegram_video(out_mp4, f"Render hoàn tất (Voice + SFX + BGM + Motion): {title}")
    print(f"[RENDER] Output MP4: {out_mp4}")
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
