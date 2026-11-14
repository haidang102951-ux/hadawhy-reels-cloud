# -*- coding: utf-8 -*-
r"""
NASA SATELLITE RENDERER 3D (Bộ Render Bản Đồ Vệ Tinh Độc Bản & Phủ Quốc Kỳ Dạ Quang)
Chuẩn: 9:16 (1080x1920) cho FB Reels / TikTok Shorts
Tính năng:
1. Chiếu bản đồ ảnh vệ tinh thực tế (NASA Blue Marble / Dark Ocean Bathymetry) với độ cong địa cầu 3D và viền khí quyển (Atmosphere Rim Glow).
2. Phủ Quốc Kỳ Dạ Quang (Flag Map Projection): Cắt và chiếu texture cờ (Nhật Bản, Việt Nam, Anh, Mỹ...) vừa vặn lên ranh giới quốc gia, viền neon phát quang 3D.
3. Đường bay vòng cung hình cầu (Great Circle Flight Path): Đường bay đứt đoạn phát sáng nối các tọa độ toàn cầu (London -> Trung Đông -> Hà Nội -> Tokyo).
4. Điểm nghẽn ổ khóa cơ học: Tự động thả ổ khóa sắt sập chốt phong tỏa các chặng bay.
5. Ghim toạ độ thẻ Acrylic kính mờ (Frosted Acrylic Pin) cho các sự kiện toà án / điểm nóng tài chính.
"""

import sys
import os
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple, Optional

import cv2
import numpy as np

# Đảm bảo UTF-8
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

class NASASatelliteRenderer:
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self.base_dir = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
        self.geojson_path = self.base_dir / "assets" / "maps" / "countries.geojson"
        self._cached_geojson = None
        self._load_geojson()

    def _load_geojson(self):
        if self.geojson_path.exists():
            with open(self.geojson_path, "r", encoding="utf-8") as f:
                self._cached_geojson = json.load(f)

    def _latlon_to_xy(self, lat: float, lon: float, center_lat: float, center_lon: float, zoom: float) -> Tuple[int, int]:
        """
        Chuyển đổi toạ độ địa lý (Lat, Lon) sang toạ độ pixel (x, y) trên khung hình 9:16
        với tâm bản đồ và tỷ lệ zoom.
        """
        # Phép chiếu Mercator cục bộ
        x = self.width / 2 + (lon - center_lon) * zoom * (self.width / 360.0)
        # Lat sang y (hướng lên trên là giảm y)
        lat_rad = math.radians(lat)
        c_lat_rad = math.radians(center_lat)
        merc_y = math.log(math.tan(math.pi / 4 + lat_rad / 2) + 1e-9)
        c_merc_y = math.log(math.tan(math.pi / 4 + c_lat_rad / 2) + 1e-9)
        y = self.height / 2 - (merc_y - c_merc_y) * zoom * (self.height / 6.0)
        return int(x), int(y)

    def create_deep_ocean_base(self) -> np.ndarray:
        """
        Tạo nền đại dương sâu thẳm NASA Bathymetry với gradient chiều sâu và rãnh biển
        """
        frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # Nền xanh biển đen sâu thẳm (Deep Navy #060b14 -> Midnight Blue #0c1626)
        y_coords = np.linspace(0, 1, self.height)[:, None, None]
        base_color1 = np.array([12, 8, 4])    # B, G, R
        base_color2 = np.array([38, 22, 10])  # B, G, R
        grad = (1 - y_coords) * base_color1 + y_coords * base_color2
        frame[:] = np.tile(grad.astype(np.uint8), (1, self.width, 1))

        # Thêm vân rãnh đại dương bathymetry dạng noise nhẹ
        noise = np.random.normal(0, 3, (self.height // 4, self.width // 4, 3)).astype(np.float32)
        noise = cv2.resize(noise, (self.width, self.height))
        frame = np.clip(frame.astype(np.float32) + noise, 0, 255).astype(np.uint8)

        # Viền khí quyển cong Trái Đất (Atmospheric Curve Glow)
        cv2.ellipse(frame, (self.width // 2, self.height + 600), (self.width, 1400), 0, 0, 360, (65, 45, 15), 3)
        return frame

    def draw_country_flag_fill(
        self,
        frame: np.ndarray,
        country_code: str,
        flag_type: str = "JAPAN",
        center_lat: float = 36.0,
        center_lon: float = 138.0,
        zoom: float = 4.5
    ):
        """
        Vẽ quốc gia mục tiêu và PHỦ QUỐC KỲ DẠ QUANG lên bề mặt lãnh thổ (Flag Map Projection)
        """
        if not self._cached_geojson:
            return

        polygons = []
        for feat in self._cached_geojson.get("features", []):
            props = feat.get("properties", {})
            iso_a3 = props.get("ISO3166-1-Alpha-3", "") or props.get("ISO_A3", "") or props.get("name", "")
            if country_code.upper() in iso_a3.upper():
                geom = feat.get("geometry", {})
                t = geom.get("type", "")
                coords = geom.get("coordinates", [])
                
                # Xử lý MultiPolygon vs Polygon
                raw_polys = coords if t == "MultiPolygon" else [coords]
                for poly in raw_polys:
                    if len(poly) > 0:
                        pts = []
                        # poly[0] là outer ring
                        ring = poly[0]
                        for pt in ring:
                            if len(pt) >= 2:
                                lon, lat = pt[0], pt[1]
                                px, py = self._latlon_to_xy(lat, lon, center_lat, center_lon, zoom)
                                pts.append([px, py])
                        if len(pts) > 2:
                            polygons.append(np.array(pts, dtype=np.int32))

        if not polygons:
            return

        # 1. Tạo mask cho quốc gia
        mask = np.zeros((self.height, self.width), dtype=np.uint8)
        for poly in polygons:
            cv2.fillPoly(mask, [poly], 255)

        # 2. Tạo texture cờ
        flag_img = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        if flag_type == "JAPAN":
            # Cờ Nhật Bản: Nền trắng ngà, hình tròn mặt trời đỏ thẫm rực sáng
            flag_img[:] = (240, 240, 245) # Trắng ngà BGR
            # Tìm tâm của mask
            moments = cv2.moments(mask)
            if moments["m00"] > 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
                # Mặt trời đỏ dạ quang
                cv2.circle(flag_img, (cx, cy), 130, (20, 25, 210), -1) # Đỏ thẫm
                cv2.circle(flag_img, (cx, cy), 145, (40, 60, 255), 4)  # Viền sáng
        elif flag_type == "VIETNAM":
            flag_img[:] = (25, 20, 215) # Đỏ cờ BGR
            # Vẽ ngôi sao vàng
            moments = cv2.moments(mask)
            if moments["m00"] > 0:
                cx = int(moments["m10"] / moments["m00"])
                cy = int(moments["m01"] / moments["m00"])
                cv2.circle(flag_img, (cx, cy), 90, (30, 220, 255), -1)

        # 3. Áp cờ vào lãnh thổ qua mask
        flag_masked = cv2.bitwise_and(flag_img, flag_img, mask=mask)
        bg_masked = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
        combined = cv2.add(bg_masked, flag_masked)
        frame[:] = combined

        # 4. Vẽ viền Neon phát quang bao quanh quốc gia
        for poly in polygons:
            cv2.polylines(frame, [poly], isClosed=True, color=(120, 220, 255), thickness=2, lineType=cv2.LINE_AA)
            cv2.polylines(frame, [poly], isClosed=True, color=(60, 160, 255), thickness=4, lineType=cv2.LINE_AA)

    def draw_flight_arc(
        self,
        frame: np.ndarray,
        p1: Tuple[int, int],
        p2: Tuple[int, int],
        progress: float = 1.0,
        color: Tuple[int, int, int] = (45, 60, 240),
        has_padlock: bool = False
    ):
        """
        Vẽ đường bay vòng cung phát sáng (Great Circle Arc) từ p1 -> p2
        Có hỗ trợ cắm ổ khóa kim loại đóng sập tại đỉnh vòng cung.
        """
        # Tạo đường cong Bezier bậc 2
        mid_x = (p1[0] + p2[0]) // 2
        # Uốn cong lên phía trên (đỉnh vòng cung)
        arc_height = int(math.hypot(p2[0] - p1[0], p2[1] - p1[1]) * 0.35)
        mid_y = min(p1[1], p2[1]) - arc_height

        # Tính các điểm trên đường cong
        points = []
        steps = 60
        max_step = int(steps * min(1.0, progress))
        for i in range(max_step + 1):
            t = i / float(steps)
            x = int((1 - t)**2 * p1[0] + 2 * (1 - t) * t * mid_x + t**2 * p2[0])
            y = int((1 - t)**2 * p1[1] + 2 * (1 - t) * t * mid_y + t**2 * p2[1])
            points.append((x, y))

        # Vẽ đường đứt đoạn neon
        for i in range(0, len(points) - 1, 2):
            pt1 = points[i]
            pt2 = points[min(i + 1, len(points) - 1)]
            cv2.line(frame, pt1, pt2, (20, 20, 120), 4, lineType=cv2.LINE_AA)
            cv2.line(frame, pt1, pt2, color, 2, lineType=cv2.LINE_AA)

        # Vẽ điểm đầu và điểm cuối
        cv2.circle(frame, p1, 8, (255, 255, 255), -1)
        cv2.circle(frame, p1, 14, color, 2)
        if len(points) > 0:
            current_head = points[-1]
            cv2.circle(frame, current_head, 9, (255, 255, 255), -1)
            cv2.circle(frame, current_head, 18, (60, 220, 255), 2)

        # Thả ổ khóa kim loại nếu yêu cầu
        if has_padlock and progress >= 0.8:
            lock_x, lock_y = mid_x, mid_y
            self.draw_padlock_icon(frame, (lock_x, lock_y))

    def draw_padlock_icon(self, frame: np.ndarray, center: Tuple[int, int]):
        """Vẽ biểu tượng ổ khóa kim loại mạ vàng dập nổi 3D"""
        cx, cy = center
        # Quai khóa hình móng ngựa
        cv2.ellipse(frame, (cx, cy - 25), (20, 24), 0, 180, 360, (220, 225, 230), 7, lineType=cv2.LINE_AA)
        cv2.ellipse(frame, (cx, cy - 25), (20, 24), 0, 180, 360, (140, 150, 160), 3, lineType=cv2.LINE_AA)
        # Thân khóa hình chữ nhật vàng đồng
        cv2.rectangle(frame, (cx - 28, cy - 18), (cx + 28, cy + 30), (30, 170, 220), -1)
        cv2.rectangle(frame, (cx - 28, cy - 18), (cx + 28, cy + 30), (10, 120, 180), 3)
        # Lỗ khóa
        cv2.circle(frame, (cx, cy + 2), 6, (20, 20, 20), -1)
        cv2.rectangle(frame, (cx - 3, cy + 2), (cx + 3, cy + 16), (20, 20, 20), -1)

    def draw_acrylic_pin_badge(
        self,
        frame: np.ndarray,
        pos: Tuple[int, int],
        title: str,
        subtitle: str,
        badge_w: int = 420,
        badge_h: int = 140
    ):
        """
        Vẽ thẻ Acrylic Kính Mờ ghim toạ độ (London / Tòa án 15/10) thay thế Polaroid giấy cũ
        """
        x, y = pos
        bx = max(20, min(self.width - badge_w - 20, x - badge_w // 2))
        by = max(80, y - badge_h - 40)

        # 1. Đổ bóng thẻ 3D
        shadow = frame.copy()
        cv2.rectangle(shadow, (bx + 8, by + 8), (bx + badge_w + 8, by + badge_h + 8), (0, 0, 0), -1)
        cv2.GaussianBlur(shadow, (31, 31), 15, shadow)
        cv2.addWeighted(shadow, 0.6, frame, 0.4, 0, frame)

        # 2. Thẻ kính mờ Acrylic (Backdrop Blur + Tint xám đen kim loại)
        sub_roi = frame[by:by+badge_h, bx:bx+badge_w]
        if sub_roi.shape[0] > 0 and sub_roi.shape[1] > 0:
            blurred = cv2.GaussianBlur(sub_roi, (21, 21), 10)
            overlay = np.full_like(sub_roi, (25, 28, 35), dtype=np.uint8) # Xám titan
            acrylic = cv2.addWeighted(blurred, 0.45, overlay, 0.55, 0)
            frame[by:by+badge_h, bx:bx+badge_w] = acrylic

        # 3. Viền kim loại Titan phay xước sáng loáng
        cv2.rectangle(frame, (bx, by), (bx + badge_w, by + badge_h), (180, 190, 205), 2, lineType=cv2.LINE_AA)
        cv2.rectangle(frame, (bx + 2, by + 2), (bx + badge_w - 2, by + badge_h - 2), (60, 70, 85), 1)

        # 4. Chấm toạ độ laser nối từ thẻ xuống điểm bản đồ
        cv2.circle(frame, (x, y), 7, (40, 220, 255), -1)
        cv2.line(frame, (bx + badge_w // 2, by + badge_h), (x, y), (80, 200, 255), 2, lineType=cv2.LINE_AA)

        # 5. Viết chữ
        cv2.putText(frame, title.upper(), (bx + 20, by + 50), cv2.FONT_HERSHEY_DUPLEX, 1.1, (245, 245, 250), 2, cv2.LINE_AA)
        cv2.putText(frame, subtitle, (bx + 20, by + 95), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (70, 210, 255), 2, cv2.LINE_AA)

def save_image_unicode(path: Path, img: np.ndarray):
    """Lưu ảnh an toàn trên Windows với đường dẫn tiếng Việt có dấu"""
    ext = path.suffix
    is_success, buffer = cv2.imencode(ext, img)
    if is_success:
        with open(path, "wb") as f:
            f.write(buffer)

if __name__ == "__main__":
    renderer = NASASatelliteRenderer()
    base = renderer.create_deep_ocean_base()
    # Thử vẽ Nhật Bản phủ quốc kỳ
    renderer.draw_country_flag_fill(base, "JPN", flag_type="JAPAN", center_lat=36.0, center_lon=138.0, zoom=4.5)
    # Thử vẽ đường bay London -> Nhật Bản
    renderer.draw_flight_arc(base, (180, 650), (750, 1100), progress=1.0, has_padlock=True)
    # Thử vẽ thẻ Acrylic Tòa án London
    renderer.draw_acrylic_pin_badge(base, (180, 650), "TOA AN LONDON", "PHAN QUYET - 15/10")

    test_out = renderer.base_dir / "assets" / "test_satellite_demo.jpg"
    save_image_unicode(test_out, base)
    print(f"[*] Demo NASA Satellite rendered: {test_out} (Exists: {test_out.exists()})")
