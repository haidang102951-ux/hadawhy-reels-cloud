# -*- coding: utf-8 -*-
r"""
render_reel.py - ĐƯỜNG ỐNG SẢN XUẤT DUY NHẤT & SẠCH 100% (TSX ĐỘC BẢN -> QC -> RENDER -> MIX -14 LUFS -> DUAL-EMBED -> QC VIDEO)

Cách dùng:
  python render_reel.py --comp "TenComposition" --project "D:\DuAn_DangLam\ten_du_an" --name "HaDaWhy_TenVideo"

Đặc điểm cốt lõi:
1. KHÔNG dùng mklink /J (triệt tiêu 100% lỗi EPERM symlink của Remotion Webpack trên Windows).
   Thay vào đó chép tạm assets từ <project>/temp/assets/ sang remotion_reels/public/harvested/ lúc render
   và XÓA SẠCH trong khối `finally:` -> Đầu Não luôn 0 bytes media!
2. Hỗ trợ bất kỳ Composition .tsx độc bản nào (chuẩn NvidiaSuccession40s), không khóa cứng vào template JSON.
3. Chạy bắt buộc qc_gate.check_tsx() trước render và qc_gate.check_video() sau render (chống màn hình đen rỗng).
4. Tự động cào nhạc/SFX tươi mới nếu thiếu, hòa âm -14.0 LUFS + Vacuum Drop, nhúng kép Thumbnail 3D (frame 00:00 + attached_pic).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, List, Optional, Tuple

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

FB_ROOT = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
ENGINE_DIR = FB_ROOT / "engine"
REMOTION_DIR = FB_ROOT / "remotion_reels"
PUBLIC_HARVEST = REMOTION_DIR / "public" / "harvested"
REMOTION_OUT_DIR = REMOTION_DIR / "out"
ACTIVE_EPISODE_PATH = REMOTION_DIR / "src" / "ActiveEpisode.tsx"
TEMP_GEO_PATHS_DEST = REMOTION_DIR / "src" / "components" / "geoPaths.ts"
OUT_FINAL_DIR = Path(r"D:\Video thành phẩm")

DEFAULT_ACTIVE_EPISODE_TSX = (
    'import React from "react";\n\n'
    "export const ACTIVE_DURATION_FRAMES = 600;\n"
    "export const ActiveEpisode: React.FC = () => null;\n"
)

sys.path.insert(0, str(ENGINE_DIR))
import qc_gate  # noqa: E402
import voice_visual_sync  # noqa: E402
from sfx_timeline_mixer import (  # noqa: E402
    auto_choreograph_script_sfx_cues,
    mix_reels_master_audio,
    set_project_sfx_dir,
)


def stage_assets_temporarily(assets_dir: Path) -> None:
    if PUBLIC_HARVEST.exists():
        shutil.rmtree(PUBLIC_HARVEST, ignore_errors=True)
    PUBLIC_HARVEST.mkdir(parents=True, exist_ok=True)
    if assets_dir.exists():
        for f in assets_dir.iterdir():
            if f.is_file():
                shutil.copy2(f, PUBLIC_HARVEST / f.name)


def stage_episode_temporarily(
    assets_dir: Path,
    tsx_path: Optional[Path] = None,
    temp_dir: Optional[Path] = None,
) -> bool:
    """Nạp tạm assets, EpisodeComp.tsx -> ActiveEpisode.tsx và geoPaths.ts (nếu có) trước khi render."""
    stage_assets_temporarily(assets_dir)
    if tsx_path and tsx_path.exists() and tsx_path.resolve() != ACTIVE_EPISODE_PATH.resolve():
        shutil.copy2(tsx_path, ACTIVE_EPISODE_PATH)
    staged_geo = False
    if temp_dir:
        geo_src = temp_dir / "geoPaths.ts"
        if geo_src.exists():
            shutil.copy2(geo_src, TEMP_GEO_PATHS_DEST)
            staged_geo = True
    return staged_geo


def cleanup_staged_assets(remove_temp_geo: bool = True) -> None:
    """Dọn sạch 100% file tạm trong Đầu Não (public/harvested, out, geoPaths.ts tạm và reset ActiveEpisode.tsx)."""
    if PUBLIC_HARVEST.exists():
        shutil.rmtree(PUBLIC_HARVEST, ignore_errors=True)
    if REMOTION_OUT_DIR.exists():
        for item in REMOTION_OUT_DIR.iterdir():
            if item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            else:
                item.unlink(missing_ok=True)
    if remove_temp_geo and TEMP_GEO_PATHS_DEST.exists():
        TEMP_GEO_PATHS_DEST.unlink(missing_ok=True)
    ACTIVE_EPISODE_PATH.write_text(DEFAULT_ACTIVE_EPISODE_TSX, encoding="utf-8")


def render_thumbnail_still(temp_dir: Path) -> Optional[Path]:
    """Render ThumbnailCover9x16 vào temp/thumbnail_9x16.png khi đã nạp tạm public/harvested/."""
    thumb_props = temp_dir / "thumb_props.json"
    thumb_out = temp_dir / "thumbnail_9x16.png"
    if not thumb_props.exists():
        return None
    print("[THUMB] Rendering ThumbnailCover9x16...")
    still_cmd = (
        f'npx remotion still ThumbnailCover9x16 "{thumb_out.as_posix()}" '
        f'--props="{thumb_props.as_posix()}" --gl=angle'
    )
    subprocess.run(still_cmd, shell=True, cwd=str(REMOTION_DIR), check=True)
    return thumb_out if thumb_out.exists() else None


def get_video_duration_sec(video_path: Path) -> float:
    res = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
        capture_output=True, text=True,
    )
    try:
        return float(res.stdout.strip())
    except Exception:
        return 40.0


def extract_beat_timestamps_and_bgm_segments(
    bp_path: Path,
    tsx_path: Path,
    script_json_path: Path,
    total_sec: float,
) -> Tuple[List[float], Optional[List[dict[str, Any]]]]:
    """Đọc mốc Beat thực tế từ choreography_blueprint.json hoặc <Sequence from={...}> trong .tsx; đọc bgm_segments cho Music Spotting."""
    beat_ts: List[float] = []
    bgm_segments: Optional[List[dict[str, Any]]] = None
    fps = 60.0

    if bp_path.exists():
        try:
            bp = json.loads(bp_path.read_text(encoding="utf-8"))
            if isinstance(bp, dict):
                fps = float(bp.get("fps", 60.0) or 60.0)
                if isinstance(bp.get("bgm_segments"), list) and bp["bgm_segments"]:
                    bgm_segments = bp["bgm_segments"]
                if isinstance(bp.get("beat_timestamps"), list) and bp["beat_timestamps"]:
                    beat_ts = sorted({round(float(x), 2) for x in bp["beat_timestamps"] if float(x) >= 0})
                elif isinstance(bp.get("beats"), list) and bp["beats"]:
                    extracted = []
                    for b in bp["beats"]:
                        if not isinstance(b, dict):
                            continue
                        if "start_sec" in b:
                            extracted.append(round(float(b["start_sec"]), 2))
                        elif "start_ms" in b:
                            extracted.append(round(float(b["start_ms"]) / 1000.0, 2))
                        elif "start_frame" in b:
                            extracted.append(round(float(b["start_frame"]) / fps, 2))
                        elif "from" in b:
                            extracted.append(round(float(b["from"]) / fps, 2))
                    if extracted:
                        beat_ts = sorted(set(extracted))
        except Exception as exc:
            print(f"[WARN] Không đọc được beat/bgm_segments từ blueprint: {exc}")

    if not beat_ts and tsx_path.exists():
        try:
            tsx_code = tsx_path.read_text(encoding="utf-8", errors="replace")
            seq_frames = [int(m) for m in re.findall(r"<Sequence\b[^>]*\bfrom=\{\s*(\d+)\s*\}", tsx_code)]
            if seq_frames:
                beat_ts = sorted({round(f / fps, 2) for f in seq_frames if f >= 0 and (f / fps) < total_sec})
        except Exception as exc:
            print(f"[WARN] Không parse được <Sequence from={{...}}> từ {tsx_path.name}: {exc}")

    if bgm_segments is None and script_json_path.exists():
        try:
            sdata = json.loads(script_json_path.read_text(encoding="utf-8"))
            if isinstance(sdata, dict) and isinstance(sdata.get("bgm_segments"), list) and sdata["bgm_segments"]:
                bgm_segments = sdata["bgm_segments"]
        except Exception:
            pass

    if not beat_ts:
        beat_ts = [round(total_sec * p, 2) for p in (0.0, 0.15, 0.35, 0.60, 0.82)]

    return beat_ts, bgm_segments


def main() -> int:
    ap = argparse.ArgumentParser(description="Clean FB Reels 9:16 Production Pipeline (Zero-Trash MasterBrain)")
    ap.add_argument("--comp", default="ActiveEpisode", help="Tên Composition ID trong Root.tsx (mặc định: ActiveEpisode)")
    ap.add_argument("--tsx", default="", help="Đường dẫn file .tsx (mặc định: <project>/temp/EpisodeComp.tsx)")
    ap.add_argument("--project", required=True, help="Thư mục WIP dự án (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--name", default="", help="Tên file xuất bản (không đuôi .mp4; mặc định lấy tên thư mục dự án)")
    ap.add_argument("--mood", default="conspiracy_thriller", help="Mood nhạc nền kịch tính")
    ap.add_argument("--bgm-mood", default="", help="Override mood nhạc nền kịch tính cho audio_harvester & mixer")
    ap.add_argument("--sfx-keywords", default="", help="Từ khóa SFX tiếng Anh cách nhau dấu phẩy cho kịch bản")
    ap.add_argument("--skip-render", action="store_true", help="Bỏ qua bước render nếu đã có temp/raw_video.mp4")
    ap.add_argument("--thumb-only", action="store_true", help="Chỉ nạp tạm ảnh để render temp/thumbnail_9x16.png rồi dọn sạch Đầu Não")
    args = ap.parse_args()

    project_dir = Path(args.project)
    temp_dir = project_dir / "temp"
    assets_dir = temp_dir / "assets"
    temp_dir.mkdir(parents=True, exist_ok=True)
    out_name = args.name.strip() or f"HaDaWhy_{project_dir.name}"
    tsx_path = Path(args.tsx) if args.tsx else (temp_dir / "EpisodeComp.tsx")

    # Chế độ chỉ render Thumbnail 9:16 (mượn tạm public/harvested -> trả sạch 100% trong finally)
    if args.thumb_only:
        if not (temp_dir / "thumb_props.json").exists():
            raise FileNotFoundError(f"Thiếu {temp_dir / 'thumb_props.json'} để chạy --thumb-only!")
        try:
            stage_assets_temporarily(assets_dir)
            thumb_out = render_thumbnail_still(temp_dir)
        finally:
            cleanup_staged_assets(remove_temp_geo=True)
        clean_res = qc_gate.check_brain_clean()
        if not clean_res["passed"]:
            raise RuntimeError(f"BRAIN NOT CLEAN: {clean_res['issues']}")
        print(f"[THUMB-ONLY OK] {thumb_out}")
        return 0

    # 0. Kiểm tra giọng đọc gốc & words.json TRƯỚC KHI RENDER để khóa cứng thời lượng (0 giây im lặng thừa)
    words_path = voice_visual_sync.find_words_json(project_dir)
    if not words_path:
        raise FileNotFoundError(f"Thiếu words.json trong {project_dir}")
    voice_wav = temp_dir / "voiceover.wav"
    if not voice_wav.exists():
        voice_wav = temp_dir / "voice.wav"
    if not voice_wav.exists():
        raise FileNotFoundError(f"Thiếu voiceover.wav / voice.wav trong {temp_dir}")

    voice_sec = get_video_duration_sec(voice_wav)
    exact_frames = math.ceil(voice_sec * 60.0)

    # 1. Pre-Render Gate (Chặn lỗi & khóa khung hình khớp voice_sec trước khi tốn 1 giây render)
    if not args.skip_render:
        print(f"[1/5] Pre-Render QC Gate: {tsx_path} (voice={voice_sec:.2f}s -> exact_frames={exact_frames})...")
        gate_res = qc_gate.check_tsx(tsx_path, project_dir)
        if not gate_res["passed"]:
            print(json.dumps(gate_res, ensure_ascii=False, indent=2))
            raise RuntimeError("PRE-RENDER QC GATE FAILED! Sửa toàn bộ lỗi trên trước khi render.")
        tsx_frames = qc_gate.extract_tsx_total_frames(tsx_path.read_text(encoding="utf-8"))
        if tsx_frames is not None and abs(tsx_frames - exact_frames) > 20:
            raise RuntimeError(
                f"DURATION_MISMATCH_SILENT_TAIL: TSX có {tsx_frames} frames, lệch quá ±20 frames so với "
                f"giọng đọc {voice_sec:.2f}s (bắt buộc ACTIVE_DURATION_FRAMES = {exact_frames})! Dừng render."
            )

    # 2. Mượn tạm (assets + EpisodeComp.tsx -> ActiveEpisode.tsx + geoPaths.ts) và khóa dọn sạch 100% trong finally:
    raw_mp4 = temp_dir / "raw_video.mp4"
    staged_geo = False
    try:
        if not args.skip_render:
            staged_geo = stage_episode_temporarily(assets_dir, tsx_path=tsx_path, temp_dir=temp_dir)
            print("[2/5] TypeScript check (npx tsc --noEmit)...")
            subprocess.run(["cmd", "/c", "npx tsc --noEmit"], cwd=str(REMOTION_DIR), check=True)
            # Tự động render bìa nếu có temp/thumb_props.json mà chưa có temp/thumbnail_9x16.png
            if (temp_dir / "thumb_props.json").exists() and not (temp_dir / "thumbnail_9x16.png").exists():
                render_thumbnail_still(temp_dir)
            print(f"[3/5] Rendering {args.comp} (60fps, --gl=angle)...")
            render_cmd = f'npx remotion render {args.comp} "{raw_mp4.as_posix()}" --gl=angle --concurrency=4'
            subprocess.run(render_cmd, shell=True, cwd=str(REMOTION_DIR), check=True)
        elif (temp_dir / "thumb_props.json").exists() and not (temp_dir / "thumbnail_9x16.png").exists():
            stage_assets_temporarily(assets_dir)
            render_thumbnail_still(temp_dir)
    finally:
        cleanup_staged_assets(remove_temp_geo=staged_geo or TEMP_GEO_PATHS_DEST.exists())

    if not raw_mp4.exists():
        raise FileNotFoundError(f"Không tìm thấy raw_video.mp4: {raw_mp4}")

    raw_sec = get_video_duration_sec(raw_mp4)
    # Khóa chặt thời lượng đầu ra theo voice_sec (tối đa +0.25s để tròn nhịp cuối, CẤM chạy trôi im lặng)
    total_sec = round(min(raw_sec, voice_sec + 0.25), 3)
    print(f"[DURATION LOCK] voice={voice_sec:.2f}s | raw_mp4={raw_sec:.2f}s -> locked_output={total_sec:.2f}s")

    # 4. Đọc script_5beat.json (lấy script_text, sfx_keywords, bgm_mood) & Cào âm thanh 6 vai trò tươi mới nếu thiếu
    print("[4/5] Mixing master audio (-14.0 LUFS, voice-clear, Vacuum Drop)...")
    script_text = ""
    script_sfx_keywords = args.sfx_keywords.strip()
    script_bgm_mood = (args.bgm_mood or args.mood).strip()
    script_json_path = temp_dir / "script_5beat.json"
    if script_json_path.exists():
        try:
            sdata = json.loads(script_json_path.read_text(encoding="utf-8"))
            if isinstance(sdata, dict):
                if not script_sfx_keywords and sdata.get("sfx_keywords"):
                    raw_kw = sdata["sfx_keywords"]
                    script_sfx_keywords = ",".join(raw_kw) if isinstance(raw_kw, list) else str(raw_kw)
                if not args.bgm_mood and isinstance(sdata.get("bgm_mood"), str) and sdata["bgm_mood"].strip():
                    script_bgm_mood = sdata["bgm_mood"].strip()
                parts = []
                for k in ("title", "topic", "full_script", "script"):
                    if isinstance(sdata.get(k), str) and sdata[k].strip():
                        parts.append(sdata[k].strip())
                for b in sdata.get("beats", []) or []:
                    if isinstance(b, dict):
                        txt = b.get("voiceover") or b.get("narration") or b.get("text") or b.get("script")
                        if isinstance(txt, str) and txt.strip():
                            parts.append(txt.strip())
                    elif isinstance(b, str) and b.strip():
                        parts.append(b.strip())
                script_text = " ".join(parts).strip() or script_json_path.read_text(encoding="utf-8")[:1500]
            else:
                script_text = script_json_path.read_text(encoding="utf-8")[:1500]
        except Exception as exc:
            print(f"[WARN] Không đọc được script_5beat.json cho mix audio: {exc}")

    sfx_dir = temp_dir / "sfx"
    has_role_sfx = sfx_dir.exists() and any(sfx_dir.glob("role_*.mp3"))
    has_cta_sfx = sfx_dir.exists() and any(sfx_dir.glob("role_cta_*.mp3"))
    if not has_role_sfx or not has_cta_sfx:
        harv_cmd = [
            sys.executable, str(ENGINE_DIR / "audio_harvester.py"),
            "--project", str(project_dir),
            "--sfx-only",
        ]
        if script_sfx_keywords:
            harv_cmd.extend(["--sfx-keywords", script_sfx_keywords])
        low_script = script_text.lower()
        if any(tok in low_script for tok in ("tiền", "đồng", "vnđ", "vnd", "usd", "$", "tỷ", "triệu", "giá", "cước")):
            harv_cmd.append("--include-money")
        subprocess.run(harv_cmd, check=False)
    if sfx_dir.exists():
        set_project_sfx_dir(sfx_dir)

    bp_path = temp_dir / "choreography_blueprint.json"
    beat_ts, bgm_segments = extract_beat_timestamps_and_bgm_segments(
        bp_path=bp_path,
        tsx_path=tsx_path,
        script_json_path=script_json_path,
        total_sec=total_sec,
    )
    sfx_cues, vac_drops = auto_choreograph_script_sfx_cues(
        words_json_path=words_path,
        total_duration_sec=total_sec,
        beat_timestamps=beat_ts,
        blueprint_json_path=bp_path if bp_path.exists() else None,
    )

    master_wav = temp_dir / "master_audio.wav"
    mix_reels_master_audio(
        voice_wav=voice_wav,
        output_wav=master_wav,
        sfx_cues=sfx_cues,
        total_duration_sec=total_sec,
        bgm_path=None,
        script_topic=out_name,
        script_text=script_text,
        beat_timestamps=beat_ts,
        bgm_segments=bgm_segments,
        mood=script_bgm_mood,
        bgm_base_volume=0.85,
        bgm_duck_volume=0.50,
        vacuum_drops=vac_drops,
        words_json_path=words_path,
    )

    # 5. Mux + Dual-Embed Thumbnail 3D (Frame 00:00 + attached_pic) + Bàn giao đủ 3 file cuối sang D:\Video thành phẩm\
    OUT_FINAL_DIR.mkdir(parents=True, exist_ok=True)
    final_mp4 = OUT_FINAL_DIR / f"{out_name}_FB_Reels_Master.mp4"
    final_thumb = OUT_FINAL_DIR / f"{out_name}_Thumbnail_9x16.png"
    final_seo = OUT_FINAL_DIR / f"{out_name}_SEO_Titles.txt"
    temp_mux = temp_dir / "temp_muxed.mp4"
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(raw_mp4), "-i", str(master_wav),
            "-map", "0:v:0", "-map", "1:a:0",
            "-t", f"{total_sec:.3f}",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "320k",
            "-shortest", str(temp_mux),
        ],
        check=True,
    )

    thumb_cand = None
    for tp in (temp_dir / "thumbnail_9x16.png", OUT_FINAL_DIR / f"{out_name}_thumbnail.png", final_thumb):
        if tp.exists():
            thumb_cand = tp
            break

    if thumb_cand:
        if thumb_cand.resolve() != final_thumb.resolve():
            shutil.copy2(thumb_cand, final_thumb)
        try:
            from thumbnail_3d_seo_engine import embed_thumbnail_into_video
            shutil.copy2(temp_mux, final_mp4)
            embed_thumbnail_into_video(final_mp4, thumb_cand, temp_dir, prepend_cover_frames=True)
        except Exception as exc:
            print(f"[WARN] Dual-embed fallback sang attached_pic: {exc}")
            subprocess.run(
                [
                    "ffmpeg", "-y", "-i", str(temp_mux), "-i", str(thumb_cand),
                    "-map", "0", "-map", "1", "-c", "copy", "-c:v:1", "png",
                    "-disposition:v:1", "attached_pic", "-movflags", "+faststart",
                    str(final_mp4),
                ],
                check=True,
            )
    else:
        shutil.copy2(temp_mux, final_mp4)

    for seo_cand in (temp_dir / "SEO_Titles.txt", temp_dir / "seo_titles.txt", temp_dir / f"{out_name}_SEO_Titles.txt"):
        if seo_cand.exists():
            shutil.copy2(seo_cand, final_seo)
            break

    # 6. Post-Render Visual & Audio QC Gate + Contact Sheet 3x3 + Kiểm tra Đầu Não 0 bytes rác
    print("[5/5] Running Post-Render QC Gate (Anti-Void, LUFS, 3x3 Contact Sheet, Zero-Trash Brain)...")
    grid_path = temp_dir / "qc_grid_3x3.jpg"
    report = qc_gate.check_video(
        final_mp4,
        grid_path,
        project_dir=project_dir,
        tsx_path=tsx_path if tsx_path.exists() else None,
    )
    if report.get("passed") and not report.get("layout_history_recorded") and tsx_path.exists():
        sig = qc_gate.extract_layout_signature(tsx_path.read_text(encoding="utf-8"))
        qc_gate.record_visual_layout_history(
            project_name=project_dir.name,
            opening_style=sig["opening_style"],
            component_sequence=sig["component_sequence"],
        )
        report["layout_history_recorded"] = True
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"FINAL MP4: {final_mp4}")
    if final_thumb.exists():
        print(f"FINAL THUMBNAIL: {final_thumb}")
    if final_seo.exists():
        print(f"FINAL SEO TITLES: {final_seo}")
    print(f"QC GRID 3x3: {grid_path}")
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
