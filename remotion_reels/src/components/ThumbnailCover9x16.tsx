import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

export interface ThumbnailCover9x16Props {
  /** Real event context backdrop photo in public/ (e.g. "harvested/nvidia_context_backdrop.png") */
  backgroundPhotoSrc?: string;
  /** Backdrop Gaussian blur px (default 1.2 for crisp identifiable real backdrop) */
  backgroundBlurPx?: number;
  /** Backdrop zoom scale (default 1.04) */
  backgroundScale?: number;
  /** Backdrop focal position / transform origin (default "50% 50%") */
  backgroundObjectPosition?: string;
  /** Backdrop brightness multiplier (default 0.72) */
  backgroundBrightness?: number;
  /** Backdrop contrast multiplier (default 1.15) */
  backgroundContrast?: number;
  /** Backdrop saturation multiplier (default 1.0) */
  backgroundSaturate?: number;
  /** Main foreground hero subject cutout PNG in public/ (rendered B&W High-Contrast by default) */
  heroSubjectSrc: string;
  /** Mystery secondary cutout PNG in public/ (rendered as dark rim-lit silhouette + "?") */
  mysteryOrSecondarySrc?: string;
  /** Headline Line 1 (HaDa Bright Blue #22B8FF by default) */
  headlineLine1: string;
  /** Headline Line 2 (WHY Pure White #FFFFFF by default) */
  headlineLine2: string;
  /** Official channel logo PNG in public/ (strictly "brand/hadawhy_logo.png") */
  brandLogoSrc?: string;
  /** Glow accent color behind subjects & on "?" hook (default "#E11D2E" Noir Crimson) */
  glowAccentColor?: string;
  /** Line 1 text color (default "#42B2F2" HaDa Sky Blue) */
  headlineLine1Color?: string;
  /** Line 2 text color (default "#FFFFFF" WHY White) */
  headlineLine2Color?: string;
  /** Apply Noir high-contrast B&W filter to hero subject */
  heroBwHighContrast?: boolean;
  /** Render secondary subject as mysterious dark silhouette + giant "?" */
  mysterySilhouetteMode?: boolean;
  /** Optional custom symbol on mystery silhouette (default "?") */
  mysterySymbol?: string;
  /**
   * Dynamic Story Layout Mode (Tư duy linh hoạt theo đúng bản chất kịch bản):
   * - "mystery_silhouette": Chủ thể chính + Bóng đen bí ẩn kèm dấu "?" đỏ (Mặc định khi có ẩn số nhân vật).
   * - "dual_confrontation": 2 Nhân vật / 2 Đế chế đối đầu trực diện (Cả 2 lộ diện rõ nét + mũi tên xung đột).
   * - "forensic_object": Giải phẫu Vật thể / Sự cố / Bằng chứng khổng lồ kèm vòng tròn đỏ khoanh vùng tử huyệt.
   * - "titan_evidence": Nhân vật trung tâm B&W + Vật chứng / Hồ sơ mật nổi 3D bên cạnh kèm vòng khoanh đỏ.
   */
  layoutMode?: "mystery_silhouette" | "dual_confrontation" | "forensic_object" | "titan_evidence";
  /** Optional red forensic circle coordinates for "forensic_object" or "titan_evidence" mode */
  forensicCircle?: { cx: number; cy: number; r: number };
  /** Optional overrides for foreground hero subject positioning & sizing */
  heroWidth?: number;
  heroLeft?: number;
  heroBottom?: number;
  /** Optional overrides for secondary evidence card in "titan_evidence" mode */
  secondaryWidth?: number;
  secondaryTop?: number;
  secondaryLeft?: number;
  /** Optional custom SVG path for the red dashed investigative arrow */
  arrowPath?: string;
  /** Optional smooth top-down linear scrim opacity (0 to 1, Zero-Blob) for headline legibility */
  topScrimOpacity?: number;
  /** Index signature required for Remotion Still compatibility */
  [key: string]: unknown;
}

function fitEditorialSize(text: string, baseSize: number, minSize: number): number {
  const len = text.trim().length;
  if (len <= 18) return baseSize;
  return Math.max(minSize, Math.round(baseSize * (18.2 / len)));
}

export const ThumbnailCover9x16: React.FC<ThumbnailCover9x16Props> = ({
  backgroundPhotoSrc = "",
  backgroundBlurPx = 3.5,
  backgroundScale = 1.04,
  backgroundObjectPosition = "50% 50%",
  backgroundBrightness = 0.65,
  backgroundContrast = 1.15,
  backgroundSaturate = 0.96,
  heroSubjectSrc,
  mysteryOrSecondarySrc,
  headlineLine1,
  headlineLine2,
  brandLogoSrc = "brand/hadawhy_logo.png",
  glowAccentColor = "#E11D2E",
  headlineLine1Color = "#22B8FF",
  headlineLine2Color = "#FFFFFF",
  heroBwHighContrast = false,
  mysterySilhouetteMode = true,
  mysterySymbol = "?",
  layoutMode = "titan_evidence",
  forensicCircle,
  heroWidth,
  heroLeft,
  heroBottom = 0,
  secondaryWidth = 425,
  secondaryTop = 815,
  secondaryLeft = 825,
  arrowPath = "M 555 620 Q 670 575 740 665",
  topScrimOpacity = 0.45,
}) => {
  const isSilhouette = layoutMode === "mystery_silhouette" ? mysterySilhouetteMode : false;
  const line1Size = fitEditorialSize(headlineLine1, 86, 54);
  const line2Size = fitEditorialSize(headlineLine2, 84, 52);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#06101E",
        overflow: "hidden",
      }}
    >
      {/* Khóa 100% font tiếng Việt đầy đủ dấu BeVietnamPro-Black */}
      <style>
        {`
          @font-face {
            font-family: 'BeVietnamProBlack';
            src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
            font-weight: 900;
          }
          @font-face {
            font-family: 'KanitBlack';
            src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
            font-weight: 900;
          }
        `}
      </style>

      {/* ===================================================================
          1. FULL 1080x1920 REAL CONTEXT BACKDROP (SCALED & BLURRED EVENLY)
         =================================================================== */}
      {backgroundPhotoSrc && (
        <Img
          src={staticFile(backgroundPhotoSrc)}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            objectPosition: backgroundObjectPosition,
            transform: `scale(${backgroundScale})`,
            transformOrigin: backgroundObjectPosition,
            filter: backgroundBlurPx > 0
              ? `blur(${backgroundBlurPx}px) brightness(${backgroundBrightness}) contrast(${backgroundContrast}) saturate(${backgroundSaturate})`
              : `brightness(${backgroundBrightness}) contrast(${backgroundContrast}) saturate(${backgroundSaturate})`,
          }}
        />
      )}

      {/* Smooth Zero-Blob Top Scrim for Headline Legibility */}
      {topScrimOpacity > 0 && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: `linear-gradient(180deg, rgba(5, 7, 12, ${topScrimOpacity}) 0%, rgba(5, 7, 12, ${topScrimOpacity * 0.55}) 26%, rgba(5, 7, 12, 0) 48%)`,
            pointerEvents: "none",
          }}
        />
      )}



      {/* ===================================================================
          2. CHANNEL LOGO AT SAFE TOP-LEFT (brand/hadawhy_logo.png)
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: 52,
          top: 64,
          width: 225,
          filter: "drop-shadow(0 6px 16px rgba(0, 0, 0, 0.9))",
        }}
      >
        <Img
          src={staticFile(brandLogoSrc)}
          style={{ width: "100%", height: "auto", display: "block" }}
        />
      </div>

      {/* ===================================================================
          3. DUY NHẤT 2 DÒNG TIÊU ĐỀ CHÍNH (#22B8FF + #FFFFFF) — CẤM TAG ĐỎ THỨ 3
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: 540,
          top: 385,
          width: 970,
          transform: "translate3d(-50%, -50%, 0)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          gap: 8,
        }}
      >
        <div
          style={{
            width: "100%",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: line1Size,
            fontWeight: 900,
            lineHeight: 1.08,
            letterSpacing: "-0.015em",
            color: headlineLine1Color,
            WebkitTextStroke: "11px #05070C",
            paintOrder: "stroke fill",
            textShadow: `0px 8px 0px #05070C, 0px 16px 32px rgba(0,0,0,0.95)`,
            textTransform: "uppercase",
            whiteSpace: "nowrap",
          }}
        >
          {headlineLine1}
        </div>
        <div
          style={{
            width: "100%",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: line2Size,
            fontWeight: 900,
            lineHeight: 1.08,
            letterSpacing: "-0.015em",
            color: headlineLine2Color,
            WebkitTextStroke: "11px #05070C",
            paintOrder: "stroke fill",
            textShadow: `0px 8px 0px #05070C, 0px 16px 32px rgba(0,0,0,0.95)`,
            textTransform: "uppercase",
            whiteSpace: "nowrap",
          }}
        >
          {headlineLine2}
        </div>
      </div>

      {/* ===================================================================
          4. MYSTERY SILHOUETTE RIGHT + GLOWING "?" (ANCHORED TO BOTTOM 1920)
         =================================================================== */}
      {mysteryOrSecondarySrc && (
        <>
          <div
            style={
              layoutMode === "titan_evidence"
                ? {
                    position: "absolute",
                    left: secondaryLeft,
                    top: secondaryTop,
                    width: secondaryWidth,
                    transform: "translateX(-50%) rotate(3deg)",
                    zIndex: 5,
                  }
                : {
                    position: "absolute",
                    left: 815,
                    bottom: 0,
                    width: 850,
                    transform: "translateX(-50%)",
                  }
            }
          >
            <Img
              src={staticFile(mysteryOrSecondarySrc)}
              style={{
                width: "100%",
                height: "auto",
                display: "block",
                borderRadius: layoutMode === "titan_evidence" ? 12 : 0,
                border:
                  layoutMode === "titan_evidence"
                    ? "3px solid rgba(255, 255, 255, 0.25)"
                    : "none",
                filter: isSilhouette
                  ? `brightness(0) drop-shadow(0px 8px 16px rgba(0,0,0,0.85)) drop-shadow(0px 8px 16px rgba(0,0,0,0.85))`
                  : `drop-shadow(0px 22px 34px rgba(0,0,0,0.9))`,
              }}
            />
          </div>

          {/* Red Dashed Investigative Arrow pointing toward Secondary Subject / Evidence */}
          <svg
            width={1080}
            height={1920}
            style={{ position: "absolute", inset: 0, pointerEvents: "none", zIndex: 8 }}
          >
            <defs>
              <marker
                id="cov-mystery-arrow"
                viewBox="0 0 10 10"
                refX="6"
                refY="5"
                markerWidth="6"
                markerHeight="6"
                orient="auto-start-reverse"
              >
                <path d="M 0 1 L 9 5 L 0 9 z" fill={glowAccentColor} />
              </marker>
            </defs>
            <path
              d={arrowPath}
              fill="none"
              stroke={glowAccentColor}
              strokeWidth={7}
              strokeDasharray="16 12"
              strokeLinecap="round"
              markerEnd="url(#cov-mystery-arrow)"
              style={{ filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.8))" }}
            />
            {forensicCircle && (
              <circle
                cx={forensicCircle.cx}
                cy={forensicCircle.cy}
                r={forensicCircle.r}
                fill="none"
                stroke={glowAccentColor}
                strokeWidth={8}
                strokeDasharray="22 12"
                style={{ filter: "drop-shadow(0 6px 14px rgba(0,0,0,0.85))" }}
              />
            )}
          </svg>

          {/* Giant Glowing Crimson "?" over Silhouette (Safe inside 4:5) */}
          {isSilhouette && (
            <div
              style={{
                position: "absolute",
                left: 815,
                top: 865,
                transform: "translate(-50%, -50%) rotate(4deg)",
                fontFamily: "KanitBlack, sans-serif",
                fontSize: 345,
                fontWeight: 900,
                lineHeight: 0.9,
                color: glowAccentColor,
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: `0 8px 18px rgba(0,0,0,0.85), 0px 12px 28px rgba(0,0,0,0.95)`,
                pointerEvents: "none",
              }}
            >
              {mysterySymbol}
            </div>
          )}
        </>
      )}

      {/* ===================================================================
          5. GIANT FOREGROUND HERO SUBJECT (ANCHORED FULL TO BOTTOM: 0)
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: heroLeft ?? (layoutMode === "forensic_object" && !mysteryOrSecondarySrc ? 540 : 345),
          bottom: heroBottom,
          width: heroWidth ?? (layoutMode === "forensic_object" && !mysteryOrSecondarySrc ? 1020 : 990),
          transform: "translateX(-50%)",
          zIndex: 6,
        }}
      >
        <Img
          src={staticFile(heroSubjectSrc)}
          style={{
            width: "100%",
            height: "auto",
            display: "block",
            filter: heroBwHighContrast
              ? `grayscale(100%) contrast(1.38) brightness(1.06) drop-shadow(0px 24px 38px rgba(0,0,0,0.95))`
              : `drop-shadow(0px 24px 38px rgba(0,0,0,0.95))`,
          }}
        />
      </div>
    </AbsoluteFill>
  );
};
