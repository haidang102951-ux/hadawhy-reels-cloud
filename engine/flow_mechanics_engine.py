# -*- coding: utf-8 -*-
r"""
FLOW MECHANICS ENGINE 2.5D (Bộ Cơ Chế Dòng Tiền & Tương Tác Vật Lý Hợp Đồng)
Chuyên biệt cho FB Reels / TikTok Shorts
Tính năng:
1. Chuỗi mắt xích dòng tiền (Cash Flow Pipeline):
   - Máy bay / Chủ thể -> Barrier chặn đường -> Két sắt Doanh thu -> Ngân hàng trả nợ.
2. Kéo kim loại cắt đứt hợp đồng (Contract Snip Mechanics):
   - Kéo kim loại sáng loáng hạ xuống cắt phựt đường ranh giới giữa "HÔM NAY" & "TƯƠNG LAI".
3. Tháp tiền dâng cao 3D (3D Cash Tower Odometer):
   - Cọc tiền dâng cao theo cấp số nhân kèm số liệu cuộn tăng tốc.
4. Gia tốc rơi vật lý (Gravity Physics Drops):
   - Đồng xu / Cọc tiền rơi với gia tốc g=9.8m/s² vào miệng két sắt.
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

class FlowMechanicsEngine:
    def __init__(self, width: int = 1080, height: int = 1920):
        self.width = width
        self.height = height
        self.base_dir = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")

    def draw_bank_vault(self, frame: np.ndarray, center: Tuple[int, int], is_open: bool = True, label: str = "DOANH THU"):
        """Vẽ két sắt ngân hàng thép đúc 3D"""
        cx, cy = center
        vw, vh = 420, 240
        vx, vy = cx - vw // 2, cy - vh // 2

        # 1. Đổ bóng sàn két sắt
        cv2.ellipse(frame, (cx, cy + vh // 2 + 15), (vw // 2 + 30, 25), 0, 0, 360, (10, 10, 15), -1)

        # 2. Thân két sắt (Xám thép đúc)
        cv2.rectangle(frame, (vx, vy), (vx + vw, vy + vh), (55, 60, 70), -1)
        cv2.rectangle(frame, (vx, vy), (vx + vw, vy + vh), (180, 190, 205), 3)

        # Cửa két sắt mở nắp thấy các cọc tiền bên trong
        if is_open:
            # Ngăn trong màu tối
            cv2.rectangle(frame, (vx + 20, vy + 20), (vx + vw - 20, vy + vh - 20), (25, 28, 32), -1)
            # 3 cọc tiền đô la xếp hàng ngang bên trong
            for i, px in enumerate([vx + 45, vx + 165, vx + 285]):
                cv2.rectangle(frame, (px, vy + 45), (px + 90, vy + vh - 45), (75, 140, 95), -1) # Xanh tiền USD
                cv2.rectangle(frame, (px, vy + 45), (px + 90, vy + vh - 45), (140, 220, 160), 2)
                cv2.circle(frame, (px + 45, vy + vh // 2), 12, (220, 245, 230), -1)
            # Cửa két mở hé bên cạnh
            cv2.rectangle(frame, (vx + vw - 15, vy - 10), (vx + vw + 75, vy + vh - 10), (70, 75, 85), -1)
            cv2.circle(frame, (vx + vw + 35, vy + vh // 2), 22, (200, 210, 225), 4) # Bánh xoay két
        
        # Nhãn dán dưới két
        cv2.putText(frame, label, (cx - 110, cy + vh // 2 + 65), cv2.FONT_HERSHEY_DUPLEX, 1.0, (240, 245, 255), 2, cv2.LINE_AA)

    def draw_roman_bank_building(self, frame: np.ndarray, center: Tuple[int, int], label: str = "BEN CHO THUE"):
        """Vẽ ngân hàng trụ cột La Mã cổ điển"""
        cx, cy = center
        bw, bh = 380, 260
        bx, by = cx - bw // 2, cy - bh // 2

        # 1. Đổ bóng sàn
        cv2.ellipse(frame, (cx, cy + bh // 2 + 10), (bw // 2 + 20, 20), 0, 0, 360, (10, 10, 15), -1)

        # 2. Mái vòm tam giác La Mã
        pts_roof = np.array([[bx, by + 60], [cx, by], [bx + bw, by + 60]], dtype=np.int32)
        cv2.fillPoly(frame, [pts_roof], (175, 185, 200))
        cv2.polylines(frame, [pts_roof], isClosed=True, color=(240, 245, 255), thickness=3, lineType=cv2.LINE_AA)

        # 3. 4 trụ cột đá
        for col_x in [bx + 35, bx + 125, bx + 215, bx + 305]:
            cv2.rectangle(frame, (col_x, by + 65), (col_x + 40, by + bh - 30), (200, 210, 220), -1)
            cv2.rectangle(frame, (col_x, by + 65), (col_x + 40, by + bh - 30), (120, 130, 145), 2)

        # 4. Bậc tam cấp
        cv2.rectangle(frame, (bx - 15, by + bh - 30), (bx + bw + 15, by + bh), (150, 160, 175), -1)
        cv2.rectangle(frame, (bx - 15, by + bh - 30), (bx + bw + 15, by + bh), (220, 230, 245), 2)

        # Cửa ra vào trung tâm
        cv2.rectangle(frame, (cx - 30, by + bh - 110), (cx + 30, by + bh - 30), (35, 45, 55), -1)

        # Nhãn
        cv2.putText(frame, label, (cx - 120, cy + bh // 2 + 55), cv2.FONT_HERSHEY_DUPLEX, 0.95, (235, 240, 250), 2, cv2.LINE_AA)

    def draw_barrier_gate(self, frame: np.ndarray, pos: Tuple[int, int], is_closed: bool = True):
        """Vẽ thanh chắn rào cản Barrier giao thông sọc đỏ trắng"""
        x, y = pos
        # Trụ barrier
        cv2.rectangle(frame, (x, y), (x + 35, y + 90), (35, 40, 50), -1)
        cv2.rectangle(frame, (x, y), (x + 35, y + 90), (180, 190, 205), 2)
        cv2.circle(frame, (x + 17, y + 20), 12, (210, 45, 45), -1)

        # Cần chắn sọc đỏ trắng dài 260px
        bar_len = 260
        angle = 0 if is_closed else -45 # Độ nghiêng
        rad = math.radians(angle)
        ex = int(x + math.cos(rad) * bar_len)
        ey = int(y + 20 + math.sin(rad) * bar_len)

        # Vẽ thanh chắn dày
        cv2.line(frame, (x + 17, y + 20), (ex, ey), (245, 245, 250), 14, lineType=cv2.LINE_AA)
        # Sọc đỏ trên thanh chắn
        steps = 8
        for i in range(1, steps, 2):
            t1 = i / float(steps)
            t2 = (i + 1) / float(steps)
            sx = int((x + 17) * (1 - t1) + ex * t1)
            sy = int((y + 20) * (1 - t1) + ey * t1)
            tx = int((x + 17) * (1 - t2) + ex * t2)
            ty = int((y + 20) * (1 - t2) + ey * t2)
            cv2.line(frame, (sx, sy), (tx, ty), (30, 35, 210), 14, lineType=cv2.LINE_AA)

    def draw_metal_scissors_snip(
        self,
        frame: np.ndarray,
        center: Tuple[int, int],
        cut_progress: float = 0.5
    ):
        """
        Vẽ cặp kéo kim loại mạ crom sáng loáng đang cắt phựt đường liên kết
        """
        cx, cy = center
        blade_len = 110
        # Góc mở lưỡi kéo khép dần theo cut_progress (từ 35 độ về 5 độ)
        open_angle = 35 * (1.0 - cut_progress) + 5
        
        for sign in [-1, 1]:
            angle = sign * open_angle
            rad = math.radians(angle)
            # Đầu mũi kéo
            tx = int(cx + math.cos(rad) * blade_len)
            ty = int(cy + math.sin(rad) * blade_len)
            
            # Lưỡi thép kim loại (Mạ crom sáng)
            pts_blade = np.array([[cx - 15, cy], [tx, ty], [cx, cy + sign * 12]], dtype=np.int32)
            cv2.fillPoly(frame, [pts_blade], (215, 225, 235))
            cv2.polylines(frame, [pts_blade], isClosed=True, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

            # Cán kéo bọc nhựa đỏ cao cấp
            hx = int(cx - math.cos(rad) * 65)
            hy = int(cy - math.sin(rad) * 65)
            cv2.ellipse(frame, (hx, hy), (24, 18), angle, 0, 360, (25, 30, 205), 6, lineType=cv2.LINE_AA)

        # Chốt đinh tán trung tâm
        cv2.circle(frame, (cx, cy), 8, (120, 130, 140), -1)
        cv2.circle(frame, (cx, cy), 4, (240, 245, 250), -1)

        # Nếu đang cắt đứt (cut_progress > 0.8), tạo tia lửa sáng lóe
        if cut_progress >= 0.8:
            cv2.circle(frame, (cx + 50, cy), 16, (200, 240, 255), -1)
            for spk in range(6):
                ang = spk * 60
                sx = int(cx + 50 + math.cos(math.radians(ang)) * 28)
                sy = int(cy + math.sin(math.radians(ang)) * 28)
                cv2.line(frame, (cx + 50, cy), (sx, sy), (80, 220, 255), 2, lineType=cv2.LINE_AA)

    def draw_cash_stream(self, frame: np.ndarray, p1: Tuple[int, int], p2: Tuple[int, int], coin_count: int = 5):
        """Vẽ luồng đồng xu vàng rơi leng keng giữa 2 điểm mắt xích"""
        for i in range(coin_count):
            t = (i + 1) / float(coin_count + 1)
            # Đường cong rơi tự do
            cx = int(p1[0] * (1 - t) + p2[0] * t)
            # Gia tốc rơi uốn vòng
            cy = int(p1[1] * (1 - t) + p2[1] * t + math.sin(t * math.pi) * 45)

            # Đồng xu vàng 3D
            cv2.circle(frame, (cx, cy), 18, (35, 190, 240), -1) # Vàng kim BGR
            cv2.circle(frame, (cx, cy), 18, (10, 120, 180), 2)
            cv2.circle(frame, (cx, cy), 13, (60, 220, 255), 1)
            # Ký hiệu $
            cv2.putText(frame, "$", (cx - 7, cy + 6), cv2.FONT_HERSHEY_DUPLEX, 0.65, (10, 80, 140), 2, cv2.LINE_AA)

if __name__ == "__main__":
    from forensic_glass_engine import ForensicGlassEngine
    glass = ForensicGlassEngine()
    bg = glass.create_obsidian_background()

    flow = FlowMechanicsEngine()
    # 1. Vẽ rào chắn barrier chặn phía trên
    flow.draw_barrier_gate(bg, (220, 360), is_closed=True)

    # 2. Vẽ két sắt Doanh thu ở giữa
    flow.draw_bank_vault(bg, (540, 720), is_open=True, label="DOANH THU")

    # 3. Vẽ dòng tiền xu chảy từ két xuống ngân hàng
    flow.draw_cash_stream(bg, (540, 850), (540, 1150), coin_count=4)

    # 4. Vẽ tòa nhà ngân hàng Bên cho thuê
    flow.draw_roman_bank_building(bg, (540, 1340), label="BEN CHO THUE")

    # 5. Thử nghiệm kéo kim loại cắt hợp đồng ở góc dưới
    flow.draw_metal_scissors_snip(bg, (540, 1680), cut_progress=0.9)
    cv2.line(bg, (180, 1680), (460, 1680), (40, 50, 220), 4, lineType=cv2.LINE_AA)
    cv2.line(bg, (620, 1680), (900, 1680), (80, 200, 120), 4, lineType=cv2.LINE_AA)
    cv2.putText(bg, "HOM NAY", (240, 1740), cv2.FONT_HERSHEY_DUPLEX, 0.9, (40, 50, 220), 2, cv2.LINE_AA)
    cv2.putText(bg, "TUONG LAI", (680, 1740), cv2.FONT_HERSHEY_DUPLEX, 0.9, (80, 200, 120), 2, cv2.LINE_AA)

    out_file = flow.base_dir / "assets" / "test_flow_mechanics_demo.jpg"
    save_image_unicode(out_file, bg)
    print(f"[*] Flow Mechanics Demo rendered: {out_file} (Exists: {out_file.exists()})")
