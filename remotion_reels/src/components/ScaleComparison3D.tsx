import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface ScaleComparison3DProps {
  startFrame: number;
  endFrame: number;
  leftItemSrc: string;
  leftItemCount: number;
  leftLabel: string;
  rightPrimaryStackSrc?: string;
  rightSecondaryStackSrc?: string;
  rightTopTitle: string;
  rightStartNumber?: number;
  rightTargetNumber: number;
  rightUnitSuffix: string;
  rightLabel: string;
  stampText?: string;
}

export const ScaleComparison3D: React.FC<ScaleComparison3DProps> = ({
  startFrame,
  endFrame,
  leftItemSrc,
  leftItemCount,
  leftLabel,
  rightPrimaryStackSrc = "",
  rightSecondaryStackSrc = "",
  rightTopTitle,
  rightStartNumber = 0,
  rightTargetNumber,
  rightUnitSuffix,
  rightLabel,
  stampText,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;

  const towerGrow = spring({
    frame: Math.max(0, localFrame - 20),
    fps,
    config: { damping: 14, stiffness: 85, mass: 1.0 },
  });

  const counterProgress = interpolate(localFrame, [20, 150], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const currentVal = Math.round(
    interpolate(counterProgress, [0, 1], [rightStartNumber, rightTargetNumber])
  );

  const baselineY = 1380;
  const maxTowerHeight = 580;
  const currentTowerHeight = Math.max(20, maxTowerHeight * towerGrow);

  const stampFrame = 180;
  const showStamp = Boolean(stampText) && localFrame >= stampFrame;
  const stampPop = spring({
    frame: Math.max(0, localFrame - stampFrame),
    fps,
    config: { damping: 10, stiffness: 240, mass: 0.7 },
  });
  const stampScale = interpolate(stampPop, [0, 1], [2.2, 1.0]);

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <div
        style={{
          position: "absolute",
          left: 90,
          top: baselineY,
          width: 900,
          height: 8,
          borderRadius: 4,
          background:
            "linear-gradient(90deg, rgba(255,255,255,0.15) 0%, rgba(255,230,0,0.85) 50%, rgba(255,59,71,0.9) 100%)",
          boxShadow: "0 8px 20px rgba(0, 0, 0, 0.85)",
        }}
      />

      {Array.from({ length: leftItemCount }).map((_, idx) => {
        const pStart = 10 + idx * 11;
        if (localFrame < pStart) return null;
        const pPop = spring({
          frame: localFrame - pStart,
          fps,
          config: { damping: 11, stiffness: 200 },
        });
        const py = baselineY - 95 - idx * 125 + Math.sin((frame + idx * 15) * 0.09) * 5;
        return (
          <div
            key={`left-item-${idx}`}
            style={{
              position: "absolute",
              left: 285,
              top: py,
              width: 310,
              transform: `translate(-50%, -50%) scale(${pPop}) rotate(-4deg)`,
            }}
          >
            <Img
              src={staticFile(leftItemSrc)}
              style={{
                width: "100%",
                height: "auto",
                filter: "drop-shadow(0px 16px 24px rgba(0,0,0,0.88))",
              }}
            />
          </div>
        );
      })}

      {localFrame >= 15 && (
        <div
          style={{
            position: "absolute",
            left: 285,
            top: baselineY + 78,
            transform: "translate(-50%, -50%)",
            textAlign: "center",
            whiteSpace: "nowrap",
          }}
        >
          <div
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 44,
              color: "#FFFFFF",
              WebkitTextStroke: "9px #05070C",
              paintOrder: "stroke fill",
              textShadow: "0 8px 20px rgba(0,0,0,0.95)",
            }}
          >
            {leftLabel}
          </div>
        </div>
      )}

      {localFrame >= 92 && (
        <>
          <div
            style={{
              position: "absolute",
              left: 775,
              top: baselineY - currentTowerHeight,
              width: 210,
              height: currentTowerHeight,
              transform: "translateX(-50%)",
              borderRadius: "22px 22px 6px 6px",
              background:
                "linear-gradient(180deg, rgba(255, 59, 71, 0.96) 0%, rgba(190, 15, 35, 0.92) 65%, rgba(90, 5, 18, 0.95) 100%)",
              border: "3px solid rgba(255, 200, 180, 0.85)",
              boxShadow:
                "0 18px 36px rgba(0, 0, 0, 0.88), inset 0 12px 28px rgba(255, 255, 255, 0.25)",
            }}
          />

          {Array.from({ length: 8 }).map((_, sIdx) => {
            const threshold = (sIdx + 1) / 8;
            if (towerGrow < threshold * 0.85) return null;
            const sy = baselineY - 55 - sIdx * 78;
            const offsetX = (sIdx % 2 === 0 ? -1 : 1) * 18;
            const useSec = sIdx % 3 === 2;
            return (
              <div
                key={`stack-${sIdx}`}
                style={{
                  position: "absolute",
                  left: 775 + offsetX,
                  top: sy,
                  width: useSec ? 95 : 130,
                  transform: `translate(-50%, -50%) rotate(${sIdx % 2 === 0 ? -8 : 8}deg)`,
                  filter: "drop-shadow(0 12px 18px rgba(0,0,0,0.85))",
                }}
              >
                {(() => {
                  const stackSrc = useSec ? (rightSecondaryStackSrc || rightPrimaryStackSrc) : rightPrimaryStackSrc;
                  return stackSrc ? (
                    <Img
                      src={staticFile(stackSrc)}
                      style={{ width: "100%", height: "auto" }}
                    />
                  ) : null;
                })()}
              </div>
            );
          })}

          <div
            style={{
              position: "absolute",
              left: 775,
              top: baselineY - currentTowerHeight - 92,
              transform: "translate(-50%, -50%)",
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 30,
                color: "#FFFFFF",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              {rightTopTitle}
            </div>
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 82,
                color: "#FF3B47",
                WebkitTextStroke: "11px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 10px 26px rgba(0, 0, 0, 0.95)",
                lineHeight: 1.05,
                whiteSpace: "nowrap",
              }}
            >
              {currentVal}
              {rightUnitSuffix}
            </div>
          </div>

          <div
            style={{
              position: "absolute",
              left: 775,
              top: baselineY + 78,
              transform: "translate(-50%, -50%)",
              textAlign: "center",
              whiteSpace: "nowrap",
            }}
          >
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 38,
                color: "#FFE600",
                WebkitTextStroke: "9px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 8px 20px rgba(0,0,0,0.95)",
              }}
            >
              {rightLabel}
            </div>
          </div>
        </>
      )}

      {showStamp && (
        <div
          style={{
            position: "absolute",
            left: 265,
            top: 900,
            transform: `translate(-50%, -50%) scale(${stampScale}) rotate(-10deg)`,
            padding: "10px 30px",
            border: "7px solid #FF3B47",
            borderRadius: 12,
            background: "transparent",
            boxShadow: "0 12px 24px rgba(0, 0, 0, 0.85)",
            whiteSpace: "nowrap",
          }}
        >
          <div
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 42,
              color: "#FF3B47",
              letterSpacing: "0.04em",
              WebkitTextStroke: "6px #05070C",
              paintOrder: "stroke fill",
            }}
          >
            {stampText}
          </div>
        </div>
      )}
    </div>
  );
};
