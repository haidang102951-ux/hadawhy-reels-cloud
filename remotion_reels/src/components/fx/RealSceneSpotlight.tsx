import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface SceneCameraWaypoint {
  frame: number;
  scale: number;
  x: number; // px shift
  y: number; // px shift
}

export interface PopSubject3D {
  src: string;
  appearFrame: number;
  x: number; // % or px inside stage (0..1080)
  y: number; // px inside stage
  width: number;
  rotateDeg?: number;
  glowColor?: string;
}

/**
 * RealSceneCameraStage — Lấy ẢNH THẬT / TÀI LIỆU THẬT làm nhân vật chính toàn khung sân khấu,
 * camera bay mượt qua các điểm focus (không bao giờ đứng im) + vật thể thật tách nền 3D bật ra từng nhịp.
 */
export const RealSceneCameraStage: React.FC<{
  bgSrc: string;
  waypoints?: SceneCameraWaypoint[];
  subjects?: PopSubject3D[];
  durationFrames?: number;
  bgBrightness?: number;
  children?: React.ReactNode;
}> = ({
  bgSrc,
  waypoints,
  subjects = [],
  durationFrames = 360,
  bgBrightness = 0.88,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pts: SceneCameraWaypoint[] =
    waypoints && waypoints.length >= 2
      ? waypoints
      : [
          { frame: 0, scale: 1.04, x: -24, y: 12 },
          { frame: Math.round(durationFrames * 0.5), scale: 1.14, x: 18, y: -10 },
          { frame: durationFrames, scale: 1.22, x: -12, y: 6 },
        ];

  const inputFrames = pts.map((p) => p.frame);
  const camScale = interpolate(frame, inputFrames, pts.map((p) => p.scale), {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const camX = interpolate(frame, inputFrames, pts.map((p) => p.x), {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const camY = interpolate(frame, inputFrames, pts.map((p) => p.y), {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div style={{ position: "relative", width: "100%", height: "100%", overflow: "hidden", borderRadius: 24 }}>
      <Img
        src={staticFile(bgSrc)}
        style={{
          position: "absolute",
          inset: -40,
          width: "calc(100% + 80px)",
          height: "calc(100% + 80px)",
          objectFit: "cover",
          transform: `translate3d(${camX.toFixed(1)}px, ${camY.toFixed(1)}px, 0) scale(${camScale.toFixed(3)})`,
          filter: `brightness(${bgBrightness}) contrast(1.06)`,
        }}
      />

      {subjects.map((sub, idx) => {
        if (frame < sub.appearFrame) return null;
        const rel = frame - sub.appearFrame;
        const pop = spring({
          frame: rel,
          fps,
          config: { damping: 14, stiffness: 185, mass: 0.72 },
        });
        const floatY = Math.sin(rel * 0.06 + idx) * 7;
        const glow = sub.glowColor ?? "#F59E0B";
        return (
          <div
            key={idx}
            style={{
              position: "absolute",
              left: sub.x,
              top: sub.y,
              width: sub.width,
              transform: `translate(-50%, -50%) translateY(${floatY.toFixed(1)}px) scale(${pop.toFixed(3)}) rotate(${sub.rotateDeg ?? 0}deg)`,
              filter: `drop-shadow(0 18px 30px rgba(0,0,0,0.82)) drop-shadow(0px 8px 16px rgba(0,0,0,0.85))`,
            }}
          >
            <Img src={staticFile(sub.src)} style={{ width: "100%", height: "auto", objectFit: "contain" }} />
          </div>
        );
      })}

      {children}
    </div>
  );
};

/**
 * EvidenceCalloutOverlay — Vẽ đường đứt nét phát sáng + tâm ngắm đỏ/vàng chỉ trực tiếp
 * vào chi tiết trên ảnh thật (chuẩn phong cách Bia Hơi 1986 & TIME 1997).
 */
export const EvidenceCalloutOverlay: React.FC<{
  targetX: number;
  targetY: number;
  labelX: number;
  labelY: number;
  label: string;
  metric?: string;
  startFrame?: number;
  color?: string;
}> = ({
  targetX,
  targetY,
  labelX,
  labelY,
  label,
  metric,
  startFrame = 0,
  color = "#FACC15",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const pop = spring({ frame: rel, fps, config: { damping: 15, stiffness: 200, mass: 0.65 } });
  const pulse = 1 + Math.sin(rel * 0.18) * 0.18;

  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      <svg width="100%" height="100%" style={{ position: "absolute", inset: 0, overflow: "visible" }}>
        <line
          x1={labelX}
          y1={labelY}
          x2={targetX}
          y2={targetY}
          stroke={color}
          strokeWidth={4}
          strokeDasharray="10 7"
          strokeDashoffset={-rel * 1.8}
          opacity={pop}
        />
        <circle cx={targetX} cy={targetY} r={10 * pulse} fill={color} opacity={pop} />
        <circle cx={targetX} cy={targetY} r={22 * pulse} fill="none" stroke={color} strokeWidth={3.5} opacity={pop * 0.7} />
      </svg>
      <div
        style={{
          position: "absolute",
          left: labelX,
          top: labelY,
          transform: `translate(-50%, -100%) scale(${pop.toFixed(3)})`,
          textAlign: "center",
        }}
      >
        {metric && (
          <div
            style={{
              fontFamily: "'KanitBlack', sans-serif",
              fontSize: 44,
              color,
              lineHeight: 1.0,
              WebkitTextStroke: "2px rgba(0,0,0,0.92)",
              textShadow: "0 6px 16px rgba(0,0,0,0.95)",
              whiteSpace: "nowrap",
            }}
          >
            {metric}
          </div>
        )}
        <div
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: 28,
            color: "#FFFFFF",
            WebkitTextStroke: "1.5px rgba(0,0,0,0.9)",
            textShadow: "0 4px 12px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {label}
        </div>
      </div>
    </div>
  );
};

/**
 * FactPunchlineCard — Câu chốt kiến thức ngắn gọn ở đáy màn hình (thay thế hoàn toàn phụ đề chạy từng chữ).
 */
export const FactPunchlineCard: React.FC<{
  headline: string;
  subline?: string;
  startFrame?: number;
  accentColor?: string;
}> = ({ headline, subline, startFrame = 0, accentColor = "#FACC15" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (frame < startFrame) return null;
  const rel = frame - startFrame;
  const pop = spring({ frame: rel, fps, config: { damping: 16, stiffness: 210, mass: 0.7 } });

  return (
    <div
      style={{
        position: "absolute",
        left: 56,
        right: 56,
        bottom: 245,
        textAlign: "center",
        opacity: pop,
        transform: `translateY(${interpolate(pop, [0, 1], [28, 0]).toFixed(1)}px) scale(${interpolate(pop, [0, 1], [0.92, 1]).toFixed(3)})`,
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          fontFamily: "'BeVietnamProBlack', sans-serif",
          fontSize: 44,
          color: accentColor,
          lineHeight: 1.15,
          WebkitTextStroke: "2px rgba(0,0,0,0.92)",
          textShadow: "0 6px 20px rgba(0,0,0,0.95)",
        }}
      >
        {headline}
      </div>
      {subline && (
        <div
          style={{
            marginTop: 6,
            fontFamily: "'BeVietnamProExtraBold', sans-serif",
            fontSize: 28,
            color: "#FFFFFF",
            WebkitTextStroke: "1.5px rgba(0,0,0,0.88)",
            textShadow: "0 4px 14px rgba(0,0,0,0.95)",
          }}
        >
          {subline}
        </div>
      )}
    </div>
  );
};
