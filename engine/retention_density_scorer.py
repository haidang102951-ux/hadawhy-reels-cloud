"""
RETENTION DENSITY SCORER - chấm điểm sức giữ chân TRƯỚC KHI RENDER (và kiểm lại SAU render).

Luật:
  1. Không có cửa sổ 1.5s nào (90 frame @60fps) trống sự kiện thị giác (cắt cảnh, chữ bật, số nhảy, hiệu ứng mới).
  2. Câu hỏi mở vòng (open loop) phải xuất hiện trong 3s đầu.
  3. Phải có re-hook (câu hỏi / đảo chiều / con số sốc) quanh mốc ~10s và ~20s (cửa sổ ±3s).
  4. Mật độ trung bình >= 1 sự kiện thị giác / 1.2s.

Nguồn sự kiện:
  - choreography_blueprint.json: trường "events" (list frame) hoặc "frames" của từng beat (bắt buộc).
  - .tsx: from={N}, startFrame={N}, lockFrame: N, impactFrames=[...], Sequence from.
  - words.json: phát hiện câu hỏi/từ khóa re-hook theo thời gian giọng đọc.
  - (tùy chọn) --video: đo cắt cảnh thực tế bằng ffmpeg scene detection sau render.

Dùng:
  python retention_density_scorer.py --tsx <file.tsx> --project <D:\\DuAn_DangLam\\id> [--video out.mp4]
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

FPS = 60
WINDOW_SEC = 1.5
MIN_DENSITY_PER_SEC = 1 / 1.2

QUESTION_MARKERS = (
    "?", "tại sao", "vì sao", "sao lại", "bao nhiêu", "liệu", "có biết", "ai ", "điều gì",
    "thế nào", "làm sao", "bí mật", "sự thật", "nhưng", "thực ra", "ngược lại", "sốc",
)


def _words(project_dir: Path) -> list[dict]:
    for cand in (project_dir / "temp" / "words.json", project_dir / "words.json"):
        if cand.exists():
            data = json.loads(cand.read_text(encoding="utf-8"))
            items = data.get("words", data) if isinstance(data, dict) else data
            out = []
            for w in items:
                st = w.get("start", w.get("startMs", 0) / 1000.0 if "startMs" in w else 0.0)
                txt = w.get("word", w.get("text", ""))
                out.append({"start": float(st), "text": str(txt)})
            return out
    return []


def _blueprint_events(project_dir: Path) -> tuple[list[int], int]:
    for cand in (project_dir / "temp" / "choreography_blueprint.json", project_dir / "choreography_blueprint.json"):
        if cand.exists():
            bp = json.loads(cand.read_text(encoding="utf-8"))
            total = int(bp.get("total_frames", 0))
            ev: list[int] = []
            for b in bp.get("beats", []):
                for e in b.get("events", []) or []:
                    if isinstance(e, (int, float)):
                        ev.append(int(e))
                    elif isinstance(e, dict) and "frame" in e:
                        ev.append(int(e["frame"]))
                fr = str(b.get("frames", ""))
                m = re.match(r"\s*(\d+)", fr)
                if m:
                    ev.append(int(m.group(1)))
            return ev, total
    return [], 0


def _tsx_events(tsx: Path) -> list[int]:
    code = tsx.read_text(encoding="utf-8")
    ev = [int(x) for x in re.findall(r"(?:from|startFrame)\s*=\s*\{\s*(\d+)\s*\}", code)]
    ev += [int(x) for x in re.findall(r"(?:lockFrame|startFrame|from|frame)\s*:\s*(\d+)", code)]
    for arr in re.findall(r"(?:impactFrames|eventFrames|cutFrames)\s*=\s*\[([^\]]+)\]", code):
        ev += [int(x) for x in re.findall(r"\d+", arr)]
    return ev


def _video_cuts(video: Path) -> list[int]:
    cmd = ["ffmpeg", "-hide_banner", "-i", str(video), "-vf", "select='gt(scene,0.06)',showinfo", "-f", "null", "-"]
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return [int(float(t) * FPS) for t in re.findall(r"pts_time:([\d.]+)", proc.stderr)]


def _learned_window_sec() -> float:
    """Siết cửa sổ khoảng chết theo nhịp cắt đã học từ video viral (viral_patterns_kb.json)."""
    kb = Path(__file__).resolve().parent / "viral_patterns_kb.json"
    if kb.exists():
        try:
            samples = json.loads(kb.read_text(encoding="utf-8")).get("samples", [])
            vals = [s["recommended_rules"]["target_cut_interval_sec"] for s in samples if s.get("recommended_rules")]
            if vals:
                return max(0.8, min(WINDOW_SEC, sum(vals) / len(vals)))
        except Exception:
            pass
    return WINDOW_SEC


def score(tsx: Path, project_dir: Path, video: Path | None = None) -> dict:
    issues: list[str] = []
    window_sec = _learned_window_sec()
    bp_events, total_frames = _blueprint_events(project_dir)
    events = sorted(set(bp_events + _tsx_events(tsx) + (_video_cuts(video) if video else [])))
    words = _words(project_dir)
    if not total_frames:
        total_frames = int((words[-1]["start"] + 1.5) * FPS) if words else (max(events) if events else 0)
    events = [e for e in events if 0 <= e <= total_frames]
    dur = total_frames / FPS if total_frames else 0.0

    if not bp_events:
        issues.append("BLUEPRINT THIẾU: choreography_blueprint.json phải có 'events' (frame từng sự kiện thị giác) cho mỗi beat.")

    # 1. Cửa sổ trống
    win = int(window_sec * FPS)
    dead: list[str] = []
    pts = [0] + events + [total_frames]
    for a, b in zip(pts, pts[1:]):
        if b - a > win:
            dead.append(f"{a / FPS:.2f}s-{b / FPS:.2f}s ({(b - a) / FPS:.2f}s)")
    if dead:
        issues.append(f"KHOẢNG CHẾT THỊ GIÁC > {window_sec:.2f}s: " + "; ".join(dead[:8]))

    # 2-3. Open loop & re-hook
    def has_hook(t0: float, t1: float) -> bool:
        seg = " ".join(w["text"].lower() for w in words if t0 <= w["start"] <= t1)
        return any(m in seg for m in QUESTION_MARKERS)

    if words:
        if not has_hook(0.0, 3.0):
            issues.append("THIẾU OPEN LOOP: 3s đầu không có câu hỏi/bí mật/nghịch lý gài tò mò.")
        for mark in (10.0, 20.0):
            if dur > mark + 2 and not has_hook(mark - 3, mark + 3):
                issues.append(f"THIẾU RE-HOOK quanh {mark:.0f}s (±3s): cần câu hỏi, đảo chiều hoặc con số sốc.")
    else:
        issues.append("THIẾU words.json: không kiểm được open loop / re-hook.")

    # 4. Mật độ
    density = (len(events) / dur) if dur else 0.0
    if density < MIN_DENSITY_PER_SEC:
        issues.append(f"MẬT ĐỘ THẤP: {density:.2f} sự kiện/giây (tối thiểu {MIN_DENSITY_PER_SEC:.2f}).")

    retention_score = max(0, round(100 - len(dead) * 8 - (0 if density >= MIN_DENSITY_PER_SEC else 15)
                                   - sum(10 for i in issues if "HOOK" in i or "OPEN LOOP" in i), 1))
    return {
        "passed": not issues,
        "retention_score": retention_score,
        "duration_sec": round(dur, 2),
        "visual_events": len(events),
        "density_per_sec": round(density, 2),
        "issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsx", required=True)
    ap.add_argument("--project", required=True)
    ap.add_argument("--video")
    a = ap.parse_args()
    res = score(Path(a.tsx), Path(a.project), Path(a.video) if a.video else None)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
