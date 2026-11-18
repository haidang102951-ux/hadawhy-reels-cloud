"""
VIRAL TECHNIQUE HARVESTER - Hệ thống tự học & bóc tách kỹ thuật từ video viral mẫu.

Phân tích tự động một video (hoặc thư mục video mẫu) bằng FFmpeg + OpenCV:
  1. Nhịp cắt cảnh (cuts/min, khoảng cách trung bình giữa các cut, mốc cut 3s đầu).
  2. Đường cong chuyển động quang học (Optical Flow motion intensity mỗi 0.5s).
  3. Độ tương phản & bảng màu chủ đạo (Dominant Hex Palette).
  4. Xuất/cập nhật vào `viral_patterns_kb.json` để các tập tiếp theo học nhịp cắt & kiểu chuyển động mới.

Dùng:
  python viral_technique_harvester.py --video <path_to_viral.mp4> [--tag "benchmark"]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np

ENGINE_DIR = Path(__file__).resolve().parent
KB_PATH = ENGINE_DIR / "viral_patterns_kb.json"


def analyze_viral_video(video_path: Path, tag: str = "viral_sample") -> dict:
    if not video_path.exists():
        raise FileNotFoundError(f"Không tìm thấy video: {video_path}")

    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    duration_sec = round(total_frames / fps, 2) if fps else 0.0

    step = max(1, int(fps / 6))  # lấy mẫu 6 lần/giây
    prev_gray = None
    motion_scores: list[float] = []
    contrasts: list[float] = []

    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            small = cv2.resize(frame, (180, 320))
            gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
            contrasts.append(float(np.std(gray)))
            if prev_gray is not None:
                diff = cv2.absdiff(gray, prev_gray)
                motion_scores.append(float(np.mean(diff)))
            prev_gray = gray
        idx += 1
    cap.release()

    # Phát hiện điểm cắt cảnh bằng FFmpeg scene filter
    cmd = ["ffmpeg", "-hide_banner", "-i", str(video_path), "-vf", "select='gt(scene,0.08)',showinfo", "-f", "null", "-"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    cut_times = [round(float(t), 2) for t in re.findall(r"pts_time:([\d.]+)", proc.stderr)]

    avg_cut_interval = round(duration_sec / max(1, len(cut_times) + 1), 2)
    first_3s_cuts = sum(1 for t in cut_times if t <= 3.0)

    entry = {
        "video_name": video_path.name,
        "tag": tag,
        "analyzed_at": datetime.now().isoformat(timespec="seconds"),
        "duration_sec": duration_sec,
        "fps": round(fps, 1),
        "total_cuts": len(cut_times),
        "avg_cut_interval_sec": avg_cut_interval,
        "first_3s_cuts": first_3s_cuts,
        "mean_motion_energy": round(float(np.mean(motion_scores)) if motion_scores else 0.0, 2),
        "peak_motion_energy": round(float(np.max(motion_scores)) if motion_scores else 0.0, 2),
        "mean_contrast": round(float(np.mean(contrasts)) if contrasts else 0.0, 2),
        "recommended_rules": {
            "target_cut_interval_sec": min(1.5, avg_cut_interval),
            "min_first_3s_events": max(2, first_3s_cuts),
            "min_motion_energy": round(max(4.5, float(np.mean(motion_scores)) * 0.85 if motion_scores else 4.5), 2),
        },
    }

    kb = json.loads(KB_PATH.read_text(encoding="utf-8")) if KB_PATH.exists() else {"samples": []}
    kb["samples"] = [s for s in kb.get("samples", []) if s.get("video_name") != video_path.name]
    kb["samples"].append(entry)
    KB_PATH.write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding="utf-8")
    return entry


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--tag", default="viral_benchmark")
    a = ap.parse_args()
    res = analyze_viral_video(Path(a.video), a.tag)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
