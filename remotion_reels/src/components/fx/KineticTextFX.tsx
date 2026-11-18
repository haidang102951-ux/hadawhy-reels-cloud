import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const MarkerHighlightText: React.FC<{
  text: string;
  startFrame?: number;
  highlightColor?: string;
  textColor?: string;
  fontSize?: number;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  highlightColor = "#FACC15",
  textColor = "#0B0F19",
  fontSize = 54,
  fontFamily = "'BeVietnamProBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const sweepPct = interpolate(rel, [0, 14], [0, 100], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <span
      style={{
        position: "relative",
        display: "inline-block",
        padding: "4px 14px",
        fontSize,
        fontFamily,
        fontWeight: 900,
        color: sweepPct > 45 ? textColor : "#FFFFFF",
        letterSpacing: "-0.02em",
      }}
    >
      <span
        style={{
          position: "absolute",
          inset: 0,
          backgroundColor: highlightColor,
          transformOrigin: "left center",
          transform: `scaleX(${sweepPct / 100})`,
          borderRadius: 6,
          zIndex: 0,
        }}
      />
      <span style={{ position: "relative", zIndex: 1 }}>{text}</span>
    </span>
  );
};

export const StaggerWaveText: React.FC<{
  text: string;
  startFrame?: number;
  staggerFrames?: number;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  staggerFrames = 3,
  fontSize = 52,
  color = "#FFFFFF",
  fontFamily = "'BeVietnamProBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = text.split(" ");

  return (
    <div
      style={{
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
        gap: "10px 14px",
        fontSize,
        fontFamily,
        fontWeight: 900,
        color,
      }}
    >
      {words.map((word, idx) => {
        const rel = Math.max(0, frame - (startFrame + idx * staggerFrames));
        const p = spring({
          frame: rel,
          fps,
          config: { damping: 14, stiffness: 240, mass: 0.55 },
        });
        const y = interpolate(p, [0, 1], [34, 0]);
        const op = interpolate(rel, [0, 4], [0, 1], { extrapolateRight: "clamp" });
        return (
          <span
            key={idx}
            style={{
              display: "inline-block",
              opacity: op,
              transform: `translateY(${y}px) scale(${interpolate(p, [0, 1], [0.85, 1])})`,
              WebkitTextStroke: "2px rgba(0,0,0,0.85)",
              textShadow: "0 6px 18px rgba(0,0,0,0.9)",
            }}
          >
            {word}
          </span>
        );
      })}
    </div>
  );
};

export const GlitchSplitText: React.FC<{
  text: string;
  startFrame?: number;
  fontSize?: number;
  color?: string;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  fontSize = 58,
  color = "#FFFFFF",
  fontFamily = "'BeVietnamProBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const glitchAmp = rel < 14 ? interpolate(rel, [0, 14], [10, 0]) : 0;
  const offset = Math.sin(rel * 2.7) * glitchAmp;

  return (
    <div style={{ position: "relative", display: "inline-block", fontSize, fontFamily, fontWeight: 900 }}>
      {glitchAmp > 0.3 && (
        <>
          <span
            style={{
              position: "absolute",
              left: offset,
              top: 0,
              color: "#EF4444",
              opacity: 0.75,
              pointerEvents: "none",
            }}
          >
            {text}
          </span>
          <span
            style={{
              position: "absolute",
              left: -offset,
              top: 0,
              color: "#38BDF8",
              opacity: 0.75,
              pointerEvents: "none",
            }}
          >
            {text}
          </span>
        </>
      )}
      <span
        style={{
          position: "relative",
          color,
          WebkitTextStroke: "2px rgba(0,0,0,0.9)",
          textShadow: "0 6px 20px rgba(0,0,0,0.9)",
        }}
      >
        {text}
      </span>
    </div>
  );
};

export const MetallicSweepText: React.FC<{
  text: string;
  startFrame?: number;
  fontSize?: number;
  fontFamily?: string;
}> = ({
  text,
  startFrame = 0,
  fontSize = 62,
  fontFamily = "'KanitBlack', sans-serif",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const pos = interpolate(rel % 90, [0, 45, 90], [-40, 140, 140]);

  return (
    <div
      style={{
        fontSize,
        fontFamily,
        fontWeight: 900,
        backgroundImage: `linear-gradient(110deg, #F59E0B 0%, #FDE68A ${pos}%, #FFFBEB ${pos + 8}%, #F59E0B ${pos + 18}%, #D97706 100%)`,
        WebkitBackgroundClip: "text",
        color: "transparent",
        filter: "drop-shadow(0 6px 18px rgba(0,0,0,0.9))",
      }}
    >
      {text}
    </div>
  );
};

export const OdometerCounter: React.FC<{
  from?: number;
  to: number;
  startFrame?: number;
  durationFrames?: number;
  prefix?: string;
  suffix?: string;
  fontSize?: number;
  color?: string;
}> = ({
  from = 0,
  to,
  startFrame = 0,
  durationFrames = 36,
  prefix = "",
  suffix = "",
  fontSize = 84,
  color = "#42B2F2",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const t = interpolate(rel, [0, durationFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const eased = 1 - Math.pow(1 - t, 3);
  const val = Math.round(from + (to - from) * eased);

  return (
    <span
      style={{
        fontSize,
        fontFamily: "'KanitBlack', monospace",
        fontWeight: 900,
        color,
        fontVariantNumeric: "tabular-nums",
        WebkitTextStroke: "2px rgba(0,0,0,0.88)",
        textShadow: "0 8px 24px rgba(0,0,0,0.92)",
      }}
    >
      {prefix}
      {val.toLocaleString("vi-VN")}
      {suffix}
    </span>
  );
};
