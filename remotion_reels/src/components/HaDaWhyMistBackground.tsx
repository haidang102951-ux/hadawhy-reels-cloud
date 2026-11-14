import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

export interface HaDaWhyMistBackgroundProps {
  /**
   * Default 0.11 (Level 1 — subtle #42B2F2 blue mist over deep obsidian).
   * Keeps background strictly supportive so foreground 3D subjects & text pop.
   */
  intensity?: number;
  /** Primary brand mist color (HaDa Why blue). */
  accentHex?: string;
}

/**
 * Brand-signature animated background for HaDa Why (@hadawhy) 9:16 videos.
 * Renders a deep obsidian stage with slow-drifting #42B2F2 blue mist plumes
 * and soft vignette framing for maximum text & 3D subject contrast.
 */
export const HaDaWhyMistBackground: React.FC<HaDaWhyMistBackgroundProps> = ({
  intensity = 0.11,
  accentHex = "66, 178, 242",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;

  // Slow organic drift across 60fps timeline
  const driftX1 = Math.sin(t * 0.22) * 5.5;
  const driftY1 = Math.cos(t * 0.18) * 3.5;
  const driftX2 = Math.cos(t * 0.19) * 6.5;
  const driftY2 = Math.sin(t * 0.15) * 4.0;
  const waveShift = Math.sin(t * 0.35) * 18;

  const alphaMain = Math.min(0.25, Math.max(0.04, intensity));
  const alphaSecondary = alphaMain * 0.72;
  const alphaWisp = alphaMain * 0.28;

  return (
    <AbsoluteFill
      style={{
        background:
          "radial-gradient(ellipse at 50% 44%, #091320 0%, #050911 55%, #030509 100%)",
        overflow: "hidden",
      }}
    >
      {/* Plume 1: Upper-left HaDa Why blue mist */}
      <div
        style={{
          position: "absolute",
          inset: "-15%",
          background: `radial-gradient(circle at ${35 + driftX1}% ${38 + driftY1}%, rgba(${accentHex}, ${alphaMain}) 0%, rgba(${accentHex}, ${alphaMain * 0.32}) 32%, transparent 64%)`,
          filter: "blur(36px)",
          pointerEvents: "none",
        }}
      />

      {/* Plume 2: Lower-right deep navy-cyan mist */}
      <div
        style={{
          position: "absolute",
          inset: "-15%",
          background: `radial-gradient(circle at ${68 + driftX2}% ${52 + driftY2}%, rgba(30, 111, 168, ${alphaSecondary}) 0%, rgba(30, 111, 168, ${alphaSecondary * 0.3}) 34%, transparent 66%)`,
          filter: "blur(42px)",
          pointerEvents: "none",
        }}
      />

      {/* Soft flowing mist wisps (SVG, subtle horizontal drift) */}
      <svg
        viewBox="0 0 1080 1920"
        preserveAspectRatio="none"
        style={{
          position: "absolute",
          inset: 0,
          width: "100%",
          height: "100%",
          opacity: 0.9,
          pointerEvents: "none",
        }}
      >
        <defs>
          <filter id="hadawhyMistBlur" x="-10%" y="-10%" width="120%" height="120%">
            <feGaussianBlur stdDeviation="18" />
          </filter>
        </defs>
        <g filter="url(#hadawhyMistBlur)">
          {[0, 1, 2, 3, 4, 5].map((i) => {
            const y0 = 560 + i * 165;
            const dy = waveShift * (i % 2 === 0 ? 1 : -0.8);
            const d = `M -80 ${y0 + dy} Q 320 ${y0 - 75 - dy} 600 ${y0 + 35 + dy} T 1180 ${y0 - 20 - dy}`;
            return (
              <path
                key={i}
                d={d}
                fill="none"
                stroke={`rgba(${accentHex}, ${alphaWisp})`}
                strokeWidth={54 + i * 6}
                strokeLinecap="round"
              />
            );
          })}
        </g>
      </svg>

      {/* Outer vignette: preserves deep contrast behind top Hook and bottom Captions */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(ellipse at 50% 46%, rgba(0,0,0,0) 32%, rgba(3,5,10,0.48) 72%, rgba(2,4,8,0.90) 100%)",
          pointerEvents: "none",
        }}
      />
    </AbsoluteFill>
  );
};
