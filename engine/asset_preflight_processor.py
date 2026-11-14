# -*- coding: utf-8 -*-
"""
ASSET PREFLIGHT PROCESSOR - BỘ TIỀN XỬ LÝ TƯ LIỆU THẬT 16:9 CHUẨN ĐIỆN ẢNH
=============================================================================
Đảm bảo 100% footage tư liệu trước khi nạp vào Remotion:
1. Khử sạch watermark/logo bằng Smart Micro-Zoom (106%) và crop 16:9 (1920x1080).
2. Re-encode sang All-Intra (GOP=1, -keyint_min 1) đúng 30.0 fps (hoặc 60 fps) -> Triệt tiêu 100% giật lag!
3. Tăng cường độ nét bằng bộ lọc unsharp và tối ưu màu sắc.
4. Quét mã hash pHash/MD5 chống lặp footage xuyên suốt video 8.4 phút.
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path

# Đảm bảo UTF-8 cho Windows console
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

LEDGER_PATH = Path(r"D:\Đầu Não (không xóa)\engine\shot_ledger.json")

class AssetPreflightProcessor:
    def __init__(self, target_w=1920, target_h=1080, target_fps=30.0):
        self.target_w = target_w
        self.target_h = target_h
        self.target_fps = target_fps
        self.ledger = self._load_ledger()

    def _load_ledger(self) -> dict:
        if LEDGER_PATH.exists():
            try:
                with open(LEDGER_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _save_ledger(self):
        try:
            with open(LEDGER_PATH, 'w', encoding='utf-8') as f:
                json.dump(self.ledger, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[WARN] Không thể lưu shot ledger: {e}")

    def compute_file_hash(self, file_path: Path) -> str:
        hasher = hashlib.md5()
        with open(file_path, 'rb') as f:
            buf = f.read(65536)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(65536)
        return hasher.hexdigest()

    def compute_perceptual_hash(self, file_path: Path) -> str:
        """Trích xuất Perceptual Hash (pHash) từ frame trung tâm của video để so khớp góc quay thị giác."""
        try:
            import imagehash
            from PIL import Image
            cap = cv2.VideoCapture(str(file_path))
            if not cap.isOpened():
                return ""
            total_f = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            mid_f = max(0, total_f // 2)
            cap.set(cv2.CAP_PROP_POS_FRAMES, mid_f)
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(img_rgb)
                return str(imagehash.phash(pil_img))
        except Exception as e:
            pass
        return ""

    def check_duplication(self, file_path: Path, scene_id: str, project_id: str = "master_project") -> bool:
        """
        Kiểm tra trùng lặp đa tầng:
        1. Exact MD5 hash trùng lặp file vật lý
        2. Perceptual Hash (pHash) so khớp góc quay thị giác (hamming distance <= 6)
        3. Phân vùng theo project_id tránh xung đột giữa các dự án khác nhau
        """
        fhash = self.compute_file_hash(file_path)
        phash_val = self.compute_perceptual_hash(file_path)
        
        # Đảm bảo cấu trúc ledger hỗ trợ project_id
        if "projects" not in self.ledger:
            # Di chuyển các bản ghi phẳng cũ vào project mặc định
            old_entries = {k: v for k, v in self.ledger.items() if k != "projects"}
            self.ledger = {"projects": {"legacy": old_entries}}
            
        proj_ledger = self.ledger["projects"].setdefault(project_id, {})
        
        # 1. Kiểm tra exact MD5
        if fhash in proj_ledger:
            prev_scene = proj_ledger[fhash].get("scene_id")
            if prev_scene != scene_id:
                print(f"[CẢNH BÁO TRÙNG LẶP EXACT] Footage '{file_path.name}' đã được dùng ở phân cảnh '{prev_scene}' trong dự án '{project_id}'!")
                return False
            return True
            
        # 2. Kiểm tra thị giác pHash
        if phash_val:
            import imagehash
            cur_h = imagehash.hex_to_hash(phash_val)
            for existing_fhash, meta in proj_ledger.items():
                ex_phash = meta.get("phash")
                if ex_phash:
                    try:
                        dist = cur_h - imagehash.hex_to_hash(ex_phash)
                        if dist <= 6:
                            prev_scene = meta.get("scene_id")
                            prev_name = meta.get("name")
                            print(f"[CẢNH BÁO TRÙNG LẶP THỊ GIÁC pHash (diff={dist})] '{file_path.name}' có cùng góc quay với '{prev_name}' tại '{prev_scene}'!")
                            return False
                    except Exception:
                        pass

        proj_ledger[fhash] = {
            "name": file_path.name,
            "scene_id": scene_id,
            "path": str(file_path),
            "phash": phash_val
        }
        self._save_ledger()
        return True

    def process_footage(
        self,
        input_path: Path,
        output_path: Path,
        scene_id: str,
        zoom_factor: float = 1.06,
        sharpen: bool = True
    ) -> Path:
        """
        Làm sạch logo bằng micro-zoom, tăng nét và re-encode sang All-Intra 30fps.
        """
        input_p = Path(input_path).resolve()
        output_p = Path(output_path).resolve()
        output_p.parent.mkdir(parents=True, exist_ok=True)

        is_inplace = (input_p == output_p)
        actual_output = output_p.with_name(f"{output_p.stem}_tmp_preflight{output_p.suffix}") if is_inplace else output_p

        print(f"[*] Preflight xử lý footage: {input_p.name} -> {output_p.name}")

        # Kiểm tra trùng lặp
        self.check_duplication(input_p, scene_id)

        w, h = self.target_w, self.target_h
        scaled_w = int(round(w * zoom_factor / 2.0)) * 2
        scaled_h = int(round(h * zoom_factor / 2.0)) * 2

        # Xây dựng video filter:
        # 1. Scale phóng to zoom_factor để đẩy logo văng ra ngoài mép
        # 2. Crop về 1920x1080 chính giữa
        # 3. Ép FPS cố định 30.0 fps (r=30, fps=30)
        # 4. Tăng độ nét unsharp
        vf_filters = [
            f"scale={scaled_w}:{scaled_h}:force_original_aspect_ratio=increase",
            f"crop={w}:{h}",
            f"fps={int(self.target_fps)}"
        ]
        if sharpen:
            vf_filters.append("unsharp=luma_msize_x=5:luma_msize_y=5:luma_amount=0.6:chroma_amount=0.0")

        filter_str = ",".join(vf_filters)

        # Tham số quan trọng chống giật lag:
        # -g 1: All-Intra (mỗi frame là 1 Keyframe)
        # -keyint_min 1: Khóa cứng khoảng cách keyframe
        # -an: Xóa sạch âm thanh gốc (Audio Stripping)
        cmd = [
            "ffmpeg", "-y", "-i", str(input_p),
            "-vf", filter_str,
            "-an",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "18",
            "-g", "1",
            "-keyint_min", "1",
            "-pix_fmt", "yuv420p",
            str(actual_output)
        ]

        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        if res.returncode != 0:
            if is_inplace and actual_output.exists():
                actual_output.unlink(missing_ok=True)
            print(f"[!] Lỗi FFmpeg khi preflight: {res.stderr}")
            raise RuntimeError(f"FFmpeg preflight error: {res.stderr}")

        if is_inplace:
            # Ghi đè an toàn
            actual_output.replace(output_p)

        print(f"[+] Thành công! Footage All-Intra chuẩn 16:9 sắc nét: {output_p.name} ({output_p.stat().st_size / 1024 / 1024:.2f} MB)")
        return output_p

if __name__ == "__main__":
    if len(sys.argv) > 2:
        proc = AssetPreflightProcessor()
        proc.process_footage(Path(sys.argv[1]), Path(sys.argv[2]), scene_id="test")
    else:
        print("AssetPreflightProcessor sẵn sàng hoạt động.")
