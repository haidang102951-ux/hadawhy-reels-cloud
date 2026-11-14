import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";

export type ThumbnailDNAVariant = "ivory_dossier" | "noir_red" | "graphite_gold";

export interface ThumbnailDNAStudy9x16Props {
  variant: ThumbnailDNAVariant;
  brandLogoSrc?: string;
  topTag?: string;
  headlineLine1: string;
  headlineLine2: string;
  mainSubjectSrc: string;
  mysterySilhouetteSrc: string;
  [key: string]: unknown;
}

const VARIANT_THEMES: Record<
  ThumbnailDNAVariant,
  {
    canvasBg: string;
    radialGlow: string;
    gridColor: string;
    tagBg: string;
    tagText: string;
    tagBorder: string;
    line1Color: string;
    line2Color: string;
    lineShadow: string;
    line2Glow: string;
    jensenFilter: string;
    silhouetteRim: string;
    questionColor: string;
    questionGlow: string;
    arrowColor: string;
    bottomFade: string;
    isLightPaper: boolean;
  }
> = {
  ivory_dossier: {
    canvasBg: "#F3F0E8",
    radialGlow:
      "radial-gradient(circle at 54% 48%, rgba(255, 255, 255, 0.85) 0%, rgba(243, 240, 232, 0.55) 55%, rgba(226, 220, 206, 0.92) 100%)",
    gridColor: "rgba(11, 14, 20, 0.065)",
    tagBg: "#D90429",
    tagText: "#FFFFFF",
    tagBorder: "#0B0E14",
    line1Color: "#0B0E14",
    line2Color: "#D90429",
    lineShadow: "0px 4px 0px rgba(11, 14, 20, 0.14)",
    line2Glow: "0px 6px 18px rgba(217, 4, 41, 0.22)",
    jensenFilter:
      "contrast(1.07) saturate(1.06) drop-shadow(0px 18px 28px rgba(11, 14, 20, 0.48))",
    silhouetteRim: "#D90429",
    questionColor: "#D90429",
    questionGlow: "0px 0px 28px rgba(217, 4, 41, 0.72), 0px 10px 24px rgba(0, 0, 0, 0.8)",
    arrowColor: "#D90429",
    bottomFade: "linear-gradient(to bottom, transparent 0%, rgba(11, 14, 20, 0.85) 100%)",
    isLightPaper: true,
  },
  noir_red: {
    canvasBg: "#090B10",
    radialGlow:
      "radial-gradient(circle at 55% 54%, rgba(225, 29, 46, 0.72) 0%, rgba(125, 12, 26, 0.34) 40%, #090B10 78%)",
    gridColor: "rgba(255, 31, 56, 0.08)",
    tagBg: "#E11D2E",
    tagText: "#FFFFFF",
    tagBorder: "#FF6B7A",
    line1Color: "#FFFFFF",
    line2Color: "#FF1F38",
    lineShadow: "0px 8px 0px #040508, 0px 18px 34px rgba(0, 0, 0, 0.96)",
    line2Glow: "0px 0px 32px rgba(255, 31, 56, 0.78)",
    jensenFilter:
      "grayscale(100%) contrast(1.42) brightness(1.04) drop-shadow(0px 0px 10px rgba(255, 31, 56, 0.82)) drop-shadow(0px 24px 36px rgba(0, 0, 0, 0.95))",
    silhouetteRim: "#FF1F38",
    questionColor: "#FF1F38",
    questionGlow: "0px 0px 36px rgba(255, 31, 56, 0.95), 0px 10px 26px rgba(0, 0, 0, 0.95)",
    arrowColor: "#FF4D63",
    bottomFade: "linear-gradient(to bottom, transparent 0%, rgba(9, 11, 16, 0.95) 100%)",
    isLightPaper: false,
  },
  graphite_gold: {
    canvasBg: "#12141A",
    radialGlow:
      "radial-gradient(circle at 54% 52%, rgba(255, 230, 0, 0.34) 0%, rgba(190, 145, 20, 0.16) 44%, #12141A 78%)",
    gridColor: "rgba(255, 230, 0, 0.065)",
    tagBg: "#D90429",
    tagText: "#FFFFFF",
    tagBorder: "#FFE600",
    line1Color: "#FFFFFF",
    line2Color: "#FFE600",
    lineShadow: "0px 8px 0px #07080C, 0px 18px 34px rgba(0, 0, 0, 0.96)",
    line2Glow: "0px 0px 30px rgba(255, 230, 0, 0.62)",
    jensenFilter:
      "contrast(1.08) saturate(1.08) drop-shadow(0px 0px 10px rgba(255, 230, 0, 0.92)) drop-shadow(0px 0px 26px rgba(255, 195, 0, 0.45)) drop-shadow(0px 24px 36px rgba(0, 0, 0, 0.94))",
    silhouetteRim: "#FFE600",
    questionColor: "#FFE600",
    questionGlow: "0px 0px 38px rgba(255, 230, 0, 0.95), 0px 10px 26px rgba(0, 0, 0, 0.95)",
    arrowColor: "#FFE600",
    bottomFade: "linear-gradient(to bottom, transparent 0%, rgba(12, 14, 18, 0.95) 100%)",
    isLightPaper: false,
  },
};

export const ThumbnailDNAStudy9x16: React.FC<ThumbnailDNAStudy9x16Props> = ({
  variant,
  brandLogoSrc = "brand/hadawhy_logo.png",
  topTag = "HỒ SƠ TỐI MẬT",
  headlineLine1,
  headlineLine2,
  mainSubjectSrc,
  mysterySilhouetteSrc,
}) => {
  const t = VARIANT_THEMES[variant];

  return (
    <AbsoluteFill
      style={{
        backgroundColor: t.canvasBg,
        overflow: "hidden",
      }}
    >
      {/* Editorial Investigative Font: Kanit-Black */}
      <style>
        {`
          @font-face {
            font-family: 'KanitBlack';
            src: url('${staticFile("fonts/Kanit-Black.ttf")}') format('truetype');
            font-weight: 900;
          }
          @font-face {
            font-family: 'BeVietnamProBlack';
            src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
            font-weight: 900;
          }
        `}
      </style>

      {/* Studio Radial Backdrop */}
      <AbsoluteFill style={{ background: t.radialGlow }} />

      {/* Editorial Newspaper / Forensic Grid + Geometric Cuts */}
      <svg
        width={1080}
        height={1920}
        style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
      >
        {/* Subtle Architectural Grid */}
        {Array.from({ length: 14 }).map((_, i) => (
          <line
            key={`dna-gx-${i}`}
            x1={i * 80}
            y1={0}
            x2={i * 80}
            y2={1920}
            stroke={t.gridColor}
            strokeWidth={1.5}
          />
        ))}
        {Array.from({ length: 24 }).map((_, i) => (
          <line
            key={`dna-gy-${i}`}
            x1={0}
            y1={i * 80}
            x2={1080}
            y2={i * 80}
            stroke={t.gridColor}
            strokeWidth={1.5}
          />
        ))}

        {/* Variant 1: Bold Red & Obsidian Geometric Editorial Cut Blocks */}
        {variant === "ivory_dossier" && (
          <>
            <polygon points="0,1470 1080,1310 1080,1920 0,1920" fill="#0B0E14" />
            <polygon points="0,1440 1080,1280 1080,1322 0,1482" fill="#D90429" />
            <rect x={54} y={270} width={972} height={4} fill="#0B0E14" opacity={0.18} />
          </>
        )}

        {/* Variant 2: High-Tension Noir Red Slash Bands */}
        {variant === "noir_red" && (
          <>
            <polygon
              points="0,1520 1080,1360 1080,1920 0,1920"
              fill="rgba(18, 4, 8, 0.85)"
            />
            <polygon
              points="0,1512 1080,1352 1080,1364 0,1524"
              fill="#E11D2E"
              opacity={0.9}
            />
          </>
        )}

        {/* Variant 3: Luxury Gold Stage Diagonal Beam */}
        {variant === "graphite_gold" && (
          <>
            <polygon
              points="180,0 760,0 1080,1280 420,1280"
              fill="rgba(255, 230, 0, 0.045)"
            />
            <polygon points="0,1520 1080,1380 1080,1920 0,1920" fill="#0B0D12" />
            <polygon
              points="0,1514 1080,1374 1080,1384 0,1524"
              fill="#FFE600"
              opacity={0.92}
            />
          </>
        )}
      </svg>

      {/* Variant 1 subtle archival paper dot texture */}
      {t.isLightPaper && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundImage:
              "radial-gradient(rgba(11,14,20,0.06) 1px, transparent 1px)",
            backgroundSize: "18px 18px",
            opacity: 0.45,
            pointerEvents: "none",
          }}
        />
      )}

      {/* ===================================================================
          1. TOP-LEFT CHANNEL BADGE (X: 60, Y: 140)
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: 60,
          top: 140,
          width: 280,
          filter: "drop-shadow(0 8px 18px rgba(0,0,0,0.45))",
        }}
      >
        <Img
          src={staticFile(brandLogoSrc)}
          style={{ width: "100%", height: "auto", display: "block" }}
        />
      </div>

      {/* ===================================================================
          2. EDITORIAL INVESTIGATIVE HEADLINE BLOCK (Y: 306..595, 88-92% WIDTH)
         =================================================================== */}
      {/* Top Tag: HỒ SƠ TỐI MẬT */}
      <div
        style={{
          position: "absolute",
          left: 62,
          top: 306,
          padding: "5px 22px",
          borderRadius: 6,
          background: t.tagBg,
          border: `2.5px solid ${t.tagBorder}`,
          boxShadow: "0 8px 20px rgba(0,0,0,0.28)",
        }}
      >
        <span
          style={{
            fontFamily: "KanitBlack, sans-serif",
            fontSize: 28,
            color: t.tagText,
            letterSpacing: "0.08em",
            lineHeight: 1.1,
            display: "block",
          }}
        >
          {topTag}
        </span>
      </div>

      {/* Line 1 & Line 2: Stretched across 88-92% width (~960px), Zero Wrap */}
      <div
        style={{
          position: "absolute",
          left: 540,
          top: 486,
          width: 970,
          transform: "translate(-50%, -50%)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          gap: 2,
        }}
      >
        <div
          style={{
            width: "100%",
            fontFamily: "KanitBlack, sans-serif",
            fontSize: 89,
            fontWeight: 900,
            lineHeight: 1.02,
            letterSpacing: "-0.015em",
            color: t.line1Color,
            textShadow: t.lineShadow,
            whiteSpace: "nowrap",
          }}
        >
          {headlineLine1}
        </div>
        <div
          style={{
            width: "100%",
            fontFamily: "KanitBlack, sans-serif",
            fontSize: 85,
            fontWeight: 900,
            lineHeight: 1.04,
            letterSpacing: "-0.015em",
            color: t.line2Color,
            textShadow: `${t.lineShadow}, ${t.line2Glow}`,
            whiteSpace: "nowrap",
          }}
        >
          {headlineLine2}
        </div>
      </div>

      {/* ===================================================================
          3. MYSTERY SILHOUETTE ON THE RIGHT + GIANT "?" HOOK
         =================================================================== */}
      {/* Stephen Neal converted into Dark Mystery Silhouette */}
      <div
        style={{
          position: "absolute",
          left: 805,
          top: 1125,
          width: 585,
          transform: "translate(-50%, -50%)",
          maskImage: "linear-gradient(to bottom, black 75%, transparent 99%)",
          WebkitMaskImage: "linear-gradient(to bottom, black 75%, transparent 99%)",
        }}
      >
        <Img
          src={staticFile(mysterySilhouetteSrc)}
          style={{
            width: "100%",
            height: "auto",
            display: "block",
            filter: `brightness(0) drop-shadow(0px 0px 4px ${t.silhouetteRim}) drop-shadow(0px 0px 20px ${t.silhouetteRim})`,
            opacity: variant === "ivory_dossier" ? 0.92 : 0.96,
          }}
        />
      </div>

      {/* Subtle Investigative Dashed Arrow pointing toward "?" Silhouette */}
      <svg
        width={1080}
        height={1920}
        style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
      >
        <defs>
          <marker
            id={`arrow-${variant}`}
            viewBox="0 0 10 10"
            refX="6"
            refY="5"
            markerWidth="6"
            markerHeight="6"
            orient="auto-start-reverse"
          >
            <path d="M 0 1 L 9 5 L 0 9 z" fill={t.arrowColor} />
          </marker>
        </defs>
        <path
          d="M 555 695 Q 660 660 725 745"
          fill="none"
          stroke={t.arrowColor}
          strokeWidth={7}
          strokeDasharray="16 12"
          strokeLinecap="round"
          markerEnd={`url(#arrow-${variant})`}
          style={{
            filter: `drop-shadow(0 4px 10px rgba(0,0,0,0.45))`,
          }}
        />
      </svg>

      {/* Giant Glowing Question Mark centered over Mystery Silhouette */}
      <div
        style={{
          position: "absolute",
          left: 808,
          top: 905,
          transform: "translate(-50%, -50%) rotate(4deg)",
          fontFamily: "KanitBlack, sans-serif",
          fontSize: 330,
          fontWeight: 900,
          lineHeight: 0.9,
          color: t.questionColor,
          textShadow: t.questionGlow,
          WebkitTextStroke: variant === "ivory_dossier" ? "5px #FFFFFF" : "6px #06080E",
          paintOrder: "stroke fill",
          pointerEvents: "none",
        }}
      >
        ?
      </div>

      {/* ===================================================================
          4. GIANT POWERFUL FOREGROUND JENSEN HUANG (width 755px, Y: 600..1585+)
         =================================================================== */}
      <div
        style={{
          position: "absolute",
          left: 350,
          top: 1110,
          width: 755,
          transform: "translate(-50%, -50%)",
          maskImage: "linear-gradient(to bottom, black 76%, transparent 99%)",
          WebkitMaskImage: "linear-gradient(to bottom, black 76%, transparent 99%)",
        }}
      >
        <Img
          src={staticFile(mainSubjectSrc)}
          style={{
            width: "100%",
            height: "auto",
            display: "block",
            filter: t.jensenFilter,
          }}
        />
      </div>

      {/* Sleek Bottom Grounding Gradient (prevents harsh cut at bottom edge of torso) */}
      <div
        style={{
          position: "absolute",
          left: 0,
          right: 0,
          bottom: 0,
          height: 360,
          background: t.bottomFade,
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
