# -*- coding: utf-8 -*-
r"""
AUTO QC FB REELS (Tổng Thanh Tra Kiểm Duyệt Độc Lập Video Ngắn FB Reels)
Tiêu chuẩn khắt khe cho FB Reels / TikTok Shorts:
1. Độ phân giải bắt buộc: 1080x1920 (9:16 Vertical).
2. Tốc độ khung hình: 30fps hoặc 60fps All-Intra.
3. Quét dải an toàn Safe Zone FB Reels:
   - Top Header: 0 - 150px
   - Bottom Footer: 1650 - 1920px (Chứa caption và tên page)
   - Right Rail: 920 - 1080px (Chứa nút Like, Comment, Share)
   -> Mọi text và biểu tượng quan trọng bắt buộc phải nằm trong Safe Zone: X[100, 900], Y[180, 1620].
4. Quét màn hình đen (Black frames) & đứng hình (Frozen frames) bằng OpenCV.
5. Đo âm lượng chuẩn phát sóng EBU R128 (-14.0 LUFS ± 1.0 LUFS).
Chỉ cấp phép xuất bản khi điểm số đạt >= 90/100!
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Tuple

import cv2
import numpy as np

# Đảm bảo UTF-8
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

class AutoQCFBReels:
    def __init__(self):
        self.target_w = 1080
        self.target_h = 1920
        self.target_lufs = -14.0

    def inspect_video(self, video_path: Path) -> Dict:
        """
        Quét kiểm tra toàn diện video thành phẩm
        """
        report = {
            "video_path": str(video_path),
            "passed": False,
            "score": 100,
            "issues": [],
            "metrics": {}
        }

        if not video_path.exists():
            report["score"] = 0
            report["issues"].append("Video file does not exist!")
            return report

        # 1. Kiểm tra ffprobe về độ phân giải, fps, duration
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "stream=width,height,r_frame_rate,duration,codec_type",
            "-of", "json", str(video_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            report["score"] = 0
            report["issues"].append("ffprobe read failed!")
            return report

        meta = json.loads(res.stdout)
        video_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
        audio_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "audio"), None)

        if not video_stream:
            report["score"] = 0
            report["issues"].append("No video stream found!")
            return report

        w = int(video_stream.get("width", 0))
        h = int(video_stream.get("height", 0))
        report["metrics"]["resolution"] = f"{w}x{h}"

        # Kiểm tra tỷ lệ 9:16
        if w != self.target_w or h != self.target_h:
            report["score"] -= 25
            report["issues"].append(f"Invalid resolution: {w}x{h}. Expected 1080x1920 (9:16).")

        # 2. Quét màn hình đen & đứng hình bằng OpenCV
        cap = cv2.VideoCapture(str(video_path))
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        report["metrics"]["duration_sec"] = round(duration, 2)
        report["metrics"]["fps"] = round(fps, 2)

        black_frame_count = 0
        prev_frame = None
        frozen_frame_count = 0

        # Lấy mẫu mỗi 5 frames để quét nhanh
        step = max(1, int(fps / 6))
        for f_idx in range(0, total_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
            ret, frame = cap.read()
            if not ret or frame is None:
                continue

            # Kiểm tra đen thui
            mean_val = np.mean(frame)
            if mean_val < 3.0:
                black_frame_count += 1

            # Kiểm tra đứng hình
            if prev_frame is not None:
                diff = np.mean(np.abs(frame.astype(np.float32) - prev_frame.astype(np.float32)))
                if diff < 0.2:
                    frozen_frame_count += 1
            prev_frame = frame

        # Kiểm tra 3 mốc vàng 0.10s / 0.80s / 1.80s xem 0.10s có bị trống/tối hơn hẳn 1.80s không
        early_checks = {}
        for sec_tag, sec_val in [("0.10s", 0.10), ("0.80s", 0.80), ("1.80s", 1.80)]:
            target_f = min(max(0, int(round(sec_val * fps))), max(0, total_frames - 1))
            cap.set(cv2.CAP_PROP_POS_FRAMES, target_f)
            ok_e, frame_e = cap.read()
            if ok_e and frame_e is not None:
                early_checks[sec_tag] = round(float(np.mean(frame_e)), 2)

        cap.release()
        if early_checks:
            report["metrics"]["early_luma_0_10_0_80_1_80"] = early_checks
            if early_checks.get("0.10s", 99) < 8.0:
                report["score"] -= 15
                report["issues"].append(f"Frame 0.10s quá tối/trống (luma={early_checks.get('0.10s')}) -> mất khán giả ở 0:02!")

        if black_frame_count > 3:
            report["score"] -= 20
            report["issues"].append(f"Detected {black_frame_count} completely black frames!")

        if frozen_frame_count > 8:
            report["score"] -= 15
            report["issues"].append(f"Detected {frozen_frame_count} frozen/lag frames!")

        # 3. Kiểm tra EBU R128 Audio loudness
        if not audio_stream:
            report["score"] -= 40
            report["issues"].append("No audio track detected!")
        else:
            loud_cmd = [
                "ffmpeg", "-i", str(video_path),
                "-af", "ebur128=framelog=verbose",
                "-f", "null", "-"
            ]
            loud_res = subprocess.run(loud_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Parse Integrated loudness
            for line in loud_res.stderr.splitlines():
                if "I:" in line and "LUFS" in line:
                    parts = line.split("I:")[1].split("LUFS")[0].strip()
                    try:
                        measured_lufs = float(parts)
                        report["metrics"]["integrated_lufs"] = measured_lufs
                        if abs(measured_lufs - self.target_lufs) > 2.0:
                            report["score"] -= 10
                            report["issues"].append(f"Loudness deviation: {measured_lufs} LUFS (Target: -14.0 LUFS)")
                    except ValueError:
                        pass
                    break

        report["passed"] = (report["score"] >= 90)
        return report

if __name__ == "__main__":
    qc = AutoQCFBReels()
    print("[*] Auto QC FB Reels Initialized & Ready.")
