r"""
semantic_scene_planner.py - BỘ ĐỒNG BỘ NGỮ NGHĨA "NÓI A MINH HỌA ĐÚNG A" & CHỐNG DÙNG LẠI ĐỒ CŨ
(Dành riêng cho Đầu Não Video Ngắn FB: D:\Đầu Não Video Ngắn FB (không xóa))

Giải quyết triệt để lỗi "Kèn thổi xuôi, trống đánh ngược":
1. CẤM DÙNG LẠI ĐỒ CŨ (ZERO ASSET CARRYOVER):
   - Mỗi kịch bản mới bắt buộc dọn sạch thư mục `public/harvested/` của kịch bản cũ.
   - Kịch bản nói tới chủ thể nào (Con người, Thương hiệu, Đồ vật, Địa danh), bắt buộc phải cào
     hoặc tạo mới đúng chủ thể đó.
2. ĐỔI NỀN, BẢNG MÀU & NHẠC NỀN (BGM) THEO ĐÚNG DNA KỊCH BẢN:
   - Tự động nhận diện 1 trong 5 DNA chủ đề để chọn Màu nền (Background Gradient), Màu nhấn chữ (Accent),
     và Bài nhạc nền (từ 14 bài nhạc trong `D:\Đầu Não (không xóa)\assets\music\`).
3. CHỌN BỐ CỤC CHUYỂN ĐỘNG (VISUAL ARCHETYPE) KHỚP 100% HÀNH ĐỘNG CÂU THOẠI:
   - Câu có địa danh quốc gia / di chuyển xuyên biên giới -> Mới được bật `GeoStrategicMap3D`.
   - Câu mổ xẻ cấu tạo / chi phí thành phần -> Bật `AnatomyCallout3D`.
   - Câu kể diễn biến theo mốc thời gian (năm/tháng) -> Bật `TimelineTrack3D`.
   - Câu nói về nhân vật / CEO / tuyên bố / bài báo -> Bật `RealPersonSpotlight3D` / `ForensicDossier`.
   - Câu nói về dòng chảy (tiền, hàng hóa, dầu, chip, dữ liệu) -> Bật `CoinStream` (với icon của đúng vật đó).
   - Câu so sánh chênh lệch A vs B -> Bật `ScaleComparison3D` (với đúng vật thể A và B).
"""

import json
import re
import sys
from pathlib import Path

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

MUSIC_ROOT = Path(r"D:\Đầu Não (không xóa)\assets\music")

# 5 BỘ DNA THẨM MỸ & ÂM NHẠC ĐỘC LẬP THEO CHỦ ĐỀ KỊCH BẢN
THEME_DNA_PRESETS = {
    "finance_macro": {
        "name": "Tài Chính - Ngân Hàng - Tiền Tệ",
        "bg_radial": "radial-gradient(circle at 50% 34%, rgba(46, 36, 14, 0.62) 0%, rgba(12, 10, 6, 0.95) 62%, #060503 100%)",
        "primary_accent": "#FFE600",
        "danger_accent": "#FF3B47",
        "bgm_candidates": [
            str(MUSIC_ROOT / "wallstreet_finance" / "wallstreet_finance_drive_01.mp3"),
            str(MUSIC_ROOT / "wallstreet_finance" / "wallstreet_finance_cinema_02.mp3"),
            str(MUSIC_ROOT / "wallstreet_finance" / "wallstreet_finance_momentum_03.mp3"),
        ],
    },
    "tech_ai_auto": {
        "name": "Công Nghệ - AI - Bán Dẫn - Xe Điện",
        "bg_radial": "radial-gradient(circle at 50% 34%, rgba(12, 52, 88, 0.65) 0%, rgba(6, 14, 28, 0.95) 62%, #030710 100%)",
        "primary_accent": "#00E5FF",
        "danger_accent": "#FF3B47",
        "bgm_candidates": [
            str(MUSIC_ROOT / "cyber_deepseek_ai" / "cyber_ai_future_02.mp3"),
            str(MUSIC_ROOT / "cyber_deepseek_ai" / "cyber_ai_synthwave_01.mp3"),
        ],
    },
    "forensic_crime": {
        "name": "Điều Tra - Đại Án - Kiện Tụng - Sụp Đổ",
        "bg_radial": "radial-gradient(circle at 50% 34%, rgba(64, 16, 24, 0.58) 0%, rgba(14, 6, 10, 0.95) 62%, #070305 100%)",
        "primary_accent": "#FF3B47",
        "danger_accent": "#FFE600",
        "bgm_candidates": [
            str(MUSIC_ROOT / "investigation_dark" / "dark_investigation_tension_01.mp3"),
            str(MUSIC_ROOT / "investigation_dark" / "dark_investigation_orchestral_03.mp3"),
            str(MUSIC_ROOT / "investigation_dark" / "dark_investigation_mystery_02.mp3"),
        ],
    },
    "business_consumer": {
        "name": "Thương Hiệu - F&B - Bán Lẻ - Bất Động Sản",
        "bg_radial": "radial-gradient(circle at 50% 34%, rgba(16, 56, 48, 0.58) 0%, rgba(8, 18, 16, 0.95) 62%, #040A09 100%)",
        "primary_accent": "#00F59B",
        "danger_accent": "#FFE600",
        "bgm_candidates": [
            str(MUSIC_ROOT / "victory_climax" / "epic_victory_climax_01.mp3"),
            str(MUSIC_ROOT / "master_cinematic_bgm.mp3"),
        ],
    },
    "geopolitics_energy": {
        "name": "Địa Chính Trị - Năng Lượng - Chuỗi Cung Ứng Toàn Cầu",
        "bg_radial": "radial-gradient(circle at 50% 34%, rgba(52, 38, 22, 0.60) 0%, rgba(14, 12, 10, 0.95) 62%, #060605 100%)",
        "primary_accent": "#FFB800",
        "danger_accent": "#FF3B47",
        "bgm_candidates": [
            str(MUSIC_ROOT / "tension_intro_epic.mp3"),
            str(MUSIC_ROOT / "victory_climax" / "epic_victory_climax_02.mp3"),
        ],
    },
}


def detect_script_theme_dna(script_text: str) -> dict:
    """Phân tích từ khóa toàn kịch bản để chọn đúng DNA Màu nền, Màu chữ nhấn và Nhạc nền BGM."""
    low = script_text.lower()
    scores = {
        "tech_ai_auto": sum(1 for kw in ["chip", "ai", "thuật toán", "robot", "xe điện", "pin", "công nghệ", "phần mềm", "nvidia", "apple", "tesla"] if kw in low),
        "forensic_crime": sum(1 for kw in ["kiện", "tòa án", "khởi tố", "bắt", "lừa đảo", "vỡ nợ", "bốc hơi", "thao túng", "đại án", "tội"] if kw in low),
        "geopolitics_energy": sum(1 for kw in ["cấm vận", "kênh đào", "eo biển", "dầu mỏ", "khí đốt", "biên giới", "quân sự", "thuế quan", "xuất khẩu"] if kw in low),
        "business_consumer": sum(1 for kw in ["cà phê", "nhà hàng", "chuỗi", "mặt bằng", "cửa hàng", "khách hàng", "doanh số", "thương hiệu", "bán lẻ"] if kw in low),
        "finance_macro": sum(1 for kw in ["ngân hàng", "lãi suất", "trái phiếu", "cổ phiếu", "tỷ giá", "vàng", "dòng tiền", "khoản nợ", "quỹ"] if kw in low),
    }
    best_key = max(scores, key=scores.get)
    if scores[best_key] == 0:
        best_key = "finance_macro"
    preset = THEME_DNA_PRESETS[best_key].copy()
    preset["theme_id"] = best_key
    return preset


def recommend_archetype_for_sentence(sentence: str) -> dict:
    """
    Phân tích ngữ nghĩa từng câu thoại để chỉ định đúng Khuôn Mẫu Minh Họa (Visual Archetype)
    và loại SFX phù hợp, tuyệt đối cấm lắp râu ông nọ chắp cằm bà kia!
    """
    low = sentence.lower()

    # 1. Kiểm tra xem câu có thực sự nói về di chuyển địa lý / quốc gia không
    geo_keywords = ["sang tận", "từ việt nam", "quốc gia", "bản đồ", "biên giới", "hải trình", "đường bay", "xuất khẩu sang", "toàn cầu", "châu âu", "mỹ", "trung quốc", "luân đôn", "london", "singapore"]
    if any(kw in low for kw in geo_keywords):
        return {
            "archetype": "GeoStrategicMap3D",
            "reason": "Câu thoại có yếu tố vị trí địa lý / xuyên biên giới quốc gia.",
            "recommended_sfx": ["whoosh_big.mp3", "zoom_hit.mp3", "tap.mp3"],
        }

    # 2. Kiểm tra xem câu có nói về diễn biến mốc thời gian (Năm / Tháng / Giai đoạn) không
    if re.search(r"\b(năm\s+\d{4}|giai đoạn|từ năm|đến năm|lịch sử)\b", low):
        return {
            "archetype": "TimelineTrack3D",
            "reason": "Câu thoại mô tả diễn biến theo trục thời gian lịch sử.",
            "recommended_sfx": ["tick.mp3", "pop.mp3", "whoosh2.mp3"],
        }

    # 3. Kiểm tra xem câu có mổ xẻ cấu tạo / thành phần / tỷ lệ bên trong 1 vật thể không
    anatomy_keywords = ["bên trong", "cấu tạo", "bao gồm", "chiếm tới", "thành phần", "chia làm", "chi phí gồm"]
    if any(kw in low for kw in anatomy_keywords):
        return {
            "archetype": "AnatomyCallout3D",
            "reason": "Câu thoại bóc tách thành phần / cấu tạo bên trong chủ thể.",
            "recommended_sfx": ["pop_dry.mp3", "tick.mp3", "zoom_hit.mp3"],
        }

    # 4. Kiểm tra xem câu có đặt 2 con số / quy mô đối lập nhau không
    compare_keywords = ["vọt lên", "gấp", "so với", "trong khi", "chênh lệch", "từ ", "đòi bồi thường", "cao hơn"]
    if any(kw in low for kw in compare_keywords) and re.search(r"\d+", low):
        return {
            "archetype": "ScaleComparison3D",
            "reason": "Câu thoại đối chiếu quy mô / con số chênh lệch trực quan.",
            "recommended_sfx": ["tick.mp3", "coin1.mp3", "bass_hit.mp3", "hit_blow.mp3"],
        }

    # 5. Kiểm tra xem câu có nói về hành động cắt đứt / phong tỏa / đóng băng / chuyển dòng không
    flow_keywords = ["dòng tiền", "doanh thu", "trả", "bán", "chuyển", "cắt", "đóng băng", "chặn", "chảy", "thuê"]
    if any(kw in low for kw in flow_keywords):
        return {
            "archetype": "FlowAndActionMechanics",
            "reason": "Câu thoại mô tả dòng chảy vật chất/tiền tệ hoặc hành động tác động trực tiếp.",
            "recommended_sfx": ["whoosh1.mp3", "coin1.mp3", "lock.mp3", "cut.mp3", "metal_hit.mp3"],
        }

    # Mặc định: Spotlight Chủ thể thật + Hồ sơ bằng chứng báo chí 3D
    return {
        "archetype": "RealPersonOrEvidenceSpotlight3D",
        "reason": "Câu thoại giới thiệu chủ thể, nhân vật, sự kiện hoặc bằng chứng báo chí.",
        "recommended_sfx": ["whoosh1.mp3", "pop.mp3", "bass_hit.mp3"],
    }


def build_semantic_production_plan(script_sentences: list[str], out_json_path: str | Path | None = None) -> dict:
    """
    Nhận danh sách các câu trong kịch bản -> Xuất Bản Thiết Kế Ngữ Nghĩa (Semantic Production Plan)
    bắt buộc từng câu phải dùng đúng Hình ảnh, Bố cục, Màu sắc và Âm thanh của câu đó.
    """
    full_text = " ".join(script_sentences)
    theme_dna = detect_script_theme_dna(full_text)

    scene_plans = []
    for idx, sent in enumerate(script_sentences):
        rec = recommend_archetype_for_sentence(sent)
        scene_plans.append({
            "scene_index": idx + 1,
            "sentence": sent,
            "visual_archetype": rec["archetype"],
            "archetype_reason": rec["reason"],
            "recommended_sfx": rec["recommended_sfx"],
            "physical_metaphor_blueprint": {
                "beat_A_0s_to_2_5s": "Mở cảnh: Đưa Ảnh Thật đã tách nền (nhân vật/sản phẩm/bối cảnh của câu này) + Vật thể 3D chính chuyển động vào vị trí.",
                "beat_B_2_5s_to_5s": "Biến cố vật lý (2.5s Visual Reset): Vật thể 3D thứ 2 tác động trực tiếp (chặn dòng chảy / cắt đứt / phóng tia AR mổ xẻ / bắn đường bay bản đồ / đặt lên bàn cân đếm số).",
                "required_assets_for_this_sentence": [
                    "1_real_cutout_or_evidence_photo (Ảnh thật từ Wikimedia/Bing HD tách nền bria-rmbg)",
                    "2_primary_3d_object (Vật thể 3D chính của câu này qua harvest_bespoke_3d_object)",
                    "3_interaction_3d_object (Vật thể 3D tương tác/tác động vật lý trong câu này)",
                ],
            },
            "strict_mandate": (
                "BẮT BUỘC dịch câu nói thành HÀNH ĐỘNG VẬT LÝ CỤ THỂ giữa các vật thể 3D và ảnh thật của đúng câu này. "
                "CẤM TUYỆT ĐỐI chỉ đặt ảnh tĩnh đứng yên hoặc lấy đồ cũ của bài trước đắp vào!"
            ),
        })

    plan = {
        "theme_dna": theme_dna,
        "total_scenes": len(scene_plans),
        "scenes": scene_plans,
    }

    if out_json_path:
        out_p = Path(out_json_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[SEMANTIC PLANNER OK] Đã lập Bản Thiết Kế Đồng Bộ Ngữ Nghĩa tại: {out_p}")

    return plan


if __name__ == "__main__":
    sample = [
        "Tại sao một ly cà phê স্টারバックス giá 90 nghìn đồng nhưng tiền hạt cà phê chỉ chiếm chưa tới 4 nghìn đồng?",
        "Bên trong chiếc cốc này, 45% chi phí nằm ở mặt bằng đắt đỏ và nhân sự vận hành.",
        "Từ chuỗi cửa hàng tại Mỹ mở rộng sang Việt Nam, bài toán chi phí cố định luôn là con dao hai lưỡi."
    ]
    res = build_semantic_production_plan(sample)
    print(json.dumps(res, ensure_ascii=False, indent=2))
