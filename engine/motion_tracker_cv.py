"""
MOTION TRACKER CV - Bám theo tọa độ vật thể đang chuyển động trong video bằng OpenCV Optical Flow (Lucas-Kanade).
Xuất ra mảng [{frame, x, y}, ...] chuẩn 1080x1920 để truyền vào <MotionTrackedCallout trackPoints={...} />.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import cv2
import numpy as np


def track_point_in_video(
    video_path: str | Path,
    init_x: float,
    init_y: float,
    start_frame: int = 0,
    max_frames: int = 240,
    target_w: int = 1080,
    target_h: int = 1920,
) -> list[dict]:
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    ok, first_frame = cap.read()
    if not ok:
        cap.release()
        return [{"frame": start_frame, "x": round(init_x, 1), "y": round(init_y, 1)}]

    first_resized = cv2.resize(first_frame, (target_w, target_h))
    old_gray = cv2.cvtColor(first_resized, cv2.COLOR_BGR2GRAY)
    p0 = np.array([[[float(init_x), float(init_y)]]], dtype=np.float32)

    lk_params = dict(
        winSize=(31, 31),
        maxLevel=3,
        criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.03),
    )

    points = [{"frame": start_frame, "x": round(float(init_x), 1), "y": round(float(init_y), 1)}]
    cur_x, cur_y = float(init_x), float(init_y)

    for idx in range(1, max_frames):
        ok, frame = cap.read()
        if not ok:
            break
        resized = cv2.resize(frame, (target_w, target_h))
        frame_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
        p1, st, _ = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        if p1 is not None and st[0][0] == 1:
            cur_x = float(np.clip(p1[0][0][0], 60, target_w - 60))
            cur_y = float(np.clip(p1[0][0][1], 100, target_h - 100))
            p0 = np.array([[[cur_x, cur_y]]], dtype=np.float32)
        points.append({"frame": start_frame + idx, "x": round(cur_x, 1), "y": round(cur_y, 1)})
        old_gray = frame_gray

    cap.release()
    return points


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--x", type=float, required=True)
    ap.add_argument("--y", type=float, required=True)
    ap.add_argument("--start-frame", type=int, default=0)
    ap.add_argument("--max-frames", type=int, default=240)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    pts = track_point_in_video(a.video, a.x, a.y, a.start_frame, a.max_frames)
    Path(a.out).write_text(json.dumps(pts, indent=2), encoding="utf-8")
    print(f"Tracked {len(pts)} frames -> {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
