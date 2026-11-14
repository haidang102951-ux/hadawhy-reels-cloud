"""
cctv_grid_engine.py - Bộ sinh lưới camera an ninh CCTV & Bức tường tin tức quốc tế
Hỗ trợ cả 16:9 (Dài) & 9:16 (Ngắn)
Tính năng:
1. CCTV 4-Cam Grid: Màn hình camera an ninh chia 4 ô với timestamp đếm mili-giây, đèn REC nhấp nháy, vạch quét CRT.
2. International News Wall: Bức tường 3 mặt báo quốc tế (Reuters, Bloomberg, AP) trồi lên từ chiều sâu.
"""

import sys
import os
import math
import random
from pathlib import Path

# Đảm bảo UTF-8 cho Windows console
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path(r"D:\Video thành phẩm")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def get_font(size=18, bold=True):
    font_names = ["consola.ttf", "segoeuib.ttf", "arialbd.ttf"] if bold else ["consolab.ttf", "segoeui.ttf", "arial.ttf"]
    for fn in font_names:
        fp = Path("C:/Windows/Fonts") / fn
        if fp.exists():
            try:
                return ImageFont.truetype(str(fp), size)
            except Exception:
                pass
    return ImageFont.load_default()


def render_cctv_grid_clip(
    cam_labels=None,
    out_video_path: str | Path = None,
    duration: float = 4.0,
    fps: int = 30,
    ratio: str = "16:9"
) -> Path:
    """
    Xuất video lưới camera giám sát an ninh (CCTV Grid):
    - Đèn REC đỏ nhấp nháy.
    - Đồng hồ thời gian thực tế nhảy số mili-giây.
    - Hiệu ứng vạch quét trinh sát CRT & Hạt cảm biến hồng ngoại.
    """
    if cam_labels is None:
        cam_labels = [
            "CAM 01 // CỔNG AN NINH CHÍNH",
            "CAM 02 // TRUNG TÂM DỮ LIỆU SERVER",
            "CAM 03 // HẦM BÍ MẬT KHU B",
            "CAM 04 // PHÒNG HỌP BAN ĐIỀU HÀNH"
        ]

    if ratio == "9:16":
        width, height = 1080, 1920
        # 4 ô xếp chồng dạng 2x2 hoặc 4 tầng
        cols, rows = 2, 2
    else:
        width, height = 1920, 1080
        cols, rows = 2, 2

    if out_video_path is None:
        out_video_path = OUTPUT_DIR / f"cctv_grid_{ratio.replace(':', 'x')}.mp4"
    else:
        out_video_path = Path(out_video_path)

    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))

    w_box = width // cols
    h_box = height // rows

    for f in range(total_frames):
        t = f / fps
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Vẽ từng ô camera
        for i in range(4):
            r = i // cols
            c = i % cols
            x1 = c * w_box
            y1 = r * h_box
            x2 = x1 + w_box
            y2 = y1 + h_box

            # Nền tối xám xanh ánh kim camera giám sát
            cam_tint = (22, 28, 20) if i % 2 == 0 else (28, 24, 22)
            frame[y1:y2, x1:x2] = cam_tint

            # Vạch quét ngang CRT
            scan_y = int((t * 220 + i * 80) % h_box)
            cv2.line(frame, (x1, y1 + scan_y), (x2, y1 + scan_y), (60, 80, 60), 2)

            # Khung viền camera
            cv2.rectangle(frame, (x1 + 4, y1 + 4), (x2 - 4, y2 - 4), (50, 60, 50), 2)
            # Dấu ngắm 4 góc (Crosshairs)
            ch_len = 16
            cv2.line(frame, (x1 + 15, y1 + 15), (x1 + 15 + ch_len, y1 + 15), (100, 140, 100), 2)
            cv2.line(frame, (x1 + 15, y1 + 15), (x1 + 15, y1 + 15 + ch_len), (100, 140, 100), 2)

            # Tên camera
            cv2.putText(frame, cam_labels[i], (x1 + 25, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (160, 200, 160), 2)

            # Đồng hồ góc dưới
            ms = int((t * 100) % 100)
            time_str = f"2024-05-14 02:41:{int(15 + t):02d}:{ms:02d}"
            cv2.putText(frame, time_str, (x1 + 25, y2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 220, 200), 2)

            # Đèn REC nhấp nháy 1Hz
            if int(t * 2) % 2 == 0:
                cv2.circle(frame, (x2 - 80, y1 + 30), 6, (40, 40, 230), -1)
                cv2.putText(frame, "REC", (x2 - 65, y1 + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (60, 60, 240), 2)

        # Phủ nhiễu hạt hồng ngoại toàn khung hình
        noise = np.random.randint(-6, 7, (height, width, 3), dtype=np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)

        out_writer.write(frame)

    out_writer.release()
    print(f"[CCTV OK] CCTV Grid exported ({ratio}): {out_video_path.name}")
    return out_video_path


def render_news_wall_clip(
    headlines=None,
    out_video_path: str | Path = None,
    duration: float = 4.0,
    fps: int = 30,
    ratio: str = "16:9"
) -> Path:
    """
    Xuất video bức tường tin tức quốc tế (International News Wall):
    - 3 mặt báo uy tín (Reuters, Bloomberg, AP) trồi lên từ chiều sâu.
    - Tạo bằng chứng pháp lý và tài chính thuyết phục tuyệt đối.
    """
    if headlines is None:
        headlines = [
            ("REUTERS", "CHÍNH THỨC BAN HÀNH LỆNH CẤM VẬN THIẾT BỊ GIÁM SÁT AN NINH"),
            ("BLOOMBERG", "CỔ PHIẾU CÔNG NGHỆ CHÂU Á BỐC HƠI 18 TỶ USD TRONG 24H"),
            ("THE WALL STREET JOURNAL", "BỘ TƯ PHÁP MỞ RỘNG ĐIỀU TRA ĐẠI ÁN GIAN LẬN THỊ PHẦN")
        ]

    if ratio == "9:16":
        width, height = 1080, 1920
    else:
        width, height = 1920, 1080

    if out_video_path is None:
        out_video_path = OUTPUT_DIR / f"news_wall_{ratio.replace(':', 'x')}.mp4"
    else:
        out_video_path = Path(out_video_path)

    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))

    card_w = int(width * 0.8)
    card_h = int(height * 0.22) if ratio == "9:16" else int(height * 0.24)

    for f in range(total_frames):
        p = f / total_frames

        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (18, 14, 10) # Nền tối

        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)
        font_brand = get_font(22, bold=True)
        font_title = get_font(20, bold=True)

        for i, (brand, title) in enumerate(headlines):
            # Hiệu ứng trồi lên so le (Staggered Entrance)
            card_delay = i * 0.2
            card_p = max(0.0, min(1.0, (p - card_delay) / 0.5))
            ease_card = 1.0 - math.pow(1.0 - card_p, 3)

            base_y = int(height * 0.18 + i * (card_h + 35))
            cur_y = int(base_y + (1.0 - ease_card) * 120)
            cur_x = (width - card_w) // 2

            if ease_card > 0.05:
                # Vẽ thẻ tin tức báo chí viền sáng
                draw.rounded_rectangle(
                    [(cur_x, cur_y), (cur_x + card_w, cur_y + card_h)],
                    radius=12,
                    fill=(24, 30, 42),
                    outline=(56, 189, 248, 160) if i == 0 else (255, 255, 255, 40),
                    width=2
                )
                
                # Brand logo & chấm đỏ Breaking
                brand_color = (239, 68, 68) if i == 0 else (56, 189, 248)
                draw.text((cur_x + 30, cur_y + 20), f"[BREAKING] {brand}", fill=brand_color, font=font_brand)
                draw.line([(cur_x + 30, cur_y + 54), (cur_x + card_w - 30, cur_y + 54)], fill=(255, 255, 255, 30), width=1)
                
                # Dòng tít bài báo
                draw.text((cur_x + 30, cur_y + 68), title, fill=(241, 245, 249), font=font_title)

        frame_final = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
        out_writer.write(frame_final)

    out_writer.release()
    print(f"[NEWS WALL OK] News Wall exported ({ratio}): {out_video_path.name}")
    return out_video_path


if __name__ == "__main__":
    print("[CCTV & NEWS] Testing CCTV Grid & International News Wall...")
    render_cctv_grid_clip(ratio="16:9")
    render_cctv_grid_clip(ratio="9:16")
    render_news_wall_clip(ratio="16:9")
    render_news_wall_clip(ratio="9:16")
