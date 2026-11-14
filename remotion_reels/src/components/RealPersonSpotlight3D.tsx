import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";

export interface RealPersonSpotlight3DProps {
  startFrame: number;
  endFrame: number;
  /** Real background photo in public/ (e.g. "harvested/company_hq.png") */
  backdropSrc?: string;
  /** AI-cutout transparent PNG of the real person/product/vehicle in public/ */
  cutoutSrc: string;
  cutoutWidth?: number;
  centerX?: number;
  backdropWidth?: number;
  cutoutTop?: number;
  labelTop?: number;
  rimGlowColor?: string;
  subjectName: string;
  subjectSubtitle?: string;
  keyMetricValue?: string;
  keyMetricAccentColor?: string;
}

export const RealPersonSpotlight3D: React.FC<RealPersonSpotlight3DProps> = ({
  startFrame,
  endFrame,
  backdropSrc,
  cutoutSrc,
  cutoutWidth = 620,
  centerX = 540,
  backdropWidth = 860,
  cutoutTop = 1020,
  labelTop = 1520,
  rimGlowColor = "rgba(255,255,255,0.92)",
  subjectName,
  subjectSubtitle,
  keyMetricValue,
  keyMetricAccentColor = "#FFE600",
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

  const bgPop = spring({
    frame: localFrame,
    fps,
    config: { damping: 16, stiffness: 100 },
  });

  const cutoutPop = spring({
    frame: Math.max(0, localFrame - 10),
    fps,
    config: { damping: 12, stiffness: 170, mass: 0.8 },
  });

  const floatY = Math.sin(localFrame * 0.08) * 8;

  return (
    <div style={{ position: "absolute", inset: 0, opacity: exitOpacity }}>
      {/* Optional Tilted 3D Real Context Backdrop */}
      {backdropSrc && (
        <div
          style={{
            position: "absolute",
            left: centerX,
            top: 760,
            width: backdropWidth,
            height: 520,
            perspective: 1100,
            transform: `translate(-50%, -50%) scale(${bgPop})`,
          }}
        >
          <div
            style={{
              width: "100%",
              height: "100%",
              transform: "rotateX(8deg) rotateY(-6deg)",
              borderRadius: 28,
              overflow: "hidden",
              border: "3px solid rgba(255, 255, 255, 0.35)",
              boxShadow: "0 35px 70px rgba(0,0,0,0.92)",
            }}
          >
            <Img
              src={staticFile(backdropSrc)}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "brightness(0.68) contrast(1.12)",
              }}
            />
          </div>
        </div>
      )}

      {/* 3D Foreground Real Cutout Subject */}
      <div
        style={{
          position: "absolute",
          left: centerX,
          top: cutoutTop + floatY,
          width: cutoutWidth,
          transform: `translate(-50%, -50%) scale(${cutoutPop})`,
        }}
      >
        <Img
          src={staticFile(cutoutSrc)}
          style={{
            width: "100%",
            height: "auto",
            filter:
              `drop-shadow(0px 0px 6px ${rimGlowColor}) drop-shadow(0px 26px 40px rgba(0,0,0,0.92))`,
          }}
        />
      </div>

      {/* ZERO-BOX Subject Name & Key Metric below */}
      {localFrame >= 18 && (
        <div
          style={{
            position: "absolute",
            left: centerX,
            top: labelTop,
            transform: "translate(-50%, -50%)",
            textAlign: "center",
            whiteSpace: "nowrap",
          }}
        >
          {subjectSubtitle && (
            <div
              style={{
                fontFamily: "BeVietnamProExtraBold, sans-serif",
                fontSize: 30,
                color: "#FFFFFF",
                WebkitTextStroke: "6px #05070C",
                paintOrder: "stroke fill",
              }}
            >
              {subjectSubtitle}
            </div>
          )}
          <div
            style={{
              fontFamily: "BeVietnamProBlack, sans-serif",
              fontSize: 54,
              color: "#FFFFFF",
              WebkitTextStroke: "10px #05070C",
              paintOrder: "stroke fill",
              textShadow: "0 10px 24px rgba(0,0,0,0.95)",
            }}
          >
            {subjectName}
          </div>
          {keyMetricValue && (
            <div
              style={{
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: 72,
                color: keyMetricAccentColor,
                WebkitTextStroke: "11px #05070C",
                paintOrder: "stroke fill",
                textShadow: `0 0 32px ${keyMetricAccentColor}88`,
                marginTop: 4,
              }}
            >
              {keyMetricValue}
            </div>
          )}
        </div>
      )}
    </div>
  );
};
