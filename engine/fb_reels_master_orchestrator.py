r"""
fb_reels_master_orchestrator.py - BỘ ĐIỀU PHỐI TRUNG TÂM ĐẦU NÃO VIDEO NGẮN FB (60FPS)
Thư mục gốc: D:\Đầu Não Video Ngắn FB (không xóa)
Đích xuất bản duy nhất: D:\Video thành phẩm\<Ten_Video>.mp4

Kết nối đồng bộ toàn bộ 6 Engine cốt lõi:
1. `fact_and_retention_engine.py` : Trinh sát sự thật đa nguồn (`fact_sheet.json`) & Kiểm định 5 nhịp giữ chân (5-Beat Retention).
2. `vieneu_whisper_pacer.py`      : Sinh giọng đọc Hải Đăng + tọa độ từng từ `faster-whisper`.
3. `auto_asset_harvester.py`      : Tự động lên mạng cào Hình Thật + tách nền AI `bria-rmbg` (`auto_cutout.py`).
4. `geo_map_builder.py`           : Trích xuất tọa độ biên giới thật từ `countries.geojson` cho `GeoStrategicMap3D.tsx`.
5. `sfx_timeline_mixer.py`        : Hòa âm giọng đọc + 18 file SFX thu âm thật + BGM ducking chuẩn `-14.0 LUFS`.
6. `auto_qc_fb_reels.py`          : Thanh tra kỹ thuật & xuất bản MP4 1080x1920 @ 60fps.
"""

import json
import subprocess
import sys
from pathlib import Path

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

FB_BRAIN = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
ENGINE_DIR = FB_BRAIN / "engine"
REMOTION_DIR = FB_BRAIN / "remotion_reels"
FINAL_OUT_DIR = Path(r"D:\Video thành phẩm")

if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from fact_and_retention_engine import build_verified_fact_sheet, validate_short_script_retention
from auto_asset_harvester import harvest_script_manifest, purge_harvested_folder, harvest_bespoke_3d_object
from geo_map_builder import build_geo_paths_ts
from semantic_scene_planner import build_semantic_production_plan, detect_script_theme_dna
from sfx_timeline_mixer import mix_reels_master_audio


def execute_step1_research_and_script(topic_vi: str, topic_en: str, out_dir: Path | None = None) -> dict:
    """
    Bước 1: Trinh sát sự thật 100% báo chí (Zero-Hallucination) -> Lập fact_sheet.json.
    Đạo Diễn Biên Kịch fb-reels-fact-scriptwriter dựa vào đây để viết kịch bản 5 nhịp.
    """
    if out_dir is None:
        out_dir = FB_BRAIN / "temp_render"
    out_dir.mkdir(parents=True, exist_ok=True)
    fact_sheet_path = out_dir / "fact_sheet.json"
    facts = build_verified_fact_sheet(topic_vi, topic_en, fact_sheet_path)
    return facts


def execute_step2_semantic_blueprint(sentences: list[str], out_dir: Path | None = None) -> dict:
    """
    Bước 2: Phân tích ngữ nghĩa từng câu kịch bản -> Lập semantic_plan.json:
    - Xác định Theme DNA (Màu nền, màu chữ 80/20, nhạc nền BGM)
    - Chỉ định Visual Archetype & Hành động vật lý 2 nhịp (Beat A -> Beat B) cho từng câu.
    """
    if out_dir is None:
        out_dir = FB_BRAIN / "temp_render"
    out_dir.mkdir(parents=True, exist_ok=True)
    plan_path = out_dir / "semantic_plan.json"
    plan = build_semantic_production_plan(sentences, plan_path)
    return plan


def execute_step3_purge_and_harvest(entities: list[dict]) -> list[dict]:
    """
    Bước 3: Dọn sạch kho ảnh kịch bản cũ (purge_harvested_folder)
    và cào ảnh thật HD tách nền AI bria-rmbg + nạp vật thể 3D đặc thù khớp 100% kịch bản.
    """
    purge_harvested_folder()
    manifest = harvest_script_manifest(entities)
    return manifest


def execute_step4_pre_render_gate(tsx_path: Path, project_dir: Path) -> dict:
    """Bước 4: Chạy cổng khóa cứng trước render (nền ADN Mức 1 #42B2F2, cấm lưới, cấm karaoke, chặn ảnh mờ)."""
    from pre_render_gate import inspect_composition
    res = inspect_composition(tsx_path, project_dir)
    if not res.get("passed"):
        raise RuntimeError(f"PRE-RENDER GATE FAILED: {res.get('issues')}")
    return res


def inspect_arsenal_status() -> dict:
    """Kiểm tra toàn diện trạng thái sẵn sàng của Đầu Não Video Ngắn FB."""
    gemini_cfg = Path.home() / ".gemini" / "config"
    agents_dir = gemini_cfg / "agents" if (gemini_cfg / "agents").exists() else FB_BRAIN / ".agents" / "agents"
    skills_dir = gemini_cfg / "skills" / "fb-reels-master-studio" if (gemini_cfg / "skills" / "fb-reels-master-studio").exists() else FB_BRAIN / ".agents" / "skills" / "fb-reels-master-studio"
    sfx_dir = REMOTION_DIR / "public" / "sfx"
    objects_dir = REMOTION_DIR / "public" / "objects"
    harvested_dir = REMOTION_DIR / "public" / "harvested"

    status = {
        "brain_root": str(FB_BRAIN),
        "skill_ready": (skills_dir / "SKILL.md").exists(),
        "subagents": [p.stem for p in agents_dir.glob("*.md")],
        "engines": [p.name for p in ENGINE_DIR.glob("*.py")],
        "remotion_components": [p.name for p in (REMOTION_DIR / "src" / "components").glob("*.tsx")],
        "studio_sfx_count": len(list(sfx_dir.glob("*.mp3"))),
        "objects_3d_count": len(list(objects_dir.glob("*.png"))),
        "harvested_real_assets": [p.name for p in harvested_dir.glob("*.png")],
    }
    print(json.dumps(status, ensure_ascii=False, indent=2))
    return status


if __name__ == "__main__":
    inspect_arsenal_status()
