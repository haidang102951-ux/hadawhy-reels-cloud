"""
Engine: Depth Layering 3D Engine (Chữ & Vật thể 3D luồn sau lưng người nói)
Chức năng: Tách lớp người bằng AI, đặt Typography 3D hoặc vật thể 3D vào khoảng giữa nền và người,
tạo chiều sâu điện ảnh (Depth Layering) như video BĐS và video công nghệ đỉnh cao.
Tác giả: Antigravity Video Architecture
"""

import sys
import math
from pathlib import Path
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import rembg

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

# Import Typography Engine sẵn có
sys.path.append(r"D:\Đầu Não (không xóa)\engine")
try:
    from typography_fx_engine import render_typography_fx
except ImportError:
    render_typography_fx = None

FONTS_DIR = Path(r"D:\Đầu Não (không xóa)\assets\fonts")

def get_bold_font(size: int):
    candidates = [
        FONTS_DIR / "Montserrat-Variable.ttf",
        FONTS_DIR / "BeVietnamPro-Black.ttf",
        FONTS_DIR / "Kanit-Black.ttf",
        Path("C:/Windows/Fonts/impact.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf")
    ]
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                continue
    return ImageFont.load_default()

def create_3d_text_behind(text: str, font_size: int = 150, text_color=(255, 255, 255), shadow_color=(255, 20, 147), depth: int = 24) -> Image.Image:
    """
    Tạo chữ 3D vát cạnh sâu (Extruded 3D Text) với lớp bóng neon hồng/cyan
    """
    font = get_bold_font(font_size)
    dummy = Image.new("RGBA", (1, 1))
    draw_d = ImageDraw.Draw(dummy)
    bbox = draw_d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    pad = depth + 60
    w = tw + pad * 2
    h = th + pad * 2
    ox = pad - bbox[0]
    oy = pad - bbox[1]
    
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Vẽ các lớp Extrusion 3D đổ về hướng dưới-phải
    for d in range(depth, 0, -2):
        shade_factor = 1.0 - (d / depth) * 0.4
        c = (int(shadow_color[0] * shade_factor), int(shadow_color[1] * shade_factor), int(shadow_color[2] * shade_factor), 255)
        draw.text((ox + d, oy + d), text, font=font, fill=c)
        
    # 2. Mặt chữ chính (Face)
    draw.text((ox, oy), text, font=font, fill=(*text_color, 255))
    
    # 3. Viền sáng Bevel mảnh trên mặt chữ
    # Tạo glow nhẹ
    glow = img.filter(ImageFilter.GaussianBlur(12))
    final = Image.alpha_composite(glow, img)
    return final

def draw_neon_ring(img: Image.Image, center_xy: tuple, rx: int, ry: int, color=(255, 20, 147), angle_deg: int = -15):
    """
    Vẽ vòng elip năng lượng Neon (Neon Energy Ring) phát sáng xoay quanh trục
    """
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Tạo elip trong surface riêng rồi xoay
    ew = rx * 2 + 60
    eh = ry * 2 + 60
    esurf = Image.new("RGBA", (ew, eh), (0, 0, 0, 0))
    edraw = ImageDraw.Draw(esurf)
    
    box = [(30, 30), (ew - 30, eh - 30)]
    # Glow ngoài
    edraw.ellipse(box, outline=(*color, 80), width=16)
    # Lõi sáng
    edraw.ellipse(box, outline=(*color, 220), width=6)
    edraw.ellipse(box, outline=(255, 255, 255, 255), width=2)
    
    # Xoay elip
    rotated = esurf.rotate(angle_deg, resample=Image.Resampling.BICUBIC, expand=True)
    paste_x = center_xy[0] - rotated.width // 2
    paste_y = center_xy[1] - rotated.height // 2
    
    img.paste(rotated, (paste_x, paste_y), rotated)
    return img

def render_depth_layering_video(
    person_img_path: str,
    output_path: str,
    middle_text: str = "15 TRIỆU",
    sub_text: str = "TỐI ƯU CHI PHÍ",
    bg_img_path: str = None,
    duration: float = 3.0,
    fps: int = 30,
    ratio: str = '9:16',
    width: int = None,
    height: int = None,
    neon_color: tuple = (255, 20, 147), # Magenta Neon
    has_neon_ring: bool = True
):
    """
    Tạo clip Depth Layering hoàn chỉnh:
    Layer 0: Nền phong cảnh (subtle zoom)
    Layer 1: Chữ 3D Text khổng lồ luồn sau lưng người
    Layer 2: Người nói (đã tách nền bằng AI sắc nét)
    Layer 3: Vòng Neon phát sáng & Subtitle phía trước
    """
    out_p = Path(output_path)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    if width is None or height is None:
        width, height = (1920, 1080) if ratio == '16:9' else (1080, 1920)
    
    # 1. Load ảnh người và tách nền AI
    person_raw = Image.open(person_img_path).convert("RGBA")
    
    # Nếu không có bg_img_path thì dùng chính ảnh gốc làm nền mờ
    if bg_img_path and Path(bg_img_path).exists():
        bg_raw = Image.open(bg_img_path).convert("RGBA")
    else:
        bg_raw = person_raw.copy().filter(ImageFilter.GaussianBlur(8))
        
    # Resize bg và person vừa vặn khung hình 9:16
    def fit_cover(im):
        im_ratio = im.width / im.height
        target_ratio = width / height
        if im_ratio > target_ratio:
            new_h = height
            new_w = int(height * im_ratio)
        else:
            new_w = width
            new_h = int(width / im_ratio)
        im_resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
        left = (new_w - width) // 2
        top = (new_h - height) // 2
        return im_resized.crop((left, top, left + width, top + height))

    bg_covered = fit_cover(bg_raw)
    person_covered = fit_cover(person_raw)
    
    print("[AI] Đang tách nền người bằng rembg...")
    person_cutout = rembg.remove(person_covered)
    
    # Khử viền lem nhem (alpha feathering)
    r, g, b, a = person_cutout.split()
    a_feathered = a.filter(ImageFilter.GaussianBlur(1))
    person_cutout.putalpha(a_feathered)
    
    # 2. Tạo Chữ 3D khổng lồ nằm sau lưng
    text_3d = create_3d_text_behind(middle_text, font_size=160, text_color=(255, 255, 255), shadow_color=neon_color, depth=22)
    
    # 3. Tạo Subtext nổi phía trước
    font_sub = get_bold_font(44)
    dummy = Image.new("RGBA", (1, 1))
    d_d = ImageDraw.Draw(dummy)
    sbox = d_d.textbbox((0, 0), sub_text, font=font_sub)
    sw = sbox[2] - sbox[0] + 40
    sh = sbox[3] - sbox[1] + 24
    sub_badge = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
    d_sub = ImageDraw.Draw(sub_badge)
    d_sub.rounded_rectangle([(0, 0), (sw - 1, sh - 1)], radius=sh//2, fill=(20, 20, 25, 230), outline=(*neon_color, 200), width=2)
    d_sub.text((20 - sbox[0], 12 - sbox[1]), sub_text, font=font_sub, fill=(255, 255, 255, 255))
    
    # 4. Render Video Timeline
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(str(out_p), fourcc, fps, (width, height))
    
    # Tọa độ chữ 3D sau lưng (ngang tầm ngực/vai người nói)
    t3d_x = (width - text_3d.width) // 2
    t3d_y = int(height * 0.22)
    
    sub_x = (width - sw) // 2
    sub_y = int(height * 0.68)
    
    for f in range(total_frames):
        t = f / float(total_frames)
        # Background zoom nhẹ (Ken Burns)
        scale_bg = 1.0 + t * 0.04
        bg_w = int(width * scale_bg)
        bg_h = int(height * scale_bg)
        bg_zoomed = bg_covered.resize((bg_w, bg_h), Image.Resampling.BILINEAR)
        crop_x = (bg_w - width) // 2
        crop_y = (bg_h - height) // 2
        frame = bg_zoomed.crop((crop_x, crop_y, crop_x + width, crop_y + height)).convert("RGBA")
        
        # Chữ 3D sau lưng xuất hiện với hiệu ứng nhịp thở nhẹ (Floating)
        float_y = int(math.sin(t * math.pi * 2) * 12)
        frame.paste(text_3d, (t3d_x, t3d_y + float_y), text_3d)
        
        # Đè người lên trên Chữ 3D (Depth Layering Magic!)
        frame.paste(person_cutout, (0, 0), person_cutout)
        
        # Nếu bật vòng Neon Ring
        if has_neon_ring:
            ring_pulse = int(math.sin(t * math.pi * 4) * 6)
            draw_neon_ring(frame, (width // 2, int(height * 0.65)), 320 + ring_pulse, 85, color=neon_color, angle_deg=-12)
            
        # Dán nhãn phụ đề phía trước
        frame.paste(sub_badge, (sub_x, sub_y), sub_badge)
        
        frame_rgb = frame.convert("RGB")
        frame_bgr = cv2.cvtColor(np.array(frame_rgb), cv2.COLOR_RGB2BGR)
        writer.write(frame_bgr)
        
    writer.release()
    print(f"[OK] Đã xuất video Depth Layering 3D thành công: {out_p}")
    return str(out_p)

if __name__ == "__main__":
    print("Depth Layering 3D Engine Sẵn Sàng!")
