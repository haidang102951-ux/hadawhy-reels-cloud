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
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
REMOTION_DIR = BASE_DIR / "remotion_reels"
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


def mode_revise(feedback: str) -> None:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is required for --mode revise")
    from google import genai  # type: ignore

    client = genai.Client(api_key=api_key)
    current_plan = PLAN_PATH.read_text(encoding="utf-8")
    prompt = (
        "Bạn là Đạo diễn kỹ thuật Remotion. Hãy cập nhật JSON scene_plan dưới đây theo đúng góp ý của Người Chỉ Huy.\n"
        "Chỉ trả về JSON hợp lệ (không markdown ```json), giữ nguyên cấu trúc và các cảnh không được yêu cầu sửa.\n\n"
        f"GÓP Ý CẦN SỬA:\n{feedback}\n\n"
        f"SCENE_PLAN HIỆN TẠI:\n{current_plan}"
    )
    resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    raw = (resp.text or "").strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    parsed = json.loads(raw)
    PLAN_PATH.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[REVISE] Updated {PLAN_PATH}")


def mode_preview() -> list[Path]:
    plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
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


def build_audio_track(plan: dict, temp_dir: Path) -> Path | None:
    """Build Vietnamese voiceover (edge-tts) + Text Hook SFX + Ducked BGM at -14.0 LUFS."""
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

    # 1. Generate per-phrase Vietnamese voiceover clips via edge-tts
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
                delay_ms = max(0, int(round(float(phrase.get("startSec", 0)) * 1000)))
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
    parser.add_argument("--mode", choices=["preview", "render", "revise"], required=True)
    parser.add_argument("--feedback", default="")
    args = parser.parse_args()

    if args.mode == "revise":
        mode_revise(args.feedback)
        mode_preview()
    elif args.mode == "preview":
        mode_preview()
    elif args.mode == "render":
        mode_render()
    return 0


if __name__ == "__main__":
    sys.exit(main())
