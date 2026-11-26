import React from "react";
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from "remotion";
import { AE_SNAP_OUT, AE_WHIP_TRANSITION } from "./motionPresets";

/**
 * CameraStageWrapper: Bọc mỗi Beat tạo chuyển động 1 ống kính camera duy nhất (60fps AE):
 * - Vào cảnh: đẩy/trượt nhanh mượt 7 frames bằng AE_SNAP_OUT, giữ opacity: 1 (CẤM cross-fade mờ bóng ma).
 * - Giữa cảnh: trôi nhẹ scale 1.0 -> 1.018.
 * - Ra cảnh: đẩy nhẹ 6 frames cuối bằng AE_WHIP_TRANSITION tạo đà sang Beat tiếp theo.
 */
export const CameraStageWrapper: React.FC<{
  durationInFrames: number;
  enterDirection?: "up" | "left" | "right" | "zoom";
  children: React.ReactNode;
}> = ({ durationInFrames, enterDirection = "zoom", children }) => {
  const frame = useCurrentFrame();
  const enterDur = 7;
  const exitDur = 6;
  const exitStart = Math.max(enterDur + 1, durationInFrames - exitDur);

  const enterT = interpolate(frame, [0, enterDur], [0, 1], {
    easing: AE_SNAP_OUT,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const midScale = interpolate(frame, [enterDur, exitStart], [1.0, 1.018], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const exitT = interpolate(frame, [exitStart, durationInFrames], [0, 1], {
    easing: AE_WHIP_TRANSITION,
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  let tx = 0;
  let ty = 0;
  let enterScale = 1.0;
  if (enterDirection === "up") ty = (1 - enterT) * 44;
  else if (enterDirection === "left") tx = (1 - enterT) * 52;
  else if (enterDirection === "right") tx = -(1 - enterT) * 52;
  else enterScale = 0.955 + 0.045 * enterT;

  const finalScale = enterScale * midScale * (1 + exitT * 0.032);
  const exitY = -exitT * 18;

  return (
    <AbsoluteFill
      style={{
        opacity: 1,
        transform: `translate3d(${tx}px, ${ty + exitY}px, 0) scale(${finalScale})`,
        willChange: "transform",
      }}
    >
      {children}
    </AbsoluteFill>
  );
};

export interface ParallaxDepthStageProps {
  /** Tầng xa (trôi chậm 0.3x): chữ số khổng lồ chìm, bản đồ, kiến trúc xa */
  backLayer?: React.ReactNode;
  /** Tầng trung (trôi chuẩn 1.0x): sơ đồ, ảnh tư liệu chính */
  midLayer?: React.ReactNode;
  /** Tầng tiền cảnh (trôi nhanh 1.35x): HeroCutout3D hoặc SpeechPopCard25D */
  frontLayer?: React.ReactNode;
  /** Tương thích ngược: ảnh nền mờ + chủ thể */
  bgSrc?: string;
  subjectSrc?: string;
  bgBlur?: number;
  startFrame?: number;
  durationFrames?: number;
  /** Biên độ lia camera ngang/dọc (px) trong suốt Beat */
  panX?: number;
  panY?: number;
}

export const ParallaxDepthStage: React.FC<ParallaxDepthStageProps> = ({
  backLayer,
  midLayer,
  frontLayer,
  bgSrc,
  subjectSrc,
  bgBlur = 5,
  startFrame = 0,
  durationFrames = 240,
  panX = 44,
  panY = 14,
}) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const progress = interpolate(rel, [0, Math.max(1, durationFrames)], [-0.5, 0.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // 3 tốc độ chiều sâu 60fps: back 0.3x | mid 1.0x | front 1.35x
  const backX = -progress * panX * 0.3;
  const backY = -progress * panY * 0.3;
  const midX = -progress * panX * 1.0;
  const midY = -progress * panY * 1.0;
  const frontX = -progress * panX * 1.35;
  const frontY = -progress * panY * 1.35;

  const backScale = interpolate(rel, [0, Math.max(1, durationFrames)], [1.02, 1.06], { extrapolateRight: "clamp" });
  const midScale = interpolate(rel, [0, Math.max(1, durationFrames)], [1.0, 1.035], { extrapolateRight: "clamp" });
  const frontScale = interpolate(rel, [0, Math.max(1, durationFrames)], [0.99, 1.045], { extrapolateRight: "clamp" });

  return (
    <div style={{ position: "absolute", inset: 0, overflow: "hidden", perspective: "1100px" }}>
      {/* TẦNG 1 — BACK LAYER (0.3x) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${backX.toFixed(2)}px, ${backY.toFixed(2)}px, 0) scale(${backScale.toFixed(4)})`,
          willChange: "transform",
          zIndex: 10,
        }}
      >
        {backLayer}
        {!backLayer && bgSrc && (
          <Img
            src={staticFile(bgSrc)}
            style={{
              position: "absolute",
              inset: -30,
              width: "calc(100% + 60px)",
              height: "calc(100% + 60px)",
              objectFit: "cover",
              filter: `blur(${bgBlur}px) brightness(0.55)`,
            }}
          />
        )}
      </div>

      {/* TẦNG 2 — MID LAYER (1.0x) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${midX.toFixed(2)}px, ${midY.toFixed(2)}px, 0) scale(${midScale.toFixed(4)})`,
          willChange: "transform",
          zIndex: 20,
        }}
      >
        {midLayer}
      </div>

      {/* TẦNG 3 — FRONT LAYER (1.35x) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translate3d(${frontX.toFixed(2)}px, ${frontY.toFixed(2)}px, 0) scale(${frontScale.toFixed(4)})`,
          willChange: "transform",
          zIndex: 30,
        }}
      >
        {frontLayer}
        {!frontLayer && subjectSrc && (
          <div
            style={{
              position: "absolute",
              inset: 0,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Img
              src={staticFile(subjectSrc)}
              style={{
                maxWidth: "82%",
                maxHeight: "54%",
                objectFit: "contain",
                filter: "drop-shadow(0 28px 42px rgba(0,0,0,0.88))",
              }}
            />
          </div>
        )}
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
  const width = 900;
  const height = 560;
  const startX = 125;
  const startY = height / 2;

  const splitBranchLabel = (label: string): string[] => {
    if (label.length <= 14) return [label];
    const words = label.split(/\s+/);
    const lines: string[] = [];
    let cur = "";
    for (const w of words) {
      if ((cur + " " + w).trim().length > 14 && cur) {
        lines.push(cur);
        cur = w;
      } else {
        cur = (cur + " " + w).trim();
      }
    }
    if (cur) lines.push(cur);
    return lines.slice(0, 2);
  };

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        {branches.map((br, i) => {
          const endY = 95 + i * ((height - 190) / Math.max(1, branches.length - 1));
          const endX = 540;
          const drawPct = interpolate(rel, [i * 12, i * 12 + 36], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          });
          const particleT = ((rel * 0.018 + i * 0.27) % 1);
          const cx1 = startX + 170;
          const cx2 = endX - 160;
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

          const labelLines = splitBranchLabel(br.label);

          return (
            <g key={i} opacity={drawPct}>
              <path
                d={`M ${startX + 95} ${startY} C ${cx1 + 40} ${startY}, ${cx2} ${endY}, ${endX} ${endY}`}
                fill="none"
                stroke={br.color}
                strokeWidth={Math.max(6, br.percent * 0.45)}
                strokeOpacity={0.35}
                strokeLinecap="round"
              />
              <circle cx={px} cy={py} r={8} fill="#FFFFFF" />
              <text
                x={endX + 20}
                y={endY - 8}
                fill={br.color}
                fontSize={34}
                fontWeight={900}
                fontFamily="'BeVietnamProBlack', sans-serif"
              >
                {br.percent}%
              </text>
              {labelLines.map((line, li) => (
                <text
                  key={`bl-${li}`}
                  x={endX + 20}
                  y={endY + 22 + li * 26}
                  fill="#E2E8F0"
                  fontSize={22}
                  fontWeight={700}
                  fontFamily="'BeVietnamProExtraBold', sans-serif"
                >
                  {line}
                </text>
              ))}
            </g>
          );
        })}
        <rect
          x={startX - 105}
          y={startY - 32}
          width={210}
          height={64}
          rx={28}
          fill="#0F172A"
          stroke="#42B2F2"
          strokeWidth={4}
          style={{ filter: "drop-shadow(0 10px 22px rgba(0,0,0,0.88))" }}
        />
        <text
          x={startX}
          y={startY + 8}
          textAnchor="middle"
          fill="#FFFFFF"
          fontSize={22}
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

  // Continuous looping circuit pulse down the trunk & along winning Bezier M 450 220 Q 320 260 220 340
  const evalPulsePos = (phase: number) => {
    if (phase < 0.35) {
      const s = phase / 0.35;
      return { x: 450, y: 80 + 140 * s };
    }
    const u = (phase - 0.35) / 0.65;
    const inv = 1 - u;
    return {
      x: inv * inv * 450 + 2 * inv * u * 320 + u * u * 220,
      y: inv * inv * 220 + 2 * inv * u * 260 + u * u * 340,
    };
  };
  const loopT1 = (rel % 48) / 48;
  const loopT2 = ((rel + 24) % 48) / 48;
  const p1 = evalPulsePos(loopT1);
  const p2 = evalPulsePos(loopT2);

  const rootPulseScale = 1 + Math.sin(rel * 0.12) * 0.022;
  const winPulseScale = 1 + Math.sin(rel * 0.16) * 0.03;
  const winGlowOpacity = 0.55 + Math.sin(rel * 0.16) * 0.35;

  return (
    <div style={{ width: "100%", display: "flex", justifyContent: "center" }}>
      <svg
        width={900}
        height={460}
        viewBox="0 0 900 460"
        style={{ fontFamily: "'BeVietnamProBlack', sans-serif", overflow: "visible" }}
      >
      <line x1={450} y1={80} x2={450} y2={220} stroke="#38BDF8" strokeWidth={6} />
      <line
        x1={450}
        y1={80}
        x2={450}
        y2={220}
        stroke="#BAE6FD"
        strokeWidth={3}
        strokeDasharray="10 14"
        strokeDashoffset={-rel * 2.2}
        opacity={0.75}
      />
      <path d="M 450 220 Q 320 260 220 340" fill="none" stroke="#EF4444" strokeWidth={6} strokeOpacity={0.35 + 0.65 * splitProgress} />
      <path
        d="M 450 220 Q 320 260 220 340"
        fill="none"
        stroke="#FCA5A5"
        strokeWidth={3}
        strokeDasharray="12 16"
        strokeDashoffset={-rel * 2.4}
        strokeOpacity={0.4 + 0.5 * splitProgress}
      />
      <path d="M 450 220 Q 580 260 680 340" fill="none" stroke="#64748B" strokeWidth={4} strokeOpacity={0.45} />

      {t < 1 && <circle cx={450} cy={pulseY} r={12} fill="#FACC15" />}

      {/* Looping bright signal pulses */}
      <circle cx={p1.x} cy={p1.y} r={16} fill="#FACC15" opacity={0.28} />
      <circle cx={p1.x} cy={p1.y} r={8} fill="#FEF08A" opacity={0.95} />
      <circle cx={p2.x} cy={p2.y} r={13} fill="#EF4444" opacity={0.28 * splitProgress} />
      <circle cx={p2.x} cy={p2.y} r={6} fill="#FFFFFF" opacity={0.85 * splitProgress} />

      <g transform={`translate(450, 54) scale(${rootPulseScale}) translate(-450, -54)`}>
        <rect
          x={230}
          y={24}
          width={440}
          height={60}
          rx={30}
          fill="#0F172A"
          stroke="#38BDF8"
          strokeWidth={3 + Math.sin(rel * 0.14) * 0.8}
        />
        <text x={450} y={63} textAnchor="middle" fill="#FFFFFF" fontSize={26} fontWeight={900} fontFamily="'BeVietnamProBlack', sans-serif">
          {rootLabel}
        </text>
      </g>

      <g transform={`translate(225, 390) scale(${winPulseScale}) translate(-225, -390)`}>
        <text
          x={225}
          y={395}
          textAnchor="middle"
          fill="#F87171"
          fontSize={28}
          fontWeight={900}
          fontFamily="'BeVietnamProBlack', sans-serif"
          style={{ filter: "drop-shadow(0 8px 16px rgba(0,0,0,0.88))" }}
        >
          {winLabel}
        </text>
      </g>
      <text x={675} y={395} textAnchor="middle" fill="#94A3B8" fontSize={25} fontWeight={800} fontFamily="'BeVietnamProExtraBold', sans-serif">
        {loseLabel}
      </text>
      </svg>
    </div>
  );
};
