# -*- coding: utf-8 -*-
r"""
VIENEU WHISPER PACER (Bộ Điều Phối Giọng Hải Đăng & Bóc Tách Word-Level Timestamps)
Tích hợp:
1. VieNeu TTS (Giọng Hải Đăng - Nam Bắc Tự Nhiên & Uy Lực)
2. faster-whisper (Bóc tách toạ độ mili-giây từng từ vựng)
Đầu ra:
- voice.wav (Âm thanh giọng đọc sạch sẽ)
- speech_words.json (Danh sách từ + start_ms + end_ms phục vụ đồng bộ động hình & Foley)
"""
import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Đảm bảo UTF-8 cho Windows console
if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

class VieNeuWhisperPacer:
    def __init__(self):
        self.base_dir = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
        self.voice_output_dir = self.base_dir / "assets" / "voice_temp"
        self.voice_output_dir.mkdir(parents=True, exist_ok=True)
        self.whisper_model = None

    def _get_whisper(self):
        if self.whisper_model is None:
            from faster_whisper import WhisperModel
            # Sử dụng model base/tiny để nhận diện cực nhanh trên CPU
            self.whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        return self.whisper_model

    def generate_voiceover(
        self,
        script_text: str,
        voice_name: str = "Hải Đăng",
        output_wav: Optional[Path] = None
    ) -> Path:
        """
        Sinh file WAV giọng đọc từ VieNeu TTS (ưu tiên giọng Hải Đăng)
        """
        if output_wav is None:
            output_wav = self.voice_output_dir / "voiceover.wav"

        vieneu_root = Path(r"D:\VieNeu-TTS")
        if str(vieneu_root) not in sys.path:
            sys.path.insert(0, str(vieneu_root))

        old_voice_py = Path(r"D:\Đầu Não (không xóa)\engine\vieneu_voice_engine.py")
        if old_voice_py.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location("old_voice", str(old_voice_py))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.generate_voice(text=script_text, voice=voice_name, output_path=str(output_wav))
        else:
            raise RuntimeError(f"Cannot initialize VieNeu TTS: {e}")

        return output_wav

    def extract_word_timestamps(self, audio_wav: Path) -> List[Dict]:
        """
        Dùng faster-whisper trích xuất toạ độ từng từ (start, end tính theo giây)
        """
        model = self._get_whisper()
        segments, info = model.transcribe(
            str(audio_wav),
            word_timestamps=True,
            language="vi"
        )

        words_data = []
        for segment in segments:
            for w in segment.words:
                words_data.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 3),
                    "end": round(w.end, 3),
                    "probability": round(w.probability, 3)
                })

        return words_data

    def process_script(self, script_text: str, out_prefix: str = "reels_voice") -> Dict:
        """
        Quy trình trọn gói: Sinh giọng Hải Đăng -> Whisper Word-Timestamps
        """
        wav_path = self.voice_output_dir / f"{out_prefix}.wav"
        json_path = self.voice_output_dir / f"{out_prefix}_words.json"

        # 1. Sinh voiceover
        self.generate_voiceover(script_text, voice_name="Hải Đăng", output_wav=wav_path)

        # 2. Bóc tách timestamps
        words = self.extract_word_timestamps(wav_path)

        # 3. Lưu JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "script": script_text,
                "voice": "Hải Đăng",
                "duration": words[-1]["end"] if words else 0.0,
                "word_count": len(words),
                "words": words
            }, f, ensure_ascii=False, indent=2)

        return {
            "wav_path": str(wav_path),
            "json_path": str(json_path),
            "duration": words[-1]["end"] if words else 0.0,
            "word_count": len(words),
            "words": words
        }

if __name__ == "__main__":
    pacer = VieNeuWhisperPacer()
    test_text = "Thực hư vụ đòi 250 triệu đô từ Vietjet bắt đầu từ phán quyết của tòa án London."
    res = pacer.process_script(test_text, out_prefix="test_pacer")
    print(f"[*] Processed {res['word_count']} words. Duration: {res['duration']}s")
