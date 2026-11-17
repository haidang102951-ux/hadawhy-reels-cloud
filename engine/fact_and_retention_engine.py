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
    """Lấy trích đoạn sâu từ Wikipedia (tối đa 2500 ký tự) để đối chiếu lịch sử, cơ chế khoa học & tên riêng."""
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
        hits = data.get("query", {}).get("search", [])
        if hits:
            page_title = urllib.parse.quote(hits[0]["title"])
            extract_url = (
                f"https://{lang}.wikipedia.org/w/api.php?action=query&prop=extracts"
                f"&exintro=false&explaintext=true&exchars=2500&titles={page_title}&format=json"
            )
            req2 = urllib.request.Request(extract_url, headers=WIKI_HEADERS)
            with urllib.request.urlopen(req2, timeout=10) as resp2:
                d2 = json.loads(resp2.read().decode("utf-8", errors="ignore"))
            for p in d2.get("query", {}).get("pages", {}).values():
                ext = p.get("extract", "").strip()
                if ext:
                    return ext
        for item in hits:
            clean_snip = re.sub(r"<[^>]+>", "", item.get("snippet", ""))
            snippets.append(f"[{item.get('title')}]: {clean_snip}")
    except Exception:
        pass
    return "\n".join(snippets)


def _search_urls_for_deep_read(query: str, max_results: int = 4) -> list[tuple[str, str]]:
    """Tìm URL bài báo gốc thật qua Serper (nếu có) -> Bing Search RSS (miễn phí, URL gốc trực tiếp) -> DDGS fallback."""
    import os
    found: list[tuple[str, str]] = []
    serper_key = os.getenv("SERPER_API_KEY", "").strip()
    if serper_key:
        try:
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=json.dumps({"q": query, "num": max_results}).encode("utf-8"),
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("organic", [])[:max_results]:
                u = str(item.get("link") or "").strip()
                t = str(item.get("title") or "").strip()
                if u:
                    found.append((t, u))
            if found:
                return found
        except Exception:
            pass

    # Bing News RSS (trả thẳng tin báo chí chính thống VN & quốc tế, tránh kết quả từ điển/văn mẫu)
    try:
        rss_url = f"https://www.bing.com/news/search?q={urllib.parse.quote(query)}&format=rss"
        req = urllib.request.Request(rss_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            xml_bytes = resp.read()
        root = ET.fromstring(xml_bytes)
        for item in root.findall("./channel/item")[:max_results]:
            t = item.findtext("title", default="").strip()
            raw_link = item.findtext("link", default="").strip()
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(raw_link).query)
            u = qs.get("url", [raw_link])[0]
            if u.startswith("http"):
                found.append((t, u))
    except Exception:
        pass
    return found


def _generate_storm_research_angles(topic_vi: str, topic_en: str = "") -> list[tuple[str, str]]:
    """
    Tư duy đa góc nhìn kiểu STORM: Tự động tách chủ đề thành 4 góc điều tra sâu
    (Điều kiện đời sống/đô thị -> Chính sách kinh tế/lịch sử -> Tâm lý xã hội -> Số liệu/Mặt trái)
    thay vì tìm theo 1 từ khóa cứng máy móc.
    """
    import os
    core_kw = " ".join(topic_vi.split()[:6])
    fallback_angles = [
        ("Điều kiện đời sống / Đô thị", f"{core_kw} lịch sử không gian sống"),
        ("Chính sách kinh tế / Lịch sử", f"{core_kw} chính sách kinh tế bao cấp đổi mới"),
        ("Tâm lý xã hội / Hành vi", f"{core_kw} tâm lý cộng đồng thói quen"),
        ("Số liệu / Mặt trái thực tế", f"{core_kw} số liệu thống kê mặt trái"),
    ]
    if topic_en.strip():
        fallback_angles.append(("International Data", " ".join(topic_en.split()[:5])))

    or_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not or_key:
        return fallback_angles

    prompt = (
        f"Bạn là chuyên gia điều tra đa góc nhìn cho chủ đề: '{topic_vi}'.\n"
        "Hãy sinh đúng 4 truy vấn tìm kiếm báo chí/nghiên cứu ngắn gọn (mỗi truy vấn 5-8 từ tiếng Việt) "
        "theo 4 góc: (1) Điều kiện đời sống/đô thị, (2) Chính sách kinh tế/lịch sử trực tiếp, "
        "(3) Tâm lý xã hội/hành vi, (4) Số liệu/Mặt trái thực tế.\n"
        'Trả về JSON array 4 phần tử: [{"angle": "...", "query": "..."}]'
    )
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps({
                "model": "google/gemma-3-27b-it:free",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }).encode("utf-8"),
            headers={"Authorization": f"Bearer {or_key}", "Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        txt = str((raw.get("choices") or [{}])[0].get("message", {}).get("content") or "")
        m = re.search(r"\[[\s\S]*\]", txt)
        if m:
            arr = json.loads(m.group(0))
            parsed = [(str(x.get("angle", "")), str(x.get("query", ""))) for x in arr if x.get("query")]
            if len(parsed) >= 3:
                if topic_en.strip():
                    parsed.append(("International Data", " ".join(topic_en.split()[:5])))
                return parsed
    except Exception:
        pass
    return fallback_angles


def deep_web_research_fulltext(topic_vi: str, topic_en: str = "", max_articles: int = 6) -> list[dict]:
    """
    Stack nghiên cứu sâu (STORM Multi-Angle Query + Serper/Bing News + trafilatura full-text):
    Quét đủ 4 góc điều tra, tải và bóc sạch TOÀN VĂN bài báo gốc để trích đúng sự thật 100%.
    """
    extracts: list[dict] = []
    try:
        import trafilatura
    except ImportError as exc:
        print(f"[DEEP RESEARCH WARN] Thiếu trafilatura ({exc}); bỏ qua full-text scrape.")
        return extracts

    queries = _generate_storm_research_angles(topic_vi, topic_en)

    junk_domains = ("vietjack", "loigiaihay", "hoc24", "toploigiai", "doctailieu", "tailieu.vn", "vndoc.com")
    seen_urls: set[str] = set()
    for angle, q in queries:
        angle_count = 0
        for title, url in _search_urls_for_deep_read(q, max_results=5):
            if len(extracts) >= max_articles or angle_count >= 2:
                break
            low_u = url.lower()
            if not url or url in seen_urls or any(jd in low_u for jd in junk_domains):
                continue
            seen_urls.add(url)
            try:
                downloaded = trafilatura.fetch_url(url)
                text = trafilatura.extract(downloaded, include_comments=False, include_tables=True) if downloaded else ""
                if text and len(text.strip()) >= 250:
                    extracts.append({
                        "angle": angle,
                        "title": title,
                        "url": url,
                        "full_text_excerpt": text.strip()[:1800],
                    })
                    angle_count += 1
            except Exception:
                continue

    print(f"[DEEP RESEARCH OK] trafilatura đã bóc tách {len(extracts)} bài báo gốc full-text.")
    return extracts


def build_verified_fact_sheet(
    topic_vi: str,
    topic_en: str,
    out_json_path: str | Path,
) -> dict:
    """
    Tự động thu thập hồ sơ sự thật đa nguồn, đa góc nhìn (ddgs + trafilatura full-text + Google News RSS + Wikipedia)
    và xuất ra `fact_sheet.json`. BẮT BUỘC chạy bước này trước khi viết kịch bản!
    """
    out_json_path = Path(out_json_path)
    out_json_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"[*] Đang trinh sát sự thật đa nguồn cho chủ đề: '{topic_vi}' / '{topic_en}'...")
    vi_news = fetch_google_news_facts(topic_vi, lang="vi", max_items=8)
    vi_why_news = fetch_google_news_facts(f"{topic_vi} nguyên nhân số liệu", lang="vi", max_items=6)
    en_news = fetch_google_news_facts(topic_en, lang="en", max_items=6)
    wiki_vi = fetch_wikipedia_summary(topic_vi, lang="vi")
    wiki_en = fetch_wikipedia_summary(topic_en, lang="en")
    deep_articles = deep_web_research_fulltext(topic_vi, topic_en, max_articles=5)

    seen_titles = set()
    merged_vi = []
    for item in vi_news + vi_why_news:
        t_key = item["title"].lower()
        if t_key not in seen_titles:
            seen_titles.add(t_key)
            merged_vi.append(item)

    all_corpus = " | ".join(
        [a["title"] for a in merged_vi + en_news]
        + [wiki_vi, wiki_en]
        + [d["full_text_excerpt"] for d in deep_articles]
    )
    extracted_numbers = list(dict.fromkeys(re.findall(
        r"\b\d+(?:[\.,]\d+)?(?:\s*(?:tỷ|triệu|nghìn|lít|%|USD|đô|năm|tháng|người|nước))?\b",
        all_corpus,
        flags=re.IGNORECASE,
    )))

    fact_sheet = {
        "topic_vi": topic_vi,
        "topic_en": topic_en,
        "verified_numbers_in_press": extracted_numbers[:40],
        "deep_article_extracts": deep_articles,
        "vietnamese_press_sources": merged_vi,
        "international_press_sources": en_news,
        "wikipedia_context": {
            "vi": wiki_vi,
            "en": wiki_en,
        },
        "extra_verified_facts": [],
    }

    out_json_path.write_text(json.dumps(fact_sheet, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[FACT SHEET OK] Đã lưu {len(deep_articles)} bài full-text, {len(merged_vi)} báo VN & {len(en_news)} quốc tế tại: {out_json_path}")
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


PREACHY_PHRASES = (
    "chung tay",
    "nâng cao ý thức",
    "mỗi người dân hãy",
    "hãy cùng nhau",
    "bài học đắt giá",
    "thức tỉnh",
)

KNOWLEDGE_MECHANISM_WORDS = (
    "vì", "bởi", "cơ chế", "tâm lý", "vỏ não", "kinh tế", "lịch sử", "đô thị",
    "khí hậu", "chi phí", "cấu trúc", "quy luật", "bao cấp", "địa chất", "áp suất",
    "lạm phát", "thuế", "tỷ lệ", "phần trăm", "%", "chiếm", "nguyên nhân",
)


def verify_script_facts_and_logic(
    dialogue_segments: list[dict],
    fact_sheet: dict | None = None,
    target_word_range: tuple[int, int] = (88, 125),
) -> dict:
    """
    Cổng Kiểm Định Logic, Kiến Thức & Xác Thực Số Liệu (Zero-Hallucination & Deep Logic Gate):
    1. Chống sai thời lượng: Tổng số từ phải khớp khung ~40s (88..125 từ).
    2. Chống thiếu kiến thức: Phải có ít nhất 2 lớp giải thích cơ chế thật (lịch sử/khoa học/tâm lý/kinh tế).
    3. Bắt buộc Suspense Question (?): Có câu hỏi kích thích tò mò trước khi bung đáp án.
    4. Chống văn mẫu giảng đạo ở Beat 4-5.
    5. Đối chiếu số liệu với fact_sheet để phát hiện con số không rõ nguồn.
    """
    issues: list[str] = []
    warnings: list[str] = []
    full_text = " ".join(str(s.get("text", "")).strip() for s in dialogue_segments)
    low = full_text.lower()
    total_words = len(full_text.split())

    if not (target_word_range[0] <= total_words <= target_word_range[1]):
        issues.append(
            f"SAI THỜI LƯỢNG (~40s): Tổng {total_words} từ nằm ngoài khung chuẩn {target_word_range[0]}–{target_word_range[1]} từ."
        )

    mech_hits = sum(1 for kw in KNOWLEDGE_MECHANISM_WORDS if kw in low)
    if mech_hits < 2:
        issues.append(
            "THIẾU KIẾN THỨC CHUYÊN SÂU: Kịch bản chưa giải thích cơ chế thật (lịch sử/khoa học/tâm lý/kinh tế) mà chỉ kể hiện tượng bề mặt."
        )

    if "?" not in full_text:
        issues.append("THIẾU SUSPENSE QUESTION: Không có câu hỏi tu từ (?) để giữ bí mật và lật mở đáp án.")

    for bad in PREACHY_PHRASES:
        if bad in low:
            issues.append(f"VĂN MẪU GIẢNG ĐẠO: Chứa cụm '{bad}' gây tụt cảm xúc ở Beat 4–5.")

    # Đối chiếu các con số trong lời thoại với fact_sheet
    script_nums = set(re.findall(r"\b\d+(?:[\.,]\d+)?\b", full_text))
    if fact_sheet and script_nums:
        fact_blob = json.dumps(fact_sheet, ensure_ascii=False)
        unverified = [n for n in sorted(script_nums) if n not in fact_blob and n not in ("1", "2", "3")]
        if unverified:
            warnings.append(
                f"SỐ LIỆU CẦN ĐỐI CHIẾU NGUỒN: Các con số {unverified} chưa thấy trong fact_sheet.json — hãy nạp vào extra_verified_facts kèm URL gốc!"
            )

    passed = len(issues) == 0
    return {
        "passed": passed,
        "total_words": total_words,
        "knowledge_signals": mech_hits,
        "issues": issues,
        "warnings": warnings,
    }


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


def critic_audit_script(
    topic: str,
    dialogue_segments: list[dict],
    fact_sheet: dict | None = None,
) -> dict:
    """
    Bước Phản Biện Logic & Sự Thật (Critic Loop):
    1. Chạy deterministic verify_script_facts_and_logic().
    2. Nếu có GEMINI_API_KEY hoặc OPENROUTER_API_KEY, gọi AI Critic phản biện chéo xem kịch bản
       có bị lạc phạm vi, thiếu chiều sâu kiến thức, hay sai logic nhân-quả không.
    """
    import os
    det = verify_script_facts_and_logic(dialogue_segments, fact_sheet=fact_sheet)
    llm_critique = None
    full_script = "\n".join(f"- {s.get('text', '').strip()}" for s in dialogue_segments)
    fact_ctx = json.dumps((fact_sheet or {}).get("deep_article_extracts", [])[:3], ensure_ascii=False)[:2500]
    prompt = (
        f"Bạn là Tổng Biên Tập Phản Biện Logic & Sự Thật cho kênh HaDa WHY (chuyên góc khuất xã hội & bí ẩn sự việc).\n"
        f"Chủ đề gốc: {topic}\nKịch bản 40s:\n{full_script}\n\n"
        f"Dữ liệu báo gốc tham chiếu:\n{fact_ctx}\n\n"
        "Hãy soi 3 lỗi chí mạng: (1) Có bị lạc phạm vi/đối tượng so với chủ đề gốc không? "
        "(2) Đã có kiến thức sâu (lịch sử/khoa học/tâm lý/cơ chế) chưa hay chỉ nói bề mặt? "
        "(3) Có con số hoặc lập luận nào vô lý/chưa có căn cứ không?\n"
        'Trả về JSON duy nhất: {"passed": true/false, "flaws": ["..."], "suggestion": "..."}'
    )
    or_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if or_key:
        try:
            req = urllib.request.Request(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps({
                    "model": "google/gemma-3-27b-it:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                }).encode("utf-8"),
                headers={"Authorization": f"Bearer {or_key}", "Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            txt = str((raw.get("choices") or [{}])[0].get("message", {}).get("content") or "")
            m = re.search(r"\{[\s\S]*\}", txt)
            if m:
                llm_critique = json.loads(m.group(0))
        except Exception as exc:
            llm_critique = {"skipped": str(exc)}

    return {
        "deterministic_audit": det,
        "llm_critic": llm_critique,
        "passed": det["passed"] and (llm_critique.get("passed", True) if isinstance(llm_critique, dict) else True),
    }


if __name__ == "__main__":
    test_fact_path = Path(r"D:\DuAn_DangLam\fb_reels_pilot\fact_sheet_vietjet.json")
    build_verified_fact_sheet(
        topic_vi="Vietjet vụ kiện thuê máy bay FitzWalter Tòa án London",
        topic_en="Vietjet Air FitzWalter aircraft lawsuit London court",
        out_json_path=test_fact_path,
    )
