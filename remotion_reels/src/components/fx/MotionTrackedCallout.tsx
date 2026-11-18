import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface TrackPoint {
  frame: number;
  x: number;
  y: number;
}

export const interpolateTrackPath = (points: TrackPoint[], frame: number): { x: number; y: number } => {
  if (!points || points.length === 0) return { x: 540, y: 960 };
  if (points.length === 1 || frame <= points[0].frame) return { x: points[0].x, y: points[0].y };
  const last = points[points.length - 1];
  if (frame >= last.frame) return { x: last.x, y: last.y };

  for (let i = 0; i < points.length - 1; i++) {
    const a = points[i];
    const b = points[i + 1];
    if (frame >= a.frame && frame <= b.frame) {
      const t = (frame - a.frame) / Math.max(1, b.frame - a.frame);
      return {
        x: a.x + (b.x - a.x) * t,
        y: a.y + (b.y - a.y) * t,
      };
    }
  }
  return { x: last.x, y: last.y };
};

export const MotionTrackedCallout: React.FC<{
  trackPoints: TrackPoint[];
  title: string;
  subtitle?: string;
  metricValue?: string;
  offsetX?: number;
  offsetY?: number;
  startFrame?: number;
  accentColor?: string;
}> = ({
  trackPoints,
  title,
  subtitle,
  metricValue,
  offsetX = 150,
  offsetY = -120,
  startFrame = 0,
  accentColor = "#42B2F2",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const pop = spring({
    frame: rel,
    fps,
    config: { damping: 15, stiffness: 190, mass: 0.7 },
  });

  const target = interpolateTrackPath(trackPoints, frame);
  const elbowX = target.x + offsetX * 0.45;
  const elbowY = target.y + offsetY;
  const endX = target.x + offsetX;
  const endY = target.y + offsetY;
  const lineDraw = interpolate(rel, [0, 12], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const pulse = 1 + Math.sin(rel * 0.22) * 0.18;

  return (
    <div style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
      <svg width={1080} height={1920} style={{ position: "absolute", inset: 0 }}>
        <circle
          cx={target.x}
          cy={target.y}
          r={10 * pulse}
          fill={accentColor}
          opacity={pop}
        />
        <circle
          cx={target.x}
          cy={target.y}
          r={22 * pulse}
          fill="none"
          stroke={accentColor}
          strokeWidth={3}
          opacity={pop * 0.65}
        />
        <polyline
          points={`${target.x},${target.y} ${elbowX},${elbowY} ${endX},${endY}`}
          fill="none"
          stroke={accentColor}
          strokeWidth={4}
          strokeDasharray={360}
          strokeDashoffset={360 * (1 - lineDraw)}
          strokeLinecap="round"
        />
      </svg>

      <div
        style={{
          position: "absolute",
          left: endX + (offsetX >= 0 ? 12 : -12),
          top: endY,
          transform: `translate(${offsetX >= 0 ? "0%" : "-100%"}, -55%) scale(${interpolate(pop, [0, 1], [0.75, 1])})`,
          opacity: pop,
          display: "flex",
          flexDirection: "column",
          alignItems: offsetX >= 0 ? "flex-start" : "flex-end",
        }}
      >
        {metricValue && (
          <div
            style={{
              fontFamily: "'KanitBlack', sans-serif",
              fontSize: 52,
              fontWeight: 900,
              color: accentColor,
              lineHeight: 1.0,
              WebkitTextStroke: "2px rgba(0,0,0,0.9)",
              textShadow: "0 6px 20px rgba(0,0,0,0.95)",
            }}
          >
            {metricValue}
          </div>
        )}
        <div
          style={{
            fontFamily: "'BeVietnamProBlack', sans-serif",
            fontSize: 32,
            fontWeight: 900,
            color: "#FFFFFF",
            WebkitTextStroke: "1.5px rgba(0,0,0,0.88)",
            textShadow: "0 4px 16px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {title}
        </div>
        {subtitle && (
          <div
            style={{
              fontFamily: "'BeVietnamProExtraBold', sans-serif",
              fontSize: 23,
              fontWeight: 700,
              color: "#CBD5E1",
              textShadow: "0 3px 12px rgba(0,0,0,0.95)",
              whiteSpace: "nowrap",
            }}
          >
            {subtitle}
          </div>
        )}
      </div>
    </div>
  );
};
