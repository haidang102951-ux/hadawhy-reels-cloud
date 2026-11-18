import React from "react";
import { Img, interpolate, staticFile, useCurrentFrame } from "remotion";

export const ParallaxDepthStage: React.FC<{
  bgSrc: string;
  subjectSrc?: string;
  startFrame?: number;
  durationFrames?: number;
  bgBlur?: number;
}> = ({ bgSrc, subjectSrc, startFrame = 0, durationFrames = 240, bgBlur = 5 }) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const bgScale = interpolate(rel, [0, durationFrames], [1.06, 1.18], { extrapolateRight: "clamp" });
  const bgX = interpolate(rel, [0, durationFrames], [-18, 18], { extrapolateRight: "clamp" });
  const subScale = interpolate(rel, [0, durationFrames], [0.96, 1.07], { extrapolateRight: "clamp" });
  const subX = interpolate(rel, [0, durationFrames], [24, -24], { extrapolateRight: "clamp" });
  const floatY = Math.sin(rel * 0.045) * 9;

  return (
    <div style={{ position: "relative", width: "100%", height: "100%", overflow: "hidden" }}>
      <Img
        src={staticFile(bgSrc)}
        style={{
          position: "absolute",
          inset: -30,
          width: "calc(100% + 60px)",
          height: "calc(100% + 60px)",
          objectFit: "cover",
          transform: `translate3d(${bgX}px, 0, 0) scale(${bgScale})`,
          filter: `blur(${bgBlur}px) brightness(0.62)`,
        }}
      />
      {subjectSrc && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            transform: `translate3d(${subX}px, ${floatY}px, 0) scale(${subScale})`,
          }}
        >
          <Img
            src={staticFile(subjectSrc)}
            style={{
              maxWidth: "82%",
              maxHeight: "54%",
              objectFit: "contain",
              filter: "drop-shadow(0 28px 42px rgba(0,0,0,0.85))",
            }}
          />
        </div>
      )}
    </div>
  );
};

export const DotMatrixZoom: React.FC<{
  totalDots?: number;
  highlightCount?: number;
  startFrame?: number;
  durationFrames?: number;
  highlightColor?: string;
  label?: string;
}> = ({
  totalDots = 400,
  highlightCount = 1,
  startFrame = 0,
  durationFrames = 150,
  highlightColor = "#EF4444",
  label = "1 / 1.000.000",
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const zoom = interpolate(rel, [0, durationFrames * 0.75], [3.6, 1.0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cols = 20;
  const rows = Math.ceil(totalDots / cols);
  const centerIdx = Math.floor(rows / 2) * cols + Math.floor(cols / 2);

  return (
    <div style={{ width: "100%", height: "100%", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: `repeat(${cols}, 26px)`,
          gap: 10,
          transform: `scale(${zoom})`,
          transformOrigin: "center center",
        }}
      >
        {Array.from({ length: totalDots }).map((_, idx) => {
          const isTarget = idx >= centerIdx && idx < centerIdx + highlightCount;
          const pulse = isTarget ? 1 + Math.sin(rel * 0.2) * 0.25 : 1;
          return (
            <div
              key={idx}
              style={{
                width: 18,
                height: 18,
                borderRadius: "50%",
                backgroundColor: isTarget ? highlightColor : "rgba(226, 232, 240, 0.26)",
                boxShadow: isTarget ? `0 0 22px ${highlightColor}` : undefined,
                transform: `scale(${pulse})`,
              }}
            />
          );
        })}
      </div>
      <div
        style={{
          marginTop: 34,
          fontSize: 44,
          fontFamily: "'KanitBlack', monospace",
          fontWeight: 900,
          color: highlightColor,
          textShadow: "0 6px 18px rgba(0,0,0,0.9)",
        }}
      >
        {label}
      </div>
    </div>
  );
};

export interface FlowBranch {
  label: string;
  percent: number;
  color: string;
}

export const FlowPipeline3D: React.FC<{
  sourceLabel: string;
  branches: FlowBranch[];
  startFrame?: number;
}> = ({ sourceLabel, branches, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const width = 940;
  const height = 560;
  const startX = 120;
  const startY = height / 2;

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        {branches.map((br, i) => {
          const endY = 95 + i * ((height - 190) / Math.max(1, branches.length - 1));
          const endX = 680;
          const drawPct = interpolate(rel, [i * 12, i * 12 + 36], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const particleT = ((rel * 0.018 + i * 0.27) % 1);
          const cx1 = startX + 200;
          const cx2 = endX - 200;
          const px =
            Math.pow(1 - particleT, 3) * startX +
            3 * Math.pow(1 - particleT, 2) * particleT * cx1 +
            3 * (1 - particleT) * Math.pow(particleT, 2) * cx2 +
            Math.pow(particleT, 3) * endX;
          const py =
            Math.pow(1 - particleT, 3) * startY +
            3 * Math.pow(1 - particleT, 2) * particleT * startY +
            3 * (1 - particleT) * Math.pow(particleT, 2) * endY +
            Math.pow(particleT, 3) * endY;

          return (
            <g key={i} opacity={drawPct}>
              <path
                d={`M ${startX} ${startY} C ${cx1} ${startY}, ${cx2} ${endY}, ${endX} ${endY}`}
                fill="none"
                stroke={br.color}
                strokeWidth={Math.max(6, br.percent * 0.45)}
                strokeOpacity={0.35}
                strokeLinecap="round"
              />
              <circle cx={px} cy={py} r={8} fill="#FFFFFF" />
              <text
                x={endX + 20}
                y={endY - 6}
                fill={br.color}
                fontSize={34}
                fontWeight={900}
                fontFamily="'KanitBlack', sans-serif"
              >
                {br.percent}%
              </text>
              <text
                x={endX + 20}
                y={endY + 26}
                fill="#E2E8F0"
                fontSize={24}
                fontWeight={700}
                fontFamily="'BeVietnamProExtraBold', sans-serif"
              >
                {br.label}
              </text>
            </g>
          );
        })}
        <circle cx={startX} cy={startY} r={54} fill="#0F172A" stroke="#42B2F2" strokeWidth={5} />
        <text
          x={startX}
          y={startY + 8}
          textAnchor="middle"
          fill="#FFFFFF"
          fontSize={26}
          fontWeight={900}
          fontFamily="'BeVietnamProBlack', sans-serif"
        >
          {sourceLabel}
        </text>
      </svg>
    </div>
  );
};

export const DecisionBranchPulse: React.FC<{
  rootLabel: string;
  winLabel: string;
  loseLabel: string;
  startFrame?: number;
}> = ({ rootLabel, winLabel, loseLabel, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const t = Math.min(1, rel / 40);
  const pulseY = interpolate(t, [0, 1], [80, 290]);
  const splitProgress = Math.max(0, Math.min(1, (rel - 24) / 30));

  return (
    <svg width={900} height={460} viewBox="0 0 900 460">
      <line x1={450} y1={80} x2={450} y2={220} stroke="#38BDF8" strokeWidth={6} />
      <path d="M 450 220 Q 320 260 220 340" fill="none" stroke="#EF4444" strokeWidth={6} strokeOpacity={0.3 + 0.7 * splitProgress} />
      <path d="M 450 220 Q 580 260 680 340" fill="none" stroke="#64748B" strokeWidth={4} strokeOpacity={0.45} />
      {t < 1 && <circle cx={450} cy={pulseY} r={12} fill="#FACC15" />}
      <rect x={310} y={24} width={280} height={60} rx={30} fill="#0F172A" stroke="#38BDF8" strokeWidth={3} />
      <text x={450} y={63} textAnchor="middle" fill="#FFFFFF" fontSize={26} fontWeight={800}>
        {rootLabel}
      </text>
      <text x={220} y={395} textAnchor="middle" fill="#F87171" fontSize={30} fontWeight={900}>
        {winLabel}
      </text>
      <text x={680} y={395} textAnchor="middle" fill="#94A3B8" fontSize={26} fontWeight={700}>
        {loseLabel}
      </text>
    </svg>
  );
};
