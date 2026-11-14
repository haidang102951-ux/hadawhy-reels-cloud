"""Pre-Render Gate for FB Reels 9:16 Remotion compositions.

Catches common subagent failures BEFORE spending ~80s on `npx remotion render`:
1. Missing `@font-face` (`BeVietnamPro`) inside the composition `.tsx`.
2. Opaque/semi-opaque text card boxes (`backgroundColor` + `borderRadius` + `border` wrapping text) violating Zero-Box.
3. Missing geographic map visuals (`MAP_` / `<svg` / `GeoStrategicMap3D`) when `script_scenes.json` mentions countries/world.
4. Missing `words.json` alignment or voice audio asset.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

COUNTRY_KEYWORDS = (
    "nước anh", "london", "nước pháp", "paris", "nước mỹ", "hoa kỳ", "mỹ",
    "việt nam", "trung quốc", "nhật bản", "nga", "đức", "châu âu", "châu á",
    "thế giới", "toàn cầu",
)


def inspect_composition(tsx_path: Path, project_dir: Path) -> dict:
    issues: list[str] = []
    warnings: list[str] = []

    if not tsx_path.exists():
        return {"passed": False, "issues": [f"Missing composition file: {tsx_path}"], "warnings": []}

    code = tsx_path.read_text(encoding="utf-8")

    # 1. @font-face check
    if "@font-face" not in code or "BeVietnamPro" not in code:
        issues.append("MISSING @font-face BeVietnamPro in composition .tsx (causes ugly system font fallback).")

    # 2. Zero-Box check: detect dark card boxes wrapping text
    box_pattern = re.compile(
        r"backgroundColor\s*:\s*[\"']rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*0\.[789]\d*\s*\)[\"']",
        re.IGNORECASE,
    )
    box_matches = box_pattern.findall(code)
    if box_matches:
        issues.append(
            f"ZERO-BOX VIOLATION: Found {len(box_matches)} opaque dark backgroundColor box(es) ({box_matches[0]}). "
            "Use floating typography with textShadow + thin underline/transparent ink stamp instead."
        )

    # 3. words.json & audio check
    words_file = project_dir / "words.json"
    if not words_file.exists():
        issues.append(f"Missing words.json at {words_file}; timings cannot be verified against voiceover.")
    else:
        words_data = json.loads(words_file.read_text(encoding="utf-8"))
        dur = float(words_data.get("audio_duration_sec", 0))
        if dur <= 0:
            issues.append("words.json has invalid audio_duration_sec <= 0.")

    # 4. Geographic map check if script mentions countries/global spread
    scenes_file = project_dir / "script_scenes.json"
    if scenes_file.exists():
        scenes_text = scenes_file.read_text(encoding="utf-8").lower()
        mentioned = [kw for kw in COUNTRY_KEYWORDS if kw in scenes_text]
        if mentioned:
            has_map = ("<svg" in code and "path" in code) or "GeoStrategicMap3D" in code or "MAP_" in code
            if not has_map:
                issues.append(
                    f"MISSING GEO MAP: Script mentions {mentioned[:5]}, but composition has no SVG/GeoJSON map visual."
                )

    # 5. Watermark & KineticWordCaption check
    if "<ChannelWatermark9x16" not in code:
        issues.append("Missing <ChannelWatermark9x16 /> 2-layer copyright watermark.")
    if "<KineticWordCaption" not in code:
        issues.append("Missing <KineticWordCaption />.")

    return {
        "passed": len(issues) == 0,
        "tsx_path": str(tsx_path),
        "issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-Render Gate for FB Reels Remotion composition.")
    parser.add_argument("--tsx", required=True, help="Path to composition .tsx file")
    parser.add_argument("--project", required=True, help="Path to D:\\DuAn_DangLam\\<project_id>")
    args = parser.parse_args()

    result = inspect_composition(Path(args.tsx), Path(args.project))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
