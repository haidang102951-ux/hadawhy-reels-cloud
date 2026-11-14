# -*- coding: utf-8 -*-
r"""
=====================================================================================
CHƯƠNG TRÌNH LỌC AN TOÀN BẢN QUYỀN, NỘI DUNG LẶP LẠI & CHÍNH SÁCH NỀN TẢNG
(PLATFORM COMPLIANCE SENTINEL - 8 POLICY GROUPS & 7-LAYER ANTI-COPYRIGHT SHIELD)
Trung tâm Đầu Não: D:\Đầu Não (không xóa)\engine\policy_and_copyright_filter.py
Chuẩn mực: YouTube YPP Advertiser-Friendly, TikTok Creator Rewards, Meta Rights Manager,
           Mục 107 Đạo luật Bản quyền Hoa Kỳ (17 U.S. Code § 107 - Fair Use)
=====================================================================================
"""

import os
import sys
import re
import json
import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

POLICY_DB_PATH = r"D:\Đầu Não (không xóa)\engine\policy_database.json"

# BẢNG 8 NHÓM CHÍNH SÁCH TỪ CẤM NỀN TẢNG MẶC ĐỊNH (BUILT-IN FALLBACK)
DEFAULT_FORBIDDEN_POLICY_GROUPS = {
    "GROUP_1_VIOLENCE_AND_GORE": {
        "name": "Nhóm 1: Bạo lực, Đẫm máu & Chết chóc",
        "risk_level": "CRITICAL_YELLOW_DOLLAR",
        "triggers": [
            "giết", "đồ sát", "chém chết", "thanh trừng đẫm máu", "bắn hạ", 
            "tai nạn thảm khốc", "chết thảm", "xác chết", "chặt xác", "tùng xẻo",
            "máu me bê bết", "thảm sát", "chết chóc", "hành quyết"
        ],
        "neutral_replacements": {
            "giết": "tước đi sinh mạng / khiến đối tượng thiệt mạng",
            "đồ sát": "hành vi bạo lực quy mô lớn",
            "chém chết": "tấn công gây hậu quả tử vong",
            "thanh trừng đẫm máu": "chiến dịch trấn áp quyết liệt / thanh lọc nội bộ",
            "bắn hạ": "tiêu diệt mục tiêu trong tác chiến / can thiệp vũ lực",
            "tai nạn thảm khốc": "sự cố va chạm nghiêm trọng",
            "chết thảm": "tai nạn thương tâm / qua đời đột ngột",
            "thảm sát": "biến cố xung đột nghiêm trọng"
        }
    },
    "GROUP_2_SELF_HARM_AND_SUICIDE": {
        "name": "Nhóm 2: Tự hại, Tự sát & Khủng hoảng tâm lý cực đoan",
        "risk_level": "STRICT_BAN_OR_TAKEDOWN",
        "triggers": [
            "tự sát", "tự tử", "nhảy lầu", "rạch tay", "uống thuốc độc", 
            "chán sống", "kết liễu cuộc đời", "thắt cổ"
        ],
        "neutral_replacements": {
            "tự sát": "hành vi tự tổn thương / sự cố tiêu cực cá nhân",
            "tự tử": "qua đời do khủng hoảng tâm lý",
            "nhảy lầu": "ngã từ trên cao trong tình trạng bất ổn",
            "kết liễu cuộc đời": "chấm dứt sự sống đột ngột"
        }
    },
    "GROUP_3_ADULT_AND_SEXUAL_CONTENT": {
        "name": "Nhóm 3: Nội dung người lớn, Gợi dục & Đồi trụy",
        "risk_level": "STRICT_AGE_RESTRICTED_OR_BAN",
        "triggers": [
            "khiêu dâm", "tấn công tình dục", "hiếp dâm", "lộ clip nóng", 
            "gái gọi", "bán dâm", "ấu dâm", "quấy rối tình dục", "dâm ô"
        ],
        "neutral_replacements": {
            "khiêu dâm": "nội dung nhạy cảm / vi phạm thuần phong mỹ tục",
            "tấn công tình dục": "hành vi xâm hại thân thể trái pháp luật",
            "hiếp dâm": "tội phạm xâm hại tình dục nghiêm trọng",
            "lộ clip nóng": "phát tán tư liệu đời tư cá nhân trái phép"
        }
    },
    "GROUP_4_HATE_SPEECH_AND_HARASSMENT": {
        "name": "Nhóm 4: Ngôn từ thù ghét, Miệt thị, Xúc phạm danh dự & Phân biệt đối xử",
        "risk_level": "CRITICAL_YELLOW_DOLLAR",
        "triggers": [
            "kỳ thị chủng tộc", "kỳ thị tôn giáo", "bọn mọi rợ", "lũ ngu xuẩn", 
            "chửi bới thóa mạ", "đồ rác rưởi", "bọn cặn bã", "miệt thị ngoại hình",
            "xúc phạm danh dự", "lũ vô học"
        ],
        "neutral_replacements": {
            "kỳ thị chủng tộc": "mâu thuẫn sắc tộc / bất đồng văn hóa",
            "kỳ thị tôn giáo": "xung đột tín ngưỡng",
            "bọn mọi rợ": "nhóm đối tượng có hành vi cực đoan",
            "lũ ngu xuẩn": "thiếu hiểu biết chuyên sâu / nhận định sai lệch"
        }
    },
    "GROUP_5_FINANCIAL_FRAUD_AND_GAMBLING": {
        "name": "Nhóm 5: Lừa đảo tài chính, Đa cấp biến tướng, Tiền ảo cam kết & Cờ bạc",
        "risk_level": "CRITICAL_YELLOW_DOLLAR_OR_SCAM_FLAG",
        "triggers": [
            "làm giàu nhanh", "bao lỗ 100%", "kèo đổi đời", "tiền ảo uy tín nhất", 
            "đầu tư chắc thắng", "hoa hồng siêu khủng", "đa cấp ngầm", "cờ bạc online", 
            "đánh bạc", "casino trực tuyến", "nhà cái uy tín", "nổ hũ", "tài xỉu", 
            "game bài đổi thưởng", "xóc đĩa qua mạng"
        ],
        "neutral_replacements": {
            "làm giàu nhanh": "mô hình tăng trưởng tài sản thiếu cơ sở",
            "bao lỗ 100%": "cam kết phi thực tế trong đầu tư mạo hiểm",
            "kèo đổi đời": "cơ hội đầu cơ chứa đựng rủi ro cực lớn",
            "đa cấp ngầm": "mô hình ponzi huy động vốn trái quy định",
            "cờ bạc online": "hoạt động cá cược không được cấp phép"
        }
    },
    "GROUP_6_CONTROLLED_SUBSTANCES_AND_WEAPONS": {
        "name": "Nhóm 6: Ma túy, Chất cấm, Thuốc kích thích & Vũ khí sát thương",
        "risk_level": "STRICT_LEGAL_VIOLATION",
        "triggers": [
            "ma túy đá", "buôn ma túy", "hít ke", "chất gây nghiện", "thuốc lắc", 
            "cần sa trái phép", "buôn bán vũ khí", "súng quân dụng", "bom tự chế", 
            "chế tạo chất nổ", "vũ khí sát thương"
        ],
        "neutral_replacements": {
            "ma túy đá": "chất kích thích thuộc danh mục cấm",
            "buôn ma túy": "đường dây vận chuyển tiền chất gây nghiện",
            "buôn bán vũ khí": "giao dịch khí tài quân dụng trái phép",
            "bom tự chế": "thiết bị nổ tự tạo có tính sát thương"
        }
    },
    "GROUP_7_TERRORISM_AND_HARMFUL_MISINFO": {
        "name": "Nhóm 7: Khủng bố, Cực đoan chính trị & Tin giả nguy hại",
        "risk_level": "STRICT_BAN_OR_TAKEDOWN",
        "triggers": [
            "khủng bố", "lật đổ chính quyền", "kích động bạo loạn", "biểu tình đập phá", 
            "tuyên truyền chống phá", "tin mật rò rỉ giả mạo", "thao túng bầu cử phi pháp"
        ],
        "neutral_replacements": {
            "khủng bố": "phần tử cực đoan gây bất ổn an ninh",
            "lật đổ chính quyền": "biến cố chính trị gây xáo trộn thể chế",
            "kích động bạo loạn": "tụ tập đông người gây mất trật tự công cộng",
            "tin mật rò rỉ giả mạo": "luồng thông tin chưa được kiểm chứng độc lập"
        }
    },
    "GROUP_8_UNVERIFIED_ACCUSATIONS_AND_COPYRIGHT": {
        "name": "Nhóm 8: Cáo buộc pháp lý phiến diện/Vô căn cứ & Vi phạm bản quyền lậu",
        "risk_level": "LEGAL_DEFAMATION_AND_CONTENT_ID",
        "triggers": [
            "tham nhũng chắc chắn", "lừa đảo chiếm đoạt (chưa tuyên án)", "tên tội phạm (khi chưa xét xử)",
            "full movie", "phim lậu", "link tải crack", "leak phim", "bản quyền thuộc về", "reup không xin phép"
        ],
        "neutral_replacements": {
            "tham nhũng chắc chắn": "đang đối diện với các cáo buộc liên quan đến tài chính",
            "lừa đảo chiếm đoạt (chưa tuyên án)": "đang bị điều tra về hành vi nghi vấn gian lận",
            "tên tội phạm (khi chưa xét xử)": "nghi can / bị can theo kết luận của cơ quan điều tra",
            "bản quyền thuộc về": "trích xuất nguồn tư liệu báo chí nghiên cứu độc lập"
        }
    }
}

class PlatformSafetyShield:
    def __init__(self, policy_db_path: str = POLICY_DB_PATH):
        self.policy_db_path = policy_db_path
        self.policy_data = self._load_policy_db()
        self.forbidden_groups = self.policy_data.get("forbidden_policy_lexicon_8_groups", DEFAULT_FORBIDDEN_POLICY_GROUPS)
        
        self.report = {
            "policy_check": {
                "status": "PASS",
                "risk_score": 100,
                "warnings": [],
                "flagged_items": [],
                "sanitized_suggestions": {}
            },
            "anti_copyright_check": {
                "status": "PASS",
                "score": 100,
                "violations": [],
                "layer_audits": {}
            },
            "anti_reused_content_check": {
                "status": "PASS",
                "transformative_score": 100,
                "metrics": {}
            },
            "fair_use_metadata": {}
        }

    def _load_policy_db(self):
        if os.path.exists(self.policy_db_path):
            try:
                with open(self.policy_db_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Cảnh báo không đọc được {self.policy_db_path}: {e}")
        return {}

    def audit_script_policy(self, script_text: str):
        """
        1. Kiểm tra kịch bản qua 8 nhóm chính sách từ cấm nền tảng (YouTube Yellow Dollar, TikTok Ban, Meta Flag).
        Tự động bóc tách từ khóa rủi ro và gợi ý văn phong báo chí điều tra trung lập.
        """
        text_lower = script_text.lower()
        warnings = []
        flagged_items = []
        suggestions = {}
        score = 100

        for group_id, group_info in self.forbidden_groups.items():
            group_name = group_info.get("name", group_id)
            triggers = group_info.get("triggers", [])
            replacements = group_info.get("neutral_replacements", {})
            risk_level = group_info.get("risk_level", "WARNING")

            for trigger in triggers:
                # Tìm kiếm theo từ hoàn chỉnh hoặc cụm từ
                pattern = r"(?<!\w)" + re.escape(trigger.lower()) + r"(?!\w)"
                if re.search(pattern, text_lower):
                    rec = replacements.get(trigger, f"thay thế bằng thuật ngữ báo chí trung lập phù hợp cho '{trigger}'")
                    flagged_item = {
                        "group_id": group_id,
                        "group_name": group_name,
                        "flagged_word": trigger,
                        "risk_level": risk_level,
                        "suggested_replacement": rec
                    }
                    flagged_items.append(flagged_item)
                    suggestions[trigger] = rec

                    # Trừ điểm an toàn
                    if "STRICT" in risk_level:
                        score -= 25
                        warnings.append(f"[{group_name}] CỰC KỲ NGUY HIỂM: Phát hiện '{trigger}' -> Đề xuất: '{rec}'")
                    else:
                        score -= 10
                        warnings.append(f"[{group_name}] Cảnh báo vàng tiền: Phát hiện '{trigger}' -> Đề xuất: '{rec}'")

        score = max(0, score)
        self.report["policy_check"]["risk_score"] = score
        self.report["policy_check"]["flagged_items"] = flagged_items
        self.report["policy_check"]["sanitized_suggestions"] = suggestions

        if score < 70 or any("STRICT" in item["risk_level"] for item in flagged_items):
            self.report["policy_check"]["status"] = "FAIL"
        elif score < 95:
            self.report["policy_check"]["status"] = "WARNING"
        else:
            self.report["policy_check"]["status"] = "PASS"
            self.report["policy_check"]["warnings"] = ["Ngôn từ báo chí trung lập, đạt chuẩn 8 nhóm chính sách từ cấm."]

        if flagged_items:
            self.report["policy_check"]["warnings"] = warnings

        return self.report["policy_check"]

    def audit_anti_copyright_rules(self, scene_breakdown: list, bgm_info: dict = None):
        """
        2. Kiểm tra bộ khiên bản quyền 7 lớp (Anti-Copyright 7-Layer Shield):
           - Layer 1: 100% Audio Stripping (Xóa sạch audio gốc của footage).
           - Layer 2: Safe Cut Cadence (Không footage thô nào > 4.5 giây).
           - Layer 3: Dynamic Smart Zoom & Pan (105% - 108%).
           - Layer 4: Micro-speed ramp (1.03x - 1.04x).
           - Layer 5: Cinematic 3D LUT Color Grading.
           - Layer 6: Optical Texture & 35mm Film Grain + Vignette.
           - Layer 7: Spatial Transformative Overlay (Kinetic Text, Card 2.5D, Biểu đồ 3D).
        """
        violations = []
        score = 100
        layer_audits = {
            "layer_1_audio_stripping": {"pass": True, "details": "Toàn bộ footage đã được tước bỏ âm thanh gốc."},
            "layer_2_safe_cut_cadence": {"pass": True, "details": "Toàn bộ shot B-roll tuân thủ nhịp cắt <= 4.5s."},
            "layer_3_dynamic_smart_zoom": {"pass": True, "details": "Áp dụng phóng to thông minh 105%-108% đẩy lề watermark."},
            "layer_4_micro_speed_ramp": {"pass": True, "details": "Tốc độ khung hình biến thiên 1.03x-1.04x phá vỡ temporal hash."},
            "layer_5_cinematic_3d_lut": {"pass": True, "details": "Áp bảng màu 3D LUT chuyên dụng thay đổi phổ màu."},
            "layer_6_optical_texture_grain": {"pass": True, "details": "Lớp phủ hạt phim 35mm + Vignette tạo chữ ký quang học mới."},
            "layer_7_spatial_transformative_overlay": {"pass": True, "details": "Phủ đồ họa Spatial AR / 2.5D Card / Kinetic Typography."}
        }

        # Kiểm tra từng cảnh
        for idx, scene in enumerate(scene_breakdown):
            duration = scene.get("duration_seconds", 0)
            is_raw_footage = scene.get("is_raw_footage", False)
            has_visual_overlay = scene.get("has_visual_overlay", True)
            raw_audio_stripped = scene.get("raw_audio_stripped", True)
            zoom_ratio = scene.get("zoom_ratio", 1.06)
            lut_applied = scene.get("lut_applied", True)
            grain_applied = scene.get("grain_applied", True)
            speed_ramp = scene.get("speed_ramp", 1.03)

            # Lớp 1: Tước âm thanh gốc
            if not raw_audio_stripped:
                violations.append(f"Cảnh {idx+1}: Chưa tước bỏ âm thanh gốc (Nguy cơ dính Content ID âm thanh).")
                layer_audits["layer_1_audio_stripping"]["pass"] = False
                layer_audits["layer_1_audio_stripping"]["details"] = f"Phát hiện cảnh {idx+1} chưa tước âm thanh gốc."
                score -= 30

            # Lớp 2: Cắt nhịp tối đa 4.5s
            if is_raw_footage and duration > 4.5:
                violations.append(f"Cảnh {idx+1}: Thời lượng footage thô ({duration}s) vượt ngưỡng an toàn 4.5s.")
                layer_audits["layer_2_safe_cut_cadence"]["pass"] = False
                layer_audits["layer_2_safe_cut_cadence"]["details"] = f"Cảnh {idx+1} dài {duration}s (> 4.5s)."
                score -= 15

            # Lớp 3: Smart Zoom
            if is_raw_footage and (zoom_ratio < 1.04 or zoom_ratio > 1.12):
                violations.append(f"Cảnh {idx+1}: Zoom ratio ({zoom_ratio}) nằm ngoài dải an toàn (105% - 108%).")
                layer_audits["layer_3_dynamic_smart_zoom"]["pass"] = False
                score -= 10

            # Lớp 4: Speed Ramp
            if is_raw_footage and (speed_ramp < 1.01 or speed_ramp > 1.08):
                violations.append(f"Cảnh {idx+1}: Chưa cấu hình Micro-speed ramp vi mô an toàn.")
                layer_audits["layer_4_micro_speed_ramp"]["pass"] = False
                score -= 5

            # Lớp 5: LUT
            if not lut_applied:
                violations.append(f"Cảnh {idx+1}: Chưa áp dụng bảng màu 3D LUT (Giữ màu gốc dễ trùng pixel).")
                layer_audits["layer_5_cinematic_3d_lut"]["pass"] = False
                score -= 10

            # Lớp 6: Film Grain
            if not grain_applied:
                violations.append(f"Cảnh {idx+1}: Thiếu lớp Texture Film Grain 35mm.")
                layer_audits["layer_6_optical_texture_grain"]["pass"] = False
                score -= 10

            # Lớp 7: Transformative Overlay
            if not has_visual_overlay:
                violations.append(f"Cảnh {idx+1}: Thiếu lớp phủ đồ họa/chữ động (Không đạt Fair Use thị giác).")
                layer_audits["layer_7_spatial_transformative_overlay"]["pass"] = False
                score -= 15

        # Kiểm tra BGM
        if bgm_info:
            is_zero_copyright = bgm_info.get("is_zero_copyright", True)
            source = bgm_info.get("source", "ACE-Step 1.5 / Math Zero-Copyright")
            if not is_zero_copyright:
                violations.append(f"Nhạc nền BGM ({source}): Nguy cơ dính Content ID thương mại.")
                score -= 35

        score = max(0, score)
        self.report["anti_copyright_check"]["violations"] = violations
        self.report["anti_copyright_check"]["score"] = score
        self.report["anti_copyright_check"]["status"] = "PASS" if score >= 85 else ("WARNING" if score >= 70 else "FAIL")
        self.report["anti_copyright_check"]["layer_audits"] = layer_audits
        return self.report["anti_copyright_check"]

    def audit_reused_content_risk(self, transformative_elements: dict):
        """
        3. Kiểm tra chống nội dung lặp lại (Anti-Reused / Repetitious Content Policy của YouTube YPP 2026):
           Yêu cầu video phải có giá trị sáng tạo phái sinh cao:
           - Tỷ lệ đồ họa / 3D / Text động >= 70% thời lượng.
           - Nhạc nền độc bản (ACE-Step / AI Gen hoặc Zero-Copyright).
           - Mô hình bóc tách 3D / Biểu đồ trực quan hóa dữ liệu độc bản.
           - Giọng đọc thuyết minh có phân tầng cảm xúc, tốc độ biên tập riêng.
        """
        motion_graphics_ratio = transformative_elements.get("motion_graphics_ratio", 0.75)
        bgm_is_unique = transformative_elements.get("bgm_is_unique", True)
        has_original_3d = transformative_elements.get("has_original_3d", True)
        has_custom_vo_pacing = transformative_elements.get("has_custom_vo_pacing", True)

        score = 100
        metrics = {
            "Tỷ lệ can thiệp đồ họa chuyển động": f"{int(motion_graphics_ratio * 100)}% (Ngưỡng đạt chuẩn 2026: >= 70%)",
            "Nhạc nền độc bản / AI Gen": "ĐẠT (Không trùng lặp Content ID)" if bgm_is_unique else "CẢNH BÁO",
            "Mô hình 3D dữ liệu phân tích riêng": "ĐẠT (Độc bản theo kịch bản)" if has_original_3d else "CHƯA CÓ",
            "Biên tập giọng đọc Voiceover riêng biệt": "ĐẠT" if has_custom_vo_pacing else "THIẾU"
        }

        if motion_graphics_ratio < 0.70:
            score -= int((0.70 - motion_graphics_ratio) * 100)
        if not bgm_is_unique:
            score -= 25
        if not has_original_3d:
            score -= 15
        if not has_custom_vo_pacing:
            score -= 10

        score = max(0, score)
        self.report["anti_reused_content_check"]["transformative_score"] = score
        self.report["anti_reused_content_check"]["status"] = "PASS" if score >= 80 else ("WARNING" if score >= 65 else "FAIL")
        self.report["anti_reused_content_check"]["metrics"] = metrics
        return self.report["anti_reused_content_check"]

    def generate_fair_use_legal_kit(self, topic_title: str):
        """
        4. Tự động sinh Bộ Tuyên bố Pháp lý Fair Use song ngữ (Mục 107 Đạo luật Bản quyền Hoa Kỳ) 
           cho phần Mô tả (Description) để tự động hóa khiên kháng nghị YouTube/Facebook/TikTok.
        """
        disclaimer_en = f"""LEGAL FAIR USE & ATTRIBUTION DISCLAIMER (17 U.S. Code § 107):
This video titled "{topic_title}" is created strictly for investigative, educational, commentary, and journalistic documentary purposes.
Under Section 107 of the Copyright Act 1976 (17 U.S. Code § 107), allowance is made for 'fair use' for purposes such as criticism, comment, news reporting, teaching, scholarship, and research.
- All historical footage and news clips are transformed via non-destructive editorial commentary, analytical 3D data overlays, and original narration (Transformative Value >= 70%).
- Audio contains 100% original / licensed / mathematically generated zero-copyright background music and multi-layer transient foleys.
- For copyright inquiries, attribution, or licensing requests, please contact our channel administration directly."""

        disclaimer_vi = f"""TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM & BẢN QUYỀN HỢP LÝ (FAIR USE):
Tác phẩm phóng sự tài liệu "{topic_title}" được sản xuất phục vụ mục đích nghiên cứu, giáo dục, phân tích báo chí độc lập và bình luận xã hội.
Theo Mục 107 của Đạo luật Bản quyền Hoa Kỳ năm 1976 (17 U.S. Code § 107), việc sử dụng có giới hạn các tư liệu có bản quyền được công nhận là 'Hợp lệ' (Fair Use) cho các mục đích phê bình, bình luận, đưa tin thời sự và nghiên cứu học thuật.
- Mọi tư liệu lịch sử và bản tin thời sự đã được phái sinh hóa sâu sắc qua đồ họa không gian AR, mô hình hóa số liệu 3D, và giọng đọc phân tích nguyên bản.
- Toàn bộ âm nhạc nền được sinh tự động hoặc chứng nhận Zero-Copyright, không phụ thuộc vào nhạc thương mại có Content ID."""

        self.report["fair_use_metadata"] = {
            "title_topic": topic_title,
            "disclaimer_en": disclaimer_en,
            "disclaimer_vi": disclaimer_vi,
            "statute": "17 U.S. Code § 107 - Fair Use Doctrine",
            "generated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        return self.report["fair_use_metadata"]

    def run_full_audit(self, script_text: str, scene_breakdown: list, transformative_elements: dict, topic_title: str, bgm_info: dict = None):
        """Thực hiện toàn diện 4 trụ cột kiểm soát tuân thủ của Platform Compliance Sentinel."""
        self.audit_script_policy(script_text)
        self.audit_anti_copyright_rules(scene_breakdown, bgm_info)
        self.audit_reused_content_risk(transformative_elements)
        self.generate_fair_use_legal_kit(topic_title)
        return self.report

    def print_formal_report(self):
        """In báo cáo định dạng chuẩn quân sự chuyên nghiệp."""
        r = self.report
        print("\n" + "="*80)
        print("🛡️  BÁO CÁO THANH TRA BẢO VỆ NỀN TẢNG & KHIÊN ANTI-COPYRIGHT 7 LỚP")
        print("    Platform Compliance Sentinel - Supreme Inspection Unit")
        print("="*80)

        # 1. Policy Lexicon
        pol = r["policy_check"]
        print(f"\n[1] KIỂM SOÁT 8 NHÓM CHÍNH SÁCH TỪ CẤM: [{pol['status']}] (Điểm an toàn: {pol['risk_score']}/100)")
        if pol["flagged_items"]:
            print(f"    Phát hiện {len(pol['flagged_items'])} điểm chạm chính sách:")
            for item in pol["flagged_items"]:
                print(f"    - [{item['group_name']}] '{item['flagged_word']}' -> Đề xuất: '{item['suggested_replacement']}'")
        else:
            print("    -> 100% Sạch: Toàn bộ kịch bản tuân thủ chuẩn báo chí trung lập.")

        # 2. 7-Layer Shield
        cpy = r["anti_copyright_check"]
        print(f"\n[2] KHIÊN BẢN QUYỀN 7 LỚP (ANTI-COPYRIGHT): [{cpy['status']}] (Điểm bảo vệ: {cpy['score']}/100)")
        for layer_k, layer_v in cpy["layer_audits"].items():
            mark = "✅" if layer_v["pass"] else "❌"
            print(f"    {mark} {layer_k.upper()}: {layer_v['details']}")
        if cpy["violations"]:
            print("    Cảnh báo vi phạm:")
            for v in cpy["violations"]:
                print(f"    [!] {v}")

        # 3. Anti-Reused Content
        reused = r["anti_reused_content_check"]
        print(f"\n[3] CHỐNG NỘI DUNG LẶP LẠI (ANTI-REUSED CONTENT): [{reused['status']}] (Chỉ số phái sinh: {reused['transformative_score']}/100)")
        for k, v in reused["metrics"].items():
            print(f"    - {k}: {v}")

        # 4. Fair Use Kit
        fu = r["fair_use_metadata"]
        print(f"\n[4] BỘ PHÁP LÝ FAIR USE MỤC 107 HOA KỲ: ĐÃ SẴN SÀNG ({fu.get('title_topic', 'N/A')})")
        print("    - Tuyên bố bản quyền tiếng Anh & tiếng Việt sẵn sàng nạp vào Description YouTube.")
        print("="*80 + "\n")

# Hỗ trợ backward compatibility alias
PlatformComplianceSentinel = PlatformSafetyShield

if __name__ == "__main__":
    sentinel = PlatformSafetyShield()

    test_script = (
        "Tháng 10 năm 2022, Bộ Thương mại Mỹ tung đòn cấm vận bán dẫn toàn diện. "
        "Nvidia H100 bị chặn xuất khẩu sang Trung Quốc. Nhưng chỉ 2 năm sau, "
        "DeepSeek bùng nổ với chi phí chỉ bằng 1 phần 16, gây chấn động thung lũng Silicon."
    )

    test_scenes = [
        {"duration_seconds": 4.2, "is_raw_footage": True, "has_visual_overlay": True, "raw_audio_stripped": True, "zoom_ratio": 1.06, "lut_applied": True, "grain_applied": True, "speed_ramp": 1.03},
        {"duration_seconds": 4.5, "is_raw_footage": True, "has_visual_overlay": True, "raw_audio_stripped": True, "zoom_ratio": 1.07, "lut_applied": True, "grain_applied": True, "speed_ramp": 1.04},
        {"duration_seconds": 3.8, "is_raw_footage": True, "has_visual_overlay": True, "raw_audio_stripped": True, "zoom_ratio": 1.05, "lut_applied": True, "grain_applied": True, "speed_ramp": 1.03},
        {"duration_seconds": 4.0, "is_raw_footage": False, "has_visual_overlay": True, "raw_audio_stripped": True, "zoom_ratio": 1.00, "lut_applied": True, "grain_applied": True, "speed_ramp": 1.00},
    ]

    test_transformative = {
        "motion_graphics_ratio": 0.85,
        "bgm_is_unique": True,
        "has_original_3d": True,
        "has_custom_vo_pacing": True
    }

    test_bgm = {
        "is_zero_copyright": True,
        "source": "ACE-Step 1.5 Custom Prompted Synthwave Noir"
    }

    result = sentinel.run_full_audit(
        script_text=test_script,
        scene_breakdown=test_scenes,
        transformative_elements=test_transformative,
        topic_title="Chiến Tranh Bán Dẫn & Cú Đột Phá Bất Ngờ Của DeepSeek",
        bgm_info=test_bgm
    )

    sentinel.print_formal_report()
