"""
fact_and_retention_engine.py - BỘ TRINH SÁT SỰ THẬT 100% & KIỂM ĐỊNH ĐỘ CUỐN VIDEO NGẮN
(Dành riêng cho Đầu Não Video Ngắn FB: D:\Đầu Não Video Ngắn FB (không xóa))

Thực thi 2 Quy Tắc Cứng của Người Chỉ Huy:
1. NGHIÊN CỨU ĐÚNG SỰ THẬT 100% (ZERO HALLUCINATION):
   - Tuyệt đối cấm tự bịa số liệu, ngày tháng, tên tổ chức/nhân vật.
   - Tự động quét Google News RSS (VnExpress, CafeF, Tuổi Trẻ, Reuters, Bloomberg...) và Wikipedia API
     để lập Hồ Sơ Sự Thật (`fact_sheet.json`) trước khi viết kịch bản.
2. CÔNG THỨC LÔI CUỐN NGƯỜI XEM ĐẾN GIÂY CUỐI (5-BEAT VIRAL RETENTION):
   - Cấm mở đầu rề rà ("Xin chào các bạn", "Hôm nay chúng ta...").
   - Bắt buộc 3 giây đầu (Câu 1) phải có Con Số Gây Sốc + Nghịch Lý (Paradox Hook).
   - Bắt buộc đổi biến cố thị giác mỗi 2.5s - 3.5s (Camera Pan, Kéo cắt, Bản đồ 3D, Tháp tiền).
   - Bắt buộc có Nút Thắt Lật Mặt (Micro-Twist) ở giữa video và Đóng Dấu Kết Luận ở cuối video.
"""

import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}
WIKI_HEADERS = {
    "User-Agent": "AntigravityFactBot/1.0 (https://example.org; contact@example.org)"
}

FORBIDDEN_WEAK_OPENINGS = [
    "xin chào",
    "chào các bạn",
    "chào mọi người",
    "hôm nay chúng ta",
    "trong video này",
    "hãy cùng tìm hiểu",
    "bạn có biết rằng",
]

# Các tiền tố rào đón tiểu sử/thời gian ở ngay đầu Câu 1 làm người xem vuốt bỏ ở 0:02
SLOW_PREAMBLE_REGEX = re.compile(
    r"^(sau\s+(?:hơn\s+)?\d+|từ\s+năm\s+\d+|trải\s+qua\s+|từng\s+là\s+|suốt\s+(?:hơn\s+)?\d+|vốn\s+là\s+|trước\s+đây\s+)"
)

HOOK_ARCHETYPES = {
    "crisis_risk": {
        "label": "Biến cố / Vụ án / Rủi ro",
        "rule": "Đưa tình huống nguy cấp/rủi ro lên 5 từ đầu. Cấm kể công trạng trước.",
        "visual_mood": "Căng thẳng, nghiêm túc; tuyệt đối CẤM ảnh cười tươi ở 0.00s–2.00s.",
    },
    "paradox_secret": {
        "label": "Nghịch lý / Chiến lược dị biệt",
        "rule": "Nêu sự vô lý hoặc chi tiết bất thường ngay 5–7 từ đầu.",
        "visual_mood": "Tương phản sắc nét giữa hai vế đối lập (không cần màu đỏ tai họa).",
    },
    "tech_scale": {
        "label": "Công nghệ / Kỳ tích / Quy mô",
        "rule": "Đưa thẳng con số kỷ lục hoặc cảnh tượng khó tin ngay 5–7 từ đầu.",
        "visual_mood": "Vật thể 3D tả thực cận cảnh + Odometer nhảy số ngay 0.00s, sắc thái hiện đại.",
    },
    "money_consumer": {
        "label": "Tiền bạc / Tâm lý tiêu dùng",
        "rule": "Chạm thẳng túi tiền hoặc hiểu lầm của người xem trong 5–7 từ đầu.",
        "visual_mood": "Đặt 2 vật thật / 2 mức giá đối lập cạnh nhau ngay Frame 0.",
    },
}

HOOK_ANCHOR_REGEX = re.compile(
    r"(\d+|triệu|tỷ|nghìn|kiện|điều tra|khẩn cấp|sập|bốc hơi|đóng băng|bí mật|sự thật|"
    r"nghịch lý|vô lý|không có|tại sao|suýt|đặc biệt|cấm|lừa|mất|rời|đối đầu|sống còn|"
    r"kỷ lục|nhanh nhất|mạnh nhất|đắt|rẻ|lỗ|bẫy|độc quyền|lật tẩy|thất bại)"
)


def fetch_google_news_facts(topic_query: str, lang: str = "vi", max_items: int = 8) -> list[dict]:
    """
    Quét trực tiếp Google News RSS để lấy tiêu đề, nguồn báo chính thống và ngày xuất bản thật.
    """
    hl = "vi" if lang == "vi" else "en-US"
    gl = "VN" if lang == "vi" else "US"
    ceid = "VN:vi" if lang == "vi" else "US:en"
    encoded = urllib.parse.quote(topic_query)
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl={hl}&gl={gl}&ceid={ceid}"

    articles = []
    try:
        req = urllib.request.Request(rss_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
        for item in root.findall("./channel/item")[:max_items]:
            title = item.findtext("title", default="").strip()
            pub_date = item.findtext("pubDate", default="").strip()
            source_el = item.find("source")
            source_name = source_el.text.strip() if source_el is not None and source_el.text else "News"
            link = item.findtext("link", default="").strip()
            if title:
                articles.append({
                    "title": title,
                    "source": source_name,
                    "pub_date": pub_date,
                    "link": link,
                })
    except Exception as e:
        print(f"[FACT ENGINE WARN] Google News RSS error for '{topic_query}': {e}")
    return articles


def fetch_wikipedia_summary(query: str, lang: str = "vi") -> str:
    """Lấy tóm tắt bách khoa toàn thư từ Wikipedia để đối chiếu tên riêng & lịch sử."""
    encoded = urllib.parse.quote(query)
    api_url = (
        f"https://{lang}.wikipedia.org/w/api.php?action=query&list=search"
        f"&srsearch={encoded}&srlimit=2&format=json"
    )
    snippets = []
    try:
        req = urllib.request.Request(api_url, headers=WIKI_HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        for item in data.get("query", {}).get("search", []):
            clean_snip = re.sub(r"<[^>]+>", "", item.get("snippet", ""))
            snippets.append(f"[{item.get('title')}]: {clean_snip}")
    except Exception:
        pass
    return "\n".join(snippets)


def build_verified_fact_sheet(
    topic_vi: str,
    topic_en: str,
    out_json_path: str | Path,
) -> dict:
    """
    Tự động thu thập hồ sơ sự thật đa nguồn (Tiếng Việt + Quốc Tế) và xuất ra `fact_sheet.json`.
    BẮT BUỘC chạy bước này trước khi viết kịch bản!
    """
    out_json_path = Path(out_json_path)
    out_json_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[*] Đang trinh sát sự thật đa nguồn cho chủ đề: '{topic_vi}' / '{topic_en}'...")
    vi_news = fetch_google_news_facts(topic_vi, lang="vi", max_items=8)
    en_news = fetch_google_news_facts(topic_en, lang="en", max_items=6)
    wiki_vi = fetch_wikipedia_summary(topic_vi, lang="vi")
    wiki_en = fetch_wikipedia_summary(topic_en, lang="en")

    # Trích xuất tự động các con số xuất hiện trong tiêu đề báo chí để làm neo kiểm chứng
    all_titles = " | ".join([a["title"] for a in vi_news + en_news])
    extracted_numbers = list(dict.fromkeys(re.findall(r"\b\d+(?:[\.,]\d+)?(?:\s*(?:tỷ|triệu|nghìn|%|USD|đô|năm|tháng|máy bay|tàu bay))?\b", all_titles, flags=re.IGNORECASE)))

    fact_sheet = {
        "topic_vi": topic_vi,
        "topic_en": topic_en,
        "verified_numbers_in_press": extracted_numbers[:25],
        "vietnamese_press_sources": vi_news,
        "international_press_sources": en_news,
        "wikipedia_context": {
            "vi": wiki_vi,
            "en": wiki_en,
        },
    }

    out_json_path.write_text(json.dumps(fact_sheet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[FACT SHEET OK] Đã lưu {len(vi_news)} nguồn báo VN & {len(en_news)} nguồn quốc tế tại: {out_json_path}")
    return fact_sheet


def validate_short_script_retention(
    dialogue_segments: list[dict],
    hook_archetype: str = "auto",
) -> dict:
    """
    Kiểm định kịch bản video ngắn theo Công Thức Giữ Chân 5 Nhịp (5-Beat Retention)
    với Thiết Quân Luật Tối Ưu 2 Giây Đầu (chống rơi mốc 0:02 của FB Reels):
    1. Cấm mở đầu rề rà ("Xin chào...", "Sau X năm...", "Từ năm..."). Bối cảnh đẩy sang Câu 2.
    2. Câu 1 (Hook) dài tối đa 14 từ (~2.0s–2.6s) để kết thúc gọn trước ngưỡng mất kiên nhẫn.
    3. TỪ KHÓA TRỌNG TÂM PHẢI NỔ TRONG 7 TỪ ĐẦU (~1.4s đầu), linh hoạt theo 1 trong 4 kiểu Hook:
       crisis_risk | paradox_secret | tech_scale | money_consumer.
    4. Các câu thân bài không quá 28 từ để giữ nhịp cắt cảnh 2.5s - 4.0s.
    """
    issues = []
    if not dialogue_segments:
        return {"passed": False, "issues": ["Kịch bản trống!"]}

    first_text = dialogue_segments[0].get("text", "").strip()
    first_line = first_text.lower()
    first_words = first_text.split()

    for bad in FORBIDDEN_WEAK_OPENINGS:
        if bad in first_line:
            issues.append(f"VI PHẠM HOOK 3 GIÂY ĐẦU: Câu mở đầu chứa cụm từ rề rà '{bad}' làm tụt retention!")

    if SLOW_PREAMBLE_REGEX.match(first_line):
        issues.append(
            "VI PHẠM CẤU TRÚC HOOK (CHẬM Ở 0:02): Câu 1 mở đầu bằng tiền đề thời gian/lai lịch "
            "('Sau X năm / Từ năm / Trải qua...'). Hãy đẩy bối cảnh sang Câu 2 và đưa thẳng biến cố/nghịch lý lên đầu Câu 1!"
        )

    if len(first_words) > 14:
        issues.append(
            f"VI PHẠM ĐỘ DÀI HOOK: Câu 1 dài {len(first_words)} từ (> 14 từ, vượt ngưỡng 0:02–0:03). "
            "Bắt buộc rút gọn còn 7–13 từ (~2.0s–2.6s)!"
        )
    elif len(first_words) < 5:
        issues.append(f"CẢNH BÁO HOOK QUÁ NGẮN: Câu 1 chỉ có {len(first_words)} từ, chưa đủ thiết lập móc câu.")

    first_7_words = " ".join(first_words[:7]).lower()
    has_front_loaded_anchor = bool(HOOK_ANCHOR_REGEX.search(first_7_words))
    if not has_front_loaded_anchor:
        issues.append(
            "VI PHẠM VỊ TRÍ TỪ KHÓA HOOK: 7 từ đầu tiên (< 1.5s) chưa có Con Số hoặc Từ Khóa "
            "Xung Đột/Nghịch Lý/Kỷ Lục/Tiền Bạc -> khán giả sẽ vuốt bỏ ở mốc 0:02!"
        )

    for idx, seg in enumerate(dialogue_segments[1:], start=2):
        words = seg.get("text", "").strip().split()
        if len(words) > 28:
            issues.append(f"Câu {idx} quá dài ({len(words)} từ > 28 từ) -> Cần tách câu để giữ nhịp cắt cảnh 2.5s-4.0s!")

    passed = len(issues) == 0
    archetype_info = HOOK_ARCHETYPES.get(hook_archetype, {}).get("label", hook_archetype)
    print(f"[RETENTION QC | {archetype_info}] Kết quả kiểm định kịch bản: {'ĐẠT CHUẨN VIRAL 100%' if passed else 'CẦN SỬA LỖI'}")
    for iss in issues:
        print(f"  [!] {iss}")
    return {"passed": passed, "hook_archetype": hook_archetype, "issues": issues}


def build_hook_3s_sync_brief(
    hook_text: str,
    highlight_words: list[str],
    visual_shock_action: str,
    hero_asset_hint: str,
    sound_impact_cue: str,
    thumbnail_hook_line1: str,
    thumbnail_hook_line2: str,
    out_json_path: str | Path,
    hook_archetype: str = "paradox_secret",
    subject_mood_requirement: str = "",
) -> dict:
    """
    Xuất Bản Hợp Đồng Tác Chiến 3 Giây Đầu (`hook_3s_sync_brief.json`) để đồng bộ hóa
    4 bộ phận + QC Mắt Thần, linh hoạt theo đúng 4 kiểu Hook và BẮT BUỘC ĐẠO CỤ TẢ THỰC (cấm emoji hoạt hình).
    """
    out_json_path = Path(out_json_path)
    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    archetype_meta = HOOK_ARCHETYPES.get(hook_archetype, HOOK_ARCHETYPES["paradox_secret"])
    mood_req = subject_mood_requirement.strip() or archetype_meta["visual_mood"]

    brief = {
        "hook_window_sec": [0.0, 3.0],
        "hook_archetype": hook_archetype,
        "hook_archetype_label": archetype_meta["label"],
        "spoken_hook_text": hook_text.strip(),
        "word_count": len(hook_text.strip().split()),
        "front_loaded_first_7_words": " ".join(hook_text.strip().split()[:7]),
        "kinetic_caption_highlight_words": highlight_words,
        "prop_visual_standard": "PHOTOREALISTIC_REAL_PROP_ONLY (Bắt buộc ảnh chụp thật tách nền AI hoặc Đạo cụ 3D Studio tả thực riêng cho kịch bản; CẤM icon hoạt hình / emoji trong public/objects/)",
        "departments_sync": {
            "asset_harvester": {
                "priority_hero_asset": hero_asset_hint,
                "subject_mood_requirement": mood_req,
                "prop_requirement": "Chỉ dùng đồ vật chụp thật tách nền AI (auto_cutout.py) hoặc 3D Studio Render tả thực (kim loại/gỗ/kính thật), TUYỆT ĐỐI CẤM sticker/emoji hoạt hình và CẤM dùng lại ảnh/icon bài cũ.",
            },
            "motion_3d_director": {
                "frame_0_ready_rule": "Chủ thể + Đạo cụ chính PHẢI đứng sẵn trên sân khấu ngay Frame 0 (0.00s) — TUYỆT ĐỐI CẤM bục trống lúc 0.10s–0.20s hay fade-in đen.",
                "entry_motion": "Slam Zoom 1.35 -> 1.0 + Weighted Physical Spring ngay tại 0.04s.",
                "first_visual_turn_before_0_8s": f"Biến cố/Điểm nhấn thị giác đầu tiên PHẢI nổ trong khoảng 0.25s–0.80s (KHÔNG đợi tới 3.0s): {visual_shock_action}",
                "micro_escalation_at_1_6s": "Đẩy góc máy / bật lớp dữ liệu hoặc đạo cụ thật thứ 2 tại ~1.6s để giữ mắt qua mốc 0:02.",
            },
            "sound_sentinel": {
                "bgm_0_00s": "Vào nhịp nhạc đúng mood kịch bản ngay 0.00s (cấm intro kéo dài).",
                "sfx_0_00s": f"Đánh SFX khóa tay người xem tại 0.00s–0.20s ({sound_impact_cue}) khớp từ khóa đầu tiên.",
            },
            "qc_sentinel": {
                "early_frame_checkpoints_sec": [0.10, 0.80, 1.80],
                "pass_condition": "0.10s không được trống chủ thể; <=0.80s đã có biến cố/tương phản thị giác + chữ nhấn đúng mood; không có sticker hoạt hình.",
            },
            "thumbnail_architect": {
                "headlineLine1": thumbnail_hook_line1,
                "headlineLine2": thumbnail_hook_line2,
                "continuity_rule": "Thumbnail đặt câu hỏi/cú sốc -> 2 giây đầu video lập tức xác nhận và đẩy cao trào đúng mạch câu chuyện đó.",
            },
        },
    }
    out_json_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[HOOK 3S SYNC BRIEF OK | {hook_archetype}] Đã khóa hợp đồng đồng bộ tại: {out_json_path}")
    return brief


if __name__ == "__main__":
    test_fact_path = Path(r"D:\DuAn_DangLam\fb_reels_pilot\fact_sheet_vietjet.json")
    build_verified_fact_sheet(
        topic_vi="Vietjet vụ kiện thuê máy bay FitzWalter Tòa án London",
        topic_en="Vietjet Air FitzWalter aircraft lawsuit London court",
        out_json_path=test_fact_path,
    )
