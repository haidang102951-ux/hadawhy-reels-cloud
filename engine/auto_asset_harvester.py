# -*- coding: utf-8 -*-
r"""
auto_asset_harvester.py - ĐẦU NÃO CÀO TƯ LIỆU THỰC TẾ & MẮT THẦN GEMINI VISION ĐỘC BẢN
(Dành riêng cho Hệ thống Video Ngắn FB Reels: D:\Đầu Não Video Ngắn FB (không xóa))

TRIỆT TIÊU 100% CÁC LỖI TỬ HUYỆT (ZERO-MISMATCH MANDATE):
1. CẤM TUYỆT ĐỐI ẨN DỤ TRỪU TƯỢNG VÔ NGHĨA (BANNED METAPHORS):
   - Chặn đứng 100% việc video công nghệ/đời thực lại đi cào cân công lý thời trung cổ,
     não hoạt hình, chai nước hoa hay bảng ăn kiêng!
   - Bắt buộc tư liệu phải là THỰC THỂ THỰC TẾ: Giao diện app thật, tài xế thật,
     máy chủ thật, bản đồ nhiệt thật, hồ sơ/bằng chứng thật.
2. ĐA TẦNG NGUỒN DỮ LIỆU ĐẲNG CẤP:
   - Tầng 1: Tavily Image Search (Báo chí chính thống VN: Thanh Niên, Tuổi Trẻ, Dân Trí, CafeF).
   - Tầng 2: Wikimedia Commons API (Kho lưu trữ quốc tế, siêu máy chủ, bản đồ, phần cứng).
   - Tầng 3: Bing HD Clean qua Playwright (Lọc sạch 100% domain rác).
3. CHẶN ĐỨNG 100% WATERMARK & DOMAIN RÁC:
   - Danh sách đen: Alamy, Shutterstock, Getty, iStock, Pinterest, eBay, Shopee...
4. MẮT THẦN GEMINI VISION PHÊ DUYỆT BẮT BUỘC (MULTI-KEY FAILOVER):
   - Soi chiếu trực tiếp ảnh tải về với chủ đề bài viết và bối cảnh câu thoại.
   - Bác bỏ ngay lập tức nếu ảnh lạc đề, mờ nhòe, hoặc dính chữ bản quyền.
5. TỰ ĐỘNG XUẤT ẢNH TIẾP XÚC (CONTACT SHEET) KIỂM ĐỊNH THỊ GIÁC:
   - Ghép toàn bộ tư liệu đã cào vào 1 ảnh lưới contact sheet duy nhất có nhãn sắc nét
     để Con Tổng soi trực tiếp trước khi bắt tay vào dựng video.
"""

from __future__ import annotations

import html
import io
import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if sys.stderr:
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

FB_ROOT = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
ENGINE_DIR = FB_ROOT / "engine"
DEFAULT_HARVEST_DIR = Path(r"D:\DuAn_DangLam\temp\assets")

# Nạp API keys từ hệ thống HaDaWhy Facebook AI
HADA_FB_DIR = Path(r"D:\HaDaWhy_Facebook_AI")
load_dotenv(HADA_FB_DIR / ".env")
if str(HADA_FB_DIR) not in sys.path:
    sys.path.insert(0, str(HADA_FB_DIR))

try:
    import hd_image_extractor as vision_inspector
    HAS_VISION_INSPECTOR = True
except Exception as exc:
    print(f"[HARVESTER WARN] Không thể import hd_image_extractor ({exc}). Fallback sang chế độ lọc chữ ký.")
    HAS_VISION_INSPECTOR = False


# =============================================================================
# 1. BỘ LỌC ẨN DỤ TRỪU TƯỢNG VÔ NGHĨA (CHỐNG LỆCH CHỦ ĐỀ NGAY TỪ ĐẦU VÀO)
# =============================================================================
BANNED_ABSTRACT_METAPHORS = [
    "scale", "justice scale", "balance scale", "cái cân", "chiếc cân", "cân công lý",
    "perfume", "nước hoa", "louis vuitton",
    "diet", "nutrition", "workout", "giảm cân", "thực đơn",
    "cartoon brain", "icon não", "plastic icon", "sticker",
    "handshake 3d", "bàn tay bắt tay", "hộp quà 3d",
    # Chặn các từ khóa kéo ra đồ CGI/nhựa giả, siêu thực/ma-nơ-canh & nhạy cảm vi phạm chính sách FB/TikTok
    "3d icon", "3d render", "3d model", "blender", "cgi", "isometric",
    "glossy icon", "illustration", "mockup", "vector", "pngtree", "clipart",
    "mannequin", "ma-nơ-canh", "surreal", "wax figure", "doll",
    "bikini", "lingerie", "nsfw", "nude", "sexy", "erotic", "gore", "blood", "corpse", "deformed",
]

def validate_harvest_query(query: str, topic_domain: str = "") -> None:
    """
    Kiểm tra tính hợp lệ của từ khóa tìm kiếm:
    Tuyệt đối cấm các từ khóa ẩn dụ vô hồn (cái cân, nước hoa, thực đơn ăn kiêng) và từ khóa CGI/render/icon.
    """
    q_low = query.lower()
    for banned in BANNED_ABSTRACT_METAPHORS:
        if banned in q_low:
            raise ValueError(
                f"[LỖI VI PHẠM KỶ LUẬT THỊ GIÁC] Từ khóa '{query}' chứa ẩn dụ trừu tượng/sai lệch '{banned}'. "
                f"Chủ đề '{topic_domain}' yêu cầu thực thể thực tế (tên riêng chính xác + ảnh chụp thật)!"
            )
    if re.search(r"\brender\b", q_low):
        raise ValueError(
            f"[LỖI VI PHẠM KỶ LUẬT THỊ GIÁC] Từ khóa '{query}' chứa từ cấm 'render'. "
            "Chỉ dùng từ khóa chụp thật ('official photo', 'close up', 'isolated', 'product photography', 'archival photo')!"
        )


# =============================================================================
# 2. DANH SÁCH ĐEN TÊN MIỀN RÁC & WATERMARK THƯƠNG MẠI
# =============================================================================
BANNED_DOMAINS = [
    # Stock photo watermark heavy
    "alamy.com", "shutterstock.com", "gettyimages.com", "istockphoto.com",
    "dreamstime.com", "depositphotos.com", "123rf.com", "vecteezy.com",
    "stock.adobe.com", "ftcdn.net", "vectorstock.com", "canstockphoto.com", "bigstockphoto.com",
    "freepik.com", "pngwing.com", "pngtree.com", "flaticon.com", "stockcake.com", "magnific.com",
    "thuthuatphanmem.vn",
    # Pinterest & spam pinboards
    "pinterest.com", "pinimg.com",
    # E-commerce marketplace ads
    "ebay.com", "amazon.com", "aliexpress.com", "temu.com",
    "shopee.vn", "lazada.vn", "tiki.vn", "alibaba.com", "dhgate.com",
    # Low quality user avatars
    "lookaside.fbsbx.com", "lookaside.instagram.com", "fbcdn.net",
]

JUNK_PATH_PATTERNS = [
    "logo_default", "logo.", "/logo", "logo_", "icon.", "/icon",
    "/avatar.", "/avatars/", "avatar_default", "default_avatar",
    "placeholder", "default_image", "banner", "tracking", "button", "badge",
    "meme", "clipart", "emoji", "sticker", "cartoon", "vector",
    "3d icon", "3d-icon", "3d_icon", "3d render", "3d-render", "3d_render",
    "3d model", "3d-model", "blender", "cgi", "isometric",
    "glossy icon", "illustration", "mockup", "pngtree",
    "watermark", "logo-tron", "stamp-logo", "mannequin", "surreal",
    "bikini", "lingerie", "nsfw", "nude", "sexy", "gore", "blood",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
}

WIKI_HEADERS = {
    "User-Agent": "HaDaWhyMediaProducer/2.0 (mailto:admin@hadawhy.vn)"
}

SSL_CTX = ssl._create_unverified_context()


def is_banned_url(url: str) -> bool:
    """Kiểm tra URL có thuộc tên miền dính watermark hoặc spam không."""
    low = url.lower()
    for dom in BANNED_DOMAINS:
        if dom in low:
            return True
    for pat in JUNK_PATH_PATTERNS:
        if pat in low:
            return True
    return False


# =============================================================================
# 3. NGUỒN TƯ LIỆU 1: TAVILY IMAGE SEARCH (BÁO CHÍ CHÍNH THỐNG VIỆT NAM)
# =============================================================================
def search_tavily_editorial_images(query: str, max_urls: int = 8) -> List[str]:
    """Tìm kiếm ảnh báo chí thực tế chất lượng cao qua Tavily Search API."""
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if not tavily_key:
        return []

    urls: List[str] = []
    try:
        req = urllib.request.Request(
            "https://api.tavily.com/search",
            data=json.dumps({
                "api_key": tavily_key,
                "query": query,
                "include_images": True,
                "max_results": max_urls,
            }).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=12, context=SSL_CTX) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for u in data.get("images", []):
                if is_banned_url(u):
                    continue
                if u not in urls:
                    urls.append(u)
    except Exception as exc:
        print(f"[HARVESTER WARN] Tavily Image Search error: {exc}")
    return urls


# =============================================================================
# 4. NGUỒN TƯ LIỆU 2: WIKIMEDIA COMMONS CHÍNH QUY (FILE NAMESPACE = 6)
# =============================================================================
def search_wikimedia_commons(query: str, max_urls: int = 8) -> List[str]:
    """Tìm kiếm trực tiếp trên Wikimedia Commons API chuẩn namespace 6 (File:)."""
    encoded = urllib.parse.quote(query)
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&list=search"
        f"&srsearch={encoded}&srnamespace=6&srlimit={max_urls}&format=json"
    )
    urls: List[str] = []
    try:
        req = urllib.request.Request(api_url, headers=WIKI_HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        search_items = data.get("query", {}).get("search", [])

        for item in search_items:
            title = item.get("title", "")
            if not any(title.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                continue

            info_url = (
                f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}"
                f"&prop=imageinfo&iiprop=url|size&format=json"
            )
            req2 = urllib.request.Request(info_url, headers=WIKI_HEADERS)
            with urllib.request.urlopen(req2, timeout=8, context=SSL_CTX) as resp2:
                info_data = json.loads(resp2.read().decode("utf-8", errors="ignore"))
            pages = info_data.get("query", {}).get("pages", {})
            for _, p in pages.items():
                iinfo = p.get("imageinfo", [])
                if iinfo:
                    direct_url = iinfo[0].get("url", "")
                    w = iinfo[0].get("width", 0)
                    h = iinfo[0].get("height", 0)
                    if direct_url and w >= 600 and h >= 400:
                        urls.append(direct_url)
    except Exception as exc:
        print(f"[HARVESTER WARN] Wikimedia search error: {exc}")
    return urls


# =============================================================================
# 5. NGUỒN TƯ LIỆU 3: BING IMAGES HD (LỌC 100% SPAM DOMAINS)
# =============================================================================
def search_bing_hd_clean(query: str, max_urls: int = 15) -> List[str]:
    """Quét Bing Images bằng Playwright headless, tự động gạt bỏ 100% domain rác."""
    encoded = urllib.parse.quote(query)
    search_url = f"https://www.bing.com/images/search?q={encoded}"
    urls: List[str] = []

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=HEADERS["User-Agent"])
            page = ctx.new_page()
            page.goto(search_url, wait_until="domcontentloaded", timeout=16000)
            page.wait_for_timeout(1500)
            cards = page.evaluate("""() => {
                const out = [];
                for (const el of document.querySelectorAll('a.iusc')) {
                    const m = el.getAttribute('m');
                    if (m) {
                        try {
                            const parsed = JSON.parse(m);
                            if (parsed.murl) out.push(parsed.murl);
                        } catch(e) {}
                    }
                }
                return out;
            }""")
            browser.close()
            for u in cards:
                if is_banned_url(u):
                    continue
                if any(ext in u.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                    if u not in urls:
                        urls.append(u)
                if len(urls) >= max_urls:
                    break
        if urls:
            return urls
    except Exception as exc:
        print(f"[HARVESTER WARN] Playwright error: {exc}. Fallback regex...")

    # Fallback nhẹ bằng urllib
    try:
        req = urllib.request.Request(search_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
            page_html = resp.read().decode("utf-8", errors="ignore")
        matches = re.findall(r'murl&quot;:&quot;(https?://[^&]+?)&quot;', page_html)
        for m in matches:
            clean_url = html.unescape(m)
            if is_banned_url(clean_url):
                continue
            if any(ext in clean_url.lower() for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                if clean_url not in urls:
                    urls.append(clean_url)
            if len(urls) >= max_urls:
                break
    except Exception as exc:
        print(f"[HARVESTER WARN] Bing fallback error: {exc}")
    return urls


# =============================================================================
# 6. MẮT THẦN GEMINI VISION THẨM ĐỊNH NỘI DUNG (CÓ --skip-vision & AUTO-FALLBACK 429)
# =============================================================================
_SKIP_VISION_SESSION = False


def set_skip_vision(skip: bool) -> None:
    global _SKIP_VISION_SESSION
    _SKIP_VISION_SESSION = bool(skip)


def verify_candidate_with_vision(
    img_path: Path,
    expected_entity: str,
    context_sentence: str = "",
    topic_domain: str = "",
    skip_vision: bool = False,
) -> Tuple[bool, str]:
    """
    Soi mắt thần Gemini Vision trước khi cấp phép lưu ảnh.
    - Nếu bật skip_vision hoặc phiên đã gặp 429/RESOURCE_EXHAUSTED: tự động bỏ qua API Vision
      (vẫn giữ nguyên 100% lọc domain rác, độ phân giải, từ khóa cấm, dHash và check_cutout_completeness).
    """
    global _SKIP_VISION_SESSION

    if skip_vision or _SKIP_VISION_SESSION:
        return True, "Đã bỏ qua API Vision (--skip-vision / auto-fallback 429)."

    if not HAS_VISION_INSPECTOR:
        return True, "Vision Inspector không khả dụng, bỏ qua."

    strict_real_photo_rule = (
        "YÊU CẦU TUYỆT ĐỐI VỀ CHẤT LIỆU & KHUNG HÌNH: "
        "TỪ CHỐI NGAY (is_match=false) mọi ảnh 3D render bóng nhựa, CGI, Blender, hình vẽ minh họa (illustration), "
        "clipart, vector, mockup, icon hoạt hình, HOẶC ảnh bị cắt cụt mất đầu/nửa xe/nửa vật thể ở viền khung hình. "
        "CHỈ DUYỆT ảnh chụp vật lý thật ngoài đời có vật liệu thật (kim loại, gỗ, giấy in, linh kiện thật, hiện trường thật) và chủ thể nằm trọn trong khung hình."
    )
    full_context = f"{topic_domain} | {context_sentence} | {strict_real_photo_rule}".strip(" |")
    try:
        status, reason = vision_inspector._verify_image_with_vision(
            str(img_path),
            topic_title=expected_entity,
            topic_context=full_context,
        )
        reason_low = str(reason or "").lower()
        if status is None or any(tok in reason_low for tok in ("429", "resource_exhausted", "quota", "hạn ngạch", "rate limit")):
            _SKIP_VISION_SESSION = True
            print(f"   [VISION AUTO-FALLBACK 429] Gặp giới hạn API ({reason}) -> Tự động bật --skip-vision cho các ảnh còn lại!")
            return True, f"Auto-fallback bỏ qua Vision do 429/quota ({reason})."
        return bool(status), str(reason)
    except Exception as exc:
        err_low = str(exc).lower()
        if any(tok in err_low for tok in ("429", "resource_exhausted", "quota", "rate limit")):
            _SKIP_VISION_SESSION = True
            print(f"   [VISION AUTO-FALLBACK 429] Gặp ngoại lệ API ({exc}) -> Tự động bật --skip-vision cho các ảnh còn lại!")
            return True, f"Auto-fallback bỏ qua Vision do 429/quota ({exc})."
        return False, f"Lỗi Mắt Thần Vision: {exc}"


# =============================================================================
# 7. CHỐNG LẶP ẢNH 3 TẦNG (URL + MD5 + PERCEPTUAL DHASH + LỊCH SỬ TẬP CŨ)
# =============================================================================
IMAGE_HISTORY_PATH = ENGINE_DIR / "image_used_history.json"


def _compute_dhash_hex(img: Image.Image) -> str:
    """Tính perceptual dHash 64-bit (16 ký tự hex) để phát hiện ảnh trùng kể cả khác kích thước/CDN."""
    gray = img.convert("L").resize((9, 8), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    bits = 0
    for row in range(8):
        row_start = row * 9
        for col in range(8):
            bits = (bits << 1) | (1 if pixels[row_start + col] > pixels[row_start + col + 1] else 0)
    return f"{bits:016x}"


def _dhash_hamming(hex_a: str, hex_b: str) -> int:
    try:
        return (int(hex_a, 16) ^ int(hex_b, 16)).bit_count()
    except Exception:
        return 64


class ImageDedupeRegistry:
    """Sổ kiểm soát chống lặp ảnh trong cùng 1 video và giữa các video/tập khác nhau."""

    def __init__(self, history_path: Path = IMAGE_HISTORY_PATH, check_global_history: bool = True):
        self.history_path = history_path
        self.check_global_history = check_global_history
        self.session_urls: set[str] = set()
        self.session_md5s: set[str] = set()
        self.session_dhashes: list[str] = []
        self.history_entries: list[dict[str, Any]] = []
        self._load_history()

    def _load_history(self) -> None:
        if self.history_path.exists():
            try:
                data = json.loads(self.history_path.read_text(encoding="utf-8"))
                if isinstance(data, list):
                    self.history_entries = data
                elif isinstance(data, dict):
                    self.history_entries = data.get("entries", [])
            except Exception:
                self.history_entries = []

    def _save_history(self) -> None:
        try:
            self.history_path.parent.mkdir(parents=True, exist_ok=True)
            trimmed = self.history_entries[-500:]
            self.history_path.write_text(
                json.dumps({"entries": trimmed}, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except Exception as exc:
            print(f"[DEDUPE WARN] Không lưu được lịch sử ảnh: {exc}")

    def is_url_used(self, url: str) -> Tuple[bool, str]:
        norm = url.strip().lower()
        if norm in self.session_urls:
            return True, "trùng URL trong cùng dự án"
        if self.check_global_history:
            for e in self.history_entries:
                if str(e.get("url", "")).strip().lower() == norm:
                    return True, f"đã dùng ở tập cũ ({e.get('project', 'unknown')})"
        return False, ""

    def is_image_duplicate(self, md5_hex: str, dhash_hex: str, max_hamming: int = 6) -> Tuple[bool, str]:
        if md5_hex in self.session_md5s:
            return True, "trùng MD5 tuyệt đối trong cùng dự án"
        for h in self.session_dhashes:
            if _dhash_hamming(dhash_hex, h) <= max_hamming:
                return True, "ảnh gần giống/trùng nội dung (dHash) trong cùng dự án"
        if self.check_global_history:
            for e in self.history_entries:
                if e.get("md5") == md5_hex:
                    return True, f"trùng MD5 với tập cũ ({e.get('project', 'unknown')})"
                eh = str(e.get("dhash", ""))
                if eh and _dhash_hamming(dhash_hex, eh) <= max_hamming:
                    return True, f"ảnh trùng nội dung (dHash) với tập cũ ({e.get('project', 'unknown')})"
        return False, ""

    def register(self, url: str, md5_hex: str, dhash_hex: str, project_name: str, entity_id: str) -> None:
        norm = url.strip().lower()
        self.session_urls.add(norm)
        self.session_md5s.add(md5_hex)
        self.session_dhashes.append(dhash_hex)
        self.history_entries.append({
            "date": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "project": project_name,
            "entity_id": entity_id,
            "url": url,
            "md5": md5_hex,
            "dhash": dhash_hex,
        })
        self._save_history()


# =============================================================================
# 7B. TẢI VÀ DUYỆT ẢNH THẬT QUA MẮT THẦN + CHỐNG TRÙNG 100%
# =============================================================================
def remove_background_safe(
    input_png: Path,
    output_png: Path,
    soft_bottom_fade: bool = False,
) -> Path:
    """
    Tách nền chất lượng cao bằng auto_cutout.cutout_image (bria-rmbg, defringe=True,
    edge_feather=0.8, add_rim_light=False); tự động fallback u2net nếu thiếu RAM.
    """
    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    import auto_cutout

    output_png.parent.mkdir(parents=True, exist_ok=True)
    # Chuẩn hóa kích thước ảnh lớn > 1400px vào file tạm để bảo vệ RAM
    work_in = input_png
    scaled_tmp: Optional[Path] = None
    with Image.open(input_png) as orig:
        if max(orig.size) > 1400:
            scale = 1400.0 / max(orig.size)
            resized = orig.convert("RGBA").resize(
                (int(orig.size[0] * scale), int(orig.size[1] * scale)),
                Image.Resampling.LANCZOS,
            )
            scaled_tmp = output_png.with_name(f"tmp_scale_{output_png.name}")
            resized.save(scaled_tmp, format="PNG")
            work_in = scaled_tmp

    try:
        try:
            auto_cutout.cutout_image(
                work_in,
                output_png,
                model_name="bria-rmbg",
                defringe=True,
                edge_feather=0.7,
                add_rim_light=False,
                crop_tight=False,
                soft_bottom_fade=soft_bottom_fade,
            )
        except Exception as exc:
            print(f"[AI CUTOUT WARN] bria-rmbg lỗi ({exc}), fallback sang u2net...")
            auto_cutout.cutout_image(
                work_in,
                output_png,
                model_name="u2net",
                defringe=True,
                edge_feather=0.7,
                add_rim_light=False,
                crop_tight=False,
                soft_bottom_fade=soft_bottom_fade,
            )
    finally:
        if scaled_tmp and scaled_tmp.exists():
            scaled_tmp.unlink(missing_ok=True)

    return output_png


def download_and_verify_image(
    urls: List[str],
    out_path: Path,
    expected_entity: str,
    context_sentence: str = "",
    topic_domain: str = "",
    min_width: int = 600,
    min_height: int = 400,
    dedupe: Optional[ImageDedupeRegistry] = None,
    project_name: str = "",
    entity_id: str = "",
    remove_bg: bool = False,
    final_cutout_path: Optional[Path] = None,
) -> Tuple[Optional[Path], str]:
    """
    Duyệt từng ứng viên: Kiểm trùng URL -> Tải -> Kiểm kích thước & dHash -> Mắt Thần soi.
    Nếu remove_bg=True: chạy tách nền thử + check_cutout_completeness(), tự loại ảnh bị chém cụt mép;
    nếu hết ứng viên mà chỉ còn ảnh bán thân chạm đáy -> tự bật soft_bottom_fade=True + display_mode='framed_or_faded'.
    Trả về: (saved_raw_path_or_None, display_mode).
    """
    import hashlib
    import shutil

    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    import auto_cutout

    tmp_path = out_path.with_name(f"tmp_verify_{out_path.name}")
    tmp_cut_path = out_path.with_name(f"tmp_cut_{out_path.name}")
    fallback_raw_path = out_path.with_name(f"tmp_fb_raw_{out_path.name}")
    fallback_meta: Optional[Tuple[str, str, str]] = None  # (url, md5, dhash)

    for idx, u in enumerate(urls[:20]):
        try:
            if dedupe is not None:
                used, why = dedupe.is_url_used(u)
                if used:
                    print(f"   [Bỏ qua trùng #{idx+1}] {why}: {u[:70]}...")
                    continue

            print(f"   [Soi ứng viên #{idx+1}] Đang tải: {u[:80]}...")
            hdrs = WIKI_HEADERS if "wikimedia.org" in u else HEADERS
            req = urllib.request.Request(u, headers=hdrs)
            with urllib.request.urlopen(req, timeout=12, context=SSL_CTX) as resp:
                raw_bytes = resp.read()

            if len(raw_bytes) < 25000:
                print(f"   [Bỏ qua #{idx+1}] File quá nhẹ ({len(raw_bytes)} bytes < 25KB)")
                continue

            md5_hex = hashlib.md5(raw_bytes).hexdigest()
            with open(tmp_path, "wb") as f:
                f.write(raw_bytes)

            with Image.open(tmp_path) as img:
                w, h = img.size
                if w < min_width or h < min_height:
                    print(f"   [Bỏ qua #{idx+1}] Kích thước {w}x{h} < {min_width}x{min_height}")
                    should_skip = True
                    dhash_hex = ""
                else:
                    should_skip = False
                    dhash_hex = _compute_dhash_hex(img)

            if should_skip:
                tmp_path.unlink(missing_ok=True)
                continue

            if dedupe is not None:
                is_dup, dup_why = dedupe.is_image_duplicate(md5_hex, dhash_hex)
                if is_dup:
                    print(f"   [Bỏ qua trùng ảnh #{idx+1}] {dup_why}")
                    tmp_path.unlink(missing_ok=True)
                    continue

            # SOI MẮT THẦN GEMINI VISION
            matched, reason = verify_candidate_with_vision(
                tmp_path,
                expected_entity=expected_entity,
                context_sentence=context_sentence,
                topic_domain=topic_domain,
            )

            if not matched:
                print(f"   [MẮT THẦN TỪ CHỐI #{idx+1}] {reason}")
                tmp_path.unlink(missing_ok=True)
                continue

            print(f"   [MẮT THẦN DUYỆT OK #{idx+1}] {reason}")

            if remove_bg and final_cutout_path is not None:
                # Chạy tách nền thử và kiểm tra độ nguyên vẹn 4 viền TRƯỚC crop_tight
                remove_background_safe(tmp_path, tmp_cut_path, soft_bottom_fade=False)
                with Image.open(tmp_cut_path) as cut_im:
                    comp = auto_cutout.check_cutout_completeness(cut_im)
                print(
                    f"   [CHECK VIỀN #{idx+1}] top={comp['top_touch']} bottom={comp['bottom_touch']} "
                    f"left={comp['left_touch']} right={comp['right_touch']} area={comp['subject_area_ratio']}"
                )
                if comp["is_chopped"]:
                    if comp["is_bottom_only_touch"] and fallback_meta is None:
                        print(f"   [DỰ PHÒNG CHẠM ĐÁY #{idx+1}] Giữ làm phương án soft_bottom_fade nếu hết ảnh trọn vẹn...")
                        shutil.copy2(tmp_path, fallback_raw_path)
                        fallback_meta = (u, md5_hex, dhash_hex)
                    else:
                        print(f"   [LOẠI CẮT CỤT MÉP #{idx+1}] Vật thể bị chém cụt viền khung -> chuyển ứng viên kế tiếp!")
                    tmp_path.unlink(missing_ok=True)
                    tmp_cut_path.unlink(missing_ok=True)
                    continue

                # Ảnh nguyên vẹn 4 cạnh! Lưu luôn bản raw và bản cutout sạch
                out_path.parent.mkdir(parents=True, exist_ok=True)
                final_cutout_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(tmp_path, out_path)
                shutil.copy2(tmp_cut_path, final_cutout_path)
                tmp_path.unlink(missing_ok=True)
                tmp_cut_path.unlink(missing_ok=True)
                fallback_raw_path.unlink(missing_ok=True)
                if dedupe is not None:
                    dedupe.register(u, md5_hex, dhash_hex, project_name or out_path.parent.parent.parent.name, entity_id or out_path.stem)
                return out_path, "cutout_clean"

            # Không tách nền (ảnh bối cảnh bg_*)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(tmp_path, out_path)
            tmp_path.unlink(missing_ok=True)
            if dedupe is not None:
                dedupe.register(u, md5_hex, dhash_hex, project_name or out_path.parent.parent.parent.name, entity_id or out_path.stem)
            return out_path, "full_backdrop"

        except Exception as exc:
            print(f"   [Lỗi tải ứng viên #{idx+1}] {exc}")
            tmp_path.unlink(missing_ok=True)
            tmp_cut_path.unlink(missing_ok=True)
            continue

    # Nếu hết ứng viên mà có ảnh bán thân chỉ chạm đáy -> tự bật soft_bottom_fade=True
    if remove_bg and final_cutout_path is not None and fallback_meta is not None and fallback_raw_path.exists():
        u, md5_hex, dhash_hex = fallback_meta
        print(f"   [FALLBACK SOFT_BOTTOM_FADE] Áp dụng làm tan mượt 18% cạnh đáy -> {final_cutout_path.name}")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fallback_raw_path, out_path)
        remove_background_safe(out_path, final_cutout_path, soft_bottom_fade=True)
        fallback_raw_path.unlink(missing_ok=True)
        if dedupe is not None:
            dedupe.register(u, md5_hex, dhash_hex, project_name or out_path.parent.parent.parent.name, entity_id or out_path.stem)
        return out_path, "framed_or_faded"

    fallback_raw_path.unlink(missing_ok=True)
    return None, ""


# =============================================================================
# 9. HÀM CÀO CHÍNH THỐNG CHO MỌI THỰC THỂ
# =============================================================================
def harvest_entity_asset(
    entity_id: str,
    search_query: str,
    remove_bg: bool = True,
    target_dir: Path = DEFAULT_HARVEST_DIR,
    context_sentence: str = "",
    topic_domain: str = "",
    dedupe: Optional[ImageDedupeRegistry] = None,
    project_name: str = "",
) -> Dict[str, Any]:
    """
    Quy trình cào dữ liệu chuẩn mực 5 bước:
    1. Kiểm định từ khóa (chặn đứng ẩn dụ trừu tượng & CGI/nhựa giả)
    2. Săn ảnh đa tầng (Tavily Báo chí -> Wikimedia Commons -> Bing HD Clean)
    3. Chống trùng URL + MD5 + dHash + duyệt Mắt Thần Gemini Vision (chỉ duyệt ảnh chụp thật)
    4. Tách nền bria-rmbg + kiểm tra check_cutout_completeness() chống cắt cụt mép
    5. Xuất thông tin chuẩn (gồm display_mode) cho đạo diễn
    """
    validate_harvest_query(search_query, topic_domain=topic_domain)

    target_dir.mkdir(parents=True, exist_ok=True)
    raw_path = target_dir / f"{entity_id}_raw.png"
    final_path = target_dir / f"{entity_id}.png"

    print(f"\n========================================================")
    print(f"[*] SĂN TƯ LIỆU CHO [{entity_id}]: '{search_query}'")
    print(f"[*] Bối cảnh câu thoại: '{context_sentence}'")
    if topic_domain:
        print(f"[*] Miền chủ đề dự án: '{topic_domain}'")
    print(f"========================================================")

    # 1. Gom ứng viên từ 3 tầng nguồn sạch
    tavily_urls = search_tavily_editorial_images(search_query, max_urls=8)
    wiki_urls = search_wikimedia_commons(search_query, max_urls=6)
    bing_urls = search_bing_hd_clean(search_query, max_urls=12)

    candidate_urls = tavily_urls + wiki_urls + bing_urls
    print(f"[*] Tìm thấy {len(candidate_urls)} ứng viên tiềm năng (Tavily: {len(tavily_urls)}, Wiki: {len(wiki_urls)}, Bing: {len(bing_urls)})")

    downloaded, display_mode = download_and_verify_image(
        candidate_urls,
        raw_path,
        expected_entity=search_query,
        context_sentence=context_sentence,
        topic_domain=topic_domain,
        dedupe=dedupe,
        project_name=project_name,
        entity_id=entity_id,
        remove_bg=remove_bg,
        final_cutout_path=final_path if remove_bg else None,
    )

    if not downloaded or not downloaded.exists():
        raise RuntimeError(f"Mắt Thần/Kiểm tra viền từ chối toàn bộ ứng viên cho: '{search_query}'. Không có ảnh nào đạt chuẩn!")

    if not remove_bg:
        import shutil
        shutil.copy2(raw_path, final_path)

    with Image.open(final_path) as fin_im:
        fw, fh = fin_im.size
    if abs(fw - fh) <= max(fw, fh) * 0.08:
        orient = "square"
    elif fw > fh:
        orient = "landscape"
    else:
        orient = "portrait"

    return {
        "entity_id": entity_id,
        "query": search_query,
        "remove_bg": remove_bg,
        "display_mode": display_mode,
        "width": fw,
        "height": fh,
        "orientation": orient,
        "public_path": f"harvested/{final_path.name}",
        "abs_path": str(final_path),
    }


# =============================================================================
# 10. TẠO ẢNH TIẾP XÚC (CONTACT SHEET) KIỂM ĐỊNH TOÀN BỘ TƯ LIỆU BẰNG MẮT
# =============================================================================
def generate_assets_contact_sheet(
    assets_dir: Path,
    output_path: Path,
    title: str = "TỔNG THANH TRA TƯ LIỆU THỰC TẾ (HADA WHY)",
) -> Path:
    """
    Ghép toàn bộ file ảnh thành 1 contact sheet lưới 3 cột,
    có nhãn kích thước, tên file rõ ràng để Con Tổng soi trực tiếp.
    """
    image_files = sorted(
        [p for p in assets_dir.glob("*.png") if not p.name.endswith("_raw.png")] +
        [p for p in assets_dir.glob("*.jpg") if not p.name.endswith("_raw.jpg")]
    )

    if not image_files:
        raise ValueError(f"Không có ảnh nào trong thư mục: {assets_dir}")

    cols = 3
    rows = (len(image_files) + cols - 1) // cols
    cell_w, cell_h = 500, 360
    header_h = 100
    sheet_w = cols * cell_w + 40
    sheet_h = rows * cell_h + header_h + 30

    sheet = Image.new("RGB", (sheet_w, sheet_h), color=(15, 18, 24))
    draw = ImageDraw.Draw(sheet)

    # Tiêu đề Header
    draw.text((30, 25), title, fill=(255, 230, 0))
    draw.text((30, 60), f"Tổng cộng: {len(image_files)} tư liệu | Thư mục: {assets_dir.name}", fill=(180, 200, 220))

    for idx, fpath in enumerate(image_files):
        r = idx // cols
        c = idx % cols
        x0 = 20 + c * cell_w + 10
        y0 = header_h + r * cell_h + 10

        # Khung viền
        draw.rectangle([x0, y0, x0 + cell_w - 20, y0 + cell_h - 20], fill=(24, 28, 38), outline=(50, 60, 80))

        try:
            with Image.open(fpath) as im:
                im_w, im_h = im.size
                thumb = im.convert("RGBA")
                thumb.thumbnail((cell_w - 40, cell_h - 80), Image.Resampling.LANCZOS)
                tw, th = thumb.size

                # Paste thumb ở giữa
                px = x0 + (cell_w - 20 - tw) // 2
                py = y0 + 10 + (cell_h - 80 - th) // 2
                sheet.paste(thumb, (px, py), mask=thumb.split()[3] if len(thumb.split()) == 4 else None)

                # Nhãn file & kích thước
                label = f"#{idx+1}: {fpath.name}"
                info = f"{im_w}x{im_h} | {fpath.stat().st_size // 1024}KB"
                draw.text((x0 + 10, y0 + cell_h - 55), label[:35], fill=(255, 255, 255))
                draw.text((x0 + 10, y0 + cell_h - 35), info, fill=(0, 229, 255))
        except Exception as e:
            draw.text((x0 + 10, y0 + 50), f"Lỗi đọc ảnh: {e}", fill=(255, 80, 80))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path, quality=92)
    print(f"[CONTACT SHEET OK] Đã tạo ảnh lưới kiểm định: {output_path} ({sheet_w}x{sheet_h})")
    return output_path


def purge_harvested_folder(target_dir: Path = DEFAULT_HARVEST_DIR) -> None:
    """Làm sạch thư mục assets dự án trước khi cào mới."""
    if target_dir.exists():
        for p in target_dir.glob("*"):
            if p.is_file():
                p.unlink(missing_ok=True)
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"[ZERO-CARRYOVER OK] Đã dọn sạch: {target_dir}")


# =============================================================================
# 11. TỰ ĐỘNG ĐỌC KỊCH BẢN -> BÓC TÁCH THỰC THỂ KHỚP ĐÚNG LỜI ĐỌC (SCRIPT-TO-PLAN)
# =============================================================================
def build_harvest_plan_from_script(script_path: Path, output_plan_path: Path) -> Dict[str, Any]:
    """
    Đọc script_5beat.json (hoặc .txt), dùng Gemini bóc tách từng nhịp/câu thoại
    thành danh sách tư liệu ĐỜI THẬT/CÔNG NGHỆ khớp chính xác 1-1 với những thứ cần hiện ra:
    - KHÔNG lặp ảnh giữa các cảnh (mỗi cảnh có bg_* và/hoặc 3d_* riêng biệt).
    - Gắn đúng voice_anchor_quote (cụm từ trong lời đọc) + context_sentence (nguyên câu thoại).
    - Cấm tuyệt đối ẩn dụ trừu tượng vô nghĩa.
    """
    raw_script = script_path.read_text(encoding="utf-8").strip()
    try:
        from gemini_utils import generate_content_resilient
    except Exception as exc:
        raise RuntimeError(f"Không thể import gemini_utils để phân tích kịch bản: {exc}")

    prompt = f"""Bạn là Đạo diễn Hình ảnh & Trinh sát Tư liệu của kênh FB Reels HaDa Why.
Hãy đọc kỹ kịch bản sau và lập kế hoạch cào ảnh JSON (`harvest_plan.json`) khớp CHÍNH XÁC TỪNG CÂU LỜI ĐỌC.

KỊCH BẢN GỐC:
{raw_script[:6000]}

YÊU CẦU BẮT BUỘC:
1. Chỉ chọn những thực thể HỮU HÌNH, ĐỜI THẬT hoặc CÔNG NGHỆ THẬT được nhắc trực tiếp trong lời đọc (nhân vật thật, địa điểm thật, hiện trường thật, giao diện app/báo cáo thật, thiết bị/máy chủ/bản đồ thật).
2. CẤM TUYỆT ĐỐI ẩn dụ trừu tượng vô nghĩa (cân công lý, não hoạt hình, bàn tay bắt tay, chai nước hoa, icon nhựa, bảng ăn kiêng).
3. CHỐNG LẶP ẢNH: Mỗi cảnh (`scene_id`) phải có `entity_id` và `search_query` RIÊNG BIỆT. Tạo đủ cả:
   - Ảnh nền hiện trường (`entity_id` bắt đầu bằng `bg_`, `remove_bg`: false) — mỗi nhịp/bối cảnh 1 ảnh khác nhau.
   - Chủ thể nổi khối (`entity_id` bắt đầu bằng `3d_`, `remove_bg`: true) — khớp chính xác danh từ chính trong từng câu thoại.
4. `voice_anchor_quote`: trích ĐÚNG 2-5 từ có thật trong câu thoại khi hình này phải xuất hiện.
5. `context_sentence`: trích nguyên câu thoại tương ứng để Mắt Thần Gemini Vision đối chiếu.
6. `search_query`: viết cực kỳ cụ thể (tiếng Việt cho sự kiện/địa điểm VN, tiếng Anh cho công nghệ/quốc tế) để tìm ra ảnh chụp thật HD, không watermark.
7. Tổng cộng khoảng 7–12 tư liệu chất lượng cao phủ trọn các nhịp kịch bản.

TRẢ VỀ DUY NHẤT JSON HỢP LỆ (không markdown, không giải thích ngoài JSON):
{{
  "topic_domain": "mô tả ngắn miền chủ đề video",
  "assets": [
    {{
      "scene_id": "scene_1",
      "entity_id": "bg_ten_khong_dau",
      "voice_anchor_quote": "cụm từ chính xác trong lời đọc",
      "search_query": "từ khóa tìm ảnh thật cực sát",
      "remove_bg": false,
      "context_sentence": "Nguyên câu thoại tương ứng trong kịch bản"
    }}
  ]
}}"""

    resp_text = generate_content_resilient(prompt)
    if not resp_text:
        raise RuntimeError("Gemini không phản hồi khi phân tích kịch bản để lập harvest_plan.json.")

    cleaned = resp_text.strip()
    m = re.search(r"\{[\s\S]*\}", cleaned)
    if not m:
        raise ValueError(f"Gemini không trả về JSON hợp lệ:\n{cleaned[:400]}")

    plan = json.loads(m.group(0))
    topic_domain = str(plan.get("topic_domain", "") or "").strip()
    raw_assets = plan.get("assets") or []

    # Chuẩn hóa, khử trùng entity_id và kiểm tra cấm ẩn dụ trừu tượng
    seen_ids: set[str] = set()
    clean_assets: List[Dict[str, Any]] = []
    for idx, item in enumerate(raw_assets, 1):
        eid = re.sub(r"[^a-z0-9_]", "_", str(item.get("entity_id", f"asset_{idx}")).lower()).strip("_")
        if not eid:
            eid = f"asset_{idx}"
        base_eid = eid
        c = 2
        while eid in seen_ids:
            eid = f"{base_eid}_{c}"
            c += 1
        seen_ids.add(eid)

        sq = str(item.get("search_query", "")).strip()
        if not sq:
            continue
        validate_harvest_query(sq, topic_domain=topic_domain)
        clean_assets.append({
            "scene_id": str(item.get("scene_id", f"scene_{idx}")),
            "entity_id": eid,
            "voice_anchor_quote": str(item.get("voice_anchor_quote", "")).strip(),
            "search_query": sq,
            "remove_bg": bool(item.get("remove_bg", not eid.startswith("bg_"))),
            "context_sentence": str(item.get("context_sentence", "")).strip(),
        })

    if not clean_assets:
        raise ValueError("Không trích xuất được thực thể hợp lệ nào từ kịch bản.")

    final_plan = {"topic_domain": topic_domain, "assets": clean_assets}
    output_plan_path.parent.mkdir(parents=True, exist_ok=True)
    output_plan_path.write_text(json.dumps(final_plan, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[SCRIPT->PLAN OK] Đã bóc tách {len(clean_assets)} thực thể khớp lời đọc -> {output_plan_path}")
    return final_plan


# =============================================================================
# 12. CHẾ ĐỘ 6 ỨNG VIÊN SOI 1 LẦN (A..F, >= 700px, MUST_SHOW & REJECT)
# =============================================================================
def _extract_item_queries(item: Dict[str, Any]) -> List[str]:
    """Đọc mảng search_queries (2-3 từ khóa) hoặc fallback search_query đơn."""
    qs: List[str] = []
    raw_qs = item.get("search_queries")
    if isinstance(raw_qs, list):
        qs.extend(str(q).strip() for q in raw_qs if str(q).strip())
    single_q = str(item.get("search_query", "") or "").strip()
    if single_q and single_q not in qs:
        qs.append(single_q)
    return qs


def _compute_orientation(w: int, h: int) -> str:
    if abs(w - h) <= max(w, h) * 0.08:
        return "square"
    return "landscape" if w > h else "portrait"


VALID_ASSET_ROLES = {"prop_3d", "avatar_node", "ev_card"}


def _normalize_asset_role(item: Dict[str, Any]) -> str:
    """Chuẩn hóa asset_role thuộc 1 trong 3 vai trò: prop_3d | avatar_node | ev_card."""
    raw_role = str(item.get("asset_role") or "").strip().lower()
    if raw_role in VALID_ASSET_ROLES:
        return raw_role
    eid = str(item.get("entity_id") or "").strip().lower()
    if eid.startswith("avatar"):
        return "avatar_node"
    if bool(item.get("remove_bg", False)) or eid.startswith("prop"):
        return "prop_3d"
    return "ev_card"


def _role_badge_spec(asset_role: str) -> Tuple[str, Tuple[int, int, int], Tuple[int, int, int]]:
    """Trả về (nhãn vai trò, màu nền badge, màu chữ/viền badge) để in lên candidates_sheet.jpg."""
    if asset_role == "prop_3d":
        return "[PROP 3D]", (64, 42, 6), (255, 204, 30)
    if asset_role == "avatar_node":
        return "[AVATAR]", (8, 48, 66), (34, 211, 238)
    return "[EVIDENCE]", (14, 52, 34), (110, 235, 155)


def search_ddg_hd_clean(query: str, max_urls: int = 10, min_dim: int = 700) -> List[str]:
    """Tìm ảnh độ phân giải cao (>= 700px) trên DuckDuckGo Images (nếu có ddgs/duckduckgo_search), lọc sạch spam."""
    urls: List[str] = []
    DDGS_cls = None
    try:
        from ddgs import DDGS as DDGS_cls  # type: ignore
    except Exception:
        try:
            from duckduckgo_search import DDGS as DDGS_cls  # type: ignore
        except Exception:
            DDGS_cls = None
    if DDGS_cls is None:
        return urls
    try:
        with DDGS_cls() as ddgs:
            results = ddgs.images(query, size="Large", type_image="photo", max_results=max_urls * 2)
            for r in results or []:
                u = str(r.get("image") or "").strip()
                w = int(r.get("width") or 0)
                h = int(r.get("height") or 0)
                if not u or is_banned_url(u):
                    continue
                if (w and h) and (max(w, h) < min_dim or min(w, h) < 400):
                    continue
                urls.append(u)
                if len(urls) >= max_urls:
                    break
    except Exception:
        pass
    return urls


def _crop_avatar_top_weighted(im: Image.Image) -> Image.Image:
    """
    Tự động nhận diện vùng đầu/mặt phía trên (Haar Cascade + fallback top-weighted crop)
    để giữ trọn khoảng thở trên đỉnh đầu & trán cho avatar_node, tuyệt đối không xén mất đỉnh đầu hay trán.
    """
    rgb = im.convert("RGB")
    w, h = rgb.size
    if w < 64 or h < 64:
        return rgb

    face_box: Optional[Tuple[int, int, int, int]] = None
    try:
        import cv2
        gray = np.array(rgb.convert("L"), dtype=np.uint8)
        cascade_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        if os.path.exists(cascade_path):
            detector = cv2.CascadeClassifier(cascade_path)
            faces = detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(max(36, min(w, h) // 10), max(36, min(w, h) // 10)),
            )
            if len(faces) > 0:
                # Ưu tiên khuôn mặt lớn nằm ở 75% nửa trên khung hình
                upper_faces = [f for f in faces if (f[1] + f[3] * 0.5) <= h * 0.78]
                cand_faces = upper_faces if upper_faces else list(faces)
                cand_faces.sort(key=lambda b: int(b[2]) * int(b[3]), reverse=True)
                fx, fy, fw, fh = [int(v) for v in cand_faces[0]]
                face_box = (fx, fy, fw, fh)
    except Exception:
        face_box = None

    side = min(w, h)
    if face_box is not None:
        fx, fy, fw, fh = face_box
        # Mở khung rộng ~2.4x bề ngang mặt để ôm trọn vai + khoảng thở trên đỉnh đầu
        crop_side = max(min(side, int(fw * 2.5)), min(side, int(min(w, h) * 0.72)))
        cx = fx + fw // 2
        # Đặt tâm mắt/trán ở ~34% từ mép trên xuống -> chừa đầy đủ tóc và đỉnh đầu
        ideal_y0 = fy - int(fh * 0.68)
        x0 = max(0, min(w - crop_side, cx - crop_side // 2))
        y0 = max(0, min(h - crop_side, ideal_y0))
        return rgb.crop((x0, y0, x0 + crop_side, y0 + crop_side))

    # Fallback Top-Weighted Crop: bám sát phần trên khung hình (chỉ lùi 4% nếu ảnh dọc, 0% nếu ảnh ngang)
    if h >= w:
        x0 = 0
        y0 = max(0, min(h - side, int((h - side) * 0.04)))
    else:
        x0 = (w - side) // 2
        y0 = 0
    return rgb.crop((x0, y0, x0 + side, y0 + side))


def _gather_candidates_by_hint(
    search_queries: List[str],
    source_hint: str = "auto",
    asset_role: str = "ev_card",
) -> List[str]:
    """
    Gom ứng viên đa nguồn từ cả 2-3 từ khóa (Wikimedia Commons + Bing/DDG >= 700px + Tavily).
    Nếu asset_role == 'prop_3d': tự động ưu tiên ảnh chụp vật thể rõ nét trên nền sạch.
    """
    hint = (source_hint or "auto").strip().lower()
    merged: List[str] = []
    seen: set[str] = set()

    effective_queries = list(search_queries)
    if asset_role == "prop_3d" and effective_queries:
        clean_mods = ("isolated", "product photography", "close up", "white background", "studio")
        if not any(any(m in q.lower() for m in clean_mods) for q in effective_queries):
            effective_queries.append(f"{effective_queries[0]} isolated close up")

    for sq in effective_queries:
        if asset_role == "prop_3d":
            # Ưu tiên Wikimedia Commons + Bing HD Clean + DDG (>= 700px) cho vật thể 3D nền sạch
            batch = (
                search_wikimedia_commons(sq, max_urls=8)
                + search_bing_hd_clean(sq, max_urls=14)
                + search_ddg_hd_clean(sq, max_urls=8, min_dim=700)
            )
        elif hint == "wikimedia":
            batch = search_wikimedia_commons(sq, max_urls=8) + search_bing_hd_clean(sq, max_urls=10)
        elif hint == "web":
            batch = (
                search_bing_hd_clean(sq, max_urls=12)
                + search_ddg_hd_clean(sq, max_urls=6, min_dim=700)
                + search_tavily_editorial_images(sq, max_urls=5)
                + search_wikimedia_commons(sq, max_urls=4)
            )
        else:
            batch = (
                search_wikimedia_commons(sq, max_urls=6)
                + search_bing_hd_clean(sq, max_urls=12)
                + search_ddg_hd_clean(sq, max_urls=6, min_dim=700)
                + search_tavily_editorial_images(sq, max_urls=5)
            )
        for u in batch:
            if u not in seen:
                seen.add(u)
                merged.append(u)
    return merged


def harvest_candidates_sheet(
    items: List[Dict[str, Any]],
    temp_dir: Path,
    topic_domain: str = "",
    only_ids: Optional[set[str]] = None,
) -> Path:
    """
    Tải 6 ứng viên (A, B, C, D, E, F, >= 700px chiều chính, lọc sạch watermark/CGI/nhạy cảm)
    cho từng thực thể vào temp/candidates/ và ghép temp/candidates_sheet.jpg
    gắn nhãn vai trò [PROP 3D] / [AVATAR] / [EVIDENCE] + entity_id + must_show bên trái từng hàng.
    """
    cand_dir = temp_dir / "candidates"
    cand_dir.mkdir(parents=True, exist_ok=True)
    index_path = cand_dir / "candidates_index.json"
    existing_index: Dict[str, Any] = {}
    if index_path.exists():
        try:
            existing_index = json.loads(index_path.read_text(encoding="utf-8"))
        except Exception:
            existing_index = {}

    letters = ("A", "B", "C", "D", "E", "F")
    dedupe = ImageDedupeRegistry(check_global_history=True)

    for item in items:
        entity_id = str(item["entity_id"]).strip()
        if only_ids and entity_id not in only_ids:
            continue
        queries = _extract_item_queries(item)
        if not queries:
            raise ValueError(f"Mục '{entity_id}' thiếu search_queries / search_query!")
        for sq in queries:
            validate_harvest_query(sq, topic_domain=topic_domain)

        raw_role = str(item.get("asset_role") or "").strip().lower()
        visual_reasoning = str(item.get("visual_reasoning") or "").strip()
        if len(visual_reasoning) < 15 or raw_role not in VALID_ASSET_ROLES:
            raise ValueError(
                f"MISSING_VISUAL_REASONING: Mục '{entity_id}' bắt buộc có 'visual_reasoning' (>= 15 ký tự) "
                f"và 'asset_role' thuộc {{'prop_3d', 'avatar_node', 'ev_card'}} trước khi cào!"
            )
        asset_role = raw_role
        must_show = str(item.get("must_show") or item.get("context_sentence") or item.get("context") or "").strip()
        script_line = str(item.get("script_line") or item.get("context_sentence") or "").strip()
        source_hint = str(item.get("source_hint", "auto") or "auto")
        remove_bg = True if asset_role == "prop_3d" else (False if asset_role == "ev_card" else bool(item.get("remove_bg", False)))

        role_label, _, _ = _role_badge_spec(asset_role)
        print(f"\n[*] TẢI 6 ỨNG VIÊN (A..F) CHO {role_label} [{entity_id}] (hint={source_hint}): {queries}")
        urls = _gather_candidates_by_hint(queries, source_hint=source_hint, asset_role=asset_role)
        saved_slots: Dict[str, Dict[str, Any]] = {}
        slot_idx = 0

        for u in urls[:40]:
            if slot_idx >= 6:
                break
            try:
                used, _ = dedupe.is_url_used(u)
                if used:
                    continue
                hdrs = WIKI_HEADERS if "wikimedia.org" in u else HEADERS
                req = urllib.request.Request(u, headers=hdrs)
                with urllib.request.urlopen(req, timeout=12, context=SSL_CTX) as resp:
                    raw = resp.read()
                if len(raw) < 28000:
                    continue
                import hashlib
                md5_hex = hashlib.md5(raw).hexdigest()
                letter = letters[slot_idx]
                out_jpg = cand_dir / f"{entity_id}_{letter}.jpg"
                with Image.open(io.BytesIO(raw)) as im:
                    w, h = im.size
                    if max(w, h) < 700 or min(w, h) < 400:
                        continue
                    dhash_hex = _compute_dhash_hex(im)
                    is_dup, _ = dedupe.is_image_duplicate(md5_hex, dhash_hex)
                    if is_dup:
                        continue
                    im.convert("RGB").save(out_jpg, format="JPEG", quality=92)
                dedupe.session_urls.add(u.strip().lower())
                dedupe.session_md5s.add(md5_hex)
                dedupe.session_dhashes.append(dhash_hex)
                saved_slots[letter] = {
                    "path": str(out_jpg),
                    "url": u,
                    "width": w,
                    "height": h,
                    "orientation": _compute_orientation(w, h),
                }
                print(f"   [OK {entity_id}:{letter}] {w}x{h} <- {u[:72]}...")
                slot_idx += 1
            except Exception:
                continue

        existing_index[entity_id] = {
            "entity_id": entity_id,
            "asset_role": asset_role,
            "visual_reasoning": visual_reasoning,
            "must_show": must_show,
            "script_line": script_line,
            "voice_anchor_quote": str(item.get("voice_anchor_quote") or "").strip(),
            "search_queries": queries,
            "remove_bg": remove_bg,
            "slots": saved_slots,
        }

    index_path.write_text(json.dumps(existing_index, ensure_ascii=False, indent=2), encoding="utf-8")

    # Ghép lưới lớn temp/candidates_sheet.jpg: cột trái in nổi bật voice_anchor_quote + script_line + must_show
    ordered_ids = [str(it["entity_id"]).strip() for it in items if str(it["entity_id"]).strip() in existing_index]
    info_col_w = 400
    cell_w, cell_h = 340, 312
    top_banner_h = 86
    sheet_w = info_col_w + 6 * cell_w + 40
    sheet_h = top_banner_h + len(ordered_ids) * (cell_h + 16) + 30
    sheet = Image.new("RGB", (sheet_w, max(320, sheet_h)), color=(10, 14, 24))
    draw = ImageDraw.Draw(sheet)

    try:
        font_lg = ImageFont.truetype("arialbd.ttf", 26)
        font_md = ImageFont.truetype("arialbd.ttf", 18)
        font_sm = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font_lg = font_md = font_sm = ImageFont.load_default()

    draw.text((24, 18), f"CANDIDATES SHEET (6 UNG VIEN A..F >= 700px) — {len(ordered_ids)} MUC", fill=(255, 230, 0), font=font_lg)
    draw.text(
        (24, 52),
        "[PROP 3D]: chon vat nguyen ven 4 goc, nen sach | [AVATAR]: ro mat & tran | [EVIDENCE]: giu nguyen khung | Sai y -> REJECT",
        fill=(180, 210, 240),
        font=font_sm,
    )

    for r_idx, eid in enumerate(ordered_ids):
        y0 = top_banner_h + r_idx * (cell_h + 16)
        entry = existing_index[eid]
        role_code = str(entry.get("asset_role") or "ev_card")
        badge_txt, badge_bg, badge_fg = _role_badge_spec(role_code)

        # Cột thông tin bên trái từng hàng: Nhãn vai trò [PROP 3D]/[AVATAR]/[EVIDENCE] + entity_id + must_show
        draw.rectangle([16, y0, 16 + info_col_w - 10, y0 + cell_h - 6], fill=(18, 30, 50), outline=badge_fg, width=2)
        draw.rectangle([24, y0 + 10, 162, y0 + 38], fill=badge_bg, outline=badge_fg, width=2)
        draw.text((32, y0 + 14), badge_txt, fill=badge_fg, font=font_md)
        draw.text((170, y0 + 14), f"#{r_idx+1} {eid}", fill=(255, 255, 255), font=font_md)

        role_guide = (
            "Cat nen 3D: CAM cat goc/che tay"
            if role_code == "prop_3d"
            else ("Node tron: ro mat, du dinh dau" if role_code == "avatar_node" else "The contain: giu 100% khung")
        )
        draw.text((26, y0 + 44), role_guide, fill=badge_fg, font=font_sm)

        # In nổi bật nguyên văn voice_anchor_quote & script_line để đối chiếu thẳng mắt với câu thoại
        anchor_txt = str(entry.get("voice_anchor_quote", "")).strip()
        draw.text((26, y0 + 68), f'NEO THOAI: "{anchor_txt[:34]}"', fill=(255, 230, 0), font=font_md)

        sl_txt = str(entry.get("script_line", "")).strip()
        if sl_txt:
            draw.text((26, y0 + 94), "Cau thoai:", fill=(120, 215, 255), font=font_sm)
            for li in range(0, min(len(sl_txt), 114), 38):
                draw.text((26, y0 + 112 + (li // 38) * 18), sl_txt[li:li + 38], fill=(225, 240, 255), font=font_sm)

        ms_txt = str(entry.get("must_show", "")).strip()
        draw.text((26, y0 + 174), "Must show:", fill=(140, 255, 180), font=font_sm)
        for li in range(0, min(len(ms_txt), 114), 38):
            draw.text((26, y0 + 192 + (li // 38) * 18), ms_txt[li:li + 38], fill=(235, 242, 250), font=font_sm)

        vr_txt = str(entry.get("visual_reasoning", "")).strip()
        if vr_txt:
            draw.text((26, y0 + 252), f"Why: {vr_txt[:36]}", fill=(175, 205, 235), font=font_sm)
            if len(vr_txt) > 36:
                draw.text((26, y0 + 270), vr_txt[36:74], fill=(175, 205, 235), font=font_sm)

        slots = entry.get("slots", {})
        for c_idx, letter in enumerate(letters):
            x0 = 16 + info_col_w + c_idx * cell_w + 4
            draw.rectangle([x0, y0, x0 + cell_w - 10, y0 + cell_h - 6], fill=(16, 22, 34), outline=(55, 75, 105))
            info = slots.get(letter)
            if info and Path(info["path"]).exists():
                try:
                    with Image.open(info["path"]) as im:
                        th = im.convert("RGB")
                        th.thumbnail((cell_w - 22, cell_h - 48), Image.Resampling.LANCZOS)
                        px = x0 + (cell_w - 10 - th.size[0]) // 2
                        py = y0 + 36 + (cell_h - 48 - th.size[1]) // 2
                        sheet.paste(th, (px, py))
                except Exception:
                    pass
                draw.rectangle([x0 + 6, y0 + 6, x0 + 54, y0 + 36], fill=(5, 7, 12), outline=(255, 230, 0), width=2)
                draw.text((x0 + 20, y0 + 7), letter, fill=(255, 230, 0), font=font_lg)
                dim_txt = f"{info.get('width', 0)}x{info.get('height', 0)}"
                draw.rectangle([x0 + 60, y0 + 8, x0 + 185, y0 + 34], fill=(5, 7, 12))
                draw.text((x0 + 66, y0 + 11), dim_txt, fill=(255, 255, 255), font=font_sm)
            else:
                draw.text((x0 + 85, y0 + 120), f"{letter}: TRONG", fill=(255, 90, 90), font=font_md)

    sheet_out = temp_dir / "candidates_sheet.jpg"
    sheet.save(sheet_out, quality=90)
    print(f"[CANDIDATES SHEET 6-SLOTS OK] Đã xuất 1 ảnh lưới duy nhất: {sheet_out} ({sheet_w}x{sheet_h})")
    return sheet_out


def select_candidates_to_assets(
    select_spec: str,
    items: List[Dict[str, Any]],
    temp_dir: Path,
    topic_domain: str = "",
) -> Path:
    """
    Chốt ảnh đã chọn (--select 'ev_01:B,prop_02:E,ev_03:REJECT') theo đúng asset_role:
    - prop_3d: bria-rmbg + defringe_alpha + check_cutout_completeness(); cảnh báo đỏ CUTOUT_CHOPPED_WARNING nếu chạm mép trái/phải/trên > 8%.
    - avatar_node: top-weighted face/head crop giữ trọn đỉnh đầu & trán.
    - ev_card: giữ nguyên 100% khung (remove_bg=False, imageFit='contain').
    """
    import shutil

    if str(ENGINE_DIR) not in sys.path:
        sys.path.insert(0, str(ENGINE_DIR))
    import auto_cutout

    cand_dir = temp_dir / "candidates"
    index_path = cand_dir / "candidates_index.json"
    if not index_path.exists():
        raise FileNotFoundError(f"Chưa chạy --candidates! Không thấy {index_path}")
    cand_index = json.loads(index_path.read_text(encoding="utf-8"))

    choices: Dict[str, str] = {}
    rejected_ids: List[str] = []
    for pair in select_spec.split(","):
        if ":" not in pair:
            continue
        k, v = pair.split(":", 1)
        eid_k = k.strip()
        val_v = v.strip().upper()
        if val_v == "REJECT":
            rejected_ids.append(eid_k)
        else:
            choices[eid_k] = val_v

    if rejected_ids:
        rej_csv = ",".join(rejected_ids)
        raise RuntimeError(
            f"[REJECT DETECTED] Các mục chưa đạt yêu cầu must_show: {rej_csv}. "
            f"CẤM chọn bừa ảnh lệch ý! Hãy đổi search_queries trong harvest_plan.json rồi chạy lại: "
            f"--candidates --only {rej_csv}"
        )

    assets_dir = temp_dir / "assets"
    purge_harvested_folder(assets_dir)
    manifest_assets: List[Dict[str, Any]] = []
    dedupe = ImageDedupeRegistry(check_global_history=True)
    project_name = temp_dir.parent.name

    for item in items:
        eid = str(item["entity_id"]).strip()
        if eid not in choices:
            continue
        letter = choices[eid]
        slot = cand_index.get(eid, {}).get("slots", {}).get(letter)
        if not slot or not Path(slot["path"]).exists():
            raise FileNotFoundError(f"Không tìm thấy ứng viên {eid}:{letter} trong {cand_dir}")

        src_path = Path(slot["path"])
        raw_path = assets_dir / f"{eid}_raw.png"
        final_path = assets_dir / f"{eid}.png"

        asset_role = _normalize_asset_role(item)
        visual_reasoning = str(item.get("visual_reasoning") or "").strip()
        cutout_chopped_warning = False

        if asset_role == "avatar_node":
            with Image.open(src_path) as im:
                cropped_avatar = _crop_avatar_top_weighted(im)
                cropped_avatar.save(raw_path, format="PNG")
            remove_bg = bool(item.get("remove_bg", False))
            if remove_bg:
                remove_background_safe(raw_path, final_path, soft_bottom_fade=True)
            else:
                shutil.copy2(raw_path, final_path)
            display_mode = "avatar_node_circle"
            print(f"   [AVATAR TOP-WEIGHTED OK] {eid}:{letter} -> giữ trọn vùng đầu/trán phía trên ({final_path.name})")

        elif asset_role == "prop_3d":
            with Image.open(src_path) as im:
                im.convert("RGB").save(raw_path, format="PNG")
            remove_bg = True
            remove_background_safe(raw_path, final_path, soft_bottom_fade=False)
            with Image.open(final_path) as cut_im:
                comp = auto_cutout.check_cutout_completeness(cut_im)

            side_or_top_chopped = (
                comp["left_touch"] > 0.08 or comp["right_touch"] > 0.08 or comp["top_touch"] > 0.08
            )
            if side_or_top_chopped:
                cutout_chopped_warning = True
                display_mode = "chopped_warning_replace"
                print(
                    f"\033[91m[CUTOUT_CHOPPED_WARNING] {eid}:{letter} bị cắt cụt mép trái/phải/trên > 8% "
                    f"(left={comp['left_touch']:.1%}, right={comp['right_touch']:.1%}, top={comp['top_touch']:.1%})! "
                    f"YÊU CẦU ĐỔI ỨNG VIÊN KHÁC nguyên vẹn trên candidates_sheet.jpg "
                    f"(hoặc sửa search_queries & chạy --candidates --only {eid}) thay vì lờ đi!\033[0m"
                )
            elif comp["is_bottom_only_touch"]:
                print(f"   [SOFT BOTTOM FADE] {eid}:{letter} chạm nhẹ đáy ({comp['bottom_touch']:.1%}) -> bật soft_bottom_fade=True")
                remove_background_safe(raw_path, final_path, soft_bottom_fade=True)
                display_mode = "prop_3d_bottom_faded"
            else:
                display_mode = "prop_3d_clean"

        else:
            # ev_card: giữ nguyên 100% khung hình gốc (imageFit="contain", không tách nền)
            with Image.open(src_path) as im:
                im.convert("RGB").save(raw_path, format="PNG")
            remove_bg = False
            shutil.copy2(raw_path, final_path)
            display_mode = "ev_card_contain"

        with Image.open(final_path) as fin_im:
            fw, fh = fin_im.size
            try:
                fin_dhash = _compute_dhash_hex(fin_im)
            except Exception:
                fin_dhash = ""
        try:
            src_bytes = src_path.read_bytes()
            src_md5 = hashlib.md5(src_bytes).hexdigest()
            src_url = str(slot.get("url") or slot.get("source_url") or src_path.name)
            dedupe.register(
                url=src_url,
                md5_hex=src_md5,
                dhash_hex=fin_dhash,
                project_name=project_name,
                entity_id=eid,
            )
        except Exception as exc:
            print(f"   [DEDUPE WARN] Không ghi được lịch sử cho {eid}: {exc}")

        queries = _extract_item_queries(item)
        manifest_assets.append({
            "entity_id": eid,
            "asset_role": asset_role,
            "visual_reasoning": visual_reasoning,
            "selected_candidate": letter,
            "search_queries": queries,
            "must_show": str(item.get("must_show") or ""),
            "script_line": str(item.get("script_line") or item.get("context_sentence") or item.get("context") or ""),
            "voice_anchor_quote": str(item.get("voice_anchor_quote") or ""),
            "remove_bg": remove_bg,
            "display_mode": display_mode,
            "cutout_chopped_warning": cutout_chopped_warning,
            "width": fw,
            "height": fh,
            "orientation": _compute_orientation(fw, fh),
            "public_path": f"harvested/{final_path.name}",
            "abs_path": str(final_path),
        })

    manifest_out = temp_dir / "asset_manifest.json"
    manifest_out.write_text(
        json.dumps({"topic_domain": topic_domain, "count": len(manifest_assets), "assets": manifest_assets}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    sheet_out = temp_dir / "assets_contact_sheet.jpg"
    generate_assets_contact_sheet(assets_dir, sheet_out)
    print(f"[SELECT OK] Đã chốt {len(manifest_assets)} tư liệu sạch (kèm width/height/orientation) -> {manifest_out}")
    return sheet_out


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="Bộ cào tư liệu thật đa tầng + 4 Ứng viên A/B/C/D + Chống trùng dHash/Lịch sử + Tách nền bria-rmbg."
    )
    ap.add_argument("--project", required=True, help="Thư mục dự án WIP (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--candidates", action="store_true", help="Tải 4 ứng viên A/B/C/D cho mỗi mục -> xuất temp/candidates_sheet.jpg")
    ap.add_argument("--only", default="", help="Khi dùng --candidates, chỉ cào lại các entity_id cách nhau dấu phẩy")
    ap.add_argument("--select", default="", help="Chốt ứng viên đã chọn dạng 'ev_01:B,prop_02:A,...' -> tách nền & xuất contact sheet")
    ap.add_argument("--script", help="Đường dẫn script_5beat.json/.txt để tự bóc tách kế hoạch")
    ap.add_argument("--plan-only", action="store_true", help="Khi dùng --script, chỉ xuất temp/harvest_plan.json rồi dừng")
    ap.add_argument("--manifest", help="Đường dẫn file kế hoạch cào JSON có sẵn (VD: temp/harvest_plan.json)")
    ap.add_argument("--contact-sheet", action="store_true", help="Chỉ xuất lại temp/assets_contact_sheet.jpg từ temp/assets/")
    ap.add_argument("--skip-vision", action="store_true", help="Bỏ qua gọi API Gemini Vision (chống 429)")
    ap.add_argument("--allow-history-reuse", action="store_true", help="Cho phép dùng lại ảnh từng dùng ở tập cũ (mặc định: CẤM)")
    args = ap.parse_args()

    if args.skip_vision:
        set_skip_vision(True)
        print("[MODE] --skip-vision ĐANG BẬT (lọc domain rác + độ phân giải + dHash + check_cutout_completeness).")

    project_dir = Path(args.project)
    temp_dir = project_dir / "temp"
    assets_dir = temp_dir / "assets"
    sheet_path = temp_dir / "assets_contact_sheet.jpg"

    if args.contact_sheet:
        generate_assets_contact_sheet(assets_dir, sheet_path)
        return 0

    if args.candidates or args.select:
        if not args.manifest:
            ap.error("Cần truyền --manifest <temp/harvest_plan.json> khi dùng --candidates hoặc --select.")
        plan_path = Path(args.manifest)
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        topic_domain = "" if isinstance(plan, list) else str(plan.get("topic_domain", "") or "")
        items = plan if isinstance(plan, list) else (plan.get("assets") or plan.get("items") or plan.get("entities") or [])
        if args.candidates:
            only_ids = {x.strip() for x in args.only.split(",") if x.strip()} if args.only else None
            harvest_candidates_sheet(items, temp_dir, topic_domain=topic_domain, only_ids=only_ids)
            return 0
        select_candidates_to_assets(args.select, items, temp_dir, topic_domain=topic_domain)
        return 0

    plan_path: Optional[Path] = None
    if args.script:
        script_path = Path(args.script)
        if not script_path.exists():
            raise FileNotFoundError(f"Không tìm thấy kịch bản: {script_path}")
        plan_path = temp_dir / "harvest_plan.json"
        build_harvest_plan_from_script(script_path, plan_path)
        if args.plan_only:
            print(f"[PLAN-ONLY] Đã dừng sau khi xuất kế hoạch tại: {plan_path}")
            return 0
    elif args.manifest:
        plan_path = Path(args.manifest)
        if not plan_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file kế hoạch cào: {plan_path}")
    else:
        ap.error("Cần truyền --script <path>, --manifest <path>, hoặc --contact-sheet.")

    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    if isinstance(plan, list):
        topic_domain = ""
        items = plan
    else:
        topic_domain = str(plan.get("topic_domain", "") or "")
        items = plan.get("assets") or plan.get("items") or plan.get("entities") or []

    if not items:
        raise ValueError(f"Danh sách tài nguyên trong {plan_path} đang rỗng!")

    purge_harvested_folder(assets_dir)
    dedupe = ImageDedupeRegistry(check_global_history=not args.allow_history_reuse)
    project_name = project_dir.name

    harvested_manifest: List[Dict[str, Any]] = []
    for item in items:
        entity_id = str(item["entity_id"]).strip()
        search_query = str(item["search_query"]).strip()
        remove_bg = bool(item.get("remove_bg", True))
        context_sentence = str(item.get("context_sentence") or item.get("context") or "")

        res = harvest_entity_asset(
            entity_id=entity_id,
            search_query=search_query,
            remove_bg=remove_bg,
            target_dir=assets_dir,
            context_sentence=context_sentence,
            topic_domain=topic_domain,
            dedupe=dedupe,
            project_name=project_name,
        )
        res["context_sentence"] = context_sentence
        if item.get("scene_id"):
            res["scene_id"] = item["scene_id"]
        if item.get("voice_anchor_quote"):
            res["voice_anchor_quote"] = item["voice_anchor_quote"]
        harvested_manifest.append(res)

    manifest_out = temp_dir / "asset_manifest.json"
    manifest_out.write_text(
        json.dumps(
            {
                "topic_domain": topic_domain,
                "count": len(harvested_manifest),
                "assets": harvested_manifest,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[MANIFEST OK] Đã xuất: {manifest_out} ({len(harvested_manifest)} tư liệu, 0 trùng lặp)")
    generate_assets_contact_sheet(assets_dir, sheet_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
