# -*- coding: utf-8 -*-
r"""
sfx_timeline_mixer.py - BỘ HÒA ÂM ĐA TẦNG PHÒNG THU & TRÍ TUỆ BIÊN ĐẠO SFX THEO NGỮ NGHĨA KỊCH BẢN (-14.0 LUFS)
(Dành riêng cho Đầu Não Video Ngắn FB: D:\Đầu Não Video Ngắn FB (không xóa))

LUẬT THÉP BẤT DI BẤT DỊCH:
1. MỖI KỊCH BẢN LÀ MỘT BẢN PHỐI MỚI 100% — CẤM LẤY ÂM THANH CŨ:
   - Nhạc nền 5 Nhịp phải được sáng tác/tổng hợp mới theo đúng nội dung kịch bản qua `ACEStepFBRunner`.
   - Điểm rơi SFX phải được tự động biên đạo mới (`auto_choreograph_script_sfx_cues`) dựa trên file `words.json`
     của kịch bản mới — TUYỆT ĐỐI CẤM copy-paste danh sách mốc thời gian SFX của kịch bản cũ sang kịch bản mới!
2. Giọng đọc Hải Đăng luôn ở NGÔI THƯỢNG TẦNG (`voice_volume = 1.28`, tăng độ nét `3.0kHz +2.8dB`, lọc đáy `85Hz`):
   TUYỆT ĐỐI KHÔNG BAO GIỜ BỊ NHẠC NỀN LẤN ÁT DÙ CHỈ 1 dB!
3. Nhạc nền Trailer Điện Ảnh 5 Nhịp (đã chuẩn hóa `-12.0 LUFS, LRA=5`):
   - Áp dụng Cắt rãnh tần số phẫu thuật (`Surgical Spectral Pocket: -3.5dB tại 2.5kHz`) để nhường dải giọng nói cho Hải Đăng
     nhưng bảo toàn 100% lực đập của dàn dây Staccato (`400Hz-1.5kHz`), Sub-Bass/War Drums (`+2.0dB tại 90Hz`) và tiếng tích tắc đồng hồ (`4kHz-10kHz`).
   - Âm lượng nhạc nền cân đối hài hòa (`bgm_base_volume = 0.44`, tức thấp hơn giọng đọc `5.5 - 6.5 dB`): Vừa đủ nghe rõ từng nhịp trống,
     từng tiếng đàn cello kịch tính lôi cuốn như trailer phim mà tuyệt đối không làm át giọng đọc!
   - Vacuum Drop: Ngắt sạch nhạc `0.65s` ngay trước câu chốt kịch tính.
4. Tự động xuất file `_qc_listen_preview.mp3` ngay sau khi mix để Agent bắt buộc mở nghe kiểm chứng bằng `view_file`/`read_file`!
"""

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Tuple

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

FB_BRAIN = Path(r"D:\Đầu Não Video Ngắn FB (không xóa)")
SFX_DIR = FB_BRAIN / "remotion_reels" / "public" / "sfx"

# Từ điển ngữ nghĩa từ khóa -> SFX phòng thu tương ứng để tự động biên đạo cho kịch bản mới
SEMANTIC_SFX_MAP = [
    # 1. Tiền bạc, Tỷ đô, Vốn hóa, Tài chính
    (
        ["tỷ", "triệu", "đô", "usd", "vốn", "ipo", "giá", "tiền", "lãi", "lỗ", "cổ", "thuế", "%"],
        [("coin1.mp3", 0.55), ("bass_hit.mp3", 0.48), ("hit_blow.mp3", 0.60)],
    ),
    # 2. Thời gian, Năm tháng, Lịch sử, Đếm ngược
    (
        ["năm", "tháng", "ngày", "giờ", "phút", "giây", "lịch", "suốt", "19", "20", "tuổi", "thời"],
        [("tick.mp3", 1.50), ("gear_lock.mp3", 0.82), ("tap.mp3", 0.90)],
    ),
    # 3. Điều tra, Pháp lý, Bí mật, Gián điệp, Bất ngờ, Cấm vận
    (
        ["điều", "tra", "luật", "án", "tòa", "điệp", "nghi", "mật", "ngờ", "cấm", "phạt", "bắt", "rối", "ngầm"],
        [("lock.mp3", 0.68), ("glitch.mp3", 0.48), ("cut.mp3", 0.82)],
    ),
    # 4. Đế chế, Quyền lực, Khổng lồ, Ngai vàng, Độc quyền, Chấn động
    (
        ["đế", "chế", "ngai", "vàng", "quyền", "lực", "khổng", "lồ", "vua", "trùm", "thống", "trị", "sụp", "đổ"],
        [("metal_hit.mp3", 0.65), ("zoom_hit.mp3", 0.52), ("hit_blow.mp3", 0.62)],
    ),
]


def auto_choreograph_script_sfx_cues(
    words_json_path: str | Path,
    total_duration_sec: float,
    beat_timestamps: Optional[List[float]] = None,
) -> Tuple[List[Tuple[str, int, float]], List[Tuple[float, float]]]:
    """
    Trí tuệ biên đạo SFX tự động & sáng tạo cho từng kịch bản mới dựa trên `words.json`:
    - Quét từng từ và mốc thời gian mili-giây của giọng đọc Hải Đăng.
    - Đặt hiệu ứng mở cảnh (Whoosh + Pop/Tap) tại đầu mỗi Beat trong 5 Nhịp.
    - Điểm huyệt SFX ngữ nghĩa (Tiền tệ, Thời gian, Điều tra, Quyền lực) khớp chính xác từng chữ khóa.
    - Tự động phát hiện câu hỏi Cliffhanger cuối cùng để đặt khoảng lặng chân không (Vacuum Drop).
    """
    words_path = Path(words_json_path)
    if not words_path.exists():
        raise FileNotFoundError(f"Không tìm thấy words.json để biên đạo SFX: {words_path}")

    raw_data = json.loads(words_path.read_text(encoding="utf-8"))
    words = raw_data.get("words", raw_data) if isinstance(raw_data, dict) else raw_data

    if not beat_timestamps or len(beat_timestamps) < 5:
        step = total_duration_sec / 5.0
        beat_timestamps = [0.0, round(step * 0.85, 2), round(step * 1.75, 2), round(step * 2.80, 2), round(step * 3.82, 2)]

    cues: List[Tuple[str, int, float]] = []
    used_ms: List[int] = []

    def add_cue(sfx_file: str, ms: int, vol: float, min_gap_ms: int = 550) -> bool:
        ms = max(0, min(int(total_duration_sec * 1000) - 250, int(ms)))
        if any(abs(ms - u) < min_gap_ms for u in used_ms):
            return False
        cues.append((sfx_file, ms, round(vol, 2)))
        used_ms.append(ms)
        return True

    # 1. Đặt hiệu ứng Chuyển cảnh + Text Hook Pop tại mở đầu 5 Nhịp (5 Beats)
    whoosh_cycle = [
        ("whoosh_big.mp3", 0.72),
        ("whoosh1.mp3", 0.52),
        ("whoosh2.mp3", 0.72),
        ("whoosh3.mp3", 0.52),
        ("whoosh_big.mp3", 0.65),
    ]
    pop_cycle = [
        ("tick.mp3", 1.50),
        ("pop_dry.mp3", 0.72),
        ("tap.mp3", 0.92),
        ("type_soft.mp3", 0.92),
        ("pop.mp3", 0.65),
    ]
    for idx, bt in enumerate(beat_timestamps[:5]):
        b_ms = int(bt * 1000)
        w_file, w_vol = whoosh_cycle[idx % len(whoosh_cycle)]
        p_file, p_vol = pop_cycle[idx % len(pop_cycle)]
        add_cue(w_file, b_ms, w_vol, min_gap_ms=400)
        add_cue(p_file, b_ms + 280, p_vol, min_gap_ms=220)

    # 2. Quét ngữ nghĩa từng từ trong `words.json` để điểm huyệt SFX thông minh
    cat_counters = [0] * len(SEMANTIC_SFX_MAP)
    for w_obj in words:
        w_text = str(w_obj.get("word", w_obj.get("text", ""))).strip().lower()
        w_clean = re.sub(r"[^\w%]", "", w_text)
        if not w_clean:
            continue
        start_sec = float(w_obj.get("start", w_obj.get("startMs", 0) / 1000.0 if "startMs" in w_obj else 0.0))
        start_ms = int(start_sec * 1000)

        matched = False
        for c_idx, (kw_list, sfx_pool) in enumerate(SEMANTIC_SFX_MAP):
            if any(kw == w_clean or (len(kw) >= 3 and kw in w_clean) for kw in kw_list):
                sfx_file, sfx_vol = sfx_pool[cat_counters[c_idx] % len(sfx_pool)]
                if add_cue(sfx_file, start_ms, sfx_vol, min_gap_ms=750):
                    cat_counters[c_idx] += 1
                    matched = True
                break

        # Nếu là con số thuần túy (ví dụ: 33, 60, 3000, 1993) mà chưa match
        if not matched and any(ch.isdigit() for ch in w_clean):
            num_pool = [("tick.mp3", 1.50), ("coin1.mp3", 0.52), ("tap.mp3", 0.90), ("gear_lock.mp3", 0.82)]
            sfx_file, sfx_vol = num_pool[len(cues) % len(num_pool)]
            add_cue(sfx_file, start_ms, sfx_vol, min_gap_ms=700)

    # 3. Đảm bảo mật độ nhịp điệu đồng đều (nếu khoảng trống > 2.4s thì chèn accent nhẹ hỗ trợ Text Hook)
    cues.sort(key=lambda x: x[1])
    filler_pool = [
        ("pop.mp3", 0.65),
        ("tap.mp3", 0.88),
        ("pop_dry.mp3", 0.70),
        ("zoom_hit.mp3", 0.48),
        ("type_soft.mp3", 0.90),
    ]
    f_idx = 0
    for w_obj in words:
        start_sec = float(w_obj.get("start", w_obj.get("startMs", 0) / 1000.0 if "startMs" in w_obj else 0.0))
        start_ms = int(start_sec * 1000)
        if not any(abs(start_ms - u) < 1600 for u in used_ms):
            sfx_file, sfx_vol = filler_pool[f_idx % len(filler_pool)]
            if add_cue(sfx_file, start_ms, sfx_vol, min_gap_ms=1100):
                f_idx += 1

    # 4. Tìm điểm Vacuum Drop (khoảng ngắt trước câu chốt cuối cùng ở vùng 82% - 94% thời lượng)
    drop_start = round(total_duration_sec * 0.88, 2)
    best_gap = 0.0
    for i in range(len(words) - 1):
        end_cur = float(words[i].get("end", words[i].get("endMs", 0) / 1000.0 if "endMs" in words[i] else 0.0))
        st_nxt = float(words[i + 1].get("start", words[i + 1].get("startMs", 0) / 1000.0 if "startMs" in words[i + 1] else 0.0))
        if total_duration_sec * 0.80 <= end_cur <= total_duration_sec * 0.94:
            gap = st_nxt - end_cur
            if gap >= best_gap:
                best_gap = gap
                drop_start = round(max(0.0, end_cur - 0.15), 2)

    drop_end = round(min(total_duration_sec - 1.0, drop_start + 0.65), 2)
    vacuum_drops = [(drop_start, drop_end)]

    # Đặt cú nổ Bass Hit + Metal Hit ngay sau Vacuum Drop để chốt hạ câu hỏi cuối
    add_cue("bass_hit.mp3", int(drop_end * 1000) + 80, 0.52, min_gap_ms=300)
    add_cue("metal_hit.mp3", int((total_duration_sec - 0.85) * 1000), 0.62, min_gap_ms=300)

    cues.sort(key=lambda x: x[1])
    print(f"[SFX CHOREOGRAPHER OK] Đã tự động thiết kế {len(cues)} điểm rơi SFX mới & Vacuum Drop {vacuum_drops} từ words.json!")
    return cues, vacuum_drops


def validate_fresh_ai_bgm(bgm_path: Path) -> None:
    bgm_str = str(bgm_path.resolve()).lower()
    forbidden_markers = [
        "demo_fb_reels_forensic_bgm",
        "wallstreet_finance_drive_01",
        "dark_investigation_tension_01",
        "cyber_ai_future_02",
        "epic_victory_climax_01",
        r"\assets\music\\",
        r"\public\music\\",
        r"\public\audio\bgm\\",
    ]
    for marker in forbidden_markers:
        if marker in bgm_str:
            raise ValueError(
                f"VI PHẠM LUẬT THÉP: Phát hiện lấy nhạc nền tĩnh cũ trong máy ({bgm_path})! "
                f"Bắt buộc dùng bộ sáng tác nhạc Trailer 5 Nhịp ĐỘC BẢN theo kịch bản!"
            )


def mix_reels_master_audio(
    voice_wav: str | Path,
    output_wav: str | Path,
    sfx_cues: Optional[list[tuple[str, int, float]]] = None,
    total_duration_sec: float = 43.0,
    bgm_path: str | Path | None = None,
    script_topic: str = "",
    script_text: str = "",
    words_json_path: str | Path | None = None,
    beat_timestamps: Optional[List[float]] = None,
    mood: str = "conspiracy_thriller",
    voice_volume: float = 1.28,
    bgm_base_volume: float = 0.44,
    bgm_duck_volume: float = 0.36,
    vacuum_drops: list[tuple[float, float]] | None = None,
) -> Path:
    """
    Hòa âm Trailer Hollywood 5 Nhịp kịch tính & cân đối hài hòa với giọng đọc Hải Đăng (-14.0 LUFS).
    Nếu truyền `words_json_path` mà chưa có `sfx_cues`, hệ thống tự động biên đạo SFX mới 100% theo từng từ khóa!
    """
    voice_wav = Path(voice_wav)
    output_wav = Path(output_wav)
    output_wav.parent.mkdir(parents=True, exist_ok=True)

    if not voice_wav.exists():
        raise FileNotFoundError(f"Không tìm thấy voice_wav: {voice_wav}")

    # Tự động biên đạo SFX mới 100% từ words.json nếu chưa truyền sfx_cues
    if (not sfx_cues or len(sfx_cues) == 0) and words_json_path:
        sfx_cues, auto_drops = auto_choreograph_script_sfx_cues(
            words_json_path=words_json_path,
            total_duration_sec=total_duration_sec,
            beat_timestamps=beat_timestamps,
        )
        if not vacuum_drops:
            vacuum_drops = auto_drops
    elif not sfx_cues:
        raise ValueError("Bắt buộc truyền sfx_cues hoặc words_json_path để biên đạo SFX mới cho kịch bản!")

    if bgm_path is None:
        if not script_topic:
            raise ValueError("Bắt buộc truyền bgm_path hoặc script_topic để biên soạn nhạc trailer 5 nhịp mới!")
        from ace_step_fb_runner import ACEStepFBRunner
        runner = ACEStepFBRunner()
        bgm_path = output_wav.parent / f"bespoke_5beat_trailer_{output_wav.stem}.wav"
        runner.generate_unique_script_bgm(
            script_topic=script_topic,
            output_path=bgm_path,
            duration_sec=total_duration_sec + 0.5,
            mood=mood,
            script_text=script_text,
            beat_timestamps=beat_timestamps,
        )
    else:
        bgm_path = Path(bgm_path)

    if not bgm_path.exists():
        raise FileNotFoundError(f"Không tìm thấy bgm_path: {bgm_path}")

    validate_fresh_ai_bgm(bgm_path)

    cmd = ["ffmpeg", "-y", "-i", str(voice_wav), "-i", str(bgm_path)]
    for fname, _, _ in sfx_cues:
        fpath = SFX_DIR / fname
        if not fpath.exists():
            raise FileNotFoundError(f"SFX không tồn tại trong kho phòng thu: {fpath}")
        cmd.extend(["-i", str(fpath)])

    fade_out_st = max(0.5, round(total_duration_sec - 1.2, 2))

    # 1. Đường tiếng Giọng đọc Hải Đăng: Lọc sạch tạp âm đáy 85Hz, tăng độ rõ chữ 3.0kHz (+2.8dB)
    vo_filter = (
        f"[0:a]highpass=f=85,"
        f"equalizer=f=3000:width_type=o:width=1.3:g=2.8,"
        f"volume={voice_volume}[vo_clean]"
    )

    # 2. Đường tiếng Nhạc nền Trailer 5 Nhịp:
    # - Surgical Spectral Pocket (-3.5dB tại 2.5kHz) nhường dải giọng nói nhưng giữ trọn lực đàn dây & trống trận.
    # - Boost nhẹ sub-bass 90Hz (+2.0dB) tạo độ dày rạp chiếu phim.
    bgm_proc_filter = (
        f"[1:a]atrim=0:{total_duration_sec:.2f},"
        f"equalizer=f=2500:width_type=o:width=1.2:g=-3.5,"
        f"equalizer=f=90:width_type=o:width=1.2:g=2.0,"
        f"volume={bgm_base_volume},"
        f"afade=t=out:st={fade_out_st:.2f}:d=1.2[bgm_eq]"
    )

    if vacuum_drops:
        drop_filters = [f"between(t,{d_st:.2f},{d_end:.2f})" for d_st, d_end in vacuum_drops]
        cond_str = "+".join(drop_filters)
        bgm_final_filter = f"[bgm_eq]volume=enable='{cond_str}':volume=0[bgm_final]"
    else:
        bgm_final_filter = "[bgm_eq]volume=1.0[bgm_final]"

    filter_parts = [vo_filter, bgm_proc_filter, bgm_final_filter]
    mix_inputs = ["[vo_clean]", "[bgm_final]"]

    # 3. Nạp các điểm rơi SFX sắc nét
    for idx, (_, delay_ms, vol) in enumerate(sfx_cues):
        inp_idx = idx + 2
        tag = f"[s{idx}]"
        filter_parts.append(f"[{inp_idx}:a]adelay={int(delay_ms)}|{int(delay_ms)},volume={vol}{tag}")
        mix_inputs.append(tag)

    total_inputs = len(mix_inputs)
    filter_parts.append(
        f"{''.join(mix_inputs)}amix=inputs={total_inputs}:duration=first:dropout_transition=0:normalize=0[pre_norm]"
    )

    tmp_pre_wav = output_wav.with_name(f"._tmp_{output_wav.stem}_pre_norm.wav")
    try:
        cmd.extend([
            "-filter_complex", ";".join(filter_parts),
            "-map", "[pre_norm]",
            "-c:a", "pcm_f32le",
            "-ar", "48000",
            "-ac", "2",
            str(tmp_pre_wav),
        ])

        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode != 0:
            raise RuntimeError(f"Lỗi mix audio FFmpeg Pass 1: {res.stderr[-500:]}")

        measure_cmd = [
            "ffmpeg", "-i", str(tmp_pre_wav),
            "-af", "loudnorm=I=-14.0:TP=-1.0:LRA=7:print_format=json",
            "-f", "null", "-",
        ]
        m_res = subprocess.run(measure_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        json_match = re.search(r"\{[\s\S]*\}", m_res.stderr)
        if not json_match:
            raise RuntimeError(f"Không đo được thông số loudnorm Pass 1: {m_res.stderr[-500:]}")
        stats = json.loads(json_match.group(0))

        norm_filter = (
            f"loudnorm=I=-14.0:TP=-1.0:LRA=7:"
            f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
            f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
            f"offset={stats['target_offset']}:linear=true"
        )
        pass2_cmd = [
            "ffmpeg", "-y", "-i", str(tmp_pre_wav),
            "-af", norm_filter,
            "-c:a", "pcm_s16le",
            "-ar", "48000",
            "-ac", "2",
            str(output_wav),
        ]
        p2_res = subprocess.run(pass2_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if p2_res.returncode != 0:
            raise RuntimeError(f"Lỗi chuẩn hóa loudnorm Pass 2: {p2_res.stderr[-500:]}")
    finally:
        if tmp_pre_wav.exists():
            tmp_pre_wav.unlink()

    # Tự động trích xuất file MP3 để Agent bắt buộc mở nghe kiểm định bằng view_file/read_file
    qc_preview_mp3 = output_wav.parent / "master_audio_qc_preview.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(output_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(qc_preview_mp3)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"[SFX MIXER OK] Master Audio 5-Beat Trailer (-14.0 LUFS, {len(sfx_cues)} SFX Cues): {output_wav}")
    print(f"[MANDATORY EAR QC] Bắt buộc dùng view_file/read_file nghe kiểm định tại: {qc_preview_mp3}")
    return output_wav
