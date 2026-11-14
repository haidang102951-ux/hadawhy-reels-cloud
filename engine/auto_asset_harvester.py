"""
auto_asset_harvester.py - BỘ CÀO DỮ LIỆU THẬT & TÁCH NỀN TỰ ĐỘNG THEO KỊCH BẢN
(Dành riêng cho Đầu Não Video Ngắn FB: D:\Đầu Não Video Ngắn FB (không xóa))

Chức năng cốt lõi (giống workflow tự động của @lopphovlog & Finpath):
1. Nhận danh sách Thực thể / Sự vật / Sự việc từ kịch bản (kèm mốc giây Whisper).
2. Tự động lên mạng cào ảnh thật độ phân giải cao (Bing Images HD + Wikimedia Commons).
3. Kiểm tra kích thước thật (>= 500px), loại bỏ ảnh lỗi/ảnh thumbnail rác.
4. Tự động chạy AI `bria-rmbg` (qua `auto_cutout.py`) để tách nền 100% thành PNG trong suốt
   hoặc giữ nguyên ảnh báo chí/bối cảnh thật, xuất thẳng vào `remotion_reels/public/harvested/`
   kèm file manifest JSON để Remotion tự động chèn đúng mốc thời gian kịch bản.
"""

import html
import io
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr:
    sys.stderr.reconfigure(encoding="utf-8")

FB_BRAIN_DIR = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
REMOTION_PUBLIC_HARVEST = FB_BRAIN_DIR / "remotion_reels" / "public" / "harvested"
REMOTION_PUBLIC_HARVEST.mkdir(parents=True, exist_ok=True)

AUTO_CUTOUT_SCRIPT = FB_BRAIN_DIR / "engine" / "auto_cutout.py"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
}


WIKI_HEADERS = {
    "User-Agent": "AntigravityBot/1.0 (https://example.org; contact@example.org)"
}


JUNK_URL_PATTERNS = [
    "freepngimg",
    "meme",
    "clipart",
    "emoji",
    "sticker",
    "icon",
    "cartoon",
    "vector",
    "avatar",
]


def search_bing_hd_images(query: str, max_urls: int = 8) -> list[str]:
    """Quét trực tiếp Bing Images để lấy danh sách URL ảnh thật (chặn toàn bộ web meme/clipart rác)."""
    encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/images/search?q={encoded}"
    urls = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            page_html = resp.read().decode("utf-8", errors="ignore")
        matches = re.findall(r'murl&quot;:&quot;(https?://[^&]+?)&quot;', page_html)
        for m in matches:
            clean_url = html.unescape(m)
            low = clean_url.lower()
            if any(junk in low for junk in JUNK_URL_PATTERNS):
                continue
            if any(ext in low for ext in [".jpg", ".jpeg", ".png", ".webp"]):
                if clean_url not in urls:
                    urls.append(clean_url)
            if len(urls) >= max_urls:
                break
    except Exception as e:
        print(f"[HARVESTER WARN] Bing search error for '{query}': {e}")
    return urls


def search_wikimedia_images(query: str, max_urls: int = 5) -> list[str]:
    """Quét Wikimedia Commons API (namespace=6) để lấy ảnh tư liệu thật độ phân giải cao."""
    encoded = urllib.parse.quote(query)
    api_url = (
        f"https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrsearch={encoded}&gsrnamespace=6&gsrlimit={max_urls}"
        f"&prop=imageinfo&iiprop=url|dimensions&format=json"
    )
    urls = []
    try:
        req = urllib.request.Request(api_url, headers=WIKI_HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        pages = data.get("query", {}).get("pages", {})
        for _, page in pages.items():
            infos = page.get("imageinfo", [])
            if infos:
                info = infos[0]
                w = info.get("width", 0)
                h = info.get("height", 0)
                u = info.get("url", "")
                if w >= 500 and h >= 350 and u:
                    urls.append(u)
    except Exception as e:
        print(f"[HARVESTER WARN] Wikimedia search error for '{query}': {e}")
    return urls


def download_valid_image(urls: list[str], out_raw_path: Path, min_width: int = 500) -> Path | None:
    """Tải và kiểm tra nghiêm ngặt độ phân giải ảnh thật bằng PIL."""
    for u in urls:
        try:
            hdrs = WIKI_HEADERS if "wikimedia.org" in u else HEADERS
            req = urllib.request.Request(u, headers=hdrs)
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw_bytes = resp.read()
            img = Image.open(io.BytesIO(raw_bytes))
            w, h = img.size
            if w < min_width or h < 350:
                continue
            img = img.convert("RGBA")
            if max(w, h) > 1400:
                scale = 1400.0 / max(w, h)
                img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
            out_raw_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(out_raw_path, format="PNG")
            print(f"[HARVESTER OK] Đã tải ảnh thật '{out_raw_path.name}' ({img.size[0]}x{img.size[1]}) từ: {u[:85]}")
            return out_raw_path
        except Exception:
            continue
    return None


def remove_background_bria(input_png: Path, output_cutout_png: Path) -> Path:
    """Gọi cutout_image từ auto_cutout.py (bria-rmbg) để tách nền chủ thể thật thành PNG trong suốt."""
    from auto_cutout import cutout_image
    res = cutout_image(
        input_png,
        output_cutout_png,
        model_name="bria-rmbg",
        defringe=True,
        edge_feather=0.8,
        add_rim_light=False,
        add_floor_shadow=False,
        crop_tight=True,
    )
    return Path(res)


def purge_harvested_folder(target_dir: Path = REMOTION_PUBLIC_HARVEST):
    """
    Xóa sạch các ảnh cào của kịch bản cũ trước khi chạy kịch bản mới,
    ngăn chặn tuyệt đối việc râu ông nọ cắm cằm bà kia (dùng nhầm ảnh bài cũ cho bài mới).
    """
    if target_dir.exists():
        for p in target_dir.glob("*"):
            if p.is_file():
                p.unlink(missing_ok=True)
    target_dir.mkdir(parents=True, exist_ok=True)
    print(f"[ZERO-CARRYOVER OK] Đã làm sạch kho ảnh kịch bản cũ tại: {target_dir}")


def harvest_3d_fluent_icon(
    icon_id: str,
    fluent_folder: str,
    fluent_filename: str,
    out_dir: Path = FB_BRAIN_DIR / "remotion_reels" / "public" / "objects",
) -> Path:
    """
    Tải trực tiếp bất kỳ mô hình 3D nào trong kho 1,500+ vật thể 3D của Microsoft Fluent UI Emoji
    theo đúng vật thể mà kịch bản mới nhắc tới (VD: cốc cà phê, thùng dầu, con chip, nhà máy,
    tòa nhà, xe hơi, tên lửa, thỏi vàng, kính lúp, cân công lý, ngọn lửa...).
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    encoded_folder = urllib.parse.quote(fluent_folder)
    url = f"https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/{encoded_folder}/3D/{fluent_filename}_3d.png"
    out_path = out_dir / f"{icon_id}.png"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=12) as resp:
        raw_bytes = resp.read()
    img = Image.open(io.BytesIO(raw_bytes)).convert("RGBA")
    img = img.resize((512, 512), Image.Resampling.LANCZOS)
    img.save(out_path, format="PNG")
    print(f"[3D OBJECT HARVEST OK] Đã nạp mô hình 3D mới '{out_path.name}' (512x512) cho kịch bản!")
    return out_path


def harvest_bespoke_3d_object(
    object_id: str,
    object_query_en: str,
    fluent_fallback: tuple[str, str] | None = None,
    out_dir: Path = FB_BRAIN_DIR / "remotion_reels" / "public" / "objects",
) -> Path:
    """
    Tự động chế tạo Vật Thể 3D Đặc Thù cho kịch bản mới ngay trong Python (KHÔNG đẻ thêm Sub-Agent phụ):
    - Ưu tiên 1: Nếu có trong kho 1,500+ Fluent 3D (`fluent_fallback`), nạp bản 3D chuẩn 512x512.
    - Ưu tiên 2: Tự động săn render 3D / vật thể studio độ phân giải cao từ Bing HD,
      tách nền sạch bằng `bria-rmbg`, tăng độ khối Specular Contrast và chuẩn hóa khung 512x512.
    """
    from PIL import ImageEnhance

    out_dir.mkdir(parents=True, exist_ok=True)
    final_path = out_dir / f"{object_id}.png"

    if fluent_fallback is not None:
        try:
            return harvest_3d_fluent_icon(object_id, fluent_fallback[0], fluent_fallback[1], out_dir=out_dir)
        except Exception as e:
            print(f"[3D FLUENT FALLBACK WARN] Chuyển sang chế tạo 3D đặc thù từ Bing HD ({e})")

    q_3d = f"{object_query_en} 3d render isometric icon isolated studio"
    urls = search_bing_hd_images(q_3d, max_urls=8) + search_bing_hd_images(f"{object_query_en} studio product shot", max_urls=6)
    tmp_raw = out_dir / f"_{object_id}_raw_tmp.png"
    tmp_cut = out_dir / f"_{object_id}_cut_tmp.png"

    downloaded = download_valid_image(urls, tmp_raw, min_width=400)
    if not downloaded:
        raise RuntimeError(f"Không tìm thấy mẫu vật thể 3D cho: {object_query_en}")

    remove_background_bria(tmp_raw, tmp_cut)
    tmp_raw.unlink(missing_ok=True)

    cut_img = Image.open(tmp_cut).convert("RGBA")
    # Tăng nhẹ độ nổi khối 3D Studio
    rgb, alpha = cut_img.convert("RGB"), cut_img.split()[3]
    rgb = ImageEnhance.Contrast(rgb).enhance(1.12)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.20)
    polished = Image.merge("RGBA", (*rgb.split(), alpha))

    # Đặt vào tâm khung vuông 512x512
    canvas = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    scale = min(460.0 / max(1, polished.width), 460.0 / max(1, polished.height))
    new_w, new_h = max(1, int(polished.width * scale)), max(1, int(polished.height * scale))
    resized = polished.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas.paste(resized, ((512 - new_w) // 2, (512 - new_h) // 2), resized)
    canvas.save(final_path, format="PNG")
    tmp_cut.unlink(missing_ok=True)

    print(f"[BESPOKE 3D STUDIO OK] Đã tạo & tách nền vật thể 3D đặc thù '{final_path.name}' (512x512)!")
    return final_path


def harvest_entity_asset(
    entity_id: str,
    search_query: str,
    remove_bg: bool = True,
    target_dir: Path = REMOTION_PUBLIC_HARVEST,
) -> dict:
    """
    Cào tự động 1 thực thể trong kịch bản:
    - Tìm trên Bing HD + Wikimedia Commons
    - Tải ảnh hợp lệ (>= 500px)
    - Tách nền bằng bria-rmbg nếu remove_bg=True
    - Trả về metadata đường dẫn để chèn thẳng vào Remotion
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    raw_path = target_dir / f"{entity_id}_raw.png"
    final_path = target_dir / f"{entity_id}.png"

    print(f"\n[*] Đang cào dữ liệu thật cho thực thể [{entity_id}]: '{search_query}'...")
    urls = search_wikimedia_images(search_query, max_urls=5) + search_bing_hd_images(search_query, max_urls=8)
    downloaded = download_valid_image(urls, raw_path)

    if not downloaded:
        raise RuntimeError(f"Không tìm thấy ảnh hợp lệ cho truy vấn: {search_query}")

    if remove_bg:
        remove_background_bria(raw_path, final_path)
    else:
        raw_path.replace(final_path)

    return {
        "entity_id": entity_id,
        "query": search_query,
        "remove_bg": remove_bg,
        "public_path": f"harvested/{final_path.name}",
        "abs_path": str(final_path),
    }


def harvest_script_manifest(entities: list[dict], out_manifest_json: Path | None = None) -> list[dict]:
    """
    Nhận danh sách thực thể theo mốc kịch bản:
    [
      {"entity_id": "vietjet_plane_real", "query": "Vietjet Air Airbus A321 aircraft", "startSec": 0.0, "endSec": 2.5, "remove_bg": True},
      ...
    ]
    Tự động cào toàn bộ và xuất ra manifest JSON cho Remotion.
    """
    results = []
    for item in entities:
        meta = harvest_entity_asset(
            entity_id=item["entity_id"],
            search_query=item["query"],
            remove_bg=item.get("remove_bg", True),
        )
        meta["startSec"] = item.get("startSec", 0.0)
        meta["endSec"] = item.get("endSec", 5.0)
        meta["label"] = item.get("label", "")
        results.append(meta)

    if out_manifest_json is None:
        out_manifest_json = REMOTION_PUBLIC_HARVEST / "harvested_manifest.json"
    out_manifest_json.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n[MANIFEST OK] Đã xuất manifest dữ liệu thật: {out_manifest_json}")
    return results


if __name__ == "__main__":
    # Test thực chiến với 2 thực thể thật trong kịch bản Vietjet 250M đô
    sample_entities = [
        {
            "entity_id": "vietjet_real_aircraft",
            "query": "VietJet Air Airbus A321",
            "remove_bg": True,
            "startSec": 0.0,
            "endSec": 2.5,
            "label": "TÀU BAY VIETJET",
        },
        {
            "entity_id": "london_high_court_real",
            "query": "Royal Courts of Justice London exterior",
            "remove_bg": False,
            "startSec": 2.5,
            "endSec": 5.0,
            "label": "TÒA ÁN TỐI CAO LONDON",
        },
    ]
    harvest_script_manifest(sample_entities)
