"""
document_inspector.py - Bộ soi tài liệu mật, bài báo & Bút dạ quang (Document Inspector)
Hỗ trợ cả 16:9 (Dài) & 9:16 (Ngắn)
Tính năng:
1. Tạo trang tài liệu điều tra / Báo cáo mật / Bài báo rò rỉ chuẩn pháp lý.
2. Camera 3D quét lướt nghiêng trên mặt văn bản (3D Perspective Document Flyover).
3. Vệt bút dạ quang vàng neon quét sáng dòng chữ bằng chứng (Highlighter Sweep).
4. Dấu mộc đỏ dập mạnh (Stamp Slam: KHỞI TỐ, TOP SECRET, LỆNH BẮT) kèm rung màn hình.
"""

import sys
import os
import math
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


def get_font(size=20, bold=False):
    font_names = ["timesbd.ttf", "segoeuib.ttf", "arialbd.ttf"] if bold else ["times.ttf", "segoeui.ttf", "arial.ttf"]
    for fn in font_names:
        fp = Path("C:/Windows/Fonts") / fn
        if fp.exists():
            try:
                return ImageFont.truetype(str(fp), size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_mock_classified_document(
    title="HỒ SƠ ĐIỀU TRA: TẬP ĐOÀN HIKVISION",
    highlight_text="ĐÃ VI PHẠM ĐẠO LUẬT THẨM QUYỀN QUỐC PHÒNG (NDAA)",
    doc_type="CLASSIFIED DOSSIER",
    case_no="CASE NO: 2024-CRIM-8841-FED",
    width=1600,
    height=2200
) -> Image.Image:
    """Tạo một văn bản tài liệu hồ sơ mật / báo cáo kiểm toán cổ điển chân thực"""
    # Nền giấy hơi ố vàng cổ điển (Parchment beige)
    img = Image.new("RGBA", (width, height), (242, 238, 228, 255))
    draw = ImageDraw.Draw(img)

    # Viền kỹ thuật xung quanh
    draw.rectangle([(40, 40), (width - 40, height - 40)], outline=(180, 170, 155, 255), width=2)
    draw.rectangle([(48, 48), (width - 48, height - 48)], outline=(200, 190, 175, 255), width=1)

    font_stamp = get_font(32, bold=True)
    font_hdr = get_font(20, bold=True)
    font_title = get_font(36, bold=True)
    font_body = get_font(24, bold=False)
    font_hl = get_font(26, bold=True)

    # Tiêu đề hồ sơ
    draw.text((80, 80), f"DEPARTMENT OF JUSTICE // {doc_type}", fill=(120, 50, 50), font=font_hdr)
    draw.text((width - 450, 80), case_no, fill=(100, 100, 100), font=font_hdr)
    draw.line([(80, 120), (width - 80, 120)], fill=(150, 140, 130), width=2)

    draw.text((80, 160), title.upper(), fill=(20, 20, 25), font=font_title)
    draw.text((80, 220), "NGÀY BAN HÀNH: 14 THÁNG 05 NĂM 2024 // TỐ TỤNG HÌNH SỰ", fill=(90, 90, 95), font=font_hdr)

    # Đoạn văn bản nội dung điều tra
    paragraphs = [
        "Căn cứ tài liệu thu thập từ các thiết bị giám sát mạng và lời khai nhân chứng tại phiên điều trần kín,",
        "Cơ quan An ninh điều tra đã làm rõ hành vi trốn thuế và thao túng báo cáo tài chính có tổ chức.",
        "Toàn bộ dòng tiền hơn 1.2 tỷ USD được chia nhỏ qua hàng loạt tài khoản ma tại nước ngoài.",
        f"KẾT LUẬN: ĐỐI TƯỢNG {highlight_text}.",
        "Hành vi này đã gây thiệt hại nghiêm trọng cho hệ thống an ninh quốc gia và trật tự thị trường.",
        "Đề nghị Viện Kiểm sát phê chuẩn Lệnh khởi tố bị can và Lệnh bắt tạm giam phục vụ điều tra mở rộng."
    ]

    curr_y = 300
    for p in paragraphs:
        if highlight_text in p:
            # Dòng chữ quan trọng sẽ được bôi bút dạ quang
            draw.text((80, curr_y), p, fill=(180, 20, 20), font=font_hl)
            curr_y += 75
        else:
            draw.text((80, curr_y), p, fill=(40, 40, 45), font=font_body)
            curr_y += 55

    # Con dấu chữ ký giả lập ở góc dưới
    draw.line([(width - 500, height - 200), (width - 100, height - 200)], fill=(80, 80, 80), width=2)
    draw.text((width - 480, height - 180), "THẨM PHÁN TRƯỞNG // ĐÃ KÝ VÀ PHÊ DUYỆT", fill=(80, 80, 80), font=font_hdr)

    return img


def render_document_inspector_clip(
    doc_title="HỒ SƠ KHỞI TỐ: ĐẠI ÁN GIAN LẬN TÀI CHÍNH",
    highlight_sentence="VI PHẠM QUY ĐỊNH VỀ RỬA TIỀN VÀ TRỐN THUẾ ĐẶC BIỆT",
    stamp_text="KHỞI TỐ",
    out_video_path: str | Path = None,
    duration: float = 4.0,
    fps: int = 30,
    ratio: str = "16:9"
) -> Path:
    """
    Xuất video ống kính 3D lướt trên văn bản, quét bút dạ quang và đóng dấu mộc đỏ 3D:
    - 0.0s -> 2.0s: Camera 3D trôi nghiêng dọc theo trang tài liệu.
    - 1.2s -> 2.5s: Vệt bút dạ quang vàng neon quét sáng dòng chữ quan trọng.
    - 2.8s: Con dấu mộc đỏ dập mạnh xuống mặt giấy kèm rung chấn màn hình (Screen Shake).
    """
    if ratio == "9:16":
        width, height = 1080, 1920
    else:
        width, height = 1920, 1080

    if out_video_path is None:
        out_video_path = OUTPUT_DIR / f"doc_inspector_{ratio.replace(':', 'x')}.mp4"
    else:
        out_video_path = Path(out_video_path)

    # 1. Sinh văn bản gốc
    doc_img = create_mock_classified_document(title=doc_title, highlight_text=highlight_sentence)
    doc_w, doc_h = doc_img.size

    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))

    stamp_frame = int(2.7 * fps)

    for f in range(total_frames):
        p = f / total_frames
        t = f / fps

        # 2. Camera 3D Pan: Lướt từ từ từ góc trên xuống góc dưới
        cam_y = int(p * (doc_h - height * 0.9))
        crop_h = int(height * 0.85)
        crop_w = int(width * 0.85)
        crop_box = (80, max(0, min(doc_h - crop_h, cam_y)), 80 + crop_w, max(0, min(doc_h - crop_h, cam_y)) + crop_h)
        
        frame_pil = doc_img.crop(crop_box).resize((width, height), Image.Resampling.LANCZOS)
        draw = ImageDraw.Draw(frame_pil)

        # 3. Bút dạ quang vàng neon quét (1.0s -> 2.4s)
        if 1.0 <= t <= 2.6:
            hl_progress = (t - 1.0) / 1.4
            hl_w = int(width * 0.75 * min(1.0, hl_progress))
            hl_y = int(height * 0.46)
            hl_h = 42
            # Vẽ vệt dạ quang vàng bán trong suốt
            hl_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            hl_draw = ImageDraw.Draw(hl_overlay)
            hl_draw.rectangle([(int(width * 0.12), hl_y), (int(width * 0.12) + hl_w, hl_y + hl_h)], fill=(255, 235, 59, 130))
            frame_pil = Image.alpha_composite(frame_pil.convert("RGBA"), hl_overlay)
        elif t > 2.6:
            # Đã bôi xong, giữ nguyên vệt dạ quang
            hl_overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            hl_draw = ImageDraw.Draw(hl_overlay)
            hl_draw.rectangle([(int(width * 0.12), int(height * 0.46)), (int(width * 0.87), int(height * 0.46) + 42)], fill=(255, 235, 59, 130))
            frame_pil = Image.alpha_composite(frame_pil.convert("RGBA"), hl_overlay)

        # 4. Đóng dấu mộc đỏ 3D (Stamp Slam tại t >= 2.7s)
        shake_x, shake_y = 0, 0
        if f >= stamp_frame:
            stamp_p = min(1.0, (f - stamp_frame) / 4) # Rơi cực nhanh trong 4 frame
            # Screen shake rung giật khi va đập
            if f - stamp_frame < 8:
                shake_decay = (8 - (f - stamp_frame)) / 8.0
                shake_x = int(math.sin(f * 2.5) * 12 * shake_decay)
                shake_y = int(math.cos(f * 2.5) * 8 * shake_decay)

            # Vẽ dấu mộc đỏ nghiêng góc
            stamp_w, stamp_h = 360, 130
            stamp_img = Image.new("RGBA", (stamp_w, stamp_h), (0, 0, 0, 0))
            st_draw = ImageDraw.Draw(stamp_img)
            # Khung đôi đỏ rực
            st_draw.rounded_rectangle([(4, 4), (stamp_w - 4, stamp_h - 4)], radius=8, outline=(220, 38, 38, 240), width=6)
            st_draw.rounded_rectangle([(12, 12), (stamp_w - 12, stamp_h - 12)], radius=6, outline=(220, 38, 38, 180), width=2)
            
            font_st = get_font(42, bold=True)
            st_draw.text((32, 38), stamp_text.upper(), fill=(220, 38, 38, 255), font=font_st)
            
            # Xoay con dấu nghiêng -12 độ
            rotated_stamp = stamp_img.rotate(12, resample=Image.Resampling.BILINEAR, expand=True)
            
            # Dán con dấu vào giữa trang
            st_pos_x = int(width * 0.52) - rotated_stamp.width // 2
            st_pos_y = int(height * 0.52) - rotated_stamp.height // 2
            frame_pil.paste(rotated_stamp, (st_pos_x, st_pos_y), rotated_stamp)

        # Chuyển đổi sang BGR và áp dụng Screen Shake
        frame_np = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGBA2BGR)
        if shake_x != 0 or shake_y != 0:
            M_shake = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
            frame_np = cv2.warpAffine(frame_np, M_shake, (width, height), borderMode=cv2.BORDER_REFLECT)

        # Tông màu điện ảnh tối góc (Vignette)
        out_writer.write(frame_np)

    out_writer.release()
    print(f"[DOC INSPECTOR OK] Exported document flyover ({ratio}): {out_video_path.name}")
    return out_video_path


if __name__ == "__main__":
    print("[DOC INSPECTOR] Testing Document & Highlighter Engine...")
    render_document_inspector_clip(ratio="16:9")
    render_document_inspector_clip(ratio="9:16")
