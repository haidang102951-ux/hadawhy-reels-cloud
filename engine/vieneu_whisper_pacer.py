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

_VN_LETTER_PRON = {
    "a": "a", "b": "bê", "c": "xê", "d": "đê", "e": "e", "f": "ép",
    "g": "gờ", "h": "hát", "i": "i", "j": "giây", "k": "ca", "l": "lờ",
    "m": "mờ", "n": "nờ", "o": "o", "p": "pê", "q": "quy", "r": "rờ",
    "s": "ét", "t": "tê", "u": "u", "v": "vê", "w": "đắp liu", "x": "ích",
    "y": "y", "z": "dét",
}
_VN_DIGIT_PRON = {
    "0": "không", "1": "một", "2": "hai", "3": "ba", "4": "bốn",
    "5": "năm", "6": "sáu", "7": "bảy", "8": "tám", "9": "chín",
}


def normalize_vietnamese_tts_codes(text: str) -> str:
    """
    Chuẩn hóa đọc mượt các mã viết tắt chữ+số ngắn (VD: C04 -> 'xê không bốn', A05 -> 'a không năm', PC02 -> 'pê xê không hai')
    tránh TTS ngắt khựng giữa chữ cái và chữ số; giữ nguyên các đơn vị thông dụng (m2, 3D, 4K, G7, H3, F0/F1 nếu cần đọc liền).
    """
    import re

    skip_tokens = {"3D", "2D", "4K", "8K", "5G", "4G", "M2", "S24", "B52"}

    def _repl(match: re.Match) -> str:
        tok = match.group(0)
        if tok.upper() in skip_tokens:
            return tok
        letters = match.group(1)
        digits = match.group(2)
        if digits.startswith("0") or (letters.isupper() and len(digits) in (2, 3)):
            l_spoken = " ".join(_VN_LETTER_PRON.get(ch.lower(), ch) for ch in letters)
            d_spoken = " ".join(_VN_DIGIT_PRON.get(d, d) for d in digits)
            return f"{l_spoken} {d_spoken}"
        return tok

    return re.sub(r"\b([A-Za-z]{1,2})(\d{2,3})\b", _repl, text)


class VieNeuWhisperPacer:
    def __init__(self, output_dir: Optional[Path | str] = None):
        self.base_dir = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
        if output_dir:
            self.voice_output_dir = Path(output_dir)
        else:
            # Mặc định trỏ về thư mục WIP dự án, TUYỆT ĐỐI KHÔNG lưu vào Đầu Não
            self.voice_output_dir = Path(r"D:\DuAn_DangLam\temp")
        self.voice_output_dir.mkdir(parents=True, exist_ok=True)
        self.whisper_model = None

    def _get_whisper(self):
        if self.whisper_model is None:
            from faster_whisper import WhisperModel
            # Sử dụng model base/tiny để nhận diện cực nhanh trên CPU
            self.whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
        return self.whisper_model

    def _assert_local_hai_dang_voice(self, voice_name: str):
        """Khóa cứng giọng nội bộ 'Hải Đăng', cấm fallback sang bất kỳ giọng/TTS nào khác."""
        required_voice = "Hải Đăng"
        if (voice_name or "").strip() != required_voice:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Chỉ cho phép giọng local '{required_voice}', "
                f"từ chối giọng '{voice_name}'."
            )

        vieneu_root = Path(r"D:\VieNeu-TTS")
        old_voice_py = Path(r"D:\Đầu Não (không xóa)\engine\vieneu_voice_engine.py")
        if not vieneu_root.exists() or not old_voice_py.exists():
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Thiếu VieNeu-TTS local ({vieneu_root}) "
                f"hoặc voice engine ({old_voice_py})."
            )

        if str(vieneu_root) not in sys.path:
            sys.path.insert(0, str(vieneu_root))

        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("old_voice", str(old_voice_py))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            client = mod.get_vieneu_client()
            if hasattr(client, "list_preset_voices"):
                presets = client.list_preset_voices()
                names = [
                    (p[0] if isinstance(p, (tuple, list)) else str(p))
                    for p in (presets or [])
                ]
                if not any(required_voice.lower() in n.lower() for n in names):
                    raise RuntimeError(
                        f"MISSING_LOCAL_VOICE_HAI_DANG: Không tìm thấy giọng '{required_voice}' "
                        f"trong danh sách local VieNeu-TTS: {names}"
                    )
            return mod
        except RuntimeError:
            raise
        except Exception as exc:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Không thể nạp giọng local '{required_voice}': {exc}"
            ) from exc

    def generate_voiceover(
        self,
        script_text: str,
        voice_name: str = "Hải Đăng",
        output_wav: Optional[Path] = None
    ) -> Path:
        """
        Sinh file WAV giọng đọc local 'Hải Đăng' từ VieNeu TTS (CẤM fallback giọng khác).
        """
        if output_wav is None:
            output_wav = self.voice_output_dir / "voiceover.wav"
        output_wav = Path(output_wav)
        output_wav.parent.mkdir(parents=True, exist_ok=True)

        mod = self._assert_local_hai_dang_voice(voice_name)
        try:
            mod.generate_voice(text=script_text, voice="Hải Đăng", output_path=str(output_wav))
        except Exception as exc:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: Lỗi khi sinh giọng local 'Hải Đăng': {exc}"
            ) from exc

        if not output_wav.exists() or output_wav.stat().st_size < 1024:
            raise RuntimeError(
                f"MISSING_LOCAL_VOICE_HAI_DANG: File WAV sinh ra không hợp lệ ({output_wav})."
            )
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

    def process_script(
        self,
        script_text: str,
        out_prefix: str = "voiceover",
        output_dir: Optional[Path | str] = None,
        voice_name: str = "Hải Đăng",
    ) -> Dict:
        """
        Quy trình trọn gói: Sinh giọng Hải Đăng -> Whisper Word-Timestamps.
        Luôn xuất đúng chuẩn: voiceover.wav & words.json khi dùng mặc định.
        """
        target_dir = Path(output_dir) if output_dir else self.voice_output_dir
        target_dir.mkdir(parents=True, exist_ok=True)
        wav_path = target_dir / ("voiceover.wav" if out_prefix == "voiceover" else f"{out_prefix}.wav")
        json_path = target_dir / ("words.json" if out_prefix == "voiceover" else f"{out_prefix}_words.json")

        # 1. Tiền xử lý mã chữ+số ngắn (C04 -> xê không bốn) rồi sinh voiceover
        tts_ready_text = normalize_vietnamese_tts_codes(script_text)
        self.generate_voiceover(tts_ready_text, voice_name=voice_name, output_wav=wav_path)

        # 2. Bóc tách timestamps
        words = self.extract_word_timestamps(wav_path)

        # 3. Lưu JSON kèm metadata khóa giọng local Hải Đăng
        meta_payload = {
            "voice_name": "Hải Đăng",
            "voice_source": "local",
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump({
                "script": script_text,
                "voice": "Hải Đăng",
                **meta_payload,
                "duration": words[-1]["end"] if words else 0.0,
                "word_count": len(words),
                "words": words
            }, f, ensure_ascii=False, indent=2)

        voice_meta_path = target_dir / "voice_meta.json"
        with open(voice_meta_path, "w", encoding="utf-8") as mf:
            json.dump({
                **meta_payload,
                "wav_path": str(wav_path),
                "words_path": str(json_path),
                "duration": words[-1]["end"] if words else 0.0,
            }, mf, ensure_ascii=False, indent=2)

        return {
            "wav_path": str(wav_path),
            "json_path": str(json_path),
            "duration": words[-1]["end"] if words else 0.0,
            "word_count": len(words),
            "words": words
        }


def _extract_script_text(script_path: Path) -> str:
    """Đọc nội dung lời thoại từ file .txt hoặc .json (tự nối toàn bộ nhịp theo thứ tự)."""
    raw = script_path.read_text(encoding="utf-8").strip()
    if script_path.suffix.lower() != ".json":
        return raw

    data = json.loads(raw)
    if isinstance(data, str):
        return data.strip()
    if isinstance(data, dict):
        for key in ("full_script", "full_voiceover", "script_text"):
            if isinstance(data.get(key), str) and data[key].strip():
                return data[key].strip()
        parts: List[str] = []
        beats = data.get("beats") or data.get("scenes") or data.get("segments") or []
        if isinstance(beats, list):
            for b in beats:
                if isinstance(b, str):
                    if b.strip():
                        parts.append(b.strip())
                elif isinstance(b, dict):
                    txt = (
                        b.get("voiceover")
                        or b.get("narration")
                        or b.get("voice_text")
                        or b.get("spoken_text")
                        or b.get("text")
                        or b.get("script")
                    )
                    if isinstance(txt, str) and txt.strip():
                        parts.append(txt.strip())
                    elif isinstance(b.get("lines"), list):
                        for ln in b["lines"]:
                            if isinstance(ln, str) and ln.strip():
                                parts.append(ln.strip())
                            elif isinstance(ln, dict):
                                lt = ln.get("text") or ln.get("voiceover") or ln.get("narration")
                                if isinstance(lt, str) and lt.strip():
                                    parts.append(lt.strip())
        if parts:
            return " ".join(parts)
        if isinstance(data.get("script"), str) and data["script"].strip():
            return data["script"].strip()
    elif isinstance(data, list):
        parts = []
        for item in data:
            if isinstance(item, str) and item.strip():
                parts.append(item.strip())
            elif isinstance(item, dict):
                txt = item.get("voiceover") or item.get("narration") or item.get("text") or item.get("script")
                if isinstance(txt, str) and txt.strip():
                    parts.append(txt.strip())
        if parts:
            return " ".join(parts)

    raise ValueError(f"Không trích xuất được lời thoại từ file JSON: {script_path}")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="Sinh giọng đọc VieNeu TTS (Hải Đăng) & bóc tách word timestamps (temp/voiceover.wav + temp/words.json)."
    )
    ap.add_argument("--script", help="Đường dẫn tới script_5beat.json hoặc file .txt lời thoại")
    ap.add_argument("--project", help="Thư mục dự án WIP (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--voice", default="Hải Đăng", help="Tên giọng đọc VieNeu TTS (khóa cứng mặc định: Hải Đăng)")
    ap.add_argument("--check-voice", action="store_true", help="Kiểm tra nhanh giọng local 'Hải Đăng' trên máy")
    args = ap.parse_args()

    if args.check_voice:
        pacer = VieNeuWhisperPacer()
        pacer._assert_local_hai_dang_voice(args.voice)
        print(f"[OK] Verified local voice: {args.voice} (source=local)")
        return 0

    if not args.script or not args.project:
        ap.error("Cần truyền --script và --project (hoặc --check-voice).")

    script_path = Path(args.script)
    if not script_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file kịch bản: {script_path}")

    script_text = _extract_script_text(script_path)
    out_dir = Path(args.project) / "temp"
    pacer = VieNeuWhisperPacer(output_dir=out_dir)
    res = pacer.process_script(
        script_text=script_text,
        out_prefix="voiceover",
        output_dir=out_dir,
        voice_name=args.voice,
    )
    print(f"[OK] WAV: {res['wav_path']}")
    print(f"[OK] WORDS: {res['json_path']}")
    print(f"[OK] Processed {res['word_count']} words | Duration: {res['duration']}s | Voice: {args.voice}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
