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
        "iiprop": "url|mime",
        "iiurlwidth": "1024",
        "format": "json",
    }
    try:
        r = requests.get("https://commons.wikimedia.org/w/api.php", params=params, headers=headers, timeout=20)
        r.raise_for_status()
        pages = r.json().get("query", {}).get("pages", {})
        for page in pages.values():
            info = (page.get("imageinfo") or [{}])[0]
            mime = info.get("mime", "")
            img_url = info.get("thumburl") or info.get("url")
            if img_url and mime in ("image/jpeg", "image/png", "image/webp"):
                img_resp = requests.get(img_url, headers=headers, timeout=25)
                if img_resp.ok and len(img_resp.content) > 5000:
                    return img_resp.content
    except Exception as exc:
        print(f"[HARVEST] Wikimedia fallback for '{query}': {exc}")
    return None


def _fetch_pollinations_image(query: str) -> bytes | None:
    import requests  # type: ignore

    prompt_enc = urllib.parse.quote(f"{query}, clean studio lighting, centered isolated subject, photorealistic, high detail")
    url = f"https://image.pollinations.ai/prompt/{prompt_enc}?width=1024&height=1024&nologo=true"
    try:
        r = requests.get(url, timeout=45)
        if r.ok and len(r.content) > 5000:
            return r.content
    except Exception as exc:
        print(f"[HARVEST] Pollinations error for '{query}': {exc}")
    return None


def harvest_assets(plan: dict, clean: bool = False) -> None:
    specs = plan.get("assetSpecs", [])
    if clean and HARVESTED_DIR.exists():
        shutil.rmtree(HARVESTED_DIR, ignore_errors=True)
    HARVESTED_DIR.mkdir(parents=True, exist_ok=True)
    if not specs:
        return

    from PIL import Image  # type: ignore
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

        raw_bytes = _fetch_wikimedia_image(query) or _fetch_pollinations_image(query)
        if not raw_bytes:
            # Generate clean transparent placeholder so Remotion never crashes
            Image.new("RGBA", (512, 512), (66, 178, 242, 40)).save(out_path, "PNG")
            continue

        if remove_bg and remove is not None:
            try:
                cut_bytes = remove(raw_bytes)
                img = Image.open(io.BytesIO(cut_bytes)).convert("RGBA")
                bbox = img.getbbox()
                if bbox:
                    img = img.crop(bbox)
                img.save(out_path, "PNG")
                continue
            except Exception as exc:
                print(f"[HARVEST] rembg failed for {filename}: {exc}")

        Image.open(io.BytesIO(raw_bytes)).convert("RGBA").save(out_path, "PNG")


def _extract_json_object(text: str) -> dict:
    import re
    raw = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1 and end > start:
        raw = raw[start : end + 1]
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    return json.loads(raw, strict=False)


def _call_gemini_json(prompt: str) -> dict:
    import requests  # type: ignore

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    last_err = None

    if api_key:
        for model in ("gemini-3.8-flash", "gemini-flash-latest"):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"},
            }
            try:
                print(f"[GEMINI] Calling {model}...")
                r = requests.post(url, json=payload, timeout=60)
                if r.status_code == 404:
                    print(f"[GEMINI] {model} returned 404, trying next model...")
                    last_err = r.text
                    continue
                r.raise_for_status()
                data = r.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return _extract_json_object(text)
            except Exception as exc:
                print(f"[GEMINI] {model} error: {exc}")
                last_err = exc

    for attempt in range(1, 3):
        try:
            print(f"[POLLINATIONS] Calling free model 'openai' (attempt {attempt})...")
            r = requests.post(
                "https://text.pollinations.ai/openai",
                headers={"Content-Type": "application/json"},
                json={
                    "model": "openai",
                    "messages": [
                        {"role": "system", "content": "Output ONLY valid raw JSON. No markdown, no comments, no trailing commas."},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.3,
                },
                timeout=90,
            )
            r.raise_for_status()
            text = r.json()["choices"][0]["message"]["content"]
            return _extract_json_object(text)
        except Exception as exc:
            print(f"[POLLINATIONS] attempt {attempt} error: {exc}")
            last_err = exc

    raise RuntimeError(f"All LLM providers (Gemini + Pollinations) failed: {last_err}")


def _build_captions_from_scenes(plan: dict) -> dict:
    """Auto-generate word-level captions from each scene's narration if captions are omitted."""
    if plan.get("captions"):
        return plan
    captions = []
    for scene in plan.get("scenes", []):
        narration = str(scene.get("narration", "")).strip()
        if not narration:
            continue
        words = [w for w in narration.split() if w]
        if not words:
            continue
        s0 = float(scene.get("startSec", 0)) + 0.1
        s1 = max(s0 + 0.5, float(scene.get("endSec", s0 + 3.0)) - 0.1)
        step = (s1 - s0) / len(words)
        tokens = []
        for i, w in enumerate(words):
            t0 = round(s0 + i * step, 2)
            t1 = round(s0 + (i + 1) * step, 2)
            tokens.append({"text": w.upper(), "startSec": t0, "endSec": t1, "highlight": (i % 3 == 1)})
        mid = max(1, (len(tokens) + 1) // 2)
        lines = [tokens[:mid]] + ([tokens[mid:]] if tokens[mid:] else [])
        captions.append({"startSec": round(s0, 2), "endSec": round(s1, 2), "lines": lines})
    plan["captions"] = captions
    return plan


def mode_create(topic_prompt: str) -> None:
    if not topic_prompt.strip():
        raise RuntimeError("Topic prompt (--feedback) is required for --mode create/auto")

    prompt = f"""Bạn là Tổng Đạo Diễn video ngắn dọc 9:16 (60fps) kênh HaDa Why (@hadawhy).
Hãy sáng tác JSON scene_plan ngắn gọn cho yêu cầu: "{topic_prompt}"

CHỈ trả về JSON hợp lệ (không markdown ```json):
{{
  "projectTitle": "HaDaWhy_<TenKhongDau>",
  "fps": 60,
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

5 layout hợp lệ:
- "hero_prop": primaryAsset, primaryLabel, subNote, yearWatermark
- "compare_two": leftAsset, leftLabel, leftLabelColor, rightAsset, rightLabel, rightLabelColor, centerAsset, yearWatermark
- "sat_map": mapRegion ("fra"|"uk"|"usa"|"world"), mapCaption
- "two_tier": topLeftAsset, topLeftLabel, topRightAsset, bottomAsset, bottomTitle, bottomHighlight
- "split_duo": leftAsset, leftLabel, rightAsset, rightLabel, ctaText

Mọi file "harvested/<name>.png" dùng trong scenes phải có trong assetSpecs."""

    parsed = _build_captions_from_scenes(_call_gemini_json(prompt))
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


def build_audio_track(plan: dict, temp_dir: Path) -> Path | None:
    """Build Vietnamese voiceover (VieNeu-TTS 'Hải Đăng', fallback edge-tts) + Text Hook SFX + Ducked BGM at -14.0 LUFS."""
    scenes = plan.get("scenes", [])
    captions = plan.get("captions", [])
    total_dur = max((float(s.get("endSec", 0)) for s in scenes), default=10.0)
    if total_dur <= 0:
        return None

    temp_dir.mkdir(parents=True, exist_ok=True)
    sfx_dir = REMOTION_DIR / "public" / "sfx"
    sfx_cycle = [
        sfx_dir / "bass_hit.mp3",
        sfx_dir / "zoom_hit.mp3",
        sfx_dir / "whoosh_big.mp3",
    ]
    bgm_path = BASE_DIR / "assets" / "music" / "hadawhy_mystery_bgm.mp3"

    # Initialize VieNeu-TTS (channel voice: Hải Đăng)
    vieneu_client = None
    try:
        from vieneu import Vieneu  # type: ignore
        vieneu_client = Vieneu()
        print("[TTS] VieNeu-TTS initialized (voice: Hải Đăng)")
    except Exception as exc:
        print(f"[WARN] VieNeu-TTS unavailable, falling back to edge-tts: {exc}")

    # 1. Generate per-phrase Vietnamese voiceover clips
    vo_entries: list[tuple[Path, int]] = []
    for idx, phrase in enumerate(captions):
        words = []
        for line in phrase.get("lines", []):
            for tok in line:
                t = str(tok.get("text", "")).strip()
                if t:
                    words.append(t)
        text = " ".join(words).strip()
        if not text:
            continue
        delay_ms = max(0, int(round(float(phrase.get("startSec", 0)) * 1000)))
        if vieneu_client is not None:
            vo_wav = temp_dir / f"vo_{idx:02d}.wav"
            try:
                clean_text = _normalize_vi_numbers(text)
                audio = vieneu_client.infer(clean_text, voice="Hải Đăng", temperature=0.35, top_p=0.9)
                vieneu_client.save(audio, str(vo_wav))
                if vo_wav.exists() and vo_wav.stat().st_size > 0:
                    vo_entries.append((vo_wav, delay_ms))
                    continue
            except Exception as exc:
                print(f"[WARN] VieNeu-TTS failed for phrase {idx}: {exc}")

        vo_mp3 = temp_dir / f"vo_{idx:02d}.mp3"
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "edge_tts",
                    "--voice",
                    "vi-VN-NamMinhNeural",
                    "--rate=+12%",
                    "--text",
                    text,
                    "--write-media",
                    str(vo_mp3),
                ],
                check=True,
            )
            if vo_mp3.exists() and vo_mp3.stat().st_size > 0:
                vo_entries.append((vo_mp3, delay_ms))
        except Exception as exc:
            print(f"[WARN] edge-tts failed for phrase {idx}: {exc}")

    # 2. Collect Text Hook SFX aligned to each scene's startSec
    sfx_entries: list[tuple[Path, int]] = []
    for idx, scene in enumerate(scenes):
        sfx_file = sfx_cycle[idx % len(sfx_cycle)]
        if sfx_file.exists():
            delay_ms = max(0, int(round(float(scene.get("startSec", 0)) * 1000)))
            sfx_entries.append((sfx_file, delay_ms))

    # 3. Mix Voiceover + SFX + Ducked BGM -> -14.0 LUFS WAV
    inputs: list[str] = []
    filters: list[str] = []
    idx_counter = 0

    # Base silence track to lock exact duration
    inputs.extend(["-f", "lavfi", "-t", f"{total_dur:.3f}", "-i", "anullsrc=r=44100:cl=stereo"])
    base_idx = idx_counter
    idx_counter += 1

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
    filter_complex = (
        ";".join(filters + [
            f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=first:dropout_transition=0:normalize=0,"
            f"loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
        ])
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
            f"--concurrency={concurrency}",
            "--gl=angle",
        ],
        cwd=REMOTION_DIR,
    )
    audio_wav = build_audio_track(plan, OUT_DIR / "audio_tmp")
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
