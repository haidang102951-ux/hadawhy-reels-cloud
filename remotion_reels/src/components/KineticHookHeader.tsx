import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface HookBeatSpec {
  start: number;
  eyebrow: string;
  hero: string;
  accent: string;
  heroSize?: number;
}

interface KineticHookHeaderProps {
  beat: HookBeatSpec;
  top?: number;
}

export const HaDaWhyFontFaces: React.FC = () => (
  <style>{`
    @font-face {
      font-family: 'BeVietnamProBlack';
      src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
      font-weight: 900;
      font-style: normal;
    }
    @font-face {
      font-family: 'BeVietnamProExtraBold';
      src: url('${staticFile("fonts/BeVietnamPro-ExtraBold.ttf")}') format('truetype');
      font-weight: 800;
      font-style: normal;
    }
    @font-face {
      font-family: 'KanitBlack';
      src: url('${staticFile("fonts/Kanit-Black.ttf")}') format('truetype');
      font-weight: 900;
      font-style: normal;
    }
  `}</style>
);

export const KineticHookHeader: React.FC<KineticHookHeaderProps> = ({
  beat,
  top = 310,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const hookSpring = spring({
    frame: Math.max(0, frame - beat.start),
    fps,
    config: { damping: 12, stiffness: 210, mass: 0.75 },
  });
  const hookScale = interpolate(hookSpring, [0, 1], [1.38, 1.0]);
  const hookOpacity = interpolate(hookSpring, [0, 0.35], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        left: 540,
        top,
        width: 980,
        transform: `translate(-50%, -50%) scale(${hookScale})`,
        opacity: hookOpacity,
        textAlign: "center",
        pointerEvents: "none",
        zIndex: 35,
      }}
    >
      <div
        style={{
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 42,
          lineHeight: 1.12,
          letterSpacing: "0.03em",
          color: "#FFFFFF",
          WebkitTextStroke: "8px #05070C",
          paintOrder: "stroke fill",
          textShadow: "0 8px 22px rgba(0,0,0,0.95)",
          marginBottom: 8,
          textTransform: "uppercase",
          whiteSpace: "nowrap",
        }}
      >
        {beat.eyebrow}
      </div>
      <div
        style={{
          fontFamily: "KanitBlack, sans-serif",
          fontSize: beat.heroSize ?? 76,
          lineHeight: 1.04,
          color: beat.accent,
          WebkitTextStroke: "11px #05070C",
          paintOrder: "stroke fill",
          textShadow: `0 0 36px ${beat.accent}AA, 0 10px 28px rgba(0,0,0,0.96)`,
          textTransform: "uppercase",
          whiteSpace: "nowrap",
        }}
      >
        {beat.hero}
      </div>
    </div>
  );
};
