"""
VOICE-VISUAL SYNC - hình & hiệu ứng phải BÁM THEO GIỌNG ĐỌC (luật chung cho mọi kịch bản).

Nguyên tắc (Người Chỉ Huy):
  - Hiệu ứng/hình chỉ xuất hiện khi giọng đọc nói tới nó, không rải theo đồng hồ để lấp chỗ trống.
  - Mỗi câu thoại chỉ hiện đúng thứ cần để người xem hiểu: CHỦ THỂ chính (mô hình 3D thật) và CON SỐ quan trọng.
    Ví dụ câu "...thị trường chip AI đã thống trị được 40.000$" -> chỉ hiện: hình chip AI + con số 40.000$.

Nguồn dữ liệu:
  - words.json (mốc thời gian từng từ của giọng đọc) trong <project>/temp/ hoặc <project>/.
  - choreography_blueprint.json: mỗi beat có events dạng
        {"frame": 126, "kind": "subject", "show": "chip AI", "voice_word": "chip"}
        {"frame": 228, "kind": "number",  "show": "40.000$"}
    kind = subject | number | text. 'voice_word' là từ trong lời đọc kích hoạt hình đó (số thì tự dò theo chữ số).

Kiểm tra:
  1. SYNC: hình xuất hiện sớm tối đa LEAD_SEC hoặc trễ tối đa LAG_SEC so với lúc giọng đọc nói từ/số đó.
  2. COVERAGE: mọi con số quan trọng trong lời đọc đều có hình hiển thị số đó.
  3. MINIMAL: mỗi câu tối đa MAX_PER_SENTENCE_BLOCK hình quan trọng (khuyến nghị <= MAX_PER_SENTENCE_WARN).

Dùng:
  python voice_visual_sync.py --tsx <file.tsx> --project <D:\\DuAn_DangLam\\id>
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FPS = 60
LEAD_SEC = 0.5               # hình được hiện sớm tối đa 0.5s trước khi giọng đọc nói
LAG_SEC = 0.6                # hoặc trễ tối đa 0.6s sau khi giọng đọc nói
PAUSE_SEC = 0.6              # khoảng lặng >= 0.6s coi như hết câu
MAX_PER_SENTENCE_WARN = 2    # khuyến nghị: chủ thể + con số
MAX_PER_SENTENCE_BLOCK = 3   # vượt mức này là rối mắt -> chặn
KINDS = ("subject", "number", "text", "hook", "hook_text", "knowledge", "knowledge_text", "number_knowledge", "number_money")


def find_words_json(project_dir: Path | str) -> Path | None:
    """Vị trí words.json thống nhất cho MỌI gate. Các công cụ cũ ghi ở nhiều chỗ khác nhau:
    <project>/words.json, <project>/temp/words.json, <project>/gate_tmp/words.json (cloud_reels_runner),
    <project>/**/<prefix>_words.json (vieneu_whisper_pacer). Lấy file mới nhất."""
    project_dir = Path(project_dir)
    fixed = [project_dir / "temp" / "words.json", project_dir / "words.json", project_dir / "gate_tmp" / "words.json"]
    found = [p for p in fixed if p.exists()]
    if not found and project_dir.exists():
        found = [p for p in project_dir.rglob("*words.json") if p.is_file()]
    return max(found, key=lambda p: p.stat().st_mtime) if found else None


def _load_words(project_dir: Path) -> list[dict]:
    cand = find_words_json(project_dir)
    if cand is not None:
        if True:
            data = json.loads(cand.read_text(encoding="utf-8"))
            items = data.get("words", data) if isinstance(data, dict) else data
            out: list[dict] = []
            for w in items:
                if "start" in w:
                    st = float(w["start"])
                elif "startMs" in w:
                    st = float(w["startMs"]) / 1000.0
                else:
                    st = 0.0
                if "end" in w:
                    en = float(w["end"])
                elif "endMs" in w:
                    en = float(w["endMs"]) / 1000.0
                else:
                    en = None
                out.append({"text": str(w.get("word", w.get("text", ""))), "start": st, "end": en})
            return out
    return []


def _load_events(project_dir: Path) -> list[dict]:
    for cand in (project_dir / "temp" / "choreography_blueprint.json", project_dir / "choreography_blueprint.json"):
        if cand.exists():
            bp = json.loads(cand.read_text(encoding="utf-8"))
            ev: list[dict] = []
            raw_list = list(bp.get("events") or [])
            for b in bp.get("beats", []):
                raw_list.extend(b.get("events") or [])
            for e in raw_list:
                if isinstance(e, dict) and "frame" in e:
                    k = e.get("kind") or e.get("type")
                    if k in KINDS:
                        norm_e = dict(e)
                        norm_e["kind"] = k
                        ev.append(norm_e)
            return ev
    return []


def _norm(s: str) -> str:
    return re.sub(r"[^\w]", "", s.lower())


def _digits(s: str) -> str:
    return re.sub(r"\D", "", s)


def _is_key_number(token: str) -> bool:
    d = _digits(token)
    return bool(d) and (len(d) >= 2 or bool(re.search(r"[%$đ₫]", token)))


def _sentences(words: list[dict]) -> list[tuple[float, float]]:
    """Cắt câu theo dấu chấm/hỏi/than hoặc khoảng lặng dài. Trả về [(t_start, t_end)]."""
    spans: list[tuple[float, float]] = []
    if not words:
        return spans
    s0 = words[0]["start"]
    for i, w in enumerate(words):
        nxt = words[i + 1] if i + 1 < len(words) else None
        end_t = w["end"] if w["end"] is not None else (nxt["start"] if nxt else w["start"] + 0.4)
        ends = bool(re.search(r"[.!?…]$", w["text"].strip()))
        gap = (nxt["start"] - end_t) if nxt else 99.0
        if ends or gap >= PAUSE_SEC or nxt is None:
            spans.append((s0, end_t))
            if nxt:
                s0 = nxt["start"]
    return spans


def check(project_dir: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []
    words = _load_words(project_dir)
    events = _load_events(project_dir)

    if not words:
        warnings.append("VOICE SYNC bỏ qua: chưa có words.json (không có mốc giọng đọc để đối chiếu).")
        return {"passed": True, "issues": issues, "warnings": warnings}
    if not events:
        issues.append(
            "VOICE SYNC BLUEPRINT THIẾU (Luật 12): choreography_blueprint.json phải có events dạng "
            "{frame, kind: subject|number|text, show, voice_word} bám theo mốc giọng đọc trong words.json. "
            "Mỗi câu chỉ lập sự kiện cho chủ thể chính và con số quan trọng."
        )
        return {"passed": False, "issues": issues, "warnings": warnings}

    key_tokens = [(w["start"], _digits(w["text"])) for w in words if _is_key_number(w["text"])]

    # 1. SYNC từng sự kiện với lời đọc
    for e in events:
        t = int(e["frame"]) / FPS
        show = str(e.get("show", ""))
        kind = e["kind"]
        if kind in ("number", "number_knowledge", "number_money"):
            d = _digits(show)
            starts = [s for s, dd in key_tokens if dd == d] or [
                w["start"] for w in words if _digits(w["text"]) == d and d
            ]
            label = f"số '{show}'"
        else:
            show_first = show.split()[0] if show.split() else ""
            vw = str(e.get("voice_word") or show_first)
            first = _norm(vw.split()[0]) if vw.split() else ""
            starts = [w["start"] for w in words if first and _norm(w["text"]) == first]
            label = f"hình '{show}' (từ '{vw}')"
        if not starts:
            issues.append(f"VOICE SYNC (Luật 12): {label} không có trong lời đọc words.json - hình không có điểm neo giọng đọc.")
            continue
        near = min(starts, key=lambda s: abs(s - t))
        delta = t - near
        if not (-LEAD_SEC <= delta <= LAG_SEC):
            when = "SỚM" if delta < 0 else "TRỄ"
            issues.append(
                f"VOICE SYNC (Luật 12): {label} hiện {when} {abs(delta):.2f}s so với lúc giọng đọc nói "
                f"(cho phép sớm <= {LEAD_SEC}s, trễ <= {LAG_SEC}s). Dời frame về ~{int(round(near * FPS))}."
            )

    # 2. COVERAGE con số quan trọng
    shown = {_digits(str(e.get("show", ""))) for e in events if e["kind"] in ("number", "number_knowledge", "number_money")}
    for s, d in key_tokens:
        if d not in shown:
            issues.append(
                f"VOICE SYNC COVERAGE (Luật 12): giọng đọc nói con số quan trọng tại {s:.2f}s (chữ số {d}) "
                "nhưng chưa có sự kiện kind=number hiển thị số đó."
            )
    # chỉ báo mỗi con số một lần
    issues[:] = list(dict.fromkeys(issues))

    # 3. MINIMAL: số hình quan trọng mỗi câu
    for i, (a, b) in enumerate(_sentences(words), 1):
        n = sum(1 for e in events if a - LEAD_SEC <= int(e["frame"]) / FPS <= b + LAG_SEC)
        if n > MAX_PER_SENTENCE_BLOCK:
            issues.append(
                f"VOICE SYNC MINIMAL (Luật 12): câu #{i} ({a:.1f}s-{b:.1f}s) có {n} hình quan trọng "
                f"(tối đa {MAX_PER_SENTENCE_BLOCK}). Chỉ giữ chủ thể chính + con số quan trọng."
            )
        elif n > MAX_PER_SENTENCE_WARN:
            warnings.append(f"Câu #{i} có {n} hình quan trọng (> {MAX_PER_SENTENCE_WARN}) - nên rút còn chủ thể + con số.")

    return {"passed": not issues, "issues": issues, "warnings": warnings, "events": len(events)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsx", help="(không bắt buộc) giữ để đồng bộ giao diện với các gate khác")
    ap.add_argument("--project", required=True)
    a = ap.parse_args()
    res = check(Path(a.project))
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
