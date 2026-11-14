# -*- coding: utf-8 -*-
r"""
FORENSIC GLASS ENGINE (Bộ Đồ Họa Độc Bản Thẻ Kính Mờ Acrylic & Tem Niêm Phong Pháp Lý)
Định hình ADN độc bản kênh FB Reels: "Forensic Glass Noir"
Thay thế hoàn toàn: Băng keo giấy xé viền (Paper Tape) & Nền ô ly than chì rẻ tiền của Finpath.
Tính năng:
1. Thẻ Kính Mờ Acrylic Titan (Frosted Acrylic Plate):
   - Đúc viền kim loại Titan phay xước sáng loáng.
   - Hiệu ứng Backdrop Blur khúc xạ ánh sáng nền mờ ảo.
   - Vệt sáng kim loại Light Sweep 3D quét qua bề mặt.
   - Khắc chìm mã số hồ sơ pháp lý (#CASE-082, EXHIBIT A).
2. Tem Niêm Phong Bảo Mật Pháp Lý (Forensic Security Holographic Seal):
   - Mã vạch Barcode dập nổi độ nét cao.
   - Dấu triện đỏ dạ quang niêm phong tài liệu điều tra.
3. Bảng Manh Mối 3D Obsidian Noir (Kế thừa & nâng tầm từ @lopphovlog):
   - Mặt kính đen phản chiếu mờ (Smoked Obsidian Studio).
   - Đinh ghim titan đầu tròn đỏ rực.
   - Sợi chỉ laser đỏ phát sáng dạ quang nối các nút chứng cứ.
"""

import sys
import os
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

def save_image_unicode(path: Path, img: np.ndarray):
    ext = path.suffix
    is_success, buffer = cv2.imencode(ext, img)
    if is_success:
        with open(path, "wb") as f:
            f.write(buffer)

class ForensicGlassEngine:
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self.base_dir = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")

    def create_obsidian_background(self) -> np.ndarray:
        """
        Tạo nền Obsidian Noir mặt kính đen phản chiếu mờ có khói sáng không gian sâu
        (Thay thế nền ô ly than chì học sinh của Finpath)
        """
        bg = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        # Gradient đen xám titan huyền ảo (#0a0c10 -> #121620)
        y = np.linspace(0, 1, self.height)[:, None, None]
        c1 = np.array([16, 12, 10])  # B, G, R
        c2 = np.array([32, 22, 18])  # B, G, R
        grad = (1 - y) * c1 + y * c2
        bg[:] = np.tile(grad.astype(np.uint8), (1, self.width, 1))

        # Thêm đốm sáng mờ (Specular Spotlight) ở góc trên
        center = (self.width // 2, 450)
        cv2.circle(bg, center, 480, (45, 32, 25), -1)
        bg = cv2.GaussianBlur(bg, (101, 101), 60)
        return bg

    def render_frosted_acrylic_plate(
        self,
        frame: np.ndarray,
        rect: Tuple[int, int, int, int],  # x, y, w, h
        title: str,
        subtitle: Optional[str] = None,
        case_id: str = "#EVIDENCE-082",
        highlight_color: Tuple[int, int, int] = (60, 210, 255), # Vàng kim BGR
        light_sweep_progress: float = 0.5
    ):
        """
        Vẽ thẻ Acrylic kính mờ đúc viền Titan và vệt sáng quét qua (Light Sweep)
        """
        x, y, w, h = rect
        # 1. Đổ bóng tiếp xúc sàn 3D 2 lớp (Contact Shadow + Ambient Shadow)
        shadow_mask = np.zeros((self.height, self.width), dtype=np.uint8)
        cv2.rectangle(shadow_mask, (x + 12, y + 16), (x + w + 12, y + h + 16), 180, -1)
        shadow_blurred = cv2.GaussianBlur(shadow_mask, (41, 41), 20)
        
        # Áp bóng vào frame
        for c in range(3):
            frame[:, :, c] = np.clip(frame[:, :, c].astype(np.int32) - (shadow_blurred * 0.75).astype(np.int32), 0, 255).astype(np.uint8)

        # 2. Vùng kính mờ Acrylic (Backdrop Blur)
        roi = frame[y:y+h, x:x+w]
        if roi.shape[0] > 0 and roi.shape[1] > 0:
            blurred_roi = cv2.GaussianBlur(roi, (25, 25), 12)
            # Tint xám titan cao cấp
            tint = np.full_like(roi, (26, 29, 36), dtype=np.uint8)
            acrylic_roi = cv2.addWeighted(blurred_roi, 0.4, tint, 0.6, 0)

            # 3. Vệt sáng quét qua (Light Sweep 3D)
            sweep_x = int(w * light_sweep_progress)
            for col in range(max(0, sweep_x - 40), min(w, sweep_x + 40)):
                dist = abs(col - sweep_x)
                sweep_alpha = max(0.0, 1.0 - dist / 40.0) * 0.45
                acrylic_roi[:, col] = np.clip(acrylic_roi[:, col].astype(np.float32) + sweep_alpha * 255, 0, 255).astype(np.uint8)

            frame[y:y+h, x:x+w] = acrylic_roi

        # 4. Viền kim loại Titan phay xước sáng loáng
        cv2.rectangle(frame, (x, y), (x + w, y + h), (190, 205, 220), 2, lineType=cv2.LINE_AA)
        cv2.rectangle(frame, (x + 2, y + 2), (x + w - 2, y + h - 2), (55, 65, 78), 1)

        # 4 đinh ốc titan ở 4 góc thẻ
        for cx, cy in [(x + 14, y + 14), (x + w - 14, y + 14), (x + 14, y + h - 14), (x + w - 14, y + h - 14)]:
            cv2.circle(frame, (cx, cy), 4, (180, 190, 205), -1)
            cv2.circle(frame, (cx, cy), 5, (40, 45, 55), 1)

        # 5. Khắc chìm mã hồ sơ pháp lý góc trên
        cv2.putText(frame, case_id, (x + 24, y + 36), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (140, 150, 165), 1, cv2.LINE_AA)

        # 6. Tiêu đề chính
        cv2.putText(frame, title, (x + 24, y + 85), cv2.FONT_HERSHEY_DUPLEX, 1.25, (250, 250, 255), 2, cv2.LINE_AA)

        # 7. Phụ đề / số liệu nếu có
        if subtitle:
            cv2.putText(frame, subtitle, (x + 24, y + 130), cv2.FONT_HERSHEY_SIMPLEX, 0.9, highlight_color, 2, cv2.LINE_AA)

    def render_security_seal_stamp(
        self,
        frame: np.ndarray,
        center: Tuple[int, int],
        text: str = "CONFIDENTIAL - 250M$",
        barcode: bool = True
    ):
        """
        Vẽ Tem Niêm Phong Bảo Mật Pháp Lý (Thay thế hoàn toàn băng keo dán giấy xé)
        """
        cx, cy = center
        sw, sh = 520, 95
        sx = cx - sw // 2
        sy = cy - sh // 2

        # 1. Nền tem Hologram Đỏ chu sa viền dạ quang
        seal_box = np.zeros((sh, sw, 3), dtype=np.uint8)
        seal_box[:] = (22, 25, 185) # Đỏ chu sa BGR
        
        # Viền răng cưa bảo mật
        cv2.rectangle(seal_box, (0, 0), (sw, sh), (45, 65, 255), 3)

        # 2. Vẽ mã vạch Barcode công nghệ cao
        if barcode:
            bx = 18
            for i in range(26):
                bw = np.random.choice([2, 4, 6])
                gap = np.random.choice([3, 5])
                if bx + bw < 140:
                    cv2.rectangle(seal_box, (bx, 15), (bx + bw, sh - 15), (240, 240, 250), -1)
                    bx += bw + gap

        # 3. Chữ niêm phong pháp lý
        cv2.putText(seal_box, text.upper(), (160, sh // 2 + 10), cv2.FONT_HERSHEY_DUPLEX, 0.95, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Áp seal lên frame
        frame[sy:sy+sh, sx:sx+sw] = cv2.addWeighted(frame[sy:sy+sh, sx:sx+sw], 0.15, seal_box, 0.85, 0)
        cv2.rectangle(frame, (sx, sy), (sx + sw, sy + sh), (80, 100, 255), 2, lineType=cv2.LINE_AA)

    def render_laser_pinboard_connection(
        self,
        frame: np.ndarray,
        pt1: Tuple[int, int],
        pt2: Tuple[int, int],
        label: Optional[str] = None
    ):
        """
        Vẽ mối nối điều tra chỉ đỏ Laser 3D giữa 2 manh mối (Kế thừa & Nâng cấp từ @lopphovlog)
        """
        # Sợi chỉ đỏ phát sáng dạ quang (Laser Thread)
        cv2.line(frame, pt1, pt2, (30, 25, 190), 5, lineType=cv2.LINE_AA) # Quầng sáng đỏ
        cv2.line(frame, pt1, pt2, (90, 110, 255), 2, lineType=cv2.LINE_AA) # Lõi sáng
        
        # Đinh ghim Titan đỏ ở 2 đầu
        for pt in [pt1, pt2]:
            cv2.circle(frame, pt, 12, (20, 20, 180), -1)
            cv2.circle(frame, pt, 6, (220, 230, 255), -1)
            cv2.circle(frame, pt, 14, (60, 80, 255), 2)

        if label:
            mx, my = (pt1[0] + pt2[0]) // 2, (pt1[1] + pt2[1]) // 2
            cv2.putText(frame, label, (mx - 60, my - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (230, 230, 240), 2, cv2.LINE_AA)

if __name__ == "__main__":
    engine = ForensicGlassEngine()
    bg = engine.create_obsidian_background()
    
    # 1. Thử vẽ thẻ Acrylic Kính Mờ 1
    engine.render_frosted_acrylic_plate(
        bg, (90, 320, 900, 180),
        title="KHOAN NO 250M USD",
        subtitle="PHAN QUYET TOA AN LONDON",
        case_id="#LEGAL-VIETJET-01",
        light_sweep_progress=0.65
    )

    # 2. Thử vẽ thẻ Acrylic Kính Mờ 2
    engine.render_frosted_acrylic_plate(
        bg, (90, 680, 900, 180),
        title="4 TAU BAY A321 NEO",
        subtitle="DUNG TEN CONG TY NHAT BAN",
        case_id="#ASSET-AIRCRAFT-04",
        highlight_color=(90, 240, 140), # Xanh ngọc
        light_sweep_progress=0.3
    )

    # 3. Nối sợi chỉ laser điều tra giữa 2 thẻ
    engine.render_laser_pinboard_connection(bg, (540, 500), (540, 680), label="TRANH CHAP PHAP LY")

    # 4. Thử dập tem niêm phong bảo mật
    engine.render_security_seal_stamp(bg, (540, 1020), text="TAM GIU QUOC TE", barcode=True)

    out_file = engine.base_dir / "assets" / "test_forensic_glass_demo.jpg"
    save_image_unicode(out_file, bg)
    print(f"[*] Forensic Glass Demo rendered: {out_file} (Exists: {out_file.exists()})")
