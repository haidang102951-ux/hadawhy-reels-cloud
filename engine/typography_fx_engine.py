"""
typography_fx_engine.py - Hệ thống Đa Phông Chữ & Đa Hiệu Ứng Chữ Đỉnh Cao (Multi-Font & Multi-FX Typography Engine)
Cung cấp 7 bộ phong cách thị giác hoàn chỉnh cho từng thể loại video khác nhau:
1. HOLLYWOOD_GOLD: Phong cách Bom tấn Hoàng gia, Serif giãn chữ, Bevel 3D vàng kim sa.
2. CYBER_NEON: Phong cách Công nghệ cao, Đèn Neon phát sáng rực rỡ, Hào quang Cyberpunk.
3. PLATINUM_CHROME: Phong cách Luxury Tối giản / Siêu xe, Bạc Titan gương bóng sắc lẹm.
4. FIRE_EMBER: Phong cách Sale Khủng / Bùng nổ / Thể thao, Nham thạch rực lửa, Cam đỏ than hồng.
5. GLASS_MINIMALIST: Phong cách Apple / Nội thất cao cấp, Kính mờ Frosted Glass, Tinh xảo trang nhã.
6. ARTISTIC_SCRIPT: Phong cách Thủ công mỹ nghệ / Ký tên Độc bản, Chữ viết tay mạ vàng nghệ thuật.
7. COMIC_POP: Phong cách Viral Trẻ trung / Hype TikTok / Reels, Khối 3D đa tầng màu sắc nổi bật.
"""

import sys
from pathlib import Path
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

FONTS_DIR = Path(r"D:\Đầu Não (không xóa)\assets\fonts")
OUTPUT_DIR = Path(r"D:\Đầu Não (không xóa)\assets\commercial")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Bản đồ phông chữ theo ngữ cảnh (100% hỗ trợ tiếng Việt đầy đủ, không lỗi dấu / không ô vuông)
FONT_MAP = {
    "high_fashion": [FONTS_DIR / "Syne-Bold.ttf", FONTS_DIR / "PlayfairDisplay-Bold.ttf", FONTS_DIR / "PlusJakartaSans-Bold.ttf"],
    "editorial_luxury": [FONTS_DIR / "PlayfairDisplay-Bold.ttf", FONTS_DIR / "CormorantGaramond-Bold.ttf", FONTS_DIR / "Cinzel-Bold.ttf"],
    "modern_sans": [FONTS_DIR / "PlusJakartaSans-Bold.ttf", FONTS_DIR / "Montserrat-Variable.ttf", FONTS_DIR / "BeVietnamPro-ExtraBold.ttf"],
    "impact_bold": [FONTS_DIR / "BebasNeue-Regular.ttf", FONTS_DIR / "Anton-Regular.ttf", FONTS_DIR / "BeVietnamPro-Black.ttf"],
    "tall_condensed": [FONTS_DIR / "BebasNeue-Regular.ttf", FONTS_DIR / "Montserrat-Variable.ttf"],
    "serif_royal": [FONTS_DIR / "Cinzel-Bold.ttf", FONTS_DIR / "PlayfairDisplay-Bold.ttf"],
    "tech_cyber": [FONTS_DIR / "Kanit-Black.ttf", FONTS_DIR / "PlusJakartaSans-Bold.ttf"],
    "friendly_cute": [FONTS_DIR / "Baloo2-Variable.ttf", FONTS_DIR / "Montserrat-Variable.ttf"],
    "handwriting_script": [FONTS_DIR / "CormorantGaramond-Bold.ttf", FONTS_DIR / "Syne-Bold.ttf"]
}


def create_multicolor_gradient(width: int, height: int, color_stops: list, angle_deg=0) -> Image.Image:
    """
    Sinh dải chuyển màu đa sắc (Multi-Color Gradient) mượt mà không giới hạn số lượng màu.
    color_stops: Danh sách các màu RGB [(r1, g1, b1), (r2, g2, b2), ...]
    angle_deg: Góc nghiêng chuyển màu (0 = Dọc, 90 = Ngang, 45 = Chéo)
    """
    num_colors = len(color_stops)
    if num_colors == 1:
        return Image.new("RGB", (width, height), color_stops[0])

    grad_np = np.zeros((height, width, 3), dtype=np.float32)
    rad = math.radians(angle_deg)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    # Chiếu tọa độ lên vector góc nghiêng
    x_coords = np.linspace(0, 1, width)
    y_coords = np.linspace(0, 1, height)
    xv, yv = np.meshgrid(x_coords, y_coords)
    proj = xv * sin_a + yv * cos_a
    proj = (proj - proj.min()) / (proj.max() - proj.min() + 1e-6)

    # Nội suy qua từng dải màu
    seg_len = 1.0 / (num_colors - 1)
    for i in range(num_colors - 1):
        c1 = np.array(color_stops[i], dtype=np.float32)
        c2 = np.array(color_stops[i + 1], dtype=np.float32)
        
        mask_seg = (proj >= i * seg_len) & (proj <= (i + 1) * seg_len)
        factor = (proj - i * seg_len) / seg_len
        factor = np.clip(factor, 0.0, 1.0)
        
        for ch in range(3):
            grad_np[:, :, ch] = np.where(
                mask_seg,
                c1[ch] + factor * (c2[ch] - c1[ch]),
                grad_np[:, :, ch]
            )

    return Image.fromarray(np.clip(grad_np, 0, 255).astype(np.uint8)).convert("RGBA")


def load_font(category: str, size: int) -> ImageFont.ImageFont:
    """Nạp font theo phân loại chính xác, fallback thông minh"""
    candidates = FONT_MAP.get(category, FONT_MAP["modern_sans"])
    for p in candidates:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                continue
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", size)


def render_typography_fx(
    text: str,
    style: str = "HOLLYWOOD_GOLD",
    font_size: int = 64,
    wide_spacing: bool = False
) -> Image.Image:
    """
    Tạo chữ nghệ thuật với hiệu ứng đặc biệt hoàn chỉnh:
    - Phong cách Đơn sắc/Kim loại: 'HOLLYWOOD_GOLD', 'CYBER_NEON', 'PLATINUM_CHROME', 'FIRE_EMBER', 'GLASS_MINIMALIST', 'ARTISTIC_SCRIPT', 'COMIC_POP'
    - Phong cách Đa sắc màu (Multi-Color): 'HOLOGRAPHIC_RAINBOW', 'SYNTHWAVE_DUALTONE', 'SUNSET_BURST', 'EMERALD_GOLD', 'AURORA_BOREALIS'
    """
    display_text = " ".join(list(text)) if wide_spacing else text
    
    # 1. Chọn Font theo phong cách
    if style in ["HOLLYWOOD_GOLD", "EMERALD_GOLD"]:
        font = load_font("serif_royal", font_size)
    elif style in ["CYBER_NEON", "SYNTHWAVE_DUALTONE"]:
        font = load_font("tech_cyber", font_size)
    elif style in ["PLATINUM_CHROME"]:
        font = load_font("tall_condensed", font_size)
    elif style in ["FIRE_EMBER", "SUNSET_BURST"]:
        font = load_font("impact_bold", font_size)
    elif style in ["GLASS_MINIMALIST", "HOLOGRAPHIC_RAINBOW", "AURORA_BOREALIS"]:
        font = load_font("modern_sans", font_size)
    elif style == "ARTISTIC_SCRIPT":
        font = load_font("handwriting_script", font_size)
    elif style == "COMIC_POP":
        font = load_font("friendly_cute", font_size)
    else:
        font = load_font("modern_sans", font_size)

    # Đo kích thước
    dummy = Image.new("RGBA", (1, 1))
    draw_d = ImageDraw.Draw(dummy)
    bbox = draw_d.textbbox((0, 0), display_text, font=font)
    pad = 60
    t_w = bbox[2] - bbox[0] + pad * 2
    t_h = bbox[3] - bbox[1] + pad * 2
    origin_x = pad - bbox[0]
    origin_y = pad - bbox[1]

    # Mặt nạ chữ
    mask = Image.new("L", (t_w, t_h), 0)
    draw_m = ImageDraw.Draw(mask)
    draw_m.text((origin_x, origin_y), display_text, font=font, fill=255)

    result = Image.new("RGBA", (t_w, t_h), (0, 0, 0, 0))

    # =========================================================================
    # STYLE 1: HOLLYWOOD GOLD (Hoàng gia, Kim loại 3D, Hào quang ấm)
    # =========================================================================
    if style == "HOLLYWOOD_GOLD":
        grad_np = np.zeros((t_h, t_w, 3), dtype=np.uint8)
        for y in range(t_h):
            r_ratio = y / float(t_h)
            if r_ratio < 0.4:
                r, g, b = int(255 - r_ratio * 20), int(245 - r_ratio * 70), int(175 - r_ratio * 140)
            else:
                r, g, b = int(247 + (r_ratio - 0.4) * 8), int(175 - (r_ratio - 0.4) * 60), int(35 - (r_ratio - 0.4) * 20)
            grad_np[y, :, :] = [r, g, b]
        body = Image.fromarray(grad_np).convert("RGBA")
        body.putalpha(mask)

        # Viền Bevel
        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        specular = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 255))
        specular.putalpha(edge.point(lambda p: int(p * 0.9)))

        # Backlit glow
        glow_mask = mask.filter(ImageFilter.GaussianBlur(16))
        glow = Image.new("RGBA", (t_w, t_h), (255, 195, 60, 255))
        glow.putalpha(glow_mask.point(lambda p: int(p * 0.7)))

        # Drop shadow
        sh_mask = mask.filter(ImageFilter.GaussianBlur(8))
        sh = Image.new("RGBA", (t_w, t_h), (10, 5, 0, 255))
        sh.putalpha(sh_mask.point(lambda p: int(p * 0.85)))

        result.paste(sh, (6, 8), sh)
        result.paste(glow, (0, 0), glow)
        result.paste(body, (0, 0), body)
        result.paste(specular, (0, 0), specular)

    # =========================================================================
    # STYLE 2: CYBER NEON (Ống Neon Cyberpunk, Phát sáng rực rỡ, Lõi sáng trắng)
    # =========================================================================
    elif style == "CYBER_NEON":
        # Hào quang neon 3 lớp: Tỏa rộng (Cyan), Tỏa vừa (Deep Blue), Lõi trắng
        neon_outer = mask.filter(ImageFilter.GaussianBlur(24))
        l_outer = Image.new("RGBA", (t_w, t_h), (0, 230, 255, 255))
        l_outer.putalpha(neon_outer.point(lambda p: int(p * 0.6)))

        neon_mid = mask.filter(ImageFilter.GaussianBlur(10))
        l_mid = Image.new("RGBA", (t_w, t_h), (0, 160, 255, 255))
        l_mid.putalpha(neon_mid.point(lambda p: int(p * 0.9)))

        # Thân chữ trắng ánh cyan
        body = Image.new("RGBA", (t_w, t_h), (220, 255, 255, 255))
        body.putalpha(mask)

        result.paste(l_outer, (0, 0), l_outer)
        result.paste(l_mid, (0, 0), l_mid)
        result.paste(body, (0, 0), body)

    # =========================================================================
    # STYLE 3: PLATINUM CHROME (Bạc Titan, Phản chiếu sắc lẹm, Gương bóng)
    # =========================================================================
    elif style == "PLATINUM_CHROME":
        grad_np = np.zeros((t_h, t_w, 3), dtype=np.uint8)
        for y in range(t_h):
            r_ratio = y / float(t_h)
            # Dải phản xạ Chrome: Đỉnh trắng -> Giữa tối -> Chân sáng
            val = int(255 * (0.5 + 0.5 * math.cos(r_ratio * math.pi * 3.5)))
            grad_np[y, :, :] = [val, min(255, val + 10), min(255, val + 25)]
        body = Image.fromarray(grad_np).convert("RGBA")
        body.putalpha(mask)

        # Viền sắc lẹm màu xanh băng (Ice Blue)
        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        specular = Image.new("RGBA", (t_w, t_h), (180, 230, 255, 255))
        specular.putalpha(edge)

        # Bóng đổ kim loại
        sh_mask = mask.filter(ImageFilter.GaussianBlur(6))
        sh = Image.new("RGBA", (t_w, t_h), (0, 0, 10, 255))
        sh.putalpha(sh_mask.point(lambda p: int(p * 0.9)))

        result.paste(sh, (4, 6), sh)
        result.paste(body, (0, 0), body)
        result.paste(specular, (0, 0), specular)

    # =========================================================================
    # STYLE 4: FIRE EMBER (Nham Thạch Rực Lửa, Cam Đỏ Cháy, Bùng nổ)
    # =========================================================================
    elif style == "FIRE_EMBER":
        grad_np = np.zeros((t_h, t_w, 3), dtype=np.uint8)
        for y in range(t_h):
            r_ratio = y / float(t_h)
            # Vàng chanh đỉnh (255, 240, 50) -> Đỏ rực chân (220, 20, 10)
            r = int(255 - r_ratio * 35)
            g = int(240 - r_ratio * 210)
            b = int(50 - r_ratio * 40)
            grad_np[y, :, :] = [r, max(0, g), max(0, b)]
        body = Image.fromarray(grad_np).convert("RGBA")
        body.putalpha(mask)

        # Hào quang lửa bốc cháy
        fire_glow = mask.filter(ImageFilter.GaussianBlur(18))
        f_glow = Image.new("RGBA", (t_w, t_h), (255, 60, 0, 255))
        f_glow.putalpha(fire_glow.point(lambda p: int(p * 0.85)))

        # Viền viền cháy đen
        sh_mask = mask.filter(ImageFilter.GaussianBlur(4))
        sh = Image.new("RGBA", (t_w, t_h), (20, 0, 0, 255))
        sh.putalpha(sh_mask)

        result.paste(sh, (4, 5), sh)
        result.paste(f_glow, (0, 0), f_glow)
        result.paste(body, (0, 0), body)

    # =========================================================================
    # STYLE 5: GLASS MINIMALIST (Kính Mờ Tối Giản Apple, Thanh Lịch, Tinh Tế)
    # =========================================================================
    elif style == "GLASS_MINIMALIST":
        # Chữ trắng mờ thanh khiết với viền nét mảnh tinh xảo
        body = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 220))
        body.putalpha(mask)

        # Viền sáng tinh vi (Fine edge)
        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        specular = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 255))
        specular.putalpha(edge)

        # Bóng mờ khuếch tán diện rộng (Soft ambient shadow)
        sh_mask = mask.filter(ImageFilter.GaussianBlur(14))
        sh = Image.new("RGBA", (t_w, t_h), (0, 0, 0, 255))
        sh.putalpha(sh_mask.point(lambda p: int(p * 0.45)))

        result.paste(sh, (2, 8), sh)
        result.paste(body, (0, 0), body)
        result.paste(specular, (0, 0), specular)

    # =========================================================================
    # STYLE 6: ARTISTIC SCRIPT (Chữ Viết Tay Mạ Vàng, Ký Tên Nghệ Thuật)
    # =========================================================================
    elif style == "ARTISTIC_SCRIPT":
        # Mạ vàng óng ánh trên nét bút mềm mại
        body = Image.new("RGBA", (t_w, t_h), (245, 195, 75, 255))
        body.putalpha(mask)

        # Ánh sáng ven vàng dịu
        glow_mask = mask.filter(ImageFilter.GaussianBlur(8))
        glow = Image.new("RGBA", (t_w, t_h), (255, 225, 130, 255))
        glow.putalpha(glow_mask.point(lambda p: int(p * 0.5)))

        # Bóng mực bút đen nhung
        sh_mask = mask.filter(ImageFilter.GaussianBlur(4))
        sh = Image.new("RGBA", (t_w, t_h), (15, 10, 5, 255))
        sh.putalpha(sh_mask.point(lambda p: int(p * 0.75)))

        result.paste(sh, (3, 4), sh)
        result.paste(glow, (0, 0), glow)
        result.paste(body, (0, 0), body)

    # =========================================================================
    # STYLE 7: COMIC POP (Khối 3D Dày Đa Tầng, Vàng Chanh Đổ Khối Xanh Navy)
    # =========================================================================
    elif style == "COMIC_POP":
        # Thân chữ vàng tươi (Canary Yellow)
        body = Image.new("RGBA", (t_w, t_h), (255, 220, 20, 255))
        body.putalpha(mask)

        # Viền đen dày (Thick Comic Stroke)
        stroke_outer = mask.filter(ImageFilter.MaxFilter(9))
        l_stroke = Image.new("RGBA", (t_w, t_h), (20, 20, 30, 255))
        l_stroke.putalpha(stroke_outer)

        # Khối 3D đùn về góc dưới phải (3D Extrusion)
        ext_layer = Image.new("RGBA", (t_w, t_h), (0, 0, 0, 0))
        for step in range(1, 12):
            sh_step = Image.new("RGBA", (t_w, t_h), (15, 60, 140, 255))
            sh_step.putalpha(stroke_outer)
            ext_layer.paste(sh_step, (step, step), sh_step)

        result.paste(ext_layer, (0, 0), ext_layer)
        result.paste(l_stroke, (0, 0), l_stroke)
        result.paste(body, (0, 0), body)

    # =========================================================================
    # STYLE 8: HOLOGRAPHIC RAINBOW (Cầu Vồng Đa Sắc Ánh Xà Cừ / Hologram)
    # =========================================================================
    elif style == "HOLOGRAPHIC_RAINBOW":
        rainbow_stops = [(255, 40, 160), (255, 130, 0), (255, 235, 20), (0, 240, 140), (0, 210, 255), (170, 70, 255)]
        body_grad = create_multicolor_gradient(t_w, t_h, rainbow_stops, angle_deg=35)
        body = body_grad.copy()
        body.putalpha(mask)

        glow_mask = mask.filter(ImageFilter.GaussianBlur(16))
        glow_grad = create_multicolor_gradient(t_w, t_h, rainbow_stops, angle_deg=35)
        glow_grad.putalpha(glow_mask.point(lambda p: int(p * 0.75)))

        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        specular = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 255))
        specular.putalpha(edge.point(lambda p: int(p * 0.95)))

        sh_mask = mask.filter(ImageFilter.GaussianBlur(8))
        sh = Image.new("RGBA", (t_w, t_h), (10, 5, 20, 255))
        sh.putalpha(sh_mask.point(lambda p: int(p * 0.85)))

        result.paste(sh, (5, 7), sh)
        result.paste(glow_grad, (0, 0), glow_grad)
        result.paste(body, (0, 0), body)
        result.paste(specular, (0, 0), specular)

    # =========================================================================
    # STYLE 9: SYNTHWAVE DUALTONE (Hồng Neon Chuyển Tím Điện & Xanh Cyan)
    # =========================================================================
    elif style == "SYNTHWAVE_DUALTONE":
        stops = [(255, 20, 147), (180, 50, 230), (0, 245, 255)]
        body_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=45)
        body = body_grad.copy()
        body.putalpha(mask)

        glow_mask = mask.filter(ImageFilter.GaussianBlur(20))
        glow_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=45)
        glow_grad.putalpha(glow_mask.point(lambda p: int(p * 0.85)))

        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        spec = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 255))
        spec.putalpha(edge.point(lambda p: int(p * 0.8)))

        result.paste(glow_grad, (0, 0), glow_grad)
        result.paste(body, (0, 0), body)
        result.paste(spec, (0, 0), spec)

    # =========================================================================
    # STYLE 10: SUNSET BURST (Hoàng Hôn Đa Sắc: Đỏ Ruby -> Cam Lửa -> Vàng Nắng)
    # =========================================================================
    elif style == "SUNSET_BURST":
        stops = [(255, 30, 80), (255, 120, 0), (255, 225, 0), (140, 20, 180)]
        body_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=90)
        body = body_grad.copy()
        body.putalpha(mask)

        glow_mask = mask.filter(ImageFilter.GaussianBlur(18))
        glow_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=90)
        glow_grad.putalpha(glow_mask.point(lambda p: int(p * 0.8)))

        sh_mask = mask.filter(ImageFilter.GaussianBlur(6))
        sh = Image.new("RGBA", (t_w, t_h), (20, 0, 10, 255))
        sh.putalpha(sh_mask)

        result.paste(sh, (4, 6), sh)
        result.paste(glow_grad, (0, 0), glow_grad)
        result.paste(body, (0, 0), body)

    # =========================================================================
    # STYLE 11: EMERALD GOLD (Ngọc Bích Ombre Chuyển Sắc Vàng Hoàng Kim)
    # =========================================================================
    elif style == "EMERALD_GOLD":
        stops = [(0, 240, 150), (0, 160, 100), (245, 210, 70), (210, 160, 30)]
        body_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=30)
        body = body_grad.copy()
        body.putalpha(mask)

        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        gold_edge = Image.new("RGBA", (t_w, t_h), (255, 220, 90, 255))
        gold_edge.putalpha(edge)

        glow_mask = mask.filter(ImageFilter.GaussianBlur(15))
        glow = Image.new("RGBA", (t_w, t_h), (0, 220, 140, 255))
        glow.putalpha(glow_mask.point(lambda p: int(p * 0.7)))

        sh_mask = mask.filter(ImageFilter.GaussianBlur(7))
        sh = Image.new("RGBA", (t_w, t_h), (5, 20, 10, 255))
        sh.putalpha(sh_mask)

        result.paste(sh, (4, 6), sh)
        result.paste(glow, (0, 0), glow)
        result.paste(body, (0, 0), body)
        result.paste(gold_edge, (0, 0), gold_edge)

    # =========================================================================
    # STYLE 12: AURORA BOREALIS (Cực Quang Bắc Cực Tím - Lam - Hồng Pastel)
    # =========================================================================
    elif style == "AURORA_BOREALIS":
        stops = [(0, 255, 210), (0, 180, 255), (160, 70, 255), (255, 100, 190)]
        body_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=-30)
        body = body_grad.copy()
        body.putalpha(mask)

        glow_mask = mask.filter(ImageFilter.GaussianBlur(22))
        glow_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=-30)
        glow_grad.putalpha(glow_mask.point(lambda p: int(p * 0.85)))

        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        spec = Image.new("RGBA", (t_w, t_h), (220, 245, 255, 255))
        spec.putalpha(edge)

        result.paste(glow_grad, (0, 0), glow_grad)
        result.paste(body, (0, 0), body)
        result.paste(spec, (0, 0), spec)

    # =========================================================================
    # STYLE 13: CYBER MAGENTA 3D (Trắng Vát Khối Bevel + Bóng Đổ Hồng Neon Sâu)
    # Đặc trưng video Bất Động Sản & Talking-head Chuyên Gia
    # =========================================================================
    elif style == "CYBER_MAGENTA_3D":
        body = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 255))
        body.putalpha(mask)

        # 3D Extrusion đổ bóng hồng đậm (255, 20, 147)
        depth = 18
        for d in range(depth, 0, -2):
            shade = 1.0 - (d / depth) * 0.35
            sh_color = (int(255 * shade), int(20 * shade), int(147 * shade), 255)
            sh_img = Image.new("RGBA", (t_w, t_h), sh_color)
            sh_img.putalpha(mask)
            result.paste(sh_img, (d, d), sh_img)

        # Hào quang neon hồng
        glow_mask = mask.filter(ImageFilter.GaussianBlur(16))
        glow = Image.new("RGBA", (t_w, t_h), (255, 20, 147, 255))
        glow.putalpha(glow_mask.point(lambda p: int(p * 0.6)))
        result.paste(glow, (0, 0), glow)
        result.paste(body, (0, 0), body)

        # Viền Bevel trắng sáng lấp lánh
        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        spec = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 255))
        spec.putalpha(edge)
        result.paste(spec, (0, 0), spec)

    # =========================================================================
    # STYLE 14: SYNTHWAVE PURPLE DUAL (Tím Cyber Điện Tử + Viền Đen Dày)
    # Đặc trưng video AI Tech & Đổi mới sáng tạo
    # =========================================================================
    elif style == "SYNTHWAVE_PURPLE_DUAL":
        stops = [(180, 0, 255), (255, 0, 128)]
        body_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=45)
        body = body_grad.copy()
        body.putalpha(mask)

        # Viền đen dày dặn bảo vệ chữ
        stroke_mask = mask.filter(ImageFilter.MaxFilter(7))
        stroke_edge = ImageChops.subtract(stroke_mask, mask)
        stroke = Image.new("RGBA", (t_w, t_h), (10, 5, 20, 255))
        stroke.putalpha(stroke_edge)

        # Hào quang tím
        glow_mask = mask.filter(ImageFilter.GaussianBlur(14))
        glow = Image.new("RGBA", (t_w, t_h), (180, 0, 255, 255))
        glow.putalpha(glow_mask.point(lambda p: int(p * 0.7)))

        result.paste(glow, (0, 0), glow)
        result.paste(stroke, (0, 0), stroke)
        result.paste(body, (0, 0), body)

    # =========================================================================
    # STYLE 15: EARTHY FOREST GREEN (Xanh Rêu Trầm + Vàng Kem Be Sang Trọng)
    # Đặc trưng Phong Cách Sống Xanh, Tự Nhiên & Bền Vững
    # =========================================================================
    elif style == "EARTHY_FOREST_GREEN":
        stops = [(35, 80, 60), (60, 120, 90), (230, 220, 190)]
        body_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=20)
        body = body_grad.copy()
        body.putalpha(mask)

        # Viền vàng kem thanh lịch
        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        spec = Image.new("RGBA", (t_w, t_h), (245, 235, 210, 255))
        spec.putalpha(edge)

        sh_mask = mask.filter(ImageFilter.GaussianBlur(6))
        sh = Image.new("RGBA", (t_w, t_h), (10, 25, 15, 255))
        sh.putalpha(sh_mask)

        result.paste(sh, (4, 5), sh)
        result.paste(body, (0, 0), body)
        result.paste(spec, (0, 0), spec)

    # =========================================================================
    # STYLE 16: COOL STEEL ICE (Xanh Băng Bạc + Xám Titan Chuẩn Cơ Khí)
    # Đặc trưng Máy Móc CNC, Dây Chuyền Nhà Máy Hiện Đại
    # =========================================================================
    elif style == "COOL_STEEL_ICE":
        stops = [(210, 240, 255), (120, 180, 220), (50, 90, 130)]
        body_grad = create_multicolor_gradient(t_w, t_h, stops, angle_deg=90)
        body = body_grad.copy()
        body.putalpha(mask)

        # Viền sắc bạc titan
        edge = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(3)))
        spec = Image.new("RGBA", (t_w, t_h), (255, 255, 255, 255))
        spec.putalpha(edge)

        glow_mask = mask.filter(ImageFilter.GaussianBlur(12))
        glow = Image.new("RGBA", (t_w, t_h), (0, 200, 255, 255))
        glow.putalpha(glow_mask.point(lambda p: int(p * 0.5)))

        result.paste(glow, (0, 0), glow)
        result.paste(body, (0, 0), body)
        result.paste(spec, (0, 0), spec)

    return result


def generate_font_style_catalog(output_path=None) -> Path:
    """
    Tạo Bảng Triển Lãm (Catalog Showcase) hiển thị trọn vẹn 7 phong cách thị giác
    để người dùng dễ dàng chiêm ngưỡng và lựa chọn.
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "typography_showcase_catalog.png"

    canvas_w = 1920
    canvas_h = 1600
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (16, 18, 22, 255))
    draw = ImageDraw.Draw(canvas)

    # Tiêu đề catalog
    header_font = load_font("modern_sans", 52)
    sub_header_font = load_font("modern_sans", 26)
    draw.text((80, 50), "BỘ SƯU TẬP ĐA PHÔNG CHỮ & ĐA HIỆU ỨNG THỊ GIÁC", font=header_font, fill=(255, 255, 255, 255))
    draw.text((80, 115), "Tích hợp sẵn trong hệ thống - Tự động chọn font & hiệu ứng phù hợp từng kịch bản", font=sub_header_font, fill=(160, 175, 200, 255))

    styles = [
        ("HOLLYWOOD_GOLD", "HOÀNG GIA ĐIỆN ẢNH", "PREMIUM CREATOR COLLECTION", True),
        ("CYBER_NEON", "CÔNG NGHỆ CYBERPUNK", "CYBER TECH ECOSYSTEM", False),
        ("PLATINUM_CHROME", "BẠC TITAN SIÊU XE", "LUXURY INTERIOR COLLECTION", False),
        ("FIRE_EMBER", "KHUYẾN MÃI BÙNG NỔ", "GIẢM 50% - SIÊU DEAL GIỚI HẠN", False),
        ("GLASS_MINIMALIST", "KÍNH MỜ APPLE", "Tinh Tế Trong Từng Đường Nét", False),
        ("ARTISTIC_SCRIPT", "CHỮ KÝ NGHỆ THUẬT", "Tri Ân Khách Hàng Thân Thiết", False),
        ("COMIC_POP", "HYPE TIKTOK / REELS", "QUÀ TẶNG CỰC ĐỈNH - NHẬN NGAY!", False)
    ]

    start_y = 180
    for idx, (s_key, s_desc, sample_txt, is_wide) in enumerate(styles):
        # Nhãn mô tả phong cách
        label = f"{idx + 1}. {s_key} ({s_desc})"
        draw.text((90, start_y), label, font=sub_header_font, fill=(230, 190, 80, 255))

        # Render chữ nghệ thuật
        rendered_txt = render_typography_fx(sample_txt, style=s_key, font_size=46, wide_spacing=is_wide)
        
        # Ghép vào canvas
        canvas.paste(rendered_txt, (100, start_y + 35), rendered_txt)

        # Đường kẻ phân cách siêu mỏng
        draw.line([(80, start_y + 185), (canvas_w - 80, start_y + 185)], fill=(255, 255, 255, 20), width=1)
        start_y += 200

    canvas.save(output_path)
    print(f"✅ Đã tạo Catalog Showcase Typography: {output_path}")
    return output_path


def generate_multicolor_catalog(output_path=None) -> Path:
    """
    Tạo Bảng Triển Lãm Đa Sắc Màu (Multi-Color Spectrum Showcase)
    Hiển thị các hiệu ứng chuyển màu rực rỡ, Gradient đa điểm, Hologram, Synthwave, Sunset, Aurora...
    """
    if output_path is None:
        output_path = OUTPUT_DIR / "typography_multicolor_catalog.png"

    canvas_w = 1920
    canvas_h = 1350
    canvas = Image.new("RGBA", (canvas_w, canvas_h), (12, 14, 18, 255))
    draw = ImageDraw.Draw(canvas)

    header_font = load_font("modern_sans", 52)
    sub_header_font = load_font("modern_sans", 24)
    draw.text((80, 50), "BỘ SƯU TẬP ĐA SẮC MÀU & CHUYỂN MÀU GRADIENT ĐA ĐIỂM", font=header_font, fill=(255, 255, 255, 255))
    draw.text((80, 115), "Ứng dụng dải quang phổ rực rỡ: Hologram 6 màu, Synthwave Hồng-Tím-Cyan, Sunset Đỏ-Cam-Vàng, Aurora Cực quang", font=sub_header_font, fill=(200, 215, 240, 255))

    multi_styles = [
        ("HOLOGRAPHIC_RAINBOW", "CẦU VỒNG 6 MÀU QUANG PHỔ / ÁNH XÀ CỪ HOLOGRAM", "PANEL PLUS - BẢO HÀNH CHÍNH HÃNG", False),
        ("SYNTHWAVE_DUALTONE", "HỒNG NEON CHUYỂN TÍM ĐIỆN & CYAN NĂNG ĐỘNG", "KHO MỘC HARDWARE CYBER SYSTEM", False),
        ("SUNSET_BURST", "HOÀNG HÔN NHIỆT ĐỚI: ĐỎ RUBY -> CAM LỬA -> VÀNG NẮNG", "SIÊU KHUYẾN MÃI - SIÊU DEAL GIỚI HẠN", False),
        ("EMERALD_GOLD", "NGỌC BÍCH OMBRE PHỐI VÀNG HOÀNG GIA SANG TRỌNG", "KIỆT TÁC NỘI THẤT HOÀNG GIA", False),
        ("AURORA_BOREALIS", "CỰC QUANG BẮC CỰC: LAM NGỌC -> TÍM -> HỒNG PASTEL", "Ưu Đãi Đặc Quyền Dành Riêng Cho Bạn", False)
    ]

    start_y = 180
    for idx, (s_key, s_desc, sample_txt, is_wide) in enumerate(multi_styles):
        label = f"{idx + 1}. {s_key} - {s_desc}"
        draw.text((90, start_y), label, font=sub_header_font, fill=(240, 210, 120, 255))

        rendered_txt = render_typography_fx(sample_txt, style=s_key, font_size=46, wide_spacing=is_wide)
        canvas.paste(rendered_txt, (100, start_y + 35), rendered_txt)

        draw.line([(80, start_y + 205), (canvas_w - 80, start_y + 205)], fill=(255, 255, 255, 20), width=1)
        start_y += 225

    canvas.save(output_path)
    print(f"✅ Đã tạo Catalog Đa Sắc Màu: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_font_style_catalog()
    generate_multicolor_catalog()
