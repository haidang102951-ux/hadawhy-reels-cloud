import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface Point {
  x: number;
  y: number;
}

export interface CoinStreamProps {
  p0: Point;
  p1: Point;
  p2: Point;
  startFrame: number;
  endFrame?: number;
  coinCount?: number;
  blockedAtT?: number;
  dotColor?: string;
  useDollarNotes?: boolean;
  /** Custom primary item PNG in public/ (e.g. "objects/oil_barrel.png", "objects/chip.png", "harvested/item.png") */
  primaryItemSrc?: string;
  /** Custom secondary alternating item PNG in public/ */
  secondaryItemSrc?: string;
}

function quadBezier(p0: Point, p1: Point, p2: Point, t: number): Point {
  const u = 1 - t;
  return {
    x: u * u * p0.x + 2 * u * t * p1.x + t * t * p2.x,
    y: u * u * p0.y + 2 * u * t * p1.y + t * t * p2.y,
  };
}

export const CoinStream: React.FC<CoinStreamProps> = ({
  p0,
  p1,
  p2,
  startFrame,
  endFrame = 9999,
  coinCount = 6,
  blockedAtT,
  dotColor = "#FFD600",
  useDollarNotes = false,
  primaryItemSrc = "",
  secondaryItemSrc = "",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const streamOpacity =
    endFrame < 9000
      ? interpolate(frame, [endFrame - 18, endFrame], [1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : 1;

  const localFrame = frame - startFrame;
  const drawProgress = spring({
    frame: localFrame,
    fps,
    config: { damping: 16, stiffness: 90 },
  });

  const totalDots = 16;
  const maxDotT = blockedAtT ? Math.min(drawProgress, blockedAtT) : drawProgress;
  const dots: React.ReactNode[] = [];

  for (let i = 0; i <= totalDots; i++) {
    const t = i / totalDots;
    if (t > maxDotT) continue;
    const pt = quadBezier(p0, p1, p2, t);
    const pulse = 0.75 + 0.25 * Math.sin(localFrame * 0.22 - i * 0.6);
    dots.push(
      <div
        key={`dot-${i}`}
        style={{
          position: "absolute",
          left: pt.x,
          top: pt.y,
          width: 12,
          height: 12,
          borderRadius: "50%",
          background: dotColor,
          boxShadow: "0 4px 10px rgba(0,0,0,0.8)",
          transform: `translate(-50%, -50%) scale(${pulse})`,
          opacity: 0.85,
        }}
      />
    );
  }

  const coins: React.ReactNode[] = [];
  if (frame <= endFrame) {
    const cycleFrames = 42;
    for (let c = 0; c < coinCount; c++) {
      const coinStart = c * 11;
      const cf = localFrame - coinStart;
      if (cf < 0) continue;

      const rawT = (cf % cycleFrames) / cycleFrames;
      const easedT = Math.pow(rawT, 1.35);

      if (blockedAtT !== undefined && easedT >= blockedAtT) {
        const overT = (easedT - blockedAtT) / (1 - blockedAtT);
        if (overT < 0.45) {
          const bp = quadBezier(p0, p1, p2, blockedAtT);
          const spreadX = (c % 2 === 0 ? 1 : -1) * overT * 65;
          const dropY = overT * 45;
          coins.push(
            <div
              key={`coin-blocked-${c}`}
              style={{
                position: "absolute",
                left: bp.x + spreadX,
                top: bp.y + dropY,
                width: 66,
                transform: `translate(-50%, -50%) scale(${1 - overT * 1.6}) rotate(${overT * 140}deg)`,
                opacity: Math.max(0, 1 - overT * 2.2),
                filter: "drop-shadow(0 8px 14px rgba(0,0,0,0.85))",
              }}
            >
              {primaryItemSrc ? <Img src={staticFile(primaryItemSrc)} style={{ width: "100%" }} /> : null}
            </div>
          );
        }
        continue;
      }

      const pt = quadBezier(p0, p1, p2, easedT);
      const scale = interpolate(easedT, [0, 0.15, 0.85, 1], [0.3, 1.08, 1.0, 0.45]);
      const rot = cf * 7 + c * 45;
      const useSecond = useDollarNotes && c % 2 === 1;

      coins.push(
        <div
          key={`coin-${c}`}
          style={{
            position: "absolute",
            left: pt.x,
            top: pt.y,
            width: useSecond ? 88 : 74,
            transform: `translate(-50%, -50%) scale(${scale}) rotate(${rot}deg)`,
            filter: "drop-shadow(0px 10px 18px rgba(0,0,0,0.85))",
          }}
        >
          {(() => {
            const itemSrc = useSecond ? (secondaryItemSrc || primaryItemSrc) : primaryItemSrc;
            return itemSrc ? (
              <Img
                src={staticFile(itemSrc)}
                style={{ width: "100%", height: "auto" }}
              />
            ) : null;
          })()}
        </div>
      );
    }
  }

  let blockGate: React.ReactNode = null;
  if (blockedAtT !== undefined && drawProgress >= blockedAtT * 0.9) {
    const bp = quadBezier(p0, p1, p2, blockedAtT);
    const gatePop = spring({
      frame: Math.max(0, localFrame - 10),
      fps,
      config: { damping: 9, stiffness: 220 },
    });
    blockGate = (
      <div
        style={{
          position: "absolute",
          left: bp.x,
          top: bp.y,
          transform: `translate(-50%, -50%) scale(${gatePop})`,
          width: 68,
          height: 68,
          borderRadius: "50%",
          background: "radial-gradient(circle, rgba(255,30,60,0.95) 0%, rgba(160,0,25,0.95) 100%)",
          boxShadow: "0 10px 24px rgba(0,0,0,0.88)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          color: "#FFFFFF",
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 38,
          fontWeight: 900,
          border: "3px solid #FFF",
        }}
      >
        ✕
      </div>
    );
  }

  return (
    <div style={{ opacity: streamOpacity }}>
      {dots}
      {coins}
      {blockGate}
    </div>
  );
};
