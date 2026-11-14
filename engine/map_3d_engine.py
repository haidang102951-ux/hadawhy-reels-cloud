"""
map_3d_engine.py - Bộ xử lý bản đồ địa chính trị & Vệ tinh 3D siêu tốc (Vectorized NumPy)
Hỗ trợ cả 16:9 (Dài) & 9:16 (Ngắn) - Đọc trực tiếp countries.geojson (258 nước)
Tính năng:
1. Đọc và chiếu bản đồ vector Dark Mode toàn cầu (258 quốc gia & vùng lãnh thổ).
2. Tự động highlight quốc gia mục tiêu với viền neon phát sáng.
3. Vẽ đường bay vòng cung (Trans-Pacific Arc / Flight Path) chuyển động từ điểm A -> điểm B.
4. Sóng radar sonar tỏa từ tọa độ mục tiêu.
5. Hiệu ứng Camera Zoom & 3D Tilt nghiêng 45 độ phối cảnh.
"""

import sys
import os
import json
import math
from pathlib import Path

# Đảm bảo UTF-8 cho Windows console
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

import cv2
import numpy as np

ASSETS_DIR = Path(r"D:\Đầu Não (không xóa)\assets")
GEOJSON_PATH = ASSETS_DIR / "maps" / "countries.geojson"

# Cache dữ liệu tiền xử lý tọa độ chuẩn hóa [0, 1]
_CACHED_COUNTRIES = None

def get_normalized_countries():
    """Tải và tiền tính toán tọa độ Mercator chuẩn hóa [0, 1] một lần duy nhất trong RAM"""
    global _CACHED_COUNTRIES
    if _CACHED_COUNTRIES is not None:
        return _CACHED_COUNTRIES

    if not GEOJSON_PATH.exists():
        _CACHED_COUNTRIES = []
        return _CACHED_COUNTRIES

    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    countries = []
    for feat in data.get("features", []):
        props = feat.get("properties", {})
        geom = feat.get("geometry", {})
        t = geom.get("type", "")
        coords = geom.get("coordinates", [])
        polys = [coords] if t == "Polygon" else coords

        np_polys = []
        all_pts = []
        for poly in polys:
            pts = np.array(poly[0], dtype=np.float32)
            if len(pts) > 2:
                lons = pts[:, 0]
                lats = np.clip(pts[:, 1], -85.0, 85.0)
                lat_rad = np.radians(lats)
                merc_y = np.log(np.tan(np.pi / 4.0 + lat_rad / 2.0))
                norm_x = (lons + 180.0) / 360.0
                norm_y = (1.0 - merc_y / np.pi) * 0.5
                stacked = np.column_stack([norm_x, norm_y])
                np_polys.append(stacked)
                all_pts.append(pts)

        # Tính tâm trung bình
        if all_pts:
            concat_pts = np.vstack(all_pts)
            center_lon = float(np.mean(concat_pts[:, 0]))
            center_lat = float(np.mean(concat_pts[:, 1]))
        else:
            center_lon, center_lat = 0.0, 20.0

        countries.append({
            "name": props.get("name", ""),
            "iso2": props.get("ISO3166-1-Alpha-2", ""),
            "iso3": props.get("ISO3166-1-Alpha-3", ""),
            "center": (center_lon, center_lat),
            "polys": np_polys
        })

    _CACHED_COUNTRIES = countries
    return _CACHED_COUNTRIES


def find_country(query: str):
    """Tìm quốc gia theo tên hoặc ISO"""
    countries = get_normalized_countries()
    q = query.strip().lower()
    for c in countries:
        if q == c["name"].lower() or q == c["iso2"].lower() or q == c["iso3"].lower() or (q in c["name"].lower() and len(q) > 3):
            return c
    return None


def get_norm_center(lon, lat):
    lat = max(-85.0, min(85.0, lat))
    lat_rad = np.radians(lat)
    merc_y = np.log(np.tan(np.pi / 4.0 + lat_rad / 2.0))
    return (lon + 180.0) / 360.0, (1.0 - merc_y / np.pi) * 0.5


def render_geopolitical_map_clip(
    target_country="China",
    out_video_path=None,
    route_from=None,
    route_to=None,
    duration=3.5,
    fps=30,
    ratio="16:9"
) -> Path:
    """
    Xuất video bản đồ địa chính trị chuẩn phát sóng đa tỉ lệ (16:9 hoặc 9:16):
    - Đọc dữ liệu 258 nước từ countries.geojson.
    - Vectorized NumPy projection chạy cực mượt.
    - Đường bay cong Trans-Pacific Arc & Radar Sonar.
    """
    if ratio == "9:16":
        width, height = 1080, 1920
    else:
        width, height = 1920, 1080

    if out_video_path is None:
        out_video_path = Path(r"D:\Video thành phẩm") / f"map_{target_country}_{ratio.replace(':', 'x')}.mp4"
    else:
        out_video_path = Path(out_video_path)
    out_video_path.parent.mkdir(parents=True, exist_ok=True)

    countries = get_normalized_countries()
    target_data = find_country(target_country)
    
    if target_data:
        c_lon, c_lat = target_data["center"]
    else:
        c_lon, c_lat = 105.0, 20.0

    c_norm_x, c_norm_y = get_norm_center(c_lon, c_lat)

    # Route nếu có
    has_route = route_from is not None and route_to is not None
    p_from_lon, p_from_lat = 116.4, 39.9
    p_to_lon, p_to_lat = -77.0, 38.9
    if has_route:
        c1 = find_country(route_from) if isinstance(route_from, str) else None
        c2 = find_country(route_to) if isinstance(route_to, str) else None
        if c1: p_from_lon, p_from_lat = c1["center"]
        if c2: p_to_lon, p_to_lat = c2["center"]
        # Canh tâm ở giữa 2 điểm
        c_norm_x1, c_norm_y1 = get_norm_center(p_from_lon, p_from_lat)
        c_norm_x2, c_norm_y2 = get_norm_center(p_to_lon, p_to_lat)
        c_norm_x = (c_norm_x1 + c_norm_x2) * 0.5
        c_norm_y = (c_norm_y1 + c_norm_y2) * 0.5

    norm_from_x, norm_from_y = get_norm_center(p_from_lon, p_from_lat)
    norm_to_x, norm_to_y = get_norm_center(p_to_lon, p_to_lat)

    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))

    for f in range(total_frames):
        p = f / total_frames
        smooth_p = 0.5 - 0.5 * math.cos(p * math.pi)
        cur_zoom = 1.05 + smooth_p * 1.65

        frame = np.zeros((height, width, 3), dtype=np.uint8)
        frame[:] = (18, 14, 10) # Nền tối Navy

        # Vẽ các quốc gia bằng phép nhân ma trận NumPy
        for c in countries:
            is_target = (c == target_data)
            for poly in c["polys"]:
                px = ((poly[:, 0] - c_norm_x) * cur_zoom + 0.5) * width
                py = ((poly[:, 1] - c_norm_y) * cur_zoom + 0.5) * height
                pts = np.column_stack([px, py]).astype(np.int32)
                
                # Chỉ vẽ nếu nằm trong hoặc gần khung nhìn
                if np.max(pts[:, 0]) >= 0 and np.min(pts[:, 0]) < width and np.max(pts[:, 1]) >= 0 and np.min(pts[:, 1]) < height:
                    if is_target:
                        cv2.fillPoly(frame, [pts], (25, 45, 65))
                        cv2.polylines(frame, [pts], True, (0, 215, 255), 2)
                    else:
                        cv2.fillPoly(frame, [pts], (30, 24, 20))
                        cv2.polylines(frame, [pts], True, (55, 45, 38), 1)

        # Radar Sonar tại mục tiêu
        t_px = int(((get_norm_center(c_lon, c_lat)[0] - c_norm_x) * cur_zoom + 0.5) * width)
        t_py = int(((get_norm_center(c_lon, c_lat)[1] - c_norm_y) * cur_zoom + 0.5) * height)
        radar_p = (f * 0.05) % 1.0
        r_rad = int(180 * radar_p)
        if 0 <= t_px < width and 0 <= t_py < height:
            if r_rad > 4:
                alpha = max(0.0, 1.0 - radar_p)
                col = (int(0 * alpha), int(215 * alpha), int(255 * alpha))
                cv2.circle(frame, (t_px, t_py), r_rad, col, 1)
            cv2.circle(frame, (t_px, t_py), 5, (255, 255, 255), -1)
            cv2.circle(frame, (t_px, t_py), 9, (0, 215, 255), 2)

        # Đường bay cong Arc
        if has_route:
            f_px = int(((norm_from_x - c_norm_x) * cur_zoom + 0.5) * width)
            f_py = int(((norm_from_y - c_norm_y) * cur_zoom + 0.5) * height)
            to_px = int(((norm_to_x - c_norm_x) * cur_zoom + 0.5) * width)
            to_py = int(((norm_to_y - c_norm_y) * cur_zoom + 0.5) * height)

            mid_x = (f_px + to_px) // 2
            mid_y = min(f_py, to_py) - int(height * 0.22)

            arc_pts = []
            num_steps = 30
            for i in range(num_steps + 1):
                t_b = i / num_steps
                bx = int((1 - t_b)**2 * f_px + 2 * (1 - t_b) * t_b * mid_x + t_b**2 * to_px)
                by = int((1 - t_b)**2 * f_py + 2 * (1 - t_b) * t_b * mid_y + t_b**2 * to_py)
                arc_pts.append((bx, by))

            draw_len = int(num_steps * min(1.0, p * 1.3))
            for i in range(0, draw_len, 2):
                if i + 1 < len(arc_pts):
                    cv2.line(frame, arc_pts[i], arc_pts[i+1], (0, 230, 255), 2)
            if draw_len < len(arc_pts):
                head = arc_pts[draw_len]
                cv2.circle(frame, head, 6, (255, 255, 255), -1)
                cv2.circle(frame, head, 12, (0, 215, 255), 2)

        # HUD Telemetry
        hud_text = f"TARGET: {target_country.upper()} // LAT {c_lat:.2f}N  LON {c_lon:.2f}E"
        cv2.putText(frame, hud_text, (40, height - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (200, 220, 240), 2)
        cv2.putText(frame, f"RATIO: {ratio} // MASTER GEOPOLITICAL VECTOR", (40, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (100, 150, 200), 1)

        out_writer.write(frame)

    out_writer.release()
    print(f"[MAP 3D OK] Exported {ratio} video ({duration}s): {out_video_path}")
    return out_video_path


def render_3d_satellite_flythrough(satellite_img_path, target_coords, location_name, out_video_path, duration=4.0, fps=30, ratio="16:9"):
    """Dựng video bay lượn 3D trên ảnh vệ tinh thực tế nghiêng 45 độ"""
    if ratio == "9:16":
        width, height = 1080, 1920
    else:
        width, height = 1920, 1080

    if not os.path.exists(satellite_img_path):
        return render_geopolitical_map_clip(target_country="China", out_video_path=out_video_path, duration=duration, fps=fps, ratio=ratio)

    data = np.fromfile(satellite_img_path, dtype=np.uint8)
    sat_img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    h, w = sat_img.shape[:2]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_writer = cv2.VideoWriter(str(out_video_path), fourcc, fps, (width, height))
    total_frames = int(duration * fps)

    for f in range(total_frames):
        t = f / fps
        p = t / duration

        tilt_ratio = 0.32 + p * 0.08
        src_pts = np.float32([[0, 0], [w, 0], [w, h], [0, h]])
        dst_pts = np.float32([
            [int(width * tilt_ratio), int(height * 0.16)],
            [int(width * (1 - tilt_ratio)), int(height * 0.16)],
            [width, height],
            [0, height]
        ])

        M_proj = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(sat_img, M_proj, (width, height), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(12, 16, 22))
        warped = cv2.convertScaleAbs(warped, alpha=0.75, beta=-10)

        target_x = int(width * 0.5)
        target_y = int(height * 0.62)
        radar_p = (t * 0.8) % 1.0
        r_radius = int(width * 0.12 * radar_p)
        if r_radius > 4:
            cv2.ellipse(warped, (target_x, target_y), (r_radius, int(r_radius * 0.4)), 0, 0, 360, (0, 220, 255), 2)

        out_writer.write(warped)

    out_writer.release()
    print(f"[MAP 3D OK] Flythrough rendered ({ratio}): {out_video_path}")
    return out_video_path


if __name__ == "__main__":
    out_16x9 = Path(r"D:\Video thành phẩm\test_map_china_us_16x9.mp4")
    out_9x16 = Path(r"D:\Video thành phẩm\test_map_vietnam_9x16.mp4")
    print("Testing 16:9 Vector Map with Trans-Pacific Arc...")
    render_geopolitical_map_clip(target_country="China", route_from="China", route_to="United States", out_video_path=out_16x9, duration=3.0, ratio="16:9")
    print("Testing 9:16 Vector Map...")
    render_geopolitical_map_clip(target_country="Vietnam", out_video_path=out_9x16, duration=3.0, ratio="9:16")
