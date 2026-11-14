import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import {
  EURASIA_BG_PATHS,
  HANOI_COORD,
  LONDON_COORD,
  MAP_HEIGHT,
  MAP_WIDTH,
  UK_PATHS,
  VIETNAM_PATHS,
} from "./eurasiaGeoPaths";
import { StickerPop } from "./StickerPop";

export interface GeoStrategicMap3DProps {
  startFrame: number;
  endFrame: number;
  originLabel: string;
  targetLabel: string;
  originCoord?: { x: number; y: number };
  targetCoord?: { x: number; y: number };
  originPaths?: string[];
  targetPaths?: string[];
  bgPaths?: string[];
  containerLeft?: number;
  containerTop?: number;
  containerWidth?: number;
  containerHeight?: number;
  originLabelPos?: { x: number; y: number };
  targetLabelPos?: { x: number; y: number };
  evidenceImageSrc?: string;
  evidenceTitle?: string;
  evidenceCenterX?: number;
  evidenceTop?: number;
  evidenceWidth?: number;
  evidenceHeight?: number;
  evidenceObjectPosition?: string;
  evidenceTitleFontSize?: number;
  leftFloatingIconSrc?: string;
  rightFloatingIconSrc?: string;
  leftFloatingIconPos?: { x: number; y: number; width?: number };
  rightFloatingIconPos?: { x: number; y: number; width?: number };
}

export const GeoStrategicMap3D: React.FC<GeoStrategicMap3DProps> = ({
  startFrame,
  endFrame,
  originLabel,
  targetLabel,
  originCoord = HANOI_COORD,
  targetCoord = LONDON_COORD,
  originPaths = VIETNAM_PATHS,
  targetPaths = UK_PATHS,
  bgPaths = EURASIA_BG_PATHS,
  containerLeft = 40,
  containerTop = 315,
  containerWidth = 1000,
  containerHeight = 640,
  originLabelPos,
  targetLabelPos,
  evidenceImageSrc,
  evidenceTitle,
  evidenceCenterX = 540,
  evidenceTop = 1355,
  evidenceWidth = 820,
  evidenceHeight = 450,
  evidenceObjectPosition = "center center",
  evidenceTitleFontSize = 44,
  leftFloatingIconSrc,
  rightFloatingIconSrc,
  leftFloatingIconPos,
  rightFloatingIconPos,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (frame < startFrame || frame > endFrame) {
    return null;
  }

  const localFrame = frame - startFrame;
  const enterPop = spring({
    frame: localFrame,
    fps,
    config: { damping: 15, stiffness: 95 },
  });

  const exitOpacity = interpolate(frame, [endFrame - 14, endFrame], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const arcProgress = interpolate(localFrame, [28, 125], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const ctrlX = (originCoord.x + targetCoord.x) * 0.5 + 40;
  const ctrlY = Math.min(originCoord.y, targetCoord.y) - 185;

  const arcPathD = `M ${originCoord.x} ${originCoord.y} Q ${ctrlX} ${ctrlY} ${targetCoord.x} ${targetCoord.y}`;

  const t = arcProgress;
  const u = 1 - t;
  const headX = u * u * originCoord.x + 2 * u * t * ctrlX + t * t * targetCoord.x;
  const headY = u * u * originCoord.y + 2 * u * t * ctrlY + t * t * targetCoord.y;

  const mapTiltX = interpolate(localFrame, [0, 260], [32, 22], {
    extrapolateRight: "clamp",
  });
  const mapScale = interpolate(enterPop, [0, 1], [0.84, 1.0]);

  const courtPop = spring({
    frame: Math.max(0, localFrame - 95),
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  return (
    <div
      style={{
        position: "absolute",
        inset: 0,
        opacity: exitOpacity,
      }}
    >
      <div
        style={{
          position: "absolute",
          left: containerLeft,
          top: containerTop,
          width: containerWidth,
          height: containerHeight,
          perspective: 1200,
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            transform: `scale(${mapScale}) rotateX(${mapTiltX}deg)`,
            transformStyle: "preserve-3d",
            borderRadius: 28,
            background:
              "radial-gradient(circle at 50% 45%, rgba(16, 36, 68, 0.85) 0%, rgba(6, 12, 24, 0.95) 100%)",
            border: "2px solid rgba(100, 175, 255, 0.28)",
            boxShadow:
              "0 35px 70px rgba(0,0,0,0.92), inset 0 0 50px rgba(0, 180, 255, 0.14)",
            overflow: "hidden",
          }}
        >
          <svg
            width={MAP_WIDTH}
            height={MAP_HEIGHT}
            viewBox={`0 0 ${MAP_WIDTH} ${MAP_HEIGHT}`}
            style={{ width: "100%", height: "100%", display: "block" }}
          >
            {Array.from({ length: 10 }).map((_, i) => (
              <line
                key={`vx-${i}`}
                x1={i * 100}
                y1={0}
                x2={i * 100}
                y2={MAP_HEIGHT}
                stroke="rgba(100, 170, 255, 0.08)"
                strokeWidth={1}
              />
            ))}
            {Array.from({ length: 7 }).map((_, i) => (
              <line
                key={`hy-${i}`}
                x1={0}
                y1={i * 100}
                x2={MAP_WIDTH}
                y2={i * 100}
                stroke="rgba(100, 170, 255, 0.08)"
                strokeWidth={1}
              />
            ))}

            {bgPaths.map((d, idx) => (
              <path
                key={`bg-${idx}`}
                d={d}
                fill="rgba(30, 52, 88, 0.65)"
                stroke="rgba(110, 165, 230, 0.25)"
                strokeWidth={1.1}
              />
            ))}

            {originPaths.map((d, idx) => (
              <path
                key={`orig-${idx}`}
                d={d}
                fill="rgba(255, 230, 0, 0.78)"
                stroke="#FFFFFF"
                strokeWidth={2.5}
                style={{
                  filter: "drop-shadow(0px 0px 14px rgba(255, 230, 0, 0.95))",
                }}
              />
            ))}

            {targetPaths.map((d, idx) => (
              <path
                key={`targ-${idx}`}
                d={d}
                fill="rgba(255, 59, 71, 0.85)"
                stroke="#FFFFFF"
                strokeWidth={2.5}
                style={{
                  filter: "drop-shadow(0px 0px 16px rgba(255, 59, 71, 0.95))",
                }}
              />
            ))}

            <circle
              cx={originCoord.x}
              cy={originCoord.y}
              r={18 + ((localFrame * 0.8) % 36)}
              fill="none"
              stroke="#FFE600"
              strokeWidth={3}
              opacity={1 - ((localFrame * 0.8) % 36) / 36}
            />
            <circle
              cx={originCoord.x}
              cy={originCoord.y}
              r={9}
              fill="#FFE600"
              stroke="#FFFFFF"
              strokeWidth={3}
            />

            {arcProgress > 0.75 && (
              <>
                <circle
                  cx={targetCoord.x}
                  cy={targetCoord.y}
                  r={18 + ((localFrame * 1.1) % 44)}
                  fill="none"
                  stroke="#FF3B47"
                  strokeWidth={3.5}
                  opacity={1 - ((localFrame * 1.1) % 44) / 44}
                />
                <circle
                  cx={targetCoord.x}
                  cy={targetCoord.y}
                  r={10}
                  fill="#FF3B47"
                  stroke="#FFFFFF"
                  strokeWidth={3}
                />
              </>
            )}

            <path
              d={arcPathD}
              fill="none"
              stroke="rgba(255, 230, 0, 0.25)"
              strokeWidth={5}
              strokeDasharray="10 10"
            />
            <path
              d={arcPathD}
              fill="none"
              stroke="#FFE600"
              strokeWidth={6}
              strokeLinecap="round"
              pathLength={1}
              strokeDasharray={1}
              strokeDashoffset={1 - arcProgress}
              style={{
                filter: "drop-shadow(0px 0px 14px rgba(255, 230, 0, 0.95))",
              }}
            />

            {arcProgress > 0.02 && arcProgress < 0.99 && (
              <circle
                cx={headX}
                cy={headY}
                r={12}
                fill="#FFFFFF"
                stroke="#FF3B47"
                strokeWidth={5}
                style={{
                  filter: "drop-shadow(0px 0px 18px #FF3B47)",
                }}
              />
            )}
          </svg>
        </div>

        <div
          style={{
            position: "absolute",
            left: originLabelPos ? originLabelPos.x : Math.min(880, Math.max(120, originCoord.x - 35)),
            top: originLabelPos ? originLabelPos.y : Math.min(580, Math.max(60, originCoord.y + 18)),
            transform: "translate(-50%, -50%)",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 32,
            color: "#FFE600",
            WebkitTextStroke: "8px #05070C",
            paintOrder: "stroke fill",
            textShadow: "0 8px 18px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {originLabel}
        </div>

        <div
          style={{
            position: "absolute",
            left: targetLabelPos ? targetLabelPos.x : Math.min(880, Math.max(140, targetCoord.x + 60)),
            top: targetLabelPos ? targetLabelPos.y : Math.min(580, Math.max(60, targetCoord.y - 24)),
            transform: "translate(-50%, -50%)",
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 32,
            color: "#FFFFFF",
            WebkitTextStroke: "8px #05070C",
            paintOrder: "stroke fill",
            textShadow: "0 8px 18px rgba(0,0,0,0.95)",
            whiteSpace: "nowrap",
          }}
        >
          {targetLabel}
        </div>
      </div>

      {evidenceImageSrc && localFrame >= 85 && (
        <div
          style={{
            position: "absolute",
            left: evidenceCenterX,
            top: evidenceTop,
            width: evidenceWidth,
            transform: `translate(-50%, -50%) scale(${courtPop}) rotate(-1.5deg)`,
          }}
        >
          <div
            style={{
              borderRadius: 26,
              overflow: "hidden",
              border: "4px solid rgba(255, 255, 255, 0.92)",
              boxShadow:
                "0 28px 60px rgba(0,0,0,0.92), 0 0 38px rgba(255, 59, 71, 0.45)",
            }}
          >
            <Img
              src={staticFile(evidenceImageSrc)}
              style={{
                width: "100%",
                height: evidenceHeight,
                objectFit: "cover",
                objectPosition: evidenceObjectPosition,
                display: "block",
              }}
            />
          </div>

          {evidenceTitle && (
            <div
              style={{
                marginTop: 16,
                textAlign: "center",
                fontFamily: "BeVietnamProBlack, sans-serif",
                fontSize: evidenceTitleFontSize,
                color: "#FFE600",
                WebkitTextStroke: "8px #05070C",
                paintOrder: "stroke fill",
                textShadow: "0 10px 24px rgba(0,0,0,0.95)",
                whiteSpace: "nowrap",
              }}
            >
              {evidenceTitle}
            </div>
          )}
        </div>
      )}

      {rightFloatingIconSrc && (
        <StickerPop
          src={rightFloatingIconSrc}
          x={rightFloatingIconPos?.x ?? 855}
          y={rightFloatingIconPos?.y ?? 1140}
          width={rightFloatingIconPos?.width ?? 235}
          startFrame={startFrame + 115}
          baseRotate={-18}
          floatSpeed={0.09}
          floatAmp={8}
          rimColor="rgba(255, 215, 0, 0.95)"
          shudderAtFrame={startFrame + 128}
        />
      )}

      {leftFloatingIconSrc && (
        <StickerPop
          src={leftFloatingIconSrc}
          x={leftFloatingIconPos?.x ?? 210}
          y={leftFloatingIconPos?.y ?? 1160}
          width={leftFloatingIconPos?.width ?? 205}
          startFrame={startFrame + 98}
          baseRotate={10}
          floatSpeed={0.08}
          floatAmp={7}
          rimColor="rgba(255, 80, 90, 0.95)"
        />
      )}
    </div>
  );
};
