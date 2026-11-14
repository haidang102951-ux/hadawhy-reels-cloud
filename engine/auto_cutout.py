"""
auto_cutout.py - Tự động bóc tách nền nhân vật/vật thể bằng AI (BiRefNet / BRIA-RMBG SOTA)
Hỗ trợ hiệu ứng cao cấp cho cả Video 16:9 (Dài) & 9:16 (Ngắn):
1. Multi-Model Support: Mặc định bria-rmbg (1GB High-Res), hỗ trợ birefnet-general, isnet-general-use
2. De-fringing & Alpha Feathering: Khử triệt để viền lem nhem, halo trắng/đen quanh chi tiết cơ khí
3. Soft Rim Light: Ánh sáng ven mềm hổ phách/neon tôn khối chủ thể điện ảnh
4. 3D Double-Layer Contact & Cast Shadow: Đổ bóng sàn tiếp xúc 3D 2 tầng chân thực
5. Sticker Outline: Viền nét mảnh (tùy chọn)
"""

import sys
import os
from pathlib import Path

# Đảm bảo UTF-8 cho Windows console
if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if sys.stderr:
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from PIL import Image, ImageFilter, ImageOps, ImageEnhance, ImageChops
import numpy as np
import rembg

# Session cache toàn cục tránh load lại model nhiều lần
_GLOBAL_SESSIONS = {}

def get_rembg_session(model_name: str = "bria-rmbg"):
    """Lấy hoặc khởi tạo session rembg theo model yêu cầu"""
    global _GLOBAL_SESSIONS
    if model_name not in _GLOBAL_SESSIONS:
        try:
            print(f"[AI Cutout] Khởi tạo AI Matting Engine với Model: {model_name}...")
            _GLOBAL_SESSIONS[model_name] = rembg.new_session(model_name)
        except Exception as e:
            print(f"[!] Không thể load model {model_name} ({e}), chuyển sang fallback mặc định...")
            _GLOBAL_SESSIONS[model_name] = rembg.new_session()
    return _GLOBAL_SESSIONS[model_name]


def defringe_rgba(image_rgba: Image.Image, iterations: int = 2) -> Image.Image:
    """
    Khử viền lem nhem (De-fringing / Color Bleed Removal).
    Triệt tiêu viền sáng/tối halo bao quanh các chi tiết cơ khí, kính xe hoặc sợi tóc.
    """
    if image_rgba.mode != "RGBA":
        image_rgba = image_rgba.convert("RGBA")
    
    r, g, b, a = image_rgba.split()
    alpha_np = np.array(a, dtype=np.uint8)
    
    # Nếu ảnh hoàn toàn trong suốt hoặc đục hoàn toàn, bỏ qua
    if np.all(alpha_np == 0) or np.all(alpha_np == 255):
        return image_rgba
        
    rgb_img = Image.merge("RGB", (r, g, b))
    
    # Mở rộng màu của các pixel bên trong ra vùng biên bán trong suốt (alpha mờ)
    for _ in range(iterations):
        # Tạo mask cho các vùng bán trong suốt (viền lem)
        edge_mask = a.filter(ImageFilter.FIND_EDGES).filter(ImageFilter.MaxFilter(3))
        # Blur nhẹ RGB ở viền để hòa tan màu nền cũ
        rgb_blurred = rgb_img.filter(ImageFilter.BoxBlur(1))
        rgb_img = Image.composite(rgb_img, rgb_blurred, ImageChops.invert(edge_mask))
        
    r_clean, g_clean, b_clean = rgb_img.split()
    return Image.merge("RGBA", (r_clean, g_clean, b_clean, a))


def apply_alpha_feathering(image_rgba: Image.Image, radius: float = 1.0) -> Image.Image:
    """
    Làm mềm viền alpha (Alpha Feathering) tự nhiên, triệt tiêu răng cưa thô cứng.
    """
    if radius <= 0:
        return image_rgba
    r, g, b, a = image_rgba.split()
    a_feathered = a.filter(ImageFilter.GaussianBlur(radius))
    return Image.merge("RGBA", (r, g, b, a_feathered))


def add_outline(image_rgba: Image.Image, stroke_color=(255, 255, 255), stroke_width=4) -> Image.Image:
    """Tạo viền nét (stroke) cho ảnh PNG có kênh alpha"""
    if stroke_width <= 0:
        return image_rgba
        
    alpha = image_rgba.split()[-1]
    expanded_alpha = alpha.filter(ImageFilter.MaxFilter(stroke_width * 2 + 1))
    
    outline_img = Image.new("RGBA", image_rgba.size, (*stroke_color, 255))
    outline_img.putalpha(expanded_alpha)
    
    return Image.alpha_composite(outline_img, image_rgba)


def add_soft_rim_light(image_rgba: Image.Image, color=(255, 190, 70), width=16, blur=10, opacity=0.85) -> Image.Image:
    """
    Tạo ánh sáng ven mềm (Soft Rim Light) phong cách điện ảnh / Chuyện Nhà Băng
    Ánh sáng ven viền mờ dần vào trong thân người/vật thể, không bị giả như viền sticker.
    """
    if width <= 0:
        return image_rgba

    alpha = image_rgba.split()[-1]
    
    # Tạo inner border mask bằng cách lấy alpha gốc trừ đi alpha đã co nhỏ (Erode / MinFilter)
    eroded_alpha = alpha.filter(ImageFilter.MinFilter(width * 2 + 1))
    inner_edge = ImageChops.subtract(alpha, eroded_alpha)
    
    # Làm mờ cạnh trong để ánh sáng ven tan tự nhiên vào da/quần áo/kim loại
    blurred_edge = inner_edge.filter(ImageFilter.GaussianBlur(blur))
    
    # Áp dụng opacity
    if opacity < 1.0:
        blurred_edge = blurred_edge.point(lambda p: int(p * opacity))
        
    rim_layer = Image.new("RGBA", image_rgba.size, (*color, 255))
    rim_layer.putalpha(blurred_edge)
    
    # Ghép hòa trộn rim light lên trên chủ thể (chỉ hiển thị trong phạm vi alpha của chủ thể)
    final_rim = Image.composite(rim_layer, Image.new("RGBA", image_rgba.size, (0, 0, 0, 0)), alpha)
    result = Image.alpha_composite(image_rgba, final_rim)
    return result


def add_3d_double_shadow(
    image_rgba: Image.Image,
    canvas_size=None,
    subject_pos=None,
    shadow_color=(10, 10, 15),
    contact_opacity=0.85,
    cast_opacity=0.45,
    contact_blur=8,
    cast_blur=22,
    scale_y=0.28,
    shear_x=-0.45
) -> Image.Image:
    """
    Đổ bóng tiếp xúc sàn 3D 2 Lớp (Double-Layer Contact & Cast Shadow):
    - Lớp 1 (Contact Shadow): Bóng đen đậm, sát điểm tiếp xúc sàn (bánh xe, chân đế)
    - Lớp 2 (Cast Shadow): Bóng trải dài, nghiêng theo góc sáng, mờ dần ra xa
    """
    sub_w, sub_h = image_rgba.size
    
    if canvas_size is None:
        c_w = int(sub_w * 1.8)
        c_h = int(sub_h * 1.5)
    else:
        c_w, c_h = canvas_size

    if subject_pos is None:
        sub_x = (c_w - sub_w) // 2
        sub_y = c_h - sub_h - int(c_h * 0.08)
    else:
        sub_x = subject_pos[0] - sub_w // 2
        sub_y = subject_pos[1] - sub_h

    alpha = image_rgba.split()[-1]
    
    # ==================== LỚP 1: CONTACT SHADOW (ĐẬM & SÁT CHÂN) ====================
    contact_base = Image.new("RGBA", (sub_w, sub_h), (*shadow_color, 255))
    contact_base.putalpha(alpha)
    contact_flat_h = max(4, int(sub_h * 0.12))
    contact_flat = contact_base.resize((sub_w, contact_flat_h), Image.Resampling.BILINEAR)
    contact_blurred = contact_flat.filter(ImageFilter.GaussianBlur(contact_blur))
    
    # Scale opacity contact shadow
    c_alpha = np.array(contact_blurred.split()[-1], dtype=np.float32) * contact_opacity
    contact_blurred.putalpha(Image.fromarray(np.clip(c_alpha, 0, 255).astype(np.uint8)))
    
    # ==================== LỚP 2: CAST SHADOW (DÀI, NGHIÊNG, MỜ DẦN) ====================
    cast_base = Image.new("RGBA", (sub_w, sub_h), (*shadow_color, 255))
    cast_base.putalpha(alpha)
    cast_flat_h = max(4, int(sub_h * scale_y))
    cast_flat = cast_base.resize((sub_w, cast_flat_h), Image.Resampling.BILINEAR)
    
    m = shear_x
    x_shift = abs(int(cast_flat_h * m)) if m < 0 else 0
    new_w = sub_w + abs(int(cast_flat_h * m))
    
    sheared_cast = cast_flat.transform(
        (new_w, cast_flat_h),
        Image.Transform.AFFINE,
        (1, -m, x_shift if m < 0 else 0, 0, 1, 0),
        Image.Resampling.BILINEAR
    )
    cast_blurred = sheared_cast.filter(ImageFilter.GaussianBlur(cast_blur))
    
    # Gradient fade cho cast shadow (càng ra xa càng mờ)
    sh_w, sh_h = cast_blurred.size
    fade_arr = np.linspace(cast_opacity, cast_opacity * 0.15, sh_h, endpoint=True)
    cast_alpha = np.array(cast_blurred.split()[-1], dtype=np.float32)
    for i in range(sh_h):
        cast_alpha[i, :] = cast_alpha[i, :] * fade_arr[i]
    cast_blurred.putalpha(Image.fromarray(np.clip(cast_alpha, 0, 255).astype(np.uint8)))

    # ==================== TỔNG HỢP LÊN CANVAS 3D ====================
    canvas = Image.new("RGBA", (c_w, c_h), (0, 0, 0, 0))
    
    # 1. Dán Cast Shadow (dưới cùng)
    cast_x = sub_x - (x_shift if m < 0 else 0)
    cast_y = sub_y + sub_h - int(cast_flat_h * 0.20)
    canvas.paste(cast_blurred, (cast_x, cast_y), cast_blurred)
    
    # 2. Dán Contact Shadow (đè lên cast shadow nhưng dưới vật thể)
    contact_x = sub_x
    contact_y = sub_y + sub_h - int(contact_flat_h * 0.40)
    canvas.paste(contact_blurred, (contact_x, contact_y), contact_blurred)
    
    # 3. Dán chủ thể lên trên cùng
    canvas.paste(image_rgba, (sub_x, sub_y), image_rgba)
    
    return canvas


def cutout_image(
    input_path: str | Path,
    output_path: str | Path = None,
    model_name: str = "bria-rmbg",
    defringe: bool = True,
    edge_feather: float = 0.8,
    add_rim_light: bool = True,
    rim_color=(255, 190, 70),
    rim_width: int = 14,
    add_floor_shadow: bool = False,
    double_shadow: bool = True,
    canvas_size=None,
    add_stroke: bool = False,
    stroke_color=(255, 255, 255),
    stroke_width: int = 4,
    crop_tight: bool = False
) -> Path:
    """
    Bóc tách nền của ảnh và xuất ra sản phẩm chuyên nghiệp chuẩn SOTA 2026.
    Tự động áp dụng De-fringing, Alpha Feathering, Soft Rim Light và 3D Double Shadow.
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.with_name(f"{input_path.stem}_cutout.png")
    else:
        output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[AI Cutout SOTA] Đang bóc tách nền: {input_path.name} (Model: {model_name})...")
    orig = Image.open(input_path).convert("RGBA")
    
    # 1. Chạy AI Matting theo model session
    session = get_rembg_session(model_name)
    result_img = rembg.remove(orig, session=session)
    
    # 2. De-fringing khử viền lem nhem
    if defringe:
        result_img = defringe_rgba(result_img, iterations=2)
        
    # 3. Làm mềm viền Alpha Feathering
    if edge_feather > 0:
        result_img = apply_alpha_feathering(result_img, radius=edge_feather)
    
    # 4. Thêm viền sticker (nếu bật)
    if add_stroke:
        result_img = add_outline(result_img, stroke_color=stroke_color, stroke_width=stroke_width)
        
    # 5. Thêm ánh sáng ven mềm (Soft Rim Light)
    if add_rim_light:
        result_img = add_soft_rim_light(result_img, color=rim_color, width=rim_width)
        
    # 6. Thêm bóng sàn 3D (2 tầng hoặc 1 tầng)
    if add_floor_shadow:
        if double_shadow:
            result_img = add_3d_double_shadow(result_img, canvas_size=canvas_size)
        else:
            # Fallback single shadow
            result_img = add_3d_double_shadow(result_img, canvas_size=canvas_size, cast_opacity=0.0)
    elif crop_tight:
        bbox = result_img.getbbox()
        if bbox:
            result_img = result_img.crop(bbox)
            
    result_img.save(output_path, "PNG")
    print(f"[AI Cutout OK] Đã lưu sản phẩm bóc tách hoàn mỹ: {output_path}")
    return output_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Tự động bóc tách nền AI SOTA (BiRefNet/BRIA) & Chiếu sáng 3D")
    parser.add_argument("input", help="Đường dẫn ảnh đầu vào")
    parser.add_argument("-o", "--output", help="Đường dẫn file PNG kết quả", default=None)
    parser.add_argument("--model", default="bria-rmbg", choices=["bria-rmbg", "birefnet-general", "isnet-general-use", "u2net"], help="Model bóc tách")
    parser.add_argument("--rim", action="store_true", default=True, help="Bật Soft Rim Light")
    parser.add_argument("--no-rim", dest="rim", action="store_false", help="Tắt Soft Rim Light")
    parser.add_argument("--rim-color", default="255,190,70", help="Màu ánh sáng ven R,G,B")
    parser.add_argument("--shadow", action="store_true", help="Bật bóng sàn phối cảnh 3D 2 lớp")
    parser.add_argument("--stroke", action="store_true", help="Thêm viền trắng sticker phẳng")
    parser.add_argument("--crop", action="store_true", help="Cắt sát mép vật thể")
    parser.add_argument("--no-defringe", dest="defringe", action="store_false", default=True, help="Tắt De-fringing")
    parser.add_argument("--feather", type=float, default=0.8, help="Bán kính Alpha Feathering")
    
    args = parser.parse_args()
    in_file = Path(args.input)
    out_file = Path(args.output) if args.output else None
        
    rim_c = tuple(map(int, args.rim_color.split(",")))
    cutout_image(
        in_file,
        out_file,
        model_name=args.model,
        defringe=args.defringe,
        edge_feather=args.feather,
        add_rim_light=args.rim,
        rim_color=rim_c,
        add_floor_shadow=args.shadow,
        double_shadow=True,
        add_stroke=args.stroke,
        crop_tight=args.crop
    )
