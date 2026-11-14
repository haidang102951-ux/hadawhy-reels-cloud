import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

interface StickerPopProps {
  src: string;
  x: number;
  y: number;
  width: number;
  startFrame: number;
  floatSpeed?: number;
  floatAmp?: number;
  rotateAmp?: number;
  baseRotate?: number;
  rimColor?: string;
  showFloorShadow?: boolean;
  shudderAtFrame?: number;
  children?: React.ReactNode;
}

export const StickerPop: React.FC<StickerPopProps> = ({
  src,
  x,
  y,
  width,
  startFrame,
  floatSpeed = 0.06,
  floatAmp = 5,
  rotateAmp = 0.9,
  baseRotate = 0,
  rimColor = "rgba(255, 255, 255, 0.85)",
  showFloorShadow = true,
  shudderAtFrame,
  children,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame) {
    return null;
  }

  const localFrame = frame - startFrame;

  const pop = spring({
    frame: localFrame,
    fps,
    config: {
      damping: 16,
      stiffness: 210,
      mass: 0.9,
    },
  });

  // Subtle weighted studio float (not cartoon wobble)
  const floatY = Math.sin(localFrame * floatSpeed) * floatAmp;
  const floatRot = Math.cos(localFrame * (floatSpeed * 0.85)) * rotateAmp;

  // Optional impact shudder
  let shudderX = 0;
  let shudderRot = 0;
  if (shudderAtFrame !== undefined && frame >= shudderAtFrame && frame < shudderAtFrame + 16) {
    const sf = frame - shudderAtFrame;
    const decay = Math.exp(-sf * 0.22);
    shudderX = Math.sin(sf * 2.4) * 16 * decay;
    shudderRot = Math.cos(sf * 2.1) * 4 * decay;
  }

  const scale = interpolate(pop, [0, 1], [0.78, 1]);
  const entryY = interpolate(pop, [0, 1], [28, 0]);
  const opacity = interpolate(localFrame, [0, 5], [0, 1], { extrapolateRight: "clamp" });

  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y + entryY + floatY,
        width,
        transform: `translate(-50%, -50%) scale(${scale}) rotate(${baseRotate + floatRot + shudderRot}deg) translateX(${shudderX}px)`,
        opacity,
        pointerEvents: "none",
      }}
    >
      {showFloorShadow && (
        <div
          style={{
            position: "absolute",
            left: "12%",
            bottom: -24,
            width: "76%",
            height: 28,
            borderRadius: "50%",
            background: "radial-gradient(ellipse at center, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0) 72%)",
            transform: `scale(${interpolate(floatY, [-floatAmp, floatAmp], [0.88, 1.08])})`,
            filter: "blur(6px)",
          }}
        />
      )}
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "auto",
          display: "block",
          filter: `drop-shadow(0px 0px 3px ${rimColor}) drop-shadow(0px 16px 26px rgba(0, 0, 0, 0.82))`,
        }}
      />
      {children}
    </div>
  );
};
