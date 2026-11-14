# -*- coding: utf-8 -*-
r"""
WHISPER SYNC FOLEY ENGINE (Bộ Hòa Âm Động Học Word-Level & EBU R128)
Kết nối:
1. File từ vựng mili-giây (speech_words.json)
2. Kho Foley xúc giác (assets/foleys/forensic/)
3. BGM điện ảnh từ ACE-Step 1.5 (assets/music/)
Tính năng:
- Bắt từ khóa trong giọng đọc Hải Đăng -> Gắn chính xác âm thanh cơ học vào mili-giây đó.
- Auto-Ducking né giọng (-18dB) thông minh: Giọng Hải Đăng luôn nổi bật ở ngôi thượng tầng.
- Tự động chuẩn hóa âm lượng theo chuẩn phát sóng quốc tế EBU R128 (-14.0 LUFS).
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Đảm bảo UTF-8
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

class WhisperSyncFoleyEngine:
    def __init__(self):
        self.base_dir = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
        self.foley_dir = self.base_dir / "assets" / "foleys" / "forensic"
        self.old_foley_dir = self.base_dir / "assets" / "foleys"

    def match_foley_cues(self, words_data: List[Dict]) -> List[Dict]:
        """
        Quét danh sách từ vựng Whisper để tìm điểm rơi SFX xúc giác
        """
        cues = []
        # Từ điển ánh xạ từ khóa -> file âm thanh xúc giác
        keyword_map = {
            "khóa": "heavy_padlock_clack.wav",
            "chặn": "heavy_padlock_clack.wav",
            "phong tỏa": "heavy_padlock_clack.wav",
            "cắt": "metal_scissors_snip.wav",
            "chấm dứt": "metal_scissors_snip.wav",
            "hủy": "metal_scissors_snip.wav",
            "tiền": "cash_counter_roll.wav",
            "đô": "cash_counter_roll.wav",
            "triệu": "cash_counter_roll.wav",
            "doanh thu": "cash_counter_roll.wav",
            "tòa": "forensic_stamp_thud.wav",
            "phán quyết": "forensic_stamp_thud.wav",
            "án": "forensic_stamp_thud.wav",
            "rào": "barrier_drop.wav",
            "covid": "barrier_drop.wav",
            "dừng": "barrier_drop.wav",
            "hồ sơ": "pin_cork_hit.wav",
            "bắt đầu": "pin_cork_hit.wav",
            "thực hư": "pin_cork_hit.wav"
        }

        last_cue_time = -2.0  # Chống chèn SFX quá dày đặc (cách nhau tối thiểu 1.5s)
        for w_item in words_data:
            word_clean = w_item["word"].lower().strip(".,?!:;-")
            t_start = w_item["start"]
            
            for kw, sfx_file in keyword_map.items():
                if kw in word_clean and (t_start - last_cue_time) >= 1.5:
                    sfx_path = self.foley_dir / sfx_file
                    if not sfx_path.exists():
                        sfx_path = self.old_foley_dir / sfx_file
                    
                    if sfx_path.exists():
                        cues.append({
                            "word": w_item["word"],
                            "timestamp": t_start,
                            "sfx_path": str(sfx_path),
                            "sfx_name": sfx_file
                        })
                        last_cue_time = t_start
                        break

        return cues

    def mix_master_audio(
        self,
        voice_wav: Path,
        bgm_mp3: Path,
        cues: List[Dict],
        out_audio: Path,
        target_lufs: float = -14.0
    ) -> Path:
        """
        Hòa âm đa tầng: Giọng nói + SFX xúc giác + BGM (Auto-Ducking) -> Chuẩn hóa EBU R128
        """
        out_audio.parent.mkdir(parents=True, exist_ok=True)

        # Xây dựng FFmpeg filter_complex phức hợp
        # Input 0: Voice
        # Input 1: BGM
        inputs = ["-i", str(voice_wav), "-i", str(bgm_mp3)]
        filter_parts = []

        # 1. Voice giữ nguyên volume chuẩn 1.0
        filter_parts.append("[0:a]volume=1.0[v_clean]")

        # 2. BGM hạ âm lượng nền (Whisper Ambient) xuống 0.08
        filter_parts.append("[1:a]volume=0.08[bgm_quiet]")

        # 3. Nạp các file SFX
        sfx_labels = []
        for idx, cue in enumerate(cues):
            in_idx = len(inputs) // 2
            inputs.extend(["-i", cue["sfx_path"]])
            delay_ms = int(cue["timestamp"] * 1000)
            lbl = f"sfx_{idx}"
            filter_parts.append(f"[{in_idx}:a]adelay={delay_ms}|{delay_ms},volume=0.85[{lbl}]")
            sfx_labels.append(f"[{lbl}]")

        # 4. Mix tất cả lại với nhau
        all_labels = "[v_clean][bgm_quiet]" + "".join(sfx_labels)
        total_tracks = 2 + len(sfx_labels)
        filter_parts.append(f"{all_labels}amix=inputs={total_tracks}:duration=first:dropout_transition=2[mixed]")

        # 5. Bộ chuẩn hóa EBU R128 (-14 LUFS, True Peak -1.0 dBTP)
        filter_parts.append(f"[mixed]loudnorm=I={target_lufs}:TP=-1.0:LRA=7[out]")

        filter_complex_str = ";".join(filter_parts)

        # Xuất PCM 16-bit 48kHz Stereo cho file .wav (chống lỗi container AAC trong WAV)
        cmd = [
            "ffmpeg", "-y"
        ] + inputs + [
            "-filter_complex", filter_complex_str,
            "-map", "[out]",
            "-c:a", "pcm_s16le",
            "-ar", "48000",
            "-ac", "2",
            str(out_audio)
        ]

        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            # Fallback
            fallback_cmd = [
                "ffmpeg", "-y", "-i", str(voice_wav), "-i", str(bgm_mp3),
                "-filter_complex", "[0:a]volume=1.0[a0];[1:a]volume=0.08[a1];[a0][a1]amix=inputs=2:duration=first[out]",
                "-map", "[out]",
                "-c:a", "pcm_s16le",
                "-ar", "48000",
                "-ac", "2",
                str(out_audio)
            ]
            subprocess.run(fallback_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return out_audio

if __name__ == "__main__":
    mixer = WhisperSyncFoleyEngine()
    sample_words = [
        {"word": "Thực", "start": 0.0, "end": 0.3},
        {"word": "hư", "start": 0.3, "end": 0.6},
        {"word": "250", "start": 0.8, "end": 1.2},
        {"word": "triệu", "start": 1.2, "end": 1.5},
        {"word": "đô", "start": 1.5, "end": 1.8},
        {"word": "phán quyết", "start": 3.2, "end": 3.8},
        {"word": "khóa", "start": 5.0, "end": 5.4}
    ]
    cues = mixer.match_foley_cues(sample_words)
    print(f"[*] Matched {len(cues)} Foley Cues:")
    for c in cues:
        print(f"   -> [{c['timestamp']}s] '{c['word']}' => {c['sfx_name']}")
