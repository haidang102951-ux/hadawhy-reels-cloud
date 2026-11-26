import React from "react";
import { interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface HookBeatSpec {
  start: number;
  eyebrow: string;
  hero: string;
  accent?: string;
  heroColor?: string;
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
      src: url('${staticFile("fonts/BeVietnamPro-Black.ttf")}') format('truetype');
      font-weight: 900;
      font-style: normal;
    }
  `}</style>
);

export const KineticHookHeader: React.FC<KineticHookHeaderProps> = ({
  beat,
  top = 290,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const hookSpring = spring({
    frame: Math.max(0, frame - beat.start),
    fps,
    config: { damping: 22, stiffness: 280, mass: 0.8 },
  });
  const hookScale = interpolate(hookSpring, [0, 1], [1.22, 1.0]);
  const hookOpacity = interpolate(hookSpring, [0, 0.3], [0, 1], {
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
        transform: `translate3d(-50%, -50%, 0) scale(${hookScale})`,
        willChange: "transform",
        opacity: hookOpacity,
        textAlign: "center",
        pointerEvents: "none",
        zIndex: 35,
      }}
    >
      <div
        style={{
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 36,
          lineHeight: 1.15,
          letterSpacing: "0.03em",
          color: beat.accent?.startsWith("#") ? beat.accent : "#A0ECFF",
          WebkitTextStroke: "6px #05070C",
          paintOrder: "stroke fill",
          textShadow: "0 8px 22px rgba(0,0,0,0.95)",
          marginBottom: 6,
          textTransform: "uppercase",
          whiteSpace: "nowrap",
        }}
      >
        {beat.eyebrow}
      </div>
      <div
        style={{
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: beat.heroSize ?? 72,
          lineHeight: 1.06,
          color: beat.heroColor ?? "#FFE600",
          WebkitTextStroke: "10px #05070C",
          paintOrder: "stroke fill",
          textShadow: "0 10px 26px rgba(0,0,0,0.95)",
          textTransform: "uppercase",
          whiteSpace: "nowrap",
        }}
      >
        {beat.hero}
      </div>
    </div>
  );
};
