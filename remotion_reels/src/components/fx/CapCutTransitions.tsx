import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export const WhipPanTransition: React.FC<{
  children: React.ReactNode;
  direction?: "left" | "right" | "up" | "down";
  durationFrames?: number;
  startFrame?: number;
}> = ({ children, direction = "left", durationFrames = 14, startFrame = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const progress = spring({
    frame: rel,
    fps,
    config: { damping: 18, stiffness: 210, mass: 0.7 },
    durationInFrames: durationFrames,
  });

  const dist = 1080;
  const x =
    direction === "left"
      ? interpolate(progress, [0, 1], [dist, 0])
      : direction === "right"
        ? interpolate(progress, [0, 1], [-dist, 0])
        : 0;
  const y =
    direction === "up"
      ? interpolate(progress, [0, 1], [dist, 0])
      : direction === "down"
        ? interpolate(progress, [0, 1], [-dist, 0])
        : 0;
  const blurPx = interpolate(progress, [0, 0.5, 1], [16, 6, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        transform: `translate3d(${x}px, ${y}px, 0) scale(${interpolate(progress, [0, 1], [1.06, 1])})`,
        filter: blurPx > 0.2 ? `blur(${blurPx.toFixed(1)}px)` : undefined,
      }}
    >
      {children}
    </div>
  );
};

export const ZoomThroughTransition: React.FC<{
  children: React.ReactNode;
  startFrame?: number;
  durationFrames?: number;
  initialScale?: number;
}> = ({ children, startFrame = 0, durationFrames = 16, initialScale = 1.65 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const p = spring({
    frame: rel,
    fps,
    config: { damping: 20, stiffness: 180, mass: 0.8 },
    durationInFrames: durationFrames,
  });
  const scale = interpolate(p, [0, 1], [initialScale, 1]);
  const opacity = interpolate(rel, [0, 5], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        opacity,
        transform: `scale(${scale})`,
        transformOrigin: "center center",
      }}
    >
      {children}
    </div>
  );
};

export const SplitCurtainWipe: React.FC<{
  children: React.ReactNode;
  startFrame?: number;
  durationFrames?: number;
}> = ({ children, startFrame = 0, durationFrames = 18 }) => {
  const frame = useCurrentFrame();
  const rel = Math.max(0, frame - startFrame);
  const insetPct = interpolate(rel, [0, durationFrames], [50, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        clipPath: `inset(0% ${insetPct}% 0% ${insetPct}%)`,
      }}
    >
      {children}
    </div>
  );
};

export const Tilt3DFlip: React.FC<{
  children: React.ReactNode;
  startFrame?: number;
  durationFrames?: number;
  axis?: "X" | "Y";
}> = ({ children, startFrame = 0, durationFrames = 18, axis = "Y" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const rel = Math.max(0, frame - startFrame);
  const p = spring({
    frame: rel,
    fps,
    config: { damping: 16, stiffness: 160, mass: 0.8 },
    durationInFrames: durationFrames,
  });
  const deg = interpolate(p, [0, 1], [75, 0]);
  const opacity = interpolate(rel, [0, 4], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        perspective: 1200,
        opacity,
        transform: `perspective(1200px) rotate${axis}(${deg}deg) scale(${interpolate(p, [0, 1], [0.9, 1])})`,
      }}
    >
      {children}
    </div>
  );
};
