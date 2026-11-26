# -*- coding: utf-8 -*-
r"""
qc_gate.py - CỔNG KIỂM ĐỊNH DUY NHẤT (PRE-RENDER CODE GATE + POST-RENDER VISUAL/AUDIO QC)
Thay thế toàn bộ pre_render_gate.py & auto_qc_fb_reels.py cũ.

Chốt chặn thép:
1. Pre-render (.tsx):
   - CẤM phụ đề chạy chữ karaoke đáy, CẤM icon nhựa/StickerPop, CẤM neon chói, CẤM DotMatrixZoom.
   - BẮT BUỘC có lớp bối cảnh thật mờ sâu (ContextBackdropLayer / backdropSrc / objectFit: "cover") để diệt màn hình đen rỗng.
   - BẮT BUỘC có ít nhất 2 cơ chế diễn hoạt kiến thức (FlowPipeline3D, DecisionBranchPulse, ScaleComparison3D,
     GeoStrategicMap3D, TimelineTrack3D, AnatomyCallout3D, MetricOdometerHero, <svg).
   - BẮT BUỘC có words.json & voiceover.wav trong <project>/temp/.
2. Post-render (.mp4):
   - 1080x1920, >= 30fps (chuẩn 60fps).
   - CHỐNG MÀN HÌNH ĐEN RỖNG: nếu > 68% diện tích khung hình tối đen (gray < 18) hoặc mean_luma < 26.0 -> RỚT NGAY.
   - CHỐNG SLIDE ĐỨNG IM: kiểm tra biến thiên chuyển động giữa các mốc thời gian.
   - Chuẩn âm thanh EBU R128: -14.0 LUFS (± 1.0 LUFS), True Peak <= -0.5 dBTP.
   - Xuất ảnh lưới 3x3 (qc_grid_3x3.jpg) để Con Tổng soi trực tiếp bằng mắt.
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
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

NEON_RE = re.compile(
    r"(?<![\w.-])(?<!0\s)0(?:px)?\s+0(?:px)?\s+(?:[4-9]|[1-9]\d)px\s+"
    r"(?:rgba?\(\s*(?!0\s*,\s*0\s*,\s*0\s*[,)])[^)]*\)|#[0-9A-Fa-f]{3,8}\b)",
    re.IGNORECASE,
)


VALID_ASSET_ROLES = {"prop_3d", "avatar_node", "ev_card"}

KNOWLEDGE_PRIMITIVES = (
    "SpeechPopCard25D",
    "SpeechPopCardStack25D",
    "ParallaxDepthStage",
    "Tilt3DFlip",
    "OpenHeroWatermarkStage",
    "RadialAvatarHub",
    "VisualCauseEffectFlow",
    "EditorialSplitTimeline",
    "DualStageKnowledgeLayout",
    "HighContrastConclusionCard",
    "VisualComparisonStrip",
    "ProcessStepChain",
    "VisualBarCompare",
    "EvidenceDocumentCard",
    "RadialNetworkBurst",
    "CycleDialProgress",
    "CircularAvatarNode",
    "HeroCutout3D",
    "FlowPipeline3D",
    "DecisionBranchPulse",
    "ScaleComparison3D",
    "GeoStrategicMap3D",
    "TimelineTrack3D",
    "AnatomyCallout3D",
    "CoinStream",
    "MetricOdometerHero",
    "OdometerCounter",
    "ForensicStampSlam",
    "RealPersonSpotlight3D",
    "UrbanSatelliteDive9x16",
    "MotionTrackedCallout",
    "RealSceneCameraStage",
    "EvidenceCalloutOverlay",
    "FactPunchlineCard",
    "SlashCrossOut",
    "MarkerHighlightText",
    "StaggerWaveText",
    "GlitchSplitText",
    "MetallicSweepText",
    "ForensicHighlighter",
    "EvidenceStringBoard",
    "XRayPeelReveal",
    "RealLifeArtifact",
    "BlueprintMechanism",
    "<svg",
)

# Khung dùng chung KHÔNG được tính vào chỉ số đa dạng component minh họa
SHARED_FRAME_COMPONENTS = {
    "HaDaWhyMistBackground",
    "ChannelWatermark9x16",
    "KineticHookHeader",
    "HaDaWhyFontFaces",
    "CameraStageWrapper",
    "ContainedPhotoBox",
}

# Các component bị cấm lặp quá 2 lần trong cùng 1 video
OVERUSE_LIMITED_COMPONENTS = (
    "EvidenceDocumentCard",
    "ProcessStepChain",
    "VisualBarCompare",
    "DualStageKnowledgeLayout",
)

# Nhóm component tạo chiều sâu 2.5D/3D bắt buộc có ở >= 2 Beat/video
DEPTH_25D_3D_COMPONENTS = (
    "ParallaxDepthStage",
    "SpeechPopCard25D",
    "SpeechPopCardStack25D",
    "Tilt3DFlip",
    "AnatomyCallout3D",
    "ScaleComparison3D",
    "TimelineTrack3D",
    "RealPersonSpotlight3D",
    "FlowPipeline3D",
    "ForensicHighlighter",
    "EvidenceStringBoard",
    "XRayPeelReveal",
    "RealLifeArtifact",
    "BlueprintMechanism",
)


def extract_layout_signature(code: str) -> Dict[str, Any]:
    """Trích xuất chữ ký bố cục (opening_style + component_sequence) từ mã nguồn TSX."""
    ordered_seq = sorted(
        [(code.find(k), k) for k in KNOWLEDGE_PRIMITIVES if k != "<svg" and k in code],
        key=lambda x: x[0],
    )
    comp_seq = [k for _, k in ordered_seq[:6]]
    opening_style = comp_seq[0] if comp_seq else "none"
    return {"opening_style": opening_style, "component_sequence": comp_seq}


def record_visual_layout_history(
    project_name: str,
    opening_style: str,
    component_sequence: List[str],
) -> Path:
    """
    Tự động ghi { project, opening_style, component_sequence, timestamp } vào
    engine/visual_layout_history.json sau khi qc_gate.py video hoặc render_reel.py thành công.
    """
    from datetime import datetime

    layout_hist_path = Path(__file__).resolve().parent / "visual_layout_history.json"
    entries: List[Dict[str, Any]] = []
    if layout_hist_path.exists():
        try:
            raw = json.loads(layout_hist_path.read_text(encoding="utf-8"))
            entries = raw if isinstance(raw, list) else (raw.get("entries") or [])
        except Exception:
            entries = []

    record = {
        "project": str(project_name).strip() or "unknown_project",
        "opening_style": str(opening_style or "none"),
        "component_sequence": list(component_sequence or []),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }
    # Loại bản ghi cũ cùng tên project (nếu render lại) rồi thêm bản mới nhất vào cuối
    entries = [e for e in entries if isinstance(e, dict) and e.get("project") != record["project"]]
    entries.append(record)
    entries = entries[-30:]

    layout_hist_path.write_text(
        json.dumps({"entries": entries}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return layout_hist_path


def _norm_vi_text(text: str) -> str:
    """Chuẩn hóa văn bản tiếng Việt: chữ thường, bỏ dấu câu, gộp khoảng trắng."""
    cleaned = re.sub(r"[^\w\s]", " ", (text or "").lower(), flags=re.UNICODE)
    return re.sub(r"\s+", " ", cleaned).strip()


def _load_script_and_words_norm(temp_dir: Path) -> Tuple[str, str]:
    """Đọc toàn bộ lời thoại từ temp/script_5beat.json và temp/words.json đã chuẩn hóa."""
    script_parts: List[str] = []
    script_path = temp_dir / "script_5beat.json"
    if script_path.exists():
        try:
            sdata = json.loads(script_path.read_text(encoding="utf-8"))
            if isinstance(sdata, dict):
                for k in ("full_script", "script", "voiceover", "narration", "hook", "title"):
                    val = sdata.get(k)
                    if isinstance(val, str) and val.strip():
                        script_parts.append(val.strip())
                for b in sdata.get("beats", []) or []:
                    if isinstance(b, dict):
                        for bk in ("voiceover", "narration", "text", "script", "spoken_text", "line"):
                            bv = b.get(bk)
                            if isinstance(bv, str) and bv.strip():
                                script_parts.append(bv.strip())
                    elif isinstance(b, str) and b.strip():
                        script_parts.append(b.strip())
            elif isinstance(sdata, list):
                for b in sdata:
                    if isinstance(b, dict):
                        for bk in ("voiceover", "narration", "text", "script"):
                            bv = b.get(bk)
                            if isinstance(bv, str) and bv.strip():
                                script_parts.append(bv.strip())
        except Exception:
            pass

    words_parts: List[str] = []
    words_path = temp_dir / "words.json"
    if words_path.exists():
        try:
            wdata = json.loads(words_path.read_text(encoding="utf-8"))
            wlist = wdata.get("words", wdata) if isinstance(wdata, dict) else wdata
            if isinstance(wlist, list):
                for w in wlist:
                    if isinstance(w, dict):
                        tok = str(w.get("word") or w.get("text") or "").strip()
                        if tok:
                            words_parts.append(tok)
        except Exception:
            pass

    return _norm_vi_text(" ".join(script_parts)), _norm_vi_text(" ".join(words_parts))


def get_voice_duration_sec(project_dir: Path) -> Optional[float]:
    """Đo thời lượng thực tế của temp/voiceover.wav bằng ffprobe (fallback mốc end từ cuối trong words.json)."""
    temp_dir = project_dir / "temp"
    for cand in (temp_dir / "voiceover.wav", temp_dir / "voice.wav"):
        if cand.exists():
            try:
                res = subprocess.run(
                    [
                        "ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(cand),
                    ],
                    capture_output=True, text=True, check=False,
                )
                val = float((res.stdout or "").strip())
                if val > 0.1:
                    return val
            except Exception:
                pass

    words_path = temp_dir / "words.json"
    if words_path.exists():
        try:
            wdata = json.loads(words_path.read_text(encoding="utf-8"))
            wlist = wdata.get("words", wdata) if isinstance(wdata, dict) else wdata
            if isinstance(wlist, list) and wlist:
                max_end = 0.0
                for w in wlist:
                    if not isinstance(w, dict):
                        continue
                    end_s = float(w.get("end", 0.0) or 0.0)
                    if end_s <= 0.0 and "endMs" in w:
                        end_s = float(w["endMs"]) / 1000.0
                    if end_s > max_end:
                        max_end = end_s
                if max_end > 0.1:
                    return max_end
        except Exception:
            pass
    return None


def extract_tsx_total_frames(code: str) -> Optional[int]:
    """Trích tổng số frame từ ACTIVE_DURATION_FRAMES hoặc max(from + durationInFrames) của các <Sequence>."""
    m_const = re.search(r"export\s+const\s+ACTIVE_DURATION_FRAMES\s*=\s*(\d+)", code)
    if m_const:
        return int(m_const.group(1))
    m_dur = re.search(r"durationInFrames\s*=\s*\{\s*(\d+)\s*\}", code)
    seq_ends: List[int] = []
    for sm in re.finditer(r"<Sequence\b[^>]*>", code):
        tag = sm.group(0)
        mf = re.search(r"\bfrom=\{\s*(\d+)\s*\}", tag)
        md = re.search(r"\bdurationInFrames=\{\s*(\d+)\s*\}", tag)
        if mf and md:
            seq_ends.append(int(mf.group(1)) + int(md.group(1)))
    if seq_ends:
        return max(seq_ends)
    if m_dur:
        return int(m_dur.group(1))
    return None


def check_harvest_plan(hplan_path: Path) -> Dict[str, Any]:
    """
    Kiểm định kế hoạch cào tư liệu (harvest_plan.json) — Hard Gate khớp 100% kịch bản đọc:
    - Đọc đồng thời temp/script_5beat.json và temp/words.json để đối chiếu ngược từng mục.
    - BẮT BUỘC mỗi mục có:
      * 'script_line': trích nguyên văn câu thoại có thật trong kịch bản -> sai/tự bịa báo UNMATCHED_SCRIPT_LINE.
      * 'voice_anchor_quote': cụm 2–5 từ chính xác vang lên lúc hình xuất hiện -> không tồn tại báo UNMATCHED_VOICE_ANCHOR.
      * 'must_show', 'visual_reasoning' (>= 15 ký tự), 'asset_role' thuộc {'prop_3d', 'avatar_node', 'ev_card'}.
    """
    issues: List[str] = []
    if not hplan_path.exists():
        return {
            "passed": False,
            "issues": [f"MISSING_HARVEST_PLAN: Không tìm thấy file kế hoạch cào tại {hplan_path}"],
        }

    try:
        hp = json.loads(hplan_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "passed": False,
            "issues": [f"INVALID_HARVEST_PLAN_JSON: Không đọc được JSON {hplan_path} ({exc})"],
        }

    temp_dir = hplan_path.parent
    script_norm, words_norm = _load_script_and_words_norm(temp_dir)
    combined_corpus = f"{script_norm} {words_norm}".strip()
    corpus_tokens = set(combined_corpus.split()) if combined_corpus else set()

    hp_items = hp if isinstance(hp, list) else (hp.get("assets") or hp.get("items") or hp.get("entities") or [])
    if len(hp_items) < 8:
        issues.append(
            f"LAZY_HARVEST_PLAN: harvest_plan.json mới có {len(hp_items)} mục (< 8 mục tối thiểu khớp các nhịp kịch bản)."
        )

    banned_generic_must_show = ("văn phòng chung chung", "bắt tay chung chung", "mạng xã hội chung chung", "ảnh trừu tượng")
    lazy_logged = False
    for idx, it in enumerate(hp_items):
        if not isinstance(it, dict):
            continue
        eid = str(it.get("entity_id") or f"item_{idx+1}").strip()

        # 1. Đối chiếu script_line có thật trong script_5beat.json
        script_line = str(it.get("script_line") or "").strip()
        sl_norm = _norm_vi_text(script_line)
        if not sl_norm or len(sl_norm.split()) < 3:
            issues.append(
                f"UNMATCHED_SCRIPT_LINE: Mục '{eid}' thiếu 'script_line' trích nguyên văn câu thoại từ script_5beat.json."
            )
        elif combined_corpus:
            sl_toks = [t for t in sl_norm.split() if len(t) >= 2]
            in_substr = (sl_norm in script_norm) or (sl_norm in words_norm)
            overlap_ratio = (
                sum(1 for t in sl_toks if t in corpus_tokens) / max(1, len(sl_toks))
                if sl_toks else 0.0
            )
            if not in_substr and overlap_ratio < 0.65:
                issues.append(
                    f"UNMATCHED_SCRIPT_LINE: Mục '{eid}' có script_line='{script_line[:80]}' không khớp với lời thoại thật trong script_5beat.json (overlap={overlap_ratio:.0%})."
                )

        # 2. Đối chiếu voice_anchor_quote (cụm 2–5 từ chính xác tồn tại trong script_5beat.json hoặc words.json)
        anchor_quote = str(it.get("voice_anchor_quote") or "").strip()
        aq_norm = _norm_vi_text(anchor_quote)
        aq_toks = aq_norm.split() if aq_norm else []
        if not (2 <= len(aq_toks) <= 5):
            issues.append(
                f"UNMATCHED_VOICE_ANCHOR: Mục '{eid}' thiếu hoặc sai độ dài 'voice_anchor_quote'='{anchor_quote}' "
                f"(bắt buộc cụm 2–5 từ chính xác vang lên lúc hình xuất hiện)."
            )
        elif combined_corpus:
            anchor_found = (aq_norm in script_norm) or (aq_norm in words_norm)
            if not anchor_found:
                issues.append(
                    f"UNMATCHED_VOICE_ANCHOR: Mục '{eid}' có voice_anchor_quote='{anchor_quote}' KHÔNG tồn tại trong script_5beat.json hay words.json!"
                )

        # 3. Kiểm tra visual_reasoning & asset_role
        vr = str(it.get("visual_reasoning") or "").strip()
        if len(vr) < 15:
            issues.append(
                f"MISSING_VISUAL_REASONING: Mục '{eid}' thiếu 'visual_reasoning' hợp lệ "
                f"(hiện có {len(vr)} ký tự, bắt buộc >= 15 ký tự giải thích vì sao vật thể giúp hiểu ngay câu thoại trong 1s)."
            )

        role = str(it.get("asset_role") or "").strip().lower()
        if role not in VALID_ASSET_ROLES:
            issues.append(
                f"MISSING_VISUAL_REASONING: Mục '{eid}' thiếu hoặc sai 'asset_role'='{role}' "
                f"(bắt buộc chọn đúng 1 trong 3 vai trò: prop_3d | avatar_node | ev_card)."
            )

        # 4. Kiểm tra must_show & search_queries
        must_show = str(it.get("must_show") or "").strip()
        ms_low = must_show.lower()
        if any(bg in ms_low for bg in banned_generic_must_show):
            issues.append(
                f"LAZY_HARVEST_PLAN: Mục '{eid}' có must_show='{must_show}' quá chung chung/trừu tượng. Bắt buộc mô tả đúng thực thể trong script_line!"
            )
        qs = it.get("search_queries") if isinstance(it.get("search_queries"), list) else []
        if not lazy_logged and (not must_show or len(qs) < 2):
            issues.append(
                f"LAZY_HARVEST_PLAN: Mục '{eid}' thiếu 'must_show' cụ thể hoặc 'search_queries' có < 2 từ khóa."
            )
            lazy_logged = True

    return {"passed": len(issues) == 0, "issues": issues, "count": len(hp_items)}


def check_tsx(tsx_path: Path, project_dir: Path) -> Dict[str, Any]:
    issues: List[str] = []
    warnings: List[str] = []

    if not tsx_path.exists():
        return {"passed": False, "issues": [f"Không tìm thấy file TSX: {tsx_path}"], "warnings": []}

    code = tsx_path.read_text(encoding="utf-8")

    # 1. Cấm phụ đề karaoke đáy, StickerPop, objects/*, DotMatrixZoom
    if re.search(r"<(?:KineticWordCaption|SyncCaptionBand|KaraokeCaption|SubtitleBand)\b", code):
        issues.append("BANNED_KARAOKE: Phát hiện phụ đề chạy chữ đáy màn hình. Chỉ dùng KineticHookHeader + nhãn kiến thức + số liệu.")
    if re.search(r"<StickerPop\b", code) or re.search(r'["\'\`/]objects(?:_3d)?/', code, re.IGNORECASE):
        issues.append("BANNED_PLASTIC_ICON: Phát hiện StickerPop hoặc objects/*. Bắt buộc dùng ảnh thật tách nền bria-rmbg.")
    if "DotMatrixZoom" in code:
        issues.append("BANNED_ABSTRACT_MATRIX: Cấm DotMatrixZoom trừu tượng.")
    if "CommentBubble3D" in code:
        issues.append("BANNED_OUTRO_CTA: Cấm CommentBubble3D gượng ép ở cuối video.")
    if "FloorPlatform3D" in code:
        issues.append("BANNED_FLOOR_DISC: Cấm dùng FloorPlatform3D (đĩa tròn dưới chân vật thể). Đổi sang nền sạch + bóng đổ tiếp xúc tự nhiên.")
    if "ContextBackdropLayer" in code:
        issues.append("BANNED_MESSY_PHOTO_BACKDROP: Cấm dùng ContextBackdropLayer phủ ảnh mờ toàn màn hình. Đặt ảnh thật sắc nét (opacity: 1) trong EvidenceDocumentCard / EditorialSplitTimeline trên nền lưới xanh đêm.")

    # 2. Cấm neon phát sáng nhòe
    neon_hits = [m.group(0) for m in NEON_RE.finditer(code)]
    if neon_hits:
        issues.append(f"BANNED_NEON_GLOW: Phát hiện {len(neon_hits)} hiệu ứng phát sáng màu ({neon_hits[0]}). Đổi thành bóng đen rgba(0,0,0,0.85).")

    # 3. Bắt buộc thành phần thương hiệu 2 lớp (góc trái + logo chìm chống bản quyền zIndex: 9999) & chữ chuẩn
    if "<ChannelWatermark9x16" not in code:
        issues.append("MISSING_WATERMARK: Thiếu <ChannelWatermark9x16 />.")
    wm_comp_path = Path(__file__).resolve().parent.parent / "remotion_reels" / "src" / "components" / "ChannelWatermark9x16.tsx"
    if not wm_comp_path.exists():
        issues.append(f"MISSING_STEALTH_WATERMARK: Không tìm thấy file {wm_comp_path}.")
    else:
        wm_code = wm_comp_path.read_text(encoding="utf-8")
        has_top_z = bool(re.search(r"zIndex\s*:\s*9999\b", wm_code))
        op_matches = [float(m.group(1)) for m in re.finditer(r"opacity\s*:\s*(0\.0[4-8])\b", wm_code)]
        has_stealth_opacity = bool(op_matches) or ("stealth-watermark" in wm_code)
        if not (has_top_z and has_stealth_opacity):
            issues.append(
                "MISSING_STEALTH_WATERMARK: ChannelWatermark9x16.tsx thiếu zIndex: 9999 hoặc lớp logo chìm chống bản quyền (opacity 0.04..0.08). "
                "Khôi phục đủ các lớp thương hiệu trước khi render!"
            )
    if "<HaDaWhyMistBackground" not in code:
        issues.append("MISSING_MIST_BG: Thiếu <HaDaWhyMistBackground />.")
    if "KineticHookHeader" not in code and "HaDaWhyFontFaces" not in code:
        issues.append("MISSING_HOOK_HEADER: Thiếu <KineticHookHeader /> hoặc <HaDaWhyFontFaces />.")

    # 4. Cho phép dùng nền tối sạch <HaDaWhyMistBackground /> + lưới mờ hoặc kết hợp ContextBackdropLayer để sơ đồ nổi bật

    # 5. CHỐT CHẶN ĐA DẠNG COMPONENT MINH HỌA (LOW_COMPONENT_DIVERSITY >= 5 loại, không tính khung dùng chung)
    used_primitives = [k for k in KNOWLEDGE_PRIMITIVES if k in code]
    distinct_visual_comps = [
        k for k in KNOWLEDGE_PRIMITIVES
        if k != "<svg" and k not in SHARED_FRAME_COMPONENTS and re.search(rf"<{k}\b", code)
    ]
    if len(distinct_visual_comps) < 5:
        issues.append(
            f"LOW_COMPONENT_DIVERSITY: Video mới dùng {len(distinct_visual_comps)} loại component minh họa khác nhau "
            f"({distinct_visual_comps}). Bắt buộc dùng tối thiểu 5 loại component minh họa khác nhau cho 5 Beat "
            "(tra bảng 'Kịch bản nói gì -> Gọi món đó' trong .agent/COMPONENT_CATALOG.md)."
        )

    # 5a. OVERUSED_SINGLE_COMPONENT & BANNED_OVERUSED_DOUBLE_BOX: Cấm lặp quá 2 lần cùng 1 component minh họa
    for lim_comp in OVERUSE_LIMITED_COMPONENTS:
        cnt = len(re.findall(rf"<{lim_comp}\b", code))
        if cnt > 2:
            issues.append(
                f"OVERUSED_SINGLE_COMPONENT: Component <{lim_comp} bị lặp {cnt} lần (> 2 lần tối đa/video). "
                "Hãy phối hợp đa dạng đồ nghề theo .agent/COMPONENT_CATALOG.md!"
            )
            if lim_comp == "DualStageKnowledgeLayout":
                issues.append(
                    f"BANNED_OVERUSED_DOUBLE_BOX: Phát hiện gọi <DualStageKnowledgeLayout {cnt} lần (> 2 Beat tối đa). "
                    "Cấm lặp khuôn 2 hộp PowerPoint! Hãy phối hợp với OpenHeroWatermarkStage, RadialAvatarHub, VisualCauseEffectFlow, EditorialSplitTimeline."
                )

    # 5a1. MISSING_25D_3D_DEPTH: Bắt buộc tối thiểu 2 Beat sử dụng chiều sâu 2.5D/3D rõ rệt
    seq_blocks = re.split(r"<Sequence\b", code)[1:]
    if len(seq_blocks) >= 2:
        depth_beats = sum(
            1 for blk in seq_blocks
            if any(re.search(rf"<{dc}\b", blk) for dc in DEPTH_25D_3D_COMPONENTS)
        )
    else:
        depth_beats = sum(len(re.findall(rf"<{dc}\b", code)) for dc in DEPTH_25D_3D_COMPONENTS)
    if depth_beats < 2:
        issues.append(
            f"MISSING_25D_3D_DEPTH: Chỉ có {depth_beats} Beat dùng chiều sâu 2.5D/3D (< 2 Beat bắt buộc). "
            "Bắt buộc dùng ít nhất 2 Beat có ParallaxDepthStage / SpeechPopCard25D / Tilt3DFlip / AnatomyCallout3D / ScaleComparison3D / TimelineTrack3D / RealPersonSpotlight3D / FlowPipeline3D."
        )

    # 5a2. EMPTY_EARLY_STAGE_DELAY: Chặn MetricOdometerHero xuất hiện quá muộn (startFrame > 90)
    for m_odo in re.finditer(r"<MetricOdometerHero\b[\s\S]*?/>", code):
        tag_txt = m_odo.group(0)
        m_sf = re.search(r"startFrame\s*=\s*\{\s*(\d+)\s*\}", tag_txt)
        if m_sf:
            sf_val = int(m_sf.group(1))
            if sf_val > 90:
                issues.append(
                    f"EMPTY_EARLY_STAGE_DELAY: MetricOdometerHero có startFrame={sf_val} (> 90 frames / 1.5s đầu Beat) gây trống nửa màn hình. "
                    "Bắt buộc xuất hiện trong <= 60 frames đầu Beat!"
                )

    # 5a3. OUT_OF_ORDER_STEPS: Chặn nếu triggerFrame trong ProcessStepChain không tăng dần nghiêm ngặt
    for m_psc in re.finditer(r"<ProcessStepChain\b[\s\S]*?/>", code):
        block = m_psc.group(0)
        trigs = [int(x) for x in re.findall(r"triggerFrame\s*:\s*(\d+)", block)]
        if len(trigs) >= 2 and any(trigs[i] >= trigs[i + 1] for i in range(len(trigs) - 1)):
            issues.append(
                f"OUT_OF_ORDER_STEPS: Các triggerFrame trong ProcessStepChain không tăng dần nghiêm ngặt ({trigs}). "
                "Bắt buộc step[i].triggerFrame < step[i+1].triggerFrame!"
            )

    # 5b. Nới lỏng EMPTY_BOTTOM_STAGE thành cảnh báo mềm để không ép nhét thêm hộp chữ lấp nửa dưới màn hình
    has_bottom_stage = any(
        k in code
        for k in (
            "OpenHeroWatermarkStage",
            "RadialAvatarHub",
            "VisualCauseEffectFlow",
            "EditorialSplitTimeline",
            "DualStageKnowledgeLayout",
            "HighContrastConclusionCard",
            "VisualComparisonStrip",
            "SpeechPopCard25D",
            "SpeechPopCardStack25D",
            "ParallaxDepthStage",
            "AnatomyCallout3D",
            "ScaleComparison3D",
            "TimelineTrack3D",
            "RealPersonSpotlight3D",
            "ForensicHighlighter",
            "EvidenceStringBoard",
            "XRayPeelReveal",
            "RealLifeArtifact",
            "BlueprintMechanism",
            "EvidenceDocumentCard",
            "RealSceneCameraStage",
        )
    ) or bool(re.search(r'(?:top\s*[:=]\s*\{?\s*(?:9\d\d|1[0-5]\d\d)|y\s*=\s*\{\s*(?:9\d\d|1[0-5]\d\d))', code))
    if not has_bottom_stage:
        warnings.append(
            "EMPTY_BOTTOM_STAGE: Nửa dưới màn hình (Y: 900..1540) khá thoáng — cân nhắc cân đối bố cục thị giác (KHÔNG nhồi thêm hộp chữ)."
        )

    # 5c. Chặn REPETITIVE_TEMPLATE_CLONE qua engine/visual_layout_history.json (so với 3 tập gần nhất)
    layout_hist_path = Path(__file__).resolve().parent / "visual_layout_history.json"
    sig = extract_layout_signature(code)
    comp_seq = sig["component_sequence"]
    opening_style = sig["opening_style"]
    try:
        (project_dir / "temp").mkdir(parents=True, exist_ok=True)
        (project_dir / "temp" / "layout_signature.json").write_text(
            json.dumps({"project": project_dir.name, **sig}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception:
        pass
    if layout_hist_path.exists() and comp_seq:
        try:
            hist_data = json.loads(layout_hist_path.read_text(encoding="utf-8"))
            recent = (hist_data if isinstance(hist_data, list) else hist_data.get("entries", []))[-3:]
            for rec in recent:
                if rec.get("project") != project_dir.name and rec.get("opening_style") == opening_style and rec.get("component_sequence") == comp_seq:
                    issues.append(
                        f"REPETITIVE_TEMPLATE_CLONE: Bố cục trùng y hệt tập '{rec.get('project')}' "
                        f"(opening={opening_style}, seq={comp_seq}). Hãy đổi kiểu mở đầu và thứ tự khối đồ họa!"
                    )
                    break
        except Exception:
            pass

    # 5d. Kiểm tra mật độ SFX & khớp FPS 60 trong choreography_blueprint.json
    bp_cand = project_dir / "temp" / "choreography_blueprint.json"
    if bp_cand.exists():
        try:
            bp_data = json.loads(bp_cand.read_text(encoding="utf-8"))
            bp_fps = int(bp_data.get("fps", 0) or 0)
            if bp_fps != 60:
                issues.append(f"FPS_MISMATCH: choreography_blueprint.json có fps={bp_fps}, bắt buộc fps=60 khớp 100% với .tsx.")
            all_ev = [e for e in (bp_data.get("events") or []) if isinstance(e, dict)]
            all_ev.extend([e for b in bp_data.get("beats", []) for e in (b.get("events") or []) if isinstance(e, dict)])
            if len(all_ev) < 10:
                issues.append(
                    f"INSUFFICIENT_SFX_DENSITY: choreography_blueprint.json mới có {len(all_ev)} mốc sự kiện (< 10 mốc tối thiểu; mục tiêu 10–16 điểm rơi SFX đắt giá)."
                )
            ev_kinds = {str(e.get("kind") or e.get("type") or "").lower() for e in all_ev}
            has_hook_ev = bool(ev_kinds & {"hook", "hook_text", "text"})
            has_subj_ev = bool(ev_kinds & {"subject", "knowledge", "knowledge_text"})
            has_num_ev = bool(ev_kinds & {"number", "number_knowledge", "number_money"})
            if not (has_hook_ev and has_subj_ev and has_num_ev):
                issues.append(
                    f"INSUFFICIENT_SFX_DENSITY: Thiếu nhóm sự kiện trong choreography_blueprint.json "
                    f"(hook={has_hook_ev}, subject/knowledge={has_subj_ev}, number={has_num_ev})."
                )
        except Exception:
            pass

    # 5e. Kiểm tra SHALLOW_RESEARCH, LAZY_HARVEST_PLAN & BANNED_RED_THUMBNAIL_BADGE
    temp_dir = project_dir / "temp"
    res_raw = temp_dir / "research_raw.json"
    res_dos = temp_dir / "research_dossier.json"
    if res_raw.exists():
        try:
            rd = json.loads(res_raw.read_text(encoding="utf-8"))
            n_facts = int(rd.get("hard_facts_count", len(rd.get("facts", []))))
            n_urls = int(rd.get("deep_urls_count", len({f.get("url") for f in rd.get("facts", []) if f.get("url")})))
            if n_facts < 6 or n_urls < 3:
                issues.append(
                    f"SHALLOW_RESEARCH: research_raw.json chỉ có {n_facts} dữ kiện cứng / {n_urls} URL (< 6 dữ kiện hoặc < 3 URL thật). Chạy lại fact_researcher.py với >= 4-5 truy vấn sâu!"
                )
        except Exception:
            pass
    elif res_dos.exists():
        try:
            dd = json.loads(res_dos.read_text(encoding="utf-8"))
            items_d = dd if isinstance(dd, list) else (dd.get("facts") or dd.get("items") or [])
            if len(items_d) < 6:
                issues.append(f"SHALLOW_RESEARCH: research_dossier.json chỉ có {len(items_d)} dữ kiện (< 6 dữ kiện cứng).")
        except Exception:
            pass

    hplan_path = temp_dir / "harvest_plan.json"
    if hplan_path.exists():
        hp_res = check_harvest_plan(hplan_path)
        issues.extend(hp_res.get("issues", []))

    thumb_props_path = temp_dir / "thumb_props.json"
    if thumb_props_path.exists():
        try:
            tp_txt = thumb_props_path.read_text(encoding="utf-8")
            tp_json = json.loads(tp_txt)
            if str(tp_json.get("topBadgeText", "")).strip():
                issues.append("BANNED_RED_THUMBNAIL_BADGE: Cấm truyền topBadgeText (thanh nhãn đỏ/dòng chữ thứ 3) vào thumb_props.json!")
        except Exception:
            pass
    if "topBadgeText" in code:
        issues.append("BANNED_RED_THUMBNAIL_BADGE: Phát hiện topBadgeText (thanh nhãn đỏ trên Thumbnail).")

    # 6. Kiểm tra tối thiểu 4 ảnh thật trong harvested/ & CHỐNG LẶP ẢNH TRONG CÙNG VIDEO
    raw_img_refs = re.findall(r'harvested/[^"\'\s]+\.(?:png|jpg|jpeg|webp)', code, re.IGNORECASE)
    img_refs = sorted(set(raw_img_refs))
    if len(img_refs) < 4:
        issues.append(f"INSUFFICIENT_REAL_ASSETS: Chỉ tham chiếu {len(img_refs)} ảnh thật trong harvested/. Cần ít nhất 4 ảnh thật sắc nét.")

    from collections import Counter
    ref_counts = Counter(r.lower() for r in raw_img_refs)
    dup_refs = {k: v for k, v in ref_counts.items() if v >= 2}
    if dup_refs:
        dup_str = ", ".join(f"{k} ({v}x)" for k, v in sorted(dup_refs.items()))
        issues.append(
            f"DUPLICATE_ASSET_IN_VIDEO: Cấm lặp lại cùng 1 ảnh trên nhiều cảnh trong 1 video: {dup_str}. "
            "Mỗi cảnh phải dùng ảnh riêng biệt sát với lời thoại của cảnh đó."
        )

    # 6b. Kiểm tra cấm ẩn dụ trừu tượng / rác trong tên asset (tách token theo _, -, /, ., ranh giới từ để không bắt oan upscale/landscape)
    banned_asset_keywords = {"scale", "justice", "perfume", "diet", "nutrition", "cartoon"}
    for ref in img_refs:
        ref_tokens = [tok for tok in re.split(r"[^a-z0-9]+", ref.lower()) if tok]
        for b_kw in banned_asset_keywords:
            if b_kw in ref_tokens:
                issues.append(f"BANNED_METAPHOR_ASSET: Asset '{ref}' vi phạm Luật 1 & 11 (Cấm ẩn dụ trừu tượng '{b_kw}' trong video công nghệ/đời thực). Bắt buộc dùng thực thể thực tế!")

    # 7. Kiểm tra words.json, voiceover.wav & ĐỒNG BỘ HÌNH KHỚP GIỌNG ĐỌC (Voice-Visual Sync)
    temp_dir = project_dir / "temp"
    has_words = (temp_dir / "words.json").exists() or any(project_dir.rglob("*words*.json"))
    has_voice = (temp_dir / "voiceover.wav").exists() or (temp_dir / "voice.wav").exists()
    if not has_words:
        issues.append(f"MISSING_WORDS_JSON: Không thấy words.json trong {project_dir}.")
    if not has_voice:
        issues.append(f"MISSING_VOICEOVER: Không thấy voiceover.wav / voice.wav trong {temp_dir}.")
    if has_words:
        try:
            sys.path.insert(0, str(Path(__file__).resolve().parent))
            from voice_visual_sync import check as voice_sync_check
            vs = voice_sync_check(project_dir)
            issues.extend(vs.get("issues", []))
            warnings.extend(vs.get("warnings", []))
        except Exception as exc:
            issues.append(f"VOICE_VISUAL_SYNC_ERROR: Không chạy được kiểm tra khớp hình-thoại ({exc}).")

    # 8. HARD GATE THỜI LƯỢNG TSX = ĐÚNG THỜI LƯỢNG GIỌNG ĐỌC (0 giây im lặng thừa)
    voice_sec = get_voice_duration_sec(project_dir)
    tsx_frames = extract_tsx_total_frames(code)
    if voice_sec is not None and tsx_frames is not None:
        tsx_sec = tsx_frames / 60.0
        exact_frames = math.ceil(voice_sec * 60.0)
        if tsx_sec > voice_sec + 0.35 or tsx_sec < voice_sec - 0.15:
            issues.append(
                f"DURATION_MISMATCH_SILENT_TAIL: File TSX dài {tsx_sec:.2f}s ({tsx_frames} frames) lệch so với giọng đọc "
                f"{voice_sec:.2f}s (sai số cho phép [-0.15s, +0.35s]). BẮT BUỘC đặt ACTIVE_DURATION_FRAMES = {exact_frames}!"
            )

    return {
        "passed": len(issues) == 0,
        "tsx_path": str(tsx_path),
        "used_primitives": used_primitives,
        "real_assets_count": len(img_refs),
        "voice_duration_sec": round(voice_sec, 2) if voice_sec is not None else None,
        "tsx_total_frames": tsx_frames,
        "exact_frames_required": math.ceil(voice_sec * 60.0) if voice_sec is not None else None,
        "issues": issues,
        "warnings": warnings,
    }


def make_contact_sheet(video_path: Path, out_grid: Path, dur_sec: float) -> None:
    tmp_dir = out_grid.parent / "_qc_frames_tmp"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    ts = [
        0.20, 1.50, max(2.5, dur_sec * 0.14),
        dur_sec * 0.28, dur_sec * 0.42, dur_sec * 0.56,
        dur_sec * 0.70, dur_sec * 0.84, max(0.5, dur_sec - 0.8),
    ]
    for i, t in enumerate(ts):
        subprocess.run(
            ["ffmpeg", "-y", "-ss", f"{t:.2f}", "-i", str(video_path), "-frames:v", "1", "-q:v", "3", str(tmp_dir / f"f{i}.jpg")],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    cmd = ["ffmpeg", "-y"]
    for i in range(9):
        cmd += ["-i", str(tmp_dir / f"f{i}.jpg")]
    cmd += [
        "-filter_complex",
        "xstack=inputs=9:layout=0_0|w0_0|w0+w1_0|0_h0|w0_h0|w0+w1_h0|0_h0+h3|w0_h0+h3|w0+w1_h0+h3,scale=1080:-1",
        str(out_grid),
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(tmp_dir, ignore_errors=True)


def measure_lufs(video_path: Path) -> Dict[str, float]:
    cmd = [
        "ffmpeg", "-i", str(video_path),
        "-af", "ebur128=peak=true", "-f", "null", "-",
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    stderr = res.stderr or ""
    integrated = -99.0
    true_peak = 0.0
    m_i = re.findall(r"I:\s*(-?\d+(?:\.\d+)?)\s*LUFS", stderr)
    if m_i:
        integrated = float(m_i[-1])
    m_tp = re.findall(r"Peak:\s*(-?\d+(?:\.\d+)?)\s*dBFS", stderr)
    if m_tp:
        true_peak = float(m_tp[-1])
    return {"integrated_lufs": integrated, "true_peak_db": true_peak}


def check_video(
    video_path: Path,
    grid_out: Path | None = None,
    project_dir: Path | None = None,
    tsx_path: Path | None = None,
) -> Dict[str, Any]:
    report: Dict[str, Any] = {
        "video_path": str(video_path),
        "passed": False,
        "score": 100,
        "issues": [],
        "metrics": {},
    }
    if not video_path.exists():
        report["score"] = 0
        report["issues"].append("Video không tồn tại!")
        return report

    # 1. ffprobe check
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height,r_frame_rate,duration,codec_type", "-of", "json", str(video_path)],
        capture_output=True, text=True,
    )
    if probe.returncode != 0:
        report["score"] = 0
        report["issues"].append("ffprobe đọc file thất bại!")
        return report

    meta = json.loads(probe.stdout)
    v_stream = next((s for s in meta.get("streams", []) if s.get("codec_type") == "video"), None)
    if not v_stream:
        report["score"] = 0
        report["issues"].append("Không có video stream!")
        return report

    w, h = int(v_stream.get("width", 0)), int(v_stream.get("height", 0))
    report["metrics"]["resolution"] = f"{w}x{h}"
    if w != 1080 or h != 1920:
        report["score"] -= 30
        report["issues"].append(f"Sai tỷ lệ 9:16: {w}x{h} (yêu cầu 1080x1920).")

    # 2. OpenCV visual density & anti-empty-void check
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS) or 60.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    dur_sec = total_frames / fps if fps > 0 else 0.0
    report["metrics"]["fps"] = round(fps, 2)
    report["metrics"]["duration_sec"] = round(dur_sec, 2)

    sample_times = [dur_sec * p for p in (0.08, 0.18, 0.30, 0.42, 0.54, 0.66, 0.78, 0.88, 0.95)]
    luma_list: List[float] = []
    std_luma_list: List[float] = []
    dark_ratio_list: List[float] = []
    black_frames = 0
    prev_small = None
    static_pairs = 0

    for t in sample_times:
        cap.set(cv2.CAP_PROP_POS_FRAMES, min(total_frames - 1, max(0, int(t * fps))))
        ret, frame = cap.read()
        if not ret:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean_luma = float(np.mean(gray))
        std_luma = float(np.std(gray))
        dark_ratio = float(np.mean(gray < 18))
        luma_list.append(mean_luma)
        std_luma_list.append(std_luma)
        dark_ratio_list.append(dark_ratio)
        if mean_luma < 5.0 and std_luma < 4.0:
            black_frames += 1
        small = cv2.resize(gray, (180, 320))
        if prev_small is not None:
            diff = float(np.mean(np.abs(small.astype(np.float32) - prev_small.astype(np.float32))))
            if diff < 1.8:
                static_pairs += 1
        prev_small = small
    cap.release()

    avg_luma = round(float(np.mean(luma_list)) if luma_list else 0.0, 2)
    avg_std_luma = round(float(np.mean(std_luma_list)) if std_luma_list else 0.0, 2)
    avg_dark_ratio = round(float(np.mean(dark_ratio_list)) * 100.0 if dark_ratio_list else 100.0, 1)
    report["metrics"]["avg_luma"] = avg_luma
    report["metrics"]["avg_std_luma"] = avg_std_luma
    report["metrics"]["avg_black_void_pct"] = avg_dark_ratio
    report["metrics"]["black_frames"] = black_frames
    report["metrics"]["static_pairs"] = static_pairs

    if black_frames > 0:
        report["score"] -= 40
        report["issues"].append(f"BLACK_FRAME_DETECTED: Có {black_frames} khung hình đen kịt hỏng render.")
    if avg_luma < 6.0 and avg_std_luma < 4.0:
        report["score"] -= 35
        report["issues"].append(
            f"EMPTY_DARK_VOID_SCREEN: Màn hình đen kịt hỏng render (avg_luma={avg_luma} < 6.0, std_luma={avg_std_luma} < 4.0)."
        )
    if static_pairs >= 3:
        report["score"] -= 25
        report["issues"].append(f"STATIC_SLIDESHOW_DETECTED: {static_pairs} cặp khung hình hầu như đứng im không biến chuyển.")

    # 3. Audio EBU R128 check
    audio_stats = measure_lufs(video_path)
    report["metrics"].update(audio_stats)
    lufs = audio_stats["integrated_lufs"]
    tp = audio_stats["true_peak_db"]
    if not (-15.2 <= lufs <= -12.8):
        report["score"] -= 25
        report["issues"].append(f"LOUDNESS_OUT_OF_SPEC: {lufs:.1f} LUFS (yêu cầu -14.0 ± 1.0 LUFS).")
    if tp > -0.3:
        report["score"] -= 15
        report["issues"].append(f"TRUE_PEAK_CLIPPING: {tp:.1f} dBFS (yêu cầu <= -0.5 dBTP).")

    # 3b. HARD GATE CHỐNG ĐUÔI IM LẶNG THỪA (SILENT_TAIL_OVERFLOW > 0.40s so với voiceover.wav)
    if project_dir is not None:
        voice_sec = get_voice_duration_sec(project_dir)
        if voice_sec is not None:
            report["metrics"]["voice_duration_sec"] = round(voice_sec, 2)
            overflow = round(dur_sec - voice_sec, 2)
            report["metrics"]["tail_overflow_sec"] = overflow
            if dur_sec > voice_sec + 0.40:
                report["score"] -= 40
                report["issues"].append(
                    f"SILENT_TAIL_OVERFLOW: Video thành phẩm dài {dur_sec:.2f}s, vượt quá giọng đọc {voice_sec:.2f}s "
                    f"là +{overflow:.2f}s (> 0.40s im lặng thừa). CẤM kéo dài video sau khi giọng đọc kết thúc!"
                )

    if grid_out:
        make_contact_sheet(video_path, grid_out, dur_sec)
        report["grid_path"] = str(grid_out)

    # Kiểm tra cuối: xác nhận remotion_reels/public/harvested/ và remotion_reels/out/ trống 0 bytes sau khi render
    brain_clean = check_brain_clean()
    report["brain_clean"] = brain_clean
    if not brain_clean["passed"]:
        report["issues"].extend(brain_clean["issues"])
        report["score"] -= 15

    report["score"] = max(0, report["score"])
    report["passed"] = report["score"] >= 85 and len(report["issues"]) == 0

    # Tự động ghi vào engine/visual_layout_history.json khi QC video đạt chuẩn
    if report["passed"]:
        try:
            proj_name = project_dir.name if project_dir else video_path.stem
            sig_data: Dict[str, Any] | None = None
            if tsx_path and tsx_path.exists():
                sig_data = extract_layout_signature(tsx_path.read_text(encoding="utf-8"))
            else:
                cand_sigs = []
                if project_dir:
                    cand_sigs.append(project_dir / "temp" / "layout_signature.json")
                if grid_out:
                    cand_sigs.append(grid_out.parent / "layout_signature.json")
                for sp in cand_sigs:
                    if sp.exists():
                        raw_sig = json.loads(sp.read_text(encoding="utf-8"))
                        proj_name = str(raw_sig.get("project") or proj_name)
                        sig_data = {
                            "opening_style": raw_sig.get("opening_style", "none"),
                            "component_sequence": raw_sig.get("component_sequence", []),
                        }
                        break
            if sig_data:
                record_visual_layout_history(
                    project_name=proj_name,
                    opening_style=sig_data["opening_style"],
                    component_sequence=sig_data["component_sequence"],
                )
                report["layout_history_recorded"] = True
        except Exception as exc:
            report["layout_history_error"] = str(exc)

    return report


def check_brain_clean() -> Dict[str, Any]:
    """Xác nhận Đầu Não sạch 0 bytes rác: remotion_reels/public/harvested/ và remotion_reels/out/ phải trống hoàn toàn."""
    remotion_root = Path(__file__).resolve().parent.parent / "remotion_reels"
    harvested_dir = remotion_root / "public" / "harvested"
    out_dir = remotion_root / "out"

    def _dir_stats(d: Path) -> Tuple[int, int]:
        if not d.exists():
            return 0, 0
        files = [p for p in d.rglob("*") if p.is_file()]
        return len(files), sum(p.stat().st_size for p in files)

    h_cnt, h_bytes = _dir_stats(harvested_dir)
    o_cnt, o_bytes = _dir_stats(out_dir)
    issues: List[str] = []
    if h_cnt > 0 or h_bytes > 0:
        issues.append(
            f"DIRTY_MASTERBRAIN_MEDIA: remotion_reels/public/harvested/ vẫn còn {h_cnt} file ({h_bytes} bytes). "
            "Đầu Não bắt buộc trống 0 bytes sau khi render!"
        )
    if o_cnt > 0 or o_bytes > 0:
        issues.append(
            f"DIRTY_MASTERBRAIN_OUT: remotion_reels/out/ vẫn còn {o_cnt} file ({o_bytes} bytes). "
            "Đầu Não bắt buộc trống 0 bytes sau khi render!"
        )
    return {
        "passed": len(issues) == 0,
        "harvested_files": h_cnt,
        "harvested_bytes": h_bytes,
        "out_files": o_cnt,
        "out_bytes": o_bytes,
        "issues": issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Unified QC Gate for FB Reels 9:16")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_plan = sub.add_parser("plan", help="Kiểm tra tư duy đạo diễn trong temp/harvest_plan.json trước khi cào")
    p_plan.add_argument("--project", default="")
    p_plan.add_argument("--manifest", default="")

    p_tsx = sub.add_parser("tsx", help="Kiểm tra file Composition .tsx trước khi render (mặc định: <project>/temp/EpisodeComp.tsx)")
    p_tsx.add_argument("--tsx", default="", help="Đường dẫn file .tsx (mặc định: <project>/temp/EpisodeComp.tsx)")
    p_tsx.add_argument("--project", required=True)

    p_vid = sub.add_parser("video", help="Kiểm tra video MP4 thành phẩm sau khi render")
    p_vid.add_argument("--video", required=True)
    p_vid.add_argument("--grid", default="")
    p_vid.add_argument("--project", default="")
    p_vid.add_argument("--tsx", default="")

    sub.add_parser("clean", help="Kiểm tra Đầu Não 0 bytes rác ở public/harvested/ và out/")

    args = ap.parse_args()
    if args.cmd == "plan":
        manifest_p = Path(args.manifest) if args.manifest else (Path(args.project) / "temp" / "harvest_plan.json")
        res = check_harvest_plan(manifest_p)
    elif args.cmd == "tsx":
        tsx_p = Path(args.tsx) if args.tsx else (Path(args.project) / "temp" / "EpisodeComp.tsx")
        res = check_tsx(tsx_p, Path(args.project))
    elif args.cmd == "clean":
        res = check_brain_clean()
    else:
        tsx_p = Path(args.tsx) if args.tsx else (Path(args.project) / "temp" / "EpisodeComp.tsx" if args.project else None)
        res = check_video(
            Path(args.video),
            Path(args.grid) if args.grid else None,
            project_dir=Path(args.project) if args.project else None,
            tsx_path=tsx_p if (tsx_p and tsx_p.exists()) else None,
        )

    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("passed") else 1


if __name__ == "__main__":
    sys.exit(main())
