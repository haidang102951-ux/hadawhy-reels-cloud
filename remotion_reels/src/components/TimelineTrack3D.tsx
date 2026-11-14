import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface TimelineMilestone {
  dateLabel: string;
  title: string;
  iconOrCutoutSrc: string;
  accentColor?: string;
  triggerOffsetFrames: number;
}

export interface TimelineTrack3DProps {
  startFrame: number;
  endFrame: number;
  milestones: TimelineMilestone[];
  centerX?: number;
  columnOffset?: number;
  startNodeY?: number;
  nodeStepY?: number;
  spineTop?: number;
  spineMaxHeight?: number;
  spineColors?: [string, string];
}

export const TimelineTrack3D: React.FC<TimelineTrack3DProps> = ({
  startFrame,
  endFrame,
  milestones,
  centerX = 540,
  columnOffset = 275,
  startNodeY = 470,
  nodeStepY = 360,
  spineTop = 410,
  spineMaxHeight = 1180,
  spineColors = ["#FFE600", "#FF3B47"],
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

  const lineProgress = interpolate(localFrame, [0, Math.max(30, endFrame - startFrame - 30)], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ position: "absolute", inset: 0, opacity: exitOpacity }}>
      {/* Central Glowing Vertical Timeline Spine */}
      <div
        style={{
          position: "absolute",
          left: centerX,
          top: spineTop,
          width: 8,
          height: spineMaxHeight * lineProgress,
          transform: "translateX(-50%)",
          background: `linear-gradient(180deg, ${spineColors[0]} 0%, ${spineColors[1]} 100%)`,
          boxShadow: `0 0 24px ${spineColors[0]}CC`,
          borderRadius: 4,
        }}
      />

      {milestones.map((m, idx) => {
        if (localFrame < m.triggerOffsetFrames) return null;
        const mPop = spring({
          frame: localFrame - m.triggerOffsetFrames,
          fps,
          config: { damping: 12, stiffness: 190 },
        });
        const nodeY = startNodeY + idx * nodeStepY;
        const isLeft = idx % 2 === 0;
        const color = m.accentColor || "#FFE600";

        return (
          <div key={`ms-${idx}`}>
            {/* Glowing Node on Spine */}
            <div
              style={{
                position: "absolute",
                left: centerX,
                top: nodeY,
                width: 30,
                height: 30,
                borderRadius: "50%",
                background: color,
                border: "5px solid #FFFFFF",
                boxShadow: `0 0 24px ${color}`,
                transform: `translate(-50%, -50%) scale(${mPop})`,
              }}
            />

            {/* Cutout / 3D Icon on one side */}
            <div
              style={{
                position: "absolute",
                left: isLeft ? centerX - columnOffset : centerX + columnOffset,
                top: nodeY,
                width: 220,
                transform: `translate(-50%, -50%) scale(${mPop})`,
              }}
            >
              <Img
                src={staticFile(m.iconOrCutoutSrc)}
                style={{
                  width: "100%",
                  height: "auto",
                  filter:
                    "drop-shadow(0px 0px 4px rgba(255,255,255,0.9)) drop-shadow(0px 18px 28px rgba(0,0,0,0.88))",
                }}
              />
            </div>

            {/* ZERO-BOX Date & Title on opposite side */}
            <div
              style={{
                position: "absolute",
                left: isLeft ? centerX + columnOffset : centerX - columnOffset,
                top: nodeY,
                transform: `translate(-50%, -50%) scale(${mPop})`,
                textAlign: "center",
                whiteSpace: "nowrap",
              }}
            >
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
                {m.dateLabel}
              </div>
              <div
                style={{
                  fontFamily: "BeVietnamProBlack, sans-serif",
                  fontSize: 33,
                  color: "#FFFFFF",
                  WebkitTextStroke: "8px #05070C",
                  paintOrder: "stroke fill",
                }}
              >
                {m.title}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};
