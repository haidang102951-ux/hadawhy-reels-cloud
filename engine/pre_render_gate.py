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

    # 1. @font-face & KineticHook check
    if ("@font-face" not in code and "HaDaWhyFontFaces" not in code) or ("BeVietnamPro" not in code and "HaDaWhyFontFaces" not in code):
        issues.append("MISSING @font-face / HaDaWhyFontFaces in composition .tsx (causes ugly system font fallback).")

    if "KineticHookHeader" not in code and "hookSpring" not in code:
        issues.append("MISSING KINETIC TEXT HOOK: Must use <KineticHookHeader /> or dynamic spring slam (1.38 -> 1.0) on hooks.")

    # 1b. Total ban on ALL plastic cartoon emoji, objects/*.png, demo_archive, and repetitive StickerPop
    if re.search(r'["\'\`/]objects/[a-z0-9_.\-]+', code, re.IGNORECASE):
        issues.append("BANNED PLASTIC ICON: Found reference to objects/* icon. All cartoon/plastic icons are permanently banned. Use real HD photos, custom cutouts, or programmed data graphics.")
    if re.search(r'["\'\`/]demo_archive/[a-z0-9_.\-]+', code, re.IGNORECASE):
        issues.append("BANNED ARCHIVE ASSET: Found reference to deleted demo_archive/* folder.")
    if "StickerPop" in code:
        issues.append("BANNED LEGACY EFFECT: StickerPop (pop-and-shake) is banned. Use CapCutTransitions + KineticTextFX + KnowledgeMotionFX from ./components/fx.")
    objects_dir = tsx_path.parent.parent / "public" / "objects"
    if objects_dir.exists():
        issues.append(f"BANNED FOLDER EXISTS: {objects_dir} must remain deleted so plastic icons cannot be reused.")

    fx_primitives = (
        "WhipPanTransition", "ZoomThroughTransition", "SplitCurtainWipe", "Tilt3DFlip",
        "MarkerHighlightText", "StaggerWaveText", "GlitchSplitText", "MetallicSweepText",
        "OdometerCounter", "ParallaxDepthStage", "DotMatrixZoom", "FlowPipeline3D",
        "DecisionBranchPulse", "Real3DPhotoStage", "DataBars3D", "MotionTrackedCallout",
    )
    fx_used = sum(1 for name in fx_primitives if name in code)
    if fx_used < 2:
        issues.append(
            f"LOW FX DIVERSITY: Found only {fx_used} modern FX primitive(s) from ./components/fx. "
            "Must combine at least 2 dynamic transition/text/knowledge FX (CapCutTransitions, KineticTextFX, KnowledgeMotionFX)."
        )

    # 2. Zero-Box check: detect ANY dark card boxes wrapping text (background or backgroundColor rgba)
    box_pattern = re.compile(
        r"(?:backgroundColor|background)\s*:\s*[\"']rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*0\.[456789]\d*\s*\)[\"']",
        re.IGNORECASE,
    )
    box_matches = box_pattern.findall(code)
    if box_matches:
        issues.append(
            f"ZERO-BOX VIOLATION: Found {len(box_matches)} dark background/backgroundColor box(es) ({box_matches[0]}). "
            "Use pure spatial floating typography with WebkitTextStroke + textShadow."
        )

    # 3. words.json & dead-air silence check
    words_file = project_dir / "words.json"
    if not words_file.exists():
        issues.append(f"Missing words.json at {words_file}; timings cannot be verified against voiceover.")
    else:
        words_data = json.loads(words_file.read_text(encoding="utf-8"))
        words_list = words_data.get("words", words_data) if isinstance(words_data, dict) else words_data
        dur = float(words_data.get("audio_duration_sec", 0)) if isinstance(words_data, dict) else (words_list[-1]["end"] if words_list else 0)
        if dur <= 0:
            issues.append("words.json has invalid audio_duration_sec <= 0.")
        # Check for unnatural dead-air gaps > 1.4s between spoken words
        for i in range(len(words_list) - 1):
            gap = float(words_list[i + 1].get("start", 0)) - float(words_list[i].get("end", 0))
            if gap > 1.4:
                issues.append(
                    f"DEAD AIR IN VOICEOVER: {gap:.2f}s silence between '{words_list[i].get('word')}' and '{words_list[i+1].get('word')}'. "
                    "Voiceover must flow naturally with <= 0.8s gaps."
                )
                break

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

    # 5. Watermark, NO-Karaoke-Captions & Channel DNA Level-1 Blue Mist (#42B2F2) Lock
    if "<ChannelWatermark9x16" not in code:
        issues.append("Missing <ChannelWatermark9x16 /> 2-layer copyright watermark.")
    if "<KineticWordCaption" in code:
        issues.append(
            "DEPRECATED KARAOKE CAPTION: Found <KineticWordCaption in composition. "
            "Bottom running subtitles are banned; dedicate Y:520..1580 to 3D visual illustrations."
        )
    if "<HaDaWhyMistBackground" not in code:
        issues.append(
            "MISSING CHANNEL DNA BACKDROP: Must use <HaDaWhyMistBackground intensity={0.11} accentHex=\"66, 178, 242\" />."
        )
    elif 'accentHex="255' in code or "Forensic Grid" in code or "Tech Circuit Grid" in code or 'id="grid"' in code:
        issues.append(
            "WRONG BACKDROP DNA: Found square grid or non-brand yellow/red mist color. "
            "Channel DNA Level-1 requires pure #42B2F2 (66, 178, 242) mist with NO square grid."
        )

    # 6. Strict HD Resolution & Laplacian Sharpness Gate for referenced harvested/objects images
    public_dir = tsx_path.parent.parent / "public"
    img_refs = re.findall(r'staticFile\(\s*["\']((?:harvested|objects)/[^"\']+\.(?:png|jpg|jpeg|webp))["\']\s*\)', code)
    if img_refs and public_dir.exists():
        try:
            from PIL import Image
            import cv2
            import numpy as np
            for rel_ref in sorted(set(img_refs)):
                img_path = public_dir / rel_ref
                if not img_path.exists():
                    issues.append(f"MISSING ASSET: {rel_ref} not found in {public_dir}")
                    continue
                with Image.open(img_path) as im:
                    w, h = im.size
                    if rel_ref.startswith("harvested/"):
                        if im.mode == "RGBA":
                            if max(w, h) < 900 or min(w, h) < 600:
                                issues.append(f"LOW-RES CUTOUT: {rel_ref} is {w}x{h} (HD cutout requires >= 900px long side & >= 600px short side).")
                                continue
                        elif min(w, h) < 900:
                            issues.append(f"LOW-RES PHOTO: {rel_ref} is {w}x{h} (HD photo requires >= 900px min side).")
                            continue
                    rgb = im.convert("RGB")
                    gray = cv2.cvtColor(np.array(rgb), cv2.COLOR_RGB2GRAY)
                    sharp = float(cv2.Laplacian(gray, cv2.CV_64F).var())
                    if rel_ref.startswith("harvested/") and sharp < 60.0:
                        issues.append(f"BLURRY ASSET BLOCKED: {rel_ref} ({w}x{h}) Laplacian={sharp:.1f} < 60.0 (not HD sharp).")
                    elif sharp < 30.0:
                        warnings.append(f"SOFT/BLURRY ASSET CHECK: {rel_ref} ({w}x{h}) Laplacian={sharp:.1f} < 30.0")
        except Exception as exc:
            warnings.append(f"Asset sharpness gate skipped: {exc}")

    # 7. Choreography Diversity & Anti-Cookie-Cutter Check
    blueprint_file = project_dir / "choreography_blueprint.json"
    if not blueprint_file.exists():
        warnings.append(
            f"CHOREOGRAPHY BLUEPRINT MISSING: {blueprint_file} not found. "
            "New projects should plan per-beat visual metaphors in choreography_blueprint.json before coding."
        )
    img_count = len(re.findall(r"<Img\b", code))
    dynamic_3d_primitives = sum(
        1 for kw in ("ScaleComparison3D", "TimelineTrack3D", "GeoStrategicMap3D", "RealPersonSpotlight3D", "CoinStream", "AnatomyCallout3D", "<svg")
        if kw in code
    )
    if img_count >= 5 and dynamic_3d_primitives < 2:
        issues.append(
            f"COOKIE-CUTTER LAYOUT DETECTED: Found {img_count} <Img> blocks with only {dynamic_3d_primitives} 3D/SVG motion primitive(s). "
            "Every beat must vary physical motion metaphors instead of repeating plain image cards."
        )

    # Luật Tiến Hóa & Độc Bản: so với toàn bộ tập cũ trong novelty_progress_ledger.json
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from novelty_progress_ledger import check as novelty_check
        nv = novelty_check(tsx_path, project_dir)
        issues.extend(nv.get("issues", []))
    except Exception as exc:
        issues.append(f"NOVELTY LEDGER ERROR: không chạy được kiểm tra độc bản ({exc}). Cấm render khi chưa kiểm tra.")

    # Chấm điểm sức giữ chân trước render
    try:
        from retention_density_scorer import score as retention_score
        rt = retention_score(tsx_path, project_dir)
        issues.extend(rt.get("issues", []))
    except Exception as exc:
        issues.append(f"RETENTION SCORER ERROR: ({exc}). Cấm render khi chưa chấm giữ chân.")

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
