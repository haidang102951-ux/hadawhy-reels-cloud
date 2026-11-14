import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface CalloutNode {
  /** Anchor point on the central object (canvas coordinates) */
  anchorX: number;
  anchorY: number;
  /** Label endpoint (canvas coordinates) */
  labelX: number;
  labelY: number;
  title: string;
  value: string;
  accentColor?: string;
  delayFrames?: number;
}

export interface AnatomyCallout3DProps {
  startFrame: number;
  endFrame: number;
  centerCutoutSrc: string;
  centerX?: number;
  centerY?: number;
  centerWidth?: number;
  callouts: CalloutNode[];
}

export const AnatomyCallout3D: React.FC<AnatomyCallout3DProps> = ({
  startFrame,
  endFrame,
  centerCutoutSrc,
  centerX = 540,
  centerY = 1040,
  centerWidth = 520,
  callouts,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;
  const exitOpacity = interpolate(frame, [endFrame - 14, endFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const centerPop = spring({
    frame: localFrame,
    fps,
    config: { damping: 12, stiffness: 160 },
  });
  const floatY = Math.sin(localFrame * 0.08) * 8;

  return (
    <div style={{ position: "absolute", inset: 0, opacity: exitOpacity }}>
      {/* Central Cutout Object */}
      <div
        style={{
          position: "absolute",
          left: centerX,
          top: centerY + floatY,
          width: centerWidth,
          transform: `translate(-50%, -50%) scale(${centerPop})`,
        }}
      >
        <Img
          src={staticFile(centerCutoutSrc)}
          style={{
            width: "100%",
            height: "auto",
            filter:
              "drop-shadow(0px 0px 6px rgba(255,255,255,0.92)) drop-shadow(0px 24px 36px rgba(0,0,0,0.9))",
          }}
        />
      </div>

      {/* SVG AR Pointer Lines */}
      <svg
        width={1080}
        height={1920}
        style={{ position: "absolute", inset: 0, pointerEvents: "none" }}
      >
        {callouts.map((c, idx) => {
          const dFrame = c.delayFrames ?? 18 + idx * 16;
          if (localFrame < dFrame) return null;
          const lineProg = spring({
            frame: localFrame - dFrame,
            fps,
            config: { damping: 14, stiffness: 150 },
          });
          const color = c.accentColor || "#FFE600";
          const curX = interpolate(lineProg, [0, 1], [c.anchorX, c.labelX]);
          const curY = interpolate(lineProg, [0, 1], [c.anchorY, c.labelY]);
          return (
            <g key={`ar-line-${idx}`}>
              <circle cx={c.anchorX} cy={c.anchorY} r={8} fill={color} stroke="#FFF" strokeWidth={3} />
              <line
                x1={c.anchorX}
                y1={c.anchorY}
                x2={curX}
                y2={curY}
                stroke={color}
                strokeWidth={4}
                strokeDasharray="8 6"
              />
            </g>
          );
        })}
      </svg>

      {/* ZERO-BOX Floating AR Callout Labels */}
      {callouts.map((c, idx) => {
        const dFrame = (c.delayFrames ?? 18 + idx * 16) + 6;
        if (localFrame < dFrame) return null;
        const pop = spring({
          frame: localFrame - dFrame,
          fps,
          config: { damping: 12, stiffness: 200 },
        });
        const color = c.accentColor || "#FFE600";
        return (
          <div
            key={`ar-lbl-${idx}`}
            style={{
              position: "absolute",
              left: c.labelX,
              top: c.labelY,
              transform: `translate(-50%, -50%) scale(${pop})`,
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 28,
                color: "#FFFFFF",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              {c.title}
            </div>
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 52,
                color,
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: `0 0 24px ${color}88`,
              }}
            >
              {c.value}
            </div>
          </div>
        );
      })}
    </div>
  );
};
