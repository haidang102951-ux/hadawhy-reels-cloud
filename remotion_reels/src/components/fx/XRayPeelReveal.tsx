import React from "react";
import { Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { ensureFxFonts } from "./fxFonts";

ensureFxFonts();

export interface XRayPeelRevealProps {
  /** Ảnh bề nổi bên ngoài (trước khi quét) */
  outerImageSrc: string;
  /** Ảnh bản chất / cấu tạo bên trong (hiện ra sau đường quét) */
  innerImageSrc: string;
  /** Nhãn ngắn bên ngoài (2–3 từ) */
  outerLabel?: string;
  /** Nhãn ngắn bên trong (2–3 từ) */
  innerLabel?: string;
  /** Frame bắt đầu trượt đường quét ngang bóc lớp */
  revealFrame?: number;
  /** Thời lượng trượt quét (frames @ 60fps) */
  sweepDurationFrames?: number;
  top?: number;
  width?: number;
  height?: number;
}

const resolveAsset = (src: string): string =>
  /^(https?:|data:|\/)/i.test(src) ? src : staticFile(src);

/**
 * XRayPeelReveal — Chồng khít 2 ảnh thật (bề nổi bên ngoài vs. bản chất/cấu tạo bên trong),
 * đường quét mảnh trượt ngang theo revealFrame để bóc lớp trực quan. Không hộp nhựa, không neon.
 */
export const XRayPeelReveal: React.FC<XRayPeelRevealProps> = ({
  outerImageSrc,
  innerImageSrc,
  outerLabel = "BỀ NỔI",
  innerLabel = "BÊN TRONG",
  revealFrame = 24,
  sweepDurationFrames = 42,
  top = 380,
  width = 920,
  height = 760,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const enterP = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 170, mass: 0.75 },
  });
  const enterY = interpolate(enterP, [0, 1], [28, 0]);
  const enterOpacity = interpolate(frame, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Đường quét trượt ngang mượt từ 8% -> 86%
  const rawSweep = interpolate(
    frame,
    [revealFrame, revealFrame + sweepDurationFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  // Ease-in-out cubic
  const easedSweep =
    rawSweep < 0.5
      ? 4 * rawSweep * rawSweep * rawSweep
      : 1 - Math.pow(-2 * rawSweep + 2, 3) / 2;

  const revealPct = 10 + easedSweep * 78;

  return (
    <div
      style={{
        position: "absolute",
        left: "50%",
        top,
        width,
        height,
        opacity: enterOpacity,
        transform: `translate3d(-50%, ${enterY.toFixed(2)}px, 0)`,
        willChange: "transform, opacity",
        borderRadius: 10,
        overflow: "hidden",
        backgroundColor: "#061020",
        boxShadow: "0 24px 56px rgba(0, 0, 0, 0.72)",
        border: "1px solid rgba(255, 255, 255, 0.16)",
      }}
    >
      {/* Lớp 1: Ảnh bề nổi bên ngoài */}
      <div style={{ position: "absolute", inset: 0 }}>
        <Img
          src={resolveAsset(outerImageSrc)}
          style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }}
        />
      </div>

      {/* Lớp 2: Ảnh bản chất bên trong (bóc từ trái sang phải theo revealPct) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          clipPath: `inset(0 ${(100 - revealPct).toFixed(2)}% 0 0)`,
          backgroundColor: "#050B16",
        }}
      >
        <Img
          src={resolveAsset(innerImageSrc)}
          style={{ width: "100%", height: "100%", objectFit: "contain", display: "block" }}
        />
      </div>

      {/* Đường quét mảnh sắc nét chia 2 lớp */}
      <div
        style={{
          position: "absolute",
          top: 0,
          bottom: 0,
          left: `${revealPct.toFixed(2)}%`,
          width: 3,
          backgroundColor: "#FFFFFF",
          boxShadow: "0 0 12px rgba(0, 0, 0, 0.85)",
          transform: "translate3d(-50%, 0, 0)",
          zIndex: 10,
        }}
      />

      {/* Nhãn 2–3 từ góc dưới trái (Bản chất) và dưới phải (Bề nổi) */}
      <div
        style={{
          position: "absolute",
          left: 24,
          bottom: 24,
          backgroundColor: "rgba(5, 11, 22, 0.86)",
          border: "1px solid rgba(255, 255, 255, 0.25)",
          padding: "8px 16px",
          borderRadius: 6,
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 22,
          color: "#22B8FF",
          whiteSpace: "nowrap",
          zIndex: 12,
          opacity: interpolate(rawSweep, [0.05, 0.25], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
          }),
        }}
      >
        {innerLabel}
      </div>

      <div
        style={{
          position: "absolute",
          right: 24,
          bottom: 24,
          backgroundColor: "rgba(5, 11, 22, 0.86)",
          border: "1px solid rgba(255, 255, 255, 0.2)",
          padding: "8px 16px",
          borderRadius: 6,
          fontFamily: "BeVietnamProBlack, sans-serif",
          fontSize: 22,
          color: "#FFFFFF",
          whiteSpace: "nowrap",
          zIndex: 12,
        }}
      >
        {outerLabel}
      </div>
    </div>
  );
};
