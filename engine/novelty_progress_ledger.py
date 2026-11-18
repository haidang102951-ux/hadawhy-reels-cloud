"""
NOVELTY & PROGRESS LEDGER - Luật Tiến Hóa & Độc Bản bắt buộc cho mọi kịch bản mới.

Mỗi tập mới BẮT BUỘC:
  1. Không tái sử dụng bất kỳ asset (ảnh/video/cutout) nào của tập cũ (so khớp SHA1 nội dung).
  2. Không trùng bảng màu chủ đạo với tập liền trước (Jaccard màu hex <= 0.5).
  3. Không trùng bộ hiệu ứng FX với tập liền trước (Jaccard FX <= 0.6) và không trùng chuỗi FX theo thứ tự.
  4. Không trùng câu Hook / tiêu đề Beat với bất kỳ tập cũ nào.
  5. Điểm Tiến Bộ (progress_score) phải >= điểm tập liền trước VÀ >= benchmark NvidiaSuccession40s.

Dùng:
  python novelty_progress_ledger.py check    --tsx <file.tsx> --project <D:\\DuAn_DangLam\\id>
  python novelty_progress_ledger.py register --tsx <file.tsx> --project <D:\\DuAn_DangLam\\id>
  python novelty_progress_ledger.py seed     (đăng ký các tập cũ làm mốc so sánh)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

ENGINE_DIR = Path(__file__).resolve().parent
LEDGER_PATH = ENGINE_DIR / "novelty_progress_ledger.json"
REMOTION_DIR = ENGINE_DIR.parent / "remotion_reels"
PUBLIC_DIR = REMOTION_DIR / "public"
BENCHMARK_ID = "NvidiaSuccession40s"

# Tài sản thương hiệu cố định được phép dùng lại (logo, font) - KHÔNG tính là tái sử dụng nội dung
BRAND_WHITELIST_PREFIXES = ("brand/", "fonts/", "sfx/", "audio/", "music/", "maps/")

FX_PRIMITIVES = (
    "WhipPanTransition", "ZoomThroughTransition", "SplitCurtainWipe", "Tilt3DFlip",
    "MarkerHighlightText", "StaggerWaveText", "GlitchSplitText", "MetallicSweepText",
    "OdometerCounter", "ParallaxDepthStage", "DotMatrixZoom", "FlowPipeline3D",
    "DecisionBranchPulse", "Real3DPhotoStage", "DataBars3D", "MotionTrackedCallout",
    "ScaleComparison3D", "TimelineTrack3D", "GeoStrategicMap3D",
    "RealPersonSpotlight3D", "CoinStream", "AnatomyCallout3D", "KineticHookHeader",
    "KineticWordCaption",
)
KNOWLEDGE_PRIMITIVES = (
    "DotMatrixZoom", "FlowPipeline3D", "DecisionBranchPulse", "DataBars3D",
    "Real3DPhotoStage", "MotionTrackedCallout", "ScaleComparison3D",
    "TimelineTrack3D", "GeoStrategicMap3D", "AnatomyCallout3D", "OdometerCounter", "CoinStream",
)


def _load_ledger() -> dict:
    if LEDGER_PATH.exists():
        return json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    return {"episodes": []}


def _save_ledger(ledger: dict) -> None:
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")


def _sha1(path: Path) -> str:
    h = hashlib.sha1()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / max(1, len(a | b))


def fingerprint(tsx_path: Path, project_dir: Path | None) -> dict:
    code = tsx_path.read_text(encoding="utf-8")

    # Asset nội dung (bỏ qua brand/font/sfx)
    asset_refs = sorted(set(re.findall(r"staticFile\(\s*[\"'`]([^\"'`]+)[\"'`]", code))
                        | set(re.findall(r"src=\s*[\"']([a-zA-Z0-9_\-/]+\.(?:png|jpg|jpeg|webp|mp4|mov))[\"']", code)))
    content_assets = [a for a in asset_refs if not a.startswith(BRAND_WHITELIST_PREFIXES)]
    asset_hashes = {}
    for rel in content_assets:
        p = PUBLIC_DIR / rel
        if p.exists() and p.is_file():
            asset_hashes[rel] = _sha1(p)

    colors = sorted({c.upper() for c in re.findall(r"#[0-9A-Fa-f]{6}\b", code)}
                    - {"#FFFFFF", "#000000"})

    fx_order = [m.group(1) for m in re.finditer(r"<(" + "|".join(FX_PRIMITIVES) + r")\b", code)]
    fx_set = sorted(set(fx_order))
    knowledge_layers = sum(1 for m in fx_order if m in KNOWLEDGE_PRIMITIVES) + len(re.findall(r"<svg\b", code))

    hook_texts = sorted({t.strip().upper() for t in re.findall(
        r"(?:hook|title|headline|text)\s*[:=]\s*[\"'`]([^\"'`]{6,90})[\"'`]", code, re.IGNORECASE)})

    sequences = len(re.findall(r"<Sequence\b", code))
    springs = len(re.findall(r"\bspring\(", code))

    sfx_files: list[str] = []
    distinct_sfx = 0
    if project_dir:
        for cand in ("sfx_cues.json", "sfx_plan.json"):
            cp = project_dir / "temp" / cand
            if not cp.exists():
                cp = project_dir / cand
            if cp.exists():
                try:
                    data = json.loads(cp.read_text(encoding="utf-8"))
                    items = data.get("cues", data) if isinstance(data, dict) else data
                    sfx_files = [str(c[0] if isinstance(c, list) else c.get("file", "")) for c in items]
                    distinct_sfx = len(set(sfx_files))
                except Exception:
                    pass
                break

    progress_score = round(
        len(fx_set) * 3.0
        + knowledge_layers * 4.0
        + min(sequences, 40) * 0.5
        + min(springs, 60) * 0.2
        + distinct_sfx * 1.0,
        2,
    )

    return {
        "episode_id": project_dir.name if project_dir else tsx_path.stem,
        "composition": tsx_path.stem,
        "registered_at": datetime.now().isoformat(timespec="seconds"),
        "asset_hashes": asset_hashes,
        "colors": colors,
        "fx_set": fx_set,
        "fx_order": fx_order,
        "knowledge_layers": knowledge_layers,
        "hook_texts": hook_texts,
        "sequences": sequences,
        "distinct_sfx": distinct_sfx,
        "progress_score": progress_score,
    }


def check(tsx_path: Path, project_dir: Path) -> dict:
    ledger = _load_ledger()
    fp = fingerprint(tsx_path, project_dir)
    past = [e for e in ledger["episodes"] if e["composition"] != fp["composition"] and e["episode_id"] != fp["episode_id"]]
    issues: list[str] = []

    if not past:
        return {"passed": True, "issues": [], "fingerprint": fp, "note": "Ledger trống - chạy 'seed' để có mốc so sánh."}

    last = past[-1]
    benchmark = next((e for e in past if e["composition"] == BENCHMARK_ID), None)

    # 1. Tái sử dụng asset cũ (theo nội dung SHA1)
    old_hashes = {}
    for e in past:
        for rel, h in e.get("asset_hashes", {}).items():
            old_hashes.setdefault(h, f"{e['episode_id']}:{rel}")
    reused = [f"{rel} (trùng {old_hashes[h]})" for rel, h in fp["asset_hashes"].items() if h in old_hashes]
    if reused:
        issues.append("TÁI SỬ DỤNG ASSET CŨ: " + "; ".join(reused[:6]))

    # 2. Bảng màu trùng tập liền trước
    cj = _jaccard(set(fp["colors"]), set(last.get("colors", [])))
    if cj > 0.5:
        issues.append(f"BẢNG MÀU RẬP KHUÔN: trùng {cj:.0%} với tập {last['episode_id']} (tối đa 50%). Đổi DNA màu theo chủ đề mới.")

    # 3. Bộ FX trùng
    fj = _jaccard(set(fp["fx_set"]), set(last.get("fx_set", [])))
    if fj > 0.6:
        issues.append(f"HIỆU ỨNG RẬP KHUÔN: bộ FX trùng {fj:.0%} với tập {last['episode_id']} (tối đa 60%).")
    if fp["fx_order"] and fp["fx_order"] == last.get("fx_order"):
        issues.append(f"CHUỖI HIỆU ỨNG Y HỆT tập {last['episode_id']} theo đúng thứ tự - cấm sao chép bố cục.")

    # 4. Hook trùng
    old_hooks = {h for e in past for h in e.get("hook_texts", [])}
    dup_hooks = [h for h in fp["hook_texts"] if h in old_hooks]
    if dup_hooks:
        issues.append("HOOK/TIÊU ĐỀ TRÙNG TẬP CŨ: " + " | ".join(dup_hooks[:4]))

    # 5. Điểm tiến bộ: phải >= tập TỐT NHẤT từng làm (không bao giờ thụt lùi)
    best = max(past, key=lambda e: e["progress_score"])
    floor, floor_src = best["progress_score"], best["episode_id"]
    if benchmark and benchmark["progress_score"] > floor:
        floor, floor_src = benchmark["progress_score"], BENCHMARK_ID
    if fp["progress_score"] < floor:
        issues.append(
            f"THỤT LÙI: progress_score {fp['progress_score']} < {floor} của {floor_src}. "
            "Phải tăng số lớp kiến thức động, đa dạng FX và SFX so với tập trước."
        )

    return {"passed": not issues, "issues": issues, "fingerprint": fp,
            "compared_with": last["episode_id"], "score_floor": floor}


def register(tsx_path: Path, project_dir: Path | None) -> dict:
    ledger = _load_ledger()
    fp = fingerprint(tsx_path, project_dir)
    ledger["episodes"] = [e for e in ledger["episodes"] if e["composition"] != fp["composition"]]
    ledger["episodes"].append(fp)
    _save_ledger(ledger)
    return fp


def seed() -> list[dict]:
    src = REMOTION_DIR / "src"
    mapping = [
        ("Friday13Origins45s.tsx", None),
        ("NvidiaSuccession40s.tsx", None),
        ("RapPhimBongNgo42s.tsx", None),
        ("VanHoaNhauViaHe40s.tsx", Path(r"D:\DuAn_DangLam\van_hoa_nhau_vn")),
        ("BiMatVeSo40s.tsx", Path(r"D:\DuAn_DangLam\bi_mat_ve_so_vn")),
    ]
    out = []
    for fname, proj in mapping:
        p = src / fname
        if p.exists():
            out.append(register(p, proj if proj and proj.exists() else None))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("action", choices=["check", "register", "seed"])
    ap.add_argument("--tsx")
    ap.add_argument("--project")
    a = ap.parse_args()
    if a.action == "seed":
        res = seed()
        print(json.dumps([{k: r[k] for k in ("composition", "progress_score", "fx_set")} for r in res], ensure_ascii=False, indent=2))
        return 0
    tsx, proj = Path(a.tsx), Path(a.project) if a.project else None
    if a.action == "register":
        print(json.dumps(register(tsx, proj), ensure_ascii=False, indent=2))
        return 0
    res = check(tsx, proj)
    print(json.dumps({k: v for k, v in res.items() if k != "fingerprint"}, ensure_ascii=False, indent=2))
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
