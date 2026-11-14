"""
chart_engine.py - Bộ sinh biểu đồ động đa năng (Dynamic Animated Chart Engine)
Phục vụ cả 16:9 (Dài) & 9:16 (Ngắn)
Hỗ trợ:
1. Animated Line Chart (Biểu đồ đường neon tăng trưởng hoặc lao dốc khủng hoảng)
2. Animated Bar Chart (Biểu đồ cột mọc lên so sánh thị phần)
3. Animated Donut / Pie Chart (Vòng tròn quét 360 độ phân chia cơ cấu)
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


def get_font(size=22, bold=True):
    font_names = ["segoeuib.ttf", "arialbd.ttf", "tahomabd.ttf"] if bold else ["segoeui.ttf", "arial.ttf", "tahoma.ttf"]
    for fn in font_names:
        fp = Path("C:/Windows/Fonts") / fn
        if fp.exists():
            try:
                return ImageFont.truetype(str(fp), size)
            except Exception:
                pass
    return ImageFont.load_default()


def render_animated_line_chart(
    data_points: list[float],
    labels: list[str],
    title: str = "BIẾN ĐỘNG DÒNG TIỀN & THỊ PHẦN",
    unit: str = "$ TỶ",
    out_video_path: str | Path = None,
    duration: float = 4.0,
    fps: int = 30,
    ratio: str = "16:9",
    is_crash: bool = False
) -> Path:
    """
    Xuất video biểu đồ đường chạy neon mượt mà (Line Chart Animation):
    - is_crash=True: Đường màu đỏ thẫm cảnh báo lao dốc phá sản / trừng phạt.
    - is_crash=False: Đường màu xanh Cyan neon tăng trưởng.
    - Chấm sáng lướt tới đâu, nhãn số nhảy tới đó.
    - Hỗ trợ cả 16:9 và 9:16.
    """
    if ratio == "9:16":
        width, height = 1080, 1920
        chart_w, chart_h = 880, 720
        margin_x, margin_y = 100, 560
    else:
        width, height = 1920, 1080
        chart_w, chart_h = 1440, 560
        margin_x, margin_y = 240, 260

    if out_video_path is None:
        out_video_path = OUTPUT_DIR / f"chart_line_{'crash' if is_crash else 'growth'}_{ratio.replace(':', 'x')}.mp4"
    else:
        out_video_path = Path(out_video_path)

    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))

    min_val = min(data_points)
    max_val = max(data_points)
    val_range = max(1e-5, max_val - min_val)

    # Tọa độ các điểm trên màn hình
    n_pts = len(data_points)
    pts_xy = []
    for i, val in enumerate(data_points):
        px = margin_x + int(i / (n_pts - 1) * chart_w)
        norm_v = (val - min_val) / val_range
        py = margin_y + chart_h - int(norm_v * chart_h)
        pts_xy.append((px, py))

    line_color = (68, 68, 239) if is_crash else (248, 189, 56) # BGR: Red / Cyan
    glow_color = (30, 30, 180) if is_crash else (180, 120, 20)

    for f in range(total_frames):
        p = f / total_frames
        smooth_p = min(1.0, p * 1.25) # Vẽ xong ở 80% thời lượng, giữ lại 20%

        # Nền Blueprint tối
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (20, 14, 10) if not is_crash else (18, 12, 16)

        # Lưới tọa độ
        for gy in range(margin_y, margin_y + chart_h + 1, chart_h // 4):
            cv2.line(frame, (margin_x, gy), (margin_x + chart_w, gy), (45, 35, 28), 1)
        for gx in range(margin_x, margin_x + chart_w + 1, chart_w // (n_pts - 1)):
            cv2.line(frame, (gx, margin_y), (gx, margin_y + chart_h), (45, 35, 28), 1)

        # Tính toán chiều dài đường vẽ tới hiện tại
        cur_idx_float = smooth_p * (n_pts - 1)
        cur_idx = int(cur_idx_float)
        frac = cur_idx_float - cur_idx

        drawn_pts = pts_xy[:cur_idx + 1]
        if cur_idx < n_pts - 1:
            p1 = pts_xy[cur_idx]
            p2 = pts_xy[cur_idx + 1]
            inter_x = int(p1[0] + (p2[0] - p1[0]) * frac)
            inter_y = int(p1[1] + (p2[1] - p1[1]) * frac)
            drawn_pts.append((inter_x, inter_y))

        # Vẽ bóng đường phát sáng (Glow)
        if len(drawn_pts) > 1:
            for i in range(len(drawn_pts) - 1):
                cv2.line(frame, drawn_pts[i], drawn_pts[i+1], glow_color, 8)
                cv2.line(frame, drawn_pts[i], drawn_pts[i+1], line_color, 3)

        # Vẽ các chấm điểm mốc đã qua
        for i in range(min(cur_idx + 1, n_pts)):
            pt = pts_xy[i]
            cv2.circle(frame, pt, 5, (255, 255, 255), -1)
            cv2.circle(frame, pt, 9, line_color, 2)

        # Điểm đầu dẫn sáng nhấp nháy
        if drawn_pts:
            head = drawn_pts[-1]
            cv2.circle(frame, head, 7, (255, 255, 255), -1)
            cv2.circle(frame, head, 14, line_color, 2)

            # Giá trị hiện tại
            cur_val = data_points[min(cur_idx, n_pts - 1)]
            if cur_idx < n_pts - 1:
                cur_val += (data_points[cur_idx + 1] - data_points[cur_idx]) * frac
            val_text = f"{cur_val:.1f} {unit}"
            cv2.putText(frame, val_text, (head[0] - 40, head[1] - 22), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

        # Chuyển sang PIL để viết tiêu đề tiếng Việt chuẩn
        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)
        font_title = get_font(28, bold=True)
        font_axis = get_font(18, bold=False)

        # Tiêu đề biểu đồ
        draw.text((margin_x, margin_y - 70), title.upper(), fill=(255, 255, 255), font=font_title)
        badge_text = "CRITICAL ALERT // KHỦNG HOẢNG" if is_crash else "DYNAMIC GROWTH INDEX"
        badge_color = (239, 68, 68) if is_crash else (56, 189, 248)
        draw.text((margin_x, margin_y - 105), badge_text, fill=badge_color, font=font_axis)

        # Nhãn các mốc trục X
        for i, lbl in enumerate(labels):
            px = pts_xy[i][0]
            draw.text((px - 20, margin_y + chart_h + 15), lbl, fill=(148, 163, 184), font=font_axis)

        frame_final = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
        out_writer.write(frame_final)

    out_writer.release()
    print(f"[CHART OK] Animated Line Chart exported ({ratio}): {out_video_path.name}")
    return out_video_path


def render_animated_bar_chart(
    categories: list[str],
    values: list[float],
    title: str = "SO SÁNH QUY MÔ THỊ PHẦN TOÀN CẦU",
    unit: str = "%",
    out_video_path: str | Path = None,
    duration: float = 4.0,
    fps: int = 30,
    ratio: str = "16:9"
) -> Path:
    """
    Xuất video biểu đồ cột mọc lên (Animated Bar Chart):
    - Các cột vươn cao với hiệu ứng đàn hồi Easing.
    - Đơn vị và số liệu nhảy số real-time phía trên đỉnh cột.
    """
    if ratio == "9:16":
        width, height = 1080, 1920
        chart_w, chart_h = 880, 760
        margin_x, margin_y = 100, 560
    else:
        width, height = 1920, 1080
        chart_w, chart_h = 1440, 560
        margin_x, margin_y = 240, 260

    if out_video_path is None:
        out_video_path = OUTPUT_DIR / f"chart_bar_{ratio.replace(':', 'x')}.mp4"
    else:
        out_video_path = Path(out_video_path)

    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))

    max_val = max(values) * 1.15
    n_bars = len(values)
    bar_width = int(chart_w / n_bars * 0.55)
    gap = int(chart_w / n_bars)

    colors = [
        (248, 189, 56),  # Cyan
        (68, 179, 234),  # Amber Gold
        (130, 200, 40),  # Emerald Green
        (180, 80, 240),  # Purple
        (100, 116, 139)  # Slate Gray
    ]

    for f in range(total_frames):
        p = f / total_frames
        # Smooth bounce-like easing
        ease_p = 1.0 - math.pow(1.0 - min(1.0, p * 1.25), 3)

        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (20, 14, 10)

        # Lưới ngang
        for gy in range(margin_y, margin_y + chart_h + 1, chart_h // 4):
            cv2.line(frame, (margin_x, gy), (margin_x + chart_w, gy), (45, 35, 28), 1)

        pil_frame = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_frame)
        font_title = get_font(28, bold=True)
        font_lbl = get_font(18, bold=True)
        font_val = get_font(22, bold=True)

        # Tiêu đề
        draw.text((margin_x, margin_y - 70), title.upper(), fill=(255, 255, 255), font=font_title)

        for i, val in enumerate(values):
            cur_val = val * ease_p
            cur_h = int((cur_val / max_val) * chart_h)
            bx1 = margin_x + int(i * gap + (gap - bar_width) // 2)
            by2 = margin_y + chart_h
            by1 = by2 - cur_h
            bx2 = bx1 + bar_width

            c = colors[i % len(colors)] # BGR format
            c_rgb = (c[2], c[1], c[0])
            
            # Vẽ cột bo góc nhẹ
            if cur_h > 4:
                draw.rounded_rectangle([(bx1, by1), (bx2, by2)], radius=6, fill=c_rgb)

            # Số liệu đỉnh cột
            val_str = f"{cur_val:.1f}{unit}"
            draw.text((bx1 + 4, by1 - 32), val_str, fill=(255, 255, 255), font=font_val)
            # Tên nhãn đáy
            draw.text((bx1, by2 + 15), categories[i].upper(), fill=(148, 163, 184), font=font_lbl)

        frame_final = cv2.cvtColor(np.array(pil_frame), cv2.COLOR_RGB2BGR)
        out_writer.write(frame_final)

    out_writer.release()
    print(f"[CHART OK] Animated Bar Chart exported ({ratio}): {out_video_path.name}")
    return out_video_path


def export_remotion_d3_chart_spec(
    categories: list,
    values: list,
    title: str = "SO SÁNH THỊ PHẦN CHIẾN LƯỢC",
    subtitle: str = "Nguồn: Dữ liệu phân tích HaDa Why",
    unit: str = "%",
    theme_color: str = "#00E5FF",
    accent_color: str = "#FFD700",
    position: str = "left",
    output_json_path: str = None
) -> dict:
    """
    Xuất cấu hình JSON đặc tả biểu đồ D3 Native cho Remotion UniversalD3Chart.
    Giúp Sub-Agent 3D Data Specialist và Builder truyền trực tiếp dữ liệu vào Remotion
    mà không cần render video MP4 trung gian.
    """
    data_items = []
    for i, (cat, val) in enumerate(zip(categories, values)):
        data_items.append({
            "label": str(cat),
            "value": float(val),
            "suffix": unit,
            "isHighlighted": (i == len(categories) - 1)
        })
    
    spec = {
        "title": title,
        "subtitle": subtitle,
        "chartType": "bar",
        "themeColor": theme_color,
        "accentColor": accent_color,
        "position": position,
        "data": data_items
    }
    
    if output_json_path:
        out_p = Path(output_json_path)
        out_p.parent.mkdir(parents=True, exist_ok=True)
        import json
        with open(out_p, "w", encoding="utf-8") as fp:
            json.dump(spec, fp, indent=2, ensure_ascii=False)
        print(f"[CHART D3 OK] Đã xuất cấu hình Remotion D3 Chart Spec: {out_p.name}")
        
    return spec


if __name__ == "__main__":
    print("[CHART ENGINE] Testing Dynamic Animated Charts...")
    # Test Line Chart 16:9
    render_animated_line_chart([12.5, 14.8, 19.2, 8.4, 2.1], ["2020", "2021", "2022", "2023", "2024"], is_crash=True, ratio="16:9")
    # Test Bar Chart 9:16
    render_animated_bar_chart(["HIKVISION", "DAHUA", "AXIS", "OTHERS"], [38.2, 22.4, 14.1, 25.3], ratio="9:16")
