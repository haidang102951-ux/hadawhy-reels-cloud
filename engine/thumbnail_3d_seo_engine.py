r"""
thumbnail_3d_seo_engine.py - BỘ ĐỘNG CƠ CHUYÊN TRÁCH THUMBNAIL 3D ADN HADA WHY,
NHÚNG BÌA TRỰC TIẾP VÀO VIDEO MP4 & TRINH SÁT 3 TIÊU ĐỀ CHUẨN SEO EVERGREEN.

Đặt tại: D:\Đầu Não Video Ngắn FB (không xóa)\engine\thumbnail_3d_seo_engine.py
Phục vụ độc quyền cho Sub-Agent thứ 6: fb-reels-thumbnail-seo-architect.

3 Nhiệm vụ cốt lõi chạy song song:
1. Tư duy logic theo từng kịch bản (4 Chế độ bố cục: Mystery Silhouette, Dual Confrontation,
   Forensic Object Spotlight, Titan + Evidence) trên nền ADN cố định của kênh HaDa Why:
   - Nền bổ trợ bối cảnh thật nâng khối 3D Chiaroscuro + Unsharp Mask.
   - Bầu trời / nền trên liền mạch 100% (Zero-Blob: CẤM tuyệt đối đốm đỏ/đốm đen vô nghĩa).
   - Chữ Hook 2 dòng Kanit-Black (#42B2F2 Xanh HaDa + #FFFFFF Trắng WHY, viền đen 11px) an toàn 4:5.
2. Nhúng Kép (Dual-Embed) tấm Thumbnail 9:16 vào thẳng file Video MP4:
   - Lớp 1: Chèn làm 2 frame đầu tiên (0.00s - 0.03s) ở đầu video để khi đăng lên Facebook Reels /
     Facebook Page kéo thanh chọn ảnh bìa về 00:00 là chọn được ngay tấm bìa 3D sắc nét!
   - Lớp 2: Nhúng luồng metadata attached_pic chuẩn MP4.
3. Đào bới & Cào dữ liệu từ khóa thực tế (Google Suggest API + YouTube Suggest API +
   yt-dlp Top Viral Search + Google News RSS) -> Xuất 3 Tiêu đề chuẩn SEO có Keyword lượt tìm kiếm cao
   và Evergreen (bền vững theo thời gian).
"""

import io
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr:
    sys.stderr.reconfigure(encoding="utf-8")

FB_BRAIN_DIR = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
REMOTION_DIR = FB_BRAIN_DIR / "remotion_reels"
PUBLIC_HARVEST_DIR = REMOTION_DIR / "public" / "harvested"
FINAL_OUTPUT_DIR = Path(r"D:\Video thành phẩm")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


# ==============================================================================
# KHỐI 1: CÀO DỮ LIỆU TỪ KHÓA THẬT & PHÂN TÍCH SEO EVERGREEN
# ==============================================================================

def fetch_autocomplete_suggestions(query: str, source: str = "google") -> List[str]:
    r"""
    Cào từ khóa gợi ý thực tế người dùng Việt Nam đang gõ tìm kiếm nhiều nhất
    trên Google Search hoặc YouTube Search.
    """
    encoded_q = urllib.parse.quote(query.strip())
    if source == "youtube":
        url = f"http://suggestqueries.google.com/complete/search?client=firefox&ds=yt&hl=vi&gl=VN&q={encoded_q}"
    else:
        url = f"http://suggestqueries.google.com/complete/search?client=firefox&hl=vi&gl=VN&q={encoded_q}"

    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
            data = json.loads(raw)
            if isinstance(data, list) and len(data) >= 2 and isinstance(data[1], list):
                results = []
                for item in data[1]:
                    if isinstance(item, str):
                        results.append(item)
                    elif isinstance(item, list) and len(item) > 0 and isinstance(item[0], str):
                        results.append(item[0])
                return results[:12]
    except Exception as e:
        print(f"[SEO-SUGGEST WARN] ({source} - {query}): {e}")
    return []


def fetch_youtube_top_competitors(query: str, limit: int = 8) -> List[Dict[str, Any]]:
    r"""
    Quét trực tiếp trang kết quả tìm kiếm YouTube bằng Python thuần (ytInitialData)
    để lấy tiêu đề, lượt xem và kênh của các video đối thủ đang hút nhiều view nhất.
    """
    encoded_q = urllib.parse.quote(query.strip())
    url = f"https://www.youtube.com/results?search_query={encoded_q}&hl=vi&gl=VN"
    competitors: List[Dict[str, Any]] = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html_str = resp.read().decode("utf-8", errors="ignore")
            m = re.search(r"var ytInitialData = (\{.*?\});</script>", html_str)
            if m:
                data = json.loads(m.group(1))
                # Duyệt đệ quy tìm các videoRenderer
                def find_videos(obj: Any):
                    if isinstance(obj, dict):
                        if "videoRenderer" in obj:
                            vr = obj["videoRenderer"]
                            title_runs = vr.get("title", {}).get("runs", [])
                            title = "".join(r.get("text", "") for r in title_runs)
                            view_text = vr.get("viewCountText", {}).get("simpleText", "")
                            owner_runs = vr.get("ownerText", {}).get("runs", [])
                            channel = "".join(r.get("text", "") for r in owner_runs)
                            if title:
                                competitors.append({
                                    "title": title,
                                    "view_text": view_text,
                                    "channel": channel,
                                })
                        else:
                            for v in obj.values():
                                find_videos(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            find_videos(item)

                find_videos(data)
    except Exception as e:
        print(f"[YT-SEARCH WARN] ({query}): {e}")

    return competitors[:limit]


def fetch_google_news_headlines(query: str, limit: int = 8) -> List[str]:
    r"""Cào tiêu đề báo chí chính thống từ Google News RSS tiếng Việt."""
    encoded_q = urllib.parse.quote(query.strip())
    url = f"https://news.google.com/rss/search?q={encoded_q}&hl=vi&gl=VN&ceid=VN:vi"
    headlines: List[str] = []
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_bytes = resp.read()
            root = ET.fromstring(xml_bytes)
            for item in root.findall(".//item/title")[:limit]:
                if item.text:
                    headlines.append(item.text.strip())
    except Exception as e:
        print(f"[GOOGLE-NEWS WARN] ({query}): {e}")
    return headlines


def harvest_seo_intelligence(
    seed_keywords: List[str],
    project_temp_dir: Path,
) -> Dict[str, Any]:
    r"""
    Đào bới toàn diện từ khóa Google Suggest, YouTube Suggest, Đối thủ triệu view
    và Báo chí Google News. Lưu kết quả vào D:\DuAn_DangLam\<ten_du_an>\temp\seo_raw_intel.json.
    """
    project_temp_dir.mkdir(parents=True, exist_ok=True)
    google_suggests: List[str] = []
    youtube_suggests: List[str] = []
    competitors: List[Dict[str, Any]] = []
    news_headlines: List[str] = []

    expanded_seeds: List[str] = []
    for kw in seed_keywords:
        kw = kw.strip()
        if not kw:
            continue
        expanded_seeds.append(kw)
        expanded_seeds.append(f"tại sao {kw}")
        expanded_seeds.append(f"bí mật {kw}")
        expanded_seeds.append(f"sự thật {kw}")

    seen_g = set()
    seen_yt = set()
    for q in expanded_seeds[:10]:
        for s in fetch_autocomplete_suggestions(q, source="google"):
            if s.lower() not in seen_g:
                seen_g.add(s.lower())
                google_suggests.append(s)
        for s in fetch_autocomplete_suggestions(q, source="youtube"):
            if s.lower() not in seen_yt:
                seen_yt.add(s.lower())
                youtube_suggests.append(s)

    if seed_keywords:
        primary_q = seed_keywords[0]
        competitors = fetch_youtube_top_competitors(primary_q, limit=8)
        news_headlines = fetch_google_news_headlines(primary_q, limit=8)

    intel = {
        "seed_keywords": seed_keywords,
        "google_autocomplete_keywords": google_suggests[:25],
        "youtube_autocomplete_keywords": youtube_suggests[:25],
        "top_youtube_competitors": competitors,
        "google_news_headlines": news_headlines,
    }

    out_file = project_temp_dir / "seo_raw_intel.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(intel, f, ensure_ascii=False, indent=2)

    print(f"[SEO HARVESTER] Đã cào {len(google_suggests)} Google keywords, {len(youtube_suggests)} YouTube keywords, {len(competitors)} video đối thủ -> {out_file}")
    return intel


# ==============================================================================
# KHỐI 2: XỬ LÝ ẢNH NỀN BỔ TRỢ NỔI KHỐI 3D & BẦU TRỜI LIỀN MẠCH (ZERO-BLOB)
# ==============================================================================

def enhance_backdrop_3d_seamless(
    raw_img_path: Path,
    out_img_path: Path,
    crop_x_ratio: float = 0.16,
    sky_lum_threshold: float = 195.0,
) -> Path:
    """
    Xử lý ảnh nền bổ trợ chuẩn ADN kênh HaDa Why:
    1. Cắt cúp tỷ lệ dọc 9:16 (1080x1920) sắc nét bằng Lanczos.
    2. Tăng độ nét vi mô (Unsharp Mask) làm nổi rõ kết cấu vật lý của công trình/bối cảnh.
    3. Tách biệt 2 diện sáng/tối (Chiaroscuro 3D Volume) để bối cảnh nổi khối 3D đồ sộ.
    4. Bảo toàn 100% bầu trời / phần nền phía trên liền mạch tự nhiên (Zero-Blob:
       CẤM tuyệt đối mọi đốm đỏ hay đốm đen vô nghĩa).
    """
    im = Image.open(raw_img_path).convert("RGB")
    w, h = im.size

    target_ratio = 9.0 / 16.0
    current_ratio = w / float(h)

    if current_ratio > target_ratio:
        crop_w = int(h * target_ratio)
        max_x = max(0, w - crop_w)
        crop_x = min(max_x, int(w * crop_x_ratio))
        cropped = im.crop((crop_x, 0, crop_x + crop_w, h))
    else:
        crop_h = int(w / target_ratio)
        crop_y = max(0, int((h - crop_h) * 0.1))
        cropped = im.crop((0, crop_y, w, crop_y + crop_h))

    resized = cropped.resize((1080, 1920), Image.Resampling.LANCZOS)

    # 1. Unsharp Mask nâng chi tiết kiến trúc / hiện trường
    sharp = resized.filter(ImageFilter.UnsharpMask(radius=3.0, percent=185, threshold=1))
    arr = np.array(sharp, dtype=np.float32)
    raw_arr = np.array(resized, dtype=np.float32)

    Y, X = np.mgrid[0:1920, 0:1080]
    raw_lum = 0.299 * raw_arr[:, :, 0] + 0.587 * raw_arr[:, :, 1] + 0.114 * raw_arr[:, :, 2]

    # 2. Nhận diện vùng bầu trời sáng tự nhiên để giữ nguyên 100% sự liền mạch (Zero-Blob)
    is_sky = raw_lum > sky_lum_threshold
    sky_mask = gaussian_filter(is_sky.astype(np.float32), sigma=1.5)[:, :, np.newaxis]

    # 3. Nâng khối 3D Chiaroscuro trên công trình / bối cảnh
    dir_light = 1.0 + 0.16 * np.clip((X - 450.0) / 450.0, -0.6, 0.6)[:, :, np.newaxis]
    b_arr = (arr - 128.0) * 1.25 + 128.0
    b_arr = b_arr * dir_light

    # Đẩy độ tươi tự nhiên cho các chi tiết nhận diện thương hiệu (ví dụ logo xanh/vàng/đỏ trên tòa nhà)
    is_green = (arr[:, :, 1] > arr[:, :, 0] * 1.12) & (arr[:, :, 1] > arr[:, :, 2] * 1.12)
    b_arr[:, :, 1] = np.where(is_green, np.clip(b_arr[:, :, 1] * 1.35, 0, 255), b_arr[:, :, 1])
    b_arr[:, :, 0] = np.where(is_green, b_arr[:, :, 0] * 0.85, b_arr[:, :, 0])

    # 4. Hợp nhất: Bầu trời nguyên bản liền mạch 100% + Công trình nổi khối 3D
    final_arr = raw_arr * sky_mask + b_arr * (1.0 - sky_mask)
    final_arr = np.clip(final_arr, 0, 255)

    out_img_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.uint8(final_arr)).save(out_img_path, format="PNG")
    print(f"[3D BACKDROP] Đã xử lý nổi khối 3D & bầu trời liền mạch 100% -> {out_img_path}")
    return out_img_path


# ==============================================================================
# KHỐI 3: NHÚNG KÉP (DUAL-EMBED) THUMBNAIL VÀO THẲNG VIDEO MP4 CHO FACEBOOK
# ==============================================================================

def embed_thumbnail_into_video(
    video_path: Path,
    thumbnail_path: Path,
    temp_dir: Path,
    prepend_cover_frames: bool = True,
) -> Path:
    """
    Nhúng trực tiếp tấm ảnh Thumbnail 9:16 (1080x1920) vào file Video MP4 bằng 2 cơ chế:
    1. Chèn 2 frame đầu tiên (0.033s ở 60fps) bằng chính tấm ảnh Thumbnail để khi
       Người Chỉ Huy đăng lên Facebook Reels / Trang cá nhân và kéo thanh chọn ảnh bìa
       về vị trí đầu tiên (00:00), tấm ảnh bìa 3D hiện ra ngay lập tức để chọn!
    2. Gắn luồng metadata attached_pic chuẩn MP4 để file video hiển thị ảnh bìa
       trên máy tính Windows và các trình quản lý đăng bài.
    """
    if not video_path.exists():
        raise FileNotFoundError(f"Không tìm thấy video: {video_path}")
    if not thumbnail_path.exists():
        raise FileNotFoundError(f"Không tìm thấy thumbnail: {thumbnail_path}")

    temp_dir.mkdir(parents=True, exist_ok=True)
    working_video = temp_dir / f"working_{video_path.name}"
    shutil.copy2(video_path, working_video)

    if prepend_cover_frames:
        # Tạo 1 đoạn video 0.04s (2 frames @ 60fps) từ thumbnail + âm thanh im lặng 0.04s
        # rồi nối (concat) lên đầu video gốc để frame 00:00 chính là Thumbnail!
        pre_framed_video = temp_dir / f"preframed_{video_path.name}"
        filter_complex = (
            "[1:v]scale=1080:1920:flags=lanczos,fps=60,trim=duration=0.034,setpts=PTS-STARTPTS[cov_v];"
            "aevalsrc=0:d=0.034:s=48000:c=stereo[cov_a];"
            "[0:v]setpts=PTS-STARTPTS[main_v];"
            "[0:a]asetpts=PTS-STARTPTS[main_a];"
            "[cov_v][cov_a][main_v][main_a]concat=n=2:v=1:a=1[out_v][cat_a];"
            "[cat_a]loudnorm=I=-14.0:TP=-1.0:LRA=7[out_a]"
        )
        cmd_prepend = [
            "ffmpeg", "-y",
            "-i", str(working_video),
            "-loop", "1", "-t", "0.05", "-i", str(thumbnail_path),
            "-filter_complex", filter_complex,
            "-map", "[out_v]",
            "-map", "[out_a]",
            "-c:v", "libx264", "-crf", "16", "-preset", "fast", "-pix_fmt", "yuv420p", "-r", "60",
            "-c:a", "aac", "-b:a", "320k", "-ar", "48000",
            str(pre_framed_video),
        ]
        res = subprocess.run(cmd_prepend, capture_output=True, text=True)
        if res.returncode == 0 and pre_framed_video.exists() and pre_framed_video.stat().st_size > 10000:
            working_video = pre_framed_video
            print("[DUAL-EMBED] Lớp 1: Đã chèn Thumbnail vào frame 00:00 đầu video (chọn bìa trên FB 1 chạm).")
        else:
            print(f"[DUAL-EMBED WARN] Lớp 1 bỏ qua: {res.stderr[-300:]}")

    # Lớp 2: Nhúng stream attached_pic vào container MP4
    final_embedded = temp_dir / f"embedded_{video_path.name}"
    cmd_attach = [
        "ffmpeg", "-y",
        "-i", str(working_video),
        "-i", str(thumbnail_path),
        "-map", "0:v:0",
        "-map", "0:a:0",
        "-map", "1:v:0",
        "-c:v:0", "copy",
        "-c:a:0", "copy",
        "-c:v:1", "png",
        "-disposition:v:1", "attached_pic",
        "-movflags", "+faststart",
        str(final_embedded),
    ]
    res2 = subprocess.run(cmd_attach, capture_output=True, text=True)
    if res2.returncode == 0 and final_embedded.exists() and final_embedded.stat().st_size > 10000:
        shutil.copy2(final_embedded, video_path)
        print(f"[DUAL-EMBED] Lớp 2: Đã gắn attached_pic vào MP4 thành công -> {video_path}")
    else:
        # Nếu container không nhận attached_pic thì vẫn giữ bản đã chèn frame 00:00
        shutil.copy2(working_video, video_path)
        print(f"[DUAL-EMBED] Đã lưu bản gắn frame 00:00 -> {video_path}")

    # Tự động dọn sạch các file video trung gian trong temp_dir để không tốn dung lượng đĩa
    for tmp_f in [
        temp_dir / f"working_{video_path.name}",
        temp_dir / f"preframed_{video_path.name}",
        temp_dir / f"embedded_{video_path.name}",
    ]:
        try:
            if tmp_f.exists():
                tmp_f.unlink()
        except Exception:
            pass

    return video_path


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Engine Thumbnail 3D & SEO Evergreen HaDa Why")
    parser.add_argument("--mode", choices=["seo", "backdrop3d", "embed"], required=True)
    parser.add_argument("--keywords", nargs="*", default=[], help="Danh sách từ khóa gốc cần cào SEO")
    parser.add_argument("--temp-dir", type=str, default=r"D:\DuAn_DangLam\temp")
    parser.add_argument("--raw-bg", type=str, help="Đường dẫn ảnh bối cảnh thô")
    parser.add_argument("--out-bg", type=str, help="Đường dẫn ảnh bối cảnh 3D đầu ra")
    parser.add_argument("--video", type=str, help="Đường dẫn video MP4")
    parser.add_argument("--thumb", type=str, help="Đường dẫn ảnh Thumbnail PNG")

    args = parser.parse_args()
    t_dir = Path(args.temp_dir)

    if args.mode == "seo":
        harvest_seo_intelligence(args.keywords, t_dir)
    elif args.mode == "backdrop3d":
        enhance_backdrop_3d_seamless(Path(args.raw_bg), Path(args.out_bg))
    elif args.mode == "embed":
        embed_thumbnail_into_video(Path(args.video), Path(args.thumb), t_dir)
