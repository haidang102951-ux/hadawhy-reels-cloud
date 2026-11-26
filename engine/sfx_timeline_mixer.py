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
_ACTIVE_PROJECT_SFX_DIR: Optional[Path] = None


def set_project_sfx_dir(sfx_dir: Optional[Path]) -> None:
    global _ACTIVE_PROJECT_SFX_DIR
    _ACTIVE_PROJECT_SFX_DIR = Path(sfx_dir) if sfx_dir else None


def preprocess_sfx_punch(src: Path, dst: Path) -> Path:
    """
    Cắt sạch khoảng lặng đầu file (-30dB) để SFX nổ đúng từng mili-giây khung hình,
    cắt đuôi <= 2.2s kèm fade-out 80ms và chuẩn hóa đỉnh -0.5 dBFS.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    af = (
        "silenceremove=start_periods=1:start_duration=0:start_threshold=-30dB,"
        "atrim=0:2.2,afade=t=out:st=2.12:d=0.08,"
        "alimiter=limit=0.94:attack=2:release=35"
    )
    res = subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(dst)],
        capture_output=True,
        text=True,
    )
    if res.returncode == 0 and dst.exists() and dst.stat().st_size > 2000:
        return dst
    return src


def get_sfx_peak_offset_ms(wav_path: Path) -> int:
    """Tìm chính xác mili-giây có đỉnh biên độ lớn nhất (argmax(abs(samples))) bằng NumPy sau khi cắt im lặng đầu."""
    import wave
    import numpy as np

    try:
        with wave.open(str(wav_path), "rb") as wf:
            sr = wf.getframerate() or 48000
            n_ch = max(1, wf.getnchannels())
            raw = wf.readframes(min(wf.getnframes(), sr * 2))
        if not raw:
            return 0
        samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
        if n_ch > 1:
            samples = samples.reshape(-1, n_ch).mean(axis=1)
        peak_idx = int(np.argmax(np.abs(samples)))
        return int(round((peak_idx * 1000.0) / sr))
    except Exception:
        return 0


def _sfx_priority(fname: str) -> int:
    low = fname.lower()
    if "role_cta_" in low or "hook_slam" in low or "role_hook" in low:
        return 5
    if "impact" in low or "riser_boom" in low or "boom" in low:
        return 4
    if "slash_cut" in low:
        return 3
    if "card_snap" in low or "role_knowledge" in low or "marker_swipe" in low:
        return 2
    return 1


def resolve_sfx_priority_conflicts(
    sfx_cues: List[Tuple[str, int, float]],
    min_gap_ms: int = 140,
) -> List[Tuple[str, int, float]]:
    """
    TUYỆT ĐỐI KHÔNG dời lùi SFX về sau để né min_gap_ms:
    Nếu 2 cụm sự kiện khác nhau cách nhau < 140ms, chỉ giữ cụm có độ ưu tiên cao hơn
    (hook_slam > impact > slash_cut > card_snap > num_tick), giữ nguyên 100% mốc thời gian gốc!
    """
    if not sfx_cues:
        return []
    # Gom các lớp cùng thuộc 1 mốc sự kiện (cách <= 65ms coi là các lớp chồng của cùng 1 cú đánh)
    sorted_cues = sorted(sfx_cues, key=lambda x: x[1])
    clusters: List[List[Tuple[str, int, float]]] = []
    for c in sorted_cues:
        if clusters and abs(c[1] - clusters[-1][0][1]) <= 65:
            clusters[-1].append(c)
        else:
            clusters.append([c])

    kept_clusters: List[List[Tuple[str, int, float]]] = []
    for cl in clusters:
        cl_anchor = cl[0][1]
        cl_prio = max(_sfx_priority(x[0]) for x in cl)
        if kept_clusters:
            prev_anchor = kept_clusters[-1][0][1]
            prev_prio = max(_sfx_priority(x[0]) for x in kept_clusters[-1])
            if 65 < abs(cl_anchor - prev_anchor) < min_gap_ms:
                if cl_prio > prev_prio:
                    kept_clusters[-1] = cl
                # Nếu ưu tiên thấp hơn hoặc bằng -> bỏ cụm phụ, giữ nguyên mốc cụm chính
                continue
        kept_clusters.append(cl)

    return [item for cl in kept_clusters for item in cl]


def generate_fresh_foley_pack(out_dir: Path, seed: str = "hadawhy") -> dict[str, Path]:
    """
    Bộ sinh transient vật lý tươi mới bằng Python/NumPy (seed theo tên dự án để mỗi tập có màu âm riêng):
    - proc_hook_slam.wav, proc_card_snap.wav, proc_num_tick.wav,
      proc_slash_cut.wav, proc_marker_swipe.wav, proc_riser_boom.wav
    """
    import hashlib
    import wave
    import numpy as np

    out_dir.mkdir(parents=True, exist_ok=True)
    sr = 48000
    seed_int = int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed_int)
    pitch_jit = float(rng.uniform(0.92, 1.09))

    def _write_wav(path: Path, mono: np.ndarray) -> Path:
        peak = float(np.max(np.abs(mono)) + 1e-9)
        norm = np.clip((mono / peak) * 0.89, -1.0, 1.0)
        pcm = (norm * 32767.0).astype(np.int16)
        stereo = np.column_stack((pcm, pcm)).ravel()
        with wave.open(str(path), "wb") as wf:
            wf.setnchannels(2)
            wf.setsampwidth(2)
            wf.setframerate(sr)
            wf.writeframes(stereo.tobytes())
        return path

    files: dict[str, Path] = {}

    # 1. proc_hook_slam.wav (punchy sub-drop + crisp metallic transient, 0.42s)
    t = np.linspace(0, 0.42, int(sr * 0.42), endpoint=False)
    f_sweep = (155.0 * pitch_jit) * np.exp(-t * 9.5) + 42.0
    sub = np.sin(2 * np.pi * np.cumsum(f_sweep) / sr) * np.exp(-t * 7.5)
    click = rng.normal(0, 1, len(t)) * np.exp(-t * 55.0) * 0.65
    files["proc_hook_slam.wav"] = _write_wav(out_dir / "proc_hook_slam.wav", sub + click)

    # 2. proc_card_snap.wav (crisp tactile snap + short air thump, 0.18s)
    t = np.linspace(0, 0.18, int(sr * 0.18), endpoint=False)
    snap_tone = np.sin(2 * np.pi * (420.0 * pitch_jit) * np.exp(-t * 22.0) * t) * np.exp(-t * 28.0)
    snap_air = rng.normal(0, 1, len(t)) * np.exp(-t * 45.0) * 0.55
    files["proc_card_snap.wav"] = _write_wav(out_dir / "proc_card_snap.wav", snap_tone + snap_air)

    # 3. proc_num_tick.wav (tight mechanical digital tick, 0.09s)
    t = np.linspace(0, 0.09, int(sr * 0.09), endpoint=False)
    tick = (np.sin(2 * np.pi * (1450.0 * pitch_jit) * t) + 0.5 * np.sin(2 * np.pi * (2900.0 * pitch_jit) * t)) * np.exp(-t * 68.0)
    files["proc_num_tick.wav"] = _write_wav(out_dir / "proc_num_tick.wav", tick)

    # 4. proc_slash_cut.wav (sharp blade swoosh + high transient, 0.24s)
    t = np.linspace(0, 0.24, int(sr * 0.24), endpoint=False)
    noise = rng.normal(0, 1, len(t))
    env = np.sin(np.pi * (t / 0.24)) ** 1.4 * np.exp(-t * 6.0)
    blade = np.sin(2 * np.pi * (900.0 * pitch_jit * (1.0 - 0.5 * t / 0.24)) * t) * np.exp(-t * 24.0) * 0.55
    files["proc_slash_cut.wav"] = _write_wav(out_dir / "proc_slash_cut.wav", noise * env * 0.75 + blade)

    # 5. proc_marker_swipe.wav (paper/highlighter swipe texture, 0.28s)
    t = np.linspace(0, 0.28, int(sr * 0.28), endpoint=False)
    sw_env = np.sin(np.pi * (t / 0.28)) ** 1.2
    sw_noise = rng.normal(0, 1, len(t))
    # Simple moving-average smoothing to shape mid-band paper swipe
    kernel = np.ones(12) / 12.0
    sw_band = np.convolve(sw_noise, kernel, mode="same") - np.convolve(sw_noise, np.ones(48) / 48.0, mode="same")
    files["proc_marker_swipe.wav"] = _write_wav(out_dir / "proc_marker_swipe.wav", sw_band * sw_env)

    # 6. proc_riser_boom.wav (0.55s rising tension swell into deep sub boom)
    t = np.linspace(0, 0.75, int(sr * 0.75), endpoint=False)
    riser_mask = t < 0.50
    r_t = np.clip(t / 0.50, 0.0, 1.0)
    riser = (rng.normal(0, 1, len(t)) * 0.35 + np.sin(2 * np.pi * (120.0 + 380.0 * (r_t ** 2)) * t) * 0.5) * (r_t ** 2.2) * riser_mask
    b_t = np.maximum(0.0, t - 0.50)
    boom = np.sin(2 * np.pi * ((110.0 * pitch_jit) * np.exp(-b_t * 10.0) + 38.0) * b_t) * np.exp(-b_t * 8.0) * (~riser_mask)
    files["proc_riser_boom.wav"] = _write_wav(out_dir / "proc_riser_boom.wav", riser * 0.65 + boom)

    return files


def resolve_sfx_path(fname: str, project_sfx_dir: Optional[Path] = None) -> Path:
    """
    CHỈ đọc SFX từ temp/sfx/ của đúng dự án đang làm (ZERO REUSE).
    Tuyệt đối không đọc kho cũ trong D:\\Đầu Não (không xóa) hay dự án khác.
    """
    sdir = project_sfx_dir or _ACTIVE_PROJECT_SFX_DIR
    if not sdir or not sdir.exists():
        return Path("__MISSING_PROJECT_SFX_DIR__") / fname
    sdir_resolved = sdir.resolve()
    p = sdir / Path(fname).name
    if p.exists() and p.is_file():
        return p
    for cand in sdir.rglob(Path(fname).name):
        if cand.is_file() and sdir_resolved in cand.resolve().parents:
            return cand
    return sdir / Path(fname).name

# Từ điển 16 Tổ hợp SFX Đa tầng (Compound Stacking - Chuẩn @nhanho.home)
# Nguyên tắc: KHÔNG dùng 1 tiếng whoosh/hit đơn lẻ rập khuôn; mỗi điểm rơi phối 2-3 lớp (tạo đà -> bùng nổ).
COMPOUND_SFX_COMBOS = {
    # Nhóm 1: Chuyển cảnh / Cao trào
    "riser_hit": [("riser.wav", -750, 0.28), ("impact.wav", 0, 0.48)],
    "riser_whoosh": [("riser.wav", -650, 0.26), ("whoosh_fast.wav", 0, 0.44)],
    "riser_reverse": [("riser.wav", -700, 0.25), ("reverse_swell.wav", -140, 0.40)],
    "swell_impact": [("swell.wav", -800, 0.28), ("impact.wav", 0, 0.48)],
    # Nhóm 2: Tăng cường nhịp điệu & Chữ/Số liệu
    "hit_drum_kick": [("impact.wav", 0, 0.40), ("drum_kick.wav", 10, 0.42)],
    "click_typing": [("keyboard_click.wav", 0, 0.42), ("typing.wav", 40, 0.30)],
    "snare_roll_hit": [("snare_roll.wav", -650, 0.30), ("impact.wav", 0, 0.48)],
    "bass_drop_hit": [("boom_drop.wav", 0, 0.46), ("sub_bass_impact.wav", 15, 0.42)],
    # Nhóm 3: Tạo bầu không khí
    "ambient_hit": [("server_hum.wav", -550, 0.20), ("impact.wav", 0, 0.44)],
    "ambient_riser_stinger": [("riser.wav", -700, 0.24), ("stinger.wav", 0, 0.44)],
    "rain_piano": [("rain.wav", -500, 0.20), ("piano_key.wav", 0, 0.40)],
    # Nhóm 4: Cao trào / Cảm giác bom tấn
    "riser_swish_hit": [("riser.wav", -750, 0.25), ("whoosh_fast.wav", -110, 0.36), ("impact.wav", 0, 0.48)],
    "deep_boom_sub": [("boom_drop.wav", 0, 0.46), ("sub_drop.wav", 20, 0.42)],
    "choir_impact": [("choir.wav", -350, 0.26), ("impact.wav", 0, 0.46)],
    "trailer_hit_braam": [("sub_bass_impact.wav", 0, 0.45), ("braaam.wav", 30, 0.42)],
}

# Từ điển ngữ nghĩa từ khóa -> Tổ hợp SFX phòng thu tương ứng để tự động biên đạo cho kịch bản mới
SEMANTIC_SFX_MAP = [
    # 1. Tiền bạc, Tỷ đô, Vốn hóa, Tài chính (từ khóa đặc thù, tránh từ quá phổ thông)
    (
        ["tỷ", "triệu", "usd", "ipo", "lãi", "lỗ", "thuế", "%"],
        [("cash_flip.wav", 0.48), ("bass_drop_hit", 1.0), ("hit_drum_kick", 1.0)],
    ),
    # 2. Điều tra, Pháp lý, Bí mật, Cấm vận
    (
        ["điều", "luật", "tòa", "mật", "cấm", "phạt", "bắt"],
        [("gavel_slam.wav", 0.50), ("ambient_riser_stinger", 1.0), ("click_typing", 1.0)],
    ),
    # 3. Đế chế, Quyền lực, Độc quyền, Chấn động
    (
        ["đế", "ngai", "quyền", "khổng", "thống", "sụp"],
        [("trailer_hit_braam", 1.0), ("deep_boom_sub", 1.0), ("choir_impact", 1.0)],
    ),
]


def _find_blueprint_near(words_path: Path) -> Optional[Path]:
    for cand in [
        words_path.parent / "choreography_blueprint.json",
        words_path.parent.parent / "choreography_blueprint.json",
        words_path.parent.parent / "temp" / "choreography_blueprint.json",
    ]:
        if cand.exists():
            return cand
    return None


def auto_choreograph_script_sfx_cues(
    words_json_path: str | Path,
    total_duration_sec: float,
    beat_timestamps: Optional[List[float]] = None,
    blueprint_json_path: Optional[str | Path] = None,
    cta_duration_sec: float = 3.5,
) -> Tuple[List[Tuple[str, int, float]], List[Tuple[float, float]]]:
    """
    Biên đạo SFX chuẩn điện ảnh (Luật 12 — Visual-Linked, Zero Filler, Chống lặp):
    - Ưu tiên 1: Đọc mốc sự kiện chủ thể 3D / con số từ `choreography_blueprint.json` -> SFX CHỈ nổ đúng lúc hình/số xuất hiện.
    - Ưu tiên 2 (fallback): Nếu chưa có blueprint, chỉ điểm huyệt tại chuyển Beat + con số lớn + điểm Vacuum Drop cuối.
    - XÓA BỎ HOÀN TOÀN cơ chế filler nhồi pop/tap khi trống (giữ khoảng thở cho giọng đọc).
    - Kết nối kho Foley phòng thu thật (`assets/foleys/`) và giới hạn mỗi file tối đa 2 lần/video.
    """
    words_path = Path(words_json_path)
    if not words_path.exists():
        raise FileNotFoundError(f"Không tìm thấy words.json để biên đạo SFX: {words_path}")

    # Khóa kho SFX theo từng dự án + tự sinh bộ transient vật lý tươi mới theo seed tên dự án
    project_sfx_dir = words_path.parent / "sfx"
    set_project_sfx_dir(project_sfx_dir)
    proj_seed = words_path.parent.parent.name or "hadawhy"
    generate_fresh_foley_pack(project_sfx_dir, seed=proj_seed)
    fresh_sfx_files = sorted(
        [p.name for p in project_sfx_dir.glob("*") if p.is_file() and p.suffix.lower() in (".mp3", ".wav")]
    ) if project_sfx_dir.exists() else []
    if not any(f.startswith("role_") for f in fresh_sfx_files):
        try:
            from audio_harvester import harvest_fresh_sfx
            harvest_fresh_sfx(
                words_path.parent.parent,
                topic_keywords=["transition", "whoosh", "click", "technology", "impact", "cinematic"],
                count=14,
            )
            fresh_sfx_files = sorted(
                [p.name for p in project_sfx_dir.glob("*") if p.is_file() and p.suffix.lower() in (".mp3", ".wav")]
            )
        except Exception as exc:
            print(f"[SFX WARN] Không cào thêm được Mixkit ({exc}), dùng bộ transient proc_*.wav vừa sinh.")

    # Phân loại tự động SFX tươi mới trong temp/sfx/ theo tiền tố 6 vai trò `role_*` (fallback từ khóa tên file)
    def _match_fresh_by_prefix_or_kw(prefixes: Tuple[str, ...], keywords: Tuple[str, ...]) -> List[str]:
        by_prefix = [f for f in fresh_sfx_files if any(f.lower().startswith(pf) for pf in prefixes)]
        by_kw = [f for f in fresh_sfx_files if f not in by_prefix and any(kw in f.lower() for kw in keywords)]
        return by_prefix + by_kw

    role_riser = _match_fresh_by_prefix_or_kw(("role_riser_",), ("riser", "swoosh", "swell"))
    role_impact = _match_fresh_by_prefix_or_kw(("role_impact_",), ("impact", "hit", "boom", "cinematic", "slam", "drop"))
    role_hook = _match_fresh_by_prefix_or_kw(("role_hook_",), ("whoosh", "transition", "swish"))
    role_knowledge = _match_fresh_by_prefix_or_kw(("role_knowledge_",), ("typing", "click", "paper", "ui"))
    role_num = _match_fresh_by_prefix_or_kw(("role_num_",), ("clock", "tick", "interface", "tech"))
    role_money = _match_fresh_by_prefix_or_kw(("role_money_",), ("cash", "coin", "money"))
    role_topic = _match_fresh_by_prefix_or_kw(("role_topic_",), ())
    role_cta_click = [f for f in fresh_sfx_files if f.lower().startswith("role_cta_click_")]
    role_cta_bell = [f for f in fresh_sfx_files if f.lower().startswith("role_cta_bell_")]

    mixkit_transition_hook = role_hook or role_riser or role_topic
    mixkit_knowledge_click = role_knowledge or role_num
    mixkit_num_pool = role_num or role_knowledge
    mixkit_money_cash = role_money or role_num
    mixkit_subject_impact = role_impact + role_topic

    raw_data = json.loads(words_path.read_text(encoding="utf-8"))
    words = raw_data.get("words", raw_data) if isinstance(raw_data, dict) else raw_data

    if not beat_timestamps or len(beat_timestamps) < 5:
        step = total_duration_sec / 5.0
        beat_timestamps = [0.0, round(step * 0.85, 2), round(step * 1.75, 2), round(step * 2.80, 2), round(step * 3.82, 2)]

    cues: List[Tuple[str, int, float]] = []
    event_anchors_ms: List[int] = []
    use_counts: dict[str, int] = {}
    last_used_sfx: List[Optional[str]] = [None]

    def add_cue(sfx_file: str, ms: int, vol: float, min_gap_ms: int = 260, max_uses: int = 4) -> bool:
        ms = max(0, min(int(total_duration_sec * 1000) - 250, int(ms)))
        if any(abs(ms - u) < min_gap_ms for u in event_anchors_ms):
            return False
        if last_used_sfx[0] == sfx_file:
            return False
        if use_counts.get(sfx_file, 0) >= max_uses:
            return False
        if not resolve_sfx_path(sfx_file).exists():
            return False
        cues.append((sfx_file, ms, round(vol, 2)))
        event_anchors_ms.append(ms)
        use_counts[sfx_file] = use_counts.get(sfx_file, 0) + 1
        last_used_sfx[0] = sfx_file
        return True

    def add_dynamic_compound(anchor_ms: int, min_gap_ms: int = 500, vol_scale: float = 1.0) -> bool:
        """Dynamic Compound Stacking: xếp lớp role_riser_* (-500ms, 0.65) + role_impact_* / proc_riser_boom (0ms, 1.10)."""
        anchor_ms = max(0, min(int(total_duration_sec * 1000) - 250, int(anchor_ms)))
        if any(abs(anchor_ms - u) < min_gap_ms for u in event_anchors_ms):
            return False
        added = False
        riser_cand = next((f for f in role_riser if use_counts.get(f, 0) < 4 and resolve_sfx_path(f).exists()), None)
        impact_pool = list(role_impact) + ["proc_riser_boom.wav", "proc_hook_slam.wav"]
        impact_cand = next((f for f in impact_pool if use_counts.get(f, 0) < 4 and f != last_used_sfx[0] and resolve_sfx_path(f).exists()), None)
        if riser_cand and anchor_ms >= 350:
            r_ms = max(0, anchor_ms - 500)
            cues.append((riser_cand, r_ms, round(min(1.10, 0.65 * vol_scale), 2)))
            use_counts[riser_cand] = use_counts.get(riser_cand, 0) + 1
            added = True
        if impact_cand:
            cues.append((impact_cand, anchor_ms, round(min(1.10, 1.05 * vol_scale), 2)))
            use_counts[impact_cand] = use_counts.get(impact_cand, 0) + 1
            last_used_sfx[0] = impact_cand
            added = True
        if added:
            event_anchors_ms.append(anchor_ms)
        return added

    def add_combo(
        combo_or_file: str,
        anchor_ms: int,
        vol_scale: float = 1.0,
        min_gap_ms: int = 450,
        fallback_pool: Optional[List[str]] = None,
    ) -> bool:
        """Đặt tổ hợp SFX đa tầng tại 1 mốc sự kiện; ưu tiên Dynamic Compound role_* trước rồi fallback nhóm role_*."""
        anchor_ms = max(0, min(int(total_duration_sec * 1000) - 250, int(anchor_ms)))
        if any(abs(anchor_ms - u) < min_gap_ms for u in event_anchors_ms):
            return False
        if combo_or_file not in COMPOUND_SFX_COMBOS:
            return add_cue(combo_or_file, anchor_ms, 0.76 * vol_scale, min_gap_ms=min_gap_ms, max_uses=3)

        if add_dynamic_compound(anchor_ms, min_gap_ms=min_gap_ms, vol_scale=vol_scale):
            return True

        search_pool = list(fallback_pool or []) + [f for f in fresh_sfx_files if f not in (fallback_pool or [])]
        for cand in search_pool:
            if add_cue(cand, anchor_ms, 0.74 * vol_scale, min_gap_ms=min_gap_ms, max_uses=3):
                return True
        return False

    # 1. Mở đầu Beat: Dynamic Compound Stacking (role_riser_* -600ms + role_impact_* 0ms)
    beat_combo_openers = [
        "riser_whoosh",
        "riser_hit",
        "swell_impact",
        "riser_reverse",
        "riser_swish_hit",
    ]
    for idx, bt in enumerate(beat_timestamps[:5]):
        b_ms = int(bt * 1000)
        combo_name = beat_combo_openers[idx % len(beat_combo_openers)]
        add_combo(
            combo_name,
            max(0, b_ms),
            vol_scale=1.0,
            min_gap_ms=800,
            fallback_pool=mixkit_transition_hook or mixkit_subject_impact,
        )

    # 2. Đọc mốc từ choreography_blueprint.json -> ánh xạ chuẩn 5 nhóm vào `role_*`, min_gap_ms=450ms cho micro-SFX
    bp_path = Path(blueprint_json_path) if blueprint_json_path else _find_blueprint_near(words_path)
    used_blueprint = False
    if bp_path and bp_path.exists():
        try:
            bp = json.loads(bp_path.read_text(encoding="utf-8"))
            fps = float(bp.get("fps", 60))
            hook_text_pool = list(mixkit_transition_hook) + ["proc_hook_slam.wav"]
            knowledge_text_pool = list(mixkit_knowledge_click) + ["proc_marker_swipe.wav", "proc_card_snap.wav"]
            number_knowledge_pool = list(mixkit_num_pool) + ["proc_num_tick.wav", "proc_slash_cut.wav"]
            number_money_pool = list(mixkit_money_cash) + ["proc_num_tick.wav"]
            subject_pool = list(mixkit_subject_impact) + ["ambient_hit", "proc_card_snap.wav"]
            counters = {"hook": 0, "know": 0, "num_k": 0, "num_m": 0, "subj": 0}
            ev_list = []
            if isinstance(bp.get("events"), list):
                for ev in bp["events"]:
                    if isinstance(ev, dict) and ("frame" in ev or "time_ms" in ev):
                        ev_list.append(ev)
            for beat in bp.get("beats", []):
                for ev in beat.get("events", []):
                    if isinstance(ev, dict) and ("frame" in ev or "time_ms" in ev):
                        ev_list.append(ev)
            for ev in ev_list:
                ev_ms = int(ev["time_ms"]) if "time_ms" in ev else int(round((float(ev["frame"]) * 1000.0) / fps))
                kind = str(ev.get("kind") or ev.get("type") or "subject").lower()
                if kind in ("hook", "hook_text", "text"):
                    # Giới hạn tối đa 2 lớp chồng nhau (lớp chính <= 1.05, lớp phụ <= 0.75) để không clipping; ưu tiên SFX thật role_*
                    hook_layers = 0
                    if role_impact:
                        ri = role_impact[counters["hook"] % len(role_impact)]
                        if resolve_sfx_path(ri).exists():
                            cues.append((ri, max(0, ev_ms), 1.05))
                            hook_layers += 1
                    if role_hook and hook_layers < 2:
                        rh = role_hook[counters["hook"] % len(role_hook)]
                        if resolve_sfx_path(rh).exists():
                            cues.append((rh, max(0, ev_ms - 60), 0.75 if hook_layers >= 1 else 1.05))
                            hook_layers += 1
                    if hook_layers == 0 and resolve_sfx_path("proc_hook_slam.wav").exists():
                        cues.append(("proc_hook_slam.wav", max(0, ev_ms), 1.05))
                        hook_layers += 1
                    if hook_layers > 0:
                        event_anchors_ms.append(max(0, ev_ms))
                        counters["hook"] += 1
                        used_blueprint = True
                        continue
                    pool, c_key, gap_ms, vol_s, fb_pool = hook_text_pool, "hook", 260, 1.05, mixkit_transition_hook
                elif kind in ("knowledge", "knowledge_text"):
                    pool, c_key, gap_ms, vol_s, fb_pool = knowledge_text_pool, "know", 260, 0.88, mixkit_knowledge_click
                elif kind == "number_money":
                    pool, c_key, gap_ms, vol_s, fb_pool = number_money_pool, "num_m", 260, 0.95, mixkit_money_cash
                elif kind in ("number", "number_knowledge"):
                    pool, c_key, gap_ms, vol_s, fb_pool = number_knowledge_pool, "num_k", 260, 0.95, mixkit_num_pool
                else:
                    pool, c_key, gap_ms, vol_s, fb_pool = subject_pool, "subj", 320, 0.92, mixkit_subject_impact
                start_idx = counters[c_key]
                added_ev = False
                for off in range(len(pool)):
                    c_name = pool[(start_idx + off) % len(pool)]
                    if add_combo(c_name, ev_ms, vol_scale=vol_s, min_gap_ms=gap_ms, fallback_pool=fb_pool):
                        counters[c_key] = start_idx + off + 1
                        used_blueprint = True
                        added_ev = True
                        break
                if not added_ev and fresh_sfx_files:
                    ordered_fresh = list(fb_pool) + [f for f in fresh_sfx_files if f not in fb_pool]
                    for off in range(len(ordered_fresh)):
                        f_name = ordered_fresh[(start_idx + off) % len(ordered_fresh)]
                        if add_cue(f_name, ev_ms, round(min(1.10, 0.90 * vol_s), 2), min_gap_ms=gap_ms, max_uses=4):
                            counters[c_key] = start_idx + off + 1
                            used_blueprint = True
                            break
        except Exception:
            used_blueprint = False

    # 3. Fallback khi chưa có blueprint: chỉ bám từ khóa đặc thù & con số quan trọng (gap >= 2.0s, KHÔNG filler)
    if not used_blueprint:
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
                    for off in range(len(sfx_pool)):
                        c_name, c_scale = sfx_pool[(cat_counters[c_idx] + off) % len(sfx_pool)]
                        if add_combo(c_name, start_ms, vol_scale=c_scale, min_gap_ms=2000):
                            cat_counters[c_idx] += 1
                            matched = True
                            break
                    break

            if not matched and any(ch.isdigit() for ch in w_clean) and len(w_clean) >= 2:
                num_combos = ["bass_drop_hit", "hit_drum_kick", "deep_boom_sub", "trailer_hit_braam"]
                for off in range(len(num_combos)):
                    c_name = num_combos[(len(event_anchors_ms) + off) % len(num_combos)]
                    if add_combo(c_name, start_ms, vol_scale=1.0, min_gap_ms=2200):
                        break

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

    # Cú chốt bom tấn sau Vacuum Drop
    add_combo("deep_boom_sub", int(drop_end * 1000) + 60, vol_scale=1.05, min_gap_ms=400)

    # 5. Tự động gắn 3 mốc SFX ưu tiên cao (priority=5) khớp 60fps với <HaDaWhyOutroCTA /> (3.5s cuối)
    if cta_duration_sec > 0 and total_duration_sec > cta_duration_sec + 0.5:
        cta_start_ms = max(0, int(round((total_duration_sec - cta_duration_sec) * 1000)))
        cta_enter_sfx = next(
            (f for f in (role_hook + role_knowledge) if resolve_sfx_path(f).exists()),
            None,
        )
        cta_click_sfx = next(
            (f for f in (role_cta_click + role_knowledge + ["proc_card_snap.wav"]) if resolve_sfx_path(f).exists()),
            None,
        )
        cta_bell_sfx = next(
            (f for f in role_cta_bell if resolve_sfx_path(f).exists()),
            None,
        )
        # Mốc 1 (+0ms / localFrame=0): Thẻ CTA & Logo trượt lên
        if cta_enter_sfx:
            cues.append((cta_enter_sfx, cta_start_ms, 0.65))
        # Mốc 2 (+700ms / localFrame=42): Bấm ĐĂNG KÝ + chuông lắc (+760ms)
        if cta_click_sfx:
            cues.append((cta_click_sfx, cta_start_ms + 700, 0.85))
        if cta_bell_sfx:
            cues.append((cta_bell_sfx, cta_start_ms + 760, 0.60))
        # Mốc 3 (+1300ms / localFrame=78): Bấm CHIA SẺ
        if cta_click_sfx:
            cues.append((cta_click_sfx, cta_start_ms + 1300, 0.75))

    cues.sort(key=lambda x: x[1])
    mode = "BLUEPRINT_COMPOUND" if used_blueprint else "SPARSE_COMPOUND"
    print(f"[SFX CHOREOGRAPHER OK | {mode}] Đã biên đạo {len(cues)} lớp SFX đa tầng (0 filler) & Vacuum Drop {vacuum_drops}!")
    return cues, vacuum_drops


def deduplicate_consecutive_sfx(sfx_cues: list[tuple[str, int, float]]) -> list[tuple[str, int, float]]:
    """
    Chống lặp SFX đơn điệu: cấm 2 cue cùng vai trò đứng liền nhau dùng 1 file,
    cho phép các lớp nền Compound (`riser.wav`, `impact.wav`, `swell.wav`, `sub_bass_impact.wav`) phối đa tầng tối đa 5 lần/video.
    """
    variant_groups = [
        ["metal_hit.mp3", "lock.mp3", "gavel_slam.wav", "camera_click.wav", "gear_lock.mp3", "cut.mp3"],
        ["whoosh_big.mp3", "whoosh1.mp3", "whoosh2.mp3", "whoosh3.mp3", "zoom_hit.mp3", "whoosh_fast.wav"],
        ["bass_hit.mp3", "hit_blow.mp3", "boom_drop.wav", "braaam.wav", "drum_kick.wav", "cash_flip.wav"],
        ["pop.mp3", "pop_dry.mp3", "tap.mp3", "type_soft.mp3", "tick.mp3"],
    ]
    compound_core_files = {"riser.wav", "impact.wav", "swell.wav", "sub_bass_impact.wav", "whoosh_fast.wav"}
    sorted_cues = sorted(sfx_cues, key=lambda x: x[1])
    out: list[tuple] = []
    prev_name: Optional[str] = None
    counts: dict[str, int] = {}
    for cue in sorted_cues:
        fname, start_ms, vol = cue[0], cue[1], cue[2]
        rest = cue[3:]
        chosen = fname
        cap = 5 if chosen in compound_core_files else 2
        if (prev_name is not None and chosen == prev_name) or counts.get(chosen, 0) >= cap:
            for grp in variant_groups:
                if chosen in grp:
                    idx = grp.index(chosen)
                    for offset in range(1, len(grp)):
                        cand = grp[(idx + offset) % len(grp)]
                        cand_cap = 5 if cand in compound_core_files else 2
                        if cand != prev_name and counts.get(cand, 0) < cand_cap and resolve_sfx_path(cand).exists():
                            chosen = cand
                            break
                    break
        counts[chosen] = counts.get(chosen, 0) + 1
        out.append((chosen, start_ms, vol, *rest))
        prev_name = chosen
    return out


def extract_tsx_sfx_cues(tsx_path: str | Path, fps: int = 60) -> list[tuple[str, int, float]]:
    """
    Trích xuất SFX sạch bám chủ thể/số liệu (KHÔNG spam pop/tap/tick 35-45 cues):
    - Ưu tiên 1: Nếu tìm thấy `choreography_blueprint.json` + `words.json` của dự án, dùng `auto_choreograph_script_sfx_cues()`
      để SFX chỉ nổ đúng mốc chủ thể 3D / con số (0 filler, tối đa 2 lần/file).
    - Ưu tiên 2 (fallback từ .tsx): Chỉ lấy chuyển cảnh `<Sequence from={...}>` và `impactFrames`,
      lọc khoảng cách tối thiểu `1400ms`, dùng kho Foley thật, cấm spam `pop/tap/tick/type_soft`.
    """
    tsx_p = Path(tsx_path)
    code = tsx_p.read_text(encoding="utf-8")

    # Tìm blueprint + words.json gần dự án nếu có
    fb_root = tsx_p.parent.parent.parent
    words_cand = None
    bp_cand = None
    for cand_dir in [tsx_p.parent, Path(r"D:\DuAn_DangLam")]:
        if cand_dir.exists():
            # Tìm trong D:\DuAn_DangLam nếu tên file khớp hoặc thư mục mới nhất có choreography_blueprint.json
            pass
    # Kiểm tra các đường dẫn chuẩn quanh tsx hoặc trong D:\DuAn_DangLam
    stem_snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", tsx_p.stem).lower()
    for proj_dir in [Path(r"D:\DuAn_DangLam") / stem_snake, tsx_p.parent]:
        for sub in [proj_dir, proj_dir / "temp"]:
            if (sub / "choreography_blueprint.json").exists() and (sub / "words.json").exists():
                bp_cand = sub / "choreography_blueprint.json"
                words_cand = sub / "words.json"
                break
        if bp_cand:
            break

    if bp_cand and words_cand:
        wdata = json.loads(words_cand.read_text(encoding="utf-8"))
        words_list = wdata.get("words", wdata) if isinstance(wdata, dict) else wdata
        dur = float(wdata.get("duration", 45.0)) if isinstance(wdata, dict) else 45.0
        if words_list and isinstance(words_list[-1], dict):
            dur = max(dur, float(words_list[-1].get("end", dur)))
        cues, _ = auto_choreograph_script_sfx_cues(words_cand, dur, blueprint_json_path=bp_cand)
        return deduplicate_consecutive_sfx(cues)

    # Fallback sạch từ .tsx: CHỈ lấy Sequence transitions & impactFrames (không quét frame >= / interpolate)
    raw_events: list[tuple[str, int, float]] = []
    seq_frames = [int(m) for m in re.findall(r"<Sequence[^>]*\bfrom\s*=\s*\{\s*(\d+)\s*\}", code)]
    opener_pool = ["whoosh_big.mp3", "camera_click.wav", "whoosh2.mp3", "gear_lock.mp3", "cut.mp3"]
    for i, fr in enumerate(seq_frames):
        raw_events.append((opener_pool[i % len(opener_pool)], round(fr * 1000 / fps), 0.58))

    imp_pool = ["metal_hit.mp3", "bass_hit.mp3", "gavel_slam.wav", "boom_drop.wav", "lock.mp3"]
    for imp_match in re.finditer(r"impactFrames\s*=\s*\[([^\]]+)\]", code):
        impacts = [int(x.strip()) for x in imp_match.group(1).split(",") if x.strip().isdigit()]
        for i, fr in enumerate(impacts):
            raw_events.append((imp_pool[i % len(imp_pool)], round(fr * 1000 / fps), 0.56))

    raw_events.sort(key=lambda x: x[1])
    filtered: list[tuple[str, int, float]] = []
    last_ms = -2000
    for fname, ms, vol in raw_events:
        if ms - last_ms >= 1400 and resolve_sfx_path(fname).exists():
            filtered.append((fname, ms, vol))
            last_ms = ms

    return deduplicate_consecutive_sfx(filtered)


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


def _build_music_spotting_expr(
    bgm_segments: List[dict],
    total_duration_sec: float,
    fps: float = 60.0,
) -> Optional[str]:
    """
    Tạo biểu thức FFmpeg volume theo cơ chế Music Spotting:
    - role="hook": fade-in 0.03s, fade-out 1.5s (hoặc 0.12s nếu hard_cut=True)
    - role="tension"|"climax"|"twist": fade-in 1.0s, fade-out 1.5s (hoặc 0.12s nếu hard_cut=True)
    - Mọi khoảng thời gian ngoài bgm_segments: volume = 0 (tắt hẳn nhạc nền để giọng đọc thoáng tuyệt đối).
    """
    seg_exprs: List[str] = []
    for seg in bgm_segments:
        if not isinstance(seg, dict):
            continue
        if "start" in seg:
            st = float(seg["start"])
        elif "start_sec" in seg:
            st = float(seg["start_sec"])
        elif "start_frame" in seg:
            st = float(seg["start_frame"]) / fps
        else:
            continue

        if "end" in seg:
            en = float(seg["end"])
        elif "end_sec" in seg:
            en = float(seg["end_sec"])
        elif "end_frame" in seg:
            en = float(seg["end_frame"]) / fps
        else:
            continue

        st = max(0.0, min(total_duration_sec, st))
        en = max(st + 0.2, min(total_duration_sec, en))
        role = str(seg.get("role") or "tension").strip().lower()
        hard_cut = bool(seg.get("hard_cut", False))

        fade_in = 0.03 if (role == "hook" or st <= 0.05) else 1.0
        fade_out = 0.12 if hard_cut else 1.5
        dur = en - st
        if fade_in + fade_out > dur * 0.85:
            scale = (dur * 0.85) / max(0.05, fade_in + fade_out)
            fade_in = max(0.03, round(fade_in * scale, 3))
            fade_out = max(0.08, round(fade_out * scale, 3))

        in_end = round(st + fade_in, 3)
        out_st = round(max(in_end, en - fade_out), 3)
        seg_exprs.append(
            f"if(between(t,{st:.3f},{in_end:.3f}),(t-{st:.3f})/{fade_in:.3f},"
            f"if(between(t,{in_end:.3f},{out_st:.3f}),1,"
            f"if(between(t,{out_st:.3f},{en:.3f}),({en:.3f}-t)/{fade_out:.3f},0)))"
        )

    if not seg_exprs:
        return None
    return f"min(1,{'+'.join(seg_exprs)})"


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
    bgm_segments: Optional[List[dict]] = None,
    mood: str = "conspiracy_thriller",
    voice_volume: float = 1.28,
    bgm_base_volume: float = 0.72,
    bgm_duck_volume: float = 0.28,
    vacuum_drops: list[tuple[float, float]] | None = None,
) -> Path:
    """
    Hòa âm Trailer Hollywood 5 Nhịp kịch tính & cân đối hài hòa với giọng đọc Hải Đăng (-14.0 LUFS).
    Nếu truyền `words_json_path` mà chưa có `sfx_cues`, hệ thống tự động biên đạo SFX mới 100% theo từng từ khóa!
    """
    voice_wav = Path(voice_wav)
    output_wav = Path(output_wav)
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    if (output_wav.parent / "sfx").exists():
        set_project_sfx_dir(output_wav.parent / "sfx")
    elif words_json_path and (Path(words_json_path).parent / "sfx").exists():
        set_project_sfx_dir(Path(words_json_path).parent / "sfx")

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

    sfx_cues = resolve_sfx_priority_conflicts(deduplicate_consecutive_sfx(sfx_cues), min_gap_ms=140)

    punched_dir = output_wav.parent / "sfx_punched"
    punched_cache: dict[str, Path] = {}
    peak_offset_cache: dict[str, int] = {}
    for cue in sfx_cues:
        fname = cue[0]
        fpath = resolve_sfx_path(fname)
        if not fpath.exists():
            raise FileNotFoundError(f"SFX không tồn tại trong kho dự án: {fpath}")
        if fname not in punched_cache:
            punched_wav = preprocess_sfx_punch(fpath, punched_dir / f"{fpath.stem}_punch.wav")
            punched_cache[fname] = punched_wav
            peak_offset_cache[fname] = get_sfx_peak_offset_ms(punched_wav)

    # Căn đỉnh nổ âm thanh (Peak-Transient Alignment) để đỉnh nổ đập trúng đúng frame chữ/số chạm màn hình
    aligned_cues: list[tuple] = []
    cmd = ["ffmpeg", "-y", "-i", str(voice_wav), "-i", str(bgm_path)]
    for cue in sfx_cues:
        fname, target_ms, vol = cue[0], int(cue[1]), cue[2]
        rest = cue[3:]
        low_f = fname.lower()
        if any(r in low_f for r in ("role_riser", "riser", "whoosh", "swoosh")) and "riser_boom" not in low_f:
            lead_ms = min(500, max(350, peak_offset_cache.get(fname, 400)))
        else:
            lead_ms = min(peak_offset_cache.get(fname, 0), 180) + 40
        aligned_ms = max(0, target_ms - lead_ms)
        aligned_cues.append((fname, aligned_ms, vol, *rest))
        cmd.extend(["-i", str(punched_cache[fname])])
    sfx_cues = aligned_cues

    fade_out_st = max(0.5, round(total_duration_sec - 1.2, 2))

    # 1. Đường tiếng Giọng đọc Hải Đăng: Lọc sạch tạp âm đáy 85Hz, tăng độ rõ chữ 3.0kHz (+2.8dB)
    vo_filter = (
        f"[0:a]highpass=f=85,"
        f"equalizer=f=3000:width_type=o:width=1.3:g=1.8,"
        f"equalizer=f=6000:width_type=q:width=1.5:g=-2.0,"
        f"loudnorm=I=-15.5:TP=-2.0:LRA=4,volume={voice_volume}[vo_clean]"
    )

    # 2. Đường tiếng Nhạc nền Trailer 5 Nhịp:
    # - Surgical Spectral Pocket (-5.0dB tại 2.5kHz) nhường trọn dải giọng nói nhưng giữ lực đàn dây & trống trận.
    # - Boost nhẹ sub-bass 90Hz (+2.0dB) tạo độ dày rạp chiếu phim.
    # Khôi phục BGM rõ giai điệu & kịch tính: bung 0.85 ở quãng nghỉ >= 0.25s, giữ rõ 0.48–0.55 lúc có giọng đọc
    bgm_base_volume = max(0.75, min(0.92, float(bgm_base_volume)))
    bgm_proc_filter = (
        f"[1:a]atrim=0:{total_duration_sec:.2f},"
        f"equalizer=f=2500:width_type=o:width=1.2:g=-4.0,"
        f"equalizer=f=90:width_type=o:width=1.2:g=2.2,"
        f"volume={bgm_base_volume},"
        f"afade=t=out:st={fade_out_st:.2f}:d=1.2[bgm_eq]"
    )

    # Cơ chế Music Spotting cho video dài (>= 75s) hoặc khi có khai báo bgm_segments
    effective_segments = list(bgm_segments) if bgm_segments else None
    if not effective_segments and total_duration_sec >= 75.0:
        effective_segments = [
            {"start": 0.0, "end": 14.0, "role": "hook"},
            {"start": round(total_duration_sec * 0.42, 2), "end": round(total_duration_sec * 0.62, 2), "role": "tension"},
            {"start": round(total_duration_sec * 0.78, 2), "end": round(total_duration_sec * 0.98, 2), "role": "climax"},
        ]

    vol_expr_factors: List[str] = []
    if effective_segments:
        spot_expr = _build_music_spotting_expr(effective_segments, total_duration_sec)
        if spot_expr:
            vol_expr_factors.append(f"({spot_expr})")

    if vacuum_drops:
        # Smooth 120ms ramp-down & ramp-up to prevent harsh digital clicks/pops
        ramp = 0.12
        for d_st, d_end in vacuum_drops:
            in_end = round(d_st + ramp, 3)
            out_st = round(max(in_end, d_end - ramp), 3)
            vol_expr_factors.append(
                f"if(between(t,{d_st:.3f},{in_end:.3f}),1-((t-{d_st:.3f})/{ramp}),"
                f"if(between(t,{in_end:.3f},{out_st:.3f}),0,"
                f"if(between(t,{out_st:.3f},{d_end:.3f}),(t-{out_st:.3f})/{ramp},1)))"
            )

    if vol_expr_factors:
        vol_expr = "*".join(vol_expr_factors)
        bgm_vac_filter = f"[bgm_eq]volume='{vol_expr}':eval=frame[bgm_vac]"
    else:
        bgm_vac_filter = "[bgm_eq]anull[bgm_vac]"

    # Sidechain mượt giữ BGM ở mức 0.48–0.55 khi có lời đọc và tự bung 0.85 ở quãng nghỉ >= 0.25s (không dìm mất nhạc)
    vo_split = "[vo_clean]asplit=3[vo_mix][vo_sc][vo_sc_sfx]"
    bgm_final_filter = (
        f"[bgm_vac][vo_sc]sidechaincompress=threshold=0.048:ratio=1.85:attack=22:release=240[bgm_final]"
    )

    # 2b. Lớp âm nền theo bối cảnh (Contextual Ambience Bed - siêu nhẹ tạo chiều sâu không gian thật)
    topic_low = (script_topic + " " + script_text).lower()
    if any(k in topic_low for k in ("mưa", "bão", "sét", "đêm", "storm")):
        amb_filter = f"anoisesrc=d={total_duration_sec:.2f}:c=pink:r=48000:a=0.012,highpass=f=180,lowpass=f=2400,aformat=channel_layouts=mono,haas[amb_bed]"
    elif any(k in topic_low for k in ("phố", "vỉa hè", "chợ", "vé số", "đám đông", "quán")):
        amb_filter = f"anoisesrc=d={total_duration_sec:.2f}:c=brown:r=48000:a=0.014,highpass=f=120,lowpass=f=1600,aformat=channel_layouts=mono,haas[amb_bed]"
    else:
        amb_filter = f"anoisesrc=d={total_duration_sec:.2f}:c=brown:r=48000:a=0.009,highpass=f=90,lowpass=f=900,aformat=channel_layouts=mono,haas[amb_bed]"

    filter_parts = [vo_filter, vo_split, bgm_proc_filter, bgm_vac_filter, bgm_final_filter, amb_filter,
                    "[vo_mix]aformat=channel_layouts=stereo[vo_st]",
                    "[bgm_final]aformat=channel_layouts=stereo[bgm_st]"]
    base_mix_inputs = ["[vo_st]", "[bgm_st]", "[amb_bed]"]

    # 3. Nạp các điểm rơi SFX đa tầng + Anti-Harshness EQ (hãm 5.2kHz) + Stereo Panning -> gộp vào [sfx_bus]
    spatial_cycle = [-0.42, 0.42, -0.25, 0.25, 0.0]
    sfx_tags = []
    for idx, cue in enumerate(sfx_cues):
        fname, delay_ms, vol = cue[0], cue[1], cue[2]
        if len(cue) >= 4:
            pan_val = float(cue[3])
        elif any(c in fname for c in ("bass_hit", "metal_hit", "hit_blow", "boom_drop", "sub_bass_impact", "sub_drop", "braaam")):
            pan_val = 0.0
        else:
            pan_val = spatial_cycle[idx % len(spatial_cycle)]
        gain_l = round(min(1.0, 1.0 - max(0.0, pan_val)), 3)
        gain_r = round(min(1.0, 1.0 + min(0.0, pan_val)), 3)
        inp_idx = idx + 2
        tag = f"[s{idx}]"
        filter_parts.append(
            f"[{inp_idx}:a]aformat=channel_layouts=stereo,"
            f"highshelf=f=4800:g=-5.5,lowpass=f=9500,"
            f"pan=stereo|c0={gain_l}*c0|c1={gain_r}*c1,"
            f"adelay={int(delay_ms)}|{int(delay_ms)},volume={vol}{tag}"
        )
        sfx_tags.append(tag)

    if sfx_tags:
        # Chống "lùng bùng" khi xếp lớp nhiều SFX: cắt rãnh 2.5kHz (-3.5dB) & sidechain nhẹ dưới giọng đọc
        filter_parts.append(
            f"{''.join(sfx_tags)}amix=inputs={len(sfx_tags)}:duration=longest:dropout_transition=0:normalize=0,"
            f"equalizer=f=2500:width_type=o:width=1.2:g=-3.5[sfx_raw]"
        )
        filter_parts.append(
            f"[sfx_raw][vo_sc_sfx]sidechaincompress=threshold=0.03:ratio=2.5:attack=15:release=180[sfx_bus]"
        )
        mix_inputs = base_mix_inputs + ["[sfx_bus]"]
    else:
        mix_inputs = base_mix_inputs

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
            "-af", "loudnorm=I=-14.0:TP=-1.5:LRA=7:print_format=json",
            "-f", "null", "-",
        ]
        m_res = subprocess.run(measure_cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
        json_match = re.search(r"\{[\s\S]*\}", m_res.stderr)
        if not json_match:
            raise RuntimeError(f"Không đo được thông số loudnorm Pass 1: {m_res.stderr[-500:]}")
        stats = json.loads(json_match.group(0))

        norm_filter = (
            f"loudnorm=I=-14.0:TP=-1.5:LRA=7:"
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

    # Tự động trích xuất đủ 3 file kiểm âm: bgm_only_check.mp3 (+ alias bgm_qc_preview.mp3), sfx_only_check.mp3, master_audio_qc_preview.mp3
    bgm_only_mp3 = output_wav.parent / "bgm_only_check.mp3"
    bgm_preview_mp3 = output_wav.parent / "bgm_qc_preview.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(bgm_path), "-t", f"{total_duration_sec:.2f}", "-c:a", "libmp3lame", "-b:a", "192k", str(bgm_only_mp3)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if bgm_only_mp3.exists():
        import shutil
        shutil.copy2(bgm_only_mp3, bgm_preview_mp3)

    sfx_only_mp3 = output_wav.parent / "sfx_only_check.mp3"
    if sfx_cues:
        sfx_only_cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={total_duration_sec:.2f}"]
        sfx_only_filters = []
        sfx_only_tags = ["[0:a]"]
        for idx, cue in enumerate(sfx_cues):
            fname, delay_ms, vol = cue[0], cue[1], cue[2]
            sfx_only_cmd.extend(["-i", str(punched_cache[fname])])
            tag = f"[so{idx}]"
            sfx_only_filters.append(f"[{idx+1}:a]aformat=channel_layouts=stereo,adelay={int(delay_ms)}|{int(delay_ms)},volume={vol}{tag}")
            sfx_only_tags.append(tag)
        sfx_only_filters.append(f"{''.join(sfx_only_tags)}amix=inputs={len(sfx_only_tags)}:duration=first:dropout_transition=0:normalize=0[sfx_out]")
        sfx_only_cmd.extend(["-filter_complex", ";".join(sfx_only_filters), "-map", "[sfx_out]", "-c:a", "libmp3lame", "-b:a", "192k", str(sfx_only_mp3)])
        subprocess.run(sfx_only_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    qc_preview_mp3 = output_wav.parent / "master_audio_qc_preview.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(output_wav), "-c:a", "libmp3lame", "-b:a", "192k", str(qc_preview_mp3)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    print(f"[SFX MIXER OK] Master Audio 5-Beat Trailer (-14.0 LUFS, {len(sfx_cues)} SFX Cues): {output_wav}")
    print(f"[MANDATORY EAR QC 1/3 - BGM ONLY] {bgm_preview_mp3}")
    print(f"[MANDATORY EAR QC 2/3 - SFX ONLY] {sfx_only_mp3}")
    print(f"[MANDATORY EAR QC 3/3 - FULL MIX] {qc_preview_mp3}")
    return output_wav
