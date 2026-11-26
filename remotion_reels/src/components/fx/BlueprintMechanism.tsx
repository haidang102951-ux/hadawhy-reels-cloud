import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ensureFxFonts } from "./fxFonts";

ensureFxFonts();

export type BlueprintMode = "funnel" | "bottleneck" | "loop" | "lever";

export interface BlueprintMechanismProps {
  /** Chế độ bản vẽ cơ chế: phễu lọc | cổ chai | vòng lặp | đòn bẩy */
  mode: BlueprintMode;
  /** Nhãn đầu vào (2–3 từ) */
  inputLabel: string;
  /** Nhãn lõi cơ chế (2–3 từ) */
  coreLabel: string;
  /** Nhãn đầu ra (2–3 từ) */
  outputLabel: string;
  /** Ảnh vật thể thật ở đầu vào (tùy chọn) */
  inputImageSrc?: string;
  /** Ảnh vật thể thật ở đầu ra (tùy chọn) */
  outputImageSrc?: string;
  /** Frame kích hoạt nét vẽ cơ chế */
  triggerFrame?: number;
  top?: number;
  width?: number;
  height?: number;
}

const resolveAsset = (src: string): string =>
  /^(https?:|data:|\/)/i.test(src) ? src : staticFile(src);

/**
 * BlueprintMechanism — Bản vẽ cơ chế vận hành nét mảnh SVG trắng/xanh vẽ trực tiếp lên nền lưới xanh
 * (0 hộp nền), hỗ trợ funnel | bottleneck | loop | lever, gắn ảnh vật thể thật ở đầu vào và đầu ra.
 */
export const BlueprintMechanism: React.FC<BlueprintMechanismProps> = ({
  mode,
  inputLabel,
  coreLabel,
  outputLabel,
  inputImageSrc,
  outputImageSrc,
  triggerFrame = 10,
  top = 380,
  width = 960,
  height = 760,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const drawP = interpolate(frame, [triggerFrame, triggerFrame + 32], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const outPop = spring({
    frame: Math.max(0, frame - (triggerFrame + 22)),
    fps,
    config: { damping: 16, stiffness: 185, mass: 0.75 },
  });
  const dashTotal = 900;
  const dashOffset = dashTotal * (1 - drawP);

  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top,
        width,
        height,
        transform: "translate3d(-50%, 0, 0)",
        willChange: "transform",
      }}
    >
      {/* Nét vẽ kỹ thuật SVG trực tiếp lên nền lưới xanh (0 hộp nền) */}
      <svg
        width={width}
        height={height}
        viewBox="0 0 960 760"
        style={{ position: "absolute", inset: 0, overflow: "visible" }}
      >
        {mode === "funnel" && (
          <g fill="none" strokeLinecap="round" strokeLinejoin="round">
            <path
              d="M 180 180 L 780 180 L 560 440 L 560 600 L 400 600 L 400 440 Z"
              stroke="#E2E8F0"
              strokeWidth={3.5}
              strokeDasharray={dashTotal}
              strokeDashoffset={dashOffset}
            />
            <line
              x1={290}
              y1={310}
              x2={670}
              y2={310}
              stroke="#22B8FF"
              strokeWidth={2.5}
              strokeDasharray="10 8"
              opacity={drawP}
            />
            <path
              d="M 480 615 L 480 685 M 462 667 L 480 688 L 498 667"
              stroke="#22B8FF"
              strokeWidth={4}
              opacity={outPop}
            />
          </g>
        )}

        {mode === "bottleneck" && (
          <g fill="none" strokeLinecap="round" strokeLinejoin="round">
            <path
              d="M 110 230 L 370 230 L 445 340 L 515 340 L 590 230 L 850 230"
              stroke="#E2E8F0"
              strokeWidth={3.5}
              strokeDasharray={dashTotal}
              strokeDashoffset={dashOffset}
            />
            <path
              d="M 110 530 L 370 530 L 445 420 L 515 420 L 590 530 L 850 530"
              stroke="#E2E8F0"
              strokeWidth={3.5}
              strokeDasharray={dashTotal}
              strokeDashoffset={dashOffset}
            />
            <line
              x1={480}
              y1={280}
              x2={480}
              y2={480}
              stroke="#EF4444"
              strokeWidth={3}
              strokeDasharray="8 6"
              opacity={drawP}
            />
          </g>
        )}

        {mode === "loop" && (
          <g fill="none" strokeLinecap="round" strokeLinejoin="round">
            <circle
              cx={480}
              cy={380}
              r={215}
              stroke="#E2E8F0"
              strokeWidth={3.5}
              strokeDasharray={1360}
              strokeDashoffset={1360 * (1 - drawP)}
            />
            <circle
              cx={480}
              cy={380}
              r={165}
              stroke="#22B8FF"
              strokeWidth={2}
              strokeDasharray="10 10"
              opacity={drawP * 0.85}
            />
            {/* Mũi tên chiều vòng lặp */}
            <path
              d="M 675 340 L 695 380 L 660 398"
              stroke="#22B8FF"
              strokeWidth={4}
              opacity={drawP}
            />
            <path
              d="M 285 420 L 265 380 L 300 362"
              stroke="#22B8FF"
              strokeWidth={4}
              opacity={drawP}
            />
          </g>
        )}

        {mode === "lever" && (
          <g fill="none" strokeLinecap="round" strokeLinejoin="round">
            {/* Điểm tựa tam giác */}
            <path
              d="M 480 430 L 420 555 L 540 555 Z"
              stroke="#22B8FF"
              strokeWidth={3.5}
              opacity={drawP}
            />
            {/* Thanh đòn bẩy nghiêng */}
            <line
              x1={150}
              y1={495}
              x2={810}
              y2={355}
              stroke="#E2E8F0"
              strokeWidth={4.5}
              strokeDasharray={dashTotal}
              strokeDashoffset={dashOffset}
            />
            <circle cx={480} cy={425} r={10} fill="#22B8FF" opacity={drawP} />
          </g>
        )}
      </svg>

      {/* Ảnh vật thể thật & Nhãn ĐẦU VÀO */}
      <div
        style={{
          position: "absolute",
          left: mode === "funnel" ? "50%" : 120,
          top: mode === "funnel" ? 10 : 280,
          transform: mode === "funnel" ? "translate3d(-50%, 0, 0)" : "translate3d(0, 0, 0)",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 10,
        }}
      >
        {inputImageSrc && (
          <Img
            src={resolveAsset(inputImageSrc)}
            style={{
              width: 150,
              height: 150,
              objectFit: "contain",
              filter: "drop-shadow(0 12px 24px rgba(0,0,0,0.65))",
            }}
          />
        )}
        <span
          style={{
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 26,
            color: "#FFFFFF",
            whiteSpace: "nowrap",
            textShadow: "0 3px 10px rgba(0,0,0,0.85)",
          }}
        >
          {inputLabel}
        </span>
      </div>

      {/* Nhãn LÕI CƠ CHẾ */}
      <div
        style={{
          position: "absolute",
          left: "50%",
          top: mode === "funnel" ? 345 : 352,
          transform: "translate3d(-50%, 0, 0)",
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 30,
          color: "#22B8FF",
          whiteSpace: "nowrap",
          textShadow: "0 4px 12px rgba(0,0,0,0.9)",
          opacity: drawP,
        }}
      >
        {coreLabel}
      </div>

      {/* Ảnh vật thể thật & Nhãn ĐẦU RA */}
      <div
        style={{
          position: "absolute",
          left: mode === "funnel" ? "50%" : undefined,
          right: mode === "funnel" ? undefined : 110,
          top: mode === "funnel" ? 685 : 270,
          transform:
            mode === "funnel"
              ? `translate3d(-50%, 0, 0) scale(${(0.9 + outPop * 0.1).toFixed(3)})`
              : `scale(${(0.9 + outPop * 0.1).toFixed(3)})`,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 10,
          opacity: outPop,
        }}
      >
        {outputImageSrc && (
          <Img
            src={resolveAsset(outputImageSrc)}
            style={{
              width: 155,
              height: 155,
              objectFit: "contain",
              filter: "drop-shadow(0 12px 24px rgba(0,0,0,0.65))",
            }}
          />
        )}
        <span
          style={{
            fontFamily: "BeVietnamProBlack, sans-serif",
            fontSize: 28,
            color: "#FACC15",
            whiteSpace: "nowrap",
            textShadow: "0 3px 10px rgba(0,0,0,0.85)",
          }}
        >
          {outputLabel}
        </span>
      </div>
    </div>
  );
};
