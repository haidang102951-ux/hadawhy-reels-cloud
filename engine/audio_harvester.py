# -*- coding: utf-8 -*-
r"""
audio_harvester.py - CÀO NHẠC NỀN & SFX TƯƠI MỚI 100% THEO CHỦ ĐỀ VÀO DỰ ÁN ĐANG LÀM
(Không lưu kho nhạc/SFX chết trong Đầu Não; mỗi kịch bản mới cào mới vào D:\DuAn_DangLam\<du_an>\temp\)
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import List, Optional
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding="utf-8")

HISTORY_PATH = Path(__file__).parent / "audio_used_history.json"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)


def _load_history() -> dict:
    if HISTORY_PATH.exists():
        try:
            return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"used_bgm_urls": [], "used_sfx_urls": []}


def _save_history(hist: dict) -> None:
    hist["used_bgm_urls"] = hist.get("used_bgm_urls", [])[-1000:]
    hist["used_sfx_urls"] = hist.get("used_sfx_urls", [])[-3000:]
    HISTORY_PATH.write_text(json.dumps(hist, ensure_ascii=False, indent=2), encoding="utf-8")


def _download_file(url: str, out_path: Path) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://mixkit.co/"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 4000:
            return False
        out_path.write_bytes(data)
        return True
    except Exception:
        return False


def _scrape_mixkit_urls(page, url: str, pattern: str) -> List[str]:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=22000)
        page.wait_for_timeout(1600)
        html = page.content()
        found = re.findall(pattern, html)
        # Preserve page order while deduplicating
        seen = set()
        out = []
        for u in found:
            if u not in seen:
                seen.add(u)
                out.append(u)
        return out
    except Exception:
        return []


BANNED_BGM_KEYWORDS = (
    # Nhạc buồn ngủ / nhẹ nhàng / corporate
    "lofi", "lo-fi", "chill", "relax", "calm", "ambient", "sleep",
    "meditation", "study", "acoustic", "romantic", "jazz", "happy", "peaceful",
    "soft", "gentle", "minimal", "slow", "corporate", "uplifting",
    # Nhạc vui tươi / rock / funk / dance / vlog
    "rock", "funk", "funky", "pop", "guitar", "upbeat", "indie", "energetic",
    "vlog", "summer", "motivational", "cheerful", "bright", "groove", "disco",
    "edm", "dance", "trap party",
)

DEFAULT_BGM_QUERIES = [
    "dark cinematic suspense",
    "crime documentary tension",
    "thriller pulse beat",
    "dark investigative bass",
    "intense mystery percussion",
]


def _scrape_mixkit_bgm_cards(page, url: str) -> List[tuple[str, str]]:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=22000)
        p_wait = page.wait_for_timeout(1600)
        items = page.evaluate(
            """() => {
                const cards = Array.from(document.querySelectorAll('[data-audio-player-preview-url-value], .item-grid-card'));
                const out = [];
                for (const c of cards) {
                    const txt = (c.innerText || '').toLowerCase();
                    const html = c.outerHTML || '';
                    const m = html.match(/https:\\/\\/assets\\.mixkit\\.co\\/music\\/\\d+\\/\\d+\\.mp3/);
                    if (m) out.push([m[0], txt]);
                }
                return out;
            }"""
        )
        seen = set()
        out = []
        for mp3_url, card_txt in items:
            if mp3_url in seen:
                continue
            if any(bad in card_txt for bad in BANNED_BGM_KEYWORDS):
                continue
            seen.add(mp3_url)
            out.append((mp3_url, card_txt.strip().splitlines()[0] if card_txt.strip() else mp3_url))
        return out
    except Exception:
        return []


def score_bgm_excitement(audio_path: Path) -> float:
    """
    Chấm điểm độ kịch tính & nhịp trống của BGM (0..100) trên 25s đầu bằng FFmpeg + NumPy:
    - Năng lượng trầm 40-160Hz (sub/kick punch)
    - Mật độ xung trống (onset density)
    - Độ tương phản động (dynamic contrast)
    Nhạc phẳng lì/chậm (< 65/100) sẽ bị loại tự động.
    """
    import subprocess
    import numpy as np

    try:
        cmd = [
            "ffmpeg", "-v", "error", "-i", str(audio_path),
            "-t", "25", "-ac", "1", "-ar", "16000", "-f", "f32le", "pipe:1",
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=20)
        if res.returncode != 0 or len(res.stdout) < 16000 * 4:
            return 0.0
        sig = np.frombuffer(res.stdout, dtype=np.float32)
        if np.max(np.abs(sig)) < 1e-4:
            return 0.0

        # 1. Năng lượng trầm 40-160Hz (FFT)
        n = min(len(sig), 16000 * 25)
        spec = np.abs(np.fft.rfft(sig[:n])) ** 2
        freqs = np.fft.rfftfreq(n, d=1.0 / 16000.0)
        total_e = float(np.sum(spec) + 1e-9)
        bass_e = float(np.sum(spec[(freqs >= 40.0) & (freqs <= 160.0)]))
        bass_ratio = bass_e / total_e
        bass_score = min(35.0, (bass_ratio / 0.18) * 35.0)

        # 2. Mật độ xung trống (onset density theo khung 50ms = 800 samples)
        hop = 800
        n_frames = len(sig) // hop
        if n_frames < 10:
            return 0.0
        frames = sig[: n_frames * hop].reshape(n_frames, hop)
        rms = np.sqrt(np.mean(frames ** 2, axis=1) + 1e-9)
        diff = np.maximum(0.0, np.diff(rms))
        thresh = float(np.mean(diff) + 1.15 * np.std(diff))
        onsets = int(np.sum(diff > max(thresh, 1e-4)))
        onsets_per_sec = onsets / (n_frames * 0.05)
        onset_score = min(35.0, (onsets_per_sec / 2.2) * 35.0)

        # 3. Độ tương phản động (p95 / median RMS)
        med = float(np.median(rms) + 1e-6)
        p95 = float(np.percentile(rms, 95))
        contrast = p95 / med
        contrast_score = min(30.0, max(0.0, (contrast - 1.15) / 1.4) * 30.0)

        total_score = round(bass_score + onset_score + contrast_score, 1)
        return float(total_score)
    except Exception:
        return 0.0


def harvest_fresh_bgm(project_dir: Path, mood_query: str = "dark,suspense,thriller,mystery") -> Path:
    temp_dir = Path(project_dir) / "temp"
    temp_dir.mkdir(parents=True, exist_ok=True)
    out_bgm = temp_dir / "bgm_fresh.mp3"
    hist = _load_history()
    used_bgm = set(hist.get("used_bgm_urls", []))

    # Ưu tiên nhóm từ khóa tối, kịch tính, điều tra rõ rệt — CẤM nhạc vui tươi / rock / funk / lofi
    urls_to_scan = [
        f"https://mixkit.co/free-stock-music/discover/{re.sub(r'[^a-z0-9]+', '-', q.lower()).strip('-')}/"
        for q in DEFAULT_BGM_QUERIES
    ] + [
        "https://mixkit.co/free-stock-music/tag/suspense/",
        "https://mixkit.co/free-stock-music/tag/thriller/",
        "https://mixkit.co/free-stock-music/tag/tension/",
        "https://mixkit.co/free-stock-music/tag/dark/",
        "https://mixkit.co/free-stock-music/tag/mystery/",
        "https://mixkit.co/free-stock-music/tag/trailer/",
    ]
    for raw_s in mood_query.split(","):
        sl = re.sub(r"[^a-z0-9\-]", "", raw_s.strip().lower().replace(" ", "-"))
        if sl and not any(bad in sl for bad in BANNED_BGM_KEYWORDS) and sl not in ("dramatic", "thriller", "cinematic", "suspense", "dark", "mystery"):
            urls_to_scan.insert(0, f"https://mixkit.co/free-stock-music/tag/{sl}/")

    candidates: List[tuple[str, str]] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()
        for page_url in urls_to_scan:
            candidates.extend(_scrape_mixkit_bgm_cards(page, page_url))
        browser.close()

    fresh = [(u, t) for (u, t) in candidates if u not in used_bgm] or candidates
    best_fallback: Optional[tuple[float, str, str, bytes]] = None
    tmp_bgm = temp_dir / "tmp_bgm_eval.mp3"

    for u, title in fresh[:18]:
        if not _download_file(u, tmp_bgm):
            continue
        sc = score_bgm_excitement(tmp_bgm)
        print(f"   [BGM SCORE] '{title[:40]}' -> {sc}/100")
        if sc >= 72.0:
            out_bgm.write_bytes(tmp_bgm.read_bytes())
            tmp_bgm.unlink(missing_ok=True)
            hist.setdefault("used_bgm_urls", []).append(u)
            _save_history(hist)
            print(f"[AUDIO HARVESTER BGM OK | SCORE {sc}/100 >= 72] '{title}' ({u}) -> {out_bgm}")
            return out_bgm
        if best_fallback is None or sc > best_fallback[0]:
            best_fallback = (sc, u, title, tmp_bgm.read_bytes())

    tmp_bgm.unlink(missing_ok=True)
    if best_fallback is not None:
        sc, u, title, raw_bytes = best_fallback
        out_bgm.write_bytes(raw_bytes)
        hist.setdefault("used_bgm_urls", []).append(u)
        _save_history(hist)
        print(f"[AUDIO HARVESTER BGM FALLBACK BEST | SCORE {sc}/100] '{title}' -> {out_bgm}")
        return out_bgm

    raise RuntimeError(f"Không tải được nhạc nền hồi hộp/kịch tính mới từ Mixkit cho mood={mood_query}")


BANNED_SFX_KEYWORDS = (
    "cartoon", "comedy", "funny", "cute", "toy", "boing", "bubble",
    "8-bit", "arcade", "retro", "laugh", "applause", "meow", "dog", "baby",
    "chill", "lofi", "relax", "magic", "fairy", "sparkle",
    "bell", "bells", "chime", "chimes", "ring", "ringing", "alarm", "siren",
    "howl", "howling", "screech", "scream", "shriek", "whistle", "horn",
    "buzz", "buzzer", "beep", "laser", "zap", "shrill", "high pitch",
    "ting", "ding", "gong", "church",
)


BANNED_CTA_BELL_KEYWORDS = (
    "alarm", "siren", "church", "gong", "cartoon", "comedy", "funny",
    "horror", "scream", "screech", "howl", "buzzer", "airhorn",
)


def _scrape_mixkit_sfx_cards(
    page,
    url: str,
    banned_keywords: tuple[str, ...] = BANNED_SFX_KEYWORDS,
) -> List[tuple[str, str]]:
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=22000)
        page.wait_for_timeout(1500)
        items = page.evaluate(
            """() => {
                const cards = Array.from(document.querySelectorAll('[data-audio-player-preview-url-value], .item-grid-card'));
                const out = [];
                for (const c of cards) {
                    const txt = (c.innerText || '').toLowerCase();
                    const html = c.outerHTML || '';
                    const m = html.match(/https:\\/\\/assets\\.mixkit\\.co\\/active_storage\\/sfx\\/\\d+\\/\\d+-preview\\.mp3/);
                    if (m) out.push([m[0], txt]);
                }
                return out;
            }"""
        )
        seen = set()
        out = []
        for mp3_url, card_txt in items:
            if mp3_url in seen:
                continue
            if any(bad in card_txt for bad in banned_keywords):
                continue
            seen.add(mp3_url)
            title = card_txt.strip().splitlines()[0] if card_txt.strip() else mp3_url
            out.append((mp3_url, title))
        return out
    except Exception:
        return []


ROLE_SFX_GROUPS = [
    ("role_riser", ["cinematic", "swoosh", "riser"], 2),
    ("role_impact", ["impact", "hit", "boom"], 2),
    ("role_hook", ["whoosh", "transition"], 2),
    ("role_knowledge", ["typing", "click", "paper", "ui"], 2),
    ("role_num", ["clock", "tick", "interface", "tech"], 2),
]

ROLE_CTA_GROUPS = [
    ("role_cta_click", ["mouse-click", "click"], 2, BANNED_SFX_KEYWORDS),
    ("role_cta_bell", ["notification", "bell"], 2, BANNED_CTA_BELL_KEYWORDS),
]

ROLE_MONEY_GROUP = ("role_money", ["cash", "coins", "money"], 2)


def harvest_fresh_sfx(
    project_dir: Path,
    topic_keywords: Optional[List[str]] = None,
    count: int = 14,
    include_money: bool = False,
) -> List[Path]:
    """
    Cào SFX tươi mới 100% vào temp/sfx/ theo 6 nhóm vai trò + từ khóa chủ đề kịch bản:
    - role_riser_*.mp3, role_impact_*.mp3, role_hook_*.mp3, role_knowledge_*.mp3, role_num_*.mp3
    - role_money_*.mp3 (chỉ cào khi include_money=True)
    - role_topic_*.mp3 (2-3 file theo --sfx-keywords riêng của kịch bản)
    """
    sfx_dir = Path(project_dir) / "temp" / "sfx"
    sfx_dir.mkdir(parents=True, exist_ok=True)
    hist = _load_history()
    used_sfx = set(hist.get("used_sfx_urls", []))

    groups: List[tuple[str, List[str], int, tuple[str, ...]]] = [
        (rp, kws, tn, BANNED_SFX_KEYWORDS) for (rp, kws, tn) in ROLE_SFX_GROUPS
    ]
    groups.extend(ROLE_CTA_GROUPS)
    if include_money:
        rp, kws, tn = ROLE_MONEY_GROUP
        groups.append((rp, kws, tn, BANNED_SFX_KEYWORDS))

    topic_kws = [re.sub(r"[^a-z0-9\-]", "", k.strip().lower()) for k in (topic_keywords or []) if k.strip()]
    if topic_kws:
        groups.append(("role_topic", topic_kws, 3, BANNED_SFX_KEYWORDS))

    downloaded: List[Path] = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA)
        page = ctx.new_page()

        for role_prefix, kw_list, target_n, banned_kws in groups:
            picked_for_role = 0
            for kw in kw_list:
                if picked_for_role >= target_n:
                    break
                cards = _scrape_mixkit_sfx_cards(
                    page,
                    f"https://mixkit.co/free-sound-effects/{kw}/",
                    banned_keywords=banned_kws,
                )
                fresh = [(u, t) for (u, t) in cards if u not in used_sfx] or cards
                for u, title in fresh:
                    if picked_for_role >= target_n:
                        break
                    sid = re.search(r"/(\d+)-preview\.mp3", u)
                    fname = f"{role_prefix}_{kw}_{sid.group(1) if sid else len(downloaded)}.mp3"
                    out_p = sfx_dir / fname
                    if _download_file(u, out_p):
                        downloaded.append(out_p)
                        used_sfx.add(u)
                        hist.setdefault("used_sfx_urls", []).append(u)
                        picked_for_role += 1
                        print(f"[AUDIO HARVESTER SFX OK | {role_prefix.upper()}] '{title}' -> {fname}")
        browser.close()

    _save_history(hist)
    if not downloaded:
        raise RuntimeError("Không tải được SFX kịch tính mới nào cho dự án!")
    return downloaded


def main() -> int:
    ap = argparse.ArgumentParser(description="Harvest fresh BGM & 6-role topic-matched SFX into project temp/")
    ap.add_argument("--project", required=True, help="Thư mục dự án (VD: D:\\DuAn_DangLam\\ten_du_an)")
    ap.add_argument("--sfx-keywords", default="transition,impact,technology", help="Từ khóa SFX tiếng Anh cách nhau dấu phẩy")
    ap.add_argument("--bgm-mood", default="dark,suspense,thriller,mystery", help="Mood nhạc nền tối/kịch tính/điều tra (CẤM nhạc vui/rock/funk/lofi)")
    ap.add_argument("--sfx-count", type=int, default=14)
    ap.add_argument("--include-money", action="store_true", help="Bật cào nhóm role_money_*.mp3 (khi kịch bản có yếu tố tiền)")
    ap.add_argument("--sfx-only", action="store_true", help="Chỉ cào SFX 6 vai trò, bỏ qua tải BGM Mixkit trước (ưu tiên AI tự sinh BGM)")
    args = ap.parse_args()

    proj = Path(args.project)
    kws = [k.strip() for k in args.sfx_keywords.split(",") if k.strip()]
    if not args.sfx_only:
        harvest_fresh_bgm(proj, mood_query=args.bgm_mood)
    harvest_fresh_sfx(proj, topic_keywords=kws, count=args.sfx_count, include_money=args.include_money)
    return 0


if __name__ == "__main__":
    sys.exit(main())
